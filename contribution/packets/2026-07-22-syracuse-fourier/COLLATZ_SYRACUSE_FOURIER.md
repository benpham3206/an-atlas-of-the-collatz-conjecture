# Syracuse Fourier analysis: an exact recursion, exponential L² mixing, and the precise spectral barrier to "all"

**Date:** 22 July 2026
**Status:** three proved statements + one computed barrier. **Not** a
proof of the conjectured \(\exp(-c\sqrt n)\) decay, **not** a stronger
density theorem than Tao's, **not** Collatz progress per se. It isolates,
with a number, exactly where the analytic route from "almost all" to
"all" is blocked. No literature-priority claim: the recursion is
implicit in Tao's Lemma 1.12 and the mass bound is likely folklore; the
packet makes them explicit and machine-verified.

**Companion executable evidence:** `verify_syracuse_fourier.py`,
`test_verify_syracuse_fourier.py`, `syracuse_fourier_certificate.json`.

Notation follows the tao-structural-refinement packet:
\(\mathrm{Syrac}(\mathbb Z/3^n\mathbb Z)\) is the \(n\)-Syracuse offset
distribution; \(P_n\) its mass function;
\(\widehat c_n(\xi)=\mathbb E\,e(-\xi\mathrm{Syrac}(\mathbb Z/3^n\mathbb
Z)/3^n)\) its characteristic function, \(e(t)=e^{2\pi it}\);
\(r_n=\max_x P_n(x)\).

---

## 1. Theorem 1 — exact characteristic-function recursion

**Statement.** For \(n\ge0\) and \(\xi\in\mathbb Z/3^{n+1}\mathbb Z\),

\[
\boxed{
\widehat c_{n+1}(\xi)
=
\sum_{a\ge1}2^{-a}\,
e\!\left(-\frac{\xi\, u_a}{3^{n+1}}\right)
\widehat c_n\bigl(\xi\, u_a\bmod 3^n\bigr),
\qquad
u_a=2^{-a}\bmod 3^{n+1}.
}
\tag{1.1}
\]

**Proof.** From the definition of the offset map,
\(F_{n+1}(a_1,\ldots,a_{n+1})
=2^{-a_1}\bigl(1+3F_n(a_2,\ldots,a_{n+1})\bigr)\)
(direct from \(F_n=\sum_m3^{n-m}2^{-a[m,n]}\)). Hence, distributionally,

\[
\mathrm{Syrac}(\mathbb Z/3^{n+1}\mathbb Z)
\equiv
2^{-a}\bigl(1+3\,\mathrm{Syrac}(\mathbb Z/3^n\mathbb Z)\bigr)
\pmod{3^{n+1}},
\]

with \(a\equiv\mathrm{Geom}(2)\) independent of the second factor.
(This is the stationary Markov move \(x\mapsto(3x+1)/2^a\) of Tao's
Remark 1.13.) Taking characteristic functions: the factor
\(e(-\xi u_a\cdot3X_n/3^{n+1})\) depends on \(X_n\) only through
\(\xi u_a\bmod 3^n\). \(\square\)

**Magnitude form.** With \((Tf)(\xi)=\sum_a2^{-a}f(\xi u_a\bmod3^n)\),

\[
|\widehat c_{n+1}(\xi)|\le (T|\widehat c_n|)(\xi).
\tag{1.2}
\]

The phases \(e(-\xi u_a/3^{n+1})\) discarded in (1.2) are where any
uniform bound must find cancellation. Verified to \(5\times10^{-17}\)
against FFT at \(n=3,5,9\) (see certificate).

## 2. Lemma 2 — parity-class contraction of the maximum mass

**Statement.**

\[
r_{n+1}\le\frac{2}{3}\left(1-2^{-2\cdot3^n}\right)^{-1}r_n,
\qquad\text{hence}\qquad
\boxed{
r_n\le C\,(2/3)^n,\quad
C=\prod_{j\ge1}\left(1-2^{-2\cdot3^j}\right)^{-1}<1.032.
}
\tag{2.1}
\]

**Proof.** Lemma 1.12 of Tao: for \(x\not\equiv0\pmod3\),

\[
P_{n+1}(x)
=
\left(1-2^{-2\cdot3^n}\right)^{-1}
\sum_{\substack{1\le a\le2\cdot3^n\\2^ax\equiv1\,(3)}}
2^{-a}P_n\!\left(\tfrac{2^ax-1}3\bmod3^n\right),
\]

and \(P_{n+1}(x)=0\) for \(3\mid x\). The condition \(2^ax\equiv1\pmod3\)
restricts \(a\) to one parity class: odd \(a\) if \(x\equiv2\), even
\(a\) if \(x\equiv1\). The weights sum to at most
\(\sum_{a\text{ odd}}2^{-a}=2/3\) (respectively \(1/3\)), and every
summand is at most \(r_n\). \(\square\)

