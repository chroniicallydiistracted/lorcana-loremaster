"""Reproducible deck reviews with dated list evidence and explicit strategic limits."""

import itertools
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

from loremaster.tournaments import digest, read_dataset, verify_dataset
from tools.lorcana import analyze_deck, audit_collection, load_deck, load_identities, probability, resolve

COLLECTION = "data/collections/andys-lore-library-2026-09-15.csv"


def distribution(value):
    return {"exact_fraction": str(value), "probability": float(value), "percent": 100 * float(value)}


def joint_access(counts, groups, draws):
    """At least one member of every identity group, including overlapping groups."""
    if not groups or len(groups) > 8:
        raise ValueError("Provide between one and eight target groups")
    if any(isinstance(q, bool) or not isinstance(q, int) or q < 0 for q in counts.values()):
        raise ValueError("Counts must be nonnegative integers")
    population = sum(counts.values())
    probability(population, 0, draws)  # validate sample size, including bools
    if any(not set(g) <= set(counts) for g in groups):
        raise ValueError("Target group contains an identity absent from the population")
    result = Fraction(0)
    for size in range(len(groups) + 1):
        for selected in itertools.combinations(groups, size):
            union = set().union(*selected)
            remaining = population - sum(counts[k] for k in union)
            result += (-1) ** size * Fraction(comb(remaining, draws), comb(population, draws))
    return result


def conditional_mulligan(population, successes, opening_size, opening_successes, returned, kept_successes):
    """Conditional access after setting aside replacements, before reshuffling them."""
    for value in (population, successes, opening_size, opening_successes, returned, kept_successes):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Mulligan inputs must be nonnegative integers")
    if not (
        0 < population
        and successes <= population
        and opening_size <= population
        and opening_successes <= min(successes, opening_size)
        and opening_size - opening_successes <= population - successes
        and returned <= min(opening_size, population - opening_size)
        and max(0, opening_successes - returned) <= kept_successes <= opening_successes
        and kept_successes <= opening_size - returned
    ):
        raise ValueError("Impossible observed hand or mulligan selection")
    if kept_successes:
        return Fraction(1)
    unseen = population - opening_size
    if returned == 0:
        return Fraction(0)
    return probability(unseen, successes - opening_successes, returned)


def quantities(entries):
    return Counter({card["identity_id"]: q for card, q in entries})


def card_rows(entries):
    return [
        {"identity_id": c["identity_id"], "full_name": c["full_name"], "quantity": q}
        for c, q in sorted(entries, key=lambda x: (x[0]["ink_cost"], x[0]["full_name"]))
    ]


def metrics(entries):
    total = sum(q for _, q in entries)
    if not total:
        raise ValueError("Cannot review an empty deck")
    target_counts = {
        "one_cost_characters": sum(
            q for c, q in entries if c["card_type"] == "character" and c["ink_cost"] <= 1
        ),
        "characters_cost_two_or_less": sum(
            q for c, q in entries if c["card_type"] == "character" and c["ink_cost"] <= 2
        ),
        "characters": sum(q for c, q in entries if c["card_type"] == "character"),
        "uninkable": sum(q for c, q in entries if not c["inkable"]),
        "cost_five_or_more": sum(q for c, q in entries if c["ink_cost"] >= 5),
    }
    draws = [d for d in (7, 9, 10) if d <= total]
    access = {
        name: {str(d): distribution(probability(total, q, d)) for d in draws}
        for name, q in target_counts.items()
    }
    result = {
        "classification": "calculation",
        "population": total,
        "target_counts": target_counts,
        "average_printed_cost": {
            "exact_fraction": str(Fraction(sum(c["ink_cost"] * q for c, q in entries), total)),
            "value": sum(c["ink_cost"] * q for c, q in entries) / total,
        },
        "raw_access_at_least_one": access,
        "opening_at_least_three_uninkable": distribution(probability(total, target_counts["uninkable"], 7, 3))
        if total >= 7
        else None,
        "assumptions": "Uniform sampling without replacement. 7/9/10 are cards seen, not turn labels. No mulligan, draw effects, ink choices, deployment, survival or hidden information modeled.",
    }
    counts = quantities(entries)
    groups = [
        {c["identity_id"] for c, _ in entries if c["name"] == "Mickey Mouse"},
        {c["identity_id"] for c, _ in entries if c["name"] == "Minnie Mouse"},
        {
            c["identity_id"]
            for c, _ in entries
            if c["full_name"] == "Mickey Mouse & Minnie Mouse - Adventuring Duo"
        },
    ]
    if all(groups):
        result["duo_three_part_access"] = {
            "base_and_payoff_counts": [sum(counts[k] for k in g) for g in groups],
            "draws": {str(d): distribution(joint_access(counts, groups, d)) for d in draws},
            "limits": "Joint raw access to both named bases and payoff; no independence assumption. Not the probability of a legal Shift or a quest on a particular turn.",
        }
    if any(c["full_name"] == "Nani - Stage Manager" for c, _ in entries) and total >= 4:
        result["nani_unconditioned_top_four"] = {
            **distribution(probability(total, target_counts["characters_cost_two_or_less"], 4)),
            "limits": "Reference from the full list. Actual play must subtract all known cards and use the remaining deck, including previous bottom placements.",
        }
    return result


