# Landmark Resolution Strategies and a Pointwise Collatz Advance

**Date:** 22 July 2026  
**Scope:** research strategy, exact partial theorems, and a sharply defined next bridge. This document does **not** claim a complete proof or counterexample to the Collatz conjecture. No claim of literature priority is made for the deductions below without a separate exhaustive review.

---

## Executive result

The strongest exact increment obtained in this continuation is a **complexity-pressure rationality theorem** for the Terras parity conjugacy.

Let

\[
T(x)=
\begin{cases}
x/2,&x\equiv0\pmod2,\\[1mm]
(3x+1)/2,&x\equiv1\pmod2
\end{cases}
\]

on the 2-adic integers, and let \(\Phi(q)\) be the unique 2-adic state whose Terras parity transcript is the infinite binary word \(q\).

If \(q\) is not eventually periodic and \(\Phi(q)\) is rational with odd denominator, then its factor complexity satisfies

\[
\boxed{
\limsup_{k\to\infty}\frac{p_q(k)}{k}
\ge
\frac{1}{\log_2(3/2)}
=1.709511\ldots .
}
\]

Every Sturmian word has \(p_q(k)=k+1\). Therefore

\[
\boxed{
q\text{ Sturmian}
\quad\Longrightarrow\quad
\Phi(q)\notin\mathbb Q\cap\mathbb Z_2.
}
\]

In particular, no positive integer has a Sturmian Terras parity transcript. This eliminates the full Fibonacci, golden-angle, irrational mechanical, and characteristic critical-mechanical families as candidate Collatz counterexample transcripts.

A pressure-refined finite form is stronger: a rational parity transcript with small supercritical block discrepancy must have correspondingly large factor complexity. At exactly critical bounded discrepancy it must have full binary topological entropy.

The remaining universal obstruction is consequently pushed into a narrower region:

\[
\boxed{
\text{high symbolic complexity}
+
\text{large pressure excursions}
+
\text{an eventually-zero ordinary binary lift}.
}
\]

---

# Part I. What landmark resolutions actually did

The point of studying solved problems is not to copy their surface mathematics. It is to extract the transformations that changed an intractable statement into a rigid or finite one.

## 1. Fermat's Last Theorem: transport the counterexample into a richer category

A hypothetical Fermat solution was not attacked only as an integer equation. It was transported to a Frey elliptic curve. Modularity supplied an independent description of the same object, and the contradiction was completed by proving a stronger bridge theorem: semistable elliptic curves over \(\mathbb Q\) are modular. When a gap was found, Taylor and Wiles supplied the exact missing complete-intersection statement rather than weakening the goal.

**Reusable pattern**

\[
\text{hypothetical counterexample}
\longrightarrow
\text{new object with two incompatible descriptions}
\longrightarrow
\text{strong bridge theorem}.
\]

**Collatz translation:** a hypothetical survivor should be transported to an enlarged object containing at least

\[
(
\text{parity language},
\text{multiplicative pressure},
\text{affine offset},
\text{2-adic lift digits},
\text{3-adic residue transport}
).
\]

The desired contradiction must compare two independent descriptions: symbolic survival and ordinary-integer realizability.

## 2. Poincare/geometrization: build a monotone quantity and classify the singular boundary

Ricci flow made geometry evolve. Perelman's entropy and noncollapsing estimates controlled the flow, while singular regions were classified and treated by surgery. Singularities were not discarded as an exceptional set; they became the central objects to understand. Finite extinction then closed the relevant branch.

**Reusable pattern**

\[
\text{evolution}
+
\text{monotone functional}
+
\text{boundary classification}
+
\text{controlled continuation}.
\]

**Collatz translation:** pressure and height replace geometric entropy. Tail-minimum states of a divergent orbit are the singular scales: from each such state the entire future stays above the current height. They must be classified, not averaged away.

## 3. Kepler: reduce an infinite optimization to finitely many certified local configurations

Hales replaced arbitrary infinite packings by finite-dimensional decomposition stars, classified a finite list of tame plane graphs, and eliminated cases through linear programs, branching, and interval inequalities. Flyspeck later formalized the full proof.

**Reusable pattern**

