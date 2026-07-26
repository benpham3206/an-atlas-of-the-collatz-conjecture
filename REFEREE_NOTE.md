# A factor-complexity obstruction for rational states of the Terras conjugacy

**Referee note.** 25 July 2026. Self-contained; assumes symbolic dynamics, assumes
nothing about this repository.

**One-line summary.** If an infinite binary word \(q\) is not eventually periodic and
the 2-adic state whose Terras parity transcript is \(q\) lies in \(\mathbb Q\cap\mathbb Z_2\),
then \(\limsup_k p_q(k)/k \ge 1/\log_2(3/2) = 1.7095\ldots\). The proof is one page.
The question for the referee is whether it is already in the literature.

---

## 1. The statement

**The map.** On the 2-adic integers \(\mathbb Z_2\), let

\[
T(x)=
\begin{cases}
x/2, & x\equiv 0 \pmod 2,\\
(3x+1)/2, & x\equiv 1 \pmod 2 .
\end{cases}
\]

This is Terras's accelerated form of the \(3x+1\) map; it is well defined on
\(\mathbb Z_2\) because parity is a continuous function there.

**Parity words.** The *parity transcript* of \(x\in\mathbb Z_2\) is
\(Q(x)=(q_0,q_1,\dots)\in\{0,1\}^{\mathbb N}\) with \(q_j \equiv T^j(x) \pmod 2\).

**The conjugacy \(\Phi\).** \(Q\) is a homeomorphism of \(\mathbb Z_2\) onto
\(\{0,1\}^{\mathbb N}\) (Terras 1976; Bernstein–Lagarias 1996). Write \(\Phi=Q^{-1}\).
Explicitly, if \(d_0<d_1<\cdots\) are the positions of the ones of \(q\), then

\[
\Phi(q)=-\sum_{j\ge 0}\frac{2^{d_j}}{3^{\,j+1}}\ \in\ \mathbb Z_2 ,
\]

the series converging 2-adically because \(3\) is a 2-adic unit and \(d_j\to\infty\).
\(\Phi(q)\) is the unique 2-adic integer with parity transcript \(q\). Equivalently,
with \(s_k=\sum_{t<k}q_t\), \(\ \Phi(q)=-\sum_{j\ge0} q_j 2^j/3^{s_{j+1}}\).

**Rational states.** \(\mathbb Q_{\mathrm{odd}} := \mathbb Q\cap\mathbb Z_2\), the rationals
with odd denominator; these are exactly the 2-adic integers with eventually periodic
binary expansion. Note \(\mathbb Z\subset\mathbb Q_{\mathrm{odd}}\), so anything proved
for \(\mathbb Q_{\mathrm{odd}}\) applies to ordinary integer Collatz orbits.

**Factor complexity.** \(p_q(k)=\#\{q_iq_{i+1}\cdots q_{i+k-1} : i\ge 0\}\).

> **Corollary 4.** Let \(q\in\{0,1\}^{\mathbb N}\) be not eventually periodic and suppose
> \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\). Then
> \[
> \limsup_{k\to\infty}\frac{p_q(k)}{k}\ \ge\ \kappa:=\frac{1}{\log_2(3/2)}=\frac{1}{\log_2 3-1}=1.7095112913\ldots
> \]

Two features to note before the proof. First, \(\kappa\) is **absolute**: it does not
depend on the rational \(\Phi(q)\), which enters only through an additive constant in
a length. Second, \(\kappa>1\), so the bound strictly improves the Morse–Hedlund floor
\(p_q(k)\ge k+1\) for aperiodic words; the words it excludes are exactly those of
"low linear" complexity, \(\limsup p_q(k)/k<1.7095\ldots\).

**Status of this section: proved.** Every claim above is a theorem, with proof below or
in the cited classical sources.

---

## 2. The proof

