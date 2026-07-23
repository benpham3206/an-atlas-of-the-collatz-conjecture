# Pointwise drift wall — subcritical aperiodic words are not positive-integer Collatz states

**Date:** 22 July 2026
**Status:** proved deduction, pointwise, no density or randomness assumptions.
This memo is **not** a proof of the Collatz conjecture and **not** a
counterexample. It adds one atomic exclusion lemma with a number in it —
the critical drift \(\alpha=\log_3 2\) — that needs **no structural
hypothesis** on the parity word, and combines it with the packet's
complexity-pressure theorem into a two-wall screen for every possible
counterexample transcript. No literature-priority claim is made.

**Companion executable evidence:** `verify_drift_wall.py`,
`test_verify_drift_wall.py`, `verify_drift_wall.out`,
`drift_wall_certificate.json`.

---

## 1. Setup

Terras map on \(\mathbb Z_{>0}\):

\[
T(x)=
\begin{cases}
x/2,&x\equiv0\pmod2,\\
(3x+1)/2,&x\equiv1\pmod2.
\end{cases}
\]

For an orbit \(x_{j+1}=T(x_j)\), \(x_0=n\), write
\(q_j=x_j\bmod 2\) for its parity word and

\[
s_L=\sum_{j=0}^{L-1}q_j,\qquad
\alpha=\log_3 2=0.6309297535\ldots,\qquad
\kappa=\frac1{\log_2(3/2)}=1.7095112913\ldots .
\]

\(\Phi(q)\in\mathbb Z_2\) is the inverse Terras conjugacy of
`PARTIAL_THEOREMS.md` Theorem 2: \(q\) is the parity transcript of a
positive integer iff \(\Phi(q)\in\mathbb Z_{>0}\).

---

## 2. Lemmas

### Lemma 1 — exact multiplicative expansion

For every \(L\ge0\),

\[
\boxed{
x_L
=
n\,\frac{3^{s_L}}{2^{L}}
\prod_{\substack{0\le j<L\\q_j=1}}
\left(1+\frac1{3x_j}\right).
}
\tag{2.1}
\]

**Proof.** Induction on \(L\). Even step: \(x_{j+1}=x_j/2\), absorbing one
factor \(1/2\) and no correction. Odd step:

\[
x_{j+1}=\frac{3x_j+1}{2}
=\frac32\,x_j\left(1+\frac1{3x_j}\right).
\]

Multiplying the per-step identities gives (2.1). \(\square\)

Every factor of the correction product is \(>1\), and each factor is
\(\le 4/3\) because \(x_j\ge1\).

### Lemma 2 — divergence kills the correction Cesàro mean

If \(x_j\to\infty\), then \(c_j=q_j\log(1+1/(3x_j))\to0\), hence

\[
\frac1L\sum_{j=0}^{L-1}c_j\longrightarrow0.
\]

**Proof.** \(0\le c_j\le\log(1+1/(3x_j))\) and \(x_j\to\infty\), so
\(c_j\to0\); Cesàro means of a null sequence are null. \(\square\)

### Lemma 3 — unconditional upper envelope

For every \(L\ge0\),

\[
\boxed{
x_L\le n\,2^{\,2s_L-L}.
}
\tag{2.2}
\]

In particular, if \(s_L\le\beta L\) for all \(1\le L\le L^*\) with
\(\beta<1/2\), then \(L^*\le\bigl\lceil\log_2 n/(1-2\beta)\bigr\rceil\):
every positive orbit violates any uniform half-density cap within an
explicitly bounded number of steps.

**Proof.** Odd step with \(x_j\ge1\): \((3x_j+1)/2\le2x_j\). Even step:
\(x_j/2\). Multiplying gives \(x_L\le n\,2^{s_L}2^{-(L-s_L)}\). If
\(s_L\le\beta L\) throughout, then
\(x_L\le n\,2^{(2\beta-1)L}<1\) as soon as
\(L>\log_2 n/(1-2\beta)\), contradicting \(x_L\in\mathbb Z_{>0}\).
\(\square\)

---

## 3. Theorem 1 — pointwise drift wall

**Statement.** If the Terras orbit of \(n\in\mathbb Z_{>0}\) diverges,
\(x_j\to\infty\), then its parity word satisfies

