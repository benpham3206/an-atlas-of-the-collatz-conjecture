# Rational states with irrational-like Collatz behavior

**Date:** 2026-07-22  
**Status:** exact 2-adic shadow theorem and finite verifier; no Collatz proof,
counterexample, or novelty claim.

## Verdict

The suggested object exists, exactly: for every finite prefix of an aperiodic
parity law, there is an odd-denominator rational state whose Collatz orbit has
that prefix and is then exactly periodic. These rational periodic states
converge in the **2-adic metric** to the state with the full aperiodic parity
law. In particular, rational states can imitate an irrational 2-adic state for
arbitrarily many Collatz steps.

This is useful mainly as a deletion theorem. No finite amount of strange,
chaotic, high-stopping-time, or low-complexity parity behavior can distinguish
an irrational 2-adic state from a rational periodic shadow. A valid
positive-integer counterexample search must test the nonlocal arithmetic gate:
eventual-zero lift digits for divergence, or exact divisibility for a cycle.

## Definitions

Use the Terras map on odd-denominator rationals in \(\mathbb Z_2\):

\[
T(x)=\begin{cases}
x/2,&x\equiv0\pmod2,\\
(3x+1)/2,&x\equiv1\pmod2.
\end{cases}
\]

For a nonempty binary word \(w=w_0\cdots w_{L-1}\), let \(s\) be its number
of ones. Its exact affine composite is

\[
T_w^L(x)=\frac{3^s x+c_w}{2^L},
\qquad
c_w=\sum_{j=1}^{s}3^{s-j}2^{d_j},
\]

where \(d_1<\cdots<d_s\) are the positions of the ones.

## Proposition 1 — explicit periodic rational closure

Every nonempty word \(w\) has the rational closure

\[
\boxed{x_w=\frac{c_w}{2^L-3^s}}.
\]

Its denominator is odd, its first \(L\) parity symbols are exactly \(w\), and

\[
T^L(x_w)=x_w.
\]

### Proof

The fixed-point equation for the affine composite gives the displayed
fraction. Since \(2^L-3^s\) is odd, \(x_w\in\mathbb Q\cap\mathbb Z_2\). Modulo
\(2^L\),

\[
x_w\equiv-\frac{c_w}{3^s}\pmod{2^L}.
\]

The right side is the unique Terras residue cylinder for \(w\), equivalently
the finite inverse-conjugacy sum

\[
-\sum_{j=1}^{s}\frac{2^{d_j}}{3^j}\pmod{2^L}.
\]

Thus \(x_w\) follows \(w\). Substitution into the composite gives
\(T^L(x_w)=x_w\). Therefore its full parity transcript is \(w^\omega\). ∎

## Theorem 2 — rational shadows converge to the full behavior

Let \(q\in\{0,1\}^{\mathbb N}\), let \(w_L=q_0\cdots q_{L-1}\), and set
\(x_L=x_{w_L}\). Then

\[
Q(x_L)_j=q_j\quad(0\le j<L)
\]

and

\[
x_M\equiv x_L\pmod{2^L}\qquad(M\ge L).
\]

Consequently \((x_L)\) converges 2-adically to the unique state

\[
\Phi(q)=-\sum_{j\ge0}\frac{q_j2^j}{3^{s_{j+1}}}
\]

whose parity transcript is \(q\).

### Proof

Proposition 1 says \(x_L\) occupies the length-\(L\) residue cylinder of
\(w_L\). For \(M\ge L\), both \(x_M\) and \(x_L\) occupy that cylinder, so
their difference is divisible by \(2^L\) in \(\mathbb Z_2\). The nested
congruences are exactly convergence to the inverse-limit state \(\Phi(q)\). ∎

## Proposition 3 — rational imitation has a height cost

Let \(x=a/d\), with \(d>0\) odd and the fraction reduced, match an aperiodic
word \(q\) through a finite observed depth. Suppose positions \(i<j\) have the
same length-\(K\) block, but the two observed tails later disagree. Then

\[
\boxed{|a|+d\ge 2^{K-1}(2/3)^j.}
\]

### Proof

Write \(y_t=dT^t(x)\). Equal length-\(K\) blocks imply
\(y_i\equiv y_j\pmod{2^K}\). The later mismatch proves \(y_i\ne y_j\), since
equal states have identical deterministic futures. Therefore
\(|y_i-y_j|\ge2^K\). The universal scaled growth bound gives

\[
|y_t|+d\le(3/2)^t(|a|+d),
\]

and hence

