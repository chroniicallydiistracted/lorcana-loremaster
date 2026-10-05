"""Reviewed answers and evidence retrieval, without an unverified language-model step."""

import json
import re
from datetime import date

from loremaster.index import retrieve
from loremaster.reviews import digest
from loremaster.schemas import Fact


def question_key(query):
    return " ".join(re.findall(r"\w+", query.casefold()))


def facts(root):
    data = json.loads((root / "data/policy/answer-facts.json").read_text())
    records = [Fact.model_validate(r) for r in data["records"]]
    if len({r.fact_id for r in records}) != len(records):
        raise ValueError("Duplicate fact ID")
    return records


def answer(root, query="", topic=None, as_of="2026-10-04"):
    when = date.fromisoformat(as_of)
    found = (
        [r for r in facts(root) if r.fact_id == topic]
        if topic
        else [r for r in facts(root) if question_key(query) in {question_key(q) for q in r.questions}]
    )
    if len(found) != 1:
        return {
            "status": "needs_interpretation",
            "as_of": as_of,
            "answer": "No reviewed answer matches this question. Use the retrieved original sources to analyze the exact interaction; supply cards, mode, date and relevant game state.",
            "evidence": retrieve(root, query=query, as_of=as_of) if query else [],
            "citations": [],
        }
    fact = found[0]
    source_map = {
        s["source_id"]: s for s in json.loads((root / "sources/manifest.json").read_text())["sources"]
    }
    issues = []
    if when < fact.effective_from:
        issues.append("Requested date predates this reviewed answer; retrieve contemporary sources.")
    if when > fact.checked_at and fact.classification == "official_fact":
        issues.append(
            "Requested date is newer than verification; refresh official sources before asserting current policy."
        )
    for citation in fact.citations:
        if not (root / citation.path).is_file() or digest(root / citation.path) != citation.sha256:
            issues.append("Source changed or is missing: " + citation.source_id)
            continue
        source = source_map.get(citation.source_id)
        if source and (source.get("sha256") != citation.sha256 or source.get("path") != citation.path):
            issues.append("Newer source snapshot requires re-review: " + citation.source_id)
        if citation.section:
            evidence = retrieve(root, source_id=citation.source_id, section=citation.section, as_of=as_of)
            if not any(e["citation"]["page"] == citation.page for e in evidence):
                issues.append("Section/page citation does not resolve: " + citation.section)
    if issues:
        return {
            "status": "requires_review",
            "fact_id": fact.fact_id,
            "as_of": as_of,
            "answer": "This answer requires source or date review.",
            "review_required": issues,
            "citations": [c.model_dump() for c in fact.citations],
        }
    return {
        "status": "insufficient_evidence" if fact.classification == "insufficient_evidence" else "supported",
        "fact_id": fact.fact_id,
        "domain": fact.domain,
        "as_of": as_of,
        "checked_at": fact.checked_at.isoformat(),
        "effective_from": fact.effective_from.isoformat(),
        "classification": fact.classification,
        "region": fact.region,
        "answer": fact.answer,
        "citations": [c.model_dump() for c in fact.citations],
    }