\[
\boxed{
\liminf_{L\to\infty}\frac{s_L}{L}\ \ge\ \log_3 2\ =\ \alpha.
}
\tag{3.1}
\]

**Proof.** Suppose \(\liminf s_L/L<\alpha\). Choose \(\beta\) with
\(\liminf s_L/L<\beta<\alpha\) and a subsequence \(L_i\to\infty\) with
\(s_{L_i}\le\beta L_i\). Taking logarithms in (2.1),

\[
\log x_{L_i}
\le
\log n+L_i\bigl(\beta\log 3-\log 2\bigr)+\sum_{j<L_i}c_j.
\]

Because \(\beta<\alpha=\log_3 2\), the coefficient
\(\beta\log3-\log2\) is a fixed negative number. By Lemma 2 the final
sum is \(o(L_i)\). Hence \(\log x_{L_i}\to-\infty\), so \(x_{L_i}\to0\),
contradicting \(x_{L_i}\ge1\). \(\square\)

The argument is exact and pointwise. No independence, equidistribution,
or typicality assumption enters; divergence is used only to force the
correction Cesàro mean to zero.

---

## 4. Theorem 2 — subcritical realizability obstruction

**Statement.** Let \(q\in\{0,1\}^{\mathbb N}\) be **not eventually
periodic** and satisfy

\[
\liminf_{L\to\infty}\frac{s_L(q)}{L}<\log_3 2.
\]

Then

\[
\boxed{\Phi(q)\notin\mathbb Z_{>0}.}
\tag{4.1}
\]

**Proof.** Assume \(\Phi(q)=n\in\mathbb Z_{>0}\). By the uniqueness half
of the realizability criterion (`PARTIAL_THEOREMS.md` Theorem 2), \(q\)
is the parity transcript of the orbit of \(n\). That orbit is not
eventually periodic, for an eventually periodic orbit has an eventually
periodic parity word. A positive-integer orbit that is not eventually
periodic cannot be bounded — a bounded positive orbit repeats a state
and cycles — so it diverges. Theorem 1 then gives
\(\liminf s_L/L\ge\alpha\), contradicting the hypothesis. \(\square\)

**Strength and scope, stated exactly.** The conclusion
\(\Phi(q)\notin\mathbb Z_{>0}\) is weaker than the
\(\Phi(q)\notin\mathbb Q_{\mathrm{odd}}\) conclusion of
`PRIMITIVE_UNIFORM_OBSTRUCTION.md`. In exchange, the hypothesis is
empty of structure: \(q\) need not be substitutive, automatic, morphic,
Toeplitz, recurrent, or uniquely ergodic. Where both theorems apply
(primitive uniform fixed points with \(\beta<\alpha\)), the older
theorem is strictly stronger and this one is a consistency check. Everywhere
else — non-uniform morphisms, automatic sequences known only through a
coding, normal words, ad hoc aperiodic words — this theorem is the first
applicable wall, because it consumes only a one-density liminf.

---

## 5. Corollary — the two-wall screen for any counterexample transcript

Let \(q\) be the parity transcript of a Collatz counterexample. Then
exactly one of the following holds.

**(Cycle branch).** \(q\) is periodic with \(a\) ones per period of
length \(L\),

\[
\frac aL<\alpha,
\qquad
a>18
\quad(\text{and }a>1.375\times10^{11}\text{ by Hercher--Ba\v{r}ina}),
\]

with \(a/L\) a near-neutral approximant to \(\alpha\) from below.

**(Divergence branch).** \(q\) is not eventually periodic and

\[
\boxed{
\liminf_L\frac{s_L}L\ge\alpha
\quad\text{and}\quad
\limsup_k\frac{p_q(k)}k\ge\kappa=1.709511\ldots
}
\tag{5.1}
\]

simultaneously; if in addition its critical block discrepancy is
bounded, its factor entropy is full.

**Proof.** Cycle branch: a period with \(a\) ones and length \(L\) acts
affinely as \(2^Lx=3^ax+C\) with \(C\) a positive integer (sum of
positive branch offsets), so a positive fixed state forces
\(2^L-3^a=C/x>0\), i.e. \(a/L<\log_3 2\). The count \(a>18\) is the
verified box of `EXACT_COUNTEREXAMPLE_SEARCH.md`. Divergence branch:
Theorem 1 above for the drift wall, and Corollary 4 (equation 5.1) of
`COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md` for the complexity
wall; the bounded-discrepancy addendum is its Corollary 6. \(\square\)