\[
\text{global infinite object}
\longrightarrow
\text{local normal forms}
\longrightarrow
\text{finite exhaustive list}
\longrightarrow
\text{machine-checked inequalities}.
\]

**Collatz translation:** the ideal proof should reduce every exceptional parity language to finitely many grammars, automata, or cocycle cones. The ideal counterexample should itself be a finite certificate: a small grammar plus an invariant proving infinite expansion.

## 4. Lorenz/Smale 14: numerical exploration becomes proof only after interval certification

Tucker combined normal-form theory with a rigorous ODE solver based on partitioning, interval arithmetic, and directed rounding. The numerical orbit picture was not the certificate; validated enclosures were.

**Reusable pattern:** computation is legitimate when every rounding and truncation error is enclosed and the output proves a finite theorem.

**Collatz translation:** large trajectory searches are hypothesis generators. A valid increment is an exact congruence, a finite automaton certificate, an interval-free integer inequality, or compiled proof-assistant code.

## 5. Smale 11: persistent nonhyperbolicity is converted into rigidity

The density-of-hyperbolicity program in one-dimensional dynamics required rigidity and renormalization. Persistent failure of generic hyperbolicity was not treated as arbitrary noise; it forced combinatorial structure that could be controlled.

**Reusable pattern**

\[
\text{failure of generic behavior}
\longrightarrow
\text{renormalized structure}
\longrightarrow
\text{rigidity}.
\]

**Collatz translation:** persistent failure of Tao-style mixing should force low factor complexity, a large Fourier resonance, a recurrent near-neutral language, or another explicit structured class.

## 6. Smale 17: use the right condition metric and the right output notion

Homotopy methods solve for an approximate zero, not an exact symbolic expression. Complexity is controlled by conditioning along the continuation path. Lairez's deterministic average-polynomial algorithm derandomizes by extracting randomness already present in the input.

**Reusable pattern:** reformulate the output and complexity in coordinates adapted to the problem.

**Collatz translation:** the natural condition parameters are not raw trajectory length. They include

\[
\Delta(i,j)
=
\#\{1\text{s in }q_i\ldots q_{j-1}\}
-
(j-i)\log_3 2,
\]

\[
\lambda(i,j)=3^{\Delta(i,j)},
\qquad
|2^L-3^a|,
\]

and the position of \(a/L\) among continued-fraction approximants to \(\log_3 2\).

## 7. Modern counterexamples: reverse the truth value and search for a small obstruction

Three recent examples emphasize different disproof mechanisms.

- The unit-distance counterexample imported an unexpected number-field construction and used enormous algebraic degree as a resource rather than a defect.
- The dimension-three Jacobian counterexample is an explicit finite polynomial identity: a constant nonzero Jacobian together with a displayed multi-point fiber.
- The Dinitz-Garg-Goemans flow instance reduces the issue to a seven-vertex, nine-arc finite gadget whose exact cost/capacity incompatibility is checked in Lean. Its repository correctly separates the formally certified finite model from the external domain-review question identifying it with the published conjecture.

**Reusable pattern**

\[
\text{stop improving the expected proof}
\longrightarrow
\text{negate the conclusion}
\longrightarrow
\text{search for the smallest exact obstruction}.
\]

**Collatz translation:** run proof and disproof programs in parallel.

- **Proof program:** show that permanent non-descent is incompatible with an eventually-zero ordinary binary lift.
- **Counterexample program:** construct a finite-state-with-counter parity grammar, prove positive drift by an invariant cone, and prove that its inverse 2-adic state is a positive ordinary integer.

---

# Part II. The unified resolution protocol

The uploaded Terence Method can be combined with the landmark patterns into the following protocol.

## Phase 1: verify and isolate

1. Keep the exact Terras affine identity.
2. Keep the ordinary-integer realization condition separate from 2-adic existence.
3. Separate cycle, divergence, and rational-2-adic questions.
4. Maintain an explicit ledger of every step that is statistical rather than pointwise.

## Phase 2: structuralize