def ownership(entries, collection):
    owned = collection["identity_counts"]
    rows = [
        {
            "identity_id": c["identity_id"],
            "full_name": c["full_name"],
            "needed": q,
            "owned": owned.get(c["identity_id"], 0),
            "missing": max(0, q - owned.get(c["identity_id"], 0)),
        }
        for c, q in entries
    ]
    return {
        "required_copies": sum(r["needed"] for r in rows),
        "covered_copies": sum(min(r["needed"], r["owned"]) for r in rows),
        "missing_copies": sum(r["missing"] for r in rows),
        "missing_cards": sorted((r for r in rows if r["missing"]), key=lambda r: r["full_name"]),
        "all_cards": rows,
        "unresolved_collection_rows": collection["unresolved_rows"],
        "limits": "Gameplay identities aggregate finishes/reprints. Inventory date appears in the report's collection metadata; no prices or purchase total inferred. Per-deck allocation unless explicitly combined.",
    }


def apply_changes(entries, changes, identities):
    counts, by_id, normalized = quantities(entries), {c["identity_id"]: c for c in identities}, []
    seen = set()
    for change in changes:
        delta = change["delta"]
        if isinstance(delta, bool) or not isinstance(delta, int) or delta == 0:
            raise ValueError("Every change requires a nonzero integer delta")
        card = resolve(change, identities)
        key = card["identity_id"]
        if key in seen:
            raise ValueError("Consolidate repeated changes to the same identity")
        seen.add(key)
        counts[key] += delta
        if counts[key] < 0:
            raise ValueError("Cut exceeds existing copies: " + card["full_name"])
        normalized.append({"identity_id": key, "full_name": card["full_name"], "delta": delta})
    if not changes or sum(row["delta"] for row in normalized) != 0:
        raise ValueError("Every addition must be balanced by cuts; preserve deck size")
    return [(by_id[k], q) for k, q in sorted(counts.items()) if q], normalized


