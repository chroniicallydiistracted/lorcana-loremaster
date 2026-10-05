# Web research and guide enrichment

**Reviewed:** October 4, 2026, America/Phoenix. Work began on the published `main`
branch. This batch adds product teaching, narrative and provider evidence to the
existing card/rules foundation. It closes specific gaps; it does not establish
complete coverage of every product, language or matchup.

## Official evidence acquired

Thirteen additional official documents/pages are now registered with received-byte
hashes and local snapshots. The evidence index contains **1,025 chunks from 40
official documents/pages**, separate from the supplied English card API export.

| Acquisition | Source IDs | What changed |
|---|---|---|
| Gateway Rules, Guidebook and both Deck Tips | `gateway-rules`, `gateway-guidebook`, `gateway-deck-tips-elsa`, `gateway-deck-tips-stitch` | Exact progression, first-game procedure, reset references and transition to current rules |
| Seven official story/index pages | `story-first-chapter`, `story-floodborn`, `story-azurite`, `story-ursula`, `story-belle`, `story-storm`, `story-epilogue` | Setting, glimmer continuity, early narrative reading route and attributed spoilers |
| Official app page | `official-app` | Publisher-described companion tools; installed app behavior remains untested |
| Collection Quest organizer instructions | `collection-quest-organizer` | Collecting/trading event requirements distinguished from boss encounters |

