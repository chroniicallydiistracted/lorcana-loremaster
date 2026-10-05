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

## Current provider research route

The October 4 follow-up [provider audit](providers.md) checks live services and
documentation rather than relying on the archived web directory. Start event discovery
with the Ravensburger Play Hub, then use InkDecks, LorcanaHunter or Elorcana to find
lists and upstream results. Record discovered candidates before treating them as
included observations. Their interface labels and summary statistics do not supply
missing event evidence.

Use the `research/templates/event-observation.json` record to preserve format,
registration/list timing, stage, field and published-list denominators. Leave absent
data null. Inclusion requires an event date inside the selected observation window,
a verified format and an identifiable source; unknowns stay in the candidate queue.
An October 4 scan of product and card services is not a measured Hyperia metagame.

For practice, use the engine and opponent qualifications in the provider guide and
the logging requirements in `testing.md`. Client results and AI practice can identify
questions to test, but remain distinct from verified in-person paired results.

## October 4 exact-list sample

[`research/2026-10-04/`](../../research/2026-10-04/) adds three recent Core events
and eight selected complete lists, with event dates/format corroborated officially.
Lists and reported finishes come from LorcanaHunter. Official final standings and
complete pairings remain unverified; roster discrepancies are retained. An October 7
discovery row is excluded as future-dated. This purposeful sample is neither global
metashare nor matchup win-rate evidence.

[Concrete profiles](../strategy/current-archetypes.md) and the
[deck-review workflow](../strategy/deck-review-workflow.md) supply source-bound
comparisons, exact calculations and balanced hypotheses. Current Core uses Sets
9–13. There is still no verified Set 14 field or matchup dataset; Hyperia proposals
remain theorycrafting.
