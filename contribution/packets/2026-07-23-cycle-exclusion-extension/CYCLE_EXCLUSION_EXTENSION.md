# Cycle exclusion extension: no nontrivial positive cycle with at most 20 odd members

**Verdict:** the exact valuation-word search of
`contribution/code/fence/exact_cycle_search.py` was extended from 18 to
**20** odd members.  Every ordered composition in the exact window was
evaluated with exact integer arithmetic, in two independently implemented
phases.  Zero divisibility hits and zero verified nontrivial cycles were
found at m = 19 and m = 20.  Counterexample watch did not fire.

\[
\boxed{\text{There is no nontrivial positive Collatz cycle with at most 20 odd members.}}
\]

This is a verified bounded exclusion over an explicitly enumerated finite
class, not a resolution of the Collatz conjecture.  Published work
(Hercher; Bařina — see *Dominance note* below) already implies a far
stronger lower bound on cycle length; this packet's value is an
atlas-verified, reproducible artifact at the enumeration frontier, not a
new mathematical frontier.

## Method

Identical to the fence packet (`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`).
For the odd-only map \(U(n)=(3n+1)/2^{v_2(3n+1)}\), a cycle of \(m\) odd
states with valuations \(a_i\), \(K=\sum a_i\), must satisfy the exact
window

\[
3^m < 2^K \le (22/7)^m,
\]

evaluated here with the integer comparisons `2^K <= 3^m` and
`2^K * 7^m <= 22^m` only.  The window derivation (no nontrivial cycle
contains 1, 3, or 5, so every state is \(\ge 7\)) is unchanged.

The exact integer-inequality window function reproduces the fence doc's
eleven surviving pairs for m ≤ 18 and yields exactly three new layers:

| odd members \(m\) | total valuation \(K\) | ordered compositions \(\binom{K-1}{m-1}\) |
|---:|---:|---:|
| 19 | 31 | 86,493,225 |
| 20 | 32 | 141,120,525 |
| 20 | 33 | 347,373,600 |

Extension total: **574,987,350** ordered valuation words.  Boundary checks
are exact: \(2^{30}\le3^{19}<2^{31}\), \(2^{31}\le3^{20}<2^{32}\), and
\(2^{33}\cdot7^{20}\le22^{20}<2^{34}\cdot7^{20}\).

Each word \(a=(a_0,\dots,a_{m-1})\) is evaluated by the affine recurrence
\(C_{j+1}=3C_j+2^{S_j}\) and accepted only if \(C_m\) is exactly divisible
by \(2^K-3^m\) with a positive odd quotient.  Every such divisibility hit is
then re-verified end-to-end (direct orbit iteration must observe exactly
the prescribed valuations and return to start; the orbit must not be
\(\{1\}\)) by the fence module's `evaluate_exponents`.

## Feasibility assessment (before running)

Cost model from the fence doc: per surviving pair, \(\binom{K-1}{m-1}\)
ordered compositions; per word, one \(m\)-step affine accumulation and one
divisibility test, all on integers below \(3^m\cdot 2^K\).  A timed sample
of the Python oracle at (18,29) measured ≈ 550,000 words/s single-core,
giving projections of ≈ 2.6 min (m = 19) and ≈ 14.8 min (m = 20)
single-core — inside the ~40 minute compute budget with margin.  A C
accelerator was therefore **not** the difference-maker and was **not**
used; all acceptance arithmetic is the Python big-int oracle, the same
code path that produced the m ≤ 18 exclusion.  The actual run was
chunk-parallelized (deterministic value-prefix partition, counts checked
against \(\binom{K-1}{m-1}\) per pair) across 12 of the machine's 14 cores.

## Cross-validation evidence

1. **Two independent enumerators, full depth.**  Phase *primary* uses the
   fence module's recursive `compositions_of` + `try_integral_fixed_point`.
   Phase *independent* uses a separately written iterative enumerator
   (reverse lexicographic order, different algorithm) with an inline
   independently coded affine/divisibility gate.  Both phases scanned all
   15 pairs completely: per-pair word counts agree with each other and
   with \(\binom{K-1}{m-1}\) exactly, and the divisibility-hit word sets
   are equal (empty at every new layer; the single trivial hit at (1,2)).
2. **Closed-form audit.**  \(C_m=\sum_j 3^{m-1-j}2^{S_j}\) was checked
   against the recurrence on every divisibility hit and on a strided
   mid-stream sample (stride 10,000,019; 27 audited words across the three
   extension pairs): zero mismatches.
3. **Regression against the fence results.**  The re-scan of the twelve
   m ≤ 18 pairs reproduces `exact_cycle_search_results.json` exactly:
   zero verified candidates at every nontrivial pair, and exactly the
   trivial \(a=(2), n=1\) control at (1,2).
