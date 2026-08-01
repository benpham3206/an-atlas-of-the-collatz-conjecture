# Chain-exponent law: the Beatty/rotation hypothesis is dead — and the exact chain recursion hands step 2 a better target

**Date:** 1 August 2026
**Status:** adjudication packet. **No new theorems.** All structural
verdicts below are *exact integer / Fraction arithmetic* on certified
inputs (labelled **exact**); fits, digit series, and the evaluation of
the chain recursion are **float64 measurements** (labelled). **Not** a
proof of superpolynomial decay of \(M_n\), **not** Collatz progress,
**not** a counterexample to anything proved. No literature-priority
claim.

**Companion executable evidence:** `verify_chain_exponent_law.py`,
`test_chain_exponent_law.py`, `chain_exponent_law_results.json`.

---

## 0. Verdict, up front

**The rotation/Beatty hypothesis \(k(n)=\lfloor\gamma n+\varphi\rfloor\)
is DEAD — all three pre-registered kill criteria fire ((a) and (b)
exactly, (c) as a labelled fit).** Step 2 of the program has **no
constant-slope rotation target**.

But test 4 returns the real prize, and it is *stronger* than the dead
hypothesis: **the restriction of the proved recursion (1.1) of the
syracuse-fourier packet to the resonance chain is an exact closed
subsystem** (closure identity: \(u_a\cdot2^k=2^{k-a}\bmod 3^n\), a
one-line proof), and its float64 evaluation **reproduces the certified
\(k(n)\) at every layer \(n=6..21\) and the certified \(M_n\) to a max
relative error of \(7.5\times10^{-14}\)**. The peak magnitude is, to
machine precision, entirely determined by the one-dimensional chain
dynamics. \(k(n)\) is therefore not a fit parameter but the output of an
exact integer-phase recursion — a provable target for step 2 that does
not pass through any rotation number.

The correct quantitative restatement (measured, not proved):
\(k(n)=n\log_2 3-\delta(n)\) with \(\delta(n)\in[3.09,6.12]\) over
\(n=6..21\) — the peak tracks the 2–3 Diophantine ray \(2^k\approx3^n\)
with a slowly growing bounded offset, not a Beatty line. Whether the
asymptotic slope is \(\log_23\) (\(\delta=o(n)\)) or genuinely smaller
(\(\delta\approx0.118\,n\), the measured drift) is the open question
step 2 must now attack, and the chain recursion is the object that
decides it.

## 1. The exact table (assembled from three certificates; cross-checked)

\(k(n)\): exact BSGS discrete logs (deep-fourier \(n=6..17\);
plateau-drift \(n=6..20\); streaming \(n=21\)). The deep-scan and
drift certificates agree **exactly** on \(k\) over \(n=6..17\) and on
\(M_n\) to \(\le10^{-9}\) relative (asserted by the verifier).
\(L(n,\varepsilon)\) from the drift creep table (\(n\le20\)) and the
streaming row (\(n=21\)); \(p_2(21)=0.887281\).

| \(n\) | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|
| \(k(n)\) | 6 | 8 | 9 | 10 | 12 | 13 | 14 | 16 | 17 | 18 | 20 | 21 | 23 | 24 | 26 | 28 |
| \(\Delta k\) | – | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 2 | 1 | 2 | 2 |
| \(M_n\) | .09611 | .07587 | .06089 | .04803 | .03828 | .03194 | .02646 | .02205 | .01913 | .01628 | .01441 | .01251 | .01119 | .009816 | .008885 | .007872 |
| \(L(0.05)\) | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 2 | 1 | 2 | 1 | 2 | 1 | 2 |
| \(L(0.1)\) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 2 |
| \(L(0.2)\) | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 3 | 4 | 4 | 4 | 4 | 4 |

(\(L(n,0.05)=1+(n\bmod2)\) exactly for \(n=13..21\) — the parity
alternation of the plateau-drift memo extends to \(n=21\); full values in
the results JSON.)

## 2. Test 1 — BEATTY feasibility: **EMPTY** (exact; kill criterion (a) FIRES)

