# Rulings, corrections and card-text review

**Verified policy date:** 2026-10-04. This is a review procedure and curated reference,
not a complete oracle or complete historical errata ledger.

## Current policy correction

The current official Tournament Rules are effective July 14, 2026. Section 1.6.2
lists no Core banned cards and Hiram Flaversham – Toymaker as banned in Infinity.
The former bundle's two Core-ban entries were superseded and are archived. Preserve
older policy for historical questions rather than applying today's policy backward.

## Distinguish the cause

- Functional erratum: official behavior/text changes. Record effective date and source.
- Wording/reminder update: wording changes without established functional change.
- Classification update: verify the current classification line and official guidance.
- Localization/alias: map to the same official identity; do not create extra copies.
- Extraction/data mismatch: compare the original source/image before drawing conclusions.
- Rules clarification: explains existing behavior, not necessarily an erratum.
- Ban/rotation: changes eligibility without rewriting card text.

## Resolve a disagreement

1. Retrieve the exact identity and all implicated printing IDs from the generated data.
2. Read the raw API text, official English images and any official correction/release notes.
3. Identify date, applicable rules and the disputed mechanical field.
4. Decide whether the difference is cosmetic, reminder text, an error, an official update,
   or still unresolved. Never choose the newest row solely because it is newest.
5. Record source URL/ID, section/page, effective date, reviewer/date and rationale in
   `data/policy/card-text-reviews.json`. Keep raw printing text unchanged.
6. State the current functional resolution with its source; preserve uncertainty if no
   source decides it. The CLI applies hash-bound, dated resolutions and restores the
   review gate when an export or evidence changes. Historical dates remain explicit.

The API contains 137 identity groups with raw mechanical-field differences at import.
All 137 groups are now reviewed; most differences are presentation or reminder text.
This count is not 137 functional errata. Five groups include verified API data errors.
`data/derived/conflicts.json` is the generated review queue. A candidate with
`api_consistent_unreviewed` means printings agree in this export, not official oracle
certification. `requires_review` means at least one compared field differs.
`reviewed_resolution` means the current ledger resolves the differing fields for its
specific snapshot and date. `conflict_fields` remains the raw difference inventory.

Notable corrections include Bucky's Shift requirement, Winnie the Pooh - Hunny
Wizard's current Hunny classification, Moana's conditional ready/quest text, missing
Sulley abilities, Mickey flavor text misfiled as rules, and Robin Hood - Ephemeral
Archer's incorrect API trigger construction. See each identity's ledger evidence.

Current CR 6.1.7 prohibits choosing Shift during a play instructed as free. The older
Fabled release note's free-Shift example differs; use the higher-priority current CR
for current play and retrieve contemporary rules for historical questions.

## A rules answer

Use exact current card text, identify costs and legal choices, then apply permissions,
limiters, static effects and replacements. Follow the official action/resolution,
game-state-check and bag procedure. Cite the precise CR section and relevant release
note. During an event the Lead Lore Guide decides disputed rulings and remedies.

Ink-drop edge cases require the forthcoming applicable rules/release notes;
see `ink-drops.md`. Do not invent CR numbering or extrapolate from preview prose.

Sources: [Official Resources](https://www.disneylorcana.com/en-US/resources),
[Comprehensive Rules 2.2.0](https://files.disneylorcana.com/Comprehensive-Rules_2.2.0-EN.pdf),
[Tournament Rules](https://files.disneylorcana.com/Tournament-Rules-7.14.2026_Update_EN.pdf).
