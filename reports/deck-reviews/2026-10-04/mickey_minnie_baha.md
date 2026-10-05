# Mickey & Minnie — Baha

Snapshot: 2026-10-04; format: core.

**passes_supported_checks**: 60 cards; 52 inkable / 8 uninkable.

Printed curve: 1: 8, 2: 12, 3: 12, 4: 4, 5: 8, 6: 4, 7: 10, 8: 2.

Inventory snapshot covers 33/60 copies; 27 missing.

Gameplay identities aggregate finishes/reprints. Inventory date appears in the report's collection metadata; no prices or purchase total inferred. Per-deck allocation unless explicitly combined.

## Findings and plan

- The main plan has eight named Mickey bases, twelve named Minnie bases and four Duo payoffs. Joint raw access must include all three groups; simply multiplying their marginal probabilities is incorrect.
- Twenty-four cards have printed cost five or more. Duo Shift, Detective ramp and singing change actual payment, but printed curve alone does not prove a turn-by-turn deployment plan.
- Four Donald Perfect Gentleman have no Donald base in this list, so Shift three is unavailable from these cards alone. Its draw ability is optional for each player and also offers the opponent cards.
- Dr. Bushroot pressures lore and punishes being challenged; its discard ability does not provide immediate on-play removal. Chernabog is an owned option for testing immediate intervention at the same printed cost.
- Ward does not stop challenges or Under the Sea, which does not choose characters. Under the Sea only bottoms opposing characters whose current strength is two or less; verify modifiers before relying on it.
- The list uses character filtering and conditional draw. Protect the distinct bases and usable ink rather than keeping a hand of expensive Ward bodies without an early plan.

## Calculated access

Uniform sampling without replacement. 7/9/10 are cards seen, not turn labels. No mulligan, draw effects, ink choices, deployment, survival or hidden information modeled.

| Target | Copies | Opening 7 | Seen 9 | Seen 10 |
|---|---:|---:|---:|---:|
| one cost characters | 8 | 65.36% | 75.11% | 79.02% |
| characters cost two or less | 16 | 90.08% | 95.20% | 96.71% |
| characters | 54 | 100.00% | 100.00% | 100.00% |
| uninkable | 8 | 65.36% | 75.11% | 79.02% |
| cost five or more | 24 | 97.84% | 99.36% | 99.66% |

Opening with at least three uninkable cards: 4.35%. This is a burden indicator, not a mulligan verdict.

Mickey base / Minnie base / Duo copies: 8/12/4.
Joint access: 7 seen: 17.90%, 9 seen: 29.87%, 10 seen: 35.87%.
Joint raw access to both named bases and payoff; no independence assumption. Not the probability of a legal Shift or a quest on a particular turn.

## Missing gameplay copies

| Card | Needed | Owned | Missing |
|---|---:|---:|---:|
| Donald Duck - Perfect Gentleman | 4 | 0 | 4 |
| Dr. Bushroot - Evil Botanist | 4 | 2 | 2 |
| Hades - Infernal Schemer | 2 | 0 | 2 |
| Mickey Mouse & Minnie Mouse - Adventuring Duo | 4 | 2 | 2 |
| Mickey Mouse - Bob Cratchit | 4 | 0 | 4 |
| Mickey Mouse - Detective | 4 | 2 | 2 |
| Minnie Mouse - Spinning Skater | 4 | 1 | 3 |
| Mushu - Stealthy Dragon | 4 | 1 | 3 |
| Scuttle - Birdbrained | 4 | 3 | 1 |
| Strike A Good Match | 4 | 1 | 3 |
| Under the Sea | 2 | 1 | 1 |

## Candidate: Mickey & Minnie — two-copy Chernabog test

Strategic inference; test before adopting.

Test two immediate on-play removal slots at printed cost five while preserving all eight Mickey bases, twelve Minnie bases, four Duo payoffs and the remainder of the list. The current comparison list uses Chernabog; check the candidate ownership table against the selected inventory before assuming this variant is buildable.

| Card | Change |
|---|---:|
| Dr. Bushroot - Evil Botanist | -2 |
| Chernabog - Unnatural Force | +2 |

Validated 60-card candidate: 50 inkable / 10 uninkable; 25 missing copies.

Tradeoffs: Uninkable count rises from eight to ten and you lose two three-lore Ward bodies. Chernabog chooses an opposing character, so Ward blocks that choice, and its opponent may play a character from their discard for free after a shuffle. It can improve immediate board intervention but may give away too much value.

Test: Compare baseline and candidate against the same opposing list, alternating play/draw and logging mulligan, missed ink, stranded cards, reason for each loss and individual card impact. Use public information only; retain paired game records before claiming improvement. No games have been simulated or measured here. Record specifically whether Chernabog was stranded as uninkable or allowed a strong opposing discard play.

