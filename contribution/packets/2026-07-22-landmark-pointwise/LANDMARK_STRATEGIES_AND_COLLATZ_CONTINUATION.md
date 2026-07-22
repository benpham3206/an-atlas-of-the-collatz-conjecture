# Landmark Proof Architectures and a Collatz Continuation

**Date:** 22 July 2026  
**Map:**
\[
T(n)=\begin{cases}
n/2,&n\text{ even},\\[1mm]
(3n+1)/2,&n\text{ odd}.
\end{cases}
\]

## Scope and evidence labels

This report has four layers.

- **Source-derived:** proof architectures extracted from primary papers and from *An Atlas of the Collatz Conjecture*.
- **Independently verified:** the posted Dinitz–Garg–Goemans counterexample certificate.
- **New exact deductions in this continuation:** a factor-complexity barrier, a complexity–pressure inequality, a divergence blow-up theorem, an adapted odd-run energy, and several diagnostic no-go results.
- **Prospective:** the precise lemmas still needed to turn “almost all” into “all.”

No universal Collatz proof or counterexample is claimed. No literature-priority claim is made for the new deductions without a dedicated priority search.

---

# 1. What solved landmark problems actually did

The common pattern is not “try harder on the original formula.” Successful solutions usually changed the object, the scale, or the certificate.

| Problem | Decisive move | Final certificate style | Transfer to Collatz |
|---|---|---|---|
| Fermat’s Last Theorem | A hypothetical solution is converted into a Frey elliptic curve; modularity places that curve in an incompatible category. | Bridge object plus incompatibility theorem. | Build a richer object from a hypothetical survivor, then prove that its required properties cannot coexist. |
| Poincaré conjecture / Smale 2 | Evolve geometry by Ricci flow, introduce a monotone entropy, classify singularity models, and perform surgery. | Monotone functional plus boundary classification. | Blow up a divergent orbit at its tail minima; classify the resulting boundary dynamics rather than the raw orbit. |
| Kepler conjecture | Convert an infinite-dimensional packing problem into a finite-dimensional local score optimization and a finite list of tame graphs. | Local-to-global reduction plus exact inequalities and formal checking. | Find an unavoidable set of local Collatz configurations and prove each is reducible by a persistent descent certificate. |
| Four-color theorem | Assume a minimal counterexample; prove an unavoidable set of configurations; verify every configuration is reducible. | Minimal-counterexample discharging plus finite exhaustive verification. | Use a minimal Collatz survivor, a “discharging” rule on parity/run blocks, and a certified reducibility library. |
| Sphere packing in dimensions 8 and 24 | Optimize a dual linear-programming bound; equality conditions nearly determine a “magic” auxiliary function, then modular forms construct it. | Sharp dual witness exact on the extremizer. | Search for a dual potential exact on the `1 ↔ 2` cycle and strictly coercive on every other positive-integer chart. |
| Kadison–Singer | Replace exponentially many discrete choices by mixed characteristic polynomials; interlacing ensures one choice is as good as the averaged algebraic shadow. | Algebraic shadow of a discrete selection problem. | Replace raw branch enumeration by a real-rooted or convex algebraic object whose extremal value certifies a good descent block. |
| Smale 11(b) | Repeated renormalization turns persistent nonhyperbolicity into rigid small-scale structure. | Structure forced by failure of generic behavior. | Prove persistent failure of Collatz mixing forces a low-complexity or resonant transcript, then eliminate it arithmetically. |
| Smale 14 | Reduce the Lorenz problem to finitely many rigorous return-map bounds and validate them with interval arithmetic and directed rounding. | Small independent checker for a finite analytic certificate. | Make every computational Collatz claim proof-carrying: exact residues, intervals, hashes, and an independent verifier. |
| Smale 17 | Use homotopy continuation and condition geometry; later derandomize by extracting randomness from the input itself. | Condition-controlled continuation and self-randomization. | Track first-passage distributions across scale and look for arithmetic “self-randomness” in the offset cocycle. |
| Dinitz–Garg–Goemans cost conjecture | Search for a tiny integrality-gap obstruction rather than a general rounding theorem. | One small graph and an eight-case exact certificate. | For disproof, seek a compact finite grammar or cycle certificate, not a long numerical excursion. |

