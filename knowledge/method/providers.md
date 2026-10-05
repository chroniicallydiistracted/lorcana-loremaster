# Provider access and integration

**Reviewed:** 2026-10-04, America/Phoenix. `sources/providers.json` records 18 providers,
their evidence URLs, access requirements, uses and limits. This is a reviewed routing
catalog, not a claim that every listed service supports all cards, languages or modes.
Official rules/card sources remain in `sources/manifest.json`; supplemental provider
payloads remain separate in `sources/provider-snapshots.json`.

## Choose the service for the question

| Provider | Useful role | Access and qualification |
|---|---|---|
| [Official Resources](https://www.disneylorcana.com/en-US/resources) | Rules, legality, release notes and event terms | Public documents; choose current effective version |
| [Official Card Gallery](https://cards.disneylorcana.com/en-US/?cardId=2876&search=ursula) | Inspect exact card text and printing | Public gallery; public API support contract not verified |
| [Official Companion App](https://www.disneylorcana.com/en-US/app) | Catalog, collection, deck tools, teaching and counters | Mobile app; installed-version behavior/export needs checking |
| [Play Hub](https://www.ravensburgerplay.com/) / [Carde.io](https://support.carde.io/en/articles/14466191-running-an-event-on-carde-io) | Find events; inspect available published standings | Public listings plus player/organizer accounts; publication varies |
| [Ravensburger instructions](https://www.ravensburger.org/dk/produkte/disney-lorcana/gift-sets/disney-lorcana-gateway-11098399/index.html) | Product-specific teaching booklets | Product-linked PDFs; verify title and edition |
| [LorcanaJSON](https://github.com/LorcanaJSON/LorcanaJSON-website/blob/main/index.html) | Enriched bulk data, marketplace ID links, separate Coconut files | Published downloads; prefer compressed files; reconcile against official text |
| [Lorcast](https://lorcast.com/docs/api) | Supplemental card/set/image API | Public beta v0; preserve schema changes and coverage checks |
| [Dreamborn.ink](https://dreamborn.ink/) | Deck building, discovery and collection scanning | Public decks, account tools and app; no public API contract verified |
| [InkDecks](https://inkdecks.com/contact) | Tournament deck discovery | Public pages; verify event/list source and coverage |
| [LorcanaHunter](https://lorcanahunter.com/) | Event and list discovery | Public pages; reconcile upstream IDs and color ordering |
| [Elorcana](https://elorcana.com/) | Player history and large/qualified event discovery | Public fan Elo model with selective event coverage |
| [Lore Guide Institute](https://institute.lorcanajudges.com/) | Rules, teaching and enforcement practice | Free independent training; its badges are not official certification |
| [TCGCSV](https://tcgcsv.com/) | TCGplayer-derived CSV/JSON product and price snapshots | Public daily cache; no condition/language SKU prices |
| [TCGplayer](https://docs.tcgplayer.com/docs/getting-started) | US marketplace observations | New developer API access closed in current docs |
| [Cardmarket](https://help.cardmarket.com/en/cardmarket-api) | Regional marketplace and public bulk price/catalog files | New API applications closed; public downloads are a separate path |
| [CardTrader](https://www.cardtrader.com/en/docs/api/full/reference) | Blueprint IDs and marketplace offers | Bearer-token API; credentials not configured |
| [Ink Table](https://www.inktable.net/) | Solo practice against AI | Fan browser service; current card/interaction coverage untested |
| [TCG Online](https://tcg.online/lorcana/matchmaking) | Online play, practice and replay discovery | Lorcanito's new home; guest watching/practice, account queues; unofficial engine |

Lorcast asks for 50–100 ms between API requests and caching for at least 24 hours.
Its docs suggest weekly gameplay refreshes or refreshes after releases; prices update
daily. Use returned image URIs rather than constructing CDN URLs. Its live objects
include an `inks` array absent from the reviewed card model documentation: verify
payloads before relying on the older singular `ink` field.
[API guidance](https://lorcast.com/docs/api), [card model](https://lorcast.com/docs/api/cards),
[image guidance](https://lorcast.com/docs/api/images).

TCGCSV updates around 20:00 UTC. Products and prices join on `productId`; retain the
price row's `subTypeName`. The provider offers daily price archives from February 8,
2024, but no individual transactions or condition/language SKU observations. Its FAQ
permits processing the public cache and gives a 250 ms request-spacing example.
[TCGCSV overview](https://tcgcsv.com/), [FAQ](https://tcgcsv.com/faq), [documentation](https://tcgcsv.com/docs).

Cardmarket documents publicly downloadable price guides and catalogs; its July 2025
announcement says the files can be incorporated into applications without an API
access request. Direct Lorcana file download was not verified here. Existing API
users must use `apiv2.cardmarket.com` after the 2026 domain migration.
[Public downloads](https://insight.cardmarket.com/en/Articles/whats-new-on-cardmarket-7-2025),
[Lorcana download announcement](https://news.cardmarket.com/en/Lorcana/adding-non-singles-and-accessories-to-the-price-guide),
[API migration](https://apiv2.cardmarket.com/ws/documentation/API_Main_Page).

## Capture and reconcile

```bash
uv run python tools/providers.py list --category prices
uv run python tools/providers.py snapshot lorcast sets
uv run python tools/providers.py snapshot lorcast hyperia-cards
uv run python tools/providers.py snapshot tcgcsv categories
uv run python tools/providers.py snapshot tcgcsv lorcana-groups
uv run python tools/providers.py snapshot tcgcsv hyperia-products
uv run python tools/providers.py snapshot tcgcsv hyperia-prices
```

The commands download only registered public GET endpoints, cache for at least 24
hours, validate response shape, hash raw bytes and retain old snapshots. Failed
requests leave the last valid snapshot intact. A cached snapshot is not a new live
check. No supplemental payload changes cards, corrections, bans or legality policy.
Times are stored in UTC; October 5 before 07:00 UTC is still October 4 in Phoenix.

Raw payloads are excluded from Git. If a checkout lacks a registered snapshot's raw
file, `snapshot` downloads a new observation and retains the earlier hash/time in its
history. It does not claim to have recovered identical historical bytes. An existing
file with a changed hash fails review instead of being silently replaced.

For card reconciliation, join on language, printed set and collector number first,
then check exact name/version and mechanical fields. Keep collector numbers as
strings: promotional values need not be integers. Scope marketplace IDs to their
provider and printing/finish; do not join on a bare name. Put ambiguous, missing and
conflicting matches into review rather than choosing the first candidate. Price
differences do not establish a card-text correction.

The first payload audit is in `reports/provider-coverage-2026-10-04.json`. It checks
the complete Hyperia base-number range, provider/local printing joins and empty
price fields. A provider's date or legality field is an observation to reconcile,
not permission to change our official policy.

## Research and practice requirements

For an event, preserve its native ID, organizer URL, dates, timezone, region, format,
legal pool, match structure, entrant count, stage and result publication scope.
Cross-provider copies of one event are one observation. A partial top-cut list set
can inform role analysis; it cannot supply a field-share denominator.

For online practice, record engine/version, queue format, opponent type, exact list,
play/draw and known interaction defects. Ink Table describes heuristic AI that does
not plan like a human opponent. TCG Online currently exposes different match formats;
an Infinity best-of-one queue cannot establish Core best-of-three matchup evidence.
Check the controlling official rule when a client behaves unexpectedly.
[Ink Table FAQ](https://www.inktable.net/faq), [TCG Online lobby](https://tcg.online/lorcana/matchmaking).

The current stack is sufficient for these integrations: Python, SQLite, PyMuPDF and
the locked validation tools. Add an authenticated or paid provider only when a
specific unmet data requirement justifies it and the user supplies access. Provider
docs do not establish permission to redistribute all underlying art or sell access;
LorcanaJSON's MIT code license and game-asset rights are separate.
