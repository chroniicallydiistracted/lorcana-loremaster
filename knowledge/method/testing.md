# Deck Testing Log

**Scope:** Reusable method; select the actual format, date, rules and card pool. Strategic guidance is not a measured current metagame.

## Deck identity

- Deck name:
- Version:
- Format:
- Set environment:
- Rules/policy versions and catalog/list hashes:
- Player perspective or simulation implementation coverage:
- Seed and iteration count if simulated:
- Date range:
- Pilot:
- List source:
- Cards changed from prior version:

## Aggregate record

| Opposing archetype | Play games | Draw games | Wins | Losses | Notes |
|---|---:|---:|---:|---:|---|

Do not report a matchup percentage without recording sample size and testing conditions.

## Game record

### Game ID

- Date:
- Opponent archetype:
- Opponent list confidence: exact / partial / inferred
- Play or draw:
- Opening hand:
- Mulligan out:
- Mulligan in:
- Planned first four turns:
- First ink missed:
- First unused ink:
- Permanent ink versus generated/saved/spent ink drops:
- Result:
- Final lore:
- Turning point:
- Cards overperformed:
- Cards underperformed:
- Misplays:
- Opponent surprises:
- Proposed change:
- Confidence in proposed change: low / medium / high

## Structural failure tags

- Ink failure
- No early play
- Excess early cards
- Excess top end
- No draw
- Wrong interaction
- Evasive vulnerability
- Location vulnerability
- Item vulnerability
- Could not close
- Lost race
- Poor mulligan
- Sequencing error
- Matchup knowledge error

## Revision gate

Before changing a card, state:

1. What recurring problem it solves.
2. How often the problem occurred.
3. Which matchup benefits.
4. What role is lost by removing the old card.
5. Inkability and curve change.
6. Number of games required before review.