## 1.1 The combined strategy

The recurring architecture is:

\[
\boxed{
\text{normalize}
\to
\text{construct a bridge object}
\to
\text{find monotonicity or a dual witness}
\to
\text{split structure from randomness}
\to
\text{reduce the rigid branch to finite certificates}
\to
\text{formalize and adversarially verify}.
}
\]

Five rules follow.

1. **Assume a least or extremal counterexample.** Extract every exact restriction before introducing probability.
2. **Enlarge the state.** Keep the variables that the original formulation discards.
3. **Treat exceptional behavior as a boundary object.** Blow it up and classify it.
4. **Separate a conceptual reduction from finite checking.** A machine should verify only a finite, explicit terminal certificate.
5. **Use nearby failures diagnostically.** Generalized maps and deliberately structured transcripts should reveal which invariant is actually special to `3n+1`.

---

# 2. The recent Dinitz–Garg–Goemans certificate

The publicly posted instance has three demands

\[
d_1=15,\qquad d_2=10,\qquad d_3=15,
\]

so `d_max = 15`. The displayed fractional flow sends direct amounts `10,6,10` and long-route amounts `5,4,5`. The direct unit costs are `2,3,2`, hence

\[
10\cdot2+6\cdot3+10\cdot2=58.
\]

The displayed arc loads are used as capacities.

Each commodity has two unsplittable choices: a cost-30 direct route or a zero-cost long route. Any two zero-cost choices violate one capacity by `16`, exceeding the permitted additive violation `15`:

- `t1` long and `t2` long overload `s→u`;
- `t1` long and `t3` long overload `u→v`;
- `t2` long and `t3` long overload `v→w`.

Therefore at most one commodity can use its zero-cost route. At least two must pay `30`, so every feasible unsplittable routing costs at least `60`. Feasible routings of cost `60` exist. Thus the displayed fractional cost `58` cannot be matched.

This is the exact lesson for Collatz counterexample search:

\[
\boxed{
\text{A decisive counterexample should have a tiny verifier and a structural reason, not merely a long trace.}
}
\]

The accompanying verifier enumerates all `2^3=8` unsplittable choices.

---

# 3. The Collatz state that must be retained

The earlier atlas correctly isolates the realizability wall. Every finite parity word occurs, and every infinite parity word determines a `2`-adic state. The missing condition is that this state be a positive ordinary integer.

For a length-`L` parity word, retain the enlarged chart

\[
\boxed{
\Xi_L=(r_L,z_L,m_L,s_L,D_L,\varepsilon_L,\mathcal L_L).
}
\]

Here:

- `r_L` is the canonical residue in `[0,2^L)`;
- `n=r_L+2^Lm_L` is the ordinary-integer fiber decomposition;
- `s_L` is the number of odd steps;
- `z_L=T^L(r_L)`;
- `D_L=s_L-\rho L`, with
  \[
  \rho=\log_3 2;
  \]
- `epsilon_L` is the next binary lift digit of the associated `2`-adic state;
- `mathcal L_L` records the factor language of the transcript.

The exact cylinder law is

\[
\boxed{
T^L(r_L+2^Lm)=z_L+3^{s_L}m.
}
\tag{3.1}
\]

The lift recurrence is

\[
\boxed{
\varepsilon_L\equiv z_L+q_L\pmod2,
\qquad
r_{L+1}=r_L+\varepsilon_L2^L.
}
\tag{3.2}
\]

Positive-integer realizability is exactly eventual vanishing of the lift digits, followed by stabilization at a positive residue.

The new ingredient in this report is to couple the lift/cylinder coordinates to **symbolic factor complexity** and to a **boundary blow-up at infinity**.

---

# 4. New theorem I: the Terras recurrence barrier

Let

\[
x_j=T^j(n),\qquad q_j=x_j\bmod2.
\]

For an infinite binary word `q`, let `p_q(L)` be the number of distinct contiguous factors of length `L`.

## Theorem 4.1 — Recurrence forces a `2^L` excursion

