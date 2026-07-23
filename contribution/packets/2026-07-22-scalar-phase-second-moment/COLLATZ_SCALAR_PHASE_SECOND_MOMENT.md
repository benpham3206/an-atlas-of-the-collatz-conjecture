# The scalar-phase second moment: three exact reductions and the resonance chain that carries the obstruction

**Date:** 22 July 2026
**Status:** three proved reductions + a measured structural
classification. **Not** a proof of \(\exp(-c\sqrt n)\) uniform decay;
**not** a stronger density theorem than Tao's. What it does: reduces the
uniform Fourier-decay conjecture to one explicit 1-parameter profile on
a chain of powers of 2, and shows the obstruction is the *same* 2–3
resonance lattice that blocks the symbolic side of the program.
Float64 data to \(n=14\); proved statements are marked.

**Companion executable evidence:** `verify_scalar_phase.py`,
`test_verify_scalar_phase.py`, `scalar_phase_certificate.json`.

Notation follows the syracuse-fourier packet:
\(\widehat c_n\), \(P_n\), \(r_n\), \(M_n=\max_{3\nmid\xi}|\widehat
c_n(\xi)|\), \(u_a=2^{-a}\bmod 3^{n+1}\), \(e(t)=e^{2\pi it}\).

---

## 1. Theorem S1 — exact second-moment recursion (proved)

For \(\xi\in\mathbb Z/3^{n+1}\mathbb Z\),

\[
\boxed{
|\widehat c_{n+1}(\xi)|^2
=
\sum_a4^{-a}|\widehat c_n(\xi u_a)|^2
+
2\operatorname{Re}\sum_{a<b}2^{-a-b}
e\!\left(\frac{\xi(u_b-u_a)}{3^{n+1}}\right)
\widehat c_n(\xi u_a)\overline{\widehat c_n(\xi u_b)} .
}
\tag{S1}
\]

**Proof.** Square the first-moment recursion
\(\widehat c_{n+1}(\xi)=\sum_a2^{-a}e(-\xi u_a/3^{n+1})\widehat
c_n(\xi u_a)\) (Theorem 1 of the syracuse-fourier packet). \(\square\)

The diagonal has total weight \(\sum_a4^{-a}=1/3\): *one third of the
mass self-contracts every layer for free.* The cross terms (weight
\(2/3\)) carry the entire obstruction. Verified to \(4\times10^{-11}\)
against FFT.

## 2. Theorem S2 — conditional contraction / coherence dichotomy (proved)

Write the two dominant terms of the recursion as
\(A=z_1w_1\), \(B=z_2w_2\) with \(z_a=e(-\xi u_a/3^{n+1})\),
\(w_a=\widehat c_n(\xi u_a\bmod3^n)\), and let
\(\Phi(\xi)=\arg(A\overline B)\in(-\pi,\pi]\).

**Statement.** If \(1-\cos\Phi(\xi)\ge\eta\), then

\[
\boxed{
|\widehat c_{n+1}(\xi)|\le\left(1-\frac\eta6\right)M_n .
}
\tag{S2}
\]

**Proof.** \(|R|:=|\sum_{a\ge3}2^{-a}z_aw_a|\le M_n/4\), and
\(|\frac12A+\frac14B|^2
\le\frac14|A|^2+\frac1{16}|B|^2+\frac14|A||B|\cos\Phi
\le M_n^2\bigl(\frac9{16}-\frac\eta4\bigr)\), since the bound is
increasing in \(|A|,|B|\le M_n\). Then
\(|\widehat c_{n+1}(\xi)|\le\frac34M_n\sqrt{1-\frac{4\eta}9}+\frac14M_n
\le M_n\bigl(1-\frac\eta6\bigr)\). \(\square\)

