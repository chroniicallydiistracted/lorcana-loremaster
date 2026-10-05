# Knowledge and source index

**Workspace revision:** 2026-10-04. **English gameplay baseline:** Comprehensive Rules
2.2.0, effective 2026-07-09. **Tournament baseline:** effective 2026-07-14,
Resources page updated 2026-07-23. This index is the current routing authority.
The previous numbered source bundle is preserved in `archive/knowledge-2026-07/`.

## Retrieve by task

| Task | Start with | Controlling evidence / tool |
|---|---|---|
| How to play, beginner instruction | `guides/learning.md` | Official quick-start and `rules/comprehensive.md` |
| Rules interaction or keyword | `rules/comprehensive.md`, `rules/keywords.md`, `rules/rulings.md` | Current official CR, card text/images, release notes |
| Current or future deck legality | `formats/legality.md` | `data/policy/legality.json`, current TR, event terms; CLI `deck` |
| Core or Infinity deck construction | `strategy/deckbuilding.md`, `strategy/archetypes.md` | Card corpus, applicable format evidence |
| Sealed or Draft | `formats/limited.md` | Exact personal pool and TR 1.3.2 |
| Preconstructed or Pack Rush | `formats/other-formats.md` | Product/event pool; Pack Rush official PDF |
| Multiplayer or Coconut beta | `guides/multiplayer-and-cooperative.md` | CR 9, Coconut rules and app support-card image |
| Illumineer's Quest or Gateway | `guides/multiplayer-and-cooperative.md`, `guides/learning.md` | Exact product and scenario rulebook |
| Mulligan, inking, sequencing | `strategy/mulligan.md`, `strategy/probability.md` | Exact deck, known information and explicit model |
| A particular turn or board state | `strategy/gameplay.md` | Current rules, exact state, player information boundary |
| Matchups, tech, metagame | `strategy/matchups.md`, `method/research.md` | Dated same-format lists and actual game/event observations |
| Collecting, card variants, purchases | `guides/collection-and-products.md` | Printing records, owned export, fresh regional prices |
| Tournaments and Lore Guide procedure | `rules/tournament.md`, `guides/organized-play.md` | Current TR, correction guidelines, official event terms |
| Story, characters, film connections | `guides/story-and-lore.md` | Official narrative, attributed flavor text, book/page references |
| Data refresh or source conflict | `method/maintenance.md`, `method/expert-system.md` | Raw source hash, manifest, conflict record |

All table paths are relative to `knowledge/`. Data/tools paths in prose are relative
to the workspace root. Read only the relevant guides; do not load the entire card
export into context for a simple lookup.

## Primary local sources

- `sources/manifest.json`: URLs, received-file hashes, verification date and provenance.
- `sources/official/2026-10-04/`: official PDFs/pages and extracted PDF text. PDFs
  control if extraction corrupts a symbol, table, heading or card image.
- `data/raw/ravensburger/catalog.en.json`: supplied official English API export,
  imported October 4; original export timestamp unknown.
- `data/derived/identities.jsonl`: one record per deck-building identity, explicit
  raw printing differences, aliases and current reviewed values. `identities.raw.jsonl`
  retains unmodified retrieval candidates; the dated review ledger binds corrections.
- `data/derived/printings.jsonl` and `.csv`: one record per API printing, including
  variant metadata, text, inks, assigned sets and source ID.
- `data/derived/cards.sqlite`: local name/text index, rebuilt from the same source.
- `data/derived/coverage.json` and `conflicts.json`: number coverage and raw mechanical
  field differences. Cosmetic differences can appear here; do not call them errata.
- `data/policy/legality.json`: a dated post-Set-13 policy snapshot, independent of the API.
- `data/policy/rulings.json`: curated official policy/mechanics records, not exhaustive.
- `data/derived/evidence.sqlite`: official source sections/pages, font-aware PDF text
  and SQLite FTS5 search; retrieve with `uv run python tools/knowledge.py search`.
- `data/policy/answer-facts.json`: 80 finite reviewed answers with source/date bindings.
- `sources/images/manifest.json`: 510 downloaded official printing-image records.
- `sources/gaps.json`: exact cooperative/progressive booklet and new-set evidence queue.
- `method/knowledge-engine.md`: tool setup, review lifecycle and evaluation boundaries.

## Date and format boundary

On October 4, current Core is Sets 9–13. Hyperia City's 204 base cards are published
but Set 14 is future-eligible at the US October 16 prerelease under TR 1.6. A same-card
reprint already legal in Core can be used via its older official printing; a genuinely
new Set 14 identity cannot be registered before it becomes eligible. Infinity has
its own banned list and does not use Core rotation.

Current official policy lists **no Core bans** and **Hiram Flaversham – Toymaker in
Infinity**. The old bundle's Hiram/Fortisphere Core-ban entries are historical,
superseded records. Do not restore them from archive or API rotation flags.

Official Hyperia City release notes and a new ink-drop CR version were not linked
from the Resources page at this check. The September 29 official ink-drop article
supports introductory behavior, not every timing edge case. See `rules/ink-drops.md`.

## Evidence and freshness

Apply the subject-specific hierarchy in `AGENTS.md`. Official event terms can
supersede general tournament procedure when authorized; the Hyperia City Set
Championship instructions explicitly do so. No third-party metagame source defines
rules or legality. A source's posting date, effective date, retrieval time and event
date are separate facts.

| Evidence | Recheck when |
|---|---|
| Official rules, keyword definitions, corrections | A rules question needs current/exact treatment, or a new release changes them |
| Legality, bans, release and regional event rules | Before current competitive advice or event registration |
| Metagame, matchup statistics | Every current recommendation; match format, legal pool and date window |
| Prices and stock | Every purchase/value recommendation; retain market, currency, condition, finish and time |
| Owned collection | At the export's date; never assume later purchases/trades are recorded |
| General strategy | When the card pool or game plan changes; it remains inference |
| Story | Verify exact narrative/edition/page; separate published canon from interpretation |

See `COVERAGE.md` for supported work and source gaps.
