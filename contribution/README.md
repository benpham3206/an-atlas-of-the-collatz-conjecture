# Fold program

Original results on the first-return structure of the Terras-accelerated Collatz
map. Not progress on the Collatz conjecture; the conjecture remains open.

## Contents

| Path | Contents | Status |
|---|---|---|
| [`note/NOTE.md`](note/NOTE.md) | Theorem, proof, scope | write-up |
| [`proofs/LEMMA2_PROOF.md`](proofs/LEMMA2_PROOF.md) | Counting-law lemma, all k, t | proved |
| [`proofs/PARTIAL_THEOREMS.md`](proofs/PARTIAL_THEOREMS.md) | Realizability criterion Φ(q); decidable islands; (n+b)/2 family | proved |
| [`proofs/FENCE.md`](proofs/FENCE.md) | Undecidability boundary for the fixed 3n+1 map | analysis |
| [`proofs/FORMALIZATION.md`](proofs/FORMALIZATION.md) | H_T, R_T, arithmetical hierarchy | formalization |
| [`proofs/LIFT_COCYCLE.md`](proofs/LIFT_COCYCLE.md) | ε-lift; binary digits of Φ(q) | probe |
| [`code/`](code/) | Exact-arithmetic implementations and tests | reproducible |
| [`reports/`](reports/) | Run logs and evidence | evidence |
| [`DEFINITIONS.md`](DEFINITIONS.md) | Primitives: drift, inertia, fold, realizability | definitions |

## Code

| File | Function | Runtime |
|---|---|---|
| `code/f1_word_calculus.py` | Composite affine forms; Terras bijection; cycle sweep | test ~58 s |
| `code/f2_fold_operator.py` | Exact induced first-return maps | test ~11 min |
| `code/f2b_analytic_screen.py` | Counting-law screen | ~1 s |
| `code/f4_feature_regression.py` | Feature vs mod-2^k baseline (null result) | test ~2 s |
| `code/fence/` | Fence phase scan; transcript-lift oracle | fast |

Each `test_*.py` recomputes its claims from scratch.

## Results

1. Fold non-conjugacy theorem, depths k ≤ 10. Proof in `note/NOTE.md` and
   `proofs/LEMMA2_PROOF.md`. Screen: `code/f2b_analytic_screen.py`.
2. Realizability criterion Φ(q) ∈ ℤ_{>0} and consequences.
   `proofs/PARTIAL_THEOREMS.md`.
3. Null results (closed approach families): `reports/F4_REPORT.md`.

Independent verification: `reports/VERIFICATION.md` (GPT-5.6 Sol).
