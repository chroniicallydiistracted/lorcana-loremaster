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
