# Odometer dominance to n = 1000: a=1 dominance survives, the drift flattens toward slope log₂ 3, and the Δk=2 feed gap is measured at ρ ≥ 0.94 and closing

**Date:** 1 August 2026
**Status:** adjudication packet. **No new theorems.** All \(k(n)\),
\(\Delta k\), \(x_n=2^{k(n)-1}/3^n\), and window-tail bounds are **exact
integer / Fraction arithmetic**; every magnitude, weight, \(\delta(n)\),
slope, and SSR below is a **measurement** (mpmath mpc at 660 decimal
digits, gmpy backend; labelled). **Not** a proof of superpolynomial
decay, **not** Collatz progress, **not** a counterexample to anything
proved. No literature-priority claim.

**Companion executable evidence:** `verify_odometer_dominance.py`,
`test_odometer_dominance.py`, `odometer_dominance_results.json`
(1000 per-layer records, **certificate_format `slim-v1`**).

**Certificate packaging.** The committed JSON is a **slim** certificate
(~0.45 MB, not the multi‑MB full-precision dump): integer fields
\((n,k,\Delta k,\mathrm{argmax}_a)\) exact; magnitudes / weights /
\(\delta(n)\) stored at ~12 significant figures for clone size; exact
\(x_n = 2^{k-1}/3^n\) is recovered in tests from \((k,n)\) and is not
stored. Full-precision re-run: install `mpmath` (and preferably `gmpy2`),
then `ODOM_MODE=run` / `analyze` as documented in the verifier header.
Structural tests require **no** heavy deps: `python3 test_odometer_dominance.py`.

---

## 0. Verdict, up front

**Part 1 — a=1 dominance SURVIVES to n = 1000 (measurement).** At every
one of the 1000 layers, the dominant pullback at the recursion argmax is
\(a=1\), with a unique maximum and a margin over the best competitor of
at least **0.239** (min at \(n=21\)). \(w_1\in[0.5038,0.6474]\) over the
chain regime \(n\ge6\) (the 0.647 is the \(n=6\) value; from \(n=21\)
on, \(w_1\in[0.504,0.558]\), tail value \(w_1(1000)=0.5218\)).
\(\Delta k(n)\in\{1,2\}\) at every layer \(n\ge6\), \(k(n)\) monotone.
No kill criterion fired. The recursion argmax matches the certified
(exact BSGS) \(k(n)\) at all \(n=6..21\) and the certified \(M_n\) to
max relative error \(7.5\times10^{-14}\).

**Part 2 — the drift does NOT persist; the fork breaks toward slope
\(\log_2 3\).** Over \(n=6..21\) \(\delta(n)\) drifted \(\approx0.118\)/layer;
over \(n=6..1000\) the best linear-\(\delta\) slope is only
**\(4.35\times10^{-4}\)**/layer (implied \(k\)-slope \(1.5845\), vs
\(\log_2 3 = 1.58496\)), and the model ranking prefers **logarithmic
drift** \(\delta=\alpha\log n+\beta\) on both the full range (SSR ratio
vs linear **0.805**) and the tail \(n>503\) (ratio **0.99995**, nearly
tied but same ranking). \(\delta(n)\in[3.09,7.26]\) over the full run.
The dominance weight \(w_1\) is flat in the tail (slope
\(-2.7\times10^{-7}\)/layer, consistent with 0): **no early warning of
dominance failure**.

**Part 3 — the implication "a=1 dominance ⇒ odometer (4.2)" has a real
but small and closing gap.** On \(\Delta k=2\) layers the peak is fed
from exponent \(k(n)-1=k(n-1)+1\), one **above** the previous peak, not
from the peak itself. Measured: that feed cell's magnitude is a factor
\(\rho_n\ge 0.9387\) of the previous peak (worst at \(n=10\)), **rising
with \(n\)** (fit slope \(+3.8\times10^{-6}\)/layer; tail values
\(0.96\)–\(0.9999\)). The strengthened statement that WOULD imply the
odometer is: *"a=1 dominance from a near-peak exponent whose magnitude
is within factor \(\rho\) of the peak"*, with \(\rho=0.93\) measured to
hold to \(n=1000\) and the gap closing. Without it, the odometer (4.2)
survives only as the definitional identity \(x_n=(2^{\Delta k}/3)x_{n-1}\)
(exact), not as a consequence of dominance. Additional measured warning:
the single-threshold rule "\(\Delta k=2\iff x_{n-1}<\theta\)", which
separated the tail \(n\ge15\) in the predecessor packet, **stops
separating in the deep tail** (\(n\ge500\): max \(x\) over \(\Delta k=2\)
precedents \(0.0049077\) > min \(x\) over \(\Delta k=1\) precedents
\(0.0049025\), interleaved by \(\sim0.1\%\)).

