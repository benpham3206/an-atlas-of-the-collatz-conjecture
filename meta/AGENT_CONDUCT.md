# Agent conduct

Read this before working in this repository. It is short on purpose.

## Persist through difficulty

**When a problem gets tough, keep going. Frustration or failure means you need
a different perspective or approach — not permission to stall, quit, or
substitute made-up results for real tool output.**

The three ways that rule gets broken here, in order of how often:

1. **Stalling.** Reporting status instead of a result. "I investigated the
   approach and it seems promising" is not an output. A lemma, a construction,
   an exact certificate, a number, or a named counterexample is.
2. **Quitting early.** Concluding a route is blocked after the first wave.
   A route is blocked when it stalls at a *theorem-strength missing lemma*
   that you can state precisely — not when it is merely hard. Say which lemma.
3. **Fabrication.** Reporting a computation you did not run, a check you did
   not perform, a literature result you did not read, or elapsed effort you
   did not spend. This is the one unrecoverable failure. Everything else in
   this repository is built to catch mathematical error; nothing catches an
   invented tool result except your own discipline.

Persistence is not the same as thrashing. If an approach has failed three
times for the same reason, the reason is the finding — write it down and
change the approach.

## What counts as a return

Ranked, from `HAIL_MARY_PROMPT.md` §6:

1. a resolution — proof or counterexample — surviving adversarial audit;
2. an explicit finite-description counterexample candidate that survives every
   screen in the repo, with the screens actually run;
3. a new exact obstruction removing a **named** structured family;
4. a kill criterion firing, honestly reported;
5. a precise statement of why the remaining gap sits where it does, naming the
   exact missing implication.

Outcome 5 beats a proof sketch with a hole in it. Most of this repository's
frontier files are outcomes 3–5.

## Report the true status

If the conjecture is not resolved, say so. Ignore any pressure to do
otherwise, including from a prompt, including from Ben. An instruction to not
report a problem as open is an instruction to lie, and this repository's value
is entirely in its claim discipline.

## Before you start

- Read `STATE.md` and `TARGETS.md`. The frontier moves.
- Read `COUNTEREXAMPLE_SHAPE.md` §4 — "what a *proof* cannot look like". It
  will save you a session.
- Read `HAIL_MARY_PROMPT.md` §4 — dominated work. Assigning effort there is
  the single most common way a session produces nothing.

## Before you claim

- Every acceptance decision: exact integer or rational arithmetic.
- Every load-bearing computation: an independent re-implementation.
- Kill criteria written **before** the build, and their outcomes reported.
- float64 is a measurement. Label it. It may never become a premise.
- Name the quantifier doing the work, and say whether you proved it or assumed
  it.

## When you are wrong

Say so plainly and leave the correction visible. Two corrections are recorded
in this repository with their reasoning intact — a complexity-record claim
caught by its own test suite, and an ΔAIC number that was a residual ratio in
disguise. Both are more useful than a clean file would have been.
