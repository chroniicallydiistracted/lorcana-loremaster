# Web research and guide enrichment

## Context

- Date: 2026-10-04
- Task: Fill knowledge gaps and research useful Lorcana information, services and providers.
- Branch: main (published origin/main; local work authorized).

## Problem Statement

The verified card/rules foundation leaves product-specific teaching and encounter
procedures, narrative coverage, provider access and empirical research incomplete.

## Research

Recovered four original Gateway pamphlets from official Ravensburger instruction
hosts, seven official story/index pages, the app page and Collection Quest organizer
sheet. Reviewed product titles, progression pages, current-rule differences and
narrative attribution. Expanded searches did not acquire the three Quest booklets.

Reviewed 18 providers using primary documentation. Captured six public Lorcast/TCGCSV
payloads separately from official evidence. Lorcast has all 204 Hyperia base numbers
but no populated prices and several field discrepancies. TCGCSV currently has nine
presale sealed products, eight price rows and no Hyperia singles in this snapshot.
New TCGplayer/Cardmarket API applications are closed; public price-file paths and
token-based providers have separate availability limits. No account/payment needed.

## Proposed Solution

Extend product and lore guides; register providers and repeatable read-only snapshots
with cache/provenance/error handling; add reviewed finite answers and benchmark cases.
Keep exact encounter manuals, pack manifests, later lore and measured new-set results
in an explicit next-evidence queue rather than supplying unsupported procedures.

## Status

Completed this research batch. Broader coverage continues through the recorded gaps.

## Implementation Log

### 2026-10-04

Started with clean published `main`. Added 13 official sources: index now 1,025 chunks
across 40 official documents/pages. Added `knowledge/guides/gateway.md` and enriched
learning, story, collection, organized-play and research guidance. Updated routing,
coverage and gap records. Source filenames identify the inspected pamphlets.

Added provider catalog, snapshot registry, `loremaster/providers.py`, CLI, provider
guide, dated coverage report and event-observation template. Downloads use only
registered public endpoints, cache for at least 24 hours and preserve failed-refresh
evidence. Missing ignored raw files can be reacquired as new observations after a
checkout; altered existing bytes fail integrity checks. Historical metadata remains.

Added nine reviewed answers and revised Gateway progression/glimmer continuity:
89 dated records and 109 benchmark cases. Re-read guide-backed claims after edits;
the benchmark caught a stale coverage citation, which was explicitly reviewed and
rebound. Citation-review evidence is recorded rather than silently updating hashes.

Final validation: all eight `tools/verify.py` stages passed; 109/109 benchmark cases,
43 pytest tests, Ruff lint/format, both indexes, provider coverage and card/source/
image integrity. All six supplemental snapshot hashes and `git diff --check` passed.
Preserved collection, saved decks, card corrections/policy and September research.
No additional dependency, credentials, paid service, commit or push performed.

Detailed acquisitions, observations, primary links and next queue:
`reports/web-research-2026-10-04.md`. Exact Quest booklets, Gateway reward manifests,
Hyperia release notes, singles prices, verified current events, later narrative and
localized/regional coverage remain open.