## 1. Kill criteria (stated before results, per house rules)

- **K1:** any layer \(n\) with \(\arg\max_a w_a\neq1\), or \(w_1\) not
  the unique maximum. *Applies to every layer, including the transient.*
- **K2:** \(k(n)\) non-monotone or \(\Delta k(n)\notin\{1,2\}\), checked
  for \(n\ge6\) (layers 1–5 are the \(c_0\equiv1\) transient; the chain
  has not organised and the certified window starts at \(n=6\)).
- **K3:** any stability check fails (measurement then void):
  - **S1** \(a\)-window convergence: tail bound
    \(\sum_{a>80}2^{-a}=2^{-80}<10^{-24}\) (exact) recorded per layer;
    at \(n\in\{50,100,200,300,500,750,1000\}\) the pullback sum is
    extended to \(a\le140\) and must add \(<10^{-30}\) of \(w_1\).
  - **S2** exponent-window convergence: a rerun with a deeper fixed
    bottom (\(-900\) vs \(-750\)), higher top (\(2.6n+40\) vs
    \(2.2n+30\)), and \(a\le110\) must reproduce \(k(n)\) exactly and
    \(M_n,w_1\) to \(10^{-12}\) for \(n\ge100\) (post-transient).
  - **S3** argmax cross-check against the exact certificates
    (\(n=6..21\), from the chain-exponent-law packet, read-only).
  - **S4** \(+50\) dps rerun (710 dps) to \(n=300\): identical \(k(n)\),
    \(w_a\) to \(10^{-12}\).
  - **S6** phase-chain accuracy: the squaring-chain phase factors are
    verified against direct cos/sin from the exact integer residue at
    every layer (assertion, \(<10^{-100}\)).

**Outcome: no kill criterion fired.** S1: worst extension weight
\(7.4\times10^{-37}\) of \(w_1\). S2: pass (all \(n\ge100\);
float64-floor agreement, \(dM\le2.3\times10^{-16}\)). S3: pass (16/16
layers, and \(M_n\) to \(7.5\times10^{-14}\)). S4: pass. S6: pass every
layer. Transient deviations (\(n<100\)) between the two window configs
are recorded in the results JSON (`transient_deviations_n_lt_100`); they
are a diagnosed truncation effect, decaying, and never touch \(k(n)\)
for \(n\ge6\).

## 2. Setup and methodology (including two honest failure reports)

The recursion (4.1) is evaluated with **exact integer phases**: residues
\(r_j=2^j\bmod 3^{n+1}\) are exact integers (iterated doubling; one
`pow` seed per layer), and the phase factors \(E[j]=e^{-2\pi i r_j/m}\)
are generated by complex squaring (\(\theta\to2\theta\bmod 2\pi\)
exactly), restarted from the exact residue every 256 positions.

**Failure report 1 (phase chain).** A bare squaring chain amplifies the
seed rounding by \(2^s\) after \(s\) squarings; at 660 dps the phase
factors blew up (double-exponentially, \(|E|=(1+\varepsilon)^{2^s}\)) at
\(n\approx540\), exactly where the window index \(s\approx2193\)
satisfies \(2^s\sim10^{660}\). Detected as a catastrophic \(M_n\)
excursion (\(M_{540}\sim10^{167}\)); fixed by the restart scheme above
(residual error \(\le2^{256}\cdot10^{-660}\approx10^{-583}\), asserted
per layer against direct evaluation).

**Failure report 2 (window truncation).** The window geometry is
load-bearing, and two plausible choices are *wrong*:

- A bottom edge **receding faster than the mean up-walk** (\(+2\)/layer)
  continuously eats the climbing mass: with bottom \(-2.2n-12\) the
  peak-region magnitudes were corrupted by **9% at \(n=151\)**
  (measured against a \(-6n-40\) bottom); even \(-6n-40\) drifts
  (\(6.5\times10^{-4}\) at \(n=300\) vs \(-10n-60\)). Fix: a **fixed**
  bottom \(L=-750\). Starvation is then confined to a band
  \([L,L+100)\) (error \(\le2^{-(k-L)}\)), and the starved transient
  ridge climbs away from the cut, staying \(\ge150\) exponents below
  the peak at \(n=1000\). Validated: fixed \(-750\) vs fixed \(-900\)
  agree to \(5.5\times10^{-152}\) at \(n=150\), and to a deep receding
  bottom \(-14n-80\) to \(7\times10^{-13}\).