Observed reference: [Narfdre, 2026-10-03, reported #13](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168088/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

## Matchup coaching

All matchup guidance below is strategic inference; adapt to the actual opponent's list and public board.

### Amber/Emerald Elinor

Keep/return: Keep distinct bases and a usable early curve. Keep Duo with a credible route through both bases, rather than duplicate expensive threats.

Ink plan: Preserve at least one base of each name and a route to needed ink. A spare vanilla Ward body is a reasonable ink candidate when the immediate Duo line is stronger.

Sequence and priorities: Inspect strength modifiers before Under the Sea. Disrupt their three-exerted-character engine when profitable; Chernabog can remove a key unwarded engine but the free discard play matters. Peacekeeper can temporarily close challenges without preventing your quests.

Observed opposing lists: [Kezy, 2026-09-27](https://lorcanahunter.com/tournament/16598/spielhohle-regensburg-setmeisterschaft-angriff-der-ranke/player/166030/deck); [BZ, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168094/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

### Emerald/Sapphire Mickey & Minnie

Keep/return: Keep distinct bases, usable ink and relevant interaction. Do not automatically keep two Duo payoffs without bases.

Ink plan: Protect the earliest actual assembly route; ink redundant late bodies before the last required base.

Sequence and priorities: Compare racing a five-lore Duo with disrupting a base. Chosen removal cannot target Ward, while challenges can; banishing Duo creates permanent ink and changes the next-turn resource plan.

Observed opposing lists: [Narfdre, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168088/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

### Amber/Steel Songs

Keep/return: Keep early bases and usable ink; keep a card-flow option when it fits development. Return slow all-payoff hands.

Ink plan: Preserve enough resources to rebuild after mass interaction. Ward bodies are not universally protected from songs.

Sequence and priorities: Singer development signals a possible removal window. Keep separate plans for chosen effects and non-choosing broad effects; use Under the Sea only when current opposing strength meets its condition.

Observed opposing lists: [ItsNotSlowPlay, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168128/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

### Amethyst/Ruby Retro

Keep/return: Keep a coherent early Duo plan and avoid too many high-cost threats.

Ink plan: Preserve recovery access where possible; pay attention to the difference between filtering and net cards.

Sequence and priorities: Pressure before their evolution chain creates efficient threats. A fresh normally played evolved character still has drying restrictions unless another rule or ability changes them. Bounce costs can interrupt your base setup.

Observed opposing lists: [[Ink Pass] LegendGary, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168118/deck).

### Amber/Amethyst character value

Keep/return: Keep early deployment and real resource support for the late game. Return redundant sixes and sevens.

Ink plan: Preserve the path to a threatening board rather than every large body; consider Detective when its ramp matters.

Sequence and priorities: Compare the immediate lore race with removing their value engine. Donald may supply them the missing resource; do not treat symmetric optional draw as a one-sided advantage.

Observed opposing lists: [[LF] Tidus, 2026-09-27](https://lorcanahunter.com/tournament/12941/wildcards-wildcards-attack-of-the-vine-set-championship/player/164930/deck); [Taylor Swift, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168129/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

### Emerald/Steel character tempo

Keep/return: Keep bases and an early play sequence that survives known damage thresholds. Avoid keeping all expensive Ward threats.

Ink plan: Retain flexible ink and replacement bases when visible interaction threatens the first pair.

Sequence and priorities: Track damage scaling from their public board. Ward constrains choosing, not all damage; protect the base whose loss would prevent your Duo line and compare shifting now with developing a replacement.

Observed opposing lists: [JourneyIntoLorcana, 2026-10-03](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168158/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854).

## Archetype evidence

Emerald/Sapphire Mickey & Minnie: 1 selected exact lists.

Assemble both named bases for a free Duo Shift, convert character value into resilient pressure, and use interaction to preserve a questing window.

Observed exact lists support inclusion and copy ranges; role assignments and coaching are strategic inference. Small purposeful sample; no matchup win rates or optimality claim.

- [Narfdre at Game Grid Open - CCQ, 2026-10-03, reported #13](https://lorcanahunter.com/tournament/16854/game-grid-lehi-game-grid-open-ccq/player/168088/deck?lf_set=overall&lf_sort=date_desc&lf_tournamentId=16854); [official event](https://tcg.ravensburgerplay.com/events/1016280).

## Reproduction and limits

Legality and mathematics are deterministic within the source snapshot. Role assignments, mulligans and revisions are authored strategic inference. No gameplay engine, match record, measured win rate or independent expert validation is claimed.

Exact fractions, full lists and SHA-256 input/source bindings are in the adjacent JSON report. Original decks and inventory are preserved.

