# F2b verification

## Verdicts

| Deliverable | Verdict | Exact result |
|---|---|---|
| 1. Independent re-verification | **MATCH** | 510/510 classes at `k <= 8`; zero sequence or minimal-recurrence mismatches |
| 2. Extension through `k = 10` | **MATCH** | 2,046 classes; 85 exact laws; zero cross-depth law buckets |
| 3. Avoiding-language / first-return cross-check | **CORRECTION-DERIVED** | Naive avoidance counts are not branch counts; corrected first-return counts match 196/196 terms for all 14 classes, `t=1..14` |
| 4. Reports and read-back | **MATCH** | Both required reports created under `fold/verify/`; no existing file changed |

## What ran

1. Read `fold/F2B_REPORT.md`, `fold/f2b_analytic_screen.py`, `fold/f2_fold_operator.py`, `fold/f1_word_calculus.py`, and `CLAUDE.md` section 3.
2. Ran one inline Python exact verifier. Its independent side built the avoiding automaton by direct suffix/prefix comparison, formed its integer transfer matrix `Q`, generated 100 exact terms, and recovered the scalar minimal recurrence with exact rational Berlekamp–Massey. Its comparison side separately coded the screen's KMP transitions and exact Hankel/Gaussian recurrence recovery, without importing or executing `f2b_analytic_screen.py`.
3. Ran `python3 fold/f2b_analytic_screen.py 8` as a black-box aggregate read-back.
4. Called `fold.f2_fold_operator.induced_first_return(k, r, max_s=14, node_budget=2_000_000)` for every `k=1..3`, `0 <= r < 2^k`, and grouped resolved branches by exact return time `t`.

Measured runtimes on this machine:

- independent 2,046-class law computation, including all 510 oracle comparisons: **11.6675 s**;
- 14-class first-return cross-check at cap 14: **0.1255 s**;
- existing screen reports its own runtime as approximately **0.64 s** in `fold/F2B_REPORT.md` (the fresh black-box run completed normally).

Grok contribution: none. The exact requested delegate invocation failed before task execution with `{component: codex-grok-delegate, root cause: EPERM opening the Grok plugin job log under ~/.claude/plugins/data, failure type: delegate runtime failure}`. No permission bypass or alternate invocation was used.

## Independent recurrence comparison

For each class, the positive representative was `r` when `r>0` and `2^k` when `r=0`; its word was imported from frozen `f1_word_calculus.parity_word`. No symbol was imported from `f2b_analytic_screen.py`.

For every one of the 510 classes through `k=8`:

- all first 80 independently generated avoidance counts equal the KMP-oracle counts;
- the independently recovered exact minimal recurrence equals the oracle's exact minimal recurrence;
- mismatch list: `[]`.

Aggregate black-box agreement: the existing screen prints `510 classes`, `47 distinct exact counting laws`, and `0 classes` in cross-depth law buckets. The independent computation gives the same three values.

## Extension result

The complete 85-row law table is in `fold/verify/screen_k10_results.md`. Its member counts sum to 2,046. Every law bucket has exactly one depth, so no counting law is shared across depths through `k=10`.

## Exact first-return correction

Let `w` be the length-`k` class word. Let KMP states `0,...,k-1` record the length of the longest current suffix equal to a prefix of `w`. Let `Q` be the exact integer transition matrix after deleting transitions that complete `w`. Let

- `b` be the length of the longest **proper** border of `w` (the post-match fallback state),
- `e_b` be the row vector concentrated at state `b`, and
- `h_i` be the number of bits from state `i` that complete `w`.

The naive avoidance count is

`A_w(n) = e_0 Q^n 1`.

It starts before any copy of `w` has been seen. A fold branch instead starts immediately after the already-fixed initial copy of `w` and asks for the first subsequent occurrence. The exact number of first-return branches at shift `t>=1` is therefore

`B_w(t) = e_b Q^(t-1) h`.

This is the required boundary/first-occurrence refinement. Starting at `b`, not state 0, retains self-overlaps such as `00 -> 00` and `000 -> 000`; deleting completion transitions during the first `t-1` symbols enforces that the occurrence at shift `t` is the first return. The Terras residue/parity-word bijection maps each accepted length-`t` extension to one refinement `m mod 2^t`. Empirically, every resolved engine branch in this test had `s=t`, so `B_w(t)` and the engine count are directly term-matched.

