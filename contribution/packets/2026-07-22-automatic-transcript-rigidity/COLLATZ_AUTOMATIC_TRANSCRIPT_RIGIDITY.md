# Automatic transcript rigidity: the subcritical and critical strata are closed, the supercritical stratum is provably the whole gap

**Date:** 22 July 2026
**Status:** five proved statements (Lemmas A–C, Theorems 1–4) + one exact
counterexample hunt over all small 2-automatic words. **Not** a proof of
the Collatz conjecture, **not** a counterexample, and **not** a proof of
the full 2-automatic rigidity conjecture: the supercritical stratum of
the 2-automatic class is shown to be nonempty and exactly equivalent to
"a divergent Collatz orbit with a 2-automatic parity word". The rigidity
theorem is proved for every 2-automatic word outside that stratum. No
literature-priority claim is made.

**Companion executable evidence:** `verify_automatic_rigidity.py`,
`test_verify_automatic_rigidity.py`, `verify_automatic_rigidity.out`,
`automatic_rigidity_certificate.json`.

---

## 1. Setup

Terras map \(T\) and parity words as in the drift-wall packet. For
\(q\in\{0,1\}^{\mathbb N}\) with one-positions \(d_0<d_1<\cdots\),

\[
\Phi(q)=-\sum_{j\ge0}\frac{2^{d_j}}{3^{j+1}}\in\mathbb Z_2,
\qquad
q\text{ realized by a positive orbit}\iff \Phi(q)\in\mathbb Z_{>0},
\]

the exact realizability criterion of `PARTIAL_THEOREMS.md` Theorem 2.
Write \(s_L(q)=\sum_{j<L}q_j\) and \(\alpha=\log_3 2=0.6309297\ldots\).

A word \(q\) is **2-automatic** if it is produced by a DFAO reading the
binary expansion of the index; equivalently (Cobham) if it is a letter-to-letter
coding of a fixed point of a uniform length-2 morphism. The drift wall
(packet 1, Theorems 1–2) is quoted throughout: divergent positive orbits
have \(\liminf s_L/L\ge\alpha\), and aperiodic words with
\(\liminf s_L/L<\alpha\) have \(\Phi(q)\notin\mathbb Z_{>0}\).

---

## 2. Kill criteria (stated before everything else)

1. Exhibit a 2-automatic, not eventually periodic word \(q\) with
   \(\Phi(q)\in\mathbb Z_{>0}\). This kills the rigidity conjecture — and
   is simultaneously a Collatz counterexample (a divergent orbit). The
   hunt below searched and found none.
2. Exhibit a 2-automatic word whose natural one-density equals
   \(\alpha\) exactly. This kills Theorem 2 — and also
   Gelfond–Schneider, since automatic densities are rational (Lemma B).
3. Exhibit a primitive uniform fixed point whose measured letter
   frequencies deviate from the rational Perron eigenvector beyond
   float64 tolerance; this kills the cited half of Lemma B.
4. Find an error in the exact integer comparisons \(3^a\lessgtr 2^b\) on
   which every density classification rests; the verifier recomputes all
   of them (and \(3^a\neq2^b\) for \(1\le a,b\le500\)).
5. Exhibit any inconsistency between the \(\Phi\)-engine and true Terras
   orbits; the verifier cross-checks
   \(\Phi(\text{transcript of }n)\equiv n\pmod{2^{64}}\) for
   \(1\le n\le2000\).

Kill criterion 2 cannot fire without a mathematical revolution; criteria
3–5 are engineering checks that all pass; criterion 1 is the conjecture
itself and remains **open on the supercritical stratum** (Theorem 3 shows
this is not an artifact of weak walls).

---

## 3. Lemma A — \(\log_3 2\) is transcendental (PROVED)

