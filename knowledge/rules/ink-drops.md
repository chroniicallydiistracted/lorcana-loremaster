# Hyperia City: ink drops and rules boundary

**Checked:** 2026-10-04. **Set:** 14, Hyperia City. **Evidence:** the supplied official
English card export, official product page and the September 29 ink-drop article.

## Supported introductory behavior

Official preview material says each ink drop provides one temporary ink, can be
used the turn it is made, and is removed from the game after use. Drops can be saved
for later. Cards can generate drops, reward possessing them, or improve an effect
when drops are used to play the card. Treat these as separate roles.

The product page describes drops as temporary ink added to the inkwell. The article
gives ordinary use and augmented-card examples. The exact card condition still
controls: producing a drop, having a drop, and paying with a drop are distinct events.

## What is not yet established here

At this check the official Resources hub still links CR 2.2.0 and release notes up
through Set 13. No Hyperia City release notes or ink-drop CR revision was linked.
Do not invent detailed token characteristics, payment timing, replacement handling,
trigger ordering, interactions with inkwell counts/ready effects or official rule
numbers from introductory marketing text. Retrieve an applicable updated rule or
official ruling for those questions.

## Analysis checklist

1. Retrieve the exact producer, spender and payoff text from Set 14 records.
2. Track available permanent ready ink and temporary drops separately.
3. Check whether generation happens before the intended payment, and whether the
   generation condition can be achieved without assuming a cooperative opponent.
4. Evaluate enhanced and ordinary card modes separately.
5. Compare using a drop now against keeping it for a larger play or a possession payoff.
6. Label any line requiring unsettled timing as conditional; do not present a
   preview-based simulation as rules-engine validation.

Search: `uv run python tools/lorcana.py search "ink drop" --set 14 --limit 50`.
All 204 base numbers are covered; this does not certify every variant or every ruling.

Sources: [Ink Drop Deep Dive](https://www.disneylorcana.com/en-US/news/2026/09/ink-drop-deep-dive),
[Hyperia City](https://www.disneylorcana.com/en-US/product/hyperia-city),
[Official Resources](https://www.disneylorcana.com/en-US/resources).
