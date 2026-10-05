#!/usr/bin/env python3
"""Reproduce the October 4 review; new snapshots require new manual adjudication."""

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from loremaster.schemas import ReviewLedger
from tools.lorcana import ROOT, read_json, read_jsonl, sha, write_json

REVIEWED_CATALOG = "49266e492d7545c7c7c617d239c3eb3756794b56f485a4c0918e4e4fc1abe3c3"
# These cases were adjudicated against official images/documents in this review.
# Values are taken from the specified raw printing, never from guessed card text.
ADJUDICATIONS = {
    "Moana - Of Motunui": (
        1956,
        "functional",
        "Fabled new-text ruling confirms exerted Princesses and conditional quest restriction.",
    ),
    "Bruno's Return": (1965, "functional", "Current Fabled image makes damage removal optional."),
    "Anna - Braving the Storm": (
        2082,
        "cosmetic",
        "Current image clarifies the static condition with While.",
    ),
    "Oswald - The Lucky Rabbit": (
        1341,
        "data_error",
        "Both official images include optional reveal; promo API text omits may.",
    ),
    "Bucky - Squirrel Squeak Tutor": (
        289,
        "functional",
        "Official errata effective August 9, 2024 requires Shift; both cached images show corrected text.",
    ),
    "Anna - Soothing Sister": (
        2513,
        "cosmetic",
        "Base image and Winterspell release notes confirm Unusual Transformation; card/character wording refers to the same card.",
    ),
    "Robin Hood - Unrivaled Archer": (
        2098,
        "functional",
        "Current Fabled image confirms optional card draw.",
    ),
    "Dig a Little Deeper": (
        2102,
        "cosmetic",
        "Current image combines the same ordered hand/bottom instructions into one sentence.",
    ),
    "Develop Your Brain": (2099, "cosmetic", "Current image clarifies ownership of the referenced deck."),
    "Sulley - Protective Monster": (
        3099,
        "data_error",
        "Base and promo images both contain Fearsome Glare and Riled Up; promo API field is empty.",
    ),
    "Bruno Madrigal - Undetected Uncle": (
        1936,
        "cosmetic",
        "Current image shortens that card to it; same referenced revealed card.",
    ),
    "Devil's Eye Diamond": (
        1585,
        "data_error",
        "Both images say took damage. Wilds Unknown readability update explicitly includes this card.",
    ),
    "One Last Hope": (
        2133,
        "cosmetic",
        "Current image uses can for the permission; optional challenge choice remains.",
    ),
    "Pluto - Rescue Dog": (
        1952,
        "functional",
        "Current image expressly chooses character of yours; preserve targeting wording.",
    ),
    "Judy Hopps - Optimistic Officer": (
        2093,
        "functional",
        "Current image conditions draw on actual item banishment with If you do.",
    ),
    "Mickey Mouse - True Friend": (
        1949,
        "data_error",
        "Base and promo image have no abilities; API promo rules field contains italic flavor text.",
    ),
    "Heihei - Persistent Presence": (
        2521,
        "cosmetic",
        "Current image clarifies return from discard, retains full-name alias for old spelling.",
    ),
    "Winnie the Pooh - Hunny Wizard": (
        1977,
        "classification",
        "Current Fabled image includes Hunny; Set 2 image lacks it. Apply current classification to identity.",
    ),
    "Colors of the Wind": (
        2527,
        "cosmetic",
        "Winterspell ruling explicitly counts unique ink types/symbols including all types on dual-ink cards; both wordings express this.",
    ),
    "Raya - Headstrong": (
        2063,
        "functional",
        "Current image conditions quest restriction on using the ready effect.",
    ),
    "Last-Ditch Effort": (
        1998,
        "cosmetic",
        "Fabled release note confirms independent effect parts and current text without Then.",
    ),
    "Peter Pan's Shadow - Not Sewn On": (
        1978,
        "cosmetic",
        "Only independent keyword display order changes; current image confirms both Rush and Evasive.",
    ),
    "Robin Hood - Ephemeral Archer": (
        2360,
        "data_error",
        "Both cached images use Whenever ... if ...; enchanted API incorrectly substitutes a granted-trigger construction.",
    ),
    "Tuk Tuk - Lively Partner": (
        2065,
        "functional",
        "Current image conditions strength bonus on using the move effect.",
    ),
    "Pongo - Determined Father": (
        1938,
        "functional",
        "Fabled release note and current image restrict activated use to once during your turn.",
    ),
    "Maleficent - Mistress of All Evil": (
        487,
        "cosmetic",
        "Missing sentence-ending period is punctuation only.",
    ),
    "Casa Madrigal - Casita": (2004, "cosmetic", "Comma after if-clause is punctuation only."),
    "Half Hexwell Crown": (
        1021,
        "cosmetic",
        "Story ability labels differ; CR 5.2.8 states story names are not used for gameplay. Missing period only otherwise.",
    ),
    "Moana - Adventurer of Land and Sea": (
        1589,
        "naming",
        "API groups Moana and English Vaiana regional printing in one identity; preserve Vaiana alias, use Moana English gameplay name.",
    ),
}