**Remark.** Numerically the true ratio tends to \(1/2\)
(certificate: \(r_{n+1}/r_n\to0.500\) by \(n=10\)), so (2.1) is
within one parity class of optimal.

## 3. Corollary 3 — exponential L² Fourier mixing (proved)

Parseval and (2.1):

\[
\boxed{
\frac1{3^n}\sum_{\xi\in\mathbb Z/3^n\mathbb Z}|\widehat c_n(\xi)|^2
=
\sum_xP_n(x)^2
\le r_n
\le 1.032\,(2/3)^n,
}
\tag{3.1}
\]

i.e. the root-mean-square of \(\widehat c_n\) over **all** frequencies
decays like \((2/3)^{n/2}=0.81650\ldots^n\) — exponential, unconditional,
and uniform in nothing. Verified numerically to \(n=14\).

## 4. Theorem 4 — the spectral barrier, as a number

The uniform question — \(\max_{3\nmid\xi}|\widehat c_n(\xi)|\) — is
governed by iterating (1.2). \(T\) acts on frequencies, and on
\((\mathbb Z/3^n\mathbb Z)^*\) the map \(\xi\mapsto\xi u_a\) is
multiplication by \(2^{-a}\). Since \(2\) is a primitive root mod
\(3^n\) (verified \(n\le6\)), \((\mathbb Z/3^n\mathbb
Z)^*\cong\mathbb Z/N\mathbb Z\) with \(N=2\cdot3^{n-1}\), and the
frequency walk is the additive walk \(t\mapsto t-a\) on
\(\mathbb Z/N\mathbb Z\). Its eigenvalues are

\[
\mu_\ell
=
\sum_{a\ge1}2^{-a}e\!\left(\tfrac{2\pi i\ell a}{N}\right)
=
\frac{z}{2-z},
\qquad
|\mu_\ell|
=
\frac1{\sqrt{\,5-4\cos(2\pi\ell/N)\,}},
\quad
z=e^{2\pi i\ell/N}.
\tag{4.1}
\]

The top nontrivial eigenvalue (\(\ell=1\)) is

\[
\boxed{
|\mu_1|
=
1-\frac{\pi^2}{2\cdot9^{\,n-1}}
+O\!\left(9^{-2n}\right),
}
\tag{4.2}
\]

so the frequency walk needs \(\Theta(9^n)\) steps to equidistribute —
while only \(n\) layers are available. **Therefore the route "L² bound +
spectral equidistribution of the frequency walk ⇒ uniform max decay" is
structurally blocked**: it cannot yield any decay of
\(\max_\xi|\widehat c_n|\) within \(n\) layers, let alone the measured
\(\exp(-c\sqrt n)\). Moreover, L² alone cannot even recover Tao's
Proposition 1.14: Cauchy–Schwarz on \(\mathrm{Osc}_{m,n}\) against
(3.1) loses a factor \(3^{(n-m)/2}\), giving a *growing* bound
\(\lesssim2^{n/2}\).

What remains as the only viable mechanism for the uniform bound is the
scalar-phase cancellation in (1.1) — the discarded factors
\(e(-\xi u_a/3^{n+1})\) — which is precisely the content of Tao's §7
two-dimensional renewal geometry. Any proof of the conjectured
\(\exp(-c\sqrt n)\) (measured: \(c\approx1.06\)) must extract
cancellation there, not from equidistribution.

## 5. What this buys the "almost all → all" program

1. A **cleaner formulation** of the problem's analytic heart: one exact
   recursion (1.1), replacing the renewal-process picture at the level
   of definitions.
2. **Exponential L² mixing for free** (Corollary 3) — the strongest
   unconditional Fourier statement in the packet, with an explicit
   constant.
3. **The exact barrier** (4.2): the obstruction to upgrading "almost
   all" along the Fourier route is a spectral gap of
   \(\pi^2/(2\cdot9^{n-1})\) in the frequency walk — not a vague
   difficulty but a computed quantity, mirroring how the symbolic route
   is blocked at the lift digits of \(q^*\). Both routes are now
   blocked at named, quantified walls.

## 6. Kill criteria and exact boundary

- Lemma 2 dies if a layer violates \(r_{n+1}\le(2/3)(1-2^{-2\cdot3^n})^{-1}r_n\);
  the verifier checks every computed layer (the proof, not the check, is
  the theorem).
- Theorem 4 is a barrier statement about a *proof route*, not about the
  truth of \(\exp(-c\sqrt n)\); a direct attack on the scalar phases
  bypasses it legitimately.
- Nothing here strengthens Tao's density statement or re-proves his
  Proposition 1.17. The measured \(\exp(-1.06\sqrt n)\) remains a
  hypothesis generated by float64 data at \(n\le14\).

## 7. Reproduce

```bash
python3 contribution/packets/2026-07-22-syracuse-fourier/verify_syracuse_fourier.py
python3 -m pytest contribution/packets/2026-07-22-syracuse-fourier/ -q
```

Certificate: `syracuse_fourier_certificate.json`.
