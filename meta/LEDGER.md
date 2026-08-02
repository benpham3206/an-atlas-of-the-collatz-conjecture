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

## 2026-08-01 — Corollary 7 written out (the gap that carried 114 kills)

**Strategy.** After syncing to `origin/main`, read the hail-mary / STATE /
TARGETS stack and pick the highest-EV *finite* obligation rather than the
headline problem. Amplification is still the most important open half, but it
has no theorem and no session-sized entry point. Corollary 7 was flagged
unproved while carrying **114 of 116** supercritical-closure kills — a
dependency-graph finding from 2026-07-25 that had never been closed. Write the
proof, not a new instrument.

**Worked.**

- **Tracing weight before inventing.** The AGENT_CONDUCT instrument "trace
  every claim to something proved; count how much weight each dependency
  carries" named the target before any algebra: Cor 7 was the single unproved
  lemma with almost all the kill weight.
- **Green unrolling first.** Once the integer recursion is written as
  `2^N y_N = 3^s y_0 + d Σ …`, the ones-cap inserts term-by-term and the rate
  `2^{gN}` is forced. The "believed routine" reconstruction was, in fact,
  routine — but only after the identity was written down.
- **Parity-consistent test orbits.** The first verifier failed because it fed
  random bitstrings into an integer orbit that requires `q_j ≡ y_j (mod 2)`.
  Fixing that (derive the word from the state) is the same discipline as
  never treating a free 2-adic transcript as a positive integer.

**Failed.**

- No progress on amplification, the critical-density gap, or the morphic
  residual (log-frequency vs natural liminf). Literature check on morphic
  log-frequency algebraicity returned existence (Bell 2008) but not
  algebraicity of the value — so the automatic-density style synthesis does
  not lift.
- Collatz remains open. This session is an outcome-3/5 under the hail-mary
  ranking (exact obstruction written; infrastructure gap closed), not a
  resolution.

**Mistakes.**

- First verifier used free words; parity invariant broke. Caught by the
  verifier itself, not by re-reading the proof.
- Mis-classified continued-fraction convergents of `log₃2` as subcritical
  twice (12/19 and 53/84 are above α). Integer witness `3^a ? 2^b` is the
  only check; memory of the alternation pattern is not.

**Lesson.**

> **An unproved lemma that already carries the weight of a published packet is
> higher EV than a new attack on the headline gap.** Closing Cor 7 did not
> move the Collatz frontier outward, but it stopped 114 kills from resting on
> a sketch. The compounding object was the *dependency graph*, not a new
> density regime. Separately: when testing an identity on "words", use the
> words the dynamics actually produces — free symbolic inputs silently leave
> the integer model.

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

---

## 2026-08-01 — automatic-density closure

**Strategy.** Re-read the exact critical-density target and search for a
finite-state theorem about `liminf`, rather than extend the repository's
complexity computations.

**Worked.** Bell 2020 proves that the lower density of every automatic set is
rational. López–Stoll 2021 force the lower parity density of a rational
non-cyclic trajectory to equal the irrational number `log₃2`. Their direct
synthesis closes automatic parity words in every base. The same check closes
all uniform-morphic test words and all bounded-DFAO survivors. The algebraic
frequency theorem for morphic words also closes every morphic transcript whose
natural one-frequency exists.

**Failed / stopped.** The morphic extension stops when natural frequency does
not exist. Bell 2008 gives logarithmic frequency, but López–Stoll constrain
lower natural frequency. These quantities cannot be identified without a new
argument.

**Mistake found.** The previous priority audit used Cobham's theorem only when
natural density exists. It did not search for a theorem about lower density.
That left a class marked open even though Bell had closed the needed invariant
in 2020.

**Lesson.** When a target contains `liminf`, search for a theorem about the
liminf itself. A theorem about the full limit can leave a false residual case.

---

## 2026-08-01 — amplification: the proposed bridge is killed at the handoff

