# Primitive subcritical substitutions cannot be rational Collatz transcripts

**Status:** proved deduction from the packet's complexity-pressure theorem plus
standard primitive-substitution dynamics; exact finite controls are executable.
This is a pointwise exclusion theorem for a named structured class. It is not a
proof of the Collatz conjecture, not a counterexample, and not a classification
of all automatic sequences. No literature-priority claim is made.

## Result

Let \(\theta:\{0,1\}\to\{0,1\}^k\) be a primitive, constant-length binary
substitution, prolongable on a symbol, and let

\[
q=\theta^\infty(a)=q_0q_1q_2\cdots
\]

be its fixed point. Let \(\beta\) be the frequency of `1` in \(q\), and put

\[
\alpha=\log_3 2.
\]

### Theorem — primitive uniform subcritical obstruction

If

1. \(q\) is not eventually periodic, and
2. \(\beta<\alpha\),

then

\[
\boxed{\Phi(q)\notin\mathbb Q_{\mathrm{odd}}.}
\]

Consequently \(q\) is not the parity transcript of any ordinary positive or
negative integer under the Terras map.

This closes a genuine subcase of the automatic-transcript obstruction in
`LIFT_COCYCLE.md`: pure fixed points of primitive uniform binary substitutions
whose stationary one-density is below the Collatz critical density.

## Proof

The proof keeps three layers separate: substitution dynamics, symbolic
complexity, and rational Collatz realization.

### 1. Subcritical frequency bounds every positive pressure excursion

For an interval \([i,j)\), write

\[
s(i,j)=\sum_{t=i}^{j-1}q_t
\]

and define

\[
D_N=\max\left(0,\max_{0\le i<j\le N}
  \bigl(s(i,j)-\alpha(j-i)\bigr)\right).
\]

A primitive substitution subshift is uniquely ergodic. Therefore occurrences
of `1` have frequency \(\beta\) uniformly over all sufficiently long factors:
for every \(\varepsilon>0\), there is \(L\) such that every factor \(u\) of
\(q\) with \(|u|\ge L\) satisfies

\[
\left|\frac{|u|_1}{|u|}-\beta\right|<\varepsilon.
\]

Choose \(\varepsilon=(\alpha-\beta)/2\). Every factor of length at least
\(L\) then has one-density strictly below \(\alpha\), so its contribution to
\(D_N\) is negative. Only factors shorter than \(L\) can contribute
positively. There are finitely many of those and, crudely,

\[
0\le D_N\le L
\]

for every \(N\). Thus \(D_N=O(1)\).

For completeness, uniformity here is not an independence or random-walk
assumption. It is the deterministic uniform Birkhoff property of a primitive
substitution. In the constant-length binary case it can also be read directly
from Perron-Frobenius: the incidence matrix has dominant eigenvalue \(k\), its
other eigenvalue has modulus below \(k\), and a long factor decomposes into
large substitution blocks plus two boundary pieces.

### 2. A uniform substitution fixed point has zero factor entropy

Let \(p_q(n)\) count the distinct length-\(n\) factors of \(q\). Choose \(r\)
so that

\[
k^{r-1}<n\le k^r.
\]

Since \(q=\theta^r(q)\), every length-\(n\) factor lies inside
\(\theta^r(ab)\) for some adjacent pair \(ab\) occurring in \(q\). There are
at most four binary pairs and fewer than \(2k^r\) possible starting positions
in each image. Hence

\[
p_q(n)\le 8k^r<8kn.
\]

Therefore

\[
\limsup_{n\to\infty}\frac{\log_2p_q(n)}n=0.
\]

This elementary bound is intentionally loose; only zero entropy matters.

### 3. Rational realization would force full factor entropy

Corollary 6 of the supplied pointwise packet states that if \(q\) is not
eventually periodic, \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\), and
\(D_N=O(1)\), then

\[
\limsup_{n\to\infty}\frac{\log_2p_q(n)}n=1.
\]

Steps 1 and 2 instead give bounded \(D_N\) and entropy zero. The two
conclusions are incompatible. Therefore
\(\Phi(q)\notin\mathbb Q_{\mathrm{odd}}\). \(\square\)

