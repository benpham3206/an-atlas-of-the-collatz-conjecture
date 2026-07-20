# F4 Report — Symbolic-feature regression vs mod-2^B baseline

## Protocol

- Domain: `n ∈ [2, 1048576)` (N = 1048576).
- Label: `y(n) = [σ(n) > 4]` where `σ` is Terras stopping time (least `j ≥ 1` with `T^j(n) < n`).
- Split: train = `n < 524288` (524286 points), test = `n ∈ [524288, 1048576)` (524288 points).
- Base rate P(y=1): train 18.7501%, test 18.7500%.
- Feature sets enumerated: 148 (18 singles + pairs with joint space ≤ 2^12).
- Predictor: majority label per feature key on train; default 0 on unseen keys; ties → 0.
- Win rule: test accuracy ≥ matched baseline + 1.0 absolute pp, where matched baseline is the smallest B ∈ {8,10,12} with B ≥ feature budget `⌈log2(∏ space sizes)⌉`.

## Null hypothesis

By Terras (1976), the first `k` Terras steps of `n` are exactly determined by `n mod 2^k` (verified in F1). Any feature that only repackages mod-2^k information cannot beat a residue lookup at matched information budget. Expected outcome: **no win**.

## Baselines

| B | space | train acc % | test acc % |
|---|-------|-------------|------------|
| 8 | 2^8=256 | 100.0000 | 100.0000 |
| 10 | 2^10=1024 | 100.0000 | 100.0000 |
| 12 | 2^12=4096 | 100.0000 | 100.0000 |

## Leaderboard (top 20 features + baselines inline)

```
rank  name                                      bud    train%     test%   mB     base%      Δpp  win
----------------------------------------------------------------------------------------------------
   1  baseline_mod_2^10 [BASE]                   10  100.0000  100.0000   10         —        —    —
   2  baseline_mod_2^12 [BASE]                   12  100.0000  100.0000   12         —        —    —
   3  baseline_mod_2^8 [BASE]                     8  100.0000  100.0000    8         —        —    —
   4  popcount+nu2_np1                            9   94.9774   94.9739   10  100.0000  -5.0261   no
   5  nu2_np1+popcount_3n1                        9   95.0523   94.7708   10  100.0000  -5.2292   no
   6  nu2_np1+longest_zeros                       9   94.8501   94.6701   10  100.0000  -5.3299   no
   7  nu2_3n1+longest_ones                        9   94.0752   94.0228   10  100.0000  -5.9772   no
   8  nu2_np1+longest_ones                        9   94.0752   94.0210   10  100.0000  -5.9790   no
   9  popcount+nu2_3n1                            9   93.8774   93.8105   10  100.0000  -6.1895   no
  10  nu2_3n1                                     5   93.7500   93.7500    8  100.0000  -6.2500   no
  11  nu2_3n1+mod_11                              8   93.7500   93.7500    8  100.0000  -6.2500   no
  12  nu2_3n1+mod_13                              9   93.7500   93.7500   10  100.0000  -6.2500   no
  13  nu2_3n1+mod_3^1                             7   93.7500   93.7500    8  100.0000  -6.2500   no
  14  nu2_3n1+mod_3^2                             8   93.7500   93.7500    8  100.0000  -6.2500   no
  15  nu2_3n1+mod_3^3                            10   93.7500   93.7500   10  100.0000  -6.2500   no
  16  nu2_3n1+mod_3^4                            11   93.7500   93.7500   12  100.0000  -6.2500   no
  17  nu2_3n1+mod_5                               7   93.7500   93.7500    8  100.0000  -6.2500   no
  18  nu2_3n1+mod_7                               8   93.7500   93.7500    8  100.0000  -6.2500   no
  19  nu2_3n1+popcount_mod2                       6   93.7500   93.7500    8  100.0000  -6.2500   no
  20  nu2_3n1+popcount_3n1                       10   93.7500   93.7498   10  100.0000  -6.2502   no
  21  nu2_np1                                     5   93.7500   93.7498    8  100.0000  -6.2502   no
  22  nu2_np1+nu2_3n1                             9   93.7500   93.7498   10  100.0000  -6.2502   no
  23  nu2_3n1+longest_zeros                       9   93.7504   93.7496   10  100.0000  -6.2504   no
```

## Verdict

**NO WIN vs mod-2^B baseline**

### Observation (why the baseline is perfect)

On this domain, the long-glide label `y = [σ > 4]` is **constant on each residue class mod 2^8** (hence also mod 2^10 and 2^12): baseline test accuracy is exactly 100% at every budget B ∈ {8,10,12}. The empirical base rate is 18.75% = 3/16 on the test split, consistent with a pure function of `n mod 16` (or a slightly larger 2-power). No non-2-adic feature in the grammar can exceed a perfect 2-adic lookup; the strongest feature set (`popcount+nu2_np1`) reaches only 94.97% test accuracy (−5.03 pp vs B=10).

This is the doctrine outcome: the difficulty is 2-adic; the grammar found no anomaly.

## Excursion records (sustained odd-step density)

For each `n < N`, walk the Terras orbit to 1 and track running odd-step density `a/L` (a = # of odd Terras steps in the first L steps) for all prefixes `L ≥ 20`. Per-n record = max density; table = top-10 n by that record.

A divergent orbit would need density `≥ log 2 / log 3 ≈ 0.630930` forever.

**Max L at which any n < 1048576 still has a/L ≥ log2/log3:** 217

| rank | n | L | a | a/L |
|------|---|---|---|-----|
| 1 | 1048575 | 20 | 20 | 1.000000 |
| 2 | 419839 | 24 | 23 | 0.958333 |
| 3 | 629759 | 23 | 22 | 0.956522 |
| 4 | 901119 | 22 | 21 | 0.954545 |
| 5 | 944639 | 22 | 21 | 0.954545 |
| 6 | 77671 | 21 | 20 | 0.952381 |
| 7 | 524287 | 21 | 20 | 0.952381 |
| 8 | 566719 | 21 | 20 | 0.952381 |
| 9 | 655359 | 21 | 20 | 0.952381 |
| 10 | 699049 | 21 | 20 | 0.952381 |

## Files

- `fold/f4_feature_regression.py` — experiment
- `fold/test_f4.py` — verification
- `fold/F4_REPORT.md` — this report

## Runtime note

Full domain N=2^20=1048576; protocol as specified.
