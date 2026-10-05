"""Compound contracts reject wrong claims, hidden knowledge and misleading provenance."""

import copy
import itertools
import json
from fractions import Fraction
from pathlib import Path

import pytest

from loremaster.deck_review import conditional_mulligan, joint_access
from loremaster.scenarios import evaluate, prompts, reference_probability

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def fixtures():
    return (
        json.loads((ROOT / "benchmarks/expert-scenarios.json").read_text()),
        json.loads((ROOT / "benchmarks/responses/expert-scenarios-2026-10-04.json").read_text()),
    )


def test_prompts_export_excludes_answers_and_rubrics(fixtures):
    suite, _ = fixtures
    output = prompts(suite)
    assert len(output) == 24
    assert all(
        set(p)
        == {
            "scenario_id",
            "domain",
            "as_of",
            "prompt",
            "context",
            "prompt_sha256",
            "response_contract",
            "source_catalog",
        }
        for p in output
    )
    assert all("reference_claims" not in p and "calculations" not in p for p in output)
    questions = {
        q
        for f in json.loads((ROOT / "data/policy/answer-facts.json").read_text())["records"]
        for q in f["questions"]
    }
    assert all(p["prompt"] not in questions for p in output)


def test_fixture_contracts_do_not_claim_expert_certification(fixtures):
    suite, responses = fixtures
    report = evaluate(ROOT, suite, responses)
    assert report["passed"] and report["passed_contracts"] == 24
    assert report["independent_expert_review"].startswith("pending")
    assert "reference-assisted" in report["response_provenance"]


@pytest.mark.parametrize(
    "change", ["probability", "classification", "citation", "hidden", "uncertainty", "prompt"]
)
def test_critical_mutations_fail(fixtures, change):
    suite, responses = fixtures
    bad = copy.deepcopy(responses)
    sample = next(r for r in bad["responses"] if r["scenario_id"] == "conditional-observed-mulligan")
    if change == "probability":
        sample["claims"][-1]["value"] = "1/2"
    elif change == "classification":
        sample["claims"][-1]["classification"] = "official_fact"
    elif change == "citation":
        sample["claims"][-1]["sources"] = ["invented_rule"]
    elif change == "hidden":
        sample["claims"].append(
            {"key": "opponent_next_draw", "value": "Hades", "classification": "official_fact", "sources": []}
        )
    elif change == "uncertainty":
        sample = next(r for r in bad["responses"] if r["scenario_id"] == "event-publication-denominator")
        sample["unknowns"] = []
    else:
        sample["prompt_sha256"] = "0" * 64
    assert not evaluate(ROOT, suite, bad)["passed"]


def test_reference_oracle_matches_exhaustive_independent_enumeration():
    # Direct physical-card enumeration validates the reference category oracle.
    population = ["a", "a", "b", "c", "other", "other"]
    for draws in range(3, 7):
        outcomes = list(itertools.combinations(range(6), draws))
        wins = sum({"a", "b", "c"} <= {population[k] for k in outcome} for outcome in outcomes)
        value = reference_probability({"kind": "disjoint_joint", "arguments": [6, [2, 1, 1], draws]})
        assert Fraction(value) == Fraction(wins, len(outcomes))


def test_runtime_calculators_match_separate_reference_oracle(fixtures):
    suite, _ = fixtures
    for case in suite["cases"]:
        for calc in case["calculations"]:
            if calc["kind"] == "mulligan":
                actual = conditional_mulligan(*calc["arguments"])
            elif calc["kind"] == "disjoint_joint":
                n, groups, draws = calc["arguments"]
                actual = joint_access(
                    {"a": groups[0], "b": groups[1], "c": groups[2], "other": n - sum(groups)},
                    [{"a"}, {"b"}, {"c"}],
                    draws,
                )
            else:
                from tools.lorcana import probability

                actual = probability(*calc["arguments"])
            assert str(actual) == reference_probability(calc)


def test_duplicate_response_rejected(fixtures):
    suite, responses = fixtures
    bad = copy.deepcopy(responses)
    bad["responses"].append(bad["responses"][0])
    with pytest.raises(ValueError, match="Duplicate"):
        evaluate(ROOT, suite, bad)


def test_correct_fields_do_not_certify_contradictory_prose(fixtures):
    suite, responses = fixtures
    contradictory = copy.deepcopy(responses)
    contradictory["responses"][0]["answer"] = "Rush permits this freshly played character to quest."
    # Expose the automatic contract boundary; independent prose review is required.
    report = evaluate(ROOT, suite, contradictory)
    assert report["passed"]
    assert report["independent_expert_review"].startswith("pending")
