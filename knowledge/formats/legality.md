# Format legality and rotation

**Verified snapshot:** 2026-10-04. **Policy:** Tournament Rules effective 2026-07-14.
**Local machine-readable policy:** `data/policy/legality.json`.

## Core and Infinity

Both ordinary Constructed formats require at least 60 cards, at most two ink types
including all inks on dual-ink cards, and at most four copies per full English card
name unless a legal card changes a requirement. There is no maximum deck size if the
player can shuffle promptly without assistance. Core additionally applies rotation;
Infinity admits earlier sets and maintains a separate banned list. (TR 1.3.1.)

| Date / format | Supported pool | Bans in verified policy |
|---|---|---|
| Core on 2026-10-04 | Sets 9–13, including eligible reprint identities | None listed |
| Core from 2026-10-16, conditional on unchanged policy | Sets 9–14 | None listed |
| Infinity on 2026-10-04 | Released eligible cards from Sets 1–13 | Hiram Flaversham – Toymaker |
| Infinity from 2026-10-16, conditional on unchanged policy | Released eligible cards from Sets 1–14 | Hiram Flaversham – Toymaker |

The July policy is effective July 14; the CLI's supported post-rotation environment
begins July 17. It does not attempt to certify earlier formats. Retrieve contemporary
official policy for historical answers. An empty current Core ban list does not make
rotated Hiram or Fortisphere legal absent an eligible reprint.

## Publication, release, and identity

TR 1.6 makes sets legal at hobby-store prerelease. Hyperia City's US product page
lists October 16, 2026 prerelease and October 23 wide release. Verify other regions
and event terms separately. A spoiler, app entry or preview distribution does not
advance its assigned set's eligibility.

When a card is eligible in a format, any official printing of that same card may be
used. Promos and special/preview versions inherit assigned-set release and rotation.
Do not infer reprints merely from a shared character name or art. Use the API's
`deck_building_id`, exact full name and current text, then review any conflict.

`api_rotation_state` is retained as an observed API field, never the final date-aware
legality result. Policy and card data are intentionally separate.

## Construction exceptions

Apply exact current text and CR 1.10, rather than a blanket exception:

- Dalmatian Puppy – Tail Wagger: up to 99 copies.
- The Glass Slipper: no more than two copies.
- Microbots: any number of copies. The API's 99 value is a sentinel, not a printed cap.
- Christopher Robin – Hunny Sage: other Hunny **characters** may be included regardless
  of ink. This does not exempt all Hunny cards or remove ordinary copy/legality rules.

The CLI handles these currently observed modifiers. New/unrecognized modifiers need
review and a targeted implementation/test before automated certification.

## Limited and special modes

Sealed: minimum 40 cards from the personal registered pool, at least six packs under
general TR. Draft: minimum 35 cards from drafted cards, at least four packs. Neither
has ordinary Constructed ink or four-copy restrictions. Verify product composition,
allowed promos and swaps against event terms; do not assume every pool is 72 cards.
Preconstructed and Pack Rush have their own rules; see `other-formats.md`.

Core bans and rotation do not automatically apply to a Limited pool. Encounter-only
Quest cards, marketing inserts and Coconut support cards are not ordinary Constructed
cards. A custom format needs explicitly agreed rules and must be labeled custom.

## Validation workflow

1. Fix the mode, region, event date, event level and applicable special instructions.
2. Confirm the current official policy and snapshot applicability.
3. Resolve every entry to exact identity, full English name and current functional text.
4. Find eligible assigned sets/reprints for that identity at the event date.
5. Apply the correct format's bans and restrictions.
6. Apply exact construction exceptions, then size, colors and full-name copy counts.
7. For Limited, compare every identity and quantity with the registered/drafted pool.
8. Record source hashes, rules/policy versions and unresolved reviews.

Use `uv run python tools/lorcana.py deck PATH --format core --as-of YYYY-MM-DD`. An unresolved
printing difference or unverified date yields `review_required`, not a legal verdict.

Sources: [Tournament Rules](https://files.disneylorcana.com/Tournament-Rules-7.14.2026_Update_EN.pdf),
TR 1.3 and 1.6; [Hyperia City](https://www.disneylorcana.com/en-US/product/hyperia-city).