- The **top** edge corrupts too: the \(\sim80\) cells below each
  window top miss their higher pullers, and the peak's downward
  ancestor cone intersects earlier corrupted bands. Measured effect at
  the peak: \(1.4\times10^{-8}\) at \(n=150\) with top \(1.7n+12\).
  Fix: top \(2.2n+30\) (gap \(\ge0.65n+30\) above the ray); the
  monitored right-edge ratio is then \(\le10^{-90}\) of peak for all
  \(n\ge500\), \(\le4.2\times10^{-178}\) at \(n=1000\).

The production window is therefore \(k\in[-750,\lfloor2.2n\rfloor+30)\),
\(a\le80\), at 660 dps (\(\ge0.6n+60\) at every layer per the mission
guidance). The argmax is canonicalised: \(c_n\) is exactly periodic in
\(k\) with period \(2\cdot3^{n-1}=\mathrm{ord}_{3^n}(2)\) and
\(|c_n[k+3^{n-1}]|=|c_n[k]|\) (conjugate symmetry, \(2^{3^{n-1}}\equiv-1\));
\(k(n)\) is the canonical representative in \([0,2\cdot3^{n-1})\) (at
\(n=6\) the raw argmax returns the exact tie \(k=-480\equiv6\)).

**Left-tail background (measurement).** The non-resonant background at
fixed \(k\approx-650\) decays like \(\sim3^{-n/2}\) (\(5.0\times10^{-1}\)
of peak at \(n=6\), \(5.4\times10^{-24}\) at \(n=100\), below the
truncation floor by \(n\approx120\)), while \(M_n\sim e^{-2.48\sqrt n}\)
for \(n\ge100\) (float64 fit) — the peak separates from the background
exponentially. Consequently a "window truncates nothing above
\(10^{-300}\) of peak" edge criterion is unattainable in principle at
any computationally reachable depth; the substantive truncation
validation is S2/S3/S4 above, and it passes.

**Environment.** `mpmath 1.4.1` + `gmpy2 2.3.1` were `pip install`ed
into the managed Python venv (user-site install is not visible there);
mpmath runs on the gmpy C backend. (Predecessor float64 spot checks
match; the decimal-module fallback was not needed.)

## 3. Part 1 results (all measurements at 660 dps unless stated)

Headline rows (full per-layer data in the results JSON):

| \(n\) | 6 | 21 | 100 | 300 | 500 | 750 | 1000 |
|---|---|----|-----|-----|-----|-----|------|
| \(k(n)\) (exact) | 6 | 28 | 152 | 469 | 786 | 1182 | 1578 |
| \(\delta(n)\) | 3.51 | 5.28 | 6.50 | 6.49 | 6.48 | 6.72 | 6.96 |
| \(w_1\) | 0.647 | 0.512 | 0.518 | 0.511 | 0.510 | 0.516 | 0.522 |
| \(w_2\) | – | 0.273 | 0.262 | – | 0.261 | – | 0.259 |

- \(\arg\max_a=1\) at **all 1000 layers**; \(w_1\) margin over the best
  other \(a\) \(\ge0.239\); \(w_2\le0.334\) (max at \(n=2\)),
  \(w_2\approx0.26\) and \(w_3\approx0.12\) stable, ordering
  \(w_1>w_2>w_3\) at every layer \(n\ge6\) (asserted by tests).
- \(\Delta k\in\{1,2\}\) at every layer \(n\ge6\): 578 twos, 419 ones;
  mean \(\Delta k = 1.5809\) (\(n=6..1000\)), vs \(\log_23=1.58496\).
- \(\delta(n)=n\log_23-k(n)\in[3.095,7.257]\) (exact \(k\), 60-digit
  exact-series \(\log_23\), float64 evaluation: measurement).
- Odometer band (exact Fractions): \(x_n\in[0.00327,0.0585]\) for
  \(n\ge6\) (min at \(n=874\), max at \(n=7\)); over \(n\ge500\),
  \(x_n\in[0.00327,0.00654]\) — the band keeps drifting down, i.e.
  \(\delta\) keeps creeping up, slowly (see Part 2).

## 4. Part 2: drift discrimination (float64 least squares, measurement)

Fits of \(\delta(n)\) over the chain regime \(n=6..1000\) and the tail
\(n=504..1000\):