Write \(\Phi(q)=a/d\) with \(a\in\mathbb Z\), \(d\in\mathbb Z_{>0}\) odd. Put
\(x_j=T^j(a/d)\) and \(y_j=d\,x_j\). Since \(d\) is odd, each \(x_j\in\mathbb Q_{\mathrm{odd}}\)
has denominator dividing \(d\), so \(y_j\in\mathbb Z\), and \(y_j\equiv q_j\pmod 2\).
The dynamics becomes an integer recursion:

\[
y_{j+1}=\frac{3^{\,q_j}y_j+d\,q_j}{2},\qquad y_0=a. \tag{2.1}
\]

**Lemma 1 (equal factors force a congruence).** *If the length-\(k\) factors of \(q\)
beginning at positions \(i\) and \(j\) are equal, then \(y_i\equiv y_j \pmod{2^k}\).*

*Proof.* Iterating (2.1) along a **fixed** word \(w\in\{0,1\}^k\) with \(s\) ones composes
\(k\) affine maps whose composition depends only on \(w\) (and on \(d\)):
\(2^k y_{i+k}=3^{s}y_i+d\,c(w)\) for an integer \(c(w)\). The same identity holds at \(j\)
with the same \(w\), \(s\), \(c(w)\). Subtracting,
\(2^k\bigl(y_{i+k}-y_{j+k}\bigr)=3^{s}\bigl(y_i-y_j\bigr)\).
As \(3^s\) is odd, \(2^k \mid y_i-y_j\). \(\square\)

The only arithmetic input is that \(3\) is a 2-adic unit. The number of ones \(s\) cancels.

**Lemma 2 (height–complexity collision).** *Let \(H_N=\max_{0\le j\le N}|y_j|\). If \(q\) is
not eventually periodic and \(2^k>2H_N\), then \(p_q(k)\ge N+1\).*

*Proof.* Consider the \(N+1\) length-\(k\) factors beginning at \(0,1,\dots,N\). If two of
them coincide, Lemma 1 gives \(2^k\mid y_i-y_j\); but \(|y_i-y_j|\le 2H_N<2^k\), so
\(y_i=y_j\), hence \(x_i=x_j\) with \(i<j\). By determinism the orbit is periodic from
step \(i\) on, so \(q\) is eventually periodic — contradiction. Hence the \(N+1\) factors
are pairwise distinct. \(\square\)

Lemmas 1 and 2 are the easy half: pigeonhole plus a unit. The content of the corollary
is the *rate*, and it comes from the one nontrivial estimate:

**Growth bound.** From (2.1), in both cases,
\[
|y_{j+1}|+d\ \le\ \tfrac32\bigl(|y_j|+d\bigr).
\]
(If \(q_j=0\): \(|y_j|/2+d\le \tfrac32(|y_j|+d)\). If \(q_j=1\):
\(|y_{j+1}|+d\le (3|y_j|+d)/2+d=\tfrac32(|y_j|+d)\), with equality — the all-ones case.)
Hence \(|y_N|+d\le(3/2)^N(|a|+d)\), and since the right side increases in \(N\),

\[
H_N\ <\ (|a|+d)\,(3/2)^N. \tag{2.2}
\]

*Proof of Corollary 4.* Set
\(k_N=\bigl\lceil N\log_2(3/2)+\log_2\bigl(2(|a|+d)\bigr)\bigr\rceil+1\).
Then \(2^{k_N}>2(|a|+d)(3/2)^N>2H_N\) by (2.2), so Lemma 2 gives \(p_q(k_N)\ge N+1\).
Since \(k_N\to\infty\) and \(k_N/N\to\log_2(3/2)\),
\[
\limsup_{k\to\infty}\frac{p_q(k)}{k}\ \ge\ \limsup_{N\to\infty}\frac{N+1}{k_N}=\frac{1}{\log_2(3/2)}=\kappa. \qquad\square
\]

That is the entire proof. Note what it does **not** use: no Green/telescoped expansion of
\(y_L\), no discrepancy functional, no density hypothesis, no finite computation.

