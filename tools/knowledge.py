#!/usr/bin/env python3
"""Official section/page retrieval, reviewed answers and source monitoring."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from loremaster.answers import answer, facts
from loremaster.evaluation import evaluate
from loremaster.index import build_index, retrieve
from tools.lorcana import ROOT, read_json, user_today, write_json


def watch(root=ROOT):
    """Compare the cached, recently refreshed Resources page with registered PDFs."""
    sources = read_json(root / "sources/manifest.json")["sources"]
    resources = next(s for s in sources if s["source_id"] == "resources")
    html = (root / resources["path"]).read_text()
    links = sorted(set(re.findall(r'https://files\.disneylorcana\.com/[^"<>\s]+\.pdf', html)))
    registered = {s["url"] for s in sources}
    hyperia = [
        url
        for url in links
        if "hyperia" in url.casefold()
        and any(term in url.casefold() for term in ["release", "rules", "notes"])
    ]
    report = {
        "checked_at": resources.get("checked_at"),
        "resources_sha256": resources["sha256"],
        "hyperia_rules_or_release_notes": hyperia,
        "unregistered_documents": [u for u in links if u not in registered],
        "policy_updated": False,
        "requires_review": bool(hyperia),
        "note": "Refresh the Resources page first. New publications need review before changing rules or policy.",
    }
    write_json(root / "reports/source-watch.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("topics")
    sub.add_parser("watch")
    sub.add_parser("benchmark")
    search = sub.add_parser("search")
    search.add_argument("query", nargs="?", default="")
    search.add_argument("--source")
    search.add_argument("--section")
    search.add_argument("--limit", type=int, choices=range(1, 31), default=8)
    search.add_argument("--as-of", default=user_today())
    respond = sub.add_parser("answer")
    respond.add_argument("query", nargs="?", default="")
    respond.add_argument("--topic")
    respond.add_argument("--as-of", default=user_today())
    args = parser.parse_args()
    if args.command == "build":
        result = build_index(ROOT)
        write_json(ROOT / "reports/evidence-index.json", result)
    elif args.command == "benchmark":
        result = evaluate(ROOT)
        write_json(ROOT / "reports/game-master-benchmark.json", result)
    elif args.command == "topics":
        result = [{"topic": f.fact_id, "domain": f.domain, "questions": f.questions} for f in facts(ROOT)]
    elif args.command == "watch":
        result = watch()
    elif args.command == "search":
        result = retrieve(
            ROOT,
            query=args.query,
            source_id=args.source,
            section=args.section,
            limit=args.limit,
            as_of=args.as_of,
        )
    else:
        result = answer(ROOT, args.query, args.topic, args.as_of)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if isinstance(result, dict) and result.get("failed", 0) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