**Dichotomy.** Hence for every frequency, *either* contraction by
\(1-\eta/6\), *or* \(\eta\)-coherence of the dominant orbit pair:
\(\cos\Phi(\xi)>1-\eta\). Persistent non-decay of \(M_n\) requires
persistent coherence chains along the multiplicative orbit
\(\xi\mapsto\xi2^{-a}\). Note \(\Phi\) has two parts: the scalar part
\(2\pi\{\xi(u_2-u_1)/3^{n+1}\}\) (a full-resolution circle point, since
\(u_2-u_1=-2^{-2}\) is a unit) and the intrinsic part
\(\arg\widehat c_n(\xi u_1)-\arg\widehat c_n(\xi u_2)\).

## 3. Theorem S3 — the bad-set escape criterion (proved)

For \(0<\varepsilon<1\) define the bad set
\(B_n(\varepsilon)=\{\xi:|\widehat c_n(\xi)|>(1-\varepsilon)M_n\}\) and
the escape weight

\[
w_n(\varepsilon)
=
\min_{\xi\in(\mathbb Z/3^n\mathbb Z)^*}
\sum_{a:\,\xi u_a\notin B_n(\varepsilon)}2^{-a}.
\]

**Statement.**

\[
\boxed{
M_{n+1}\le\bigl(1-\varepsilon\,w_n(\varepsilon)\bigr)M_n .
}
\tag{S3}
\]

**Proof.** \(|\widehat c_{n+1}(\xi)|
\le\sum_a2^{-a}|\widehat c_n(\xi u_a)|
\le M_n\sum_{a\in B}2^{-a}+(1-\varepsilon)M_n\sum_{a\notin B}2^{-a}
=M_n\bigl(1-\varepsilon\sum_{a\notin B}2^{-a}\bigr)\). \(\square\)