**Proof.** \(\log_3 2\) is irrational: \(\log_3 2 = a/b\) with positive
integers would give \(2^b = 3^a\), contradicting unique factorization
(the verifier checks \(2^b\neq3^a\) for \(1\le a,b\le500\) as a control).
Suppose \(\beta=\log_3 2\) were algebraic irrational. By the
Gelfond–Schneider theorem, for algebraic \(\gamma\notin\{0,1\}\) and
algebraic irrational \(\beta\), every value of \(\gamma^\beta\) is
transcendental. Taking \(\gamma=3\): \(3^\beta = 3^{\log_3 2} = 2\)
would be transcendental — but \(2\) is algebraic. Contradiction.
\(\square\)

**Consequence used everywhere.** For \(a/b\in\mathbb Q\) in lowest
terms, \(a/b<\alpha\iff 3^a<2^b\), an exact integer comparison; equality
\(a/b=\alpha\) never occurs. The verifier performs **every** density
classification in the certificate with this comparison and no floating
point.

## 4. Lemma B — automatic frequencies are rational (PROVED modulo the classical existence half)

**Statement.** Let \(\sigma\) be a primitive uniform morphism of length
\(\ell\) on an alphabet \(A\), \(u\) a fixed point, \(\tau:A\to\{0,1\}\)
a coding, \(q=\tau(u)\). Then the natural one-density
\(\rho(q)=\lim_L s_L(q)/L\) exists and is rational.

**Proof.** Existence of letter frequencies for primitive substitutions,
and their identification with the normalized right Perron eigenvector of
the incidence matrix \(M\), is the standard Perron–Frobenius theory of
substitutions (Allouche–Shallit, *Automatic Sequences*, §8.4; Queffélec,
*Substitution Dynamical Systems*, §5) — this is the cited half. For
rationality (proved here): \(M\) has integer entries and every column sum
equals \(\ell\), so \((1,\ldots,1)M=\ell(1,\ldots,1)\); hence \(\ell\) is
an eigenvalue of \(M\), and since the spectral radius is at most the
maximal column sum \(\ell\), \(\ell\) is the Perron eigenvalue. The
frequency vector \(v\) satisfies \((M-\ell I)v=0\); but \(M-\ell I\) is a
*singular integer* matrix, so its null space is defined over
\(\mathbb Q\) and \(v\), being proportional to a rational null vector,
has rational components. Coding sums rationals. \(\square\)

The verifier computes \(v\) exactly with `Fraction` arithmetic for every
primitive morphism in the enumeration (binary \(\ell\le4\), ternary
\(\ell=2\)), verifies \((M-\ell I)v=0\) exactly, and checks the prefix
frequency against \(v\) numerically as a control.

**Cited strengthening (Cobham).** For arbitrary \(k\)-automatic
sequences, a letter frequency that exists is rational (Cobham, *Uniform
tag sequences*, 1972; Allouche–Shallit, Thm 8.4.5). Lemma B is the
self-contained primitive case; Cobham's theorem is used only to extend
Theorem 1 to automatic words outside the primitive-morphism presentation.

## 5. Theorem 1 — the automatic rigidity trichotomy (PROVED)

**Statement.** Let \(q\in\{0,1\}^{\mathbb N}\) be 2-automatic with
\(\Phi(q)\in\mathbb Z_{>0}\). Then exactly one of the following holds.

- **(P)** \(q\) is eventually periodic. Then the orbit of \(\Phi(q)\)
  enters a Collatz cycle (the eventual period — not necessarily
  \(\Phi(q)\) itself, e.g. \(\Phi(000(10)^\omega)=8\) — lies on it):
  the period has \(a\) ones in length \(L\) with \(a/L<\alpha\), and
  either it is the trivial cycle (\(a=1\), \(\Phi\in\{1,2\}\)) or it is
  nontrivial with \(a>1.375\times10^{11}\) (Hercher–Bařina).
- **(S)** \(q\) is aperiodic and
  \(\liminf_L s_L(q)/L\ge\alpha\). If moreover the natural one-density
  \(\rho(q)\) exists, then \(\rho(q)\in\mathbb Q\) and
  \(\rho(q)>\alpha\) strictly.

