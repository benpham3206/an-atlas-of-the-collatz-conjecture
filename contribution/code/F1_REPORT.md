# F1 Report — Collatz word-fold calculus

Packet F1 calibration: exact-arithmetic compositions of the Terras map.

## Definitions

- **Terras map:** `T(n)=n/2` if even; `T(n)=(3n+1)/2` if odd.
- **Parity word** of length `k`: `w_i = parity(T^i(n))` (1=odd, 0=even).
- **Composite affine form:** word `w` of length `L` with `a` ones gives
  `n ↦ (3^a · n + c_w) / 2^L`, with
  `c_w = Σ_j 3^{a-j-1} · 2^{i_j}` over odd-step indices `i_j` (0-based),
  equivalently the inductive rule `c ← 3c + 2^i` on each odd step at index `i`.

## Exact statements verified

1. **Composite calculus.** For a random sample of ≥10 000 pairs `(n,L)` with
   `1 ≤ n < 10^6` and `1 ≤ L ≤ 30`, if `w` is the length-`L` parity word of `n`,
   then `(3^a n + c_w) / 2^L = T^L(n)` (exact integer equality).
2. **Terras bijection.** For each `k ≤ 20`, the map
   `φ_k : ℤ/2^kℤ → {0,1}^k` sending residue `[n]` to the length-`k` parity word
   of a positive lift of `[n]` is a **bijection** (all `2^k` words hit exactly once).
3. **Cycle candidates.** A cycle realizing word `w` requires
   `n = c_w / (2^L − 3^a)` to be a positive integer whose parity word is `w`.
   Exhaustive enumeration over necklace-canonical words with `L ≤ 24` and
   `2^L > 3^a` finds only the trivial 2-cycle through `{1,2}`.
4. **Stopping-time spectrum.** For all `n` in the reported range, stopping time
   (least `k≥1` with `T^k(n)<n`) and total stopping time (least `k` with `T^k(n)=1`)
   are computed; distribution summary below.
5. **Extremal words.** For each `k ≤ 30`, `n = 2^k − 1` has parity word
   `(1,…,1)` of length `k`, and `T^k(2^k−1) = 3^k − 1`.

## Per-section results and wall-clock runtimes

| Section | Status | Runtime (s) | Detail |
|---------|--------|-------------|--------|
| D1 composite calculus | PASS | 0.078 | samples=10000 property_t=0.075s |
| D2 Terras bijection | PASS | 4.677 | For each k≤20, φ_k : Z/2^k Z → {0,1}^k, φ_k([n]) = length-k parity word of a positive lift of [n], is bijective. |
| D3 cycle-candidate sweep | PASS | 54.139 | max_L=24 examined=1321649 pruned_growth=3254690 skipped_necklace=28978091 integral=12 verified=12 ns=[2] |
| D4 stopping-time spectrum | PASS | 1.007 | limit=1048576 stop_max=183@n=1027431 p50=1 p99=32 total_max=329@n=837799 tp50=85 tp99=181 |
| D5 extremal-word atlas | PASS | 0.000 | k=1..30 all verified; e.g. T^5(31)=242 |

## Cycle-candidate certificate detail

- max_L: 24
- words examined (after growth prune + necklace filter): 1321649
- words pruned by `2^L ≤ 3^a`: 3254690
- words skipped as non-canonical necklace: 28978091
- integral positive `n = c_w/(2^L−3^a)` candidates: 12
- verified cycles (parity word matches): 12

Verified cycle points:

- n=2, L=2, a=1, word=(0, 1), c_w=2, denom=1
- n=2, L=4, a=2, word=(0, 1, 0, 1), c_w=14, denom=7
- n=2, L=6, a=3, word=(0, 1, 0, 1, 0, 1), c_w=74, denom=37
- n=2, L=8, a=4, word=(0, 1, 0, 1, 0, 1, 0, 1), c_w=350, denom=175
- n=2, L=10, a=5, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=1562, denom=781
- n=2, L=12, a=6, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=6734, denom=3367
- n=2, L=14, a=7, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=28394, denom=14197
- n=2, L=16, a=8, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=117950, denom=58975
- n=2, L=18, a=9, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=484922, denom=242461
- n=2, L=20, a=10, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=1979054, denom=989527
- n=2, L=22, a=11, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=8034314, denom=4017157
- n=2, L=24, a=12, word=(0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), c_w=32491550, denom=16245775

- only_trivial (orbit in {1,2}): **True**

## Stopping-time spectrum summary

- limit N = 1048576 (n in ranges [2, 1048576) stopping; [1, 1048576) total)

### Stopping time (first drop below n)

- count: 1048574
- min / max / argmax: 1 / 183 / n=1027431
- mean: 3.484463
- percentiles (50, 90, 99, 99.9): 1, 8, 32, 70
- section runtime: 0.390s

### Total stopping time (to 1)

- count: 1048575
- min / max / argmax: 0 / 329 / n=837799
- mean: 88.134213
- percentiles (50, 90, 99, 99.9): 85, 134, 181, 221
- section runtime: 0.517s

## Extremal-word atlas

- max_k: 30
- all_ok: **True**
- sample: k=10, n=2^10−1=1023, T^10(1023)=3^10−1=59048

## Anomalies

An anomaly is a noteworthy result, not a test failure.

- Cycle sweep found 12 verified fixed points of words (not just n=1 and n=2). All lie on the trivial orbit {1,2} or are necklace-filtered representations; listed above. Periodic repetitions of the 2-cycle word (e.g. (1,0) repeated) yield the same n=1.
- Among n < 1048576, max stopping time is 183 at n=1027431; max total stopping time is 329 at n=837799.

## Environment

- Python: 3.14.3
- Arithmetic: Python arbitrary-precision ints only in certificates
- Dependencies: stdlib only

## Files

- `fold/f1_word_calculus.py` — library
- `fold/test_f1.py` — tests + report emitter
- `fold/F1_REPORT.md` — this report