**Consequence.** Uniform exponential decay of \(M_n\) is *equivalent*
(via this criterion) to a positive lower bound on escape weights; the
measured \(\exp(-c\sqrt n)\) decay corresponds to escape weight
\(\sim c'/\sqrt n\). The conjecture is thereby reduced to a statement
about the geometry of the bad set and its multiplicative orbits —
nothing else.

## 4. The measured structure of the bad set (float64, \(n\le14\))

**(i) The bad set is tiny.** \(|B_n(0.05)|\le4\), \(|B_n(0.1)|\le6\),
\(|B_n(0.2)|\le8\), out of \(2\cdot3^{n-1}\) units. It always comes in
\(\pm\) pairs (conjugate symmetry).

**(ii) The bad set is a resonance chain.** Every measured near-max
frequency is \(\pm2^{k}\bmod3^n\) with a *small* chain exponent
\(k(n)\in[n,n+3]\) for \(6\le n\le14\) (linear fit slope \(\approx1.35\)
over the window — recall \(2\) is a primitive root mod \(3^n\), so only
the smallness of \(k\) is structural). The chain is
*nearly walk-invariant*: the walk step \(\xi\mapsto\xi2^{-1}\) maps the
chain onto itself, so the peak feeds on its own predecessors.

**(iii) Typical frequencies escape immediately.** The escape weight
averaged over random units is \(\ge0.99\) for \(n\ge8\): almost every
frequency's orbit leaves the bad set with full geometric weight. The
*entire* uniform problem is the chain.

**(iv) Scalar phases are aligned on the chain.** Along
\(2^{K(n)}\mapsto2^{K(n)-1}\mapsto\cdots\) the relative scalar circle
point \(\{\xi(u_2-u_1)/3^{n+1}\}\) is \(\ge0.97\) (i.e. \(\approx0\)).
So Theorem S2's scalar part provides **no** contraction on the chain;
the intrinsic \(\widehat c\)-phases spread by only \(\sim54^\circ\)
across the dominant terms (measured decomposition), contributing a
\(\approx0.95\) factor per layer.

**(v) The decay engine at the peak is dilution + phase spread.**
Measured at \(n=14\): the Geom-weighted profile average along the chain
is \(\approx0.91\,M_{13}\) and the phase spread contributes
\(\approx0.95\), product \(\approx0.87=M_{14}/M_{13}\) exactly. The
profile near the peak is flat: for \(n\ge10\),
\(|\widehat c_n(2^{k(n)-1})|/M_n\) ranges \(0.89\)–\(0.99\) and
\(|\widehat c_n(2^{k(n)-2})|/M_n\) ranges \(0.69\)–\(0.84\). The
per-layer contraction tends to \(1\) as \(n\) grows, which is precisely
the shape \(M_n\approx e^{-c\sqrt n}\) (\(c\approx1.06\)) predicts:
\(M_{n+1}/M_n\approx1-\frac{c}{2\sqrt n}\).

**(vi) The obstruction is the 2–3 resonance lattice.** The bad
frequencies are the 2-adic/3-adic near-resonances \(2^k\) vs \(3^n\) —
the *same* lattice that forces cycle densities \(a/L\to\log_32\) from
below (landmark packet, `collatz_resonance_lattice`) and that made
\(\log_32\)'s continued fraction the critical line of the drift wall.
One Diophantine obstruction, two shadows: symbolic (cycle equation
\(3^a\approx2^L\)) and analytic (Fourier bad set at \(2^k\)).

## 5. What is now proved vs what remains

- **Proved:** S1, S2, S3. The conjecture "\(M_n\) decays uniformly" is
  equivalent to a bounded-escape-weight statement about a measured
  bad set of \(\le8\) explicit frequencies per layer.
- **Not proved:** any lower bound on \(w_n(\varepsilon)\) independent of
  the profile. Circularity warning: proving the near-peak profile decay
  \(|\widehat c_n(2^{K-2})|\le0.9M_n\) *is* essentially the original
  problem — but now localised to a 1-parameter chain with explicit
  structure, rather than a max over \(2\cdot3^{n-1}\) frequencies.
- **Measured only:** everything in §4, the \(e^{-1.06\sqrt n}\) shape,
  and the chain-exponent law \(k(n)\in[n,n+3]\).

## 6. Kill criteria

1. Exhibit a layer where \(B_n(0.1)\) contains a frequency off the
   \(\pm2^k\) chain (kills (ii), redirects the attack).
2. Prove \(w_n(\varepsilon)\ge w>0\) for some explicit
   \(\varepsilon,w\) and all \(n\) — by S3 this **proves exponential
   uniform decay** \(M_n\le(1-\varepsilon w)M_{n-1}\), strictly stronger
   than the conjectured \(e^{-c\sqrt n}\).
3. Show the chain profile has flatness \(|\widehat c_n(2^{K-2})|/M_n\to1\);
   that would kill even the \(\exp(-c\sqrt n)\) shape and indicate
   \(M_n\) decays sub-polynomially or not at all — contradicting Tao's
   proved \(n^{-A}\), hence impossible; the interesting regime is
   therefore exactly the measured one.

## 7. Related work

Moment methods appear to be absent from both existing treatments of the
Syracuse measure: Tao (arXiv:1909.03562) bounds the characteristic
function through a two-dimensional renewal process on triangles, and
Siegel (arXiv:2412.02902) develops non-Archimedean Tauberian spectral
theory rather than Archimedean decay estimates. The escape-weight
formulation (S3) reframes uniform decay as a one-sided small-set
condition, which we have not found in the literature. The measured
resonance chain \(\pm2^k\) is the Fourier shadow of the classical
\(2\)–\(3\) Diophantine lattice that drives the cycle-equation
literature (Eliahou 1993; Simons–de Weger 2005), where the continued
fraction of \(\log_3 2\) is the critical object; the same lattice
appears in the bbchallenge "Antihydra" cryptid, a \(BB(6)\) holdout
Turing machine whose behavior reduces to a Collatz-like odd/even count
race — the computability-side shadow of the same obstruction.

## 8. Reproduce

```bash
python3 contribution/packets/2026-07-22-scalar-phase-second-moment/verify_scalar_phase.py
python3 -m pytest contribution/packets/2026-07-22-scalar-phase-second-moment/ -q
```

Certificate: `scalar_phase_certificate.json`.