**Proof.** \(\Phi(q)=n\in\mathbb Z_{>0}\) makes \(q\) the parity
transcript of the orbit of \(n\) (uniqueness in `PARTIAL_THEOREMS.md`
Theorem 2). If that orbit is eventually periodic, so is \(q\) — case (P);
the density bound is the cycle equation (packet 1, §5). Otherwise the
orbit is not eventually periodic; a bounded positive orbit repeats a
state and cycles, so the orbit diverges, and the drift wall (packet 1,
Theorem 1) gives \(\liminf s_L/L\ge\alpha\). If the natural density
exists it equals that liminf, is rational by Lemma B (primitive
presentation) or Cobham's theorem (general 2-automatic), and cannot equal
\(\alpha\) by Lemma A; hence it is \(>\alpha\). \(\square\)

So the full rigidity conjecture — *every* 2-automatic \(q\) with
\(\Phi(q)\in\mathbb Z_{>0}\) is eventually periodic — is equivalent to
the emptiness of case (S), i.e. to:

> **(Gap)** No divergent Collatz orbit has a 2-automatic parity word.

Case (P) is the classical cycle fence, decidable word-by-word
(`PARTIAL_THEOREMS.md` Theorem 3); our hunt's periodic branch found
exactly the trivial cycle values \(\Phi\in\{1,2\}\). Case (S) is the
entire remaining gap, and Theorem 3 shows it cannot be removed by any
density argument.

## 6. Theorem 2 — the critical density is forbidden to automatic words (PROVED)

**Statement.** No 2-automatic word has natural one-density exactly
\(\alpha=\log_3 2\).

