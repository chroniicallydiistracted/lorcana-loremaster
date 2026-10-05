# Maintaining a reliable workspace

## Refresh a set or catalog

1. Obtain an official English export through the user's authorized source. Record
   actual retrieval time if known; otherwise record local import time and unknown
   original retrieval. Never invent a fresh live API check from a file's mtime.
2. Run `uv run python tools/lorcana.py import-catalog /path/to/catalog.en.json`. The importer
   validates before replacing raw data and preserves the previous hash-addressed snapshot.
3. Inspect `data/derived/coverage.json`: printing count, identity count, missing base
   numbers, denominators and variant completeness. Complete numbering does not
   guarantee image/text accuracy. Inspect new/changed cards and official images.
4. Compare `conflicts.json` with the prior snapshot and record reviewed resolutions.
5. Refresh official sources, then verify product dates, rules, rotation, bans and
   event terms. Explicitly update `data/policy/legality.json` and the relevant guides.
   A new API set or rotation flag never changes policy automatically.
6. Run `uv run python tools/lorcana.py check` and `uv run pytest -q`.
   Save the report and update the dated memory log.

`build` is deterministic for the same raw bytes, review ledger, evidence and effective date. Regeneration replaces generated
files only. Keep a backup before importer/schema changes; the original migration
backup is `archive/original-workspace-2026-10-04.tar.gz`.

## Refresh public official documents

```bash
uv run python tools/refresh_sources.py --as-of YYYY-MM-DD --only resources
uv run python tools/refresh_sources.py --as-of YYYY-MM-DD
```

Use the verification date in the user's timezone. The tool downloads registered
public URLs, retains prior changed snapshots and reports PDF links found in the
Resources hub. It does not automatically decide which new linked PDF replaces a
document. Inspect the hub and PDF contents, update registry URLs as necessary, and
record the document's effective date separately from the posting/checked date.
Failed fetches retain the last successful source and its old verification date.

Use `uv sync --frozen` and run tools through `uv run`. The downloader uses standard
HTTP facilities; PDF extraction uses the locked PyMuPDF dependency. Check the
original PDF visually for tables, symbols, images or ambiguous extracted text.
Cached source bytes are immutable evidence; editorial summaries belong in guides.

After a document refresh, rebuild the index with `uv run python tools/knowledge.py build`.
Run `uv run python tools/knowledge.py watch` after refreshing Resources to find newly
linked Hyperia notes/rules. The watch does not install schedules or change policy.
Source hashes bind curated answers; refresh requires actual re-review of affected
claims, not merely replacing their hashes. Download new printing images with
`uv run python tools/download_images.py` before reviewing new conflicts.

After new reviews, rebuild cards and run `uv run python tools/verify.py`. It rebuilds
both indexes, verifies source/image hashes and provider coverage, runs the 109-case benchmark, pytest and
Ruff. See `knowledge-engine.md` for lifecycle and scope.

For a rules update, inspect the update summary and implicated sections, then review
the digest's claims and citations. A replaced URL alone does not validate its summary.
For a policy update, explicitly compare both format ban lists, legal date, rotation,
event overrides, construction exceptions and historical applicability.

## Research and user data

Create a new `research/YYYY-MM-DD/` directory for a new meta/price window. Keep old
snapshots frozen. Preserve original collection and deck inputs; put mappings,
reconciliation and recalculated metrics in derived reports. Do not overwrite a
user's list merely because a new card or archetype is popular.

## Change record

Log source IDs/hashes, observed changes, interpretation, guide/policy edits, tests,
unresolved reviews and effective dates in `.ai_memory/`. Entries use YYYY-MM-DD,
newest first. A source's successful retrieval is not proof of complete coverage.
