# Sourced deck-review milestone — October 4, 2026

The recommended build is implemented locally: recent event/list evidence,
concrete archetype profiles, collection-aware reviews of both saved decks,
balanced candidate exports and a separate compound scenario evaluation workflow.
The existing Python/SQLite stack was sufficient; no extra service, paid access,
external model API or background job was installed.

## Delivered evidence and guides

- [Recent research snapshot](../research/2026-10-04/README.md): three Core events,
  eight complete 60-card lists, one excluded future event. Official Play Hub pages
  corroborate event date, format and roster; exact lists and finishes are secondary
  reports. Roster discrepancies and incomplete standings/pairings are retained.
- [Six archetype profiles](../knowledge/strategy/current-archetypes.md): Elinor,
  Mickey & Minnie, Retro, Songs, Amber/Amethyst and Emerald/Steel. Each includes
  packages/engines, flex choices, vulnerabilities, resource/mulligan plans, sourced
  lists and observed copy ranges. Roles and coaching are strategic inference.
- [Review workflow](../knowledge/strategy/deck-review-workflow.md): joins current
  canonical identities, legality, curve, inkability, exact access calculations,
  ownership, copy-overlap references and source-bound balanced revisions.
- [Compound evaluation](../knowledge/method/scenario-evaluation.md): 24 questions
  beyond FAQ matching, answer-free prompt export, response contracts, exact source
  bindings, an independent probability oracle and critical-mutation regressions.

## Saved-deck results

| List | Cards | Inkable / uninkable | Missing September copies |
|---|---:|---:|---:|
| [Elinor baseline](deck-reviews/2026-10-04/elinor_moluk_champ.md) | 60 | 44 / 16 | 9 |
| [Elinor Kezy comparison](deck-reviews/2026-10-04/elinor_moluk_champ--kezy-comparison.json) | 60 | 44 / 16 | 9 |
| [Mickey & Minnie baseline](deck-reviews/2026-10-04/mickey_minnie_baha.md) | 60 | 52 / 8 | 27 |
| [Mickey & Minnie Chernabog test](deck-reviews/2026-10-04/mickey_minnie_baha--chernabog-test.json) | 60 | 50 / 10 | 25 |

Both baselines and candidates pass supported October 4 Core checks. Both reviews
include six matchup-specific mulligan, ink and sequencing plans with opposing-list
references. Original deck/collection files are preserved; candidates are separate
JSON files. Output cannot replace the input deck or collection.

Elinor's eight-for-eight comparison exactly matches Kezy's reported September 27
winning list. It trades selected flex cards for Rapunzel bounce, Squeaks evasion and
additional Ursula/Thomas copies. It is a sourced alternative, not a strict upgrade.

The smaller Mickey & Minnie test cuts two Dr. Bushroot and adds two Chernabog.
The original export owns three Chernabog. It trades lore/Ward bodies for immediate
chosen shuffle removal, with the opposing free discard play and higher uninkability
as costs. Opening-seven probability of three or more uninkable cards rises from
4.3457% to 8.3042%. No measured performance advantage is claimed.

Mickey/Minnie/Duo raw joint access is 17.8975% in seven cards, 29.8741% in nine and
35.8671% in ten. These are uniform draw-only access rates, not legal Shift/quest
probabilities. Conditional observed-hand mulligans exclude every original hand
card from replacement draws; this is separate from an unconditional keep policy.

[Combined baseline ownership](deck-reviews/2026-10-04/combined-ownership.json) is
short 37 copies, rather than the independent gaps' sum of 36: both decks otherwise
allocate the same owned Mushu. Custom inventories produce their own counts and
receive no inferred September date. No prices or purchase totals were invented.

## Verification

`uv run python tools/verify.py` passed all **11 stages**:
card/evidence rebuilds, supplemental coverage, workspace and tournament checks,
both review exports, **109/109 FAQ benchmark cases**, **24/24 compound contracts**,
**74 Python tests**, Ruff lint and formatting. See [the complete verification
record](milestone-verification.json) and [scenario report](expert-scenarios-2026-10-04.json).

Tests independently enumerate small populations and cross-check runtime joint
probabilities against category counting. They reject impossible mulligans,
unbalanced/over-cut revisions, stale strategy sources, altered inputs, incomplete
tables, duplicate/future events, wrong event/player bindings, incorrect scenario
numbers/citations/classes and hidden-information claims. Input-overwrite protection,
custom inventory semantics and the prose-grading boundary are also covered.

[Citation re-review](deck-review-citation-review-2026-10-04.json) records the four
finite answers affected by guide changes and the reviewed strategy-prose revision.
[Memory Bank](../.ai_memory/deck-review-workflow.md) records implementation and checks.

## Remaining evidence boundaries

The 24 responses are authored, reference-assisted regression fixtures. Independent
expert/human grading and independently generated prose evaluation have not been
performed. The harness is operational but does not certify unrestricted expertise;
correct structured fields can coexist with wrong prose, which requires review.

The tournament sample is purposeful and cannot establish global metashare or
matchup win rates. No gameplay simulator or paired playtesting was run. Hyperia
remains theorycrafting before its verified October 16 US prerelease; the existing
Sets 9–13 evidence is not Set 14 result data. Later dates require a policy/evidence
refresh. Cooperative booklets, localized texts and full lore books retain their
documented acquisition gaps.

The next competitive validation is controlled baseline-versus-candidate play with
exact opposing lists, alternating play/draw and logging resource failures and
decisive turns. The files and hypotheses are ready for that work without representing
those games as already played.