**Proof.** If the natural density of a 2-automatic word exists it is
rational (Lemma B; Cobham's theorem for the general case). \(\alpha\) is
transcendental (Lemma A). \(\square\)

The drift wall's critical line is therefore unattainable inside the
automatic class: every 2-automatic word with an existing natural density
is strictly subcritical (\(\Phi\notin\mathbb Z_{>0}\) if aperiodic,
packet 1) or strictly supercritical (case (S), open). There is no
critical automatic word to analyze. The verifier asserts
`cmp_fraction_vs_alpha(rho) != 0` for every one of the exact rational
frequencies in the enumeration.

## 7. Theorem 3 — the supercritical stratum is nonempty and density-proof (PROVED)

The two walls of packet 1 consume a liminf. The following two witnesses
show that the surviving stratum of Theorem 1 is inhabited by explicit
2-automatic words, one of them *uniformly* supercritical — so no
strengthening of the wall to logarithmic, Cesàro, Abel, or any other
averaged density can close the gap.

**Witness 1 (primitive morphism).** Let \(\sigma(0)=11\),
\(\sigma(1)=10\), \(u=\lim\sigma^t(1)\). Then \(u\) is 2-automatic,
aperiodic, and \(\rho(u)=2/3>\alpha\).

*Proof.* The incidence matrix \(M=\bigl(\begin{smallmatrix}0&1\\2&1\end{smallmatrix}\bigr)\)
has \(M^2>0\) (primitive), column sums \(2\), and right eigenvector
\((1,2)\) at eigenvalue \(2\), so \(\rho(1)=2/3\) by Lemma B;
\(2/3>\alpha\) because \(3^2>2^3\). For aperiodicity, note
\(\sigma\)-self-similarity gives the exact identities (verified on a
\(2^{12}\) prefix as a control)
\(u_{2i}=1\), \(u_{4i+1}=0\), \(u_{4m+3}=u_m\).
Suppose \(u\) is eventually periodic with period \(p\). In a periodic
word every residue class mod \(p\) is eventually monochromatic. Take a
class \(\{n\equiv r\ (p)\}\) that meets \(E=\{n\equiv3\ (4)\}\) in a set
of positive upper density; such a class exists whenever \(4\nmid p\)
(for \(p\) odd every class meets \(E\); for \(p\equiv2\ (4)\) every
odd-\(r\) class does). On the intersection write \(n=4m+3\): then \(m\)
ranges over an arithmetic progression with odd difference (\(p\) when
\(p\) is odd, \(p/2\) when \(p\equiv2\ (4)\)), so it contains both even
\(m\), where \(u_m=u_{2i}=1\), and \(m\equiv1\ (4)\), where
\(u_m=u_{4i+1}=0\). Hence \(u_n=u_m\) takes both values on the class —
contradiction. (Classes avoiding \(E\) entirely are even-indexed, where
\(u=1\) consistently, so they give no contradiction.) Hence \(4\mid p\).
Then \(u_m=u_{4m+3}\) shows \(p/4\) is again an eventual period:
\(u_{m+p/4}=u_{4m+p+3}=u_{4m+3}=u_m\) for large \(m\). Iterating,
\(4^t\mid p\) for all \(t\) — impossible. \(\square\)

**Witness 2 (no natural density at all).** Let
\(q(n)=1\) iff \(n\) is even or \(\operatorname{bitlength}(n)\) is odd
(\(n\ge1\); \(q(0)=1\)). Then \(q\) is 2-automatic (a four-state DFAO:
state = bitlength parity × last bit read MSB-first), aperiodic, and

\[
\frac{s_L(q)}{L}\ \ge\ \frac23-o(1)\quad\text{for every }L,
\qquad
\liminf\frac{s_L}L=\frac23,\quad
\limsup\frac{s_L}L=\frac56,
\]

so the natural density fails to exist, and *every* averaging method
assigning a value to a sequence with \(s_L/L\ge2/3-o(1)\) uniformly sees
a supercritical word.

*Proof.* Automaticity: the two-bit state above is a finite DFAO.
Aperiodicity: eventual periodicity would force a natural density, which
does not exist (shell computation below). On the dyadic shell
\([2^{m},2^{m+1})\): all elements have bitlength \(m+1\); if \(m\) is
even, every element of the shell is in \(q\); if \(m\) is odd, exactly
the even elements are. Counting on \([1,2^{2K})\): evens contribute
\(\tfrac12+o(1)\), odd indices on even shells contribute
\(\tfrac12\cdot\tfrac13=\tfrac16+o(1)\) (the even shells carry
\(\tfrac13\) of the mass up to \(2^{2K}\)), total \(\tfrac23+o(1)\); on
\([1,2^{2K+1})\) the full top shell lifts this to \(\tfrac56+o(1)\).
Within an odd shell the running ratio is not monotone — each odd shell
opens with an even index (value \(1\)), a one-step transient above the
endpoint value (e.g. \(s_{129}/129=108/129=0.8372>5/6\), recurring at
every scale as \(5/6+O(2^{-2K})\)) — so the shell endpoints give the
global extrema only up to that additive transient, which vanishes as
\(L\to\infty\). Hence \(\liminf=2/3\), \(\limsup=5/6\), and the uniform
bound \(s_L/L\ge2/3-o(1)\) (numeric control: \(\min_{L\ge64}s_L/L>0.66\)
on the \(2^{14}\) prefix). \(2/3>\alpha\) since \(3^2>2^3\). \(\square\)

**Corollary (the gap is exact).** Full 2-automatic rigidity is
equivalent to the Gap statement of Theorem 1, and the drift wall — in
any averaged-density strengthening — provably cannot settle it: Witness 2
passes every density-based screen while being aperiodic and automatic.
What would kill the stratum is a genuinely different argument
(finite-state vs. 2-adic integrality), see §10.

## 8. Theorem 4 — the exact modular lift and stabilization certificates (PROVED)

**Statement.** For every \(L\ge1\),

\[
\boxed{
\Phi(q)\bmod 2^L
=
-\sum_{j:\,d_j<L}2^{d_j}\,3^{-(j+1)}\pmod{2^L},
}
\tag{8.1}
\]

an exact finite integer computation involving only the first \(L\)
symbols of \(q\). Writing \(N_L=\Phi(q)\bmod 2^L\): if
\(\Phi(q)=n\in\mathbb Z_{>0}\) then \(N_L=n\) for all \(L\) with
\(2^L>n\); hence an observed change \(N_L\neq N_{L+1}\) (equivalently,
bit \(L\) of \(\Phi(q)\) equal to \(1\)) certifies

\[
\Phi(q)\notin\{1,2,\ldots,2^{L}-1\}.
\tag{8.2}
\]

**Proof.** Terms with \(d_j\ge L\) have 2-adic valuation \(\ge L\) and
vanish mod \(2^L\); \(3\) is a 2-adic unit so \(3^{-(j+1)}\bmod 2^L\) is
exact. If \(\Phi(q)=n<2^L\) then \(N_L=n\) and \(N_{L+1}=n\).
\(\square\)

**Periodic words (exact Fraction form).** For \(q=w^\omega\) with period
\(p\) and \(m>0\) ones at positions \(r_i\) in the period, the one at
position \(r_i+kp\) has one-index \(km+i\), and the geometric series
gives the exact rational

\[
\Phi(q)
=
-\frac{3^m}{3^m-2^p}\sum_{i}\frac{2^{r_i}}{3^{i+1}}
\ \in\mathbb Q,
\tag{8.3}
\]

with the preperiod variant \(\Phi(q_0\cdots q_{h-1}w^\omega)
=\Phi_{\text{prefix}}+\frac{2^h}{3^{m_0}}\Phi(w^\omega)\). Sanity anchors
verified exactly: \(\Phi((10)^\omega)=1\), \(\Phi((01)^\omega)=2\) (the
trivial cycle), \(\Phi((110)^\omega)=-5\) (supercritical period,
correctly negative since \(2^3<3^2\)), and the engine reproduces
\(\Phi(\text{transcript of }n)\equiv n\pmod{2^{64}}\) for
\(1\le n\le 2000\).

**Lemma C (exact periodicity witness, PROVED).** Let \(\sigma\) be
uniform of length \(\ell\), \(\sigma(\text{seed})[0]=\text{seed}\),
\(u=\lim\sigma^t(\text{seed})\), and \(w=u[:p]\). If for every residue
\(j\bmod p\) the block \(\sigma(w_j)\) equals the length-\(\ell\) window
of \(v=w^\omega\) starting at position \(j\ell\bmod p\), then
\(\sigma(v)=v\), hence \(v=u\) (both are fixed points from the seed), and
\(u=w^\omega\) *exactly*.

*Proof.* The block of \(\sigma(v)\) at index \(i\) is
\(\sigma(w_{i\bmod p})\), which by hypothesis equals \(v\)'s window at
\((i\bmod p)\ell\bmod p = i\ell\bmod p\); that is exactly \(v\)'s block
at index \(i\). So \(\sigma(v)=v\), and \(v\) starts with
\(\sigma^t(\text{seed})\) for every \(t\), forcing \(v=u\). \(\square\)

## 9. The counterexample hunt (exact computation; zero candidates, as expected)

The verifier enumerates **every** uniform binary morphism of length
\(\ell\le4\) (\(16+64+256=336\) morphisms, all valid seeds) and every
uniform ternary morphism of length \(2\) with all six nonconstant binary
codings (\(729\) morphisms × codings × seeds), deduplicates by the
first \(256\) symbols (two words differing only after symbol \(255\) are
merged, so the lift window of the skipped copy is not examined
separately; no theorem depends on the enumeration),
adds the named families and the two witnesses of Theorem 3, and for each
distinct word computes: the exact rational density \(\rho\) (primitive
case, `Fraction` eigenvector, verified \((M-\ell I)v=0\)), the exact
comparison \(3^a\lessgtr2^b\) against \(\alpha\), periodicity (numeric
KMP control + Lemma C exact witness), and the lift bits
\(\Phi(q)\bmod 2^{512}\) via (8.1).

Results (certificate, full mode; 514 distinct words):

| class | binary \(\ell\le4\) | ternary \(\ell=2\) coded |
|---|---|---|
| primitive subcritical aperiodic ⇒ \(\Phi\notin\mathbb Z_{>0}\) (packet 1, PROVED) | 174 | 95 |
| primitive supercritical (case (S)) | 56 | 53 |
| periodic, exact witness (Lemma C) | 30 | 0 |
| periodic, numeric only | 10 | 32 |
| non-primitive (numeric sweep) | 16 | 48 |

- **No candidate.** No aperiodic word shows a stabilized lift window
  (top zero run \(\ge32\) bits): the maximum top zero run over all
  aperiodic words is **12 bits**, consistent with fair-bit lift digits
  (\(\sim\log_2\) of the sample size). An aperiodic automatic word with
  \(\Phi(q)\in\mathbb Z_{>0}\) would have been, verbatim, a Collatz
  counterexample; none exists in this class, and none was expected.
- **Periodic branch.** The only positive-integral \(\Phi\) values among
  exactly-witnessed periodic words are \(1\) and \(2\) — the trivial
  cycle transcripts \((10)^\omega,(01)^\omega\) — recovering the
  \(a\le18\) box of the atlas's exact cycle search from the automatic
  side.
- **Supercritical survivors.** All 109 primitive supercritical words
  have rational \(\rho\in\{2/3,3/4,4/5,5/6,5/7,6/7\}\), each certified
  \(>\alpha\) by the exact witness \(3^a>2^b\). Their lift bits change at
  every level up to \(L=505\)–\(511\), so by (8.2) each is certified
  \(\Phi(q)\notin\{1,\ldots,2^{505}-1\}\) (worst case): **if any of them
  is realized, it is by an integer \(\ge2^{505}\).** For the two proved
  witnesses of Theorem 3: \(\Phi(u)\) changes up to level 507
  (\(\ge2^{507}\) if realized), \(\Phi(\text{Witness 2})\) up to 511.
  These are exact finite-window certificates, **not** proofs of
  non-realizability — the Gap of Theorem 1 is precisely that no such
  proof currently exists.
- **Named families (confirming and extending packet 1).** Thue–Morse
  (\(1/2\)), period-doubling (\(1/3\)), Rudin–Shapiro (\(1/2\)),
  paperfolding (\(1/2\)): subcritical kills confirmed with exact
  witnesses \(3^1<2^{2}\), \(3^1<2^{3}\). Fibonacci word
  (\(2-\varphi<63/100<\alpha\); witnesses \(\sqrt5>87/50\iff12500>7569\)
  and \(3^{63}<2^{100}\)): killed, as a non-automatic control.
  **New:** the block oscillator
  \(a(n)=[\operatorname{bitlength}(n)\text{ odd}]\) — the canonical
  2-automatic word *without* a natural density (oscillation
  \(1/3\leftrightarrow2/3\)) — is killed all the same, because the drift
  wall consumes only \(\liminf s_L/L=1/3<\alpha\) (exact,
  \(3^1<2^3\)). This is the first entry in the atlas killed in the
  no-natural-density regime; the liminf form of packet 1's wall is
  exactly what reaches it.

## 10. Route 4 assessment: the lift is not a finite transduction

A natural hope: 2-adic addition is finite-state (Büchi automata), so
perhaps \(q\mapsto\Phi(q)\) is a finite transduction and
\(\Phi(q)\in\mathbb Z\) (terminating expansion) would force periodicity.
It is not, for a precise reason: the term \(2^{d_j}3^{-(j+1)}\) is gated
by the **threshold** \(d_j<L\), i.e. by the unbounded *count* of ones,
not by a congruence. (The counting residue *is* finite-state — for any
2-automatic \(q\) and any modulus \(m\), the running sum
\((\sum_{i<n}q_i)\bmod m\) is 2-automatic, by the standard kernel
argument: running sums of kernel elements form a finite set closed under
decimation. What fails is the comparison \(d_j<L\) against a growing
threshold, which no fixed automaton reads off the binary expansion of the
index.) Consequently the lift-bit sequence of a 2-automatic word need not
be automatic, and the integrality of \(\Phi(q)\) is not a finite-state
property of \(q\). A finite-state obstruction to case (S) — if one
exists — must come from the *interaction* of the DFAO with the
recursion \(x\mapsto T(x)\) itself, not from a transduction.

## 11. Confidence and the remaining gap, stated exactly

- **Proved:** Lemmas A, B (existence half cited), C; Theorems 1–4. The
  subcritical stratum of the 2-automatic class is closed
  (\(\Phi\notin\mathbb Z_{>0}\)); the critical stratum is empty; the
  periodic stratum is the classical cycle fence and shows only the
  trivial cycle in this sweep.
- **Not proved:** case (S) — *no divergent Collatz orbit has a
  2-automatic parity word*. Theorem 3 proves this is exactly the whole
  gap, that the gap class is inhabited, and that no averaged-density
  wall can close it. Confidence in the trichotomy itself: complete (it
  is a deduction from packet 1 plus Lemmas A–B).
- **Numeric-only elements (labeled):** prefix densities (float64
  controls of the exact eigenvectors), KMP periodicity detection for
  words without a Lemma C witness (periods \(\le\) prefix/4 on 8192
  symbols), and all last-change levels above the periodic branch. The
  "aperiodic" labels on the 109 survivors are numeric controls; each
  survivor's supercriticality (\(\rho>\alpha\)) and its certified
  exclusion \(\Phi(q)\notin\{1,\ldots,2^{505}-1\}\) are exact.
- **Expected and found:** no counterexample candidate. Any candidate
  would have been a Collatz counterexample.

## 12. Related work

Automatic-sequence theory: Cobham (1972, *Uniform tag sequences*) —
the DFAO/uniform-morphism equivalence and the rationality of automatic
letter frequencies; Allouche–Shallit (*Automatic Sequences*, 2003) —
the frequency theory of §8.4 and the standard no-natural-density
examples of which our Witness 2 is a Collatz-tuned variant. The
transcendence input is Gelfond–Schneider (1934). The realizability map
is the inverse of the Bernstein–Lagarias \(3x+1\) conjugacy map (*Canad.
J. Math.* 48, 1996), whose **periodicity conjecture** —
\(\Phi(q)\in\mathbb Q\iff q\) eventually periodic — contains our
rigidity statement as its automatic restriction to positive integer
values; Theorem 1 localizes the difficulty of that restriction to the
supercritical stratum, and Theorem 3 shows the restriction is already
sharp for density methods. The walls consumed are the atlas's own:
packet 1 (drift wall), whose named-family table this packet confirms and
extends to the no-natural-density regime (block oscillator). Finite-state
arithmetic (Büchi) and its limits for threshold counting (§10) are
classical automata theory.

## 13. Reproduce

```bash
python3 contribution/packets/2026-07-22-automatic-transcript-rigidity/verify_automatic_rigidity.py
python3 -m pytest contribution/packets/2026-07-22-automatic-transcript-rigidity/ -q
```

Full verifier runtime: ~3 s (budget 8 min). Reduced test mode
(`VATR_REDUCED=1`, used by the determinism test): <1 s. Certificate:
`automatic_rigidity_certificate.json` (deterministic; the test suite runs
the verifier twice in reduced mode and byte-compares). Other knobs:
`VATR_L_MAX` (lift precision, default 512), `VATR_MAXLEN` (binary
morphism length cap, default 4), `VATR_TERNARY` (ternary sweep),
`VATR_NCHECK` (orbit cross-checks, default 2000).
