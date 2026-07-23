# Repository state

Frontier of the fold program: what is established, what is blocked, and what
runs next. Proved statements use exact integer/rational arithmetic; float64
outputs are measurements, not theorems, and are labelled as such. The Collatz
conjecture remains open; nothing here proves or disproves it. Updated
2026-08-01.

## PROOF ARCHITECTURE (which branch each result serves)

The organising structure is not in this file's history — it is
[`contribution/packets/2026-07-22-landmark-pointwise/LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md`](contribution/packets/2026-07-22-landmark-pointwise/LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md)
§8. Restated here because a reader cannot otherwise tell what any single
packet is *for*.

Assume a least counterexample `N`. After cycles are excluded, the
conjunction of two statements would prove Collatz:

| Branch | Statement required | Status |
|---|---|---|
| **Rigidity** (zero-entropy / low-complexity closure) | every divergent orbit with zero-entropy symbolic closure violates positive-integer lift stabilization | **entered** — real theorems, several strata closed |
| **Amplification** (positive-entropy / high-complexity closure) | every divergent orbit with positive-entropy symbolic closure contradicts logarithmic-density descent | **not entered** — no theorem; a located barrier only |

Rigidity is served by: the realizability criterion Φ(q) and eventual-periodicity
decidability (`proofs/PARTIAL_THEOREMS.md`); the recurrence barrier and
complexity–pressure inequality (Theorems 4.1, 5.1, Corollary 5.2, landmark
packet); primitive-uniform subcritical exclusion
(`proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md`); the pointwise drift wall
(2026-07-22-pointwise-drift-wall); the automatic-transcript trichotomy's
subcritical and critical strata (2026-07-22-automatic-transcript-rigidity);
rational-shadow deletion (`proofs/RATIONAL_IRRATIONAL_SHADOW.md`).

Amplification is served by: the Tao structural refinement, syracuse-fourier,
scalar-phase-second-moment, structure-randomness-transfer, plateau-escape-weight
and plateau-drift-test packets. **Every one of these disclaims being a stronger
density statement than Tao's.** They locate the obstruction — the 2–3 resonance
lattice, which is the same object that blocks the symbolic side — and none
crosses it.

So the honest reading of the repo: the left branch has been entered with
genuine theorems; the right branch is the exact remaining leap. Work that
does not attach to one of these two statements is not on the critical path.

### The one place a measurement can still move the branch

The plateau packet's **P6 dichotomy** is stated so that either resolution is a
result — the "win–win" structure:

- **(i) L(n) bounded** → uniform *exponential* decay of M_n → **strictly
  stronger than Tao's n^(−A)**;
- **(ii) L(n) creeps** like ½log₂n → the measured e^(−c√n) law → Tao-strength.

The drift test was built to poke this with a falsifiable prediction (p₂ > 0.95
near n ≈ 22). The prediction failed on schedule — but **that reading has since
been corrected twice** (2026-07-24 streaming packet):

- the p₂ extrapolation was **misspecified**: p₂ is a sawtooth whose direction
  is fixed by Δk, not by n, so a linear-in-n fit could not have tested
  anything. On the correct subsequence the 0.95 crossing sits near n ≈ 32 and
  n = 21 is *above* trend, at an all-time high of 0.887281;
- the M_n decay law, compared directly for the first time, fits
  **branch (ii)** — Tao-strength — better: sum of squared residuals
  **6.52× smaller** than branch (i) over n = 6..21 (16 points), and 4.22×
  smaller on n ≥ 13. Adding n = 21 made the gap larger, not smaller.

**Read that as a fit quality, not as evidence about the branch.** ⚠ The
packet also reports this as "ΔAIC +30.0", and that number carries no
information the ratio does not: the code computes
`ΔAIC = N·ln(SSR_i/SSR_ii)` exactly, so it is the SSR ratio in a likelihood
costume. The likelihood is fictional here — M_n is an exact deterministic
max-reduction with no sampling noise, and the residuals are misspecification,
not scatter (they drift monotonically). An information criterion that
multiplies by N inflates a highly-correlated 16-point fit. The defensible
statement is the SSR ratio plus a held-out check, not a model-selection
verdict.

So the earlier "mild evidence toward the stronger-than-Tao branch" does not
survive the comparison, and the current direction of *fit* is branch (ii).
Neither resolution is confirmed. Branch (ii) is a statement about the
asymptotics of L(n) for all n; **no float64 fit over n ≤ 21 can constrain
it**, and any downstream packet that cites this section rather than the
streaming packet's §5 "Honest scope" would be laundering a measurement into
a premise. This remains the only live route whose success condition is
"beats Tao", and it is decided by depth measurements, not by a new idea.

