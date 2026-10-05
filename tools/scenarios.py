#!/usr/bin/env python3
"""Export compound prompts without answers or evaluate supplied structured responses."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from loremaster.scenarios import evaluate, prompts  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prompts", "evaluate"])
    parser.add_argument(
        "responses", nargs="?", default="benchmarks/responses/expert-scenarios-2026-10-04.json"
    )
    parser.add_argument("--suite", default="benchmarks/expert-scenarios.json")
    parser.add_argument("--output")
    args = parser.parse_args()
    suite = json.loads((ROOT / args.suite).read_text())
    result = (
        prompts(suite)
        if args.command == "prompts"
        else evaluate(ROOT, suite, json.loads((ROOT / args.responses).read_text()))
    )
    if args.output:
        path = ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if args.command == "prompts" or result["passed"] else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