The controlling Gateway guide was recovered from the publisher's instruction host.
Numeric filenames required inspection: document 241531 is the Guidebook; 241532 and
241533 are Deck Tips. A German-hosted guide URL returned HTTP 503 before the English
Ravensburger.org copy was acquired. PDF titles, text and rendered progression pages
were reviewed. Source paths now match the actual pamphlet titles.
[Gateway Guidebook](https://www.ravensburger.org/spielanleitungen/ecm/Spielanleitungen/241531_11098399_X_web.pdf),
[Gateway Rules](https://www.ravensburger.org/spielanleitungen/ecm/Spielanleitungen/241530_11098399_X_web.pdf).

The [Gateway guide](../knowledge/guides/gateway.md) now explains all four gates and
identifies where the older teaching booklet differs from current ordinary gameplay.
The existing missing-progression answer has become a supported answer. Exact reward
pack membership remains open because the pamphlets refer to lists through QR codes.

The [lore guide](../knowledge/guides/story-and-lore.md) now grounds introductory
answers in official narrative. Its reading route preserves displayed publication
dates separately from in-world chronology and labels outcome spoilers. Seven acquired
pages do not constitute a complete story library or the full published books.
[Official introduction](https://www.disneylorcana.com/en-US/story/magic),
[Floodborn story](https://www.disneylorcana.com/en-US/story/roar),
[Ursula epilogue](https://www.disneylorcana.com/en-US/story/missing-piece-an-epilogue).

The [collection guide](../knowledge/guides/collection-and-products.md) now routes
Collection Quests to the organizer sheet and matching Quest Card. Its source is
separate from the missing Illumineer's Quest encounter booklets.
[Official organizer sheet](https://files.disneylorcana.com/Evergreen%20Collection%20Quest%20Organizer%20Instructions.pdf).

## Provider research and usable integrations

[The provider catalog](../sources/providers.json) and [provider guide](../knowledge/method/providers.md)
document **18 services**, their primary documentation, access requirements and limits.
These cover official resources/app/gallery, regional instructions, event discovery,
supplemental card data, collection tools, marketplace data, independent training and
practice clients. Documentation review is distinct from actually exercising a service.

The new `tools/providers.py` supports registered public GET endpoints, a minimum
24-hour cache, payload-shape validation, hash-addressed raw evidence and retained
previous snapshots. A failed refresh preserves the last valid registry. Cached
responses retain their original retrieval time. Supplemental payloads cannot update
official card text, legality or bans.

When a new checkout lacks the ignored payload files, the downloader can acquire new
observations while retaining historical metadata. It rejects changed bytes in an
existing cache. A fresh observation may differ from the old snapshot; it does not
reconstruct unavailable historical bytes.

Six initial payloads were captured: Lorcast sets and Hyperia cards, plus TCGCSV
categories, Lorcana groups, Hyperia products and Hyperia prices. Actual retrieval times
are stored in UTC in [the snapshot registry](../sources/provider-snapshots.json).
They fall on October 5 UTC and October 4 in Phoenix. Raw payload bytes stay outside
Git, as do existing official snapshots; the registry and coverage report are tracked.

| Observation | Captured result | Implication |
|---|---|---|
| Lorcast Hyperia cards | 206 printing rows; all 204 base numbers; ten local numbered variants absent | Useful secondary completeness check; incomplete collector coverage |
| Lorcast names/stat fields | Five value differences and 44 null/empty subtitle representation differences | Preserve discrepancies for review; do not overwrite the official corpus |
| Lorcast Hyperia prices | No rows with populated price values | No current Hyperia single-card quote from this payload |
| TCGCSV Hyperia products/prices | Nine presale sealed products, eight price rows, no single-card number metadata | Product discovery works; this snapshot cannot cost a Hyperia singles deck |
| TCGCSV joins | No orphan price product IDs; one product without a price row | Missing data stays unknown; retrieval time does not establish an upstream valuation time |

The detailed comparisons and source hashes are in
[the provider coverage report](provider-coverage-2026-10-04.json). Local reconciliation
uses printed set 14 and collector number: 216 numbered printing rows. The broader
API-assigned Hyperia group has 217 rows because an additional Héctor Rivera printing
has no printed set/collector number. This denominator difference is explicit.

Two visible spelling discrepancies were checked against already cached official
images: collector 20 reads **Russell**, and collector 68's version reads **Magical
Market**. Lorcast supplies “Russel” and “Magical Markey.” Other differences include
accented names and a null-versus-zero lore field, whose meaning needs schema review.
No card-text correction was inferred from a price provider or applied to the reviewed
official corpus. Image provenance remains in [the image ledger](../sources/images/manifest.json).

Provider access findings shape the next build:

- Lorcast's beta API asks for request spacing and at least 24-hour caching. Its live
  dual-ink `inks` array needs attention because the reviewed model page still describes
  singular `ink`. Returned image URLs should be used directly.
  [Lorcast API documentation](https://lorcast.com/docs/api).
- TCGCSV supplies public product-level daily caches and historical price archives;
  condition/language SKU prices and individual transactions are absent.
  [TCGCSV FAQ](https://tcgcsv.com/faq), [documentation](https://tcgcsv.com/docs).
- TCGplayer's current developer documentation closes new API access. Cardmarket also
  closes new API applications, while separately documenting public bulk downloads.
  Direct Lorcana Cardmarket file retrieval was not verified. CardTrader requires a
  bearer token; none is configured.
  [TCGplayer access](https://docs.tcgplayer.com/docs/getting-started),
  [Cardmarket access](https://help.cardmarket.com/en/cardmarket-api),
  [public-download announcement](https://insight.cardmarket.com/en/Articles/whats-new-on-cardmarket-7-2025),
  [CardTrader API](https://www.cardtrader.com/en/docs/api/full/reference).
- Play Hub/Carde publication varies by event. InkDecks, LorcanaHunter and Elorcana
  can discover observations; upstream IDs, field coverage and model assumptions need
  verification before statistical claims. The new
  [event observation template](../research/templates/event-observation.json) captures
  provenance, denominators, stages, duplication and unknowns. It is not an event dataset.
  [Play Hub](https://www.ravensburgerplay.com/),
  [Carde event workflow](https://support.carde.io/en/articles/14466191-running-an-event-on-carde-io).
- Independent training and fan practice clients are supplemental. Client output does
  not establish an official ruling or a measured human matchup win rate. TCG Online
  is Lorcanito's current home; verify the queue's format and match structure.
  [Lore Guide Institute](https://institute.lorcanajudges.com/),
  [Ink Table FAQ](https://www.inktable.net/faq),
  [TCG Online lobby](https://tcg.online/lorcana/matchmaking).

The existing locked Python/SQLite/PyMuPDF stack handles this batch. No new dependency,
paid subscription, account creation or credential is needed for the public integrations.

## Review and validation

The answer corpus now contains **89 dated records**. Nine new topics were added;
Gateway progression and glimmer continuity were revised using newly acquired official
evidence. The benchmark grew to **109 cases**. This finite lookup/citation/calculation
pipeline does not evaluate unrestricted expert reasoning.

Guide-backed boundary claims were re-read after the additive edits. Hash changes are
recorded in [the citation review](web-research-citation-review-2026-10-04.json), including
the localized-identity boundary whose stale citation was caught during validation.
Card policy, the preserved collection, saved decks and historical September research
retain their existing meaning and provenance.

Run `uv run python tools/verify.py` for card/index rebuilds, provider coverage,
source/image integrity, benchmark, pytest and Ruff. The current full result is in
[the verification report](milestone-verification.json); benchmark details are in
[the benchmark report](game-master-benchmark.json).

Final validation passed all eight stages: **109/109 benchmark cases**, **43 pytest
tests**, Ruff lint/format, both builds, provider audit and card/source/image checks.
All six supplemental snapshot hashes were also inspected. `git diff --check` passed.

## Next evidence queue

1. Acquire and inspect the exact Deep Trouble, Palace Heist and Great Hunny Rescue
   booklets, encounter boards and difficulty text. Expanded publisher/resource/regional
   searches did not acquire these. Community walkthroughs remain discovery leads.
2. Monitor official Resources for Hyperia release notes and any rules/corrections
   update. Posting card data does not establish those clarifications or legality.
3. Resolve Gateway reward QR destinations and acquire the matching Collection Quest
   cards by edition. Full pack manifests and quest-card objectives are distinct gaps.
4. Extend verified marketplace printing/finish IDs and public bulk-file acquisition
   before computing current deck completion costs. Retry Hyperia singles coverage
   after the cache interval and product release; never turn absent prices into zero.
5. Capture current verified events with the observation template. Keep pre-release
   Hyperia theorycrafting separate from measured Set 14 results; historical Set 13
   research remains frozen. Validate practice-engine interactions before using them
   as implementation evidence.
6. Expand later-set narrative, official books and regional/localized coverage using
   exact editions and sources. Continue distinguishing publication dates from story order.

[The gap registry](../sources/gaps.json) and [coverage matrix](../knowledge/COVERAGE.md)
record the remaining limits. Absence from these searches does not establish that no
public source exists.
