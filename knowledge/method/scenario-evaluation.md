# Compound scenario evaluation

The 24 cases in `benchmarks/expert-scenarios.json` combine rules, calculations,
deck revisions, hidden information, event denominators, inventory allocation,
lore continuity, missing prices and cooperative-source boundaries. Their prompts
differ from all 89 FAQ questions. They form a separate suite from the existing
109-case answer/retrieval benchmark.

References bind exact official rule sections/pages, card bytes and their review
ledger, decks/collection and dated research. Probability references use a separate
category-counting implementation, checked against physical-card enumeration and
the runtime calculators. This is reference-based regression, not expert grading.

```bash
uv run python tools/scenarios.py prompts --output reports/scenario-prompts.json
uv run python tools/scenarios.py evaluate \
  benchmarks/responses/expert-scenarios-2026-10-04.json \
  --output reports/expert-scenarios-2026-10-04.json
```

## Independent responses

Export prompts first. They contain questions, state, source locations and required
claim/uncertainty key names. Reference values, classifications and calculation
answers are omitted. These protocol hints make the evaluator usable; it is not a
blinded test of discovering every uncertainty. Give the respondent the export and
original sources, without the reference suite or existing response fixtures.

Save responses in this envelope, using actual generation provenance:

```json
{
  "schema_version": 1,
  "as_of": "2026-10-04",
  "provenance": "Respondent, date, available tools/sources and procedure",
  "responses": [
    {
      "scenario_id": "copy from prompt",
      "prompt_sha256": "copy the prompt hash",
      "answer": "Explain the action, alternatives and limits.",
      "claims": [
        {"key": "required claim key", "value": true,
         "classification": "official_fact", "sources": ["source catalog ID"]}
      ],
      "unknowns": []
    }
  ]
}
```

Use the required keys, appropriate JSON value types and reduced fraction strings
for exact probabilities. Evidence classes are `official_fact`, `calculation`,
`strategic_inference`, `empirical_observation`, or `insufficient_evidence`.
An independent reviewer should separately assess prose, action/target legality,
source relevance, alternatives, player-view information, spoilers and unsupported
claims. Record reviewer/date/verdict/rationale/corrections separately; the automatic
report keeps expert grading pending.

## Score boundaries

The harness rejects missing/extra/duplicate cases or claims, wrong prompt hashes,
incorrect explicit values, mismatched evidence classes, missing/unknown citations,
changed sources and omitted uncertainty markers. Tests mutate arithmetic,
citations, evidence classes and hidden knowledge. A reference arithmetic conflict
fails the suite itself instead of grading against a bad reference.

The 24 current responses are Codex-authored, reference-assisted fixtures. Their
24/24 result verifies this pipeline on those fixtures. It does not establish
independently generated answer accuracy, unrestricted prose correctness, measured
deck strength or expert certification. No external model API or independent human
grade was run. Contradictory prose with correct structured fields needs substantive
review; the automatic evaluator cannot detect that mismatch.
