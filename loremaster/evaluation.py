"""Deterministic evaluation of knowledge plumbing, curated claims and uncertainty gates."""

import json
from collections import Counter
from fractions import Fraction

from loremaster.answers import answer
from tools.lorcana import load_identities, probability, resolve


def evaluate(root):
    suite = json.loads((root / "benchmarks/game-master.json").read_text())
    results = []
    cards = load_identities("2026-10-04")
    for case in suite["cases"]:
        failures = []
        if case["kind"] == "answer":
            actual = answer(
                root,
                query=case.get("question", ""),
                topic=case.get("topic"),
                as_of=case.get("as_of", "2026-10-04"),
            )
            if actual["status"] != case["expected_status"]:
                failures.append("Wrong support/date/uncertainty status: " + actual["status"])
            for required in case.get("required_claims", []):
                if required.casefold() not in actual["answer"].casefold():
                    failures.append("Missing expected claim: " + required)
            for sid, section in case.get("expected_sources", []):
                if not any(
                    c["source_id"] == sid and (section is None or c["section"] == section)
                    for c in actual["citations"]
                ):
                    failures.append("Missing source/section: " + sid + " " + str(section))
        elif case["kind"] == "card":
            actual = resolve(case["card"], cards)
            for key, value in case["expected_values"].items():
                if actual[key] != value:
                    failures.append("Incorrect card field: " + key)
            for required in case.get("required_text", []):
                if required not in actual["rules_text"]:
                    failures.append("Missing correct card text: " + required)
            for excluded in case.get("excluded_text", []):
                if excluded in actual["rules_text"]:
                    failures.append("Incorrect card text remains: " + excluded)
            if actual.get("review") is None:
                failures.append("Corrected card lacks review evidence")
        elif case["kind"] == "probability":
            actual = probability(**case["inputs"])
            if actual != Fraction(case["expected_fraction"]):
                failures.append("Wrong exact probability")
        else:
            raise ValueError("Unknown benchmark case type: " + case["kind"])
        results.append(
            {
                "case_id": case["case_id"],
                "domain": case["domain"],
                "passed": not failures,
                "failures": failures,
            }
        )
    return {
        "suite": suite["suite"],
        "scope": suite["scope"],
        "cases": len(results),
        "passed": sum(r["passed"] for r in results),
        "failed": sum(not r["passed"] for r in results),
        "domains": dict(Counter(r["domain"] for r in results)),
        "results": results,
        "limitations": "This checks curated claims, retrieval bindings, corrected card data, exact calculations and refusal gates. It is not a blinded LLM evaluation or proof of comprehensive expert reasoning.",
    }