Let `n` be a positive integer. If its Terras parity word `q` is not eventually periodic, then for every `L>=1`,

\[
\boxed{
\max_{0\le j\le p_q(L)}x_j\ge2^L.
}
\tag{4.1}
\]

### Proof

There are `p_q(L)+1` length-`L` blocks beginning at positions

\[
0,1,\ldots,p_q(L).
\]

Only `p_q(L)` distinct length-`L` blocks exist, so two are equal. Choose

\[
0\le i<j\le p_q(L)
\]

with

\[
(q_i,\ldots,q_{i+L-1})=(q_j,\ldots,q_{j+L-1}).
\]

The Terras parity-vector bijection implies

\[
x_i\equiv x_j\pmod{2^L}.
\]

If both states were strictly below `2^L`, this congruence would force `x_i=x_j`. Determinism would then make the orbit, and hence its parity word, eventually periodic. This contradicts the hypothesis. Therefore at least one of `x_i,x_j` is at least `2^L`. ∎

## Corollary 4.2 — Universal factor-complexity lower bound

For every Terras step,

\[
T(x)+1\le\frac32(x+1).
\]

Thus

\[
x_j+1\le(n+1)\left(\frac32\right)^j.
\]

Combining with Theorem 4.1 gives

\[
\boxed{
p_q(L)
\ge
\frac{\log(2^L+1)-\log(n+1)}{\log(3/2)}.
}
\tag{4.2}
\]

Consequently,

\[
\boxed{
\liminf_{L\to\infty}\frac{p_q(L)}L
\ge
c_*:=\frac{\log2}{\log(3/2)}
\approx1.70951129135.
}
\tag{4.3}
\]

## Consequences

1. No aperiodic Sturmian word can be the Terras parity transcript of a positive integer, because every Sturmian word has `p(L)=L+1`.
2. In particular, Fibonacci words and irrational-rotation codings based on the golden angle are excluded as complete counterexample transcripts.
3. More generally, every aperiodic positive-realizable transcript must have linear factor-complexity coefficient at least `c_*`.

This crosses the realizability wall for a broad symbolic class using only exact positive-integer arithmetic. It does not merely say that a structured word is statistically unlikely.

---

# 5. New theorem II: complexity versus critical pressure

Define

\[
s_j=\sum_{i=0}^{j-1}q_i,
\qquad
D_j=s_j-\rho j,
\qquad
\rho=\log_3 2.
\]

The exact Terras cocycle can be rewritten as

\[
\boxed{
x_j
=3^{D_j}n
+\frac12\sum_{i=0}^{j-1}q_i3^{D_j-D_{i+1}}.
}
\tag{5.1}
\]

For `N>=0`, let

\[
R_q(N)=
\max_{0\le j\le N}D_j-
\min_{0\le j\le N}D_j.
\]

## Theorem 5.1 — Complexity–pressure inequality

For every `N`,

\[
\boxed{
\max_{0\le j\le N}x_j
\le
\left(n+\frac N2\right)3^{R_q(N)}.
}
\tag{5.2}
\]

If `q` is not eventually periodic, then for every `L`,

\[
\boxed{
R_q(p_q(L))
\ge
\log_3\!\left(
\frac{2^L}{n+p_q(L)/2}
\right).
}
\tag{5.3}
\]

### Proof

Because `D_0=0`, the maximum of the `D_j` is nonnegative and the minimum is nonpositive. Hence every exponent `D_j` and every difference `D_j-D_{i+1}` in (5.1) is at most `R_q(N)` when `j<=N`. There are at most `N` additive terms. This proves (5.2). Combining (5.2) with Theorem 4.1 at `N=p_q(L)` proves (5.3). ∎

## Corollary 5.2 — Critical low-complexity transcripts are impossible

If

\[
p_q(L)=\exp(o(L)),
\]

then any nonperiodic positive realization must satisfy

\[
R_q(p_q(L))\ge(\rho-o(1))L.
\]

Therefore no nonperiodic transcript can be positive-realizable if both

\[
p_q(L)=\exp(o(L))
\]

and

\[
R_q(p_q(L))=o(L).
\]

In particular, if the critical discrepancy is uniformly bounded,

