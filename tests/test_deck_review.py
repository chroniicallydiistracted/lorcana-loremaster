"""Independent counting and regressions for source-bound deck revisions."""

import copy
import itertools
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from loremaster.deck_review import (
    ReviewContext,
    apply_changes,
    conditional_mulligan,
    joint_access,
    metrics,
    quantities,
    write_review,
)
from tools.lorcana import audit_collection, load_deck, resolve

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def context():
    return ReviewContext(ROOT, "2026-10-04")


def test_joint_access_matches_enumeration_with_overlapping_groups():
    population = ["a", "a", "b", "c", "c", "d"]
    counts = Counter(population)
    for groups in [[{"a"}, {"c"}], [{"a", "b"}, {"b", "c"}], [{"a"}, {"b"}, {"c"}], [set()]]:
        for draws in range(7):
            hands = list(itertools.combinations(range(6), draws))
            hits = sum(all(set(population[k] for k in hand) & g for g in groups) for hand in hands)
            assert joint_access(counts, groups, draws) == Fraction(hits, len(hands))


def test_conditional_mulligan_excludes_entire_opening_hand():
    # Twelve cards, four targets. Observe six cards including two targets;
    # return both targets and one miss. Unseen population has two targets, four misses.
    unseen = [True, True, False, False, False, False]
    outcomes = list(itertools.combinations(unseen, 3))
    expected = Fraction(sum(any(x) for x in outcomes), len(outcomes))
    assert conditional_mulligan(12, 4, 6, 2, 3, 0) == expected
    assert conditional_mulligan(60, 4, 7, 2, 3, 1) == 1
    assert conditional_mulligan(60, 4, 7, 0, 0, 0) == 0


@pytest.mark.parametrize(
    "values", [(60, 4, 7, 5, 3, 0), (60, 4, 7, 2, 1, 0), (60, 4, 7, 0, 3, 1), (60, 4, 7, 2, True, 0)]
)
def test_impossible_mulligans_fail(values):
    with pytest.raises(ValueError):
        conditional_mulligan(*values)


def test_changes_require_cuts_and_reject_overcut(context):
    entries = load_deck(ROOT / "decks/mickey_minnie_baha.json", context.identities)
    addition = {"full_name": "Chernabog - Unnatural Force", "delta": 2}
    for changes in [
        [addition],
        [addition, {"full_name": "Dr. Bushroot - Evil Botanist", "delta": -5}],
        [{"full_name": "Chernabog - Unnatural Force", "delta": True}],
    ]:
        with pytest.raises(ValueError):
            apply_changes(entries, changes, context.identities)


def test_both_saved_reviews_and_exact_reference(context):
    for name, missing, inkable in [("elinor_moluk_champ", 9, 44), ("mickey_minnie_baha", 27, 52)]:
        report = context.review(ROOT / f"decks/{name}.json")
        assert report["validation"]["verdict"] == "passes_supported_checks"
        assert report["validation"]["inkable"] == inkable
        assert report["ownership"]["missing_copies"] == missing
        assert len(report["coaching"]) == 6
        assert all(c["sources"] for c in report["coaching"])
        assert not report["review_required"]
        variant = report["variants"][0]
        assert sum(c["delta"] for c in variant["changes"]) == 0
        assert variant["validation"]["card_count"] == 60
        assert variant["validation"]["verdict"] == "passes_supported_checks"
    elinor = context.review(ROOT / "decks/elinor_moluk_champ.json")["variants"][0]
    reference = context.by_list["hunter-16598-166030"]["cards"]
    assert {r["identity_id"]: r["quantity"] for r in elinor["cards"]} == {
        r["identity_id"]: r["quantity"] for r in reference
    }
    baha = context.review(ROOT / "decks/mickey_minnie_baha.json")["variants"][0]
    assert baha["validation"]["uninkable"] == 10
    added = next(c for c in baha["ownership"]["all_cards"] if c["full_name"] == "Chernabog - Unnatural Force")
    assert added["owned"] == 3 and added["missing"] == 0


def test_altered_input_does_not_receive_original_plan(context, tmp_path):
    source = ROOT / "decks/elinor_moluk_champ.json"
    path = tmp_path / "altered.json"
    path.write_bytes(source.read_bytes() + b"\n")
    report = context.review(path)
    assert not report["variants"]
    assert report["review_required"]


def test_stale_strategy_is_suppressed_even_if_structural_checks_pass(context):
    changed = copy.copy(context)
    changed.as_of, changed.fresh = "2026-10-16", False
    report = changed.review(ROOT / "decks/elinor_moluk_champ.json")
    assert report["validation"]["verdict"] == "review_required"
    assert not report["variants"] and not report["profile"] and not report["coaching"]


def test_card_metrics_ignore_cached_deck_properties(context):
    entries = load_deck(ROOT / "decks/mickey_minnie_baha.json", context.identities)
    result = metrics(entries)
    assert result["target_counts"]["characters_cost_two_or_less"] == 16
    assert result["duo_three_part_access"]["base_and_payoff_counts"] == [8, 12, 4]
    assert quantities(entries)[resolve("Under the Sea", context.identities)["identity_id"]] == 2


def test_report_cannot_overwrite_its_input(context):
    path = ROOT / "decks/elinor_moluk_champ.json"
    before = path.read_bytes()
    report = context.review(path)
    with pytest.raises(ValueError, match="overwrite an input"):
        write_review(report, path.parent, path.stem)
    assert path.read_bytes() == before


def test_custom_collection_is_used_without_inventing_its_date(context, tmp_path):
    custom = copy.copy(context)
    path = tmp_path / "andys-lore-library-2026-09-15.csv"
    path.write_text("Count,Name,Set Number,Card Number,Variant\n")
    custom.collection_path = path
    custom.collection = audit_collection(path, context.identities)
    report = custom.review(ROOT / "decks/mickey_minnie_baha.json")
    assert report["collection"]["snapshot_date"] is None
    assert report["ownership"]["missing_copies"] == 60
    assert report["variants"][0]["ownership"]["missing_copies"] == 60


def test_changed_strategy_binding_requires_curation_review(monkeypatch):
    import loremaster.deck_review as review

    actual_digest = review.digest
    monkeypatch.setattr(
        review, "digest", lambda p: "0" * 64 if str(p).endswith("legality.json") else actual_digest(p)
    )
    with pytest.raises(ValueError, match="Strategy source changed"):
        ReviewContext(ROOT, "2026-10-04")
