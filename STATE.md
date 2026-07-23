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
- **Cycle exclusion, ≤ 18 odd members.** No nontrivial positive cycle with at
  most 18 odd members; exact search with independent oracle. [`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md)
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

## BLOCKED

- **Phase-blind propagation.** Proved impossible (P2, P5): no
  finite-check-at-one-layer plus phase-blind propagation argument can
  establish w_n(ε) ≥ w > 0; the missing input is the intrinsic chain phase
  pattern at every layer. [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **Supercritical automatic stratum.** Open; shown density-proof — no
  density argument can close it (Theorem 3 of the rigidity packet). [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/)
- **No bound on L(n).** No proved bound on L(n) beyond n ≤ 13; measurements
  run to n = 14. [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/)
- **n = 18 layer construction (Python verifier).** Engineering wall:
  layer-18 construction exceeded the 300 s foreground budget and was killed;
  n = 17 is the certified depth of the Python scan. [`contribution/packets/2026-07-22-deep-fourier-scan/`](contribution/packets/2026-07-22-deep-fourier-scan/)

## NEXT

- **Plateau-drift-test packet.** C-kernel rebuild of the layer recursion;
  depth certified to n = 19 in 48.2 s wall clock (n = 19: p2 = 0.721,
  k = 24). Remaining: extend depth past n = 19 and test the p2 > 0.95
  crossing — the n ≤ 14 fit predicted n ≈ 18.9; the refit through n = 19
  moves the crossing to n ≈ 32.2 (float64 measurements). [`contribution/packets/2026-07-23-plateau-drift-test/`](contribution/packets/2026-07-23-plateau-drift-test/)
- **Shadow-barrier exploratory integration.** Exact two-metric barrier for
  rational shadows (real divergence vs 2-adic convergence along near-neutral
  contractive subsequences), integrated under exploratory/ with verbatim
  provenance from chatgpt-thread-1784792218410; exploratory status, not cited
  as a result. [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/)
