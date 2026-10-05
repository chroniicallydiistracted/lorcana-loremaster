# Collections, printings, products and purchases

## Two identity layers

Gameplay ownership aggregates official reprints/finishes of the same card identity.
Collector ownership preserves set, collector number, language, art/printing, finish,
variant and condition. A foil and regular copy can fulfill the same deck slot while
remaining different physical collectibles. Never infer a full collection from complete
base-number coverage or assume missing API variants do not exist.

The original personal export is
`data/collections/andys-lore-library-2026-09-15.csv` (915 rows). It contains Set Number,
Card Number, Variant, Count, Name, Color and Rarity. It reflects September 15 holdings,
not later purchases or trades. Preserve these original rows and map identities in a
derived reconciliation rather than silently altering the user's record.

Use `uv run python tools/lorcana.py collection PATH.csv` for exact-name gameplay reconciliation; the migration report maps all 915 rows to 3,296 owned copies. This does not certify physical variant matches. Resolve physical collection entries using printing identifiers and exact names. Normalization
may standardize Unicode punctuation/case, but should not merge different versions or
ambiguous names. Flag unmapped rows and unknown finishes. For decks, distinguish total
owned, already allocated copies, usable copies and missing copies.

## Cost a proposed deck change

1. State the exact list, source/date and format eligibility.
2. Aggregate required copies by identity and subtract confirmed usable owned copies.
3. Match missing copies to exact purchasable printings and condition/finish preferences.
4. Quote current marketplace, currency, observed date/time, shipping, fees and stock.
5. Compare total completion cost and strategic role against the exact cuts/alternatives.

September research includes frozen USD Dreamborn/TCGplayer cache values. Those figures
are historical observations, not October prices or guaranteed sale proceeds. Do not
combine currencies or market/lowest/listed/sold prices without explaining the measure.

## Products and collecting questions

Verify official regional product contents, release dates, eligible cards, special
printing assignment and edition. Distinguish booster packs, starter decks, troves,
gift/collection products, prerelease boxes, promos and cooperative products. A product
name does not establish pack collation or eligibility of every enclosed card.

For odds, use only official disclosures or a transparent measured sample. Do not
invent enchanted rates, print runs or returns from rarity labels. For authenticity,
compare known official printing features and source provenance; photos may support
concerns but cannot provide certainty. Product recommendations should follow the
user's play/collection goals and actual current prices rather than an investment claim.

Sources: official regional product/app pages, printing records and current regional
marketplace product listings. Source attribution must include the exact product.

## Available data services

Use [the provider guide](../method/providers.md) to choose a current access path.
TCGCSV supplies daily product-level price aggregates, Lorcast exposes supplemental
USD fields, and Cardmarket documents public price/catalog downloads. These are
research observations; a purchase quote still needs the actual listing, condition,
language, finish, stock, shipping and fees. Native marketplace product IDs identify
market objects, while the local deck-building ID identifies gameplay equivalence.

Keep regular/foil price rows separate and retain null prices as unknown. Never turn
a missing price into zero, substitute a foil price for a regular copy, or call a
prerelease asking price a completed sale. Quote when the provider updated its data
as well as when we retrieved it. Reconcile the selected product with the card image
before costing a deck's missing copies.

Dreamborn.ink's [current site](https://dreamborn.ink/) advertises deck tools and a
collection-scanning companion app. Our existing CSV is already usable locally;
no additional account or cloud upload is needed to analyze that preserved inventory.

## Collection Quests

A Collection Quest is a collaborative collecting/trading activity. The official
organizer sheet specifies one Quest Card, three boosters matching its set, and a
promo/reward per participant. Players open and trade to complete the collection;
organizers can generously reward participants who do not finish. Exact card goals
come from the matching Quest Card. This activity has its own instructions, separate
from a constructed match or an Illumineer's Quest boss encounter.
[Collection Quest organizer instructions](https://files.disneylorcana.com/Evergreen%20Collection%20Quest%20Organizer%20Instructions.pdf).
