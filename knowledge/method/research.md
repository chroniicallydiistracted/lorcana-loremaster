# Tournament, metagame and testing evidence

Define the question, format, legal environment, region, date window and unit of
observation before collecting data. Preserve source pages and exact lists with
event date, retrieval time, source URL, placement, field size and provenance.

Deduplicate event/list/player records with explicit identifiers. Separate official
registered lists from transcriptions, partial lists and inferred archetypes. A deck
page's last-update date is not necessarily the event date or registration list.

## Denominators and bias

Winner counts describe observed event wins, not field share or game win rate. Top-cut
lists describe published finishes, not every registered participant. Conversion
requires both the field and finish denominators; matchup win rate requires actual
paired results and a clearly defined game/match measure. Do not infer results from
archetype popularity, deck price or a creator's opinion.

Record missing standings, pagination, unknown formats, online versus in-person
events, selection criteria, pilot repetition and field-size weighting. Weighting a
winner by field size does not turn winner-only records into match results.

## Current and new-set interpretation

Use the freshest reliable same-format evidence and state the observation window.
Set 13 evidence is a baseline for surviving roles and expected opponents; it does
not establish Set 14 tiers, matchups or optimized builds. For prerelease work label
package proposals and matchup predictions as theorycrafting, specify balanced list
changes and identify tests that would decide between alternatives.

`research/2026-09-15/` contains a documented Set 13 snapshot: 93 audited events,
75 included wins, exact-list/value exports and explicit exclusions. Its README
explains the limits. Preserve it rather than refreshing the frozen files in place;
create a new dated research directory for new evidence.

## Testing

Use `knowledge/method/testing.md` for exact list versions, opponent list confidence,
play/draw, mulligans, inking, observed turns and results. Keep observations separate
from proposed explanations. Define structural success metrics for goldfish tests.
For matchup tests report sample sizes and uncertainty; do not assert causal advantage
from a few games or from a favorable pilot mismatch.

No measured Set 14 dataset or gameplay simulator was added during this migration.