1. Enlarge the state from \(n\) to parity, pressure, affine offset, residue, and lift digits.
2. Identify the lost direction: replacing an integer by its residue modulo \(2^L\) discards the high binary tail.
3. Detect that direction at the endpoint modulo \(3^a\).
4. Search for a pointwise inverse theorem: persistent failure of descent must force symbolic structure.

## Phase 3: geometrize

Treat a parity prefix as a chart between two lattices:

\[
r+2^L\mathbb Z
\longleftrightarrow
z+3^a\mathbb Z.
\]

Treat near-neutral pairs \((a,L)\) as resonance tiles. Treat tail minima as boundary points of the renormalized dynamics.

## Phase 4: globalize

1. Prove local certificates persist across their full affine cylinders.
2. Classify low-complexity exceptional languages.
3. Prove high-complexity exceptional languages force nonzero lift digits.
4. Reduce any periodic residue to the finite cycle equation.
5. Formalize every finite reduction.

## Phase 5: stress-test

Replace \(3n+1\) by \(An+B\). Identify the first parameter at which each argument fails. The complexity theorem below has real force for \(A=3\), but its key threshold becomes vacuous at \(A=5\). This isolates a genuinely exceptional feature of the coefficient three.

---

# Part III. Exact Terras and rational-lift setup

Let \(q=(q_0,q_1,\ldots)\in\{0,1\}^{\mathbb N}\). The inverse Terras conjugacy is

\[
\Phi(q)
=
-\sum_{j=0}^{\infty}
\frac{q_j2^j}{3^{s_{j+1}}},
\qquad
s_k=\sum_{t=0}^{k-1}q_t,
\]

with convergence in \(\mathbb Z_2\). It is the unique 2-adic state whose parity transcript is \(q\).

A 2-adic integer has eventually periodic binary digits exactly when it lies in

\[
\mathbb Q_{\mathrm{odd}}
:=
\mathbb Q\cap\mathbb Z_2,
\]

the rationals with odd denominator.

Assume

\[
\Phi(q)=\frac ad,
\qquad
a\in\mathbb Z,
\quad d\in\mathbb Z_{>0}\text{ odd}.
\]

Let

\[
x_j=T^j(a/d),
\qquad
y_j=dx_j\in\mathbb Z.
\]

Since \(d\) is odd, \(q_j\equiv y_j\pmod2\), and

\[
\boxed{
 y_{j+1}
 =
 \frac{3^{q_j}y_j+dq_j}{2}.
}
\tag{3.1}
\]

For \(0\le i\le j\), set

\[
s(i,j)=\sum_{t=i}^{j-1}q_t,
\qquad
M(i,j)=\frac{3^{s(i,j)}}{2^{j-i}}.
\]

Repeated substitution gives the exact Green expansion

\[
\boxed{
 y_L
 =
 M(0,L)a
 +
 \frac d2\sum_{j=0}^{L-1}q_jM(j+1,L).
}
\tag{3.2}
\]

Define the critical slope

\[
\alpha=\log_3 2
\]

and the supercritical block discrepancy

\[
D_N
=
\max\left(
0,
\max_{0\le i<j\le N}
\bigl(s(i,j)-\alpha(j-i)\bigr)
\right).
\tag{3.3}
\]

Because \(3^\alpha=2\),

\[
M(i,j)=3^{s(i,j)-\alpha(j-i)}\le3^{D_N}
\]

for every interval contained in \([0,N]\), including the empty interval after adjoining the outer maximum with zero.

---

# Part IV. Complexity-pressure rationality theorem

For an infinite word \(q\), define its factor complexity

\[
p_q(k)
=
\#\{q_iq_{i+1}\cdots q_{i+k-1}:i\ge0\}.
\]

## Lemma 1. Repeated parity blocks force a power-of-two congruence

If the length-\(k\) parity blocks beginning at positions \(i\) and \(j\) are equal, then

\[
\boxed{y_i\equiv y_j\pmod{2^k}.}
\tag{4.1}
\]

### Proof

A fixed length-\(k\) parity word with \(s\) ones acts by

\[
2^k y_{i+k}=3^s y_i+d c
\]

for an integer \(c\) depending only on the word. The same equation holds at \(j\). Subtracting gives

\[
2^k(y_{i+k}-y_{j+k})=3^s(y_i-y_j).
\]

