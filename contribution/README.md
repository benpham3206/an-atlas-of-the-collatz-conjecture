# The fold program — original contribution

The question: **is the Collatz map self-similar under folding?** Take the map's
first-return behavior on a residue class mod 2^k, renormalize it, and you get
another system of the same kind — the map examining itself at depth k. If two
depths produced conjugate systems, that would be a self-similar structure worth
exploiting. This work proves they do not, for all depths ≤ 10, and along the way
gives an exact formula for the obstruction the whole conjecture rests on.

## Folder guide

| Path | What it holds | Status |
|---|---|---|
| [`note/NOTE.md`](note/NOTE.md) | The result written for a reader: theorem, proof sketch, scope | main write-up |
| [`proofs/LEMMA2_PROOF.md`](proofs/LEMMA2_PROOF.md) | The counting-law lemma, full proof (`PROVEN`, all k, t) | proof |
| [`proofs/PARTIAL_THEOREMS.md`](proofs/PARTIAL_THEOREMS.md) | Realizability formula Φ(q); decidable islands; the (n+b)/2 family | proofs |
| [`proofs/FENCE.md`](proofs/FENCE.md) | Where the undecidability boundary sits for the fixed 3n+1 map | map + obligations |
| [`proofs/FORMALIZATION.md`](proofs/FORMALIZATION.md) | Computability framing (H_T, R_T, arithmetical hierarchy) | formalization |
| [`proofs/LIFT_COCYCLE.md`](proofs/LIFT_COCYCLE.md) | The ε-lift: binary digits of Φ(q); first realizability probe | probe |
| [`code/`](code/) | Exact-arithmetic implementations + tests (stdlib only) | reproducible |
| [`reports/`](reports/) | Run logs and evidence for every numeric claim | evidence |
| [`DEFINITIONS.md`](DEFINITIONS.md) | The primitives ledger: drift, inertia, fold, realizability | vocabulary |

## Code map

| File | Role | Runtime |
|---|---|---|
| `code/f1_word_calculus.py` | Composite affine forms; Terras bijection; cycle sweep | test ~58 s |
| `code/f2_fold_operator.py` | Exact induced first-return maps (the fold operator) | test ~11 min |
| `code/f2b_analytic_screen.py` | Counting-law screen — the theorem's decisive computation | 0.64 s |
| `code/f4_feature_regression.py` | Null result: features vs mod-2^k baseline | test ~2 s |
| `code/fence/` | Fence phase scan + transcript-lift oracle | fast |

Each `test_*.py` re-derives its claims from scratch — no cached results trusted.

## Reading order

1. [`note/NOTE.md`](note/NOTE.md) — the whole result in a few pages.
2. [`reports/F2_REPORT.md`](reports/F2_REPORT.md) — where Fibonacci first appeared, in the data.
3. [`proofs/LEMMA2_PROOF.md`](proofs/LEMMA2_PROOF.md) — why (pattern-avoidance counting).
4. [`reports/VERIFICATION.md`](reports/VERIFICATION.md) — independent check (GPT-5.6 Sol).
5. [`proofs/PARTIAL_THEOREMS.md`](proofs/PARTIAL_THEOREMS.md) — the realizability wall, made exact.

## Honesty note

This is a structural result about the fold operator. It is **not** progress on
the Collatz conjecture, which remains open. The value is a certified negative
(no small self-similar shortcut), an exact statement of the central obstruction
(the Φ formula), and a demonstration that an analytic invariant can decide a
question that exact enumeration provably cannot reach.