\[
2^K\le |y_i-y_j|
<2(3/2)^j(|a|+d).
\]

Rearranging proves the claim. ∎

This supplies a quantitative meaning for “approaching irrational behavior.” If
an irrational word returns to a length-\(K\) block at shifts
\(j\sim\rho K\) and later breaks the repetition, any rational state matching
that observation must have height at least

\[
\frac12\left(\frac{2}{(3/2)^\rho}\right)^K.
\]

For Fibonacci-scale recurrence \(\rho\approx\varphi\), the base is about
\(1.037787\). The finite verifier records exact rational lower-bound
certificates for the 55-symbol Fibonacci shadow. This does not prove the
asymptotic recurrence constant or irrationality; those remain symbolic inputs.

### The requested irrational limit

Take \(q\) to be the Fibonacci word, the fixed point of
\(0\mapsto01,1\mapsto0\). The supplied complexity-pressure theorem proves that
its \(\Phi(q)\) is not rational: Fibonacci is Sturmian with
\(p_q(k)=k+1\), while an aperiodic rational Terras transcript would require

\[
\limsup_{k\to\infty}\frac{p_q(k)}k
\ge \frac1{\log_2(3/2)}=1.709511\ldots.
\]

The rational periodic shadows at Fibonacci prefix lengths begin

| \(L\) | prefix | \(x_L\) |
| ---: | --- | ---: |
| 2 | `01` | \(2\) |
| 3 | `010` | \(2/5\) |
| 5 | `01001` | \(22/23\) |
| 8 | `01001010` | \(130/229\) |
| 13 | `0100101001001` | \(6802/7949\) |
| 21 | `010010100100101001010` | \(1248614/2090591\) |

Each row is rational and exactly periodic, each matches the irrational-limit
transcript for its first \(L\) steps, and the rows converge to that irrational
state 2-adically. This claim is not about convergence in the usual real metric.

## Corollary 4 — finite-prefix counterexample searches cannot discriminate

Let a proposed anomaly score depend only on the first \(L\) parity symbols.
Every state with that score has an exact rational periodic shadow with the same
score. Therefore no finite-prefix score—entropy, apparent chaos, record height,
Benford fit, recurrence, or compression ratio—can by itself certify either
irrationality or a positive-integer divergent orbit.

The obstruction was not solved by moving to rationals; it moved into the limit:

\[
\text{all finite cylinders glue in }\mathbb Z_2
\quad\not\Rightarrow\quad
\Phi(q)\in\mathbb Z_{>0}.
\]

## Chaos and emergent-complexity interpretation

On the enlarged compact space \(\mathbb Z_2\), the parity map conjugates Terras
dynamics to the one-sided binary shift. The usual chaos signatures are
therefore structural: arbitrary symbolic transcripts exist, periodic points are
dense, and the full shift has base-2 topological entropy one. Proposition 1 is
the explicit arithmetic form of dense periodic points.

That observation also prevents category drift:

- **Chaos theory:** explains why finite orbits can shadow arbitrary symbolic
  behavior and why sensitive-looking traces are cheap in \(\mathbb Z_2\).
- **Symbolic complexity:** the supplied pointwise theorem says an aperiodic
  rational survivor needs high factor complexity **or** large pressure
  excursions. It does not require both simultaneously.
- **Computational complexity:** no NP-hardness, undecidability, or algorithmic
  lower bound for the fixed \(3n+1\) map follows.
- **Arithmetic realization:** remains the hard layer. The full shift freely
  realizes every word in \(\mathbb Z_2\); positive integers realize only states
  whose lift digits eventually vanish.

So “emergence” is not the missing miracle. Symbolic complexity emerges
automatically after enlarging the domain. The missing theorem must show that a
permanently non-descending symbolic object cannot also satisfy the rigid
ordinary-integer lift condition.

## Exact cycle gate

The same closure formula gives a decisive finite test:

\[
x_w\in\mathbb Z
\iff
(2^L-3^s)\mid c_w.
\]

If the quotient is positive, it is an ordinary positive integer on an exact
cycle. If it is a noninteger rational, it is a **ghost shadow**, not a Collatz
counterexample. Near-neutrality \(3^s\approx2^L\) can make the denominator
interesting, but cannot replace divisibility.

## Musk's five-step algorithm, with the quantifiers preserved

### 1. Make the requirements less dumb

- A Collatz counterexample is a **positive integer**, not merely a 2-adic or
  odd-denominator rational state.
- The two targets are separate: a nontrivial positive cycle or a positive orbit
  that never falls below its start and diverges.