Since \(3^s\) is odd, \(2^k\mid y_i-y_j\). \(\square\)

## Lemma 2. Height-complexity collision principle

Let

\[
H_N=\max_{0\le j\le N}|y_j|.
\]

If \(q\) is not eventually periodic and

\[
2^k>2H_N,
\]

then

\[
\boxed{p_q(k)\ge N+1.}
\tag{4.2}
\]

### Proof

Consider the \(N+1\) length-\(k\) blocks beginning at positions \(0,1,\ldots,N\). If two were equal, Lemma 1 would imply that the corresponding states differ by a multiple of \(2^k\). Their difference has absolute value at most \(2H_N<2^k\), so the states are equal. Determinism would then make the future orbit, and hence \(q\), eventually periodic. Therefore all \(N+1\) blocks are distinct. \(\square\)

## Theorem 3. Complexity-pressure rationality inequality

Suppose \(q\) is not eventually periodic and \(\Phi(q)=a/d\in\mathbb Q_{\mathrm{odd}}\). Define

\[
B_N
=
3^{D_N}\left(|a|+\frac{dN}{2}\right)
\]

and

\[
K_N
=
\left\lceil\log_2(2B_N+1)\right\rceil.
\]

Then, for every \(N\ge1\),

\[
\boxed{p_q(K_N)\ge N+1.}
\tag{4.3}
\]

### Proof

For every \(L\le N\), equation (3.2) and the definition of \(D_N\) give

\[
|y_L|
\le
3^{D_N}|a|
+
\frac d2\sum_{j=0}^{L-1}q_j3^{D_N}
\le
3^{D_N}\left(|a|+\frac{dN}{2}\right)
=B_N.
\]

Thus \(H_N\le B_N\), while \(2^{K_N}>2B_N\). Lemma 2 gives (4.3). \(\square\)

This theorem is pointwise. It contains no density, expectation, independence, or finite-search assumption.

---

# Part V. Consequences

## Corollary 4. Universal linear-complexity threshold for rational lifts

If \(q\) is not eventually periodic and \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\), then

\[
\boxed{
\limsup_{k\to\infty}\frac{p_q(k)}{k}
\ge
\kappa,
\qquad
\kappa
=
\frac1{\log_2(3/2)}
=1.709511\ldots .
}
\tag{5.1}
\]

### Proof

From (3.1),

\[
|y_{j+1}|+d
\le
\frac32(|y_j|+d).
\]

Hence

\[
H_N
<
(|a|+d)(3/2)^N.
\]

Choose

\[
k_N
=
\left\lceil
N\log_2(3/2)+\log_2(2(|a|+d))
\right\rceil+1.
\]

Then \(2^{k_N}>2H_N\), so Lemma 2 gives \(p_q(k_N)\ge N+1\). Since

\[
\frac{k_N}{N}\to\log_2(3/2),
\]

(5.1) follows. \(\square\)

## Corollary 5. Sturmian rationality obstruction

Every Sturmian word satisfies

\[
p_q(k)=k+1.
\]

Therefore

\[
\boxed{
q\text{ Sturmian}
\quad\Longrightarrow\quad
\Phi(q)\notin\mathbb Q_{\mathrm{odd}}.
}
\tag{5.2}
\]

In particular:

- \(\Phi(q)\) is not a positive integer;
- \(\Phi(q)\) is not a negative integer;
- \(\Phi(q)\) has no eventually periodic binary expansion;
- no positive Collatz orbit has a Fibonacci, golden-angle, or irrational mechanical parity transcript.

This gives a complete negative answer for the Sturmian class to the rational-realizability question studied for the \(3x+1\) conjugacy map.

## Corollary 6. Critical bounded discrepancy forces full entropy

Assume \(q\) is not eventually periodic, \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\), and

\[
D_N\le D
\quad\text{for all }N
\]

for a constant \(D\). Then

\[
\boxed{
\limsup_{k\to\infty}
\frac{\log_2 p_q(k)}{k}
=1.
}
\tag{5.3}
\]

### Proof

Theorem 3 has \(K_N=\log_2N+O(1)\) and \(p_q(K_N)\ge N+1\). Hence

