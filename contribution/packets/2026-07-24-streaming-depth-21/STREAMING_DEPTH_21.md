# Streaming depth 21: the memory ceiling removed, and a correction to the drift-test verdict

**Date:** 24 July 2026
**Status:** one engineering result (certified), one new layer (n = 21), and
two corrections to the predecessor packet's *reading* of its own data.
**Not** a proof of Collatz, **not** a counterexample, **not** a stronger
density statement than Tao's. No kill criterion fired.

---

## 1. The wall, and why it was the wrong kind of wall

The plateau-drift-test memo records n = 20 as "the honest ceiling of this
engine on this machine", because layer n costs \(3^{n-1}\) complex128 and
the transport step needs two layers live:

| n | one layer | transport (old + new) |
|---:|---:|---:|
| 20 | 17.3 GiB | 23.1 GiB |
| 21 | 52.0 GiB | **69.3 GiB** |

On a 36 GB machine n = 21 does not fit. But the wall is **memory, not
arithmetic**: the n = 21 transport is only ~3x the n = 20 work.

Nothing downstream ever needs the layer as an array. Per layer the drift
test consumes exactly four things, and three of them are reductions:

1. \(M_n\) and the peak unit — a max-reduction;
2. the bad sets \(\{|c|>(1-\varepsilon)M_n\}\) — a threshold-reduction with
   tiny output;
3. the near-peak profile \(p_j\) — **9 named units**;
4. the escape weights \(w_n(\varepsilon)\) — integer arithmetic on the bad
   set only, **no state values at all**.

So layer n can be certified with layer n−1 resident and layer n never
allocated. Peak drops from \(3^{n-1}+3^{n-2}\) to \(3^{n-2}\) plus one
chunk: **17.3 GiB instead of 69.3 GiB at n = 21, a 4x reduction.**

## 2. Bit-identity, not approximation

`transport_range()` computes output element j from j alone — the \(\nu_a\)
carry is re-seeded by exact integer arithmetic at each thread start, and the
float accumulation runs over \(a=1..\text{taps}\) in fixed order. So
chunking cannot perturb one output bit. This is **asserted, not assumed**
(`test_streaming_depth_21.py`, 5 tests):

- chunked vs full-width transport, chunk sizes 1 / 7 / 1024 / full, at
  n = 6, 9, 12, 13 — `np.array_equal` on the full complex arrays;
- thread counts 1 / 2 / 5 / 8 — identical output;
- streamed \(M_n\), argmax and every bad set vs the resident scan;
- point evaluation vs `c_at` on 46 units per layer including both halves
  and the conjugate-fold boundary;
- bad-set residues and exact escape weights unchanged.

End-to-end, the streaming engine reproduces the certificate **exactly**
(`M_n`, `k`, argmax, all `bad_count`, all `w`, all `L`, and every profile
\(p_j\) to zero absolute difference) at n = 18 and at n = 20.

## 3. The new layer

```
layer 21:  M_n = 0.0078721330   k = 28   p_2 = 0.887281
           w(0.05) = 0.250000   L(0.2) = 4
```

Wall clock 649 s total (116 s to build layers 1..20, 532 s to stream
layer 21 in two passes), peak 17.3 GiB.

**Counterexample watch: nothing fired.** The peak stayed on the
\(\pm2^k\) chain; every bad-set member has an exact base-2 discrete log;
the bad chain indices still form a contiguous interval; the tightness
identity \(w=2^{-L}-2^{-40}\) still holds exactly; no wrap.

## 4. Correction 1 — p₂ is driven by Δk, not by parity

The predecessor packet recorded a "new parity alternation" (p₂ high at even
n, low at odd n) and extrapolated p₂ linearly in n to predict a 0.95
crossing near n ≈ 22, then recorded that prediction as *falsified on
schedule*.

Parity is not the driver. Let \(\Delta k(n)=k(n)-k(n-1)\in\{1,2\}\). Then

> \(\Delta k(n)\ge 2 \iff p_2(n)>p_2(n-1)\)

holds at **every transition n = 7..21, 15/15, no exceptions** (smallest
\(|\Delta p_2|\) in the record is 0.0193, so this is not a float64 artifact).
\(k(n)\) is an exact integer from BSGS, so \(\Delta k\) is exact.

