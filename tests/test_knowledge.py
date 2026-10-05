"""Behavior checks for evidence binding, dates, correction safety and uncertainty."""

import json
import shutil
import sqlite3

import pytest
from pydantic import ValidationError

from loremaster.answers import answer, facts
from loremaster.evaluation import evaluate
from loremaster.index import retrieve
from loremaster.reviews import overlay
from loremaster.schemas import ReviewLedger
from tools.lorcana import ROOT, build, load_deck, load_identities, read_json, read_jsonl, sha


def minimal_review_workspace(tmp_path):
    catalog = tmp_path / "data/raw/ravensburger/catalog.en.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_bytes((ROOT / "data/raw/ravensburger/catalog.en.json").read_bytes())
    ledger = read_json(ROOT / "data/policy/card-text-reviews.json")
    ledger["records"] = [r for r in ledger["records"] if r["full_name"] == "Bucky - Squirrel Squeak Tutor"]
    for evidence in ledger["records"][0]["evidence"]:
        path = tmp_path / evidence["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            shutil.copyfile(ROOT / evidence["path"], path)
    path = tmp_path / "data/policy/card-text-reviews.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(ledger))
    cards = [
        c
        for c in read_jsonl(ROOT / "data/derived/identities.raw.jsonl")
        if c["full_name"] == "Bucky - Squirrel Squeak Tutor"
    ]
    return cards, ledger


def test_official_image_correction_overrides_bad_promo_data():
    card = next(c for c in load_identities("2026-10-04") if c["full_name"] == "Robin Hood - Ephemeral Archer")
    assert "Whenever this character quests, if" in card["rules_text"]
    assert 'he gains "Whenever' not in card["rules_text"]
    assert card["text_status"] == "reviewed_resolution"
    assert card["review"]["categories"] == ["data_error", "reminder"]


def test_review_does_not_apply_backwards(tmp_path):
    cards, _ = minimal_review_workspace(tmp_path)
    before, report = overlay(cards, tmp_path, "2026-10-03")
    assert before[0]["text_status"] == "requires_review"
    assert report["applied"] == 0
    current, report = overlay(cards, tmp_path, "2026-10-04")
    assert current[0]["text_status"] == "reviewed_resolution"
    assert report["applied"] == 1


@pytest.mark.parametrize("target", ["catalog", "evidence"])
def test_changed_source_invalidates_review(tmp_path, target):
    cards, ledger = minimal_review_workspace(tmp_path)
    relative = (
        "data/raw/ravensburger/catalog.en.json"
        if target == "catalog"
        else ledger["records"][0]["evidence"][-1]["path"]
    )
    with (tmp_path / relative).open("ab") as stream:
        stream.write(b"changed bytes")
    changed, report = overlay(cards, tmp_path, "2026-10-04")
    assert report["applied"] == 0
    assert report["stale"] == [cards[0]["identity_id"]]
    assert changed[0]["text_status"] == "requires_review"


def test_unresolved_review_never_overrides_card(tmp_path):
    cards, ledger = minimal_review_workspace(tmp_path)
    record = ledger["records"][0]
    record.update(status="unresolved", resolved_values={})
    (tmp_path / "data/policy/card-text-reviews.json").write_text(json.dumps(ledger))
    current, report = overlay(cards, tmp_path, "2026-10-04")
    assert current[0]["rules_text"] == cards[0]["rules_text"]
    assert current[0]["text_status"] == "requires_review"
    assert report["unresolved"] == 1


def test_unknown_field_and_overlapping_intervals_are_rejected():
    ledger = read_json(ROOT / "data/policy/card-text-reviews.json")
    ledger["records"] = [ledger["records"][0]]
    ledger["records"].append(dict(ledger["records"][0]))
    with pytest.raises(ValidationError, match="Overlapping"):
        ReviewLedger.model_validate(ledger)
    ledger["records"] = ledger["records"][:1]
    ledger["records"][0]["fields"] = ["text_status"]
    with pytest.raises(ValidationError, match="unknown mechanics"):
        ReviewLedger.model_validate(ledger)


def test_wrapped_rule_reference_is_not_a_section_heading():
    results = retrieve(ROOT, source_id="comprehensive-rules-2.2.0", section="2.2.2.3")
    assert len(results) == 1
    assert results[0]["citation"]["page"] == 10
    assert "shuffles their deck" in results[0]["text"]
    assert len(retrieve(ROOT, source_id="comprehensive-rules-2.2.0", section="2.2.2.1")) == 1


def test_symbol_font_is_transcribed_without_rewriting_ordinary_punctuation():
    results = retrieve(ROOT, source_id="comprehensive-rules-2.2.0", section="8.4.1")
    assert "{I}" in results[0]["text"]
    assert "means “" in results[0]["text"]


def test_section_continuation_keeps_both_original_page_numbers():
    results = retrieve(ROOT, source_id="comprehensive-rules-2.2.0", section="1.10.1.3")
    assert {r["citation"]["page"] for r in results} == {8, 9}
    assert "Amethyst and Sapphire" in " ".join(r["text"] for r in results)


def test_full_text_search_is_parameterized_and_has_real_page_citations():
    hits = retrieve(ROOT, '"; DROP TABLE chunks; --', limit=2)
    assert isinstance(hits, list)
    results = retrieve(ROOT, "Temporary Shift", source_id="comprehensive-rules-2.2.0", limit=30)
    assert any(h["citation"]["section"] == "8.10.8.5" for h in results)


def test_changed_registry_requires_index_rebuild(tmp_path):
    (tmp_path / "sources").mkdir()
    (tmp_path / "data/derived").mkdir(parents=True)
    shutil.copyfile(ROOT / "data/derived/evidence.sqlite", tmp_path / "data/derived/evidence.sqlite")
    (tmp_path / "sources/manifest.json").write_text('{"sources": []}')
    with pytest.raises(ValueError, match="registry changed"):
        retrieve(tmp_path, "Rush")


def test_future_and_historical_answers_require_review():
    for when in ["2026-07-01", "2026-10-16"]:
        result = answer(ROOT, topic="current-bans", as_of=when)
        assert result["status"] == "requires_review"
        assert "No current banned" not in result["answer"]


def test_arbitrary_question_does_not_get_nearest_faq_as_a_ruling():
    result = answer(ROOT, "Rush with an unknown card combo at an unspecified step")
    assert result["status"] == "needs_interpretation"
    assert result["evidence"]
    assert "fact_id" not in result


def test_no_invented_cooperative_rulebook_or_win_rate():
    for topic in ["quest-rulebooks", "hyperia-meta", "simulation", "pack-odds", "current-price"]:
        result = answer(ROOT, topic=topic)
        assert result["status"] == "insufficient_evidence"
        assert result["citations"]


def test_every_curated_citation_resolves_and_dates_are_coherent():
    for fact in facts(ROOT):
        result = answer(ROOT, topic=fact.fact_id)
        assert result["status"] in {"supported", "insufficient_evidence"}, (fact.fact_id, result)


def test_reviewed_saved_decks_pass_supported_checks_without_rewriting_user_data():
    from tools.lorcana import analyze_deck

    cards = load_identities("2026-10-04")
    for path in (ROOT / "decks").glob("*.json"):
        original = sha(path)
        result = analyze_deck(
            load_deck(path, cards), "core", "2026-10-04", read_json(ROOT / "data/policy/legality.json")
        )
        assert result["verdict"] == "passes_supported_checks"
        assert sha(path) == original


def test_snapshot_review_count_and_independent_benchmark():
    ledger = ReviewLedger.model_validate(read_json(ROOT / "data/policy/card-text-reviews.json"))
    assert len(ledger.records) == 137
    result = evaluate(ROOT)
    assert result["cases"] == 109
    assert result["failed"] == 0, [r for r in result["results"] if not r["passed"]]


def test_derived_oracle_retains_raw_text_and_deterministic_rebuild(tmp_path):
    cards, ledger = minimal_review_workspace(tmp_path)
    build(tmp_path)
    assert read_jsonl(tmp_path / "data/derived/identities.raw.jsonl")
    first = sha(tmp_path / "data/derived/identities.jsonl")
    build(tmp_path)
    assert sha(tmp_path / "data/derived/identities.jsonl") == first
    assert cards[0]["conflict_fields"] == ledger["records"][0]["fields"]
    with sqlite3.connect(tmp_path / "data/derived/cards.sqlite") as con:
        assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