The margin-1 condition
\(\max_n|k(n)-\lfloor\gamma n+\varphi\rfloor|<1\) is equivalent to
\(k(n)\le\gamma n+\varphi<k(n)+1\) for all \(n\). Eliminating
\(\varphi\), feasibility is equivalent to
\(\max_i(k_i-\gamma i)<\min_j(k_j+1-\gamma j)\), a pairwise-exact
computation over the 16 certified points (256 ordered pairs, Fraction
arithmetic). Result:

\[
\gamma>\frac32\ \ (\text{pair } k(21)=28,\,k(15)=18:\ 28-21\gamma<19-15\gamma),
\qquad
\gamma<\frac{11}{8}\ \ (\text{pair } k(7)=8,\,k(15)=18:\ 8-7\gamma<19-15\gamma).
\]

Since \(\tfrac32=\tfrac{12}{8}>\tfrac{11}{8}\), **the feasible
\((\gamma,\varphi)\) region is empty**. No Beatty line, of any slope and
phase, reproduces \(k(n)\) over \(n=6..21\) with error \(<1\). Note both
witnesses pass through \(k(15)=18\): the law is killed jointly by the
slow stretch \(k(7){\to}k(15)\) (slope \(5/4\)) and the fast stretch
\(k(15){\to}k(21)\) (slope \(5/3\)) — the slope itself accelerates.

## 3. Test 2 — STURMIAN balance: **FAILS** (exact; kill criterion (b) FIRES)

The difference word
\(\Delta k=(2,1,1,2,1,1,2,1,1,2,1,2,1,2,2)\) is two-valued
(\(\{1,2\}\)) but **not balanced**: it contains the length-2 factors
\((1,1)\) (sum 2, first at \(n=7\)) and \((2,2)\) (sum 4, at
\(n=20\)) — imbalance 2 at factor length 2, the maximal imbalance over
all factor pairs (all 120 pairs enumerated exactly). A balanced
two-valued word (Sturmian/mechanical, hence any Beatty difference word)
cannot contain both. Slope density: \(22/15=1.4\overline{6}\), with
CF \([1;2,7]\) — see test 3 for why this slope has no closed-form
standing.

## 4. Test 3 — CF-convergent law: **no alignment** (exact CF; labelled digit source)

CF of \(\log_23\) (from a ~60-digit exact-integer atanh-series value,
CF exact on those digits): \([1;1,1,2,2,3,1,5,2,23,\dots]\),
convergents \(1,2,3/2,8/5,19/12,65/41,84/53,485/306\), first
semiconvergents \(5/3,11/7,27/17,46/29,\dots\).

- The empirical slope \(22/15=[1;2,7]\) is **not** a convergent or
  semiconvergent of \(\log_23\) (checked against the exact CF tree).
- \(k(n)=\mathrm{round}(n\,c)\) fails for every candidate \(c\):
  errors for \(c=\log_23\) range over \(\{-3,-4,-5,-6\}\) (not
  constant); for \(c=3/2\) over \(\{-3,-4,-5\}\); for \(c=4/3\) over
  \(\{-2,-1,0\}\); for \(c=22/15\) over \(\{-2,-3,-4\}\). No
  single-offset rounding law.
- The \(\Delta k=2\) jump layers \(\{7,10,13,16,18,20,21\}\) do not
  align with \(\log_23\) convergent denominators
  \(\{1,2,5,12,41,53,306,\dots\}\), and their gaps
  \((3,3,3,2,2,1)\) are themselves shrinking — another exact symptom of
  the acceleration seen in test 1.
- What *does* hold (measured, float64): \(\delta(n)=n\log_23-k(n)\)
  stays in \([3.0947,6.1143]\) over the whole window — a bounded-offset
  law around the 2–3 Diophantine ray, with a visible slow upward drift
  (\(\delta(6)=3.51\) at the first \(\Delta k=2\) reset vs
  \(\delta(19)=6.11\) at the last-but-one). This is the restatement that
  replaces the dead Beatty law.

## 5. Test 4 — closed-form identification: **the chain recursion IS the law** (the prize)

**Exact (provable, one line).** In the proved recursion
\(\widehat c_{n+1}(\xi)=\sum_a2^{-a}e(-\xi u_a/3^{n+1})\,\widehat
c_n(\xi u_a\bmod3^n)\) with \(u_a=2^{-a}\bmod3^{n+1}\)
(syracuse-fourier Theorem 1), the chain is closed:
\(\xi=2^k\Rightarrow \xi u_a=2^{k-a}\bmod3^{n+1}\). Hence the
restriction to chain frequencies is the exact self-contained dynamical
system