**Strategy.** Take `TARGETS.md` §1 at its word: it named the bridge ("the
inverse/cylinder family of a single survivor") and named a kill criterion with
an instruction to test it on the smallest case first. Rather than attempt a
Tao-strength theorem, measure whether the two named families can supply the
exceptional set at all.

**Worked.**

- **Writing the identity down before arguing about it.** The tracking identity
  `T^i(y + 2^L m) = T^i(y) + 3^{s_i} 2^{L−i} m` (i ≤ L) makes the whole route
  computable in one line: control time equals `v₂(x − y)` exactly, and at the
  handoff the difference is an odd multiple of `3^{s_L}` — unit 2-adic
  distance, zero further forced symbols. Both legs of the no-go are corollaries
  of folklore (Terras affine form; isometry of the Bernstein–Lagarias
  conjugacy). The same lesson as the Mahler session: a stated bridge is a
  hypothesis, and it was cheaper to test than to reason about.
- **The smallest case did the work.** `x = 27 + 2²⁰` tracks above `2²⁰` for
  exactly 20 steps, drops below at step 34, reaches 1. One exact instance
  confirmed what the identity already proved structurally: the circularity
  criterion fires at the handoff state.
- **The outcome is a sharper gap, not just a negative.** The missing
  implication is now named precisely: permanence past the 2-adic proximity
  scale. Provably-high excursions at positive density are free
  (Corollary A1); persistence is the entire remaining content.

**Failed.**

- No entry into the amplification branch: no theorem turning one divergent
  orbit into a positive-log-density exceptional family. The branch remains
  open; only its two natural mechanisms are dead.
- The morphic lower-density question (Target 4's residual) is blocked on a
  named open problem: Bell 2020 §6 explicitly asks whether morphic lower/upper
  densities are algebraic. Not available off the shelf; recorded so it is not
  re-searched.

**Mistakes.**

- First version of the verifier's affine recurrence carried `c' = 3c + 2^{i+1}`
  instead of `3c + 2^i`; caught instantly by the independent direct-iteration
  path. Two-path verification paying for itself again — the error was in the
  *checker*, which is exactly where single-path setups hide theirs.

**Lesson.**

> **A kill criterion with a named smallest case is a task, not a warning.**
> `TARGETS.md` §1 carried its circularity criterion for a week with the test
> unrun. Running it cost one session and converted "no theorem exists" into
> "these two mechanisms provably cannot work, and here is the exact lemma that
> remains". When a frontier file ships both a bridge and a kill test for that
> bridge, the kill test is the higher-EV action: either outcome (route survives
> the smallest case / route dies on it) is a result.

**Addendum — audit of the Corollary 7 proof (same day).** Asked to double-check
PR #18. The proof is sound end-to-end (statement match with the landmark memo,
contrapositive direction, boundary at `β = α`, `1/g = α/(β−α)` exact); a third
implementation confirmed (3.1) on 4,000 adversarial words, Lemma 1 on 465,868
equal-factor pairs, and (4.3) on 34,055 full-cap instances at 88% tightness.
One real finding: the verifier's `bound_4_3` dropped a factor 2 on the
inhomogeneous term and tested the stronger unproved bound `T1 + T2/2` — benign
direction (stricter test, still validates (4.3)), but a checker/proof mismatch.
Fixed at source; correction note left in the packet. **Lesson:** audit the
*checker* against the *statement*, not only the statement against the
literature — the two factor-of-2 slips this week (mine in the affine
recurrence, this one in the bound) were both in verification code, and both
were invisible to the test suites themselves.

## 2026-08-01 — salvage Kimi formal expansion + make odometer merge-safe

**Strategy.** Resume a blocked Kimi Desktop session at the last durable write
(README formal-row edit). Verify the four subagent Lean modules by `lake build`
and axiom audit, close doc drift, then harden the co-shipped odometer
**measurement** packet so a combined PR is reviewable (clone size, tests,
indexes, no claim contradiction).

**Worked.**

- Four modules (`ChainClosure`, `BeattyKill`, `ContractionOnset`,
  `CycleExclusion`) already complete on disk; build green; no `sorryAx`.
- STATE/README claim language scoped: Lean is not m ≤ 20 or h ≤ 10⁶; 0.118
  δ-drift is shallow-window only and is superseded by odometer n = 1000.
- Odometer certificate slimmed **7.8 MB → ~0.45 MB** (`slim-v1`): integers
  exact; measurements ~12 sig figs; exact \(x_n\) recovered from \((k,n)\).
- Structural tests run without mpmath (`python3 test_odometer_dominance.py`,
  19/19). Full bak moved to Trash; gitignored.

**Failed.**

- Could not re-run full 1000-layer mpmath pipeline in this environment
  (mpmath/gmpy2 not installed). Relied on slim certificate + summary blocks
  from the original analyze.

**Mistakes.**

- Initial PR-readiness assessment mixed two products without a packaging
  plan for the 7.8 MB JSON — merge-safe only after slim + indexes.

**Lesson.**

> **A measurement packet is merge-safe when its certificate is clone-cheap
> and its tests do not require the original HPC stack.** Keep exact integers
> and a regenerable full run path; never force reviewers to download
> multi-megabyte high-precision dumps to check structural invariants.

## 2026-08-01 — standing rule: tests before final output

**Strategy.** Bank the process failure mode “final claim without running the
suite” as a hard gate, not a preference. Orthogonal to “green tests prove the
math claim” (they do not).

**Worked.** Rule written into `meta/AGENT_CONDUCT.md` and Kimi vault
`collatz-atlas-standing-rules.md` so Desktop + CLI agents both see it.

**Failed.** —

**Mistakes.** —

**Lesson.**

> **Run the test surface before the final sentence.** Identify the suite
> (lake build / packet `test_*.py` / verifier), run it, read pass/fail/skip,
> then speak. A missing dep is a named skip, not a silent pass. Fabricating a
> green line is fabrication.
