# Deep Fourier scan: the resonance-chain structure at depth n = 17, and one measured law that needed restating

**Date:** 22 July 2026
**Status:** measurement packet. **No new theorems.** The proved
statements of the predecessor packets (syracuse-fourier Lemma 2;
scalar-phase Theorems S1 and S3) are re-verified here at greater depth
and **asserted** by the verifier; everything else is a float64
hypothesis-generator and is labelled as such. **Not** a proof of
Collatz, **not** a counterexample, **not** a proof of the conjectured
\(\exp(-c\sqrt n)\) decay. No literature-priority claim.

**Companion executable evidence:** `verify_deep_fourier_scan.py`,
`test_verify_deep_fourier_scan.py`, `verify_deep_fourier_scan.out`,
`deep_fourier_scan_certificate.json`.

---

## 1. Kill criteria, stated before build criteria

This packet exists to *fire* one of the following, if the data allows:

1. **(scalar-phase kill criterion 1 — the counterexample hunt).** Find a
   layer \(n\le17\) where \(B_n(0.1)\) contains a frequency off the
   \(\pm2^k\) resonance chain. **Result: NOT FIRED.** Every member of
   \(B_n(0.1)\), every layer \(6\le n\le17\), has an exact base-2
   discrete logarithm mod \(3^n\) (baby-step giant-step, exact integer
   arithmetic) for itself or its negative. No counterexample candidate
   exists in this flank at this depth.
2. **Break the reduction machinery.** Find a violation of Theorem S1
   (second-moment identity) or Theorem S3 (escape criterion) at depth.
   **Result: NOT FIRED.** S1 holds to \(\le5.3\times10^{-18}\) at
   \(n=6,9,12\); S3 holds with full-unit escape weights at every layer
   \(6\le n\le11\) (and on sampled units above, \(n\le16\)).
3. **Break the measured decay/shape laws.** Find a departure from
   \(M_n\approx e^{-c\sqrt n}\) (\(c\approx1.06\)) or from the chain
   exponent law. **Result: the decay law SURVIVES; the chain-exponent
   *window* law \(k(n)\in[n,n+3]\) BROKE at \(n=16\)** — see §4. This is
   a falsification of a float64-measured regularity of the
   scalar-phase packet (its §4(ii)), not of any proved statement, and it
   does not redirect the program: the chain itself is intact.

## 2. What was extended

All float64 measurements of the tao-structural-refinement,
syracuse-fourier, and scalar-phase packets, previously \(n\le14\), are
pushed to **\(n=17\)** (\(3^{17}=129{,}140{,}163\) residues), streaming:
at most two Syracuse layers and one FFT are alive at any moment; layer
construction reuses the syracuse-fourier recursion verbatim (provenance
comment in the verifier). Default runtime **80.4 s** (wall clock,
36 GB Mac); \(n=18\) was attempted behind `VDFS_N_MAX=18` and **failed
the engineering budget**: layer-18 construction alone exceeded the
300 s foreground window and the run was killed. \(n=17\) is therefore
the certified depth of this packet.

Per-layer protocol (certificate `layer_table`): \(M_n\); bad-set counts
\(|B(0.05)|,|B(0.1)|,|B(0.2)|\); argmax and its exact chain exponent
\(k(n)\); chain membership of **every** \(B(0.1)\) member; conjugate
symmetry of \(B(0.1)\); flat1/flat2 near-peak profile; escape-weight
average over 8192 seeded random units (\(\varepsilon=0.1\)); S1 identity
error at sampled frequencies (\(n=6,9,12\)); S3 bound (full units
\(n\le11\), sampled above); max \(|\widehat c_n|\) over nonzero
multiples of 3.

## 3. What held (all float64 measurements, n = 6..17)

**(i) The bad set stays tiny.** \(|B(0.05)|\le4\), \(|B(0.1)|\le6\),
\(|B(0.2)|\le8\) at every layer — the scalar-phase bounds survive
unchanged to \(n=17\).

**(ii) The bad set stays on the chain.** Every \(B(0.1)\) member at
every layer is \(\pm2^k\bmod 3^n\) with \(k\le22\), certified by exact
BSGS discrete log (no floats). Members come in \(\pm\) pairs;
conjugate-symmetry defect of \(B(0.1)\) is \(\le2.8\times10^{-17}\)
(FFT roundoff).

**(iii) The decay law survives.** \(M_n\) at \(n=14,15,16,17\):
\(0.0191280,\ 0.0162845,\ 0.0144095,\ 0.0125107\). Per-layer
\(c_n=-\ln M_n/\sqrt n\): \(1.0574,\ 1.0631,\ 1.0600,\ 1.0626\) —
stable around the previously measured \(c\approx1.06\). Least squares
over \(n=6..17\): through-origin fit \(c=1.0394\) (max residual
\(0.204\)); with-intercept fit slope \(1.2336\), intercept \(-0.6667\),
\(R^2=0.99872\), max residual \(0.0385\). The \(e^{-c\sqrt n}\) picture
is intact at depth.

**(iv) Typical frequencies escape immediately.** Seeded escape-weight
average (\(\varepsilon=0.1\), 8192 units/layer): \(0.9918\) at \(n=6\),
\(\ge0.9999\) for \(n\ge8\), \(\ge0.9999999999\) for \(n\ge12\). The
entire uniform problem remains the chain.

