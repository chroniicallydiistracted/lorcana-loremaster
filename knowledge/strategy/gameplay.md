# Board-state and gameplay decisions

## Establish a complete player-view position

Record mode, turn/phase/step, active player, players/teammates, lore totals, relevant
hand, deck/discard counts, known revealed cards, permanent ready/exerted ink, drops,
and effects with durations. For each board object record exact identity, controller,
dry/ready state, damage, modified stats/lore, location and Shift/Boost stack counts.
Record waiting triggers and unresolved choices. Do not reveal unknown facedown cards.

Use the user's hand only when legitimately available to that player. Opponent hands
and upcoming draws are unknown unless revealed. In a replay, separate player-view
coaching from hindsight review. A scenario assumption is not observed information.

## Compare legal lines

1. Check any immediate win, forced loss or mandatory action.
2. Enumerate plausible lines: quest/race, favorable challenges, removal, engine
   development, song/Shift alternatives, location movement, recovery and conserving resources.
3. Apply exact costs, choices, prohibitions, replacements, game-state checks and bag
   timing before evaluating outcomes. A high-value illegal line is irrelevant.
4. Count immediate lore, likely future lore denied, surviving board, usable resources,
   hand access and opponent's next-turn clock.
5. Test reasonable opposing responses using known archetype evidence and explicit
   assumptions, without playing around every imaginable card equally.
6. Compare the safest sufficient line against lines that require a favorable draw or
   opponent mistake. If behind, justified risk can outperform slow value play.

## Inking, songs and Shift

For inking, plan the next two turns and identify indispensable answers/engine pieces.
Reassess after selection or draw. Do not ink from a memorized priority list when the
board changes. Ink is not tied to a card's printed ink color once it becomes ink.

Compare a song's saved ink with the singer's lost quest/challenge and vulnerability.
Verify dry/ready status and actual Singer/Sing Together contribution. For Shift,
compare full-cost play with eligible alternate-cost lines and track inherited damage,
state, duration effects and the multi-card consequence of removal.

For drops, track generating, keeping and spending separately. Only use an enhanced
effect if its exact condition is met. Unsettled Set 14 timing requires official verification.

## Explain the decision

Give the recommended action sequence, exact outcome and why it beats the strongest
alternative. Identify the hidden-information assumptions that could reverse the
choice. If essential state is missing, provide conditional lines and ask for only
that information. For an event ruling, cite the applicable rule and distinguish
gameplay advice from the Lore Guide's correction/remedy decision.