\[
|s_j-\rho j|\le C,
\]

and the factor complexity is subexponential, positive realization is impossible.

This eliminates low-complexity balanced models at the exact critical slope, not only subcritical-density models.

---

# 6. New theorem III: a Perelman-style blow-up at infinity

A nonperiodic Collatz counterexample must diverge to infinity. A divergent orbit has a canonical family of “tail-minimum” basepoints.

## Theorem 6.1 — Supercritical boundary blow-up

Assume

\[
x_j=T^j(n)\longrightarrow\infty.
\]

Then there exist indices `i_k→∞` with

\[
x_{i_k}=\min_{j\ge i_k}x_j,
\qquad
x_{i_k}\to\infty,
\]

and a subsequential limit parity word

\[
q^{(\infty)}=\lim_{k\to\infty}
(q_{i_k},q_{i_k+1},\ldots)
\]

such that every prefix is strictly expansive:

\[
\boxed{
3^{s_L(q^{(\infty)})}>2^L
\qquad(L\ge1).
}
\tag{6.1}
\]

Moreover, for each fixed `L`,

\[
\boxed{
\frac{x_{i_k+L}}{x_{i_k}}
\longrightarrow
\frac{3^{s_L(q^{(\infty)})}}{2^L}
\ge1.
}
\tag{6.2}
\]

### Proof

Because `x_j→∞`, each sufficiently late tail has an attained minimum, and these tail minima tend to infinity. Compactness of the binary sequence space gives a coordinatewise-convergent subsequence of parity tails.

Fix `L`. Along a further tail of the subsequence, the first `L` parity bits are one fixed word `w`, with `a` odd symbols and affine offset `c_w`. Tail minimality gives

\[
\frac{3^ax_{i_k}+c_w}{2^L}=x_{i_k+L}\ge x_{i_k}.
\]

If `3^a<2^L`, this would imply

\[
x_{i_k}\le\frac{c_w}{2^L-3^a},
\]

contradicting `x_{i_k}→∞`. Equality `3^a=2^L` is impossible by unique factorization, so `3^a>2^L`. Dividing the affine identity by `x_{i_k}` and letting `k→∞` proves (6.2). ∎

## Interpretation

A divergent ordinary orbit would create, at infinity, a homogeneous multiplicative trajectory whose every prefix stays above the critical line. This is the exact Collatz analogue of taking a geometric blow-up near a singularity.

The theorem does not yet give a contradiction. It produces the boundary object that must now be classified:

\[
\mathcal S_\rho=
\left\{
q:\sum_{j<L}q_j\ge\lceil\rho L\rceil
\text{ for every }L
\right\}.
\]

The pointwise universal problem becomes:

> Can a positive-integer orbit have a shift-limit at its tail minima lying in `S_rho`, while its lift digits still stabilize as required by ordinary-integer realizability?

---

# 7. Natural-pattern probes used correctly

The relevant natural constants are not decorative. Each must enter an exact equation.

## 7.1 Golden ratio and golden angle

The golden ratio is useful as the benchmark for **poor rational approximation**. Collatz’s intrinsic resonance is instead

\[
\log_2 3.
\]

Near-neutral blocks satisfy

\[
2^L\approx3^a,
\qquad
\frac La\approx\log_2 3.
\]

The first convergents include

\[
\frac11,
\frac21,
\frac32,
\frac85,
\frac{19}{12},
\frac{65}{41},
\frac{84}{53},
\frac{485}{306},
\frac{1054}{665},\ldots
\]

These are the correct exponent pairs for cycle and near-neutral-block searches. Fibonacci/Sturmian codings remain useful as extremal low-complexity models—but Theorem 4.1 now excludes them as complete positive Collatz transcripts.

## 7.2 Mersenne excursions

For every `p>=1`,

\[
\boxed{
T^j(2^p-1)=3^j2^{p-j}-1
\qquad(0\le j\le p).
}
\tag{7.1}
\]

Thus `2^p-1` realizes an exact block of `p` consecutive odd steps and

\[
T^p(2^p-1)=3^p-1.
\]

