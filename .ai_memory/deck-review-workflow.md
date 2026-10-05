# Deck review and scenario evaluation

## Context

- Date: 2026-10-04, America/Phoenix
- Branch: main; preceding research edits retained
- Task: Implement fresh tournament evidence, concrete archetype profiles, integrated
  reviews of both preserved decks and unfamiliar-question evaluation end to end.

## Problem Statement

Card/rules retrieval and finite reviewed answers exist. Current event evidence and
repeatable collection-aware deck advice need integration and independent checks.

## Research

Use dated public events and exact lists, verify format and publication scope, and
retain source hashes. Exclude future events and never infer matchup rates from finishes.

## Proposed Solution

Capture a recent event/list snapshot, resolve lists to reviewed card identities,
curate sourced archetype packages, implement review reports and balanced proposal
validation, and evaluate unseen scenario responses with explicit reference rubrics.

## Status

Implementation complete and locally verified. Independent expert/prose grading and
actual paired matchup play remain unperformed validation, explicitly separate from
the automated contract results.

## Implementation Log

### 2026-10-04

Completed 11-stage verification: 74 tests, 109 FAQ benchmark cases, 24 compound
contracts, card/evidence builds, provider coverage, tournament checks, both deck
reviews and Ruff lint/format all passed. Exact user deck SHA-256 values remain
30bbfc6ec67ea658c47d384eae96c565686a6b753cf4de5b334acca3353cf053 and
69f0d81aadeb421e7b3faeb18b53404963a7ec953d19d4128f160f9c50b0a52e;
collection remains e3cf22297eb3af461faba7da5d640bd6d7cc931cef789555bbef9237de5b8278.

Implemented review/mulligan CLI, six sourced archetypes, two preserved-deck reviews,
six matchup plans each, exact balanced candidate exports and combined ownership.
Missing copies: Elinor 9, Baha 27, simultaneous baselines 37. Chernabog test changes
uninkability from 8 to 10 and missing copies to 25. Its three-uninkable opening
burden is 8.3042% versus baseline 4.3457%; no measured advantage claimed.

Added 24 compound scenarios, explicit response/provenance schemas, answer-free
prompt export, independent category-counting probability oracle and adversarial
contract mutations. Current fixtures are reference-assisted; independent expert
grade remains pending. Tests document that prose can contradict correct claim fields.

Captured three recent Core events and eight exact lists from public web-tool
excerpts, with official date/format/roster corroboration. Direct provider HTTP 403
failures are retained; no restrictions bypassed. Saved excerpt capture time is
distinct from unknown origin retrieval time. Future October 7 entry excluded;
roster discrepancies and incomplete standings/pairings prevent invented rates.

Reviewed source/claim hashes for four affected finite answers. Added freshness and
source gates, event/player URL checks, custom-inventory handling and input-overwrite
protection. Existing uncommitted research work retained; no user deck/inventory
mutation or external model/service run. Details: reports/deck-review-milestone-2026-10-04.md.

Read existing validators, saved decks and evidence boundaries. Started fresh public
event research; detected future-dated discovery rows requiring exclusion.