\[
\frac{\log_2p_q(K_N)}{K_N}
\ge
\frac{\log_2(N+1)}{\log_2N+O(1)}
\to1.
\]

The reverse inequality is automatic because \(p_q(k)\le2^k\). \(\square\)

Thus a rationally realizable critical survivor cannot be quasiperiodic, substitutive with low entropy, or symbolically sparse. It must exhibit full binary factor entropy.

## Corollary 7. Balanced supercritical words require large complexity

Suppose that, for constants \(\beta>\alpha\) and \(C\), every factor of length \(\ell\) has at most \(\beta\ell+C\) ones. Put

\[
g=\beta\log_2 3-1>0.
\]

If \(q\) is aperiodic and \(\Phi(q)\in\mathbb Q_{\mathrm{odd}}\), then

\[
\boxed{
\limsup_{k\to\infty}\frac{p_q(k)}k\ge\frac1g.
}
\tag{5.4}
\]

For a Sturmian word, \(p_q(k)/k\to1\), while \(g<\log_2 3-1<1\), so the inequality is impossible. This is the pressure-refined version of Corollary 5.

---

# Part VI. Why the coefficient three is exceptional

Consider the odd-affine family

\[
T_{A,B}(x)
=
\begin{cases}
x/2,&x\text{ even},\\
(Ax+B)/2,&x\text{ odd},
\end{cases}
\]

with positive odd \(A>2\) and odd \(B\). For a rational 2-adic state \(a/d\), scaling by \(d\) gives

\[
y_{j+1}
=
\frac{A^{q_j}y_j+Bdq_j}{2}.
\]

With

\[
c=\frac{|B|}{A-2},
\]

one has

\[
|y_{j+1}|+cd
\le
\frac A2(|y_j|+cd).
\]

The universal complexity threshold becomes

\[
\limsup_{k\to\infty}\frac{p_q(k)}k
\ge
\frac1{\log_2(A/2)}.
\]

For \(A=3\), the denominator \(\log_2(3/2)\) is below one, so the threshold is greater than one and excludes Sturmian complexity.

For \(A=5\), \(\log_2(5/2)>1\); the threshold falls below one and becomes weaker than the elementary Morse-Hedlund lower bound for any aperiodic word.

Hence \(A=3\) is the unique positive odd coefficient greater than one lying on the useful side of the symbolic-growth threshold \(A<4\). This is a genuine Phase-V stress-test result, not numerology.

---

# Part VII. Natural-number probes

Natural constants and prime families are useful when they expose exact dynamics. They are not useful merely because they are aesthetically prominent.

## 1. The true critical constants

The drift boundary is

\[
\alpha=\log_3 2=0.6309297535\ldots .
\]

The maximal Terras height exponent is

\[
\gamma=\log_2(3/2)=0.5849625007\ldots ,
\]

and the rational-lift complexity threshold is

\[
\kappa=1/\gamma=1.7095112913\ldots .
\]

The golden ratio is not the governing constant. Its role is diagnostic: Fibonacci and golden-angle codings are Sturmian, so the theorem eliminates them exactly.

## 2. Near-neutral resonance tiles

The continued-fraction convergents of \(\alpha\) begin

\[
\frac12,
\frac23,
\frac58,
\frac{12}{19},
\frac{41}{65},
\frac{53}{84},
\frac{306}{485},
\frac{665}{1054},
\frac{15601}{24727},\ldots
\]

A pair \((a,L)\) from this list minimizes

\[
|L\log2-a\log3|
\]

and therefore supplies a near-neutral parity tile with multiplier \(3^a/2^L\). Early Fibonacci-like convergents explain why Fibonacci patterns appear, but the controlling irrational is \(\log_3 2\), not \(1/\varphi\).

## 3. Fermat-side descent

For \(b\ge2\),

\[
T^2(2^b+1)=3\cdot2^{b-2}+1<2^b+1.
\]

Thus every Fermat number \(2^{2^r}+1\) with \(r\ge1\) descends below itself in two Terras steps.

## 4. Mersenne-side expansion

For \(k,m\ge1\),

\[
\boxed{
T^j(2^km-1)=3^j2^{k-j}m-1
\quad(0\le j\le k).
}
\tag{7.1}
\]