## ESTABLISHED

- **Fold non-conjugacy, k ≤ 10.** No two folds at distinct depths k, k′ ≤ 10
  are affinely conjugate; exact counting-law screen over all 2,046 classes
  (85 distinct laws), independently reimplemented. [`contribution/note/NOTE.md`](contribution/note/NOTE.md), [`contribution/proofs/LEMMA2_PROOF.md`](contribution/proofs/LEMMA2_PROOF.md)
- **Realizability criterion Φ(q).** A parity transcript q is realized by a
  positive integer iff Φ(q) = −Σ 2^(d_j)/3^(j+1) ∈ ℤ_{>0}; eventually-periodic
  transcripts decidable, (n+b)/2 family non-universal. [`contribution/proofs/PARTIAL_THEOREMS.md`](contribution/proofs/PARTIAL_THEOREMS.md)
- **Cycle exclusion, ≤ 20 odd members.** No nontrivial positive cycle with at
  most 20 odd members; exact search with independent oracle (m ≤ 18), extended
  to m ≤ 20 by a dual-enumerator scan of 6.20 × 10⁸ valuation words per phase
  (1.24 × 10⁹ word-scans across both phases) with zero hits. Dominated by
  Hercher 2023 (≤ 91 local minima); kept as an exact-arithmetic oracle, not as
  a frontier bound. [`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md), [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/)
- **Automatic-transcript trichotomy.** Subcritical and critical strata of
  2-automatic parity words closed (Lemmas A–C, Theorems 1–4); the
  supercritical stratum is nonempty and exactly equivalent to a divergent
  2-automatic orbit. [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/)
- **Automatic transcripts closed in every base.** López–Stoll 2021 force a
  rational non-cyclic trajectory to have lower parity density exactly
  `log₃2`. Bell 2020 proves that the lower density of every `k`-automatic set
  is rational. Since `log₃2` is irrational, no rational non-cyclic trajectory
  has a `k`-automatic parity word for any `k ≥ 2`. This includes all divergent
  positive orbits and all uniform-morphic parity words. The critical-density
  gap remains open only for non-automatic words.
  [`contribution/packets/2026-08-01-automatic-density-closure/`](contribution/packets/2026-08-01-automatic-density-closure/)
- **Morphic transcripts with natural frequency closed.** If a morphic parity
  word has a natural one-frequency, that frequency is algebraic. López–Stoll
  force a rational non-cyclic trajectory's lower frequency to be `log₃2`,
  which is transcendental. Therefore any morphic parity word of a rational
  non-cyclic trajectory must have no natural one-frequency. Non-uniform
  morphic words without natural frequency remain open. Same packet.
- **⚠ SUBSUMED — supercritical stratum.** The exclusion below is superseded:
  López–Stoll ([arXiv:2101.12747](https://arxiv.org/abs/2101.12747), 2021)
  already prove that aperiodic q with liminf s_L/L > log₃2 has Φ(q) ∉ ℚ_odd,
  which kills all 109 survivors directly. **The remaining gap is now the
  single critical density liminf s_L/L = log₃2 exactly** — everything strictly
  above and strictly below is closed. See [`PRIORITY.md`](PRIORITY.md) §1.
  Retained below for the machinery, which is still the only tool that bites at
  the critical density.
- **Supercritical stratum: 99 of 109 closed (machinery, not conclusion).** The enumerated supercritical
  survivors are excluded by a *proved* upper bound on the factor-complexity
  constant C = limsup p_q(k)/k, computed from the exact factor language of
  each fixed point (Lemma D) and fed into the landmark packet's existing
  Corollaries 4 and 7. 97/109 need no cited input; 99/109 with the unique
  ergodicity of primitive substitutions. All 56 binary-morphism survivors
  closed; the 10 that remain are ternary-coded and are **not** bound slack —
  their exact p(1537)/1537 already exceeds α/(ρ−α). Witness 1 of the
  rigidity packet (σ(0)=11, σ(1)=10, ρ=2/3) dies on the single integer
  comparison 3²⁷ < 2⁴³. [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/)
- **⚠ REFRESH, not new — contraction onset.** Re-derives Terras (1976)
  coefficient stopping time; Garner (1981) reached κ(n) < 105,000. This is the
  same argument with Bařina's 2^71 in place of 2×10⁹. See [`PRIORITY.md`](PRIORITY.md) §5.
- **Contraction onset, h ≤ 10⁶.** A minimal counterexample `m` satisfies
  `2^(A_h) ≤ 3^h` for every `h ≤ 1,000,000` Syracuse steps — every prefix of
  its parity word is supercritical over the first ~1.58 × 10⁶ Terras steps,
  unconditionally and with no liminf. Two elementary lemmas (descent requires
  contraction; `C_h ≤ h·3^(h-1)` before onset) bound `m` by
  `M(h) = ⌊h·3^(h-1)/(2^(A*(h)) − 3^h)⌋`, whose max over that range is
  `9.85 × 10¹¹` — nine orders below Bařina's `2^71`. Records of `M` sit at the
  convergents and semiconvergents of `log₂3`, i.e. the resonance lattice.
  Separately, no odd `x > 1` up to `1.45 × 10⁹` contracts before it descends.
  [`contribution/packets/2026-07-24-contraction-onset/`](contribution/packets/2026-07-24-contraction-onset/)
- **Plateau-escape-weight reduction.** Uniform decay of M_n reduced, with a
  proved tight rate, to the integer length L(n) of the bad chain interval per
  layer (P1–P4, P6); bounds on L(n) of log type imply decay past Tao's
  n^(−A); measured dichotomy edge n* = 1776 from measured constants (float64
  measurement). [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Deep Fourier scan to n = 17.** Resonance chain intact at every layer
  6 ≤ n ≤ 17 (exact base-2 discrete logs); the measured window law
  k(n) ∈ [n, n+3] falsified at n = 16 and restated as
  k(n) ≈ 1.343n − 1.774 (float64 measurement, not a theorem). [`contribution/packets/2026-07-22-deep-fourier-scan/`](contribution/packets/2026-07-22-deep-fourier-scan/)
- **Lean 4 certificates (zero sorry).** `formal/` (plain Lean 4 core, no
  mathlib, toolchain v4.31.0): eight modules compile with empty axiom
  bases beyond the classical triple — Terras bijection (Theorem 1),
  two-branch-family non-universality (Theorem 4), parity-block collision
  principle, pigeonhole, chain closure (the chain frequencies are an
  invariant subsystem of the proved recursion; k ↦ k−a index dynamics),
  the Beatty kill triple (phase-free LP infeasibility over ℚ, Sturmian
  balance failure via a general lemma, exact CF enclosures of log₂3 with
  a semiconvergent refinement pinning a₉ = 23), contraction onset
  (cocycle identity 2^{A_h}·y = 3^h·x + C_h, Lemma 1, the M(h) onset
  theorem), and cycle exclusion (cycle equation from the odd map,
  sound verified exclusion checker, kernel-verified layers m ≤ 4). First
  artifacts toward a google-deepmind/formal-conjectures contribution.
  [`formal/`](formal/)
- **Odometer dominance survives to n = 1000 (measurement).** The chain
  recursion (4.1) at high precision: dominant pullback a = 1 at all 1000
  layers (margin ≥ 0.239, w₁ ∈ [0.504, 0.647], flat tail slope
  −2.7e-7/layer); Δk ∈ {1,2} throughout (578/419). **The drift fork
  breaks toward slope log₂3:** the ≈0.118/layer δ drift does NOT
  persist — full-range linear fit gives 4.35e-4/layer (tail 2.8e-5),
  ranking log > sqrt > linear on both full range and tail; δ(n) ∈ [3.09,
  7.26], implied k-slope 1.5845 vs log₂3 = 1.58496. The dominance ⇒
  odometer gap is real but closing: on Δk = 2 layers the feed sits one
  above the old peak with ρ_n ≥ 0.9387, fit slope +3.8e-6/layer. The
  single-threshold rule dies for n ≥ 500. Non-resonant background decays
  ~3^{−n/2} while M_n ~ e^{−2.48√n} — the peak separates exponentially;
  no chain-escape signature.
  [`contribution/packets/2026-08-01-odometer-dominance/`](contribution/packets/2026-08-01-odometer-dominance/)
- **Plateau drift test to n = 20.** C-kernel layer recursion (n=17: 80 s →
  2.3 s); certified depth n = 20 with exact full-sweep escape weights. The
  n ≈ 22 p₂ > 0.95 crossing prediction **falsified on schedule** (p₂(20) =
  0.8013 vs extrapolated 0.94); new parity alternation of w_n(0.05);
  decay and chain laws intact (float64 measurements). [`contribution/packets/2026-07-23-plateau-drift-test/`](contribution/packets/2026-07-23-plateau-drift-test/)
  **⚠ The p₂ reading above is superseded** — see the streaming packet: the
  p₂ extrapolation was misspecified (parity is a proxy for Δk), so the
  "falsification" was not evidence about the trend.
- **Streaming depth n = 21.** Layer certified without ever materialising it
  (17.3 GiB peak vs 69.3 GiB resident, 4× reduction), bit-identity gated and
  validated to zero difference against the certificate at n = 18 and n = 20.
  M₂₁ = 0.0078721330, k = 28, p₂ = 0.887281 (**all-time high**), L(0.2) = 4;
  no kill criterion fired. Two corrections to the predecessor's reading:
  (1) p₂ direction is fixed by Δk(n) = k(n)−k(n−1), with Δk ≥ 2 ⟺ p₂ rises,
  **15/15 transitions n = 7..21** — parity was a proxy that breaks at the
  first consecutive Δk = 2 pair (n = 20, 21); refit on the Δk = 2 subsequence
  puts the 0.95 crossing at n ≈ 32, with n = 21 above trend.
  (2) Direct P6 branch comparison on the M_n decay law (never run before)
  favours the **√n / Tao-strength branch**: ΔAIC +30.0 full window, +13.0 on
  n ≥ 13, strengthened by adding n = 21. [`contribution/packets/2026-07-24-streaming-depth-21/`](contribution/packets/2026-07-24-streaming-depth-21/)

- **Pointwise drift wall.** Subcritical aperiodic words are excluded as
  positive-integer states at critical drift α = log₃2, with no structural
  hypothesis on the parity word; combines with complexity pressure into a
  two-wall screen. [`contribution/packets/2026-07-22-pointwise-drift-wall/`](contribution/packets/2026-07-22-pointwise-drift-wall/)
- **Analytic-side packets (Tao route).** Structural refinement of Tao's
  exceptional set (description, not size); exact Syracuse Fourier recursion
  with exponential L² mixing and a computed spectral barrier; three exact
  second-moment reductions onto the 2–3 resonance chain; structure–randomness
  crosswalk. Each states explicitly that it is **not** a stronger density
  theorem than Tao's. [`.../2026-07-22-tao-structural-refinement/`](contribution/packets/2026-07-22-tao-structural-refinement/), [`.../2026-07-22-syracuse-fourier/`](contribution/packets/2026-07-22-syracuse-fourier/), [`.../2026-07-22-scalar-phase-second-moment/`](contribution/packets/2026-07-22-scalar-phase-second-moment/), [`.../2026-07-22-structure-randomness-transfer/`](contribution/packets/2026-07-22-structure-randomness-transfer/)

- **Dimension of the surviving set.** `G = {q : liminf s_L/L = α}` has
  Bernoulli(1/2) measure **zero** but Hausdorff dimension
  **≥ H(α) ∈ (0.949952152, 0.949957233)**, by containment of the
  Besicovitch–Eggleston level set. Exact rational bounds, each certified by one
  integer comparison. Consequence: density and measure arguments — Tao's
  included — are **structurally blind** to the remaining gap, and it is far too
  large to dismiss as degenerate. [`contribution/code/dimension_bracket.py`](contribution/code/dimension_bracket.py)
- **The Mahler tower, and where it breaks.** For every letter-coding of a
  fixed point of a k-uniform morphism, Φ(q) is the value at the rational point
  (z,y) = (2, 3^(−τ)) of an explicit d-dimensional functional system with
  substitution (z,y) ↦ (z^k, y^M), M the incidence matrix. **The mixed bases 2
  and 3 do not obstruct the equation** — they are absorbed by the monomial
  substitution. They obstruct the **evaluation point**: the y-coordinates are
  2-adic units, the boundary case excluded by every form of Mahler's method,
  and the induced one-variable tower converges iff τM^e → 0 in ℤ₂^d. Of the ten
  then-open supercritical survivors, **6 fail that condition and 4 satisfy it**
  — a split no previous instrument here could see. All ten verdicts are proved
  (F₂ pigeonhole, not an extrapolation). Closes `TARGETS.md` bounded check 1
  affirmatively and relocates the obstruction. The 2026-08-01 automatic-density
  corollary now closes all ten without Mahler theory. Prior art searched:
  nothing found connecting Φ to Mahler functions.
  [`contribution/packets/2026-07-25-mahler-tower/`](contribution/packets/2026-07-25-mahler-tower/)
- **Corollary 4 referee note.** Self-contained statement, proof, prior-art
  separation and four referee questions for the one result the priority search
  did not find in prior art. The externalization artifact. [`REFEREE_NOTE.md`](REFEREE_NOTE.md)
- **Corollary 7 proved.** Density-refined complexity floor
  `limsup p_q(k)/k ≥ α/(β−α)` under a uniform ones-cap `β > α`. Same mechanism
  as Corollary 4 with the Green unrolling + ones-cap. Exact verifier
  (unroll identity, growth bound, rate algebra, boundary).
  [`contribution/packets/2026-08-01-corollary-7-proof/`](contribution/packets/2026-08-01-corollary-7-proof/)

## BLOCKED

- **No complexity-consuming instrument exists.** Searched 2026-07-25. Every
  saturation in `TARGETS.md` has one cause — Corollary 4 is a *lower* bound, so
  it kills only simple objects — and the literature has no converse. Structural
  reason: factor complexity is an invariant of the **orbit closure**, while
  `Φ(q) ∈ ℚ_odd` is a condition on a **single point**; high complexity makes the
  closure large and the arithmetic hypothesis invisible. ×2×3 rigidity
  (Furstenberg, Rudolph, EKL) needs a jointly invariant measure of positive
  entropy — which is what one would be proving. **Redirect:** change the
  hypothesis from "low complexity" to "automatic/morphic" and switch to
  **Mahler's method**, which is indifferent to complexity level. Two bounded
  checks first: the mixed-base `(2,3)` functional equation, and a 2-adic form of
  the Adamczewski–Faverjon dichotomy. [`TARGETS.md`](TARGETS.md)
  **⚠ Check 1 is now run (2026-07-25) and the framing was wrong.** The
  functional equation exists for every uniform morphism; the mixed bases are
  absorbed by a monomial substitution. The obstruction is the evaluation point,
  which sits on the excluded unit-disc boundary because 3 is a 2-adic unit. So
  check 2 is not sufficient either: what is needed is a Mahler-type theorem
  tolerating **boundary points in the non-driving variables**, which no
  searched source provides. See
  [`2026-07-25-mahler-tower`](contribution/packets/2026-07-25-mahler-tower/).
- **Shadow-barrier: killed.** Its Theorem 2 restates its own hypothesis, so it
  excludes nothing; its regime `s_L/L − α = o(1/L)` is strictly narrower than
  the surviving gap and is assumed, not proved. [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/)
- **Amplification via inverse/cylinder families: killed.** Tracking time equals
  2-adic proximity exactly (Theorem A, folklore strength); inverse-tree
  elements get a free descent to the join point (Theorem B). Both natural
  families fail provably, the `TARGETS.md` §1 circularity criterion fired on
  the smallest case (`y=27, L=20`), and the missing implication is named:
  permanence past the handoff state. The branch itself remains open and
  unentered — only the mechanism is dead.
  [`contribution/packets/2026-08-01-amplification-cylinder-nogo/`](contribution/packets/2026-08-01-amplification-cylinder-nogo/)

- **Beatty/rotation hypothesis for k(n): killed exactly.** The chain peak
  exponent k(n) (n = 6..21: 6,8,9,10,12,13,14,16,17,18,20,21,23,24,26,28) is
  not ⌊γn⌋ for any γ: exact `Fraction` LP over all 256 ordered pairs is
  infeasible, witnesses force γ > 3/2 and γ < 11/8 simultaneously; Δk =
  (2,1,1,2,1,1,2,1,1,2,1,2,1,2,2) fails Sturmian balance (contains both (1,1)
  and (2,2) factors); 22/15 is not in the CF tree of log₂3 =
  [1;1,1,2,2,3,1,5,2,23,…]. All three pre-registered kill criteria fire.
  In its place the chain recursion is an **exact closed subsystem**:
  dominant pullback is always a = 1, so x_n = 2^{k(n)−1}/3^n obeys the
  odometer identity x_n = (2^{Δk}/3)·x_{n−1} with Δk ∈ {1,2}; reproduces
  k(n) and M_n to 7.5 × 10⁻¹⁴ against the certified layer engines on the
  n = 6..21 window. Over that **shallow window only**, δ(n) in
  k(n) = n·log₂3 − δ(n) drifted ≈ 0.118/layer with δ ∈ [3.09, 6.12]. That
  linear-δ reading **does not survive** to n = 1000 — see ESTABLISHED
  odometer-dominance (full-range slope ~4.35×10⁻⁴/layer; model ranking
  prefers logarithmic δ). a = 1 dominance and chain-mass closure remain
  theorem candidates; Lean certificates cover the Beatty kill and the
  integer mass half of chain closure, not the analytic odometer.
  [`contribution/packets/2026-08-01-chain-exponent-law/`](contribution/packets/2026-08-01-chain-exponent-law/),
  [`contribution/packets/2026-08-01-odometer-dominance/`](contribution/packets/2026-08-01-odometer-dominance/)
- **Phase-blind propagation.** Proved impossible (P2, P5): no
  finite-check-at-one-layer plus phase-blind propagation argument can
  establish w_n(ε) ≥ w > 0; the missing input is the intrinsic chain phase
  pattern at every layer. [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **The critical density, liminf s_L/L = log₃2 exactly.** The whole remaining
  gap on the symbolic side, once López–Stoll 2021 is combined with the drift
  wall. Frequency-based arguments are vacuous there by construction; the
  factor-complexity bound is the only instrument that still bites, and it is
  also the one thing in this repository the priority search did not find in
  prior art. [`PRIORITY.md`](PRIORITY.md)
- **No bound on L(n).** No proved bound on L(n) beyond n ≤ 13; measurements
  run to n = 20 (drift-test packet). [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Cycle exclusion wall at m = 21.** The next layer (21, 34) has
  5.7 × 10⁸ valuation words per phase — feasible but not worthwhile: Hercher/Bařina
  dominate the atlas bound by ~11 orders of magnitude. [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/)
- **Remaining formalization gaps.** The realizability criterion Φ(q)
  needs 2-adic machinery (mathlib `PadicInt`), and the fold non-conjugacy
  screen needs KMP-automaton formalization; cycle exclusion is
  kernel-verified only to m ≤ 4 (m ≤ 20 remains external exact pipeline
  + sound Lean checker awaiting certificate import); the analytic
  results (Fourier decay, complexity floor) need reals. [`formal/`](formal/)

## NEXT

**Session method, lessons and transfer audits: [`meta/`](meta/README.md).**
Every session ends with a `meta/LEDGER.md` entry — strategy, what worked, what
failed, mistakes, lesson. A session without one produces no compounding.

**Ranked attack targets with odds, fallbacks and kill criteria:
[`TARGETS.md`](TARGETS.md).** Read it before choosing work. Summary of the
ranking by importance-if-landed: (1) amplification — the only never-entered
half of the architecture; (2) the critical-density gap for arbitrary
non-automatic words; (3) non-uniform morphic transcripts; (4) contraction
onset to infinity — **closed door**, capped by construction at ~10¹⁰ steps
regardless of Diophantine input; (5) the formal-conjectures port. Automatic
and uniform-morphic transcripts are closed by the 2026-08-01 density corollary.

The individual entries below remain accurate; `TARGETS.md` orders them and
adds the ones that were missing.

- **formal-conjectures contribution.** Target: the Collatz section of
  google-deepmind/formal-conjectures (one file today: bare `collatzStep` +
  conjecture). Route (corrected 2026-07-23 after external review; still
  current): port **statements only** — their CONTRIBUTING caps in-repo
  proofs at ~25–50 lines; longer proofs are hosted here and linked via
  `@[formal_proof using lean4 at "<commit url>"]`, which our zero-sorry
  `formal/` modules satisfy (two-branch, Terras, collision, chain, Beatty,
  contraction onset, cycle checker). Lead with the **two-branch family**
  (`research solved`; "solved variants of open conjectures" are explicitly
  welcomed), then ask in the pre-PR issue whether the Terras bijection is
  in scope as `API` support or belongs in mathlib. The stronger long-term
  contribution is a Terras-accelerated equivalent formulation of Collatz
  (`research open`), which first needs a Lean proof of
  `collatzStep reaches 1 ↔ T reaches 1` — not yet formalized. Gates: Google
  CLA; pre-PR issue posted by the repo owner. [`formal/`](formal/)
- **Shadow-barrier exploratory integration.** Exact two-metric barrier for
  rational shadows (real divergence vs 2-adic convergence along near-neutral
  contractive subsequences), integrated under exploratory/ with verbatim
  provenance from chatgpt-thread-1784792218410; exploratory status, not cited
  as a result. [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/)