## Two exact corollaries

### Thue-Morse

For

\[
0\mapsto01,\qquad1\mapsto10,
\]

the incidence matrix, with columns indexed by source symbols, is

\[
M=\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad \beta=\frac12<\log_3 2.
\]

The fixed point is aperiodic. Hence its inverse Terras state is not an
odd-denominator rational and cannot be a positive-integer Collatz state.

### Period-doubling

For

\[
0\mapsto01,\qquad1\mapsto00,
\]

the incidence matrix and stationary one-frequency are

\[
M=\begin{pmatrix}1&2\\1&0\end{pmatrix},
\qquad \beta=\frac13<\log_3 2.
\]

Its fixed point is also aperiodic. It therefore has no odd-denominator
rational inverse Terras state and no positive-integer Collatz realization.

The critical comparisons use exact integer certificates:

\[
3^{63}<2^{100}
\quad\Longrightarrow\quad
\frac{63}{100}<\log_3 2,
\]

and

\[
2^{1000}<3^{631}
\quad\Longrightarrow\quad
\log_3 2<\frac{631}{1000}.
\]

Both \(1/2\) and \(1/3\) are already below the certified lower bound
\(63/100\).

## What was deleted from the search

The theorem removes the entire family described above without enumerating
starting integers or extending finite trajectories. In the five-step
engineering language:

1. **Question:** replace "looks chaotic" with the exact rational-realization
   predicate \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\).
2. **Delete:** discard every primitive uniform aperiodic fixed point with
   \(\beta<\log_3 2\); it cannot even be rationally realized.
3. **Simplify:** reduce each substitution to its incidence matrix, fixed-point
   property, and factor language.
4. **Accelerate:** use exact matrix arithmetic and bounded prefix diagnostics
   only as controls for theorem hypotheses.
5. **Automate:** emit a deterministic JSON record and targeted tests, while
   leaving the infinite theorem in the proof layer.

## Exact boundary of the advance

This theorem does **not** cover:

- primitive uniform substitutions with \(\beta\ge\log_3 2\);
- nonprimitive substitutions;
- a coding applied after substitution without rechecking frequency and
  aperiodicity;
- general automatic sequences that are not presented as pure fixed points in
  this form;
- high-entropy transcripts;
- the proof that every positive integer eventually reaches `1`.

The next promising split is therefore precise: investigate supercritical or
critical automatic words through unbounded pressure, and investigate whether
the ordinary-integer lift condition can coexist with that pressure. Extending
the present theorem by merely testing longer prefixes is a kill path; the
missing bridge is infinite and arithmetic.

## Executable evidence

- `verify/primitive_uniform_obstruction.py` validates binary uniform
  substitutions, decides 2-by-2 primitivity exactly, computes stationary
  one-frequencies as `Fraction`, certifies the bundled bounds on
  \(\log_3 2\), and emits finite factor/discrepancy controls.
- `verify/test_primitive_uniform_obstruction.py` checks the named controls,
  invalid inputs, deterministic CLI output, and exact-bound certificates.
- `verify/primitive_uniform_results.json` is the generated read-back record.

The finite factor counts do not prove the theorem. They test the machinery and
named examples. The proof above carries the infinite conclusion.

## Sources and provenance

- The supplied packet,
  `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`, Theorem 3 and
  Corollary 6, supplies the rational-lift complexity-pressure implication.
- Jean-Paul Allouche and Jeffrey Shallit, *Automatic Sequences*, Chapter 6,
  supplies the standard uniform-morphism/automatic-sequence framework:
  https://doi.org/10.1017/CBO9780511546563.007
- El Abdalaoui, Kułaga-Przymus, Lemańczyk, and de la Rue record the standard
  fact that primitive substitution systems are uniquely ergodic and have zero
  topological entropy:
  https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n3-p06-p.pdf
- Lejeune, Leroy, and Rigo record the standard Thue-Morse morphism,
  aperiodicity, and linear factor complexity:
  https://arxiv.org/abs/1812.07330
- Špitalský records the period-doubling fixed point as a well-known aperiodic
  binary sequence:
  https://arxiv.org/abs/1807.09096
