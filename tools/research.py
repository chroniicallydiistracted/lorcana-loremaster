#!/usr/bin/env python3
"""Verify a dated tournament snapshot or parse saved public deck excerpts."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from loremaster.tournaments import parse_hunter_excerpt, verify_dataset  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--directory", default="research/2026-10-04")
    parse = sub.add_parser("parse-decks")
    parse.add_argument("snapshot")
    args = parser.parse_args()
    result = (
        verify_dataset(ROOT, args.directory)
        if args.command == "check"
        else parse_hunter_excerpt(Path(args.snapshot).read_text())
    )
    if args.command == "check":
        (ROOT / f"reports/tournament-evidence-{result['as_of']}.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if isinstance(result, dict) and not result["passed"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
