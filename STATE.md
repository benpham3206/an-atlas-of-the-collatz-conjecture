# Repository state

Frontier of the fold program: what is established, what is blocked, and what
runs next. Proved statements use exact integer/rational arithmetic; float64
outputs are measurements, not theorems, and are labelled as such. The Collatz
conjecture remains open; nothing here proves or disproves it. Updated
2026-07-23.

## ESTABLISHED

- **Fold non-conjugacy, k ≤ 10.** No two folds at distinct depths k, k′ ≤ 10
  are affinely conjugate; exact counting-law screen over all 2,046 classes
  (85 distinct laws), independently reimplemented. [`contribution/note/NOTE.md`](contribution/note/NOTE.md), [`contribution/proofs/LEMMA2_PROOF.md`](contribution/proofs/LEMMA2_PROOF.md)
- **Realizability criterion Φ(q).** A parity transcript q is realized by a
  positive integer iff Φ(q) = −Σ 2^(d_j)/3^(j+1) ∈ ℤ_{>0}; eventually-periodic
  transcripts decidable, (n+b)/2 family non-universal. [`contribution/proofs/PARTIAL_THEOREMS.md`](contribution/proofs/PARTIAL_THEOREMS.md)
- **Cycle exclusion, ≤ 20 odd members.** No nontrivial positive cycle with at
  most 20 odd members; exact search with independent oracle (m ≤ 18), extended
  to m ≤ 20 by a dual-enumerator scan of 1.24 × 10⁹ valuation words with
  zero hits. [`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md), [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/)
- **Automatic-transcript trichotomy.** Subcritical and critical strata of
  2-automatic parity words closed (Lemmas A–C, Theorems 1–4); the
  supercritical stratum is nonempty and exactly equivalent to a divergent
  2-automatic orbit. [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/)
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

## BLOCKED

- **Phase-blind propagation.** Proved impossible (P2, P5): no
  finite-check-at-one-layer plus phase-blind propagation argument can
  establish w_n(ε) ≥ w > 0; the missing input is the intrinsic chain phase
  pattern at every layer. [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Supercritical automatic stratum.** Open; shown density-proof — no
  density argument can close it (Theorem 3 of the rigidity packet). [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/)
- **No bound on L(n).** No proved bound on L(n) beyond n ≤ 13; measurements
  run to n = 20 (drift-test packet). [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Cycle exclusion wall at m = 21.** The next layer (21, 34) has
  5.7 × 10⁸ valuation words — feasible but not worthwhile: Hercher/Bařina
  dominate the atlas bound by ~11 orders of magnitude. [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/)
- **Full formalization.** Only Theorems 1 and 4 carry Lean certificates;
  the realizability criterion Φ(q) needs 2-adic machinery (mathlib
  `PadicInt`), and the fold non-conjugacy screen needs KMP-automaton
  formalization — both future work. [`formal/`](formal/)

## NEXT

- **formal-conjectures contribution.** Target: the Collatz section of
  google-deepmind/formal-conjectures (one file today: bare `collatzStep` +
  conjecture). Route (corrected 2026-07-23 after external review): port
  STATEMENTS only — their CONTRIBUTING caps in-repo proofs at ~25–50 lines;
  longer proofs are hosted here and linked via
  `@[formal_proof using lean4 at "<commit url>"]`, which our zero-sorry
  proofs satisfy. Lead with the **two-branch family** (`research solved`;
  "solved variants of open conjectures" are explicitly welcomed), then ask
  in the pre-PR issue whether the Terras bijection is in scope as `API`
  support or belongs in mathlib. The stronger long-term contribution is a
  Terras-accelerated equivalent formulation of Collatz (`research open`),
  which first needs a Lean proof of
  `collatzStep reaches 1 ↔ T reaches 1` — not yet formalized. Gates: Google
  CLA; pre-PR issue posted by the repo owner. [`formal/`](formal/)
- **Shadow-barrier exploratory integration.** Exact two-metric barrier for
  rational shadows (real divergence vs 2-adic convergence along near-neutral
  contractive subsequences), integrated under exploratory/ with verbatim
  provenance from chatgpt-thread-1784792218410; exploratory status, not cited
  as a result. [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/)
