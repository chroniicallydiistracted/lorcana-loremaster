# Story, lore and Disney connections

Use official Lorcana narrative as the authority for Lorcana continuity: official
articles, published books, attributed card flavor text and official story/product
material. Use Disney/Pixar primary film/book sources for connections to their original
stories. A glimmer's classification or gameplay ability does not prove a narrative
event, biography or identity outside what the source establishes.

## Answering a lore question

1. Identify whether it concerns Lorcana's setting, a character's original film,
   a particular glimmer/version, card art, flavor text, or fan interpretation.
2. Honor the requested spoiler boundary. For a broad introduction default to an
   overview before revealing recent narrative outcomes.
3. Resolve the exact card printing and retrieve its attributed flavor text or art.
4. Find the official narrative article or book edition/page supporting the claim.
5. Separate explicitly published events, artistic references and thematic interpretation.
6. If the complete source is unavailable, state what the available excerpt establishes
   and leave the larger claim open. Do not fabricate a quotation or chapter reference.

Use an explicitly labeled timeline with source and publication date for each event;
publication sequence and in-world chronology are not necessarily identical. Preserve
regional title/translations when relevant without treating them as different lore.

The official Hyperia City page supports its setting and introductory Coco connections.
The official books page is cached as a discovery source; the full books are not stored.
The raw API retains flavor text, art links and search tags across printings. Search
tags are discovery hints, not a fully verified franchise/character ontology.

## Creative assistance

The user may ask for thematic decks, roleplay, a scenario, or a story inspired by cards.
Label invented narrative and house rules as original creative material. Keep gameplay
legal when ordinary play is requested; for an existing thematic list still identify
exact cuts alongside additions. Never present invented plot or mechanics as official canon.

Sources: [Official news](https://www.disneylorcana.com/en-US/news),
[Disney Lorcana books](https://www.disneylorcana.com/en-US/product/books),
[Hyperia City](https://www.disneylorcana.com/en-US/product/hyperia-city), exact official card art/flavor text.

## A sourced introduction

The Great Illuminary is the center of Lorcana. Story stars carry fragments of Disney
stories; an Illumineer uses an inkcaster, magical ink and a lorebook to summon a
glimmer. A glimmer is a version that exists in Lorcana rather than the film character
being transported unchanged. The official introduction also says no ink is inherently
good or evil: heroes and villains appear in all six.
[The First Chapter: The Story Begins](https://www.disneylorcana.com/en-US/story/magic).

The mixed-ink flood changes both storyborn and dreamborn glimmers into floodborn,
giving them unpredictable new forms and power. That published event explains a
narrative category; it does not assign every Floodborn card a particular ability.
[The Roar of Rushing Ink](https://www.disneylorcana.com/en-US/story/roar).

## Reading route and spoiler boundary

The following is a reading sequence, not a complete chronology. Dates are displayed
publication dates on the acquired pages. Several early-set stories were posted on
the same date, so those timestamps cannot order the events in-world.

| Reading | Displayed date | Supported narrative / spoilers | Local source ID |
|---|---|---|---|
| [The Story Begins](https://www.disneylorcana.com/en-US/story/magic) | 2024-09-03 | Setting, Illumineers, inkcasting and glimmers; introductory | `story-first-chapter` |
| [The Roar of Rushing Ink](https://www.disneylorcana.com/en-US/story/roar) | 2024-09-03 | Venturo and Basil encounter the flood; Rise of the Floodborn | `story-floodborn` |
| [When Hope Rose Transformed](https://www.disneylorcana.com/en-US/story/belle) | 2024-09-03 | Belle risks mixed ink to obtain the rose and help Beast; Ursula arc | `story-belle` |
| [The Eye of the Storm](https://www.disneylorcana.com/en-US/story/storm) | 2024-09-03 | Shanzay, Martin and Venturo investigate Ursula's entangled glimmers; four-part Ursula story | `story-storm` |
| [The Missing Piece — An Epilogue](https://www.disneylorcana.com/en-US/story/missing-piece-an-epilogue) | 2024-09-03 | Aftermath at Ursula's abandoned lair, recovery and guarded storage of a Hexwell Crown fragment; outcome spoilers | `story-epilogue` |
| [Azurite Sea](https://www.disneylorcana.com/en-US/story/azurite) | 2024-10-11 | Smee and Alice story previews; retrieve the linked full stories before describing their endings | `story-azurite` |

The [Palace Heist product introduction](https://www.disneylorcana.com/en-US/product/palace-heist)
establishes a later Jafar glimmer reforging the crown and becoming Supreme Sorcerer.
The [Hyperia City introduction](https://www.disneylorcana.com/en-US/product/hyperia-city)
is a separate source for the newest setting. Full connecting narrative, later-set
stories and published books still need individual acquisition and review.

Search the official story snapshots using `tools/knowledge.py search --source
story-storm "Shanzay"`, and search card flavor using `tools/lorcana.py search
"Hexwell" --field flavor`. Resolve art/flavor to a printing before relating it to
these events. A visual parallel can be a supported artistic observation without
proving a new canonical event.
