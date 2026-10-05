# Verified knowledge milestone

Implemented the authorized first build milestone for the broad Lorcana Game Master.
This follows the workspace migration audit and supersedes its open printing-review
and dependency/index work items. Existing raw export, collection and deck bytes were
verified against the original inventory and preserved.

## Delivered

- Local Git repository on `main`; code, guides, policies, source registries, benchmark
  and lockfile tracked. Large local evidence/cache/archive files are excluded.
- Python 3.12 project environment through uv with frozen dependency resolution:
  Pydantic 2.13.5, PyMuPDF 1.28.2, pytest 9.1.1 and Ruff 0.16.10. No API keys required.
- Strict schemas for mechanics, source records, citations, dated reviews and answers.
- All 137 raw printing-difference identity groups resolved for the October 4 snapshot.
  Cosmetic/reminder/name differences are separated from functional wording,
  classification changes and five verified API data-error groups. Categories overlap.
- 510 official printing-image records downloaded successfully, with zero missing or
  failed requests. This includes all 204 Hyperia base cards and every conflict printing.
- Dated, catalog/source-hash-bound correction application with raw identity candidates
  and printing texts retained. Earlier dates, changed snapshots and unresolved reviews
  preserve review gates. Bucky's known August 9, 2024 official errata date is separately
  recorded; verified oracle applicability begins at this snapshot rather than inventing
  a complete historical text database.
- 27 cached official documents/pages, including new Quick Start, Bucky errata,
  Quest product pages, CORE Lore Guide training, event instructions, community and
  replacement policy sources. Supplied API export remains a separate source.
- 943 searchable official evidence chunks using SQLite FTS5, with PDF page/section,
  source URL/hash, version, effective date and check date. Font-aware transcription
  preserves Lorcana symbols; section continuations keep their original page numbers.
- 80 manually curated, dated source-cited answers. Exact questions or topic IDs return
  reviewed answers; arbitrary questions retrieve evidence for interpretation. There
  is no hidden model invocation or general gameplay simulator.
- Source monitoring command for newly linked Hyperia rules/release notes; policy
  changes remain explicit reviewed work.
- 100 source/claim/card/calculation/uncertainty reference cases across the project's
  subject areas, plus lifecycle and behavioral regression tests.

Both original saved decks pass supported October 4 Core checks after applying the
reviewed text. Their quantities, identities and file bytes are unchanged. Raw API
text and original collection bytes also match the original inventory.

## Verification

`uv run python tools/verify.py` passed all seven stages: catalog build, evidence build,
source/image/catalog checks, 100/100 benchmark cases, 37 pytest tests, Ruff lint and
Ruff formatting. CLI smoke checks confirmed real section/page citations, reviewed
card data, saved-deck metrics and future-date review behavior.

Machine-readable results: `milestone-verification.json`, `game-master-benchmark.json`,
`card-text-review.json`, `image-downloads.json`, `evidence-index.json`,
`reviewed-saved-decks-2026-10-04.json`, and `user-data-preservation.json`.

## Explicit remaining source boundaries

The exact Deep Trouble, Palace Heist, Great Hunny Rescue and Gateway progressive
booklets were not discovered in the official public links examined. Their product
pages are cached; no ordinary rules PDF was relabeled as a scenario booklet.
`sources/gaps.json` records the acquisition queue and search scope.

The checked Resources hub still links release notes through Set 13 and CR 2.2.0;
no Hyperia rules/release notes were linked at this check. Introductory ink-drop
behavior is sourced, while unspecified edge cases require the applicable publication.

There is no measured Hyperia matchup dataset, complete localized/collector oracle,
complete book library, full gameplay engine or unrestricted conversational evaluation.
The 100-case benchmark verifies this finite evidence pipeline; it does not establish
expert-level performance on every possible question or prove a deck optimal.

## Use and continue

See `README.md` and `knowledge/method/knowledge-engine.md` for commands and lifecycle.
Refresh official sources, inspect changes, rebuild evidence, re-review affected claims
and run the complete verification command before current advice depends on a new
snapshot. Keep live empirical research in a new dated directory.
