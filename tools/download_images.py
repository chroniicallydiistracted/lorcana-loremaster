#!/usr/bin/env python3
"""Download official conflict-printing and Set 14 base images with immutable hashes."""

import argparse
import hashlib
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lorcana import ROOT, read_json, read_jsonl, sha, user_today, write_json


def download(root=ROOT, workers=6):
    rows = read_jsonl(root / "data/derived/printings.jsonl")
    conflicts = read_json(root / "data/derived/conflicts.json")
    required = {p for group in conflicts for p in group["printing_ids"]}
    required.update(r["printing_id"] for r in rows if r["printed_set_number"] == 14 and r["is_base"])
    # One image per printing: foil mask downloads are unnecessary for functional text.
    tasks = []
    for row in rows:
        if row["printing_id"] not in required:
            continue
        urls = [v["detail_image_url"] for v in row["variants"] if v.get("detail_image_url")]
        if not urls:
            continue
        tasks.append((row, urls[0]))
    target = root / "sources/images"
    target.mkdir(parents=True, exist_ok=True)
    previous = read_json(target / "manifest.json") if (target / "manifest.json").exists() else {}
    cached = {r["url"]: r for r in previous.get("records", []) if r.get("status") == "downloaded"}

    def fetch(task):
        row, url = task
        result = {
            "printing_id": row["printing_id"],
            "identity_id": row["identity_id"],
            "card_identifier": row["card_identifier"],
            "url": url,
            "checked_at": user_today(),
        }
        prior = cached.get(url)
        if prior and (root / prior["path"]).exists() and sha(root / prior["path"]) == prior["sha256"]:
            result.update({k: prior[k] for k in ["path", "sha256", "bytes", "status"]})
            return result
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "LorcanaLoremaster/0.2"})
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
            if not (payload.startswith(b"\xff\xd8\xff") or payload.startswith(b"\x89PNG")):
                raise ValueError("Response is not a JPEG/PNG image")
            digest = hashlib.sha256(payload).hexdigest()
            path = target / (digest + (".jpg" if payload.startswith(b"\xff") else ".png"))
            if not path.exists():
                path.write_bytes(payload)
            result.update(
                status="downloaded", path=str(path.relative_to(root)), sha256=digest, bytes=len(payload)
            )
        except (OSError, ValueError) as exc:
            result.update(status="download_failed", error=str(exc))
        return result

    with ThreadPoolExecutor(max_workers=workers) as executor:
        records = list(executor.map(fetch, tasks))
    report = {
        "schema_version": 1,
        "catalog_sha256": sha(root / "data/raw/ravensburger/catalog.en.json"),
        "checked_at": user_today(),
        "requested_printings": len(required),
        "downloaded": sum(r["status"] == "downloaded" for r in records),
        "failed": [r for r in records if r["status"] != "downloaded"],
        "missing_image_printings": sorted(required - {r["printing_id"] for r in records}),
        "records": records,
    }
    write_json(target / "manifest.json", report)
    write_json(root / "reports/image-downloads.json", {k: v for k, v in report.items() if k != "records"})
    return {k: v for k, v in report.items() if k != "records"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, choices=range(1, 9), default=6)
    args = parser.parse_args()
    print(json.dumps(download(workers=args.workers), indent=2))