**Immediate consequence (Corollary 5).** A Sturmian word has \(p_q(k)=k+1\), so
\(\limsup p_q(k)/k=1<\kappa\). Hence **no Sturmian word is the Terras parity transcript
of any element of \(\mathbb Q_{\mathrm{odd}}\)** — in particular of any positive integer.
See §4 for what part of this is new.

**A refinement (Corollary 7).** If in addition every length-\(\ell\) factor of \(q\)
carries at most \(\beta\ell+C_0\) ones for some \(\beta>\alpha:=\log_3 2\), then the
growth bound (2.2) improves to \(H_N\le \mathrm{poly}(N)\cdot 2^{gN}\) with
\(g=\beta\log_2 3-1>0\), and the same argument gives
\(\limsup p_q(k)/k\ \ge\ 1/g=\alpha/(\beta-\alpha)\). Setting \(\beta=1\) recovers
Corollary 4. **Caveat:** the source memo states Corollary 7 without proof; the
reconstruction just sketched is mine and should be written out before publication.

---

## 3. Why this is not the drift wall

This is the crux. Everything previously known in this direction constrains a *frequency*;
Corollary 4 constrains a *complexity*. The two are different objects, obtained by
different mechanisms, and — decisively — they fail in different places.

**The frequency instruments.** Write \(s_L=\sum_{t<L}q_t\) and \(\alpha=\log_3 2=0.63092975\ldots\).
The known results are all of the form "a constraint on \(\liminf s_L/L\) forbids
\(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\)":

| result | statement | mechanism |
|---|---|---|
| Lagarias, Relation 2.31 | \(\liminf s_L/L\ge\alpha\) for divergent orbits | \(3^{s_L}/2^L\to 0\) forces descent |
| Monks–Yazinski, Thm 2.7(b) | same, for divergent **rationals** | same |
| López–Stoll 2021, Thm 1 | aperiodic \(q\) with \(\liminf s_L/L>\alpha\) \(\Rightarrow\Phi(q)\notin\mathbb Q_{\mathrm{odd}}\) | growth of \(3^{s_L}/2^L\) |

All three read only the multiplier \(M(0,L)=3^{s_L}/2^L=3^{\,s_L-\alpha L}\). That is a
function of the **abelianization** of the prefix — a one-dimensional statistic, and the
coarsest nontrivial one available on a binary word.

**Why they are jointly exhaustive, and jointly vacuous at one point.** Combining the
drift wall (\(\liminf<\alpha\) closed) with López–Stoll (\(\liminf>\alpha\) closed), a
divergent positive orbit must satisfy

\[
\liminf_{L\to\infty}\frac{s_L}{L}=\alpha \quad\text{exactly.}
\]

At that value \(3^{s_L-\alpha L}\) is subexponential in both directions and every
argument of the table above returns no information. The frequency instrument is
*exhausted by construction*: it has been pushed to both sides of its own threshold, and
the surviving case is the single critical value where it says nothing.

**The mechanism of Corollary 4 is different, and density-free.** It uses two inputs:

1. **Lemma 1**, which depends on \(3^s\) being a 2-adic *unit* — the exponent \(s\), i.e.
   the number of ones, cancels identically. Nothing about density can enter here.
2. **The growth bound (2.2)**, which is the *worst case over all words*: \(3/2\) is the
   per-step multiplier of the all-ones word. It therefore holds for every \(q\)
   regardless of its statistics, and \(\kappa=1/\log_2(3/2)\) is exactly the reciprocal of
   the logarithm of that worst-case multiplier.

Consequently the bound is **uniform in the density**. A word of any \(\liminf s_L/L\),
including \(\alpha\), satisfies it. Corollary 7 shows the expected monotonicity: knowing a
factorwise ones-cap \(\beta<1\) makes the bound *stronger* (\(\alpha/(\beta-\alpha)>\kappa\)),
so the density-free case \(\beta=1\) is the weakest and hence the universally admissible
one. At the critical density, where excursions above \(\alpha L\) are unbounded, \(\beta=1\)
is the only admissible cap, and Corollary 4 is what remains.