## All 14 empirical comparisons

Each vector lists terms for `t=1..14`. `A` is the naive avoidance vector; `B` is the corrected prediction; `E` is the fold-operator enumeration.

| `(k,r)` | Word | Border `b` | `A` | `B = E` |
|---|---|---:|---|---|
| (1,0) | 0 | 0 | `1,1,1,1,1,1,1,1,1,1,1,1,1,1` | `1,1,1,1,1,1,1,1,1,1,1,1,1,1` |
| (1,1) | 1 | 0 | `1,1,1,1,1,1,1,1,1,1,1,1,1,1` | `1,1,1,1,1,1,1,1,1,1,1,1,1,1` |
| (2,0) | 00 | 1 | `2,3,5,8,13,21,34,55,89,144,233,377,610,987` | `1,0,1,1,2,3,5,8,13,21,34,55,89,144` |
| (2,1) | 10 | 0 | `2,3,4,5,6,7,8,9,10,11,12,13,14,15` | `0,1,2,3,4,5,6,7,8,9,10,11,12,13` |
| (2,2) | 01 | 0 | `2,3,4,5,6,7,8,9,10,11,12,13,14,15` | `0,1,2,3,4,5,6,7,8,9,10,11,12,13` |
| (2,3) | 11 | 1 | `2,3,5,8,13,21,34,55,89,144,233,377,610,987` | `1,0,1,1,2,3,5,8,13,21,34,55,89,144` |
| (3,0) | 000 | 2 | `2,4,7,13,24,44,81,149,274,504,927,1705,3136,5768` | `1,0,0,1,1,2,4,7,13,24,44,81,149,274` |
| (3,1) | 101 | 1 | `2,4,7,12,21,37,65,114,200,351,616,1081,1897,3329` | `0,1,1,1,2,4,7,12,21,37,65,114,200,351` |
| (3,2) | 010 | 1 | `2,4,7,12,21,37,65,114,200,351,616,1081,1897,3329` | `0,1,1,1,2,4,7,12,21,37,65,114,200,351` |
| (3,3) | 110 | 0 | `2,4,7,12,20,33,54,88,143,232,376,609,986,1596` | `0,0,1,2,4,7,12,20,33,54,88,143,232,376` |
| (3,4) | 001 | 0 | `2,4,7,12,20,33,54,88,143,232,376,609,986,1596` | `0,0,1,2,4,7,12,20,33,54,88,143,232,376` |
| (3,5) | 100 | 0 | `2,4,7,12,20,33,54,88,143,232,376,609,986,1596` | `0,0,1,2,4,7,12,20,33,54,88,143,232,376` |
| (3,6) | 011 | 0 | `2,4,7,12,20,33,54,88,143,232,376,609,986,1596` | `0,0,1,2,4,7,12,20,33,54,88,143,232,376` |
| (3,7) | 111 | 2 | `2,4,7,13,24,44,81,149,274,504,927,1705,3136,5768` | `1,0,0,1,1,2,4,7,13,24,44,81,149,274` |

Exact empirical result: `B_w(t) = E_w(t)` in **196/196** positions. The naive vector differs for every `k=2` and `k=3` class; its agreement at `k=1` is degenerate.

The cap leaves unresolved mass for returns after the tested range; this does not affect any resolved term `t<=14`. All 196 compared terms are exact integers, not estimates.

## Discrepancy with existing framing

`fold/F2B_REPORT.md` says the paranoia check found no distinct laws with dominant rates equal within `1e-9`. The current `python3 fold/f2b_analytic_screen.py 8` output instead prints six rate collisions, including the Fibonacci/tribonacci-style inherited rates already described elsewhere in that report. The independent table confirms those collisions and extends the pattern (for example IDs 035/064 and 048/085).

This does **not** change the exact-law or no-cross-depth-law verdict. It does invalidate any framing that different recurrence laws always have different dominant rates. Exact recurrence comparison, not growth rate alone, is the sound discriminator used here.

## Confidence

Confidence is **high** for the bounded computational claims: two differently implemented exact automata agree on all 510 original classes, the bucket keys are exact rational tuples, and the corrected first-return formula matches every enumerated small-class term. Confidence in the general avoiding-language/first-return lemma beyond the tested range would become proof-level only after a written proof that the Terras residue/parity-word bijection identifies every first-return branch with exactly one accepted extension at arbitrary `k` and `t`.
