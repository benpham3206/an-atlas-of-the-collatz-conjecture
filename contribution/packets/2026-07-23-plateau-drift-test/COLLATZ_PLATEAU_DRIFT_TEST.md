# Plateau drift test: the near-peak profile to depth n = 20, exact escape-weight sweeps at all depths, and the failure of the n ≈ 22 crossing on the current trend

**Date:** 23 July 2026
**Status:** measurement packet. **No new theorems.** The proved statements
of the predecessor packets (syracuse-fourier Lemma 2; scalar-phase
Theorems S1/S3; plateau-escape-weight P1–P6) are re-verified here at
greater depth and **asserted** by the verifier; everything else is a
float64 hypothesis-generator and is labelled as such. **Not** a proof of
Collatz, **not** a counterexample, **not** a proof of the conjectured
\(\exp(-c\sqrt n)\) decay, and the \(n\le20\) window determines nothing
about asymptotics (see §8). No literature-priority claim.

**Companion executable evidence:** `verify_plateau_drift_test.py`,
`plateau_drift_kernel.c`, `test_verify_plateau_drift_test.py`,
`verify_plateau_drift_test.out`, `plateau_drift_certificate.json`.

---

## 1. The prediction under test (stated up front)

The plateau-escape-weight packet (P6, memo §"Measured tightness" and
closing discussion) measured an upward drift of the near-peak profile —
\(p_1,p_2,p_3\) slopes \(+0.011,+0.024,+0.019\) per layer over
\(n=8..14\) — and noted that *linear* extrapolation puts \(p_2>0.95\)
(the first quantization-visible signature of L-creep at \(\varepsilon=0.05\),
i.e. \(w_n(0.05)\) dropping below \(1/4\)) near \(n\approx22\): "a
falsifiable float64 prediction, not a theorem." This packet exists to
fire or confirm that prediction.

**Result: the prediction FAILS on schedule.** Recomputing the fit from
the reproduced \(n=8..14\) table (same definitions, regression-checked to
\(10^{-9}\)) gives slope \(+0.02375\), crossing \(n\approx20.4\). Measured:
\(p_2(18)=0.8003\), \(p_2(19)=0.7213\), \(p_2(20)=0.8013\) — at the
predicted crossing layer, \(p_2\) reads \(0.80\), residual \(-0.140\)
against the extrapolation. The drift *continues* but at roughly one
third of the old rate and with a dominant parity oscillation; refit
crossings move to \(n\approx42\) (full window), \(n\approx33\) (even
branch), \(n\approx79\) (odd branch). Correspondingly \(w_n(0.05)\)
never drops below \(1/4-2^{-40}\) through \(n=20\). See §5.

Kill criteria for this packet (all **NOT FIRED**, §7):

1. An off-chain unit frequency beating the on-chain peak at any layer
   (falsifies the resonance-chain structure).
2. Escape weight \(w_n\) dropping *faster* than the creep law, or the
   tight identity \(w_n=2^{-L}-2^{-40}\) breaking (evidence of stronger
   decay).
3. \(p_j\) plateauing or reversing outright (favors the
   \(L\)-bounded \(\Rightarrow\) exponential branch). *Partially
   observed — a stall, not a reversal; this is the packet's main
   measurement, not an anomaly.*
4. Any S1/S3/Lemma 2 control failure at any checked layer.

## 2. Why the old engine died at n = 18 (diagnosis) and the new engine

The deep-fourier-scan engine certified \(n=17\) in 80 s and was killed
past 300 s constructing layer 18. Post-mortem, three compounding costs:

- **Dense layer construction.** \(P_n\) is a float64 array of length
  \(3^n\) built by 40 full-array uint64 multiply-mod passes; each pass
  materialises several \(3^n\)-sized temporaries (`X`, `t`, masks,
  gathers) — \(\sim\)15 GB of live temporaries at \(n=18\) with heavy
  allocator churn, \(\sim\)40 sequential passes over 3.1 GB each.
- **A full FFT nobody needed.** The Fourier transform of length
  \(3^{18}=387{,}420{,}489\) (radix-3, non-power-of-two, large constant)
  allocates a 6.2 GB complex128 output plus internal twiddle/work
  buffers — yet only the \(2\cdot3^{17}\) **unit** frequencies are ever
  read.
- **Per-layer auxiliary arrays** of length \(2\cdot3^{n-1}\) for the
  escape-weight sweeps.