4. **Enumerator sanity (pytest).**  The two enumerators generate identical
   sets in different orders on all pairs through (13,21); the prefix-chunk
   partition sums exactly to \(\binom{K-1}{m-1}\) on all 15 pairs.

## Results

| pair | words per phase | wall, primary (s) | wall, independent (s) | divisibility hits | verified nontrivial cycles |
|---|---:|---:|---:|---:|---:|
| (19,31) | 86,493,225 | 43.8 | 22.1 | 0 | 0 |
| (20,32) | 141,120,525 | 48.5 | 25.0 | 0 | 0 |
| (20,33) | 347,373,600 | 93.5 | 50.4 | 0 | 0 |

Regression pairs (12 pairs, 44,558,431 words incl. the (1,2) control):
both phases, zero hits except the trivial control, matching the fence
results.  Totals: 619,545,781 words per phase; 1,239,091,562 word-scans
across both phases; aggregate wall 403 s (≈ 6.7 min) at ≈ 3.07 M
word-scans/s on 12 workers; ≈ 37.5 single-core-minutes equivalent —
within the ~40 minute compute budget.

Wall-clock numbers are float64 measurements, labeled
`*_measured_float` in the results JSON; no acceptance decision uses them.

## Counterexample watch

Did not fire.  No divisibility hit existed at any new layer, so there was
nothing to verify beyond the trivial control.  Had any word produced a
verified nontrivial cycle, the runner would have emitted the certificate
(word, orbit, \(C_m\), denominator) and exited with status 3; the results
JSON carries `counterexample_watch.fired = false` and an empty
`verified_nontrivial_cycles` list.

## The next wall, quantified (m = 21)

The m = 21 window is the single layer \((21,34)\) with
\(\binom{33}{20}=573{,}166{,}440\) words — 1.17× the entire m ≤ 20 corpus.
At this packet's measured throughput that is ≈ 3.1 min wall (≈ 17
single-core-minutes) per phase, so m = 21 is computationally feasible with
the same machinery.  It is not mathematically worthwhile (see below) and
was left undone.

## Dominance note (why the enumeration stops being the frontier)

Hercher proved that convergence verified through \(1536\cdot2^{60}\)
implies every nontrivial cycle has more than \(1.375\cdot10^{11}\) odd
members; Bařina's computation verified convergence through \(2^{71}\).
Published work therefore dominates this exclusion by roughly eleven orders
of magnitude in the cycle-length bound.  Per the fence doc's deletion
decision, naive valuation-word enumeration cannot catch up with that bound
and cannot touch the divergent-orbit branch; this packet exists to keep
the atlas's self-verified enumeration frontier current and reproducible,
not to compete with the published lower bound.

## Limitations

- The exclusion holds only for the explicitly enumerated (m, K) pairs
  listed (all window members for m ≤ 20, plus the (1,2) control).
- No claim about cycles with more than 20 odd members, and no claim about
  the divergent-orbit branch of the conjecture.
- Not a Collatz proof, not an independence result, not a divergence
  certificate.

## Reproduction

```
cd contribution/packets/2026-07-23-cycle-exclusion-extension
python3 run_cycle_exclusion_extension.py plan
python3 run_cycle_exclusion_extension.py scan --pair 19:31 --phase both --workers 12
python3 run_cycle_exclusion_extension.py scan --pair 20:32 --phase both --workers 12
python3 run_cycle_exclusion_extension.py scan --pair 20:33 --phase both --workers 12
# regression pairs: 1:2 5:8 8:13 10:16 11:18 13:21 14:23 15:24 16:26 17:27 17:28 18:29
python3 run_cycle_exclusion_extension.py finalize
python3 -m pytest test_cycle_exclusion_extension.py -q     # 11 passed, ~3 s
```

Large pairs may be scanned in wall-clock-bounded slices via
`--chunk-start/--chunk-stop` (coverage is merged additively and rejected on
overlap).

## Files

- `run_cycle_exclusion_extension.py` — runner, independent enumerator,
  closed-form audit, chunk-parallel scan, finalize/regression logic
- `cycle_exclusion_extension_results.json` — full persisted results
  (per-pair counts, both phases, cross-validation fields, regression vs
  the fence results, counterexample watch)
- `test_cycle_exclusion_extension.py` — pytest suite (11 tests)
- `CYCLE_EXCLUSION_EXTENSION.md` — this memo

## Sources

- `contribution/code/fence/exact_cycle_search.py` and
  `contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` (method, window,
  acceptance gates, m ≤ 18 results)
- Christian Hercher, *There are no Collatz m-Cycles with m ≤ 91*,
  https://arxiv.org/abs/2201.00406
- David Bařina, *Improved verification limit for the convergence of the
  Collatz conjecture*, https://doi.org/10.1007/s11227-025-07337-0