Hence \(2^k-1\) shadows the negative 2-adic fixed point \(-1\) for \(k\) consecutive odd steps and reaches \(3^k-1\).

For the combined Mersenne/Fermat exponent \(k=2^r\),

\[
\boxed{
\nu_2(3^{2^r}-1)=r+2.
}
\tag{7.2}
\]

So an all-odd expansive burst of length \(2^r\) is followed by only \(r+2\) forced halvings. This is an exact adversarial model of a long excursion. It is not a divergence certificate because the subsequent parity pattern is uncontrolled.

The plus/minus pair

\[
2^{2^r}+1,
\qquad
2^{2^r}-1
\]

therefore exposes a sharp binary boundary: immediate descent on the Fermat side and an enormous transient expansion on the Mersenne side.

---

# Part VIII. What has been pushed from “almost all” toward “all”

The uploaded research state correctly identifies the universal wall:

\[
\text{statistical rarity}
\not\Rightarrow
\text{arithmetic impossibility for one integer}.
\]

The theorem above crosses part of that wall because it is pointwise.

## Established in this continuation

1. **Finite pointwise inequality:** Theorem 3 holds for each individual rational 2-adic realization.
2. **Rationality obstruction:** every Sturmian parity word has irrational \(\Phi(q)\).
3. **Golden/Fibonacci elimination:** all irrational mechanical and golden-angle models are excluded as positive-integer transcripts.
4. **Critical entropy requirement:** any rational aperiodic transcript with bounded critical discrepancy must have full binary factor entropy.
5. **Universal divergent-orbit requirement:** an aperiodic rational transcript must have linear factor-complexity coefficient at least \(1.7095\ldots\).
6. **Parameter stress-test:** the mechanism is structurally useful at \(A=3\) and becomes vacuous at \(A=5\).

## Not established

1. No nontrivial positive cycle has been produced or universally eliminated.
2. No positive diverging orbit has been produced.
3. High factor complexity does not by itself prevent \(\Phi(q)\) from being a positive integer.
4. Tao-style distributional mixing has not yet been converted into a theorem about one fixed survivor.

---

# Part IX. The remaining leap

A divergent positive-integer counterexample must now satisfy all of the following:

1. its parity word is not eventually periodic;
2. \(\Phi(q)\in\mathbb Z_{>0}\);
3. \(\limsup p_q(k)/k\ge1.709511\ldots\);
4. if its critical block discrepancy is bounded, its topological entropy is exactly one;
5. it is not Sturmian, Fibonacci, golden-angle mechanical, Thue-Morse-type subcritical, or any other already eliminated structured class;
6. its lift digits nevertheless become zero permanently, because \(\Phi(q)\) is an ordinary positive integer.

The exact missing theorem should be formulated in lift-digit language.

For every length \(L\), let \(r_L\in[0,2^L)\) be the unique residue realizing the first \(L\) parity symbols. Write

\[
r_{L+1}=r_L+\varepsilon_L2^L,
\qquad
\varepsilon_L\in\{0,1\}.
\]

Then

\[
\Phi(q)\in\mathbb Z_{\ge0}
\quad\Longleftrightarrow\quad
\varepsilon_L=0
\text{ for all sufficiently large }L.
\]

## Target theorem: pointwise complexity-lift dichotomy

For every parity word supporting permanent non-descent, prove that at arbitrarily large scales either

1. its factor language is too small for the complexity-pressure inequality; or
2. its arithmetic spreading forces \(\varepsilon_L=1\).

If the second branch occurs infinitely often, ordinary positive-integer realizability is impossible. Symbolically:

\[
\boxed{
\text{permanent non-descent}
\Longrightarrow
\bigl(\text{complexity-pressure contradiction}\bigr)
\lor
\bigl(\varepsilon_L=1\text{ infinitely often}\bigr).
}
\tag{9.1}
\]

The first branch is now rigorously populated by Theorem 3 and its corollaries. The second branch is the exact pointwise analogue of Tao-style mixing.

---

# Part X. Parallel research programs

## A. Proof route

