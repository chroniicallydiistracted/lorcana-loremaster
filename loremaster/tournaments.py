"""Dated tournament evidence: exact lists and publication limits, never inferred win rates."""

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from tools.lorcana import analyze_deck, load_identities, resolve


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_hunter_excerpt(text):
    """Parse quantity/name tables from a saved web-tool excerpt, ignoring provider stats."""
    records = []
    for part in text.split(
        "--------------------------------------------------------------------------------"
    ):
        part = part.strip()
        if not part.startswith("Decklist of "):
            continue
        url = re.search(r"\((https://[^\n]+)\)\n", part)
        rank = re.search(r"^L\d+: #(\d+) Score", part, re.M)
        if not url or not rank:
            raise ValueError("Deck excerpt lacks URL or reported rank")
        rows = []
        for line in part.splitlines():
            line = re.sub(r"^L\d+:\s*", "", line)
            match = re.match(r"[●○]\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|", line)
            if match:
                rows.append({"quantity": int(match[1]), "full_name": match[2]})
        declared = re.search(r"Main Deck (\d+) card", part)
        if not rows or not declared or sum(r["quantity"] for r in rows) != int(declared[1]):
            raise ValueError("Incomplete or duplicated deck table")
        records.append({"url": url[1], "reported_rank": int(rank[1]), "cards": rows})
    if not records:
        raise ValueError("No complete LorcanaHunter deck tables found")
    return records


def read_dataset(root, directory="research/2026-10-04"):
    directory = root / directory
    return (
        json.loads((directory / "events.json").read_text()),
        json.loads((directory / "decklists.json").read_text()),
    )


def verify_dataset(root, directory="research/2026-10-04"):
    events, lists = read_dataset(root, directory)
    start, end = date.fromisoformat(events["window_start"]), date.fromisoformat(events["as_of"])
    identities = load_identities(events["as_of"])
    policy = json.loads((root / "data/policy/legality.json").read_text())
    errors, included, excluded, seen, primary_urls = [], [], [], set(), set()
    if lists["as_of"] != events["as_of"]:
        errors.append("List/event snapshot dates differ")
    by_event = {}
    for event in events["records"]:
        eid = event["event_id"]
        if eid in seen:
            errors.append("Duplicate event ID: " + eid)
        seen.add(eid)
        by_event[eid] = event
        for source in event["sources"]:
            path = root / source["path"]
            if not path.is_file() or digest(path) != source["sha256"]:
                errors.append("Event snapshot missing or changed: " + eid)
        if event["status"] != "included":
            excluded.append({"event_id": eid, "reason": event["exclusion_reason"]})
            continue
        when = date.fromisoformat(event["event_start_date"])
        finishes = date.fromisoformat(event["event_end_date"]) if event.get("event_end_date") else when
        if (
            not start <= when <= finishes <= end
            or event["format"] != events["format"]
            or event.get("duplicate_of")
        ):
            errors.append("Invalid date, format or duplicate inclusion: " + eid)
        url = event.get("upstream_event_url")
        canonical = urlsplit(url or "")
        canonical = (canonical.netloc.lower(), canonical.path.rstrip("/"))
        if not url or canonical in primary_urls:
            errors.append("Missing or duplicated upstream event: " + eid)
        if not any(s["kind"] == "official_event_excerpt" and s["url"] == url for s in event["sources"]):
            errors.append("No matching official event corroboration: " + eid)
        primary_urls.add(canonical)
        included.append(eid)
    list_ids, list_keys, validated = set(), set(), []
    for record in lists["records"]:
        key = (record["event_id"], record["player_id"])
        if record["list_id"] in list_ids or key in list_keys:
            errors.append("Duplicate event/player list: " + record["list_id"])
        list_ids.add(record["list_id"])
        list_keys.add(key)
        event = by_event.get(record["event_id"])
        if not event or event["event_id"] not in included or record["format"] != event["format"]:
            errors.append("List lacks included same-format event: " + record["list_id"])
        address = re.search(r"/tournament/(\d+)/[^/]+/player/(\d+)/deck(?:\?|$)", record["url"])
        if (
            not event
            or not address
            or address[1] != str(event["native_event_id"])
            or address[2] != str(record["player_id"])
        ):
            errors.append("List URL does not match its event/player IDs: " + record["list_id"])
        path = root / record["snapshot_path"]
        if not path.is_file() or digest(path) != record["snapshot_sha256"]:
            errors.append("List snapshot missing or changed: " + record["list_id"])
            continue
        parsed = next((r for r in parse_hunter_excerpt(path.read_text()) if r["url"] == record["url"]), None)
        if not parsed:
            errors.append("List URL absent from excerpt: " + record["list_id"])
            continue
        actual, extracted = {}, {}
        for row in record["cards"]:
            card = resolve(row, identities)
            if (
                isinstance(row["quantity"], bool)
                or not isinstance(row["quantity"], int)
                or row["quantity"] <= 0
            ):
                raise ValueError("List quantities must be positive integers")
            if card["identity_id"] in actual:
                errors.append("Consolidate duplicate canonical list identity: " + record["list_id"])
            actual[card["identity_id"]] = actual.get(card["identity_id"], 0) + row["quantity"]
        for row in parsed["cards"]:
            card = resolve(row, identities)
            extracted[card["identity_id"]] = extracted.get(card["identity_id"], 0) + row["quantity"]
        if actual != extracted or parsed["reported_rank"] != record["reported_rank"]:
            errors.append("Transcription differs from saved excerpt: " + record["list_id"])
        entries = [(resolve(i, identities), n) for i, n in actual.items()]
        result = analyze_deck(entries, record["format"], events["as_of"], policy)
        if result["verdict"] != "passes_supported_checks":
            errors.append("List fails current snapshot checks: " + record["list_id"])
        validated.append(
            {"list_id": record["list_id"], "cards": result["card_count"], "verdict": result["verdict"]}
        )
    return {
        "passed": not errors,
        "as_of": events["as_of"],
        "window_start": events["window_start"],
        "included_events": included,
        "excluded_or_candidate_events": excluded,
        "exact_lists": validated,
        "errors": errors,
        "limitations": "Purposeful list sample, partial standings and provider discrepancies. No global field share or matchup win rates computed.",
    }
