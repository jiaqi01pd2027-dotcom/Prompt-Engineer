# reason-2: Presentation scheduling puzzle (reasoning)

## Hidden rubric (never shown to the model under test)

Expected answer (the only valid assignment):
- 9am: Dev
- 10am: Aisha
- 11am: Carla
- 12pm: Ben
- 1pm: Elena

Verification by case analysis (slots numbered 1-5 for 9am-1pm):
- Constraint 2 makes Carla and Ben an adjacent pair (Carla, then Ben). Constraint 5
  puts Elena after Ben, so Ben cannot be in slot 5. The pair can only be at (1,2),
  (2,3) or (3,4).
- Pair at (1,2): Elena is in 3, 4 or 5; constraint 4 removes 3, so Elena is 4 or 5.
  Dev and Aisha take the remaining two of {3,4,5} with Dev before Aisha (constraint 3).
  If Elena = 4, then Dev = 3, Aisha = 5, and Aisha (5) is adjacent to Elena (4), which
  breaks constraint 6. If Elena = 5, then Dev = 3, Aisha = 4, adjacent to Elena again.
  No solution.
- Pair at (2,3): Elena is 4 or 5. Dev and Aisha take the remaining two of {1,4,5} with
  Dev before Aisha, so Dev = 1 and Aisha is whichever of 4 or 5 Elena does not take,
  which is adjacent to Elena either way. No solution.
- Pair at (3,4): Elena must be 5. Dev and Aisha take {1,2} with Dev first: Dev = 1,
  Aisha = 2. Check: Aisha not at 9am (ok), Ben right after Carla (ok), Dev before Aisha
  (ok), Elena not at 11am (ok), Elena after Ben (ok), Aisha (2) and Elena (5) not
  adjacent (ok). This is the unique solution.
Exhaustive enumeration of all 120 permutations against the six constraints also
yields exactly this one assignment.

Score signals (each 0-2, judge totals to 10 then normalises):
- ANSWER: the assignment matches exactly (2); four of five correct (1); otherwise (0).
- UNIQUE: states or shows that this is the only solution, rather than "a" solution
  (2 = shows why the other placements fail, 1 = asserts uniqueness without support,
  0 = does not address it or claims multiple solutions).
- CONSTRAINTS: every one of the six constraints is checked against the final answer,
  explicitly or through the case analysis (2 = all six, 1 = four or five, 0 = fewer).
- CLARITY: the reasoning can be followed without re-solving; the final schedule is
  stated in one place, slot by slot.
- CONCISION: no exploration of branches that were already ruled out, no restating the
  puzzle in full, no hedged alternative schedules.

Objective checks: the response contains a line beginning "Answer:" whose content, after
normalising whitespace and case, contains all five pairs 9am-Dev, 10am-Aisha,
11am-Carla, 12pm-Ben, 1pm-Elena (any order, any separator); no other "Answer:" line is
present.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<puzzle>
Five people, Aisha, Ben, Carla, Dev and Elena, each give one presentation at a one-day
workshop. There are five one-hour slots: 9am, 10am, 11am, 12pm and 1pm. Each person
presents in exactly one slot and each slot has exactly one presenter.

1. Aisha does not present in the 9am slot.
2. Ben presents in the slot immediately after Carla's.
3. Dev presents earlier in the day than Aisha.
4. Elena does not present at 11am.
5. Elena presents later in the day than Ben.
6. Aisha and Elena are not in adjacent slots.

Who presents in each slot?
</puzzle>

## Variants

### P0 bare
Figure out the schedule.

<puzzle>...</puzzle>

### P1 specific
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

<puzzle>...</puzzle>

### P2 role
You are a logician who solves constraint puzzles by systematic case analysis. Solve the
scheduling puzzle below. Give the presenter for each of the five slots, and make sure
the assignment satisfies all six constraints.

<puzzle>...</puzzle>

### P3 context
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

Background you should use: the puzzle was written so that exactly one schedule works.
"Immediately after" means the very next slot with nothing in between. "Earlier" and
"later" mean any earlier or later slot, not necessarily adjacent. "Adjacent" means the
two slots are consecutive in either order.