**(v) The near-peak profile stays flat but not flattening.** For
\(n\ge10\), flat1 ranges \(0.877\)–\(0.987\) and flat2 ranges
\(0.684\)–\(0.838\) — inside the scalar-phase ranges, no drift toward 1
(compare kill criterion 3 of that packet, which remains far from
firing).

**(vi) The reduction machinery is exact at depth.** S1 max error
\(5.2\times10^{-18}\) (\(n=6\)), \(6.5\times10^{-19}\) (\(n=9\)),
\(1.4\times10^{-20}\) (\(n=12\)). S3 full-unit escape weights:
\(w_{\min}\in\{1/2,1/4,1/8\}\) across \(n=6..11\),
\(\varepsilon\in\{0.05,0.1,0.2\}\), bound holds every layer (asserted).
Sampled S3 (\(\varepsilon=0.1\)) holds at \(n=12..16\) with sampled
\(w_{\min}=1.0\) from \(n=13\). Lemma 2 of syracuse-fourier holds at
every layer; \(r_{n+1}/r_n=0.50002\) at \(n=17\), still tending to
\(1/2\).

**(vii) Sanity on the \(M_n\) definition.** Max \(|\widehat c_n|\) over
*nonzero* multiples of 3 equals \(M_1=0.5773502692\) at every layer to
within \(7.4\times10^{-12}\) — exactly as the layer marginalisation
\(\widehat c_n(3\xi')=\widehat c_{n-1}(\xi')\) predicts, and a
structural reminder that the max over **all** nonzero frequencies never
decays: restricting to units is not a convenience, it is the theorem's
content.

## 4. What broke: the window law \(k(n)\in[n,n+3]\)

Chain exponents of the argmax, exact BSGS:

| \(n\) | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|----|----|----|----|----|----|----|----|
| \(k(n)\) | 6 | 8 | 9 | 10 | 12 | 13 | 14 | 16 | 17 | 18 | **20** | **21** |
| \(k-n\) | 0 | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 3 | **4** | **4** |

The law \(k(n)\in[n,n+3]\), measured for \(6\le n\le14\) in the
scalar-phase packet, fails first at \(n=16\) (\(k=20=n+4\)) and again at
\(n=17\) (\(k=21=n+4\)). A linear fit over \(n=6..17\) gives

\[
k(n)\approx 1.3427\,n-1.7739 ,
\]

consistent with that packet's in-window slope estimate \(\approx1.35\):
the break is the predicted consequence of a super-unit slope, not a new
phenomenon. The *structural* content — the peak lies on the
\(\pm2^k\) chain with \(k=O(n)\), absurdly small against the period
\(2\cdot3^{n-1}\) — is **strengthened**, not weakened, by this scan.
The honest restatement for future packets: *the chain-exponent law is
\(k(n)\sim1.34\,n\), not \(k(n)\in[n,n+3]\).*

## 5. Verdict

- The \(e^{-c\sqrt n}\) picture (\(c\approx1.06\)) **survives** to
  \(n=17\), with per-layer \(c_n\) stable in \([1.057,1.064]\) for
  \(n\ge13\).
- The resonance-chain law **survives in structure** (every near-max
  frequency is \(\pm2^{O(n)}\)); its quantitative window form is
  **falsified and restated** as \(k(n)\approx1.343n-1.774\).
- **No counterexample candidate** to any measured or proved statement
  was found. Kill criterion 1 of the scalar-phase packet did not fire;
  Theorems S1/S3 and Lemma 2 held everywhere they were checked.
- Confidence: high in the measurements (deterministic, seeded; the
  in-repo determinism test reproduces the certificate byte-identically
  at reduced depth, and an independent full-depth rerun also reproduced
  it byte-identically); the
  remaining gap is unchanged — all of §3–§4 is float64 evidence about a
  max over \(2\cdot3^{n-1}\) frequencies, and the proved route (S3)
  still needs a profile-independent lower bound on escape weights.

## 6. Related work

This is the deep-scan successor of the scalar-phase-second-moment
packet (whose S1/S2/S3 it re-verifies and whose §4 measurements it
extends), built on the syracuse-fourier recursion and the
tao-structural-refinement packet's measured \(e^{-1.06\sqrt n}\) law.
The chain exponent is a discrete logarithm base 2 modulo \(3^n\);
that 2 is a primitive root mod \(3^n\) (verified \(n\le6\) in the
syracuse-fourier packet) makes the BSGS certification of every bad-set
member exact. The falsified window law \(k(n)\in[n,n+3]\) and its
\(1.34n\) replacement quantify how the 2–3 Diophantine lattice (the
same lattice as the cycle-equation literature, Eliahou 1993;
Simons–de Weger 2005) drifts inside the unit group as depth grows.

## 7. Reproduce

```bash
python3 contribution/packets/2026-07-22-deep-fourier-scan/verify_deep_fourier_scan.py
python3 -m pytest contribution/packets/2026-07-22-deep-fourier-scan/ -q
```

Certificate: `deep_fourier_scan_certificate.json` (deterministic
content, regenerated by the verifier; timings live only in
`verify_deep_fourier_scan.out`). Env knobs: `VDFS_N_MAX` (default 17;
reduced test mode 10 runs in < 1 s), `VDFS_SAMPLES` (default 8192,
minimum 4000). `VDFS_N_MAX=18` is reachable in principle but exceeded
the runtime budget on the development machine (see §2).
