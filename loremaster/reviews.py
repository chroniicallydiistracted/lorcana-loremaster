"""Apply reviewed values only when their input snapshot and evidence still match."""

import hashlib
import json
from datetime import date
from functools import lru_cache
from pathlib import Path

from loremaster.schemas import CardMechanics, ReviewLedger


def digest(path):
    path = Path(path)
    stat = path.stat()
    return _digest(str(path.resolve()), stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size)


@lru_cache(maxsize=4096)
def _digest(path, modified, changed, size):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def overlay(identities, root, as_of):
    path = root / "data/policy/card-text-reviews.json"
    if not path.exists():
        return identities, {"applied": 0, "unresolved": 0, "stale": []}
    data = json.loads(path.read_text())
    if data["schema_version"] == 1 and not data["records"]:
        return identities, {"applied": 0, "unresolved": 0, "stale": []}
    ledger = ReviewLedger.model_validate(data)
    when = date.fromisoformat(as_of)
    catalog_hash = digest(root / "data/raw/ravensburger/catalog.en.json")
    manifest_path = root / "sources/manifest.json"
    sources = (
        {s["source_id"]: s for s in json.loads(manifest_path.read_text())["sources"]}
        if manifest_path.exists()
        else {}
    )
    report = {"applied": 0, "unresolved": 0, "stale": []}
    records = {
        r.identity_id: r
        for r in ledger.records
        if r.effective_from <= when and (r.effective_until is None or when < r.effective_until)
    }
    output = []
    for original in identities:
        card = dict(original)
        record = records.get(card["identity_id"])
        if record:
            stale = record.catalog_sha256 != catalog_hash or any(
                not (root / e.path).is_file() or digest(root / e.path) != e.sha256 for e in record.evidence
            )
            stale = stale or any(
                e.source_id in sources and sources[e.source_id].get("sha256") != e.sha256
                for e in record.evidence
            )
            if stale:
                report["stale"].append(card["identity_id"])
                card["text_status"] = "requires_review"
            elif record.status == "resolved":
                if set(record.fields) != set(card["conflict_fields"]):
                    raise ValueError("Review fields differ from raw conflict fields: " + card["identity_id"])
                card.update(record.resolved_values)
                CardMechanics.model_validate({k: card[k] for k in CardMechanics.model_fields})
                card["full_name"] = card["name"] + (" - " + card["subtitle"] if card["subtitle"] else "")
                card["text_status"] = "reviewed_resolution"
                card["review"] = record.model_dump(mode="json")
                report["applied"] += 1
            else:
                card["review"] = record.model_dump(mode="json")
                report["unresolved"] += 1
        output.append(card)
    return output, report