Parity worked only as a proxy: in the window n ≤ 19 the \(\Delta k=2\)
layers happened to alternate parity. The \(\Delta k=2\) layers are
\(\{7,10,13,16,18,20,21\}\) — **both parities present**. At n = 20 and
n = 21 two consecutive \(\Delta k=2\) steps occur, the first such pair on
record, and the parity model fails at once:

| model | predicts p₂(21) | observed | residual |
|---|---:|---:|---:|
| packet's odd-branch fit | 0.7422 | **0.8873** | **+0.1451** |
| Δk = 2 subsequence fit | 0.8516 | **0.8873** | +0.0356 |

**p₂(21) = 0.887281 is an all-time high** (previous max 0.8379 at n = 13).

Consequence: a linear-in-n fit through a sawtooth is misspecified, so the
n ≈ 22 crossing was never a well-posed extrapolation and its failure was
not evidence about the trend. Refitting on the \(\Delta k=2\) subsequence —
the only population on which p₂ rises — puts the 0.95 crossing at
**n ≈ 32**, and n = 21 sits *above* that line. (The packet's own
even-branch refit gave 33.3; it was accidentally tracking the \(\Delta k=2\)
subsequence, four of whose seven members are even.)

The \(w_n(0.05)\) parity alternation is a **separate** phenomenon: \(\Delta k\)
does not explain \(L(n,0.05)\) (7/15 agreement). That observation stands.

## 5. Correction 2 — the decay law points at the Tao-strength branch

P6 is, on the \(M_n\) side, exactly the question *is \(-\ln M_n\) linear in
n, or in \(\sqrt n\)?* — branch (i) bounded L gives exponential decay
(stronger than Tao), branch (ii) creeping L gives \(e^{-c\sqrt n}\)
(Tao-strength).

The predecessor packets measure \(c_n=-\ln M_n/\sqrt n\) and fit it through
the origin — that is, they fit branch (ii) and report its residuals. **They
never fit branch (i) and compare.** Doing so (two-parameter least squares
each, so SSR is directly comparable):

| window | SSR exponential | SSR sqrt | ratio | ΔAIC |
|---|---:|---:|---:|---:|
| n = 6..21 | 1.642e-01 | 2.519e-02 | 6.5x | **+30.0** |
| n = 13..21 | 3.237e-03 | 7.673e-04 | 4.2x | **+13.0** |

Both windows favour **branch (ii)**, and adding n = 21 *strengthened* it.
Over n ≥ 13, \(-\ln M_n/\sqrt n\) is flat (spread 0.0070) while
\(-\ln M_n/n\) falls monotonically at every step (spread 0.0627): the
exponential constant has not begun to stabilise.

So STATE.md's summary — that the stall was "mild evidence toward the
stronger alternative (L bounded ⇒ uniform exponential decay)" — is not
supported once the comparison is actually run. It is defensible only
against a *linear*-creep strawman; against the \(\sqrt n\) law the evidence
runs the other way.

**Honest scope.** This is a finite window of float64 measurements. Branch
(i) requires L bounded at every n, and an asymptotic regime change beyond
n = 21 is not excluded by any amount of data below it. The window cannot
prove either branch — it can only say which way the evidence currently
points, and report when that disagrees with the repository's own summary.

## 6. Reproduce

```bash
python3 -m pytest contribution/packets/2026-07-24-streaming-depth-21/ -q
python3 contribution/packets/2026-07-24-streaming-depth-21/run_streaming_depth.py 18   # validates vs cert
python3 contribution/packets/2026-07-24-streaming-depth-21/decay_model_test.py
python3 contribution/packets/2026-07-24-streaming-depth-21/profile_structure_test.py
```

`run_streaming_depth.py 21` needs ~18 GiB and ~11 min. Requires `clang`
and `numpy`; the tests require `pytest`.

## 7. What this does not do

- It does not prove or disprove Collatz, and does not beat Tao.
- It does not resolve P6. It corrects the direction of the evidence and
  removes a misspecified extrapolation.
- The next honest probe is **n = 22–24**, to test whether p₂ continues to
  track the \(\Delta k=2\) line toward n ≈ 32. n = 22 needs layer 21
  resident (52.0 GiB) and does **not** fit this machine even streamed;
  crossing it needs either an out-of-core layer-21 store or a second level
  of streaming, and the latter costs 1600 random gathers per output.