\[
c_{n+1}[k]=\sum_{a\ge1}2^{-a}\,e\!\left(-\frac{2^{\,k-a}\bmod 3^{n+1}}{3^{n+1}}\right)c_n[k-a],
\qquad c_0\equiv1 ,
\tag{4.1}
\]

with **exact integer phases** (the residue \(2^{k-a}\bmod 3^{n+1}\) is a
modular power, computed in integers; negative exponents are taken mod
the group period \(2\cdot3^{n}\)). No new proof is needed for closure —
it is definitional from \(u_a=2^{-a}\).

**Measured (float64 evaluation of (4.1), labelled).** Over the full
certified window \(n=6..21\), (4.1) — evaluated with exponent window
\(k\in[-166,83]\) and \(a<147\), 0.3 s total — gives:

- \(\arg\max_k|c_n[k]|=k(n)\), the certified exponent, **at all 16
  layers** (asserted);
- \(\max_k|c_n[k]|=M_n\) to max relative error
  \(7.5\times10^{-14}\) against the certificates — i.e. the peak
  magnitude is machine-precision-equal to its chain restriction;
  off-chain frequencies contribute nothing at the peak, consistent with
  the certified on-chain argmax (BSGS) at every layer;
- the dominant pullback at the peak is **always \(a=1\)** (weight
  \(\approx0.51\)–\(0.59\); then \(a=2\approx0.27\),
  \(a=3\approx0.10\)): the peak at layer \(n\) is fed primarily from
  exponent \(k(n)-1\) at layer \(n-1\).

**The identified Diophantine condition (exact arithmetic on the
certified table).** With dominant pullback \(a=1\), the peak phase is
\(x_n=2^{k(n)-1}/3^n\) (exact Fractions in the results JSON), and

\[
x_n=\frac{2^{\Delta k(n)}}{3}\,x_{n-1},\qquad
\Delta k(n)\in\{1,2\},
\tag{4.2}
\]

a **multiplicative odometer**: each layer multiplies the phase by
\(2/3\) or \(4/3\). Over \(n=6..21\), \(x_n\in[0.0072,0.0585]\) — the
odometer is exactly the statement that \(2^{k(n)}\) stays a bounded
power-of-two fraction below \(3^n\), i.e. \(k(n)=n\log_23-O(1)\) of
test 3. A single threshold rule "\(\Delta k=2\iff x_{n-1}<\theta\)"
does **not** separate the full window (exact check:
\(\max x\) over \(\Delta k{=}2\) precedents \(=32/729=0.0439\) exceeds
\(\min x\) over \(\Delta k{=}1\) precedents \(=0.01083\)) — but it
**does separate the tail** \(n\ge15\) with
\(\theta\in\bigl(\tfrac{33554432}{3486784401},\tfrac{4194304}{387420489}\bigr)=(0.00962,0.01083)\)
(exact Fractions). The band edges themselves drift downward
(\(\max x_n\): \(0.0585\to0.0128\) over the window): a **drifting
odometer**, not a fixed rotation. This drift *is* the mechanism that
kills Beatty: the effective phase band moves, so no constant
\((\gamma,\varphi)\) survives.

**Why the peak drifts up (mechanism, measured).** The exponent walk
\(k\mapsto k-a\) (Geom(2), mean step \(-2\)) transports mass downward
in \(k\); exponents whose residue \(2^{k}\bmod3^n\) wraps to a large
cyclic value are dephased by the scalar factor and bleed out of the
chain profile. The coherent window is \(0\le k\lesssim n\log_23\); its
top edge rises by \(\log_23\approx1.585\)/layer while the walk pushes
down by \(\approx2\)/layer, and the profile's centre of mass settles
where cumulative phase cost is minimised — currently
\(\delta(n)=n\log_23-k(n)\approx3\)–\(6\) and slowly rising. Step 2's
target is now precise: **bound the drift of \(\delta(n)\) (equivalently
of the odometer band (4.2)) from the recursion (4.1)**. Bounded drift
\(\Rightarrow\) slope exactly \(\log_23\); the measured
\(\approx0.118\)/layer drift, if it persists, gives slope
\(\approx1.47\) — the data do not decide between these, and nothing in
the window forces either.