class ReviewContext:
    """Load and verify source bindings once when reviewing several decks."""

    def __init__(self, root, as_of, collection_path=COLLECTION):
        self.root, self.as_of = Path(root), as_of
        self.identities = load_identities(as_of)
        self.policy = json.loads((self.root / "data/policy/legality.json").read_text())
        self.collection_path = self.root / collection_path
        self.collection = audit_collection(self.collection_path, self.identities)
        self.profiles = json.loads((self.root / "data/strategy/archetypes.json").read_text())
        self.plans = json.loads((self.root / "data/strategy/review-plans.json").read_text())
        self.directory = self.profiles["evidence_directory"]
        self.events, self.lists = read_dataset(self.root, self.directory)
        for binding in self.profiles["source_bindings"] + self.plans["source_bindings"]:
            if digest(self.root / binding["path"]) != binding["sha256"]:
                raise ValueError("Strategy source changed; review curation: " + binding["path"])
        verified = verify_dataset(self.root, self.directory)
        if not verified["passed"]:
            raise ValueError("Tournament evidence failed verification: " + "; ".join(verified["errors"]))
        self.by_list = {r["list_id"]: r for r in self.lists["records"]}
        self.by_event = {r["event_id"]: r for r in self.events["records"]}
        self.fresh = (
            as_of == self.profiles["checked_at"] == self.plans["checked_at"] == self.events["as_of"]
            and as_of == self.policy["checked_at"]
        )
        for profile in self.profiles["profiles"]:
            if profile["checked_at"] != self.profiles["checked_at"] or profile["format"] != "core":
                raise ValueError("Profile date/format differs from its evidence snapshot")
            for key in profile["sample_ids"]:
                if key not in self.by_list:
                    raise ValueError("Profile refers to an unknown list: " + key)
            for package in profile["packages"]:
                for name in package["cards"]:
                    resolve(name, self.identities)

    def source(self, list_id):
        row = self.by_list[list_id]
        event = self.by_event[row["event_id"]]
        return {
            "list_id": list_id,
            "player": row["player"],
            "reported_rank": row["reported_rank"],
            "event": event["event_name"],
            "event_date": event["event_start_date"],
            "official_event_url": event["upstream_event_url"],
            "deck_url": row["url"],
            "snapshot_sha256": row["snapshot_sha256"],
            "limits": "Event date/format corroborated officially; list and finish reported by LorcanaHunter. Exact registration timing and independent official final standing not established.",
        }

    def match_profiles(self, entries):
        counts = quantities(entries)
        matches = []
        for profile in self.profiles["profiles"]:
            for key in profile["sample_ids"]:
                reference = Counter({r["identity_id"]: r["quantity"] for r in self.by_list[key]["cards"]})
                overlap = sum((counts & reference).values())
                matches.append(
                    {
                        "profile_id": profile["profile_id"],
                        "list_id": key,
                        "shared_copies": overlap,
                        "fraction_of_input": overlap / sum(counts.values()),
                    }
                )
        return sorted(matches, key=lambda m: (-m["shared_copies"], m["list_id"]))

    def profile_summary(self, profile):
        lists = [self.by_list[k] for k in profile["sample_ids"]]
        maps = [Counter({r["identity_id"]: r["quantity"] for r in rec["cards"]}) for rec in lists]
        names = {r["identity_id"]: r["full_name"] for rec in lists for r in rec["cards"]}
        ranges = [
            {
                "identity_id": k,
                "full_name": names[k],
                "minimum": min(m[k] for m in maps),
                "maximum": max(m[k] for m in maps),
            }
            for k in sorted(names, key=lambda key: names[key])
        ]
        return {
            **profile,
            "sources": [self.source(k) for k in profile["sample_ids"]],
            "observed_copy_ranges": ranges,
            "sample_count": len(lists),
            "range_limits": "Only these selected lists; zero means absent from a selected list. A shared core is descriptive, never mandatory or proved optimal.",
        }

    def review(self, path, fmt="core", profile_id=None, pool_path=None):
        path = Path(path)
        entries = load_deck(path, self.identities)
        pool = load_deck(pool_path, self.identities) if pool_path else None
        validation = analyze_deck(entries, fmt, self.as_of, self.policy, pool)
        input_sha = digest(path)
        plans = [p for p in self.plans["decks"] if p["deck_sha256"] == input_sha]
        plan = plans[0] if plans and self.fresh and fmt == "core" else None
        matches = self.match_profiles(entries) if self.fresh and fmt == "core" else []
        if profile_id and profile_id not in {p["profile_id"] for p in self.profiles["profiles"]}:
            raise ValueError("Unknown archetype profile: " + profile_id)
        chosen = profile_id or (plan["profile_id"] if plan else None)
        if not chosen and matches and matches[0]["fraction_of_input"] >= 0.6:
            chosen = matches[0]["profile_id"]
        profile = next((p for p in self.profiles["profiles"] if p["profile_id"] == chosen), None)
        evidence_ready = self.fresh and fmt == "core"
        summary = self.profile_summary(profile) if profile and evidence_ready else None
        role_counts = []
        if summary:
            counts = quantities(entries)
            for package in summary["packages"]:
                role_counts.append(
                    {
                        "role": package["role"],
                        "copies": sum(
                            counts[resolve(n, self.identities)["identity_id"]] for n in package["cards"]
                        ),
                        "purpose": package["purpose"],
                    }
                )
        variants = []
        if plan and validation["verdict"] == "passes_supported_checks":
            for variant in plan["variants"]:
                revised, changes = apply_changes(entries, variant["changes"], self.identities)
                verdict = analyze_deck(revised, fmt, self.as_of, self.policy)
                if verdict["verdict"] != "passes_supported_checks":
                    raise ValueError("Curated revision fails validation: " + variant["variant_id"])
                if variant.get("expected_exact_list"):
                    reference = Counter(
                        {
                            r["identity_id"]: r["quantity"]
                            for r in self.by_list[variant["expected_exact_list"]]["cards"]
                        }
                    )
                    if quantities(revised) != reference:
                        raise ValueError("Candidate differs from its claimed exact reference list")
                variants.append(
                    {
                        "variant_id": variant["variant_id"],
                        "name": variant["name"],
                        "classification": "strategic_inference",
                        "changes": changes,
                        "rationale": variant["rationale"],
                        "tradeoffs": variant["tradeoffs"],
                        "test_plan": variant["test_plan"],
                        "sources": [self.source(k) for k in variant["sample_ids"]],
                        "validation": verdict,
                        "metrics": metrics(revised),
                        "ownership": ownership(revised, self.collection),
                        "cards": card_rows(revised),
                    }
                )
        bindings = [
            "data/raw/ravensburger/catalog.en.json",
            "data/policy/card-text-reviews.json",
            "data/policy/legality.json",
            "data/strategy/archetypes.json",
            "data/strategy/review-plans.json",
            self.directory + "/events.json",
            self.directory + "/decklists.json",
        ]
        return {
            "schema_version": 1,
            "as_of": self.as_of,
            "name": json.loads(path.read_text()).get("name", path.stem)
            if path.suffix == ".json" and isinstance(json.loads(path.read_text()), dict)
            else path.stem,
            "input": {"path": str(path), "sha256": input_sha},
            "pool": {"path": str(Path(pool_path)), "sha256": digest(pool_path)} if pool_path else None,
            "source_bindings": [{"path": p, "sha256": digest(self.root / p)} for p in bindings],
            "collection": {
                "path": str(self.collection_path),
                "sha256": digest(self.collection_path),
                "snapshot_date": "2026-09-15"
                if self.collection_path.resolve() == (self.root / COLLECTION).resolve()
                else None,
            },
            "validation": validation,
            "cards": card_rows(entries),
            "metrics": metrics(entries),
            "ownership": ownership(entries, self.collection),
            "profile": summary,
            "profile_matching": {
                "classification": "calculation",
                "matches": matches,
                "limits": "Copy overlap routes to curated advice; it does not establish archetype identity, power or matchup outcomes.",
            },
            "role_counts": role_counts,
            "coaching": [
                {
                    **item,
                    "sources": [
                        self.source(k)
                        for p in self.profiles["profiles"]
                        if p["profile_id"] == item["profile_id"]
                        for k in p["sample_ids"]
                    ],
                }
                for item in plan["coaching"]
            ]
            if plan
            else [],
            "findings": plan["findings"] if plan else [],
            "variants": variants,
            "review_required": (
                []
                if evidence_ready
                else [
                    "Refresh policy and evidence for this date/format before using snapshot-specific strategy."
                ]
            )
            + (
                []
                if plan
                else [
                    "No reviewed bespoke revision plan for this exact deck; inspect references and metrics before proposing changes."
                ]
            )
            + (
                ["Resolve unmapped inventory rows before treating missing counts as complete."]
                if self.collection["unresolved_rows"]
                else []
            ),
            "limits": "Legality and mathematics are deterministic within the source snapshot. Role assignments, mulligans and revisions are authored strategic inference. No gameplay engine, match record, measured win rate or independent expert validation is claimed.",
        }


