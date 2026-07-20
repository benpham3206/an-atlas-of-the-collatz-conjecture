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
| [`proofs/FENCE.md`](proofs/FENCE.md) | Distinction between generalized undecidability results and the fixed 3n+1 map | boundary analysis |
| [`proofs/FORMALIZATION.md`](proofs/FORMALIZATION.md) | Definitions of H_T and R_T and their arithmetical-hierarchy form | formal specification |
| [`proofs/LIFT_COCYCLE.md`](proofs/LIFT_COCYCLE.md) | Lift recurrence and finite transcript experiments | proved recurrence; bounded experiments |
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
| `code/fence/` | Fence phase scan; transcript-lift oracle | fast |

Each `test_*.py` recomputes the values it checks.

## Results

1. Fold non-conjugacy theorem, depths k ≤ 10. Proof in `note/NOTE.md` and
   `proofs/LEMMA2_PROOF.md`. Screen: `code/f2b_analytic_screen.py`.
2. Realizability criterion Φ(q) ∈ ℤ_{>0} and consequences.
   `proofs/PARTIAL_THEOREMS.md`.
3. Negative feature-regression results: `reports/F4_REPORT.md`.

Independent verification: `reports/VERIFICATION.md` (GPT-5.6 Sol).