The critical line \(\alpha\) is therefore approached from **both** sides
and from nowhere else: cycles are rational densities strictly below
\(\alpha\) (constrained to continued-fraction near-resonances
\(3^a\approx2^L\)), divergent orbits are liminf densities at or above
\(\alpha\).

---

## 6. Named-class eliminations

Each entry is aperiodic; each density is a classical exact value. One
certified comparison suffices for all: \(63/100<\log_3 2\) because
\(3^{63}<2^{100}\), and every listed density is \(\le 1/2\).

| Transcript class | one-density | killed by | note |
|---|---|---|---|
| Thue–Morse | \(1/2\) | drift wall | also \(\notin\mathbb Q_{\mathrm{odd}}\) by primitive-uniform obstruction |
| Period-doubling | \(1/3\) | drift wall | also \(\notin\mathbb Q_{\mathrm{odd}}\) ibid. |
| Rudin–Shapiro | \(1/2\) | drift wall | **new**: automatic but not a pure primitive-uniform fixed point; complexity slope \(8\) is useless here — drift kills it |
| Regular paperfolding | \(1/2\) | drift wall | **new**: same reason; slope \(4\) cannot save it |
| Fibonacci word | \(2-\varphi=0.3819\ldots\) | drift wall | Sturmian; also killed by complexity wall |
| Sturmian, slope \(\theta<\alpha\) | \(\theta\) | drift wall | **new half** of the Sturmian kill |
| Sturmian, slope \(\theta\ge\alpha\) | \(\theta\) | complexity wall | packet Corollary 5; slope \(1<\kappa\) |
| Binary Champernowne | \(1/2\) | drift wall | **new**: full entropy, maximal complexity — invisible to the complexity wall |
| Any Borel-normal word | \(1/2\) | drift wall | **new**: no normal word is a divergent Collatz transcript |
| Quasi-Sturmian (\(p(k)=k+c\)) | any | complexity wall | slope \(1<\kappa\) |

The last row and the Sturmian rows together exhaust the classical
subcritical-complexity zoo; the normal-word row shows the drift wall
reaches where the complexity wall cannot. The surviving region of
\(\{0,1\}^{\mathbb N}\) — words with liminf one-density \(\ge0.6309\)
**and** complexity slope \(\ge1.7095\) — contains no classical named
aperiodic word known to this project.

---

## 7. Kill criteria and exact boundary

**Kill criteria for this memo.**

1. Exhibit a divergent positive orbit whose parity word has certified
   \(\liminf s_L/L<\log_3 2\). (That would also be a Collatz
   counterexample.)
2. Exhibit an aperiodic word with \(\liminf s_L/L<\alpha\) whose
   \(\Phi(q)\) is a positive integer. (Same.)
3. Find an error in Lemmas 1–3; the verifier checks (2.1) and (2.2) on
   exact rational orbits.

**What this memo does not do.**

- It does not prove Collatz and does not touch supercritical words.
- It does not exclude \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\setminus\mathbb Z\)
  for subcritical aperiodic \(q\) (the primitive-uniform theorem does
  more, on a smaller class).
- It says nothing about cycles beyond restating the known
  \(a/L<\alpha\) arithmetic.
- Finite prefix densities computed by the verifier are **controls**, not
  the theorem; the proof carries the infinite conclusion.
- The density values in §6 are classical exact results quoted from the
  standard literature (Allouche–Shallit, *Automatic Sequences*); the
  verifier confirms them on long finite prefixes as a sanity control.

**Position in the program.** This is the left half of the target
dichotomy (9.1) of the landmark memo, populated on the drift axis
instead of the complexity axis: *permanent non-descent forces
\(\liminf\)-supercritical one-density.* The remaining leap is unchanged:
a supercritical, high-complexity word whose ordinary lift digits are
nevertheless eventually zero.

---

## 8. Reproduce

```bash
python3 contribution/packets/2026-07-22-pointwise-drift-wall/verify_drift_wall.py
python3 -m pytest contribution/packets/2026-07-22-pointwise-drift-wall/test_verify_drift_wall.py -q
```

Certificate: `drift_wall_certificate.json` (deterministic content,
regenerated by the verifier).
