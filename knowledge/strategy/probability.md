# Probability and modeling

Use exact calculations when inputs are known. State the population, success
definition, sampling process and what the calculation does not model.

## Uniform draws without replacement

For a deck of N cards, K qualifying cards, and n cards seen uniformly without
replacement, the chance of exactly k qualifying cards is:

`P(X=k) = C(K,k) C(N-K,n-k) / C(N,n)`.

The chance of at least one is `1 - C(N-K,n)/C(N,n)`. Sum the valid terms for other
thresholds. The CLI computes an exact rational fraction before a decimal result:

```bash
uv run python tools/lorcana.py probability --population 60 --successes 4 --draws 7
```

This is access to a defined group, not the probability of a legal winning line or
having enough ink after paying for plays. Define usable early plays by board and
conditions, not printed cost alone. For turn-based access, count actual draws:
normal two-player starting player skips the first Draw step; card effects can alter
that count. Verify the mode and include only cards actually accessible.

## Mulligans

Returned opening cards go to the bottom before replacement cards are drawn; the
deck is shuffled afterward. Model the observed hand and keep policy separately.
Given an observed seven-card hand and r returns, the replacement draw samples the
N−7 previously unseen cards. Returned cards are unavailable in this replacement
draw. Remaining successes are K minus successes in the entire original hand,
not merely successes kept. After the shuffle, subsequent draws use the remaining
deck with kept and replacement cards excluded. (CR 2.2.2.)

An unconditional mulligan rate requires enumerating opening-hand category counts,
applying a stated keep policy, calculating replacement outcomes, and then combining
their weighted probabilities. The CLI does not implement that unconditional model.
Its separate `mulligan` command computes conditional target access for a specified
observed hand; see [the deck-review workflow](deck-review-workflow.md) for examples.
Never describe drawing fourteen cards as the Lorcana mulligan model.

## Multiple packages and resources

Use multivariate hypergeometric enumeration for disjoint categories. When categories
overlap (inkable early play, engine plus singer), partition into intersection groups
first; multiplying separate access probabilities assumes independence incorrectly.
Define which cards must be held, what can be inked and the order of plays before
calculating an ink-by-turn probability. Temporary ink drops, permanent inkwell cards,
Shift costs and songs are separate resource mechanisms.

For one effect that searches or looks at several cards, account for its selection,
replacement and information rules. For gameplay-dependent draw, use explicit
conditional branches or an appropriately validated simulation.

## Simulations and observed rates

Record deck hashes, rules version, implemented mechanics, seed, iteration count,
keep/ink/play policies, success metric and limitations. Report confidence intervals
for stochastic estimates, and distinguish games from matches. Small observed samples
are not proof of matchup advantage. A draw-only model cannot measure a matchup.

The local tooling is a retrieval/structure/calculation utility, not a full game
engine. Rules-engine and simulation results can only be claimed after an actual,
appropriate tool run with disclosed implementation coverage.