## 6. Kill criteria: outcomes

| criterion | status | evidence |
|---|---|---|
| (a) feasible \((\gamma,\varphi)\) interval empty | **FIRED (exact)** | §2: \(\gamma>3/2\) vs \(\gamma<11/8\) |
| (b) \(\Delta k\) fails balance | **FIRED (exact)** | §3: factors \((1,1)\) vs \((2,2)\), imbalance 2 |
| (c) residuals drift past 1 | **FIRED (labelled fit)** | vs the pre-registered prior fit \(1.3427n-1.7739\): residuals \(0.61,0.26,0.92,\mathbf{1.58}\) at \(n=18,19,20,21\) — rising tail, past 1 at \(n=21\). (Against a refit over \(6..21\) the max residual is \(0.88\); the pre-registered comparison is the prior-window fit, and it fires.) |

The rotation hypothesis is dead by (a) alone; (b) and (c) are
independent confirmations.

## 7. Counterexample watch (mandatory)

**Against the chain structure itself: nothing.** The closure identity
\(u_a2^k=2^{k-a}\) is exact at every depth, so the chain is an invariant
subsystem of the *proved* recursion by construction — the peak leaving
the \(\pm2^k\) chain would require an off-chain frequency beating every
chain value, and the certified BSGS argmax is on-chain at every layer
\(n\le21\) (deep-scan, plateau-drift, streaming packets; re-asserted by
cross-check here). No mechanism for a structural break is visible: the
off-chain mass is exactly what the L² bound (syracuse-fourier Corollary
3) and the escape weights already control. The one soft spot: (4.1)
reproduces \(M_n\) to \(7.5\times10^{-14}\), but that equality is
*measured*; a proof that the chain restriction captures the true
argmax for all \(n\) does not yet exist. Such a proof would convert the
entire uniform problem to the 1-D system (4.1) — this is the highest-
value theorem target exposed by this packet.

**Toward a theorem independent of measurements: two candidates.**
(i) The closure identity itself (provable now, one line) — it makes
(4.1) a well-defined exact object, so \(k(n)\) has a
*measurement-free definition* as the argmax of (4.1).
(ii) The odometer (4.2) with dominant pullback \(a=1\): if the \(a=1\)
dominance at the peak is proved, (4.2) becomes a theorem and \(k(n)\) is
a literal odometer — its rotation-like properties (bounded \(\delta\),
eventual slope) then reduce to drift estimates on a scalar recursion.

**Bearing on the superpolynomial program.** The dead Beatty law had
slope \(\approx1.47\); the correct ray has slope \(\log_23\). The
measured \(M_n\approx e^{-1.06\sqrt n}\) is consistent with a phase
budget set by the odometer band, but no identity found here bounds
\(\delta(n)\)'s drift, and the drift — not the slope — is what decides
whether \(k(n)\) is genuinely sub-\(\log_23\). Nothing in this packet
bears on unconditional proof or counterexample for Collatz itself;
nothing here strengthens or weakens Tao's \(n^{-A}\) (which remains the
best proved decay). The negative result is final for constant-slope
laws; the positive result (4.1) is a reduction, not a decay bound.

## 8. Related work

Built on the exact recursion of the syracuse-fourier packet (Theorem 1),
the certified tables of the deep-fourier-scan, plateau-drift-test, and
streaming-depth-21 packets, and the parity-alternation observations of
the plateau-drift memo (its dominant-pair phases
\(2^{k(n)-2}/3^n\) are the \(a=2\) pullback phases of §5). The 2–3 ray
\(2^k\approx3^n\) is the same lattice as the cycle-equation literature
(Eliahou 1993; Simons–de Weger 2005); the finding that the *peak
exponent* shadows this ray with bounded offset — rather than following a
Beatty law — appears to be new as a measured statement, and (4.1)/(4.2)
give its exact recursion form.

## 9. Reproduce

```bash
python3 contribution/packets/2026-08-01-chain-exponent-law/verify_chain_exponent_law.py
python3 -m pytest contribution/packets/2026-08-01-chain-exponent-law/ -q
```

Results: `chain_exponent_law_results.json` (deterministic content).
Env knob `VCEL_N_MAX` (default 21, min 8) reduces the chain-recursion
depth for tests; the full-depth run is < 1 s.