| model | full \(\alpha\) | full SSR | tail \(\alpha\) | tail SSR | SSR ratio (full) | SSR ratio (tail) |
|---|---|---|---|---|---|---|
| \(\delta=\alpha n+\beta\) (linear) | \(4.35\times10^{-4}\) | 152.85 | \(2.8\times10^{-5}\) | 41.345 | 1.000 | 1.000000 |
| \(\delta=\alpha\sqrt n+\beta\) | \(2.18\times10^{-2}\) | 142.97 | \(1.6\times10^{-3}\) | 41.344 | 0.935 | 0.999974 |
| \(\delta=\alpha\log n+\beta\) | 0.2316 | 123.09 | \(2.29\times10^{-2}\) | 41.342 | **0.805** | **0.999947** |

- Ranking **log > sqrt > linear on both ranges** (stable). The tail is
  nearly tied (all SSR ≈ 41.34), but the log model wins on both, and
  the full-range margin is substantial (20%).
- The \(0.118\)/layer drift measured over \(n=6..21\) **did not
  persist**: full-range linear slope \(4.35\times10^{-4}\), tail slope
  \(2.8\times10^{-5}\). The implied \(k\)-slope from the linear model is
  \(1.5845\), and the measured mean \(\Delta k=1.5809\) is still
  creeping toward \(\log_23\). The data now favour the
  **sublinear-drift branch** (asymptotic slope \(\log_23\)) — this is
  the "beat-Tao-favourable" outcome — but only as a measurement on
  \(n\le1000\); nothing here bounds \(\delta(n)\).
- Dominance-weight early warning: \(w_1\) fit slope
  \(-7.6\times10^{-6}\)/layer over \(n=6..1000\) (driven by the
  \(n=6..21\) descent from 0.65), **\(-2.7\times10^{-7}\)/layer over the
  tail** — flat. No evidence of declining dominance.

## 5. Part 3: the \(\Delta k=2\) logic gap (Kill C), quantified

The claim "a=1 dominance ⇒ odometer (4.2)" requires the peak's \(a=1\)
feed \(k(n)-1\) to coincide with the previous peak \(k(n-1)\), i.e.
\(\Delta k=1\). On \(\Delta k=2\) layers (58% of layers),
\(k(n)-1=k(n-1)+1\): the feed is the cell **one above** the old peak.

**Measured.** \(\rho_n=|c_{n-1}[k(n)-1]|/M_{n-1}\) on \(\Delta k=2\)
layers: min **0.93872** (at \(n=10\)), max 0.99992 (at \(n=875\)),
rising with fit slope \(+3.8\times10^{-6}\)/layer (intercept 0.978);
deep-tail values (\(n=984..999\)) range \(0.962\)–\(0.997\). Over all
578 \(\Delta k=2\) layers, \(\rho_n\ge0.938\).

**The correct strengthened statement** that would imply the odometer:

> **(D\(_\rho\))** At every layer, the \(a=1\) pullback to the peak
> comes from an exponent \(k(n)-1\) whose layer-\((n-1)\) magnitude is
> within factor \(\rho\) of the layer peak \(M_{n-1}\), with
> \(\rho<1\) a constant.