def functional_signature(text):
    """Whitelist only known reminder constructions; retain unknown parentheses."""
    text = unicodedata.normalize("NFKC", text).translate(str.maketrans({"’": "'", "‘": "'"}))
    text = text.replace("%", " ")
    text = re.sub(r"\\[^\\]+\\", "", text)  # story labels: CR 5.2.8
    reminder_starts = (
        "You may pay ",
        "Only characters with Evasive ",
        "This character ",
        "They can challenge ",
        "Opponents can't choose ",
        "Whenever this character quests, ",
        "Any number of your or your teammates' characters ",
        "A character with cost ",
        "Once during your turn, you may pay ",
        "Damage dealt to ",
        "They get +",
        "They get -",
    )
    reminder_starts += ("Whenever they quest, ", "You pay all costs.", "Each ink drop may be removed ")

    def reminder(match):
        inner = match[0][1:-1]
        return " " if inner.startswith(reminder_starts) else match[0]

    text = re.sub(r"\([^()]*\)", reminder, text)
    # Official Fabled readability change explicitly adds the ink symbol to Shift costs.
    text = re.sub(r"(<[^>]*Shift>\s+\d+)(?!\d|\s*\{I\})", r"\1 {I}", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def review(root=ROOT):
    if sha(root / "data/raw/ravensburger/catalog.en.json") != REVIEWED_CATALOG:
        raise ValueError("This review applies only to the inspected October 4 snapshot")
    rows = read_jsonl(root / "data/derived/printings.jsonl")
    groups = defaultdict(list)
    for row in rows:
        groups[row["identity_id"]].append(row)
    images = {r["printing_id"]: r for r in read_json(root / "sources/images/manifest.json")["records"]}
    sources = {r["source_id"]: r for r in read_json(root / "sources/manifest.json")["sources"]}

    def citation(source_id, page=None, section=None):
        s = sources[source_id]
        return {k: s[k] for k in ["source_id", "sha256", "url", "path"]} | {"page": page, "section": section}

    records = []
    for identity in read_jsonl(root / "data/derived/identities.jsonl"):
        fields = identity["conflict_fields"]
        if not fields:
            continue
        name = identity["full_name"]
        printings = groups[identity["identity_id"]]
        selected_id = identity["candidate_printing_id"]
        categories = []
        reason = "Exact functional token comparison after known reminder, Unicode, whitespace, story-label and documented Shift readability normalization."
        signatures = {functional_signature(p["rules_text"]) for p in printings}
        resolved = len(signatures) == 1 and all(f in {"rules_text", "name", "subtitle"} for f in fields)
        if "name" in fields or "subtitle" in fields:
            resolved = resolved and all(
                len({p[f].casefold() for p in printings}) == 1 for f in fields if f in {"name", "subtitle"}
            )
            categories.append("naming")
        if "rules_text" in fields:
            categories.append("reminder" if any("(" in p["rules_text"] for p in printings) else "cosmetic")
        if name in ADJUDICATIONS:
            selected_id, category, reason = ADJUDICATIONS[name]
            categories = sorted(set(categories + [category]))
            resolved = True
        chosen = next(p for p in printings if p["printing_id"] == selected_id)
        # For purely cosmetic/reminder cases retain the most complete same-set reminder text.
        if resolved and name not in ADJUDICATIONS:
            candidates = [p for p in printings if p["printed_set_number"] == chosen["printed_set_number"]]
            chosen = max(candidates, key=lambda p: (p["is_base"], len(p["rules_text"]), -p["printing_id"]))
            selected_id = chosen["printing_id"]
        evidence = [
            citation("ravensburger-catalog-en"),
            citation("comprehensive-rules-2.2.0", 3, "1.1.7"),
            citation("comprehensive-rules-2.2.0", 22, "5.2.8"),
        ]
        if "Shift" in chosen["rules_text"]:
            evidence.append(citation("fabled-release-notes", 3))
        for printing in printings:
            img = images[printing["printing_id"]]
            evidence.append(
                {
                    "source_id": "official-card-image-" + str(img["printing_id"]),
                    **{k: img[k] for k in ["sha256", "url", "path"]},
                    "page": None,
                    "section": None,
                }
            )
        if name in {"Moana - Of Motunui", "Last-Ditch Effort", "Pongo - Determined Father"}:
            evidence.append(citation("fabled-release-notes"))
        if name == "Bucky - Squirrel Squeak Tutor":
            evidence.append(citation("bucky-errata"))
        if name == "Colors of the Wind" or name == "Anna - Soothing Sister":
            evidence.append(citation("winterspell-release-notes"))
        if name == "Devil's Eye Diamond":
            evidence.append(citation("wilds-unknown-release-notes"))
        records.append(
            {
                "identity_id": identity["identity_id"],
                "full_name": name,
                "catalog_sha256": REVIEWED_CATALOG,
                "reviewed_at": "2026-10-04",
                "effective_from": "2026-10-04",
                "effective_until": None,
                "official_effective_date": "2024-08-09" if name == "Bucky - Squirrel Squeak Tutor" else None,
                "status": "resolved" if resolved else "unresolved",
                "categories": categories or ["functional"],
                "selected_printing_id": selected_id,
                "fields": fields,
                "resolved_values": {f: chosen[f] for f in fields} if resolved else {},
                "rationale": reason
                if resolved
                else "Functional text differs; no adjudication yet. Inspect attached images and official rulings.",
                "evidence": evidence,
            }
        )
    ledger = ReviewLedger.model_validate(
        {
            "schema_version": 2,
            "coverage": "All raw conflict groups triaged for the inspected snapshot. Effective from review date only; this is not a historical or complete worldwide oracle.",
            "records": records,
        }
    )
    write_json(root / "data/policy/card-text-reviews.json", ledger.model_dump(mode="json"))
    report = {
        "reviewed_at": "2026-10-04",
        "identities": len(records),
        "statuses": dict(Counter(r["status"] for r in records)),
        "categories": dict(Counter(c for r in records for c in r["categories"])),
        "unresolved": [r["full_name"] for r in records if r["status"] == "unresolved"],
    }
    write_json(root / "reports/card-text-review.json", report)
    return report


if __name__ == "__main__":
    print(json.dumps(review(), indent=2))