**The replacement engine eliminates all three.** The character
\(\widehat c_n\) itself is propagated — no dense \(P_n\), no FFT — by the
*proved* recursion identity of the syracuse-fourier packet,
\(\widehat c_n(\xi)=\sum_{a\le40}2^{-a}e(-\xi u_a/3^n)\,
\widehat c_{n-1}(\xi u_a\bmod 3^{n-1})\), carried on **half-unit-indexed
complex128 state**: units \(0<\xi<3^n/2\), index
\(j\leftrightarrow 3(j/2)+1+(j\bmod2)\), count \(3^{n-1}\), the other
half filled by conjugate symmetry (reality of \(P_n\)). The inner loop
is a C kernel (`plateau_drift_kernel.c`, clang -O3, IEEE arithmetic, no
fast-math, pthreads over disjoint output ranges, deterministic) with two
structural tricks: \(\nu_a=\xi u_a\bmod 3^n\) is carried *incrementally*
across consecutive outputs (one add + conditional subtract per tap — no
64-bit division in the hot loop), and the circle factor
\(e^{-2\pi i\nu/3^n}\) is evaluated as a product of two exact
root-of-unity tables (\(3^{\lfloor n/2\rfloor}\times
3^{\lceil n/2\rceil}\) split, cache-resident). Justification of the speed
path over the alternatives: numpy vectorisation of the same transport is
latency-bound on 40 random gathers per output (\(\sim\)45 min projected
at \(n=19\)); a pruned FFT still needs the dense \(P_n\); the walk
structure offers no log-coordinates shortcut because the phase factor is
not a function of the discrete log — that non-smoothness *is* the
intrinsic-phase problem this program studies.

Two further upgrades fall out of the structure:

