# F4 Report — Symbolic-feature regression vs mod-2^B baseline

## Protocol

- Domain: `n ∈ [2, 1048576)` (N = 1048576).
- Label: `y(n) = [σ(n) > 33]` where `σ` is Terras stopping time (least `j ≥ 1` with `T^j(n) < n`).
- Split: train = `n < 524288` (524286 points), test = `n ∈ [524288, 1048576)` (524288 points).
- Base rate P(y=1): train 0.9626%, test 0.9480%.
- Feature sets enumerated: 148 (18 singles + pairs with joint space ≤ 2^12).
- Predictor: majority label per feature key on train; default 0 on unseen keys; ties → 0.
- Win rule: test accuracy ≥ matched baseline + 1.0 absolute pp, where matched baseline is the smallest B ∈ {8,10,12} with B ≥ feature budget `⌈log2(∏ space sizes)⌉`.

## Null hypothesis

By Terras (1976), the first `k` Terras steps of `n` are exactly determined by `n mod 2^k` (verified in F1). Any feature that only repackages mod-2^k information cannot beat a residue lookup at matched information budget. Expected outcome: **no win**.

## Baselines

| B | space | train acc % | test acc % |
|---|-------|-------------|------------|
| 8 | 2^8=256 | 99.0374 | 99.0520 |
| 10 | 2^10=1024 | 99.0515 | 99.0551 |
| 12 | 2^12=4096 | 99.0721 | 99.0772 |

## Leaderboard (top 20 features + baselines inline)

```
rank  name                                      bud    train%     test%   mB     base%      Δpp  win
----------------------------------------------------------------------------------------------------
   1  baseline_mod_2^12 [BASE]                   12   99.0721   99.0772   12         —        —    —
   2  nu2_np1                                     5   99.0534   99.0644    8   99.0520  +0.0124   no
   3  nu2_np1+longest_ones                        9   99.0534   99.0644   10   99.0551  +0.0093   no
   4  nu2_np1+nu2_3n1                             9   99.0534   99.0644   10   99.0551  +0.0093   no
   5  nu2_np1+longest_zeros                       9   99.0599   99.0627   10   99.0551  +0.0076   no
   6  nu2_np1+mod_3^1                             6   99.0540   99.0625    8   99.0520  +0.0105   no
   7  nu2_np1+popcount_mod2                       6   99.0538   99.0616    8   99.0520  +0.0095   no
   8  nu2_np1+popcount_3n1                        9   99.0599   99.0595   10   99.0551  +0.0044   no
   9  nu2_np1+mod_11                              8   99.0566   99.0591    8   99.0520  +0.0071   no
  10  popcount+nu2_np1                            9   99.0574   99.0591   10   99.0551  +0.0040   no
  11  nu2_np1+mod_7                               8   99.0549   99.0589    8   99.0520  +0.0069   no
  12  nu2_np1+mod_3^2                             8   99.0553   99.0585    8   99.0520  +0.0065   no
  13  nu2_np1+mod_13                              9   99.0589   99.0580   10   99.0551  +0.0029   no
  14  baseline_mod_2^10 [BASE]                   10   99.0515   99.0551   10         —        —    —
  15  nu2_np1+mod_5                               7   99.0555   99.0543    8   99.0520  +0.0023   no
  16  nu2_3n1+longest_ones                        9   99.0396   99.0534   10   99.0551  -0.0017   no
  17  longest_zeros                               5   99.0381   99.0522    8   99.0520  +0.0002   no
  18  longest_zeros+mod_3^1                       6   99.0381   99.0522    8   99.0520  +0.0002   no
  19  longest_zeros+mod_7                         8   99.0381   99.0522    8   99.0520  +0.0002   no
  20  longest_zeros+popcount_mod2                 6   99.0381   99.0522    8   99.0520  +0.0002   no
  21  nu2_3n1+longest_zeros                       9   99.0381   99.0522   10   99.0551  -0.0029   no
  22  popcount                                    5   99.0375   99.0522    8   99.0520  +0.0002   no
  23  baseline_mod_2^8 [BASE]                     8   99.0374   99.0520    8         —        —    —
```

## Verdict

**NO WIN vs mod-2^B baseline**

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
