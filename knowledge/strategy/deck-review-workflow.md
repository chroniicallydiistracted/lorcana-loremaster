# Sourced deck review workflow

Use the October 4 snapshot for current Core analysis. A different date or format
keeps structural calculations available but suppresses snapshot-specific coaching
and revisions until their evidence is refreshed. Existing Python/SQLite dependencies
are sufficient; this workflow needs no API key or paid provider.

```bash
uv run python tools/research.py check
uv run python tools/review.py --all --as-of 2026-10-04
uv run python tools/lorcana.py review decks/elinor_moluk_champ.json \
  --as-of 2026-10-04 --output reports/my-review
uv run python tools/lorcana.py review path/to/deck.txt \
  --as-of 2026-10-04 --collection path/to/inventory.csv
```

The collection input follows the preserved CSV's Count, Name, Set Number,
Card Number and Variant columns. Alternative inventory files have no inferred
snapshot date; record that date when interpreting results. `--profile` selects a
reference profile ID. `--format sealed --pool path/to/pool.json` checks Limited
quantities. Current curated strategy and proposals are for Core only. Exit 2 means
further review, including a legal unfamiliar deck without a bespoke plan.

## What the review joins

1. Resolve identities from reviewed official data, ignoring embedded export stats.
   Validate size, inks, full-name copy limits, eligibility, bans and Limited pool.
2. Calculate printed curve, inkability, early-character counts, high-cost burden,
   raw access probabilities and joint Mickey/Minnie/Duo access when applicable.
3. Compare copy overlap with eight observed lists. Sixty-percent overlap can route
   to a representative profile; it does not establish strength or optimality.
4. Aggregate owned finishes/reprints into gameplay copies. Report missing identities
   and unmapped rows; keep physical variants and market quotes separate.
5. Apply a reviewed revision only to its exact input SHA and evidence date. Every
   addition has a cut, and every candidate is resolved and checked again.
6. Supply matchup-specific keeps, returns, ink priorities and sequencing as
   strategic inference, with a controlled-testing plan.

The [saved-deck reports](../../reports/deck-reviews/2026-10-04/) include full JSON
lists, exact fractions and input/source hashes. The [six profiles](current-archetypes.md)
identify packages, engines, flex choices, vulnerabilities and observed copy ranges.
Original decks and inventory are preserved. Output paths that replace the input
deck or collection are rejected.

## Calculations

Opening-seven and seen-nine/ten metrics are uniform sampling without replacement.
They do not model mulligans, filtering, conditional draw, ink choices, survival or
turn-specific deployment. Duo access uses inclusion-exclusion over identity unions
rather than multiplying marginal probabilities. A separate reference oracle
enumerates category outcomes; small cases use direct physical-card enumeration.

Conditional mulligans use an actual observed hand:

```bash
uv run python tools/lorcana.py mulligan --population 60 --successes 4 \
  --opening-successes 2 --returned 3 --kept-successes 0
```

Both observed targets are returned. Replacements come from 53 previously unseen
cards containing two targets; access is `153/1378`, or 11.1030%. Returned cards
are unavailable until reshuffling. This is not an unconditional keep-policy model.

Nani's full-list top-four metric is only a reference. At play time subtract known
cards and account for earlier bottom placement/order information. Mike's own
all-character reveal guarantee requires a remaining card; opponents reveal too.

## Extend and test

Create a new dated research folder. Verify event date/format and list completeness;
retain secondary finishes, unknowns, discrepancies and excerpt hashes. Review new
evidence before updating `archetypes.json` and `review-plans.json` bindings. Changed
source bytes invalidate curation. A new deck needs an authored balanced plan after
reviewing roles, resources and opponents; this tool is not an automatic optimizer.

No measured matchup advantage is claimed. Play baseline and candidate against the
same exact opposing lists, alternate play/draw, and log mulligans, missed ink,
stranded cards and decisive turns. For Chernabog, track the new uninkable burden and
the opposing free discard play before adopting the change.
