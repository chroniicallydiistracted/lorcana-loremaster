# Verified knowledge tools

The local tools support Codex's broad Game Master workflow. They retrieve evidence,
apply reviewed card corrections and check deterministic claims. They do not replace
the reasoning standards in `AGENTS.md` or turn missing evidence into expertise.

## Run

```bash
uv sync --frozen
uv run python tools/lorcana.py build
uv run python tools/knowledge.py build
uv run python tools/knowledge.py search --source comprehensive-rules-2.2.0 --section 6.1.7
uv run python tools/knowledge.py search "Temporary Shift" --source comprehensive-rules-2.2.0
uv run python tools/knowledge.py answer "Does Rush let a new character quest?"
uv run python tools/knowledge.py answer --topic current-bans --as-of 2026-10-04
uv run python tools/knowledge.py topics
uv run python tools/knowledge.py benchmark
uv run python tools/verify.py
```

Answers in `data/policy/answer-facts.json` are manually curated, dated and bound to
source bytes. An exact reviewed question or explicit topic returns the reviewed
answer. An unmatched question returns evidence with `needs_interpretation`, for
Codex to analyze using exact cards, rules and game state. There is no fuzzy nearest
FAQ substitution, external model invocation, API key, vector database or generated
matchup simulation behind this command.

## Official rules retrieval

`data/derived/evidence.sqlite` uses SQLite FTS5. Each numbered rule chunk records
the actual PDF page, section, source URL/hash, version, effective date and check date.
Continuation text keeps the same section with its own page. Contents/glossary
references are not treated as body-section headings. Original PDFs control layout.

The index translates only the `LorcanaCardGlyphsRegular` font spans into `{E}`, `{I}`,
`{S}`, `{W}`, `{L}`, `{INKABLE}` and `{MOVE_COST}`. Ordinary quotation marks, dollars
and punctuation remain unchanged. This mapping was checked against rendered pages
and the card-parts definitions. Other extraction ambiguities still require the PDF.

Source or manifest changes invalidate retrieval/answers until rebuilt or reviewed.
Historical dates exclude later-effective documents. Current/future policy answers
require a verification date matching their scope. This is a snapshot gate, not an
automatic assertion that a fetched document remains valid forever.

## Card review lifecycle

The October 4 ledger covers all 137 differing identity groups. Categories overlap:
cosmetic, reminder, naming, classification, functional wording and data errors.
It keeps each implicated printing image and the catalog/source hashes as evidence.
Strict normalization removes only recognized reminder constructions, story labels,
presentation differences and the documented Shift ink-symbol readability update.
Functional differences use explicit inspected-printing/document adjudications.

`identities.raw.jsonl` retains the API retrieval candidates; `printings.jsonl` retains
every raw printing text. `identities.jsonl` and `cards.sqlite` contain the current
reviewed values. `conflicts.json` remains the raw difference inventory. Reviews apply
from October 4, the verified snapshot date, rather than claiming an unsupported
historical correction date. Earlier dates expose raw conflicts. A changed export
or missing/changed evidence makes the affected review stale and restores the review
gate. Unresolved ledger records can never supply a functional override.

`tools/review_cards.py` reproduces this specific inspected export's review and refuses
other catalog hashes. Future exports need new human/agent evidence review; rerunning
this script is not permission to auto-adjudicate unseen text.

## Quality evaluation

`benchmarks/game-master.json` contains 100 source-cited reference cases across rules,
keywords, formats, Limited, new mechanics, multiplayer, cooperative boundaries,
organized play, cards, learning, collections, international questions, lore,
strategy, hidden information, probability and date handling.

The suite checks curated claim content, real citation bindings, corrected card
values, exact probabilities, and uncertainty/refusal status. The independent Python
tests additionally exercise changed source bytes, invalid reviews, effective-date
boundaries, continued PDF sections, glyphs, hostile FTS input and preserved user decks.
These checks do not establish unrestricted question-answer accuracy or competitive
deck strength. A future conversational evaluator needs independent expert grading,
held-out interaction questions and adversarial examples beyond the finite FAQ topics.

## Downloads and next evidence

510 official images are cached: every conflict printing and every Set 14 base card.
The cache is hash-addressed; `tools/download_images.py` verifies existing bytes and
records actual successes/failures. It downloads one functional image per printing,
not foil masks or every collectible treatment.

The source registry also includes the official Quick Start, Quest product pages,
Bucky errata, Hyperia OP instructions, CCQ terms, replacement policy, community code
and CORE Lore Guide training document. CORE means Core Operations, Rules and
Enforcement; this is tournament training, not a narrative storybook.

Exact Quest and Gateway booklets were not found in the public Resources/product
links examined. See `sources/gaps.json` for the acquisition queue. Do not substitute
the ordinary Quick Start or Comprehensive Rules for a scenario rulebook.

Refresh the Resources page and run `knowledge.py watch` to detect new Hyperia rules
or release-note links. It reports candidates without changing policy. Scheduling a
refresh is optional; no background service or system cron job has been installed.

Git tracks tools, guides, reviews, benchmark data, source registries and lockfile.
Large raw exports, official snapshots, derived databases, image bytes, archive and
vendor source remain local and are excluded. Restoring a checkout requires the
supplied raw export and original cached evidence or a newly reviewed source refresh.