Measured to hold with \(\rho=0.93\) to \(n=1000\), with the gap closing
(slowly). Under (D\(_\rho\)), the peak phase recursion
\(x_n=(2^{\Delta k}/3)x_{n-1}\) inherits from dominance up to a
multiplicative \(\rho\)-factor per \(\Delta k=2\) step — an odometer
with a bounded relative slip, which integrates to at most
\((1/\rho)^{\#\{\Delta k=2\}}\) distortion of any magnitude estimate
derived purely from dominance. Without (D\(_\rho\)), the odometer
reduces to the **definitional identity** \(x_n=(2^{\Delta k}/3)x_{n-1}\)
(exact, trivially true from \(x_n=2^{k(n)-1}/3^n\)) with no dynamical
content: dominance alone says nothing about \(\Delta k=2\) layers.

**Additional structural warning (measurement).** The predecessor
packet's tail-separated threshold rule "\(\Delta k=2\iff x_{n-1}<\theta\)"
(separated for \(n\ge15\), window \(n\le21\)) **fails to separate for
\(n\ge500\)**: max \(x\) over \(\Delta k=2\) precedents
\(0.0049077 > 0.0049025\) min \(x\) over \(\Delta k=1\) precedents —
the bands interleave by \(\sim0.1\%\). A pure-threshold odometer law is
therefore also dead in the deep tail; the odometer survives only with
the drifting, non-threshold dynamics (4.2).

## 6. Kill criteria: outcomes

| criterion | status | evidence |
|---|---|---|
| K1 argmax\(_a=1\) every layer | **not fired** | 1000/1000 layers; margin \(\ge0.239\) |
| K2 monotone, \(\Delta k\in\{1,2\}\) (\(n\ge6\)) | **not fired** | 995/995 steps |
| K3/S1 \(a\)-window tail | pass | \(\le7.4\times10^{-37}\) of \(w_1\) |
| K3/S2 window convergence | pass (post-transient) | \(dM\le2.3\times10^{-16}\), \(\Delta w_1=0\) at float floor, \(n\ge100\) |
| K3/S3 certificate cross-check | pass | \(k(n)\) exact match 16/16; \(M_n\) to \(7.5\times10^{-14}\) |
| K3/S4 +50 dps | pass | identical \(k(n)\), \(w_a\) to \(10^{-12}\), \(n\le300\) |
| K3/S6 phase chain | pass | assertion \(<10^{-100}\) every layer |

## 7. Counterexample watch (mandatory)

**Leaving the chain.** Nothing new against the chain: the recursion
argmax stays on the 2–3 ray to \(n=1000\), and the non-resonant
background decays like \(3^{-n/2}\) — exponentially faster than
\(M_n\sim e^{-2.48\sqrt n}\) (both measurements) — so the peak
separates further with depth, the opposite of an escape signature.
The one soft spot is unchanged and now sharper: (4.1)'s equality with
the true peak is *measured* (to \(7.5\times10^{-14}\) at \(n\le21\));
a proof that the chain restriction captures the true argmax for all
\(n\) remains the highest-value target.

**Counterexample shape constraints.** The drift discrimination now
favours asymptotic slope \(\log_23\) for \(k(n)\) (sublinear
\(\delta\)): measured, consistent with the density requirement
(liminf density \(\log_32\)) rather than a strictly sub-ray slope that
the \(0.118\)/layer extrapolation would have implied (slope
\(\approx1.47\)). The measured steepening of the peak decay
(\(e^{-2.48\sqrt n}\) for \(n\ge100\), vs \(e^{-1.06\sqrt n}\) over the
shallow window) also goes against, not toward, a slow-decaying
counterexample-compatible profile. Both are measurements on \(n\le1000\)
only; no proof content. Nothing here bears on the aperiodicity or
complexity-\(\ge1.71k\) constraints.

**What would kill the program next.** (i) Prove or refute (D\(_\rho\))
— it is now the precise missing lemma for the odometer. (ii) The
deep-tail threshold interleaving (§5) means any future "rotation-like"
law for \(k(n)\) must come from drift estimates on (4.1), not from a
threshold rule.

## 8. Related work

Builds directly on the 2026-08-01-chain-exponent-law packet (its (4.1)
is the system extended here; its certified \(k(n),M_n\) are the S3
cross-checks, read-only) and the syracuse-fourier packet's Theorem 1.
The window-truncation failure modes of §2 (receding-bottom starvation;
top-band corruption; squaring-chain amplification) are general hazards
for windowed evaluation of (4.1) and are documented for reuse.

## 9. Reproduce

```bash
pip install mpmath gmpy2            # into the managed venv
cd contribution/packets/2026-08-01-odometer-dominance
ODOM_MODE=run ODOM_N_LO=1   ODOM_N_HI=500 python3 verify_odometer_dominance.py   # ~4 min
ODOM_MODE=run ODOM_N_LO=501 ODOM_N_HI=1000 python3 verify_odometer_dominance.py  # ~7 min
ODOM_MODE=wide     ODOM_WIDE_N=300 python3 verify_odometer_dominance.py          # ~3.5 min
ODOM_MODE=dpscheck ODOM_DPS_N=300 python3 verify_odometer_dominance.py           # ~2 min
ODOM_MODE=analyze python3 verify_odometer_dominance.py                           # <1 s
python3 -m pytest . -q                                                           # ~7 s
```

Measured wall times (this machine): main run 241 s (1–500) + 172 s
(501–750) + 24 s (974–1000; the 751–973 leg ran ~4 min before an
interruption and resumed from its per-layer checkpoint); wide 3 m 34 s;
dpscheck 2 m 09 s; analyze < 1 s; pytest 7.2 s (18 tests).
Deterministic content: `odometer_dominance_results.json`.