1. Formalize the generalized rational-state lemmas, not only the positive-integer case.
2. Extend Theorem 3 to finite-state, morphic, Toeplitz, and linearly recurrent languages.
3. Define a quantitative 3-adic spreading statistic for the endpoint offsets of the distinct factors forced by Theorem 3.
4. Prove that enough distinct factors force both possible high lift digits with a uniform frequency.
5. Apply the result at the infinitely many tail-minimum scales of a hypothetical divergent orbit.
6. Close the periodic branch separately with the exact finite cycle equation.

## B. Counterexample route

1. Use near-neutral convergents \((a,L)\) as tiles.
2. Use Mersenne shadows of negative 2-adic cycles as expansive modules.
3. Search for a small directed grammar whose every recurrent component has positive total log multiplier.
4. Attach the exact lift transducer and require eventual-zero lift digits.
5. Prove an invariant cone for the affine offsets, not merely positive average drift.
6. Emit a finite grammar, seed, and inductive inequality as a formal divergence certificate.

## C. Adversarial audit

For every claimed bridge ask:

- Does it use a finite prefix as though it controlled an infinite word?
- Does it replace a 2-adic state by an ordinary integer without proving eventual-zero lift digits?
- Does it turn density zero into emptiness?
- Does it ignore additive offsets?
- Does it prove only absence of cycles while leaving divergence?
- Does it rely on a numerical orbit rather than an inductive invariant?
- Does the argument survive at \(A=5\), and if not, is the exact failure informative?

---

# Part XI. Proof-discovery flow

\[
\boxed{
\begin{array}{c}
\text{hypothetical survivor}\\[1mm]
\downarrow\\
\text{parity language + pressure + rational lift}\\[1mm]
\swarrow\qquad\searrow\\
\text{low complexity / recurrence}
\qquad
\text{high complexity / spreading}\\[1mm]
\downarrow\qquad\qquad\downarrow\\
\text{Theorem 3: exact collision}
\qquad
\text{target: nonzero lift digits}\\[1mm]
\downarrow\qquad\qquad\downarrow\\
\text{impossible}
\qquad
\text{impossible}\\[1mm]
\end{array}
}
\]

The left half now contains a genuine theorem. The right half is the remaining leap.

---

# Final assessment

The study of landmark solutions changes the Collatz strategy in one decisive way: stop trying to improve a typical-drift estimate until it somehow becomes universal. Translate a hypothetical survivor into a richer object and force a collision between two descriptions.

That collision has now been achieved for low-complexity rational parity words. Symbolic repetition forces congruence modulo a large power of two; the affine growth bound keeps the corresponding rational orbit states too small to be distinct. This proves that Sturmian and all golden/Fibonacci mechanical transcripts are not merely unlikely: they are arithmetically unrealizable by any rational 2-adic Collatz state.

The remaining survivor, if one exists, must live in the high-complexity/high-pressure corner while possessing an eventually-zero ordinary lift. Proving that high arithmetic spreading forces infinitely many nonzero lift digits is the precise theorem that would complete the low-complexity/high-complexity dichotomy and make the universal leap.

---

## Reference map

Primary or authoritative sources consulted for the strategy synthesis include:

- A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*.
- R. Taylor and A. Wiles, *Ring-theoretic properties of certain Hecke algebras*.
- G. Perelman, *The entropy formula for the Ricci flow and its geometric applications*; *Finite extinction time...*.
- T. Hales, *A proof of the Kepler conjecture*; the Flyspeck formal-proof paper.
- W. Tucker, *A rigorous ODE solver and Smale's 14th problem*.
- O. Kozlovski, W. Shen, and S. van Strien, *Rigidity for real polynomials* and *Density of hyperbolicity in dimension one*.
- C. Beltran and L. Pardo; P. Lairez on Smale's 17th problem.
- J. Lopez and P. Stoll, *The 3x+1 conjugacy map over a Sturmian word*.
- Bernstein and Lagarias, *The 3x+1 conjugacy map*.
- The exact-D Dinitz-Garg-Goemans Lean certificate repository.
- The OpenAI unit-distance proof and subsequent human-digested remarks.
- The explicit dimension-three Jacobian counterexample and mathematical digestion.
