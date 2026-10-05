#!/usr/bin/env python3
"""Review a deck or regenerate the sourced saved-deck milestone."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from loremaster.deck_review import COLLECTION, ReviewContext, ownership, write_review  # noqa: E402
from tools.lorcana import user_today  # noqa: E402


def profile_document(context):
    lines = [
        "# Archetype evidence — October 4, 2026",
        "",
        "Eight exact Core lists from three recent events support these six representative profiles. Event dates, format and roster sizes are corroborated by official Play Hub pages. Lists and finishes are secondary reports; field sizes disagree in places and final official standings were not visible. This purposeful sample does not support global metashare or matchup win rates.",
        "",
        "Copy ranges are observations. Packages, engines, flex choices, weaknesses and coaching are strategic inference. A one-list profile cannot establish a mandatory core. Hyperia cards are theorycrafting until the verified October 16 US prerelease; refresh policy for later dates.",
        "",
    ]
    for profile in context.profiles["profiles"]:
        p = context.profile_summary(profile)
        lines += [f"## {p['name']}", "", p["main_plan"], ""]
        for s in p["sources"]:
            lines += [
                f"- [{s['player']}, {s['event_date']}, reported #{s['reported_rank']}]({s['deck_url']}); [official event]({s['official_event_url']})."
            ]
        lines += ["", "| Package | Cards | Purpose |", "|---|---|---|"]
        for role in p["packages"]:
            lines += [f"| {role['role']} | {'; '.join(role['cards'])} | {role['purpose']} |"]
        lines += [
            "",
            "Flex choices: " + " ".join(p["flex_slots"]),
            "",
            "Weaknesses: " + " ".join(p["vulnerabilities"]),
            "",
            "Mulligan: " + p["mulligan"],
            "",
            "Sequencing: " + p["sequencing"],
            "",
            f"Observed ranges ({p['sample_count']} selected lists):",
            "",
            "| Card | Min | Max |",
            "|---|---:|---:|",
        ]
        lines += [
            f"| {r['full_name']} | {r['minimum']} | {r['maximum']} |" for r in p["observed_copy_ranges"]
        ]
        lines += ["", p["range_limits"], ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?")
    parser.add_argument(
        "--all", action="store_true", help="Regenerate both saved reviews, candidates and profiles"
    )
    parser.add_argument("--as-of", default=user_today())
    parser.add_argument("--format", choices=["core", "infinity", "sealed", "draft"], default="core")
    parser.add_argument("--collection", default=COLLECTION)
    parser.add_argument("--profile")
    parser.add_argument("--pool")
    parser.add_argument("--output", help="Output directory for JSON, Markdown and candidate lists")
    args = parser.parse_args()
    if bool(args.path) == bool(args.all):
        parser.error("Provide one deck path or --all")
    if args.all and (args.profile or args.pool or args.format != "core"):
        parser.error("--all regenerates the saved Core milestone; use a single path for other options")
    context = ReviewContext(ROOT, args.as_of, args.collection)
    directory = ROOT / (args.output or f"reports/deck-reviews/{args.as_of}")
    if args.all:
        if not context.fresh:
            raise ValueError("Refresh evidence before regenerating a different-date milestone")
        reports = [context.review(ROOT / plan["deck_path"]) for plan in context.plans["decks"]]
        combined = Counter()
        for report in reports:
            write_review(report, directory, Path(report["input"]["path"]).stem)
            combined.update({r["identity_id"]: r["quantity"] for r in report["cards"]})
        by_id = {c["identity_id"]: c for c in context.identities}
        joint = ownership([(by_id[k], q) for k, q in combined.items()], context.collection)
        joint["limits"] += (
            " Combined baseline demand assumes both decks are assembled simultaneously; variants are alternatives, not extra decks."
        )
        (directory / "combined-ownership.json").write_text(
            json.dumps(joint, ensure_ascii=False, indent=2) + "\n"
        )
        (ROOT / "knowledge/strategy/current-archetypes.md").write_text(profile_document(context))
        result = {
            "as_of": args.as_of,
            "reviews": [
                {
                    "deck": r["name"],
                    "verdict": r["validation"]["verdict"],
                    "missing_copies": r["ownership"]["missing_copies"],
                    "variants": len(r["variants"]),
                    "review_required": r["review_required"],
                }
                for r in reports
            ],
            "combined_missing_copies": joint["missing_copies"],
            "output": str(directory),
        }
        passed = all(
            r["validation"]["verdict"] == "passes_supported_checks" and not r["review_required"]
            for r in reports
        )
    else:
        result = context.review(Path(args.path), args.format, args.profile, args.pool)
        if args.output:
            write_review(result, directory, Path(args.path).stem)
        passed = (
            result["validation"]["verdict"] == "passes_supported_checks" and not result["review_required"]
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