Mersenne numbers are positive truncations of the `2`-adic repelling fixed point `-1`, whose parity word is `1^infinity`. They are therefore the correct stress test for any proposed Lyapunov function.

## 7.3 No bounded correction to logarithmic size can work

Let `h:N→R` be bounded. There is no globally nonincreasing potential of the form

\[
V(n)=\log(n+1)+h(n)
\]

along every nontrivial Terras step. Indeed, the first `p` steps from `2^p-1` increase `log(n+1)` by

\[
p\log(3/2),
\]

while the bounded correction changes by at most a constant.

Any Perelman-style Collatz entropy must therefore be unbounded near the `2`-adic point `-1`, or it must use variable-length returns rather than single steps.

## 7.4 An exact odd-run energy

Define

\[
\boxed{
E(n)=\log(n+1)+\log(3/2)\,\nu_2(n+1).
}
\tag{7.2}
\]

If `n` is odd, then

\[
T(n)+1=\frac32(n+1),
\qquad
\nu_2(T(n)+1)=\nu_2(n+1)-1,
\]

so

\[
\boxed{E(T(n))=E(n)}
\]

through every odd step. This potential exactly absorbs Mersenne-type odd runs. All nontrivial drift is transferred to the transitions initiated by even states.

## 7.5 The exact run map

Let `e_k` be successive even states after compressing one even step followed by all ensuing odd steps. Put

\[
\frac{e_k+2}{2}=2^{r_k}v_k,
\qquad v_k\text{ odd}.
\]

Then

\[
\boxed{
3^{r_k}v_k+1=2^{r_{k+1}+1}v_{k+1}.
}
\tag{7.3}
\]

The macrostep length is `r_k+1`, and its leading logarithmic drift is

\[
r_k\log(3/2)-\log2.
\]

The critical mean run length is exactly

\[
\frac{\log2}{\log(3/2)}=c_*.
\]

This explains why the same constant appears in the factor-complexity barrier.

Fermat exponents `r=2^m` and Mersenne cores `v=1` are useful stress cases for (7.3), but they do not themselves produce a counterexample.

---

# 8. The combined proof machine

## 8.1 Counterexample bridge object

Assume a least counterexample `N`.

- Its orbit never drops below `N`.
- If bounded, it yields a finite nontrivial cycle certificate.
- If nonperiodic, it diverges and yields the boundary blow-up of Theorem 6.1.
- Its parity transcript must satisfy the factor-complexity lower bound of Theorem 4.1.
- If its complexity is subexponential near critical pressure, Theorem 5.1 forces linearly growing discrepancy excursions.
- Its lift digits must nevertheless be eventually zero because `N` is an ordinary positive integer.

The bridge object is therefore

\[
\boxed{
\text{ordinary lift stabilization}
+\text{large symbolic complexity or large pressure excursions}
+\text{supercritical boundary blow-ups}.
}
\]

A proof must show that these requirements are incompatible.

## 8.2 Structure-versus-randomness split

### Zero-entropy / low-complexity branch

Use exact arithmetic:

- factor-complexity barrier;
- complexity–pressure inequality;
- lift cocycle;
- run map;
- cycle equations and linear forms in logarithms;
- classification of automatic, substitutive, Sturmian, Toeplitz, and sparse-defect languages.

Theorem 4.1 removes all Sturmian and Fibonacci/golden-angle candidates. Theorem 5.1 removes all critical balanced subexponential-complexity candidates.

### Positive-entropy / high-complexity branch

Use Tao-style scale-residue transport, but add a pointwise amplification theorem. Distributional mixing alone does not see one orbit.

The required bridge is:

> **Positive-entropy amplification target.** If one divergent positive orbit has a positive-entropy shift closure, then its compatible inverse/cylinder families generate a set of positive logarithmic density whose orbit minima exceed some function tending to infinity.

This would contradict the established almost-all descent theorem.

### The exact universal leap

The conjunction of the following two statements would prove the conjecture, after cycles are eliminated:

1. **Amplification:** every divergent orbit with positive-entropy symbolic closure contradicts logarithmic-density descent.
2. **Rigidity:** every divergent orbit with zero-entropy symbolic closure violates positive-integer lift stabilization.

