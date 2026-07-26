# Session ledger

The flywheel's memory. One entry per working session: the meta-strategy used,
what worked, what failed, mistakes made, and the lesson that generalises.

**A session is not finished until it has an entry here.** Sessions that
produce no entry produce no compounding — the mathematics survives in
`contribution/`, but the *method* is lost and the next agent repeats the
mistake.

Format per entry: **Strategy · Worked · Failed · Mistakes · Lesson.**
Keep lessons transferable — a lesson that only applies to one packet is a
note, not a lesson.

---

## 2026-07-25 — The Mahler tower: the guessed obstruction was in the wrong place

**Strategy.** Run the cheapest check the frontier file itself nominated, and
run it as *algebra first, literature second, opinion never*. `TARGETS.md`
named two bounded checks and asserted which one was blocked ("the mixed bases
2 and 3 are the obstruction"). Rather than argue about the assertion, derive
the functional equation and see whether it exists.

**Worked.**

- **Deriving instead of estimating.** The mixed-base obstruction was a
  plausible guess that had never been tested by writing the equation down. It
  took one reindexing — sum over positions rather than over ranks of ones — to
  see that the base-3 weight is absorbed by a monomial substitution `y ↦ y^M`.
  The equation exists for *every* uniform morphism. This is the same lesson as
  2026-07-24's `N = 4–5` versus `N = 2`, from the opposite direction: the
  estimate was wrong about a **blocker**, not about a reach.
- **Refusing to accept a soft verdict.** The first attraction test had three
  branches and one of them was unsound — it inferred convergence from
  `τM^e ≡ 0 mod 2`, which only bounds the valuation below by 1. Replacing it
  with a descent whose every answer is a proof changed the census by hundreds
  of words and turned an 80-step measurement into a finite pigeonhole argument.
- **Keeping the scratch implementation and disagreeing with it.** The corrected
  verifier's `stalled` counts matched the throwaway heuristic exactly at every
  `d`, and the `attracted` gap was exactly the new `undecided` column. Two
  methods agreeing on the decidable part and differing precisely on the
  undecidable part is worth more than either alone.

**Failed.**

- No survivor was closed. The packet splits the ten 4/6 and closes none.
- Check 2 (a 2-adic dichotomy) was *not* answered, and is now known to be
  insufficient even if answered — the point sits on the excluded boundary, so
  the missing theorem is about boundary points, not about `p`-adics.

**Mistakes.**

- Wrote a test asserting the Thue–Morse `F₂` orbit never vanishes. It vanishes
  at `e = 2`; `M = [[1,1],[1,1]]`. The test was wrong, not the code. Caught
  immediately because the test ran — but it is a reminder that an expectation
  typed from memory is not a check.
- Claimed a 4-minute runtime in the memo before timing it. It is 40 seconds.
  Corrected. Numbers in prose are claims and get verified like any other.

**Lesson.**

> **A stated obstruction is a hypothesis, and it is usually cheaper to test
> than to reason about.** `TARGETS.md` carried "the mixed bases 2 and 3 are the
> obstruction" as settled context for a full day. It cost one reindexing to
> falsify. The obstruction was real but sitting one level down — at the
> evaluation point, not at the equation — and no amount of arguing about the
> original sentence would have found that. **Write the object down before
> deciding it cannot be written down.**

> Corollary, transferable: when a frontier file says "X is the obstruction",
> that sentence has the same epistemic status as an unproved lemma. Trace it to
> a proof or a computation, or mark it as a guess.

---

## 2026-07-24 — Complexity bounds, contraction onset, and two informative failures

**Strategy.** Attack a *listed-open* stratum rather than the headline problem.
Look for a place where the repository already had an unused inequality, and
supply the missing input instead of a new theorem.

**Worked.**

- Reading the whole repository first surfaced Corollary 7 of the landmark
  packet — stated, correct, and *never applied*. The gap was not a missing
  theorem but a missing number: nobody had bounded factor complexity. Supplying
  it closed 99 of 109 open words. **Highest-yield move of the session, and it
  cost nothing but reading.**
- Deriving the exact factor language rather than sampling a prefix. The
  difference between "measured complexity" and "proved complexity bound" is
  the difference between a measurement and a theorem.
- Picking a target for its *failure mode*. Target 3 was chosen because a
  negative answer would be informative. It failed, and the failure retired a
  whole route with evidence.
- Elementary lemmas beat clever ones. "Descent requires contraction" is one
  line — `C_h > 0` — and it carried the strongest finite-window result of the
  day.

**Failed.**

- Target 3 saturates at two-state automata. The factor-complexity method does
  not scale, so the general 2-automatic Gap is unreachable that way.
- The `d = 4` census made it worse, not neutral: survival rose to 21% and the
  *cheap* screen (drift wall) did most of the killing at every size while the
  expensive one's share fell from 30% to 13%.
- No progress on amplification. Not attempted; correctly identified as
  Tao-strength.

**Mistakes.**

1. **Estimated N = 4–5 for the DFAO theorem; measured N = 2.** Wrong by
   inference from a *different* family — length-≤4 morphisms on two letters,
   which for ℓ = 3 are 3-automatic and not 2-automatic at all.
2. **Claimed `M(h)` sets records only at continued-fraction convergents.**
   It also sets them at semiconvergents (`306 + 665k`). Caught by the test
   suite, not by review.
3. **Let a runaway test burn 4h38m of CPU** before diagnosing that the
   quadratic blowup was in the test, not the mathematics.
4. **Reported "all repo verification commands pass"** after running only the
   fast ones.

**Lessons.**

- **Look for unused theorems before proving new ones.** A stated-but-unapplied
  corollary is the cheapest possible source of a result. Ask "what in this
  repository has never been pointed at anything?"
- **Choose targets by failure mode, not by expected success.** A target whose
  negative answer closes a route is worth more than one whose positive answer
  is narrow.
- **An inequality that is a *lower* bound on complexity can only ever kill
  simple objects.** This is why the method saturated, and it predicts the same
  wall for morphic words and for the ten survivors. Generalises: check which
  direction your bound points before planning a campaign on it.
- **Verify the estimate you are about to spend compute on.** The kill
  criterion took eight seconds and would have corrected the N = 4–5 estimate
  before any of the planning around it.
- **Don't claim a suite passes until it has passed.**

---

## 2026-07-25 — Attribution layer, meta directory, external transfer audits

**Strategy.** Stop proving and build the flywheel: make provenance explicit,
give strategy research its own tier, and run four independent audits in
parallel instead of serially.

**Worked.**

- Parallel independent audits. Four agents on disjoint questions — external
  literature transfer, Bayesian applicability, GEB, code-quality tooling —
  with no shared state. Two returned findings that changed the repository.
- **An audit caught a live defect in the claim ledger.** `ΔAIC = +30` is
  identically `N·ln(SSR ratio)` — the residual ratio wearing a likelihood
  costume, computed over 16 correlated points from a deterministic computation
  with no sampling noise. `STATE.md` now reports the ratio (6.52×) and the
  caveat. **This is exactly the failure the repository exists to prevent, and
  it survived several sessions unnoticed.**
- Asking for blunt negative verdicts. The literature audit returned "nothing
  here transfers" with a per-method table, which is worth more than a
  manufactured connection.

**Failed / not attempted.**

- No mathematical progress this session by design.

**Mistakes.**

- **Eleven packets were written before a single priority search.** The search
  took one session and retired two headline results. The cost was not the
  search; it was everything built on top of unsearched claims — memo prose,
  STATE entries, a ranked target list, and a PR body all had to be corrected.
- Guessed in the contraction-onset memo that Lemma 1 was "very likely
  folklore" and shipped it as a guess. It is not folklore; it is Terras's
  named `κ(n) ≤ σ(n)`, published 1976. A guess in a novelty section is a
  claim, and should have been either checked or omitted.
- Never cited López & Stoll 2021 despite citing their 2009 paper in the
  repository's own reference list. The relevant paper was one author-search
  away for months.

**Lessons.**

- **Audit the summary lines, not just the packets.** Every packet's own
  "honest scope" section was correct; the defect was in `STATE.md`, one
  citation away from becoming a premise. Frontier summaries are where
  measurements get laundered into theorems.
- **A "no" from an independent audit is a result.** Commission audits with an
  explicit licence to return nothing, or they will find something.
- **Run the priority search BEFORE writing the memo, not after.** It is the
  cheapest possible step and it determines whether the memo is a result or a
  re-derivation. New standing rule: no packet is complete without one.
- **A negative priority result is not a loss.** López–Stoll 2021 narrowed the
  remaining gap from "the supercritical stratum" to the single critical
  density — a sharper and more useful frontier than the repository had. The
  search gave more than it took.
- **Separate strategy from proofwork physically.** Three of the four
  most expensive mistakes in this project's history were strategic and no
  verifier could have caught any of them.


## 2026-07-25 (afternoon) — four parallel probes: three negatives and a measurement

**Meta-strategy.** Run four independent lines at once, three in subagents, and
accept negatives as the primary product. Continues the priority-search shift
from generation to digestion.

**Wins.**
- Exact rational bracket for the dimension of the surviving set,
  `H(α) ∈ (0.949952152, 0.949957233)`, certified by integer comparisons only.
  Yields the sharpest statement yet of *why* amplification has never been
  entered: the gap is measure-zero, so density methods cannot see it, and
  dimension ≥ 0.95, so it cannot be dismissed.
- A referee-ready note on Corollary 4 — the first artifact aimed at an external
  human rather than at the repository.

**Mistakes caught, both mine.**
- **"Factor complexity is strictly more information than letter frequency" is
  false.** Sturmian words realise every irrational density at `p(k) = k+1`, so
  neither statistic determines the other; they are *logically independent*. The
  load-bearing claim survives the correction — Corollary 4 is still not a
  consequence of any frequency result, and is still non-vacuous exactly where
  they are all vacuous — but the false version was in two entry-point files and
  a referee would have caught it in one line.
- **Corollary 7 is unproved and carries most of the weight.** 114 of 116 kills
  route through a corollary the landmark memo states without proof. I built on
  it for two days without checking.

**Kills, honestly reported.**
- Shadow-barrier: its Theorem 2 is an algebraic restatement of its own
  hypothesis, so it is passed by construction and excludes nothing.
- The complexity-consuming instrument does not exist in the literature, and the
  reason is structural rather than a gap in effort.
- Heinis gap probe: proposed, tested, dead in one command — the survivors'
  complexity bounds are 3.16 to 6.06, far above the `(1,2)` window.

**Lesson.** Three of four probes returned negatives, and the negatives were more
useful than the measurement. The two errors were both found by *writing for an
outside reader* — neither surfaced during two days of internal verification.
That is the strongest evidence so far that Tao's slide-48 test is the right gate.
