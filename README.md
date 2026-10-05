# Lorcana Loremaster

A local knowledge workspace for Disney Lorcana rules, competitive and casual play,
deck building, Limited, multiplayer, cooperative products, collections, products,
organized play, and story research. Codex uses [AGENTS.md](AGENTS.md) as its operating
instructions and [knowledge/INDEX.md](knowledge/INDEX.md) to find the right evidence.

The **October 4, 2026** snapshot includes the complete **204-card Hyperia City base
set**. Publication in the API does not make new cards tournament legal: the verified
US prerelease is October 16, with wide release October 23. Current Core is Sets 9–13;
Set 14 decks are forward-looking until their effective legality date.

## Use the workspace

Use Python 3.12 or newer and `uv`. The locked project environment includes Pydantic,
PyMuPDF, pytest and Ruff. SQLite FTS5 provides the local evidence search.

```bash
uv sync --frozen
uv run python tools/lorcana.py check
uv run python tools/lorcana.py search "ink drop" --set 14 --limit 30
uv run python tools/lorcana.py show "Madam Mim - Resourceful Trickster" --printings
uv run python tools/lorcana.py deck decks/elinor_moluk_champ.json --as-of 2026-10-04
uv run python tools/lorcana.py probability --population 60 --successes 4 --draws 7
uv run python tools/lorcana.py collection data/collections/andys-lore-library-2026-09-15.csv
uv run python tools/lorcana.py build
uv run pytest -q
```

`search` also accepts `--ink AMETHYST` and `--type character`. `show` accepts an exact
full name or Ravensburger deck-building ID; `--printings` includes raw printing details. Results are JSON for easy scripting.
Use `search "Coco" --field tag` for franchise discovery, or `--field flavor` for
flavor-text searches. Discovery tags are source hints; verify narrative claims.
Deck inputs can be a JSON `cards` list with positive integer quantities, or a text
file with lines such as `4 Mickey Mouse - Brave Little Tailor`. Unknown or ambiguous
identities fail explicitly. Existing user deck files remain in `decks/`.

Deck checks support Core, Infinity, Sealed and Draft. Use `--format sealed --pool
path/to/pool.json` for a personal-pool check. Exit code 0 means the supported checks
passed, 2 means an illegal list or further review, and 1 means an input/tool error.
Unresolved or stale text reviews, missing Limited pools and future/historical policy dates require
review. Passing these checks is not event certification.

## Folder map

| Location | Purpose |
|---|---|
| `AGENTS.md` | Broad expert role, reasoning standards and freshness gates |
| `knowledge/` | Topic guides and reusable analysis methods |
| `data/raw/ravensburger/` | Unmodified supplied official API export |
| `data/derived/` | Rebuildable identities, printings, SQLite index, coverage and conflicts |
| `data/policy/` | Explicit, dated policy and curated rulings |
| `data/collections/` | Original personal collection export |
| `decks/` | Preserved user decks |
| `sources/` | Source registry and official document/page snapshots |
| `research/` | Dated tournament/price evidence and original research code |
| `loremaster/`, `tools/`, `tests/` | Validated review, retrieval, answer and regression tools |
| `benchmarks/` | 109 FAQ/evidence cases plus 24 compound scenario contracts |
| `reports/` | Audit findings, coverage and migration map |
| `vendor/lorcanajson/` | Preserved upstream source, attribution and license |
| `archive/` | Original backup, inventory and superseded knowledge/data |
| `.ai_memory/` | Dated maintenance record |

## Refresh and reliability

Import a new official export with `uv run python tools/lorcana.py import-catalog /path/to/catalog.en.json`.
The importer validates it, preserves the previous raw snapshot, records the new hash,
and rebuilds the indexes. It does not infer new product dates or bans from API fields.
Follow [maintenance.md](knowledge/method/maintenance.md) to update official sources
and policy. The tools make no authenticated requests and need no credentials.