- A least counterexample is odd. A start \(4m+1\) with \(m>0\) is deleted
  because \(T^2(4m+1)=3m+1<4m+1\).
- A finite exceptional-looking transcript is not a target property; Theorem 2
  shows that every finite transcript has a rational periodic impersonator.

### 2. Delete the part or process

Delete from evidentiary status:

- continuing an orbit after it falls below its starting value in a
  least-counterexample search;
- even starts and the residue class \(1\bmod4\);
- short-cycle searches below independently verified lower bounds;
- candidate rankings based only on finite entropy, chaos, compression, Benford,
  or stopping-time behavior;
- rational shadows whose exact denominator does not divide the affine offset.

Keep these objects as adversarial controls, not as counterexample evidence.

### 3. Simplify and optimize what remains

Represent a candidate prefix by the exact tuple

\[
(w,L,s,c_w,D_w,r_L,\varepsilon_L),
\qquad D_w=2^L-3^s.
\]

The tuple separates four questions that trajectory plots conflate:

1. symbolic behavior: \(w\);
2. multiplicative pressure: \(3^s/2^L\);
3. cycle integrality: \(D_w\mid c_w\);
4. divergent positive-integer realizability: eventual-zero lift digits
   \(\varepsilon_L\).

### 4. Accelerate cycle time

- Enumerate primitive necklaces rather than all rotations for cycle closure.
- Stop a least-counterexample trajectory at its first descent below the start.
- Use near-neutral convergents only to generate stress cases, then immediately
  apply the exact divisibility or lift gate.
- Require every heuristic outlier to emit a small exact certificate:
  `(word, affine offset, denominator, residue, lift transition)`.

Subagents can expand bounded candidate families, but they cannot promote a
candidate; exact arithmetic and an independent verifier remain the acceptance
gate.

### 5. Automate last

`verify/rational_shadow.py` automates three independent checks:

1. the affine fixed-point identity;
2. direct rational Terras iteration and return;
3. agreement with the modular inverse-conjugacy series.

`verify/test_rational_shadow.py` exhausts every word through length nine and
checks 2-adic coherence of Fibonacci shadows. The next Lean target is
Proposition 1 plus the nested-cylinder convergence statement—not the Collatz
conjecture.

## Kill criteria and next exact question

This branch is dead as a direct counterexample route if it only produces longer
periodic rational shadows. Theorem 2 says that outcome is automatic.

The branch stays alive only if it yields one of:

1. a word \(w\) whose closure is a new positive integer cycle, with exact
   divisibility and direct parity verification; or
2. a nonperiodic transcript with an inductive permanent-non-descent certificate
   and a proved eventually-zero lift; or
3. a theorem that every survivor satisfying the complexity-or-pressure
   requirement forces infinitely many nonzero lift digits.

The remaining proof target is still the pointwise complexity–lift dichotomy.
The shadow theorem improves the search by proving that finite behavior alone
must be deleted from the acceptance criteria.

## Adversarial packet correction

The packet's rational-lift complexity theorem survives independent derivation.
Two scope corrections are required:

1. the proved survivor condition is **high complexity or large pressure
   excursions**, not “high complexity and high pressure”; and
2. the tail-minimum boundary limit need not inherit the original positive
   integer's eventual-zero lift. Complexity, boundary expansiveness, and
   positive-integer realization currently live on different objects until a
   compatibility theorem glues them.

The supplied finite scripts validate ingredients of the complexity theorem,
but they do not directly evaluate every displayed \(D_N,B_N,K_N\) pressure
inequality. The symbolic proof, not the `.out` files, carries that result.

## Sources and provenance

- Daniel J. Bernstein, [*A Non-Iterative 2-Adic Statement of the 3N+1
  Conjecture*](https://doi.org/10.2307/2160415), for the inverse 2-adic
  conjugacy.
- Thijs Laarhoven and Benne de Weger, [*The Collatz conjecture and De Bruijn
  graphs*](https://arxiv.org/abs/1209.3495), for the finite residue-cylinder and
  2-adic graph viewpoint.
- Terence Tao, [*Almost all orbits of the Collatz map attain almost bounded
  values*](https://doi.org/10.1017/fmp.2022.8), for the distributional result
  whose pointwise quantifier boundary must remain explicit.
- `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md` in the supplied packet,
  for the self-contained complexity-pressure theorem used to prove that the
  Fibonacci limit above is irrational.

No literature-priority claim is made for the shadow theorem; it is an explicit
consequence of the Bernstein–Lagarias conjugacy, packaged here as a search
no-go criterion.
