# Fold program

Definitions, proofs, exact-arithmetic programs, and verification records for the
first-return systems studied in this repository. These results do not prove or
disprove the Collatz conjecture.

## Files

| Path | Contents | Evidentiary status |
|---|---|---|
| [`note/NOTE.md`](note/NOTE.md) | Fold theorem, proof outline, and limitations | theorem write-up |
| [`proofs/LEMMA2_PROOF.md`](proofs/LEMMA2_PROOF.md) | Counting-law lemma for all k and t | proof |
| [`proofs/PARTIAL_THEOREMS.md`](proofs/PARTIAL_THEOREMS.md) | Realizability criterion, eventually periodic transcripts, and the (n+b)/2 family | proofs |
| [`proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](proofs/EXACT_COUNTEREXAMPLE_SEARCH.md) | Exact odd-only cycle search; no nontrivial cycle with ≤ 18 odd members | verified bounded exclusion |
| [`proofs/RATIONAL_IRRATIONAL_SHADOW.md`](proofs/RATIONAL_IRRATIONAL_SHADOW.md) | Rational periodic shadows of aperiodic parity laws | exact theorem + verifier |
| [`proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md`](proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md) | Subcritical primitive substitutions cannot be rational Collatz transcripts | pointwise exclusion |
| [`proofs/FENCE.md`](proofs/FENCE.md) | Distinction between generalized undecidability results and the fixed 3n+1 map | boundary analysis |
| [`proofs/FORMALIZATION.md`](proofs/FORMALIZATION.md) | Definitions of H_T and R_T and their arithmetical-hierarchy form | formal specification |
| [`proofs/LIFT_COCYCLE.md`](proofs/LIFT_COCYCLE.md) | Lift recurrence and finite transcript experiments | proved recurrence; bounded experiments |
| [`packets/2026-07-22-landmark-pointwise/`](packets/2026-07-22-landmark-pointwise/) | Landmark strategy, strategy machine, resonance lattice, prefix-return barrier, rational finite verifier | complete research packet |
| [`packets/2026-07-23-cycle-exclusion-extension/`](packets/2026-07-23-cycle-exclusion-extension/) | Cycle exclusion extended to ≤ 20 odd members (dual-enumerator scan, zero hits) | verified bounded exclusion |
| [`packets/2026-08-01-automatic-density-closure/`](packets/2026-08-01-automatic-density-closure/) | No rational non-cyclic trajectory has an automatic parity word; morphic natural-frequency corollary | proved synthesis of published theorems |
| [`packets/2026-08-01-corollary-7-proof/`](packets/2026-08-01-corollary-7-proof/) | Corollary 7 proved: ones-capped factors force `limsup p(k)/k ≥ 1/g` | proof + exact verifier |
| [`packets/2026-08-01-chain-exponent-law/`](packets/2026-08-01-chain-exponent-law/) | Beatty/rotation law for k(n) killed exactly; exact chain recursion Δk ∈ {1,2} | exact kill + measurement |
| [`packets/2026-08-01-odometer-dominance/`](packets/2026-08-01-odometer-dominance/) | a=1 dominance to n = 1000; δ-drift fork; Δk=2 feed gap | **measurement** (slim-v1 JSON + tests) |
| [`../formal/`](../formal/) | Zero-sorry Lean 4 certificates (Terras, two-branch, collision, chain integer half, Beatty kill, contraction onset lemmas, cycle checker m ≤ 4) | machine-checked |
| [`code/`](code/) | Exact-arithmetic implementations and executable checks | executable evidence |
| [`reports/`](reports/) | Recorded outputs and independent verification | verification records |
| [`DEFINITIONS.md`](DEFINITIONS.md) | Definitions used by the fold program | definitions |

## Code

| File | Function | Runtime |
|---|---|---|
| `code/f1_word_calculus.py` | Composite affine forms; Terras bijection; cycle sweep | test ~58 s |
| `code/f2_fold_operator.py` | Exact induced first-return maps | test ~11 min |
| `code/f2b_analytic_screen.py` | Counting-law screen | ~1 s |
| `code/f4_feature_regression.py` | Feature vs mod-2^k baseline (null result) | test ~2 s |
| `code/fence/` | Fence phase scan; transcript-lift oracle; exact cycle search; rational shadow | fast–medium |
| `packets/2026-07-22-landmark-pointwise/verify_rational_complexity_finite.py` | Rational-state finite complexity audit | fast |

Each `test_*.py` recomputes the values it checks.

## Results

1. Fold non-conjugacy theorem, depths k ≤ 10. Proof in `note/NOTE.md` and
   `proofs/LEMMA2_PROOF.md`. Screen: `code/f2b_analytic_screen.py`.
2. Realizability criterion Φ(q) ∈ ℤ_{>0} and consequences.
   `proofs/PARTIAL_THEOREMS.md`.
3. Negative feature-regression results: `reports/F4_REPORT.md`.
4. Exact exclusion of nontrivial positive cycles with m ≤ 20 odd members.
   `proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` (m ≤ 18) and
   `packets/2026-07-23-cycle-exclusion-extension/` (m ≤ 20);
   `code/fence/exact_cycle_search.py`.
5. Landmark / pointwise packet (strategy machine, resonance lattice,
   prefix-return barrier, rational finite verifier):
   `packets/2026-07-22-landmark-pointwise/`.
6. Automatic-density closure in every base, plus the morphic
   natural-frequency corollary:
   `packets/2026-08-01-automatic-density-closure/`.
7. Corollary 7 (density-refined complexity floor) fully proved:
   `packets/2026-08-01-corollary-7-proof/`.
8. Beatty kill + chain recursion target (n = 6..21 window), then odometer
   dominance measurement to n = 1000 (no new theorem):
   `packets/2026-08-01-chain-exponent-law/`,
   `packets/2026-08-01-odometer-dominance/`.
9. Lean 4 zero-sorry certificates in `../formal/` (scopes in
   `../formal/README.md` — not every packet bound is kernel-checked).

Independent verification: `reports/VERIFICATION.md` (GPT-5.6 Sol).
Agent one-pager: [`../COLLATZ_ONE_PAGE.md`](../COLLATZ_ONE_PAGE.md).