This is sharper than “improve the almost-all estimate.” It names the two precise pointwise mechanisms required.

---

# 9. Counterexample program

A counterexample must come in one of two forms.

## 9.1 Cycle certificate

Search valuation/parity words near the convergents of `log_2 3`. For a word of length `L` with `a` odd steps and offset `c`, a cycle point must satisfy

\[
\boxed{
n=\frac{c}{2^L-3^a}>0,
}
\tag{9.1}
\]

plus exact parity and valuation checks. This is a finite SMT/SAT/Lean certificate.

## 9.2 Divergence certificate

A periodic grammar cannot suffice: an eventually periodic parity word gives an eventually periodic `2`-adic orbit and, when positively realized, an actual finite cycle. A divergent certificate therefore needs genuinely nonperiodic or unbounded-memory structure.

The DGG lesson is to search for a **small inductive invariant**, for example:

- a finite grammar with an integer-valued unbounded counter;
- an adelic cone invariant under the exact lift/run recurrence;
- a substitution with a proof that its lift digits eventually vanish and its pressure is uniformly supercritical.

No such certificate was found in this continuation.

---

# 10. Progress from “almost all” toward “all”

The progress is not a universal proof, but the exceptional set has been narrowed in a new exact way.

A nonperiodic positive Collatz transcript cannot be:

- Sturmian;
- Fibonacci or golden-angle mechanical;
- any aperiodic word with factor-complexity coefficient below `1.709511...`;
- any critical balanced word with subexponential factor complexity;
- any word whose low complexity is not compensated by large critical-pressure excursions.

A divergent trajectory would additionally have to produce a supercritical boundary blow-up at every tail-minimum scaling limit.

Thus a counterexample cannot be a simple natural quasiperiodic skeleton. It must combine:

\[
\boxed{
\text{ordinary-integer lift stabilization}
+\text{high symbolic complexity or extreme discrepancy}
+\text{persistent supercritical boundary behavior}.
}
\]

The remaining leap is a pointwise entropy/rigidity theorem, not another finite verification and not a stronger density estimate alone.

---

# 11. Next proof-carrying research packets

1. **Formalize Theorems 4.1, 5.1, and 6.1.** They are short enough for Lean and directly touch the realizability boundary.
2. **Classify zero-entropy transcripts.** Start with primitive automatic/substitutive systems, coupling their discrepancy eigenvalues to (5.3) and their lift digits to (3.2).
3. **Build an amplification experiment.** For long slow-descending orbits, enumerate suffix-minimum cylinders and inverse trees, measuring logarithmic mass rather than raw counts.
4. **Search the resonance lattice.** Use convergents of `log_2 3` as the only prioritized cycle lengths; attach exact SMT certificates to every eliminated word family.
5. **Search for an unbounded dual potential.** It must be singular near `-1` in `Z_2`; the exact odd-run energy (7.2) is the first coordinate, not the final potential.
6. **Stress-test on `An+B`.** Locate the first parameter where each proposed invariant fails, as required by the Terence Method.

---

# 12. References used for the strategy synthesis

Primary sources include:

- A. Wiles, *Modular elliptic curves and Fermat’s Last Theorem*.
- G. Perelman, *The entropy formula for the Ricci flow and its geometric applications*; *Ricci flow with surgery on three-manifolds*.
- T. Hales, *A proof of the Kepler conjecture*; Hales et al., *A formal proof of the Kepler conjecture*.
- G. Gonthier, *Formal proof—the four-color theorem*.
- A. Marcus, D. Spielman, N. Srivastava, *Interlacing Families II*.
- H. Cohn and N. Elkies, *New upper bounds on sphere packings I*; M. Viazovska, *The sphere packing problem in dimension 8*.
- O. Kozlovski, W. Shen, S. van Strien, *Density of hyperbolicity in dimension one*.
- W. Tucker, *A rigorous ODE solver and Smale’s 14th problem*.
- C. Beltrán and L. Pardo; P. Bürgisser and F. Cucker; P. Lairez on Smale’s 17th problem.
- B. Ben Pham, *An Atlas of the Collatz Conjecture*, especially the realizability and lift-cocycle files.

