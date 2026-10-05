"""Compound-response contracts, separate from the FAQ lookup benchmark.

This grades explicit claims, source bindings and calculations. It does not grade
the meaning of unrestricted prose or substitute for independent expert review.
"""

import hashlib
import itertools
import json
from fractions import Fraction
from math import comb
from typing import Any, Literal

from pydantic import Field

from loremaster.schemas import StrictModel
from loremaster.tournaments import digest


class ResponseClaim(StrictModel):
    key: str
    value: Any
    classification: Literal[
        "official_fact",
        "calculation",
        "strategic_inference",
        "empirical_observation",
        "insufficient_evidence",
    ]
    sources: list[str]


class ScenarioResponse(StrictModel):
    scenario_id: str
    prompt_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    answer: str
    claims: list[ResponseClaim]
    unknowns: list[str]


class ResponseSet(StrictModel):
    schema_version: Literal[1]
    as_of: str
    provenance: str
    responses: list[ScenarioResponse]


def prompt_digest(case):
    public = {k: case[k] for k in ("scenario_id", "domain", "as_of", "prompt", "context")}
    return hashlib.sha256(json.dumps(public, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def prompts(suite):
    return [
        {
            **{k: c[k] for k in ("scenario_id", "domain", "as_of", "prompt", "context")},
            "prompt_sha256": prompt_digest(c),
            "response_contract": {
                "claim_keys": [r["key"] for r in c["reference_claims"]],
                "uncertainty_keys": c["required_unknowns"],
                "claim_fields": ["key", "value", "classification", "sources"],
                "instructions": "Return an explanatory answer and explicit claims for these keys. Choose values and evidence classifications yourself. Cite source catalog IDs; exact probabilities use reduced fraction strings. Copy scenario_id and prompt_sha256. unknowns lists the applicable uncertainty keys.",
            },
            "source_catalog": {
                key: {k: s.get(k) for k in ("path", "url", "section", "page", "selector")}
                for key, s in suite["sources"].items()
            },
        }
        for c in suite["cases"]
    ]


def reference_probability(calculation):
    """Independent oracle: category enumeration rather than runtime inclusion-exclusion."""
    kind, args = calculation["kind"], calculation["arguments"]
    if kind == "mulligan":
        n, k, opening, hits, returns, kept = args
        if kept:
            return "1"
        n, k = n - opening, k - hits
        numerator = sum(
            comb(k, i) * comb(n - k, returns - i)
            for i in range(1, min(k, returns) + 1)
            if returns - i <= n - k
        )
        return str(Fraction(numerator, comb(n, returns)))
    if kind == "access":
        n, k, draws = args
        numerator = sum(
            comb(k, i) * comb(n - k, draws - i) for i in range(1, min(k, draws) + 1) if draws - i <= n - k
        )
        return str(Fraction(numerator, comb(n, draws)))
    if kind == "disjoint_joint":
        n, counts, draws = args
        numerator = 0
        other = n - sum(counts)
        for outcome in itertools.product(*(range(1, min(k, draws) + 1) for k in counts)):
            remainder = draws - sum(outcome)
            if 0 <= remainder <= other:
                ways = comb(other, remainder)
                for k, hits in zip(counts, outcome, strict=True):
                    ways *= comb(k, hits)
                numerator += ways
        return str(Fraction(numerator, comb(n, draws)))
    raise ValueError("Unknown reference calculation: " + kind)


def evaluate(root, suite, responses):
    ResponseSet.model_validate(responses)
    if responses["as_of"] != suite["as_of"]:
        raise ValueError("Response and reference snapshot dates differ")
    for source in suite["sources"].values():
        if digest(root / source["path"]) != source["sha256"]:
            raise ValueError("Scenario evidence changed; re-review references: " + source["path"])
    ids = [r["scenario_id"] for r in responses["responses"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate scenario response")
    cases = {c["scenario_id"]: c for c in suite["cases"]}
    if len(cases) != len(suite["cases"]):
        raise ValueError("Duplicate reference scenario")
    extra = set(ids) - set(cases)
    if extra:
        raise ValueError("Unknown response scenarios: " + ", ".join(sorted(extra)))
    by_id = {r["scenario_id"]: r for r in responses["responses"]}
    results = []
    for case in suite["cases"]:
        problems, actual = [], by_id.get(case["scenario_id"])
        expected = {c["key"]: c for c in case["reference_claims"]}
        for calc in case.get("calculations", []):
            if reference_probability(calc) != expected[calc["claim_key"]]["value"]:
                raise ValueError("Reference arithmetic disagrees: " + case["scenario_id"])
        if not actual:
            problems.append("Missing response")
        else:
            if actual.get("prompt_sha256") != prompt_digest(case):
                problems.append("Response belongs to a different prompt/state")
            if not isinstance(actual.get("answer"), str) or not actual["answer"].strip():
                problems.append("Missing explanatory answer")
            keys = [claim["key"] for claim in actual["claims"]]
            if len(keys) != len(set(keys)):
                problems.append("Repeated claim key")
            claims = {c["key"]: c for c in actual["claims"]}
            if set(claims) != set(expected):
                problems.append("Missing or unsupported factual claim keys")
            for key, reference in expected.items():
                claim = claims.get(key)
                if not claim:
                    continue
                if (
                    type(claim["value"]) is not type(reference["value"])
                    or claim["value"] != reference["value"]
                ):
                    problems.append("Incorrect claim: " + key)
                if claim["classification"] != reference["classification"]:
                    problems.append("Evidence classification mismatch: " + key)
                cited = claim["sources"]
                if not set(reference["sources"]) <= set(cited) or not set(cited) <= set(suite["sources"]):
                    problems.append("Missing or unknown supporting source: " + key)
            if set(actual.get("unknowns", [])) != set(case["required_unknowns"]):
                problems.append("Uncertainty boundary incomplete or different")
        results.append(
            {
                "scenario_id": case["scenario_id"],
                "domain": case["domain"],
                "contract_passed": not problems,
                "errors": problems,
                "independent_expert_review": "pending",
            }
        )
    passed = sum(r["contract_passed"] for r in results)
    return {
        "as_of": suite["as_of"],
        "passed": passed == len(results),
        "passed_contracts": passed,
        "total": len(results),
        "cases": results,
        "response_provenance": responses["provenance"],
        "independent_expert_review": "pending; no independent human/model grade performed",
        "limits": "Finite authored compound cases, outside FAQ question matching. Source hashes, structured claims, classifications and exact numbers are checked; free-text correctness, generalization and competitive strength require independent review. Reference-assisted responses are regression fixtures, not blinded expert evaluation.",
    }