**On "strictly more information" — a correction.** The repository's internal notes say
factor complexity is "strictly more information" than letter frequency. That is not
right as stated, and a referee will catch it. The accurate statement is that the two
statistics are **logically independent**: for every irrational \(\theta\in(0,1)\) there is
a Sturmian word of density \(\theta\) with \(p_q(k)=k+1\), so no frequency hypothesis
implies any complexity bound; and \(p_q\) alone does not determine \(\liminf s_L/L\).
(The full factor *language* does constrain achievable densities — that is Corollary 7's
hypothesis — but the complexity *function* does not.) The correct claim, and the only one
needed, is: **Corollary 4 is not a consequence of any frequency result, and it is
non-vacuous at \(\liminf s_L/L=\alpha\), where all frequency results are vacuous.**

**What it does not do.** Corollary 4 does not close the critical case. High factor
complexity is a *necessary* condition it imposes; it does not by itself contradict
\(\Phi(q)\in\mathbb Z_{>0}\). Closing the gap needs a second instrument that *consumes*
high complexity rather than requiring it. The claim here is only that Corollary 4 is
currently the sole non-vacuous constraint at the critical density.

---

## 4. What is already known, and by whom

Stated plainly, because two of the three headline results in the source repository turned
out to be prior art.

- **The Terras bijection and the conjugacy.** R. Terras, *A stopping time problem on the
  positive integers*, Acta Arith. 30 (1976). D. J. Bernstein and J. C. Lagarias,
  *The 3x+1 conjugacy map*, Canad. J. Math. 48 (1996) — source of the periodicity
  conjecture (\(\Phi\) maps aperiodic words to irrational states), which is the framing
  conjecture for everything in this note.
- **The drift wall is prior art.** \(\liminf s_L/L\ge\alpha\) for a divergent orbit is
  Lagarias's Relation 2.31, and Monks–Yazinski, *The autoconjugacy of the 3x+1 function*,
  Thm 2.7(b), prove it for divergent **rationals**, which is strictly more general. The
  eliminations that follow from it — Thue–Morse, period-doubling, Rudin–Shapiro,
  paperfolding, Champernowne, all Borel-normal words — are therefore also not new.
