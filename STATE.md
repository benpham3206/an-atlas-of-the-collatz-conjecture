# Repository state

Frontier of the fold program: what is established, what is blocked, and what
runs next. Proved statements use exact integer/rational arithmetic; float64
outputs are measurements, not theorems, and are labelled as such. The Collatz
conjecture remains open; nothing here proves or disproves it. Updated
2026-07-25.

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
- **Supercritical stratum: 99 of 109 closed.** The enumerated supercritical
  survivors are excluded by a *proved* upper bound on the factor-complexity
  constant C = limsup p_q(k)/k, computed from the exact factor language of
  each fixed point (Lemma D) and fed into the landmark packet's existing
  Corollaries 4 and 7. 97/109 need no cited input; 99/109 with the unique
  ergodicity of primitive substitutions. All 56 binary-morphism survivors
  closed; the 10 that remain are ternary-coded and are **not** bound slack —
  their exact p(1537)/1537 already exceeds α/(ρ−α). Witness 1 of the
  rigidity packet (σ(0)=11, σ(1)=10, ρ=2/3) dies on the single integer
  comparison 3²⁷ < 2⁴³. [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/)
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
  mathlib, toolchain v4.31.0): the Terras bijection (Theorem 1) and the
  two-branch-family non-universality (Theorem 4) compile with empty axiom
  bases beyond the classical triple. First artifacts toward a
  google-deepmind/formal-conjectures contribution. [`formal/`](formal/)
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

## BLOCKED

- **Phase-blind propagation.** Proved impossible (P2, P5): no
  finite-check-at-one-layer plus phase-blind propagation argument can
  establish w_n(ε) ≥ w > 0; the missing input is the intrinsic chain phase
  pattern at every layer. [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Supercritical automatic stratum.** Still open as a *class* statement —
  "no divergent Collatz orbit has a 2-automatic parity word" is unproved,
  and no density argument can close it (Theorem 3 of the rigidity packet).
  What changed 2026-07-24: the *enumerated* part of the stratum is no longer
  109 words but **10 named ternary-coded automata**, because the obstruction
  there was complexity, not density. The general statement needs a bound on
  C for automata that are not codings of uniform-morphism fixed points; no
  such bound exists here. [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/), [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/)
- **No bound on L(n).** No proved bound on L(n) beyond n ≤ 13; measurements
  run to n = 20 (drift-test packet). [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Cycle exclusion wall at m = 21.** The next layer (21, 34) has
  5.7 × 10⁸ valuation words per phase — feasible but not worthwhile: Hercher/Bařina
  dominate the atlas bound by ~11 orders of magnitude. [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/)
- **Full formalization.** Only Theorems 1 and 4 carry Lean certificates;
  the realizability criterion Φ(q) needs 2-adic machinery (mathlib
  `PadicInt`), and the fold non-conjugacy screen needs KMP-automaton
  formalization — both future work. [`formal/`](formal/)

## NEXT

**Session method, lessons and transfer audits: [`meta/`](meta/README.md).**
Every session ends with a `meta/LEDGER.md` entry — strategy, what worked, what
failed, mistakes, lesson. A session without one produces no compounding.

**Ranked attack targets with odds, fallbacks and kill criteria:
[`TARGETS.md`](TARGETS.md).** Read it before choosing work. Summary of the
ranking by importance-if-landed: (1) amplification — the only never-entered
half of the architecture; (2) the 2-automatic Gap in full; (3) the Gap for
DFAOs with ≤ N states — **run 2026-07-24, N = 2; the complexity method
saturates at two states and does not scale, which retires (2) by that route**;
(4) morphic transcripts of linear complexity; (5) the ten remaining automata;
(6) contraction onset to infinity — **closed door**, capped by construction at
~10¹⁰ steps regardless of Diophantine input; (7) the formal-conjectures port.

The individual entries below remain accurate; `TARGETS.md` orders them and
adds the ones that were missing.

- **formal-conjectures contribution.** Target: the Collatz section of
  google-deepmind/formal-conjectures (one file today: bare `collatzStep` +
  conjecture). Route: port the zero-sorry Lean proofs (Terras bijection
  first, then two-branch family, now also the collision principle) into
  their mathlib-based style and open the required pre-PR issue. [`formal/`](formal/)
- **The ten remaining supercritical automata.** Each needs a genuinely
  different argument: their factor-complexity constants are exactly computed
  and sit *above* α/(ρ−α), so no sharpening of Lemma D reaches them. Either
  find a second inequality that consumes complexity rather than requiring it,
  or decide the lift-digit question for these ten words directly. [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/)
- **Shadow-barrier exploratory integration.** Exact two-metric barrier for
  rational shadows (real divergence vs 2-adic convergence along near-neutral
  contractive subsequences), integrated under exploratory/ with verbatim
  provenance from chatgpt-thread-1784792218410; exploratory status, not cited
  as a result. [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/)
