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

## Hidden insights: the failure classes verification cannot catch

**This is the most important section in this file.** Read it before you trust a
green test suite.

Every error found in this repository so far has been caught by *changing
audience or direction*, never by verification. Not once. The verification
machinery here is unusually good — exact integer and rational arithmetic,
independent re-implementations, deterministic certificates, kill criteria
written before the build, zero-`sorry` Lean — and it was green the whole time
each of the following was true:

| What was wrong | For how long | What eventually caught it |
|---|---|---|
| Two headline results were prior art (drift wall; Sturmian at all but one slope) | 3 days | reading the literature |
| "Factor complexity is strictly more information than letter frequency" — **false**; Sturmian words realise every irrational density at `p(k)=k+1`, so neither statistic determines the other | 1 day, in two entry-point files | writing a note for an outside reader |
| Corollary 7 is stated without proof, and carries **114 of 116** kills while the proved Corollary 4 carries 30 | 2 days; **closed 2026-08-01** (`2026-08-01-corollary-7-proof`) | writing a note for an outside reader |
| Shadow-barrier's Theorem 2 restates its own hypothesis, so it excludes nothing | months | re-reading it against a changed frontier |
| The `ℓ = 3` sweep is 3-automatic, not 2-automatic (Cobham 1969) | 2 days | enumerating the genuine 2-DFAO class |
| Estimated the complexity method would reach `N = 4–5` states; it reaches `N = 2` | — | running it instead of estimating |

Note what is *absent* from that table: not one arithmetic error. Not one failed
assertion. Not one certificate that did not reproduce.

### The rule

> **Exact verification is orthogonal to claim correctness.** Verification checks
> whether a computation is right. It cannot check whether the claim is
> *interesting*, *novel*, *load-bearing on something proved*, or *not a
> restatement of its own hypothesis*. Those are different failure classes and
> they need different instruments.

A test suite cannot fail on a tautology — a theorem that restates its
hypothesis is passed by construction, on every input, forever. A test suite
cannot fail on prior art. A test suite cannot notice that the lemma doing 98%
of the work was never proved.

### The instruments that do work

Use these deliberately, not incidentally. Each is cheap relative to what it
catches:

1. **Write it for someone who does not have this repository.** Both of the
   2026-07-25 corrections surfaced within an hour of drafting `REFEREE_NOTE.md`,
   after two days in which neither surfaced internally. This is the single
   highest-yield check known here. Tao's ICM 2026 rule of thumb is the bar: if
   you cannot give a clear, expert-level talk on the result — correct and
   properly attributed — it is not ready.
2. **Search the literature before writing the memo, not after.** Costs an hour.
   Retired two headline results.
3. **Trace the dependency graph to something proved.** For every claim, ask what
   it rests on, and repeat until you reach a proof or a citation. Count how much
   weight each dependency carries. If an unproved lemma carries most of it, that
   is the finding.
4. **Ask whether the conclusion could fail.** If no input could falsify it, it
   is not a test. Check that the hypothesis and the conclusion are genuinely
   different statements.
5. **Re-read old work when the frontier moves.** A packet written for a regime
   that has since become the only surviving one deserves a fresh read — it will
   either be promoted or killed, and both are useful.
6. **Measure your own method's reach instead of estimating it.** Estimates about
   where your instrument saturates have been wrong here by a factor of two.
7. **Name the direction of every inequality.** A *lower* bound on complexity can
   only ever kill *simple* objects. That single observation explained every
   saturation in `TARGETS.md` at once, and it was invisible until stated.

### What to do when you find one

Report it in the same breath as the result it damages, not in a footnote. Fix
it at source in every file that carries it — these claims propagate into entry
points fast. Then record it in [`LEDGER.md`](LEDGER.md) with what caught it, so
the instrument gets reused rather than rediscovered.

A correction is not a setback here. Three of the four probes run on 2026-07-25
returned negatives, and the negatives were worth more than the measurement.

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