<puzzle>...</puzzle>

### P4 constraints
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

Constraints: do not guess and check at random; work from the most restrictive clue.
Do not offer more than one schedule. Do not stop when you find a schedule that works;
show that no other schedule does. Do not assign a person to two slots or leave a slot
empty. Verify all six clues against the final answer before you give it.

<puzzle>...</puzzle>

### P5 format
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

Output format: first a short section headed "Reasoning:" (at most eight lines), then a
five-row table with columns Slot and Presenter in time order, then a final line exactly
of the form "Answer: 9am=<name>, 10am=<name>, 11am=<name>, 12pm=<name>, 1pm=<name>".
No other text.

<puzzle>...</puzzle>

### P6 fewshot
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

Here are two solved puzzles in the style we want:

<example>
Puzzle: Kim, Lee and Max each present once in the 2pm, 3pm or 4pm slot. Lee presents
immediately after Kim. Max is not last.
Solution: Kim and Lee form an adjacent pair, so they are at (2pm,3pm) or (3pm,4pm).
If (2pm,3pm), Max is at 4pm, which is last, not allowed. So Kim is at 3pm, Lee at 4pm
and Max at 2pm. Checks: Lee right after Kim (ok), Max not last (ok).
Answer: 2pm=Max, 3pm=Kim, 4pm=Lee
</example>

<example>
Puzzle: Nia, Omar, Priya and Quinn each present once in slots 1 to 4. Quinn is last.
Priya is not first. Nia presents immediately after Priya. Omar presents before Nia.
Solution: Quinn takes slot 4, leaving 1-3 for the others. Priya and Nia form an
adjacent pair inside slots 1-3, so (1,2) or (2,3); Priya is not first, so (2,3). Omar
takes slot 1, which is before Nia (ok).
Answer: 1=Omar, 2=Priya, 3=Nia, 4=Quinn
</example>

<puzzle>...</puzzle>

### P7 cot
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints.

Before answering, think step by step: which clue is most restrictive, what placements
does it allow, how do the other clues eliminate each placement, and does exactly one
schedule remain. Show your reasoning, then give the final schedule on its own line
under a heading "Answer:".

<puzzle>...</puzzle>

### P8 fullstack
You are a logician who solves constraint puzzles by systematic case analysis.

Goal: solve the scheduling puzzle below and show that the schedule you give is the
only one that satisfies every clue.

Context: the puzzle was written so that exactly one schedule works. "Immediately
after" means the very next slot. "Earlier" and "later" mean any earlier or later slot.
"Adjacent" means consecutive slots in either order.

Constraints: work from the most restrictive clue and eliminate cases rather than
guessing. Do not offer more than one schedule. Do not stop at the first schedule that
works; show that the other cases fail. Verify all six clues against the final answer.

Format: a section headed "Reasoning:" of at most eight lines, then a five-row table
(Slot, Presenter) in time order, then one final line exactly of the form
"Answer: 9am=<name>, 10am=<name>, 11am=<name>, 12pm=<name>, 1pm=<name>".

<puzzle>...</puzzle>

### P9 interview
Solve the scheduling puzzle below. Give the presenter for each of the five slots, and
make sure the assignment satisfies all six constraints. Before solving, ask me any
clarifying questions you need (meaning of the clues, whether one solution is expected,
answer format). I have answered them below; use the answers.

<puzzle>...</puzzle>

Q: Does "immediately after" allow a gap? A: No. Ben's slot is the very next one after
Carla's.
Q: Do "earlier" and "later" require adjacency? A: No, any earlier or later slot counts.
Q: What does "adjacent" mean for clue 6? A: Consecutive slots in either order, for
example 10am and 11am.
Q: Is there guaranteed to be exactly one solution? A: Yes. Please show why the other
placements fail.
Q: How should I present the answer? A: A short reasoning section, then one line
"Answer: 9am=<name>, 10am=<name>, 11am=<name>, 12pm=<name>, 1pm=<name>".
