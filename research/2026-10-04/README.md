# Core exact-list evidence — October 4, 2026

Purpose: obtain recent public Core lists for concrete deck comparisons and
representative profiles. Window: September 5–October 4 inclusive, using the user's
America/Phoenix date. This purposeful sample is not a census or percentage table.

| Event | Date | Official roster | Provider standings records | Selected lists |
|---|---|---:|---:|---:|
| [Game Grid Open CCQ](https://tcg.ravensburgerplay.com/events/1016280) | October 3 | 95 | 96 | 6 |
| [Spielhöhle Regensburg](https://tcg.ravensburgerplay.com/events/832430) | September 27 | 20 | 25 | 1 |
| [WildCards](https://tcg.ravensburgerplay.com/events/817144) | September 27 | 9 | 19 | 1 |

Official Play Hub pages corroborate Core format, dates and roster counts.
LorcanaHunter supplies selected lists and reported placements. Final official
standings were not visible in the default view; full pairings were not audited.
Regensburg includes zero-record provider rows. WildCards displays both 9/16 players
and 19 standings records. Game Grid's provider location label differs from the
official venue. Retain each discrepancy instead of interchanging denominators.

`events.json` separates inclusions, exclusions and unknowns. An October 7 ICL
discovery entry is excluded as future-dated. `decklists.json` stores eight complete
60-card transcriptions, event/player IDs, canonical identities, URLs, ranks and
snapshot hashes. All pass the supported Core checks. Six representative profiles
cover Elinor, Mickey & Minnie, Retro, Songs, Amber/Amethyst and Emerald/Steel; the
Emerald/Steel list is outside the top cut and supplies no superiority claim.

## Acquisition

Direct Python requests to InkDecks/LorcanaHunter returned HTTP 403, and individual
InkDecks lists also failed through the web tool. Normal public web-tool access to
Hunter lists and official pages supplied evidence; no restriction was bypassed.
Provider prices, curve summaries and matchup widgets are not used as official
card data or measured results.

`snapshots/` holds saved web-tool text excerpts, not original HTML. The tool exposed
no precise origin fetch time. Records distinguish observed date, local
`captured_at_utc` and null `retrieved_at_utc`; capture is not fetch time. Hashes bind
saved excerpts. Large caches remain local outside Git. Restore the exact cache or
perform a newly reviewed refresh to verify a fresh checkout.

```bash
uv run python tools/research.py check
uv run python tools/research.py parse-decks \
  research/2026-10-04/snapshots/recent-decks-1.txt
uv run python tools/review.py --all --as-of 2026-10-04
```

Verification rejects changed excerpts, incomplete/duplicated tables, duplicate
event/player lists, future/out-of-window events, duplicated upstream events,
inconsistent transcriptions, unknown identities and construction failures. It
checks recorded bindings and consistency rather than authenticating players or
certifying finishes.

The sample cannot establish global field shares, conversion or game/matchup win
rates. It contains no Set 14 results. Hyperia is forward-looking until its verified
US October 16 prerelease; later dates and regional event terms need a refresh.
The September 15 historical snapshot is preserved.
