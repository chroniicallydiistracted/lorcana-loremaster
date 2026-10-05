"""Reject incomplete list tables, altered snapshots and future/duplicate evidence."""

import copy
import json
import re
from pathlib import Path

import pytest

from loremaster import tournaments

ROOT = Path(__file__).resolve().parents[1]


def test_parser_keeps_only_exact_deck_table():
    text = (ROOT / "research/2026-10-04/snapshots/recent-decks-1.txt").read_text()
    parsed = tournaments.parse_hunter_excerpt(text)
    assert len(parsed) == 3
    assert all(sum(r["quantity"] for r in p["cards"]) == 60 for p in parsed)
    assert all(0 < r["quantity"] <= 4 for p in parsed for r in p["cards"])
    first = next(line for line in text.splitlines() if re.search(r"[●○]\s*\|\s*\d+\s*\|", line))
    with pytest.raises(ValueError, match="Incomplete or duplicated"):
        tournaments.parse_hunter_excerpt(text.replace(first, "", 1))


def test_current_sample_and_exclusion():
    result = tournaments.verify_dataset(ROOT)
    assert result["passed"]
    assert len(result["included_events"]) == 3
    assert len(result["exact_lists"]) == 8
    assert result["excluded_or_candidate_events"][0]["event_id"] == "candidate-icl-2026-10-07"


def test_dataset_rejects_future_and_duplicated_upstream_event(monkeypatch):
    events, lists = tournaments.read_dataset(ROOT)
    changed = copy.deepcopy(events)
    changed["records"][0]["event_start_date"] = "2026-10-07"
    changed["records"][1]["upstream_event_url"] = changed["records"][0]["upstream_event_url"]
    monkeypatch.setattr(tournaments, "read_dataset", lambda *args: (changed, lists))
    result = tournaments.verify_dataset(ROOT)
    assert not result["passed"]
    assert any("Invalid date" in e for e in result["errors"])
    assert any("duplicated upstream" in e for e in result["errors"])


def test_changed_list_snapshot_cannot_be_used(monkeypatch):
    events, lists = tournaments.read_dataset(ROOT)
    changed = json.loads(json.dumps(lists))
    changed["records"][0]["snapshot_sha256"] = "0" * 64
    monkeypatch.setattr(tournaments, "read_dataset", lambda *args: (events, changed))
    assert not tournaments.verify_dataset(ROOT)["passed"]


def test_list_cannot_be_attached_to_a_different_event(monkeypatch):
    events, lists = tournaments.read_dataset(ROOT)
    changed = copy.deepcopy(lists)
    changed["records"][0]["event_id"] = "hunter-12941"
    monkeypatch.setattr(tournaments, "read_dataset", lambda *args: (events, changed))
    report = tournaments.verify_dataset(ROOT)
    assert not report["passed"]
    assert any("does not match its event/player" in e for e in report["errors"])