- **Exact escape weights at every depth** (replacing the plateau
  packet's sampled sweeps at \(n\ge12\)): a next-layer unit \(\eta\) has
  a bad image under tap \(a\) iff \(\eta\equiv b\,2^{a}\pmod{3^n}\) for a
  bad \(b\), so the global minimum of \(w\) is attained on the explicit
  candidate set \(\{b2^a+t3^n: a\le40, b\in B_n(\varepsilon), t=0,1,2\}\)
  (\(\le 960\) units); every other unit has \(w=1-2^{-40}\) exactly. The
  \(w_n\) values below are full-sweep-exact at *all* layers, and the
  tightness identity \(w_n=2^{-L}-2^{-40}\) is now certified, not
  sampled, through \(n=20\).
- **Memory.** Two state buffers at \(n=20\): \(3^{19}\) complex128
  \(=18.6\) GB each, \(\sim\)25 GB peak — fits the 36 GB Mac. \(n=21\)
  needs 56 GB per buffer (and 128-bit index arithmetic): it does **not**
  fit. \(n=20\) is the honest ceiling of this engine on this machine;
  per the arithmetic discipline, nothing was downgraded to float32 /
  complex64 to get here.

**Correctness gate (all asserted in the verifier).** Against dense-FFT
ground truth (independent implementation): max magnitude difference
\(9.7\times10^{-17}\) over *all* unit frequencies, every layer
\(n\le15\). Against the predecessor certificates (93 regression checks,
all passed): \(M_n\) for \(n=14..17\) matches
\(0.0191280,0.0162845,0.0144095,0.0125107\) to full certificate
precision (\(\ge7\) digits, actually \(\le10^{-9}\) relative); the chain
exponents \(k(n)\) for \(n=6..17\) match exactly
\((6,8,9,10,12,13,14,16,17,18,20,21)\); bad-set counts match at every
layer/\(\varepsilon\); the plateau \(p_j\) table (\(n=8..14\)) matches to
\(<10^{-9}\); escape weights \(w_n(\varepsilon)\) and interval lengths
\(L(n,\varepsilon)\) (\(n=6..13\)) match to \(<10^{-12}\); the
recomputed \(n=8..14\) profile slopes reproduce the plateau memo's
published \(+0.0114/+0.0238/+0.0186\) to \(10^{-12}\).

## 3. What was extended (all float64 measurements unless labelled exact)

Certified depth is now **\(n=20\)** (\(3^{20}=3{,}486{,}784{,}401\)
residues; \(2\cdot3^{19}\) unit frequencies). Default verifier runtime
**165 s** wall clock (36 GB Mac; transport 79 s for the \(n=20\) layer,
\(23\) s for \(n=19\), everything else \(\le8\) s per layer; dense
cross-check, regression, exact BSGS, and all measurements included).

| \(n\) | \(M_n\) | \(c_n=-\ln M_n/\sqrt n\) | \(k(n)\) | \(k-n\) | \(p_2\) | \(w_n(0.05)\) | \(L(0.2)\) |
|---|---|---|---|---|---|---|---|
| 17 | 0.0125106867 | 1.0626 | 21 | 4 | 0.709019 | 1/4 | 4 |
| 18 | 0.0111872664 | 1.0590 | 23 | 5 | 0.800299 | 1/2 | 4 |
| 19 | 0.0098157099 | 1.0608 | 24 | 5 | 0.721270 | 1/4 | 4 |
| 20 | 0.0088845928 | 1.0562 | 26 | 6 | 0.801281 | 1/2 | 4 |

- **The decay law survives.** \(c_n\in[1.056,1.063]\) for \(n=13..20\);
  through-origin fit over \(n=6..20\): \(c=1.0450\) (reference \(1.06\)).
  The \(e^{-c\sqrt n}\) picture is intact at depth 20.
- **The chain law survives in structure.** \(k(n)=23,24,26\) at
  \(n=18,19,20\): exact BSGS, peak \(=\pm2^{k}\) with \(2^k<3^n\)
  certified in integer arithmetic; consistent with the deep-fourier
  restatement \(k(n)\approx1.343n-1.774\) (predicts \(22.4,23.7,25.1\)).
  \(\Delta K\in\{1,2\}\); no sign flips; bad-set counts stay
  \(\le4/\le6/\le8\) at \(\varepsilon=0.05/0.1/0.2\).
- **Every near-peak frequency is on the chain, certified.** For
  \(j=0..8\), the profile point \(\xi^*2^{-j}\) equals
  \(\pm2^{k(n)-j}\) by an exact integer check *and* an independent BSGS
  discrete log, at every layer.
- **Exact chain phases at depth (P1 machinery).** Dominant-pair scalar
  misalignment certified as exact Fractions: \(2^{21}/3^{18}\) at
  \(n=18\), \(2^{22}/3^{19}\) at \(n=19\), \(2^{24}/3^{20}\) at \(n=20\)
  (\(0.00541,0.00361,0.00481\)) — the no-wrap hypothesis \(2^k<3^n\)
  holds with margin at every new layer.
- **Reduction machinery exact at depth.** S1 max error
  \(2.2\times10^{-19}\) (\(n=9\)), \(6.8\times10^{-21}\) (\(n=12\)); S3
  holds at every resolved layer with *exact* escape weights; Lemma 2
  holds at every layer \(n\le15\) (dense control).
- **Phase bite at the peak.** \(\rho/\)triangle-bound for the
  transitions \(14{\to}15\dots19{\to}20\): \(0.970,0.960,0.975,0.968,
  0.980,0.974\) — a weaker intrinsic-phase contraction than the
  \(0.90\)–\(0.95\) measured in the \(n\le13\) window (measured, not
  asserted).

## 4. The parity alternation (new structural observation)

Every near-peak quantity in the new window alternates with the parity of
\(n\), exactly or near-exactly:

- \(w_n(0.05)\) alternates **exactly** \(1/2,1/4\) for \(n=13..20\)
  (even/odd), i.e. \(L(n,0.05)=1+(n\bmod2)\) in that window; \(w_n(0.1)\)
  alternates \(1/4,1/8\); \(L(n,0.1)=3\) (even) vs \(2\) (odd).
- \(p_2\) splits into two branches: even \(n\)
  \(0.787,0.800,0.801\) (\(n=16,18,20\)); odd \(n\)
  \(0.684,0.709,0.721\) (\(n=15,17,19\)) — the even branch's last
  two-layer increment is \(+0.0010\), i.e. **visibly saturating**.
- The bad chain blocks are parity-locked in the new window
  (\(n=14..20\)): at even \(n\), \(B(0.05)=\{\pm2^{k}\}\) (indices
  \(\{0,0\}\)); at odd \(n\), \(B(0.05)=\{\pm2^{k},\pm2^{k+1}\}\)
  (indices \(\{-1,-1,0,0\}\)).

The \(n\le14\) linear fits were fit across this oscillation; part of the
old \(+0.024\)/layer "drift" was oscillation phase, not trend.

## 5. The p₂-extrapolation verdict

| \(n\) | \(p_2\) measured | extrapolated (\(n\le14\) fit) | residual |
|---|---|---|---|
| 15 | 0.683773 | 0.822815 | −0.139 |
| 16 | 0.786936 | 0.846568 | −0.060 |
| 17 | 0.709019 | 0.870322 | −0.161 |
| 18 | 0.800299 | 0.894075 | −0.094 |
| 19 | 0.721270 | 0.917828 | −0.197 |
| 20 | 0.801281 | 0.941581 | −0.140 |

- **Old fit, recomputed** (window \(n=8..14\), reproduced table):
  slope \(+0.023753\)/layer, intercept \(0.46652\), crossing
  \(p_2=0.95\) at \(n\approx20.35\) — sharper than the memo's rough
  "\(\approx22\)", and it lands *inside* the newly measured window:
  the prediction is tested directly, not by further extrapolation.
- **Verdict: NOT CONFIRMED — the crossing does not occur on the
  predicted schedule.** \(p_2(20)=0.8013\) where the law requires
  \(\approx0.94\). All six new residuals are negative; the trend deficit
  is \(\sim0.14\) and grows on the odd branch.
- **What replaces it:** new-layers-only slope (\(n=15..20\))
  \(+0.0138\)/layer; full-window (\(n=8..20\)) slope \(+0.0076\)/layer
  (crossing \(n\approx41.9\)); parity-branch slopes \(+0.0101\) (even,
  crossing \(n\approx33.3\)) and \(+0.0036\) (odd, crossing
  \(n\approx79.0\)). Honest statement: the drift *toward* flatness
  continues but weakened by a factor of \(\sim3\), the oscillation
  dominates the trend, and the crossing time is now fit-dominated — the
  data no longer constrain it within the window.
- **Dichotomy reading (P6):** the window remains in resolution (ii) in
  direction (upward drift, L-creep at \(\varepsilon=0.2\)), but the
  stall is *mild* evidence toward the stronger alternative
  (\(L\) bounded \(\Rightarrow\) uniform exponential decay) relative to
  the linear-creep picture. The drift has **not** reversed, so
  resolution (i) is not confirmed either.

## 6. L-creep and \(w_n(0.05)\) vs the \(1/4\) threshold

- \(L(n,0.2)\): \(2,2,3,3,3,3,3,4\) (\(n=6..13\)), then
  \(3,4,3,4,4,4,4\) (\(n=14..20\)) — the creep that was \(2\to4\) over
  \(n=6..13\) has *slowed*: \(L=4\) stable for four consecutive layers
  (\(n=17..20\)), versus \(\tfrac12\log_2n\approx2.2\) at \(n=20\)
  (creep remains *ahead* of the \(\tfrac12\log_2n\) reference at
  \(\varepsilon=0.2\), but \(L\) is dyadic-quantized and the window is
  short).
- \(w_n(0.05)\): never below \(1/4-2^{-40}\) through \(n=20\); the
  exact alternation \(1/2\leftrightarrow1/4\) (\(\S4\)) holds for
  \(n=13..20\). The \(c/\sqrt n\) law for \(w_n(0.05)\) remains
  quantization-invisible in the window, exactly as the plateau memo
  predicted it would be until \(p_2>0.95\) — which has not happened.
- The tight identity \(w_n(\varepsilon)=2^{-L(n,\varepsilon)}-2^{-40}\)
  holds **exactly** at every layer \(n\le20\) and every
  \(\varepsilon\in\{0.05,0.1,0.2\}\) — now certified by full-sweep-exact
  minima (§2), extending the plateau packet's \(n\le13\) full sweeps.
  P4 remains tight; it cannot be improved without finer geometry.

## 7. Counterexample watch (mandatory section)

- **(a) Off-chain unit frequency beating the on-chain peak: NONE.**
  Every \(B_n(\varepsilon)\) member at every layer \(n\le20\) and
  \(\varepsilon\in\{0.05,0.1,0.2\}\) has an exact base-2 discrete
  logarithm for itself or its negative (BSGS, no floats); the bad set is
  contained in a doubled chain interval \(\{\pm2^{k-j}\}\) at every
  layer/\(\varepsilon\) (asserted); the argmax at every layer is
  \(\pm2^{k}\) with \(k=O(n)\). The resonance-chain structure is intact
  at depth 20.
- **(b) Escape weight dropping faster than the creep law: NONE.** The
  tight identity \(w_n=2^{-L}-2^{-40}\) never failed; no
  \(w_n(\varepsilon)<2^{-L}-2^{-40}\); no \(L\)-jump by more than 1
  between consecutive layers; \(w_n(0.05)\ge1/4-2^{-40}\) throughout.
- **(c) Profile plateau/reversal: STALL OBSERVED, no reversal.** The
  \(p_2\) drift rate dropped \(\sim3\times\) and the even branch is
  saturating (\(0.8003\to0.8013\) over two layers); \(p_2\) stays in
  \([0.68,0.81]\) throughout \(n=15..20\), far from both \(0.95\) and
  from collapse. This is the packet's central measurement (§5), reported
  as such, not as an anomaly: it weakens the linear form of resolution
  (ii) without confirming resolution (i).
- **(d) Proved-control failures: NONE.** S1 errors
  \(\le2.2\times10^{-19}\); S3 holds at every resolved layer (exact
  weights, asserted); Lemma 2 holds at every dense-checked layer
  (\(n\le15\)); the dense-FFT cross-check of the kernel agrees to
  \(9.7\times10^{-17}\) on all units (\(n\le15\)).

## 8. What is measured vs what is proved; honest limits

- **Exact (integer/Fraction arithmetic):** chain exponents \(k(n)\) and
  all discrete logs; on-chain membership of every bad-set member and
  every profile point; containment intervals and their lengths \(L\);
  the circle-point Fractions and dominant-pair misalignments; the
  no-wrap certificates \(2^k<3^n\); the candidate-set reduction of the
  escape-weight minimum.
- **Float64 measurements (hypothesis-generators, never theorems):**
  \(M_n\), \(c_n\), the \(p_j\) and \(\psi_j\) profiles, the \(w_n\)
  values (exact minima of float64-defined sums), all fits, slopes,
  residuals, and crossings.
- **Proved controls asserted:** Lemma 2 (\(n\le15\)), S1 (\(n=9,12\)),
  S3 (every resolved layer), P1-phase formula (exact, given the measured
  peak), P4 tightness (checked, exact).
- **Limits.** This packet changes nothing about asymptotics: the
  \(n\le20\) window cannot distinguish \(L\) bounded from
  \(L\sim\tfrac12\log_2n\) (P6's \(n^*=1776\) is far away), \(w_n(0.05)\)
  is dyadic-quantized and a \(c/\sqrt n\) law is invisible below the
  \(1/4\) threshold, and the parity alternation shows that single-window
  linear fits of this profile are not stable under extension. The
  falsified object is one float64 extrapolation, nothing more.

## 9. Provenance and related work

Built directly on the syracuse-fourier packet (the recursion, Lemma 2),
the scalar-phase-second-moment packet (S1/S3, chain machinery), the
deep-fourier-scan packet (certified \(n\le17\) values regressed against
here; BSGS code lineage), and the plateau-escape-weight packet (profile
definitions, containment/escape-weight machinery, exact chain phases,
and the prediction under test). The transport identity was re-derived
from the dense construction and validated to \(10^{-16}\) against FFT at
every layer \(n\le15\).

Methodological lineage: this program follows the structural-compression
framing of the dialogue *A Structural-Compression Framework for the
Collatz Conjecture* (**chatgpt-thread-1784792218410**) — its 'Terence
Method' template *accelerate \(\to\) encode \(\to\) transport between
scales \(\to\) classify persistent failure \(\to\) eliminate the rigid
cases*: the resonance chain is precisely the "persistent failure" class
of the layer-to-layer transport, and this packet is the classification
step carried one depth increment further (its §14 translation ledger
maps to our P4/P5 reductions; its miracle ledger to our counterexample
watch). The framework influenced motivation and framing only; every
arithmetic control here is local to this repo and unchanged by it. The
profile/chain geometry itself remains the profile form of Tao's
Proposition 1.17 (arXiv:1909.03562, §7), and the drifting chain exponent
\(k(n)\approx1.343n\) quantifies the same 2–3 Diophantine lattice as the
cycle-equation literature (Eliahou 1993; Simons–de Weger 2005) and
Siegel's non-Archimedean treatment (arXiv:2412.02902).

## 10. Reproduce

```bash
python3 contribution/packets/2026-07-23-plateau-drift-test/verify_plateau_drift_test.py
python3 -m pytest contribution/packets/2026-07-23-plateau-drift-test/ -q
```

Certificate: `plateau_drift_certificate.json` (deterministic content,
regenerated by the verifier; timings live only in
`verify_plateau_drift_test.out`). Env knobs: `VPDT_N_MAX` (default 20;
reduced test mode 12 runs in ~1 s), `VPDT_DENSE_MAX` (default 15; dense
FFT cross-check depth, 0 skips), `VPDT_THREADS` (default min(14, cores)).
The C kernel is compiled at runtime by clang (cached by source hash); a
numpy fallback exists for portability and is certified only to
\(n\le15\). Requires clang (Xcode CLT) and numpy; no other dependencies.