- **The supercritical side is prior art.** J. López and P. Stoll, *The 3x+1 periodicity
  conjecture in \(\mathbb R\)*, [arXiv:2101.12747](https://arxiv.org/abs/2101.12747) (2021),
  Thm 1. Their abstract also states the consequence that a rational 2-adic integer with a
  non-cyclic trajectory necessarily has \(\liminf h/\ell=\ln 2/\ln 3\), i.e. the critical
  density above.
- **Corollary 5 is new only at one slope.** A Sturmian word of slope \(\theta\) has letter
  density exactly \(\theta\). López–Stoll 2021 kills every \(\theta>\alpha\) and
  Monks–Yazinski every \(\theta<\alpha\). Corollary 5 is therefore new **only at
  \(\theta=\alpha=\log_3 2\)** (irrational, hence a legitimate Sturmian slope). The
  Fibonacci and golden-angle codings have slope \(1/\varphi^2\approx0.382<\alpha\) and
  were already excluded. Corollary 5 should be presented as a corollary of Corollary 4 at
  one exceptional slope, never as a headline. Note that López–Stoll's earlier Sturmian
  paper (*The 3x+1 conjugacy map over a Sturmian word*, INTEGERS 9 (2009) A13) does **not**
  prove it; it gives a 2-adic continued-fraction expansion and says explicitly that the
  aperiodic-to-rational question is open.
- **Complexity background.** \(p_q(k)\ge k+1\) for aperiodic words and \(p_q(k)=k+1\)
  characterizing Sturmian words: Morse–Hedlund 1940.
- **The computable complexity bound ("Lemma D") is folklore.** The repository's
  desubstitution bound \(\limsup_n p_u(n)/n \le \max_{m_0\le m\le k m_0} p_u(m{+}1)/(m{-}1)\)
  for a fixed point of a \(k\)-uniform morphism is the textbook argument; Allouche &
  Shallit, *Automatic Sequences* (2003), **Thm 10.3.1** already gives an effective bound
  for \(k\)-automatic sequences. See also Cassaigne (1997) for exact computation via
  bispecial factors and Klouda, TCS (2013), for computable bounds on primitive
  substitution fixed points. Only the \(m_0\)-parametrized packaging appears unstated, and
  a referee would call that folklore too.
- **Ancillary classical inputs used by the computational side:** Cobham (1972) for
  rationality of automatic densities, Gelfond–Schneider for transcendence of \(\log_3 2\),
  Fekete for subadditivity, Queffélec, *Substitution Dynamical Systems* §5, for unique
  ergodicity of primitive substitution subshifts.

**Measured, not proved.** The application of Corollary 4/7 to a 126-word sweep of
primitive uniform morphisms closed 116, of which the 109-word subset matching an earlier
enumeration gave 99. Those numbers are exact-integer computations with a deterministic
certificate — but the *conclusion* for all of them is subsumed by López–Stoll 2021, since
every word in the sweep has rational density \(\rho>\alpha\). What survives there is the
machinery, not the result.

---

## 5. The exact questions for the referee

1. **Is Corollary 4 known?** Is there a published lower bound on the factor complexity of
   parity words of rational states of the \(3x+1\) conjugacy — in the Bernstein–Lagarias
   line, in López and Stoll's own reference lists, or in the base-\(3/2\) representation
   literature? A negative search covering López–Stoll (2009, 2021), Bernstein–Lagarias
   (1996), Monks–Yazinski, and Lagarias's overview and both annotated bibliographies
   found nothing, but MathSciNet was not consulted.

2. **Is the mechanism known under another name?** "Repeated factor \(\Rightarrow\)
   congruence mod \(2^k\) (Lemma 1), combined with affine state growth, pigeonholed into a
   complexity lower bound." This looks like the standard argument used to bound complexity
   of automatic/\(b\)-expansion sequences and in the transcendence literature (Adamczewski–Bugeaud
   style complexity-vs-approximation arguments). Is it the same argument in different
   clothing? If so, does the existing form already give the constant?

3. **Is the constant recognizable?** \(\kappa=1/\log_2(3/2)=1/(\log_2 3-1)=\alpha/(1-\alpha)=1.7095112913\ldots\).
   Does this number appear anywhere in the \(3x+1\) or symbolic-dynamics literature?

4. **Is the critical-density reduction stated anywhere?** "A divergent orbit has
   \(\liminf s_L/L=\log_3 2\) exactly" follows from Monks–Yazinski plus López–Stoll 2021,
   and López–Stoll state the rational version in their abstract. Has anyone written it
   down for divergent positive integers as the definition of the remaining gap, and if so
   has anyone attacked it with a non-abelian statistic?

---

## 6. Status

**Provisional novelty only.** A negative literature search performed by an AI agent is
not a priority claim, and should not be treated as one. The search behind §4 was run once,
on 2026-07-25, after the results were written; it retired two of the repository's three
headline claims. MathSciNet was not accessible, no review-database search was performed,
and the post-2021 literature was not swept systematically. López–Stoll 2021 is
load-bearing for the subsumption findings in §4 and its full text has not been read by a
human in this project.

What is **proved** here: Lemma 1, Lemma 2, the growth bound, Corollary 4, Corollary 5.
Corollary 7 is stated in the source without proof; §2 sketches one.
What is **measured**: the sweep numbers in §4, exact-integer with certificates.
What is **asserted**: that Corollary 4 is new, and that it is the only non-vacuous
instrument at the critical density. The second assertion is only as strong as the claim
that all prior instruments are frequency-based — which §3 argues but does not exhaust.

The result is a small, clean, possibly-known lemma. Its interest is entirely positional:
after López–Stoll 2021, the remaining case is a single critical density at which every
frequency argument is vacuous, and this is the one instrument that still says something
there.
