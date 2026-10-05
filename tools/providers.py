#!/usr/bin/env python3
"""Inspect providers and cache explicitly registered public JSON endpoints."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from loremaster.providers import catalog, coverage, snapshot  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--category")
    download = sub.add_parser("snapshot")
    download.add_argument("provider")
    download.add_argument("endpoint")
    sub.add_parser("coverage")
    args = parser.parse_args()
    if args.command == "list":
        result = [p for p in catalog(ROOT) if not args.category or args.category in p["categories"]]
    elif args.command == "snapshot":
        result = snapshot(ROOT, args.provider, args.endpoint)
    else:
        result = coverage(ROOT)
        (ROOT / "reports" / ("provider-coverage-" + result["snapshot_date"] + ".json")).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
