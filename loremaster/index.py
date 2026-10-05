"""Reproducible official evidence index. PDF extraction never becomes rules authority."""

import json
import os
import re
import sqlite3
import tempfile
import unicodedata
from datetime import date
from html.parser import HTMLParser

import pymupdf

from loremaster.reviews import digest
from loremaster.schemas import SourceRegistry


class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def clean(text):
    return unicodedata.normalize("NFKC", text).replace("\x00", "")


def pdf_text(page):
    # Verified against CR card-parts definitions and rendered keyword pages.
    # Translate only spans in the official symbol font, never ordinary punctuation.
    glyphs = {
        "!": "{E}",
        '"': "{I}",
        "#": "{W}",
        "$": "{S}",
        "%": "{L}",
        "&": "{INKABLE}",
        "'": "{MOVE_COST}",
    }
    lines = []
    for block in page.get_text("dict", sort=True)["blocks"]:
        for line in block.get("lines", []):
            parts = []
            for span in line["spans"]:
                value = span["text"]
                if span["font"] == "LorcanaCardGlyphsRegular":
                    value = "".join(glyphs.get(char, char) for char in value)
                parts.append(value)
            lines.append("".join(parts))
    return clean("\n".join(lines))


def chunks_for(source, root):
    path = root / source["path"]
    if digest(path) != source["sha256"]:
        raise ValueError("Source hash mismatch: " + source["source_id"])
    if path.suffix == ".pdf":
        with pymupdf.open(path) as doc:
            previous_section = None
            in_glossary = False
            for page_number, page in enumerate(doc, 1):
                text = pdf_text(page)
                if in_glossary:
                    yield page_number, None, text
                    continue
                glossary_text = None
                if source["source_id"] == "comprehensive-rules-2.2.0":
                    marker = re.search(r"(?m)^[ \t]*Glossary[ \t]*$", text)
                    if marker:
                        glossary_text = text[marker.start() :]
                        text = text[: marker.start()]
                        in_glossary = True
                # Numbered sections are anchored to actual line starts; no invented section IDs.
                pattern = r"(?m)^[ \t]*(\d+(?:\.\d+){1,5})\.?[ \t]+(?=[A-Za-z\"'“(])"
                matches = list(re.finditer(pattern, text))
                if (source["source_id"] == "comprehensive-rules-2.2.0" and page_number == 2) or (
                    source["source_id"] == "tournament-rules-2026-07-14" and page_number in {2, 3}
                ):
                    matches = []  # Contents pages are searchable but have no rule-section anchors.
                if matches:
                    if text[: matches[0].start()].strip():
                        yield page_number, previous_section, text[: matches[0].start()].strip()
                    for n, match in enumerate(matches):
                        end = matches[n + 1].start() if n + 1 < len(matches) else len(text)
                        yield page_number, match[1], text[match.start() : end].strip()
                    previous_section = matches[-1][1]
                elif text.strip():
                    yield page_number, previous_section, text.strip()
                if glossary_text:
                    yield page_number, None, glossary_text
                    previous_section = None
    elif path.suffix == ".html":
        parser = PageText()
        parser.feed(path.read_text())
        # Overlap preserves context across paragraph boundaries.
        parts = parser.parts
        for start in range(0, len(parts), 20):
            yield None, None, "\n".join(parts[max(0, start - 2) : start + 22])


def build_index(root):
    sources = json.loads((root / "sources/manifest.json").read_text())["sources"]
    SourceRegistry.model_validate({"sources": sources})
    target = root / "data/derived/evidence.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        from pathlib import Path

        stage = Path(temporary) / "evidence.sqlite"
        con = sqlite3.connect(stage)
        con.executescript("""
            CREATE TABLE chunks (id INTEGER PRIMARY KEY, source_id TEXT, page INTEGER,
                section TEXT, text TEXT, metadata TEXT);
            CREATE VIRTUAL TABLE evidence_fts USING fts5(text, content=chunks, content_rowid=id,
                tokenize='unicode61 remove_diacritics 2');
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT);
        """)
        count = 0
        for source in sources:
            if not source.get("path") or source["source_id"] == "ravensburger-catalog-en":
                continue
            for page, section, text in chunks_for(source, root):
                count += 1
                metadata = {
                    k: source.get(k)
                    for k in [
                        "source_id",
                        "url",
                        "path",
                        "sha256",
                        "version",
                        "effective_date",
                        "checked_at",
                        "published_date",
                        "language",
                        "authority",
                    ]
                }
                con.execute(
                    "INSERT INTO chunks VALUES (?,?,?,?,?,?)",
                    (count, source["source_id"], page, section, text, json.dumps(metadata)),
                )
                con.execute("INSERT INTO evidence_fts(rowid,text) VALUES (?,?)", (count, text))
        con.execute(
            "INSERT INTO metadata VALUES (?,?)", ("manifest_sha256", digest(root / "sources/manifest.json"))
        )
        con.commit()
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Evidence index integrity failure")
        con.close()
        os.replace(stage, target)
    return {"chunks": count, "sources": len(sources) - 1, "database": str(target.relative_to(root))}


def retrieve(root, query="", source_id=None, section=None, limit=8, as_of="2026-10-04"):
    date.fromisoformat(as_of)
    path = root / "data/derived/evidence.sqlite"
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        if con.execute("SELECT value FROM metadata WHERE key='manifest_sha256'").fetchone()[0] != digest(
            root / "sources/manifest.json"
        ):
            raise ValueError("Source registry changed; rebuild the evidence index")
        words = re.findall(r"[\w]+", clean(query))
        params = []
        filters = []
        sql = "SELECT chunks.* FROM chunks"
        if words:
            sql += " JOIN evidence_fts ON evidence_fts.rowid=chunks.id"
            filters.append("evidence_fts MATCH ?")
            params.append(" OR ".join('"' + word + '"' for word in words))
        if source_id:
            filters.append("source_id=?")
            params.append(source_id)
        if section:
            filters.append("section=?")
            params.append(section)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY " + ("bm25(evidence_fts), chunks.id" if words else "chunks.id")
        rows = con.execute(sql, params).fetchall()
        output = []
        hashes = {}
        for row in rows:
            _, sid, page, sec, text, metadata = row
            meta = json.loads(metadata)
            applicable_from = (
                meta.get("effective_date") or meta.get("published_date") or meta.get("checked_at")
            )
            if applicable_from and applicable_from > as_of:
                continue
            if meta["path"] not in hashes:
                hashes[meta["path"]] = digest(root / meta["path"])
            if hashes[meta["path"]] != meta["sha256"]:
                raise ValueError("Indexed source bytes changed: " + sid)
            output.append(
                {
                    "text": text,
                    "citation": {k: meta[k] for k in ["source_id", "sha256", "url", "path"]}
                    | {"page": page, "section": sec},
                    "version": meta.get("version"),
                    "effective_date": meta.get("effective_date"),
                    "checked_at": meta.get("checked_at"),
                    "future_date": bool(meta.get("checked_at") and as_of > meta["checked_at"]),
                    "extraction": "Search excerpt; original source controls symbols and layout",
                }
            )
            if len(output) >= limit:
                break
        return output
    finally:
        con.close()