The supplied export's original download timestamp is unknown; its provenance is
recorded as **user-supplied official API export imported October 4**, rather than a
fresh live download. All 14 expansion sets have complete base-number coverage.
All **137 printing-difference groups** have reviewed resolutions for this snapshot;
raw texts and historical uncertainty remain available. **510 official card images**
are cached, including all Hyperia base cards. Missing collector variants remain explicit.
The workspace has no full gameplay engine, measured Set 14 matchup dataset, complete
localized oracle, or complete cooperative rulebook/story-book library. It routes
those questions to their exact sources instead of filling gaps from memory.

See [the audit report](reports/workspace-audit-2026-10-04.md) and
[coverage matrix](knowledge/COVERAGE.md) for the changes and remaining evidence boundaries.

## Retrieve verified answers and rules

```bash
uv run python tools/knowledge.py search --source comprehensive-rules-2.2.0 --section 6.1.7
uv run python tools/knowledge.py answer "Does Rush let a new character quest?"
uv run python tools/knowledge.py topics
uv run python tools/knowledge.py benchmark
uv run python tools/verify.py
```

The evidence index returns actual PDF sections/pages and source hashes. There are
89 reviewed answers. Exact known questions or topic IDs return their sourced answer;
unmatched questions retrieve evidence for Codex to interpret. Future dates or changed
sources trigger review. The 109-case benchmark checks this finite evidence pipeline;
it does not certify unrestricted expert reasoning or deck strength.

Read [the knowledge engine guide](knowledge/method/knowledge-engine.md) for review
lifecycle, rebuilding, source monitoring and current limitations. Git is initialized
locally; large snapshots, image bytes and derived databases remain outside Git.
The [foundation milestone report](reports/verified-knowledge-milestone-2026-10-04.md)
records the original build results. The research report below and coverage matrix
reflect the subsequent source acquisitions and remaining gaps.

## Sourced competitive deck reviews

The [deck-review workflow](knowledge/strategy/deck-review-workflow.md) joins legality,
curve, inkability, exact probabilities, collection gaps and balanced swaps.
[Six concrete archetype profiles](knowledge/strategy/current-archetypes.md) use eight
recent Core lists from three events. Official pages corroborate dates, format and
roster size; lists/finishes remain secondary observations with publication gaps.
They do not establish field shares or matchup win rates.

```bash
uv run python tools/research.py check
uv run python tools/review.py --all --as-of 2026-10-04
uv run python tools/lorcana.py review decks/mickey_minnie_baha.json --as-of 2026-10-04
uv run python tools/lorcana.py mulligan --population 60 --successes 4 \
  --opening-successes 2 --returned 3 --kept-successes 0
uv run python tools/scenarios.py evaluate --output reports/expert-scenarios-2026-10-04.json
```

Read the [Elinor review](reports/deck-reviews/2026-10-04/elinor_moluk_champ.md) and
[Mickey & Minnie review](reports/deck-reviews/2026-10-04/mickey_minnie_baha.md).
Each has six matchup plans and a separate legal candidate. The September inventory
is short nine and 27 copies respectively, or 37 for both simultaneously. Original
user data is preserved. Revised lists are strategic tests without measured advantage.
Changed inputs or sources require re-review.

The [compound evaluation guide](knowledge/method/scenario-evaluation.md) explains
24 new cases, answer-free prompt export and the response format. Reference-assisted
fixtures pass their contracts; independent expert grading remains pending. This
is separate from the 109-case finite FAQ benchmark.

See [the implemented milestone](reports/deck-review-milestone-2026-10-04.md) for
results, verification and the remaining expert/playtesting boundaries.

## Research services and product guides

The [provider guide](knowledge/method/providers.md) documents 18 card, collection,
event, price, training and practice services with access and coverage limits. Public
Lorcast/TCGCSV observations are cached separately from official evidence:

```bash
uv run python tools/providers.py list --category prices
uv run python tools/providers.py snapshot lorcast hyperia-cards
uv run python tools/providers.py coverage
uv run python tools/knowledge.py answer --topic gateway-progression
```

The [Gateway guide](knowledge/guides/gateway.md) now has official booklet/page
references for all four teaching gates. The [lore guide](knowledge/guides/story-and-lore.md)
adds an attributed reading route through the early narrative. See the
[research report](reports/web-research-2026-10-04.md) for acquisitions, provider
payload findings and the next evidence queue.
