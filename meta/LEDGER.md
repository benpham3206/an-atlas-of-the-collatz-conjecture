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

- None caught yet this session. That is not the same as none made.

**Lessons.**

- **Audit the summary lines, not just the packets.** Every packet's own
  "honest scope" section was correct; the defect was in `STATE.md`, one
  citation away from becoming a premise. Frontier summaries are where
  measurements get laundered into theorems.
- **A "no" from an independent audit is a result.** Commission audits with an
  explicit licence to return nothing, or they will find something.
- **Separate strategy from proofwork physically.** Three of the four
  most expensive mistakes in this project's history were strategic and no
  verifier could have caught any of them.
