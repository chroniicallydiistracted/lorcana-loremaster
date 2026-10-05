# Workspace audit and migration — October 4, 2026

## Outcome

The project now has a broad Lorcana Game Master remit: rules, Core/Infinity, Limited,
casual/multiplayer/cooperative play, teaching, gameplay coaching, collections,
products, organized play and story/lore research. It retains the original competitive
decision standards and adds explicit format, date, region and evidence gates.

The English API export has been indexed into gameplay identities and physical
printings, with dated policy maintained separately. All 204 Hyperia City base numbers
are present. The raw export is user-supplied; its original retrieval time is unknown.
No live authenticated API download is claimed.

## Entire original folder: inspection scope

Inventoried and hashed all **333 original files**, totaling **62,128,794 bytes**.
Checked JSON/CSV parsing, all 53 Python files' syntax, both SQLite databases'
integrity/schema, the original document structure, code/path dependencies, source
baselines, card and collection schemas, deck inputs, upstream source/license and
dated research methodology/results. No original parse, syntax or database-integrity
failure was found. HTML/text captures were classified as frozen source evidence;
this audit does not claim every historical page was freshly corroborated online.

The original folder was not a Git repository and had no project-level test/build
workflow. A complete pre-edit archive and per-file hashes were created before moving
or revising anything. No historical tournament scripts were run to overwrite results.

## Findings and revisions

| Finding | Revision |
|---|---|
| Root instructions restricted the agent to Core Constructed | Replaced with broad Game Master role and topic-specific routing |
| Active index and reasoning rules fixed the environment to Set 13 | Date-aware current/future pools; general Limited and new-set workflows |
| Old enriched catalog had 3,226 rows while supplied API already included Set 14 | Archived historical merged export; rebuilt current retrieval from 3,515 official API records |
| Index referenced two absent identity/current-text CSVs | Replaced those references with generated identity/printing tables and explicit conflict status |
| Old bundle asserted Hiram and Fortisphere were current Core bans | Corrected from July 14 official TR: no current Core bans, Hiram banned in Infinity |
| API already labels future Set 14 records CoreConstructed | Date gate uses official product prerelease and TR, independently of that field |
| No reproducible card retrieval, deck-check or probability workflow | Added standard-library CLI, SQLite/JSONL/CSV outputs and behavioral regression tests |
| Original Sealed audit demanded six Set 13 packs and 72 cards | Uses the actual supplied pool/product; six-pack Set 13 example remains historical context |
| Reusable Limited guide referred to color-splash cost | Corrected: Lorcana ink payment is not color-specific; evaluate synergy/opportunity cost |
| Inherited digest had misnumbered zone/activated-ability citations | Corrected against current official CR section headings |
| Pack Rush quick sheet and current CR describe reshuffle timing differently | Preserved discrepancy and routed exact timing to current CR 10.2.5 |
| September prices/results could be mistaken for current Set 14 evidence | Marked frozen Set 13 research; new snapshots use separate dated folders |
| Upstream OCR code mixed with core knowledge | Moved intact under vendor with license and source boundaries |
| Browser captures mixed with active project root | Preserved in archive; original complete backup also retains them |
| No breadth coverage or freshness boundaries | Added 27 topic/index/method documents and a coverage matrix |

## Data and preservation

- **3,515** API printing records; **2,784** deck-building identity groups.
- All **14 expansion sets** have complete base-number coverage in this export.
- Hyperia City: **204/204** base numbers, **217** printing records; collectible variant
  completeness is unknown, as the user cautioned.
- **137** identity groups have raw mechanical-field differences across printings.
  Many can be cosmetic/reminder differences; this is not a count of functional errata.
- **27** Coconut support records retained separately as image/name metadata.
- All **915** personal collection rows resolved by exact normalized gameplay name,
  totaling **3,296** copies. This does not certify physical variant matches.
- Both saved decks retain exactly their original bytes and quantities. Both have
  60 cards and pass supported size/ink/eligibility/copy checks at October 4. They
  still require printing-text review; see the saved-deck check report.
- Raw API bytes, original collection bytes, user decks and vendored upstream files
  are preserved; original hashes and the complete tar backup make the move reviewable.

## Official verification

The live Resources hub, current CR/TR, release notes through Set 13, Pack Rush,
Coconut rules/list, correction guidelines, Hyperia City product/ink-drop article,
Hyperia City Set Championship instructions and book/Gateway/Quest product discovery
pages were retrieved into the source registry. PDFs have extracted text for search;
the official tournament rotation/ban page was also checked visually.

The verified US Hyperia City prerelease is **October 16, 2026**, wide release
**October 23**. New Set 14 identities are future-eligible until prerelease, under the
verified TR. No Hyperia City release notes or updated ink-drop CR were linked in the
Resources hub at verification; the official introductory article does not establish
all token/timing edge cases.

Sources: [Official Resources](https://www.disneylorcana.com/en-US/resources),
[Tournament Rules](https://files.disneylorcana.com/Tournament-Rules-7.14.2026_Update_EN.pdf),
[Hyperia City](https://www.disneylorcana.com/en-US/product/hyperia-city),
[Ink Drop Deep Dive](https://www.disneylorcana.com/en-US/news/2026/09/ink-drop-deep-dive).

## Validation and limits

All **19 regression tests pass**. The regression suite covers exhaustive small-population probability outcomes,
Unicode JSONL separators, base coverage, prerelease gates, reprints, format-specific
bans/rotation, full-name copy aggregation, Microbots/Puppy/Slipper limits, dual inks,
the Hunny exception, encounter-card exclusion, Limited quantities, unknown identities,
invalid counts, future/historical policy review, text conflicts, saved decks,
deterministic rebuilds and invalid-import preservation.

Source hashes, generated counts, SQLite integrity and documentation references were
checked. See `validation-2026-10-04.json` for the final run. Smoke checks exercised
name/rules, flavor and franchise searches, printing retrieval, both decks, collection
reconciliation, exact probability and Resources discovery.

Remaining source boundaries are explicit in `knowledge/COVERAGE.md`: incomplete
collector variants/localized oracle, unresolved text reviews, no complete cooperative
scenario booklets or story-book library, no measured Set 14 meta/matchup dataset and
no full gameplay simulator. These need source retrieval for the specific question;
they do not justify guessing.

## Review and recovery

- Start: `README.md` and `knowledge/INDEX.md`.
- File moves: `reports/migration-map.json`.
- Original inventory: `archive/original-inventory-2026-10-04.json`.
- Original complete backup: `archive/original-workspace-2026-10-04.tar.gz`.
- Source dates/hashes: `sources/manifest.json`.
- Future maintenance: `knowledge/method/maintenance.md`.
# Follow-up milestone

This migration audit records the workspace before the verified-knowledge build.
Its open text-review, dependency and indexing items are superseded by
[the completed milestone](verified-knowledge-milestone-2026-10-04.md).