def markdown(report):
    v, m, owned = report["validation"], report["metrics"], report["ownership"]
    lines = [
        f"# {report['name']}",
        "",
        f"Snapshot: {report['as_of']}; format: {v['format']}.",
        "",
        f"**{v['verdict']}**: {v['card_count']} cards; {v['inkable']} inkable / {v['uninkable']} uninkable.",
        "",
        "Printed curve: " + ", ".join(f"{k}: {n}" for k, n in v["printed_cost_curve"].items()) + ".",
        "",
        f"Inventory snapshot covers {owned['covered_copies']}/{owned['required_copies']} copies; {owned['missing_copies']} missing.",
        "",
        owned["limits"],
        "",
        "## Findings and plan",
        "",
    ]
    lines.extend(
        f"- {finding}"
        for finding in report["findings"]
        or ["Inspect the metrics and sourced reference profile; bespoke revision requires review."]
    )
    lines += [
        "",
        "## Calculated access",
        "",
        m["assumptions"],
        "",
        "| Target | Copies | Opening 7 | Seen 9 | Seen 10 |",
        "|---|---:|---:|---:|---:|",
    ]
    for target, copies in m["target_counts"].items():
        values = m["raw_access_at_least_one"][target]
        lines.append(
            f"| {target.replace('_', ' ')} | {copies} | "
            + " | ".join(
                f"{values[str(d)]['percent']:.2f}%" if str(d) in values else "n/a" for d in (7, 9, 10)
            )
            + " |"
        )
    if m["opening_at_least_three_uninkable"]:
        lines += [
            "",
            f"Opening with at least three uninkable cards: {m['opening_at_least_three_uninkable']['percent']:.2f}%. This is a burden indicator, not a mulligan verdict.",
        ]
    if "duo_three_part_access" in m:
        duo = m["duo_three_part_access"]
        lines += [
            "",
            "Mickey base / Minnie base / Duo copies: "
            + "/".join(map(str, duo["base_and_payoff_counts"]))
            + ".",
            "Joint access: "
            + ", ".join(f"{d} seen: {r['percent']:.2f}%" for d, r in duo["draws"].items())
            + ".",
            duo["limits"],
        ]
    if "nani_unconditioned_top_four" in m:
        n = m["nani_unconditioned_top_four"]
        lines += [
            "",
            f"Nani target in a random top four of the full list: {n['percent']:.2f}%. {n['limits']}",
        ]
    lines += [
        "",
        "## Missing gameplay copies",
        "",
        "| Card | Needed | Owned | Missing |",
        "|---|---:|---:|---:|",
    ]
    lines += [
        f"| {r['full_name']} | {r['needed']} | {r['owned']} | {r['missing']} |"
        for r in owned["missing_cards"]
    ]
    for variant in report["variants"]:
        lines += [
            "",
            f"## Candidate: {variant['name']}",
            "",
            "Strategic inference; test before adopting.",
            "",
            variant["rationale"],
            "",
            "| Card | Change |",
            "|---|---:|",
        ]
        lines += [
            f"| {r['full_name']} | {r['delta']:+d} |"
            for r in sorted(variant["changes"], key=lambda r: r["delta"])
        ]
        s = variant["validation"]
        lines += [
            "",
            f"Validated {s['card_count']}-card candidate: {s['inkable']} inkable / {s['uninkable']} uninkable; {variant['ownership']['missing_copies']} missing copies.",
            "",
            "Tradeoffs: " + variant["tradeoffs"],
            "",
            "Test: " + variant["test_plan"],
        ]
        lines += [
            "",
            "Observed reference: "
            + "; ".join(
                f"[{s['player']}, {s['event_date']}, reported #{s['reported_rank']}]({s['deck_url']})"
                for s in variant["sources"]
            )
            + ".",
        ]
    lines += [
        "",
        "## Matchup coaching",
        "",
        "All matchup guidance below is strategic inference; adapt to the actual opponent's list and public board.",
        "",
    ]
    for matchup in report["coaching"]:
        lines += [
            f"### {matchup['against']}",
            "",
            "Keep/return: " + matchup["mulligan"],
            "",
            "Ink plan: " + matchup["inking"],
            "",
            "Sequence and priorities: " + matchup["sequencing"],
            "",
        ]
        lines += [
            "Observed opposing lists: "
            + "; ".join(f"[{s['player']}, {s['event_date']}]({s['deck_url']})" for s in matchup["sources"])
            + ".",
            "",
        ]
    if report["profile"]:
        p = report["profile"]
        lines += [
            "## Archetype evidence",
            "",
            f"{p['name']}: {p['sample_count']} selected exact lists.",
            "",
            p["main_plan"],
            "",
            p["evidence_limits"],
            "",
        ]
        lines += [
            f"- [{s['player']} at {s['event']}, {s['event_date']}, reported #{s['reported_rank']}]({s['deck_url']}); [official event]({s['official_event_url']})."
            for s in p["sources"]
        ]
    lines += [
        "",
        "## Reproduction and limits",
        "",
        report["limits"],
        "",
        "Exact fractions, full lists and SHA-256 input/source bindings are in the adjacent JSON report. Original decks and inventory are preserved.",
        "",
    ]
    lines += ["Review required: " + s for s in report["review_required"] + v["review_required"] + v["issues"]]
    return "\n".join(lines) + "\n"


def write_review(report, directory, stem):
    directory = Path(directory)
    protected = {Path(report["input"]["path"]).resolve(), Path(report["collection"]["path"]).resolve()}
    targets = [directory / (stem + suffix) for suffix in (".json", ".md")]
    targets += [directory / (stem + "--" + v["variant_id"] + ".json") for v in report["variants"]]
    if any(path.resolve() in protected for path in targets):
        raise ValueError("Review output would overwrite an input deck or collection")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / (stem + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (directory / (stem + ".md")).write_text(markdown(report))
    for variant in report["variants"]:
        payload = {
            "name": variant["name"],
            "as_of": report["as_of"],
            "format": report["validation"]["format"],
            "classification": "strategic_inference",
            "parent_sha256": report["input"]["sha256"],
            "cards": variant["cards"],
        }
        (directory / (stem + "--" + variant["variant_id"] + ".json")).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        )
