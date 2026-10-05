# Lorcana Game Master scope expansion

## Context

- Date: 2026-10-04 (America/Phoenix).
- Task: audit and reorganize the entire WSL workspace for broad Lorcana expertise,
  including the newly supplied Hyperia City base set.
- Branch: not a Git repository.

## Problem Statement

The project had a Core-only instruction boundary, Set 13 defaults, stale ban policy,
missing identity/text tables and no reproducible project-level retrieval/check workflow.

## Research

Inventoried all 333 original files. Supplied API contains 3,515 records, 2,784 identity
groups and all 204 Set 14 base numbers. Verified official CR 2.2.0 and TR effective
July 14: no Core bans; Hiram banned in Infinity. Official Hyperia prerelease October
16 and wide release October 23. Sources cached with hashes and distinct date fields.

## Proposed Solution

Broad role and routing; topic-specific guides; independent raw, derived and policy
data; reproducible standard-library tools; historical evidence/archive preservation;
explicit gaps and current-source retrieval rather than fabricated certainty.

## Status

Implemented. Final validation is recorded in `reports/validation-2026-10-04.json`.
Remaining evidence boundaries are in `knowledge/COVERAGE.md`.

## Implementation Log

### 2026-10-04

- [x] Backed up original complete workspace and recorded per-file SHA-256 inventory.
- [x] Revised AGENTS.md and source/format/reasoning guidance for all Lorcana areas.
- [x] Organized active knowledge, card data, official sources, user holdings, vendor and archives.
- [x] Indexed supplied API, retained printing differences, verified base-number coverage.
- [x] Corrected stale bans, Set 13 defaults, color-payment implications and inherited citations.
- [x] Added current/future Core/Infinity checks, Limited pool checks and known exceptions.
- [x] Added exact draw calculations, collection reconciliation and flavor/tag retrieval.
- [x] Added source refresh/discovery without automatically changing policy.
- [x] Verified original raw export, collection, user deck and upstream file preservation.
- [x] Passed all 19 behavioral regression tests, deterministic rebuild, invalid-import, source hash, SQLite integrity and documentation-reference checks.
- [x] Recorded missing scenario/narrative/variant/oracle/new-mechanic sources explicitly.
