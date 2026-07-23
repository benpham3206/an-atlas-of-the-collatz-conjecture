# Collatz rational shadows: an exact two-metric barrier

**Date:** 2026-07-23  
**Status:** proved finite-word theorem and exact verifier. No Collatz proof,
counterexample, or novelty claim.

## Verdict

The rational-to-irrational branch has one exact use and one exact limit.

For each finite parity word, its periodic rational shadow is the real boundary
between descent and non-descent in that complete residue cylinder. A divergent
least counterexample would have to remain on the non-descent side of every such
boundary.

Near the critical slope \(3^s/2^L=1\), this condition has a reciprocal cost. If
a contractive prefix satisfies \(3^s/2^L\to1\), then its rational shadows must
go to \(+\infty\) in the real metric. The same shadows still converge to the
starting integer in the \(2\)-adic metric.

Thus the proposed “rational number with irrational behavior” exists in a
precise form:

\[
x_L\longrightarrow N\quad\text{in }\mathbb Q_2,
\qquad
x_L\longrightarrow+\infty\quad\text{in }\mathbb R
\]

along any near-neutral contractive subsequence of a divergent least
counterexample.

This does not construct that counterexample. It gives an exact test that every
candidate must pass.

## 1. Definitions

Use the Terras map

\[
T(n)=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd}.
\end{cases}
\]

Let \(w=w_0\ldots w_{L-1}\) be a nonempty parity word. Let \(s=|w|_1\). Its
affine composite is

\[
T_w^L(x)=\frac{3^s x+c_w}{2^L},
\qquad c_w\ge0.
\]

Define

\[
\lambda_w=\frac{3^s}{2^L},
\qquad
D_w=2^L-3^s,
\qquad
x_w=\frac{c_w}{D_w}.
\]

Because no positive powers of \(2\) and \(3\) are equal, \(D_w\ne0\).
The number \(x_w\) is the unique rational fixed point of the affine composite.
Its denominator is odd. Direct \(2\)-adic Terras iteration follows \(w\) and
returns to \(x_w\) after \(L\) steps.

## 2. The shadow-barrier theorem

### Theorem 1

For every \(n\in\mathbb Q\cap\mathbb Z_2\) in the parity cylinder \(w\),

\[
\boxed{
T^L(n)-n=(1-\lambda_w)(x_w-n).
}
\tag{1}
\]

Therefore:

1. If \(D_w<0\), then \(x_w\le0\), and every positive state in the cylinder
   satisfies \(T^L(n)>n\).
2. If \(D_w>0\), then \(x_w\ge0\), with equality exactly when \(w=0^L\), and
   \[
   T^L(n)\ge n\iff n\le x_w.
   \]
3. If \(D_w>0\), then the exact strict-rise condition is
   \[
   \boxed{
   T^L(n)\ge n+1
   \iff
   n\le \frac{c_w-2^L}{D_w}.
   }
   \tag{2}
   \]

### Proof

Substitute \(c_w=D_wx_w=2^L(1-\lambda_w)x_w\) into the affine composite:

\[
\begin{aligned}
T^L(n)-n
&=(\lambda_w-1)n+\frac{c_w}{2^L}\\
&=(\lambda_w-1)n+(1-\lambda_w)x_w\\
&=(1-\lambda_w)(x_w-n).
\end{aligned}
\]

If \(D_w<0\), then \(\lambda_w>1\) and \(x_w=c_w/D_w\le0\). Both factors on
the right side of (1) are negative for \(n>0\), so their product is positive.

If \(D_w>0\), then \(1-\lambda_w>0\). The sign comparison in part 2 follows.
Also, \(x_w=0\) exactly when \(c_w=0\), which occurs exactly for the all-zero
word. For the strict-rise condition \(T^L(n)-n\ge1\), apply the affine formula
and multiply by \(2^L\):

\[
c_w-D_wn\ge2^L.
\]

This is equivalent to (2). \(\square\)

## 3. Exact strict-rise pruning

Let \(r_w^+\in[1,2^L]\) be the least positive integer in the residue cylinder
for \(w\). Every positive integer in the cylinder is

\[
n=r_w^++2^Lm,\qquad m\ge0.
\]

For a contractive word, Theorem 1 gives an exact finite count of starts whose
endpoint is strictly larger:

\[
\boxed{
\#\left\{n:T^L(n)\ge n+1,\ Q_L(n)=w\right\}
=
\max\left(
0,\
1+\left\lfloor
\frac{\left\lfloor(c_w-2^L)/D_w\right\rfloor-r_w^+}{2^L}
\right\rfloor
\right).
}
\tag{3}
\]

The entire cylinder is removed from the divergent least-counterexample search
when

\[
\boxed{
c_w<D_wr_w^++2^L.
}
\tag{4}
\]

This does not say that the parity word is absent. The Terras bijection proves
that every finite word occurs. Equation (4) says only that this cylinder cannot
contain a divergent least counterexample, because such a start must rise
strictly at every prefix.

This is stronger than a score that depends only on the parity word, such as its
finite entropy or compression ratio. It decides the full infinite arithmetic
progression selected by that prefix. A parity word alone does not determine
real-valued record height, Benford data, or stopping time for every state in its
cylinder.

Equation (3) is the same finite endpoint inequality used in analytic counts of
“paradoxical” Collatz segments. It does not test whether states repeat inside
the segment. The added structural point is that the cutoff is exactly the
periodic rational shadow \(x_w\).

## 4. The two-metric theorem

### Theorem 2

Assume that \(N\in\mathbb Z_{>0}\) has a nonperiodic orbit and

\[
T^L(N)\ge N\qquad\text{for every }L\ge1.
\tag{5}
\]

For each \(L\), let \(w_L\) be the first \(L\) parity symbols of \(N\), and let
\(x_L=x_{w_L}\).

Then:

1. \(x_L\equiv N\pmod{2^L}\) in \(\mathbb Z_2\). Hence
   \[
   x_L\to N\quad\text{2-adically}.
   \tag{6}
   \]
2. At every contractive prefix,
   \[
   \boxed{
   x_L-N
   =
   \frac{T^L(N)-N}{1-3^{s_L}/2^L}
   \ge
   \frac{1}{1-3^{s_L}/2^L}
   =
   \frac{2^L}{D_L}.
   }
   \tag{7}
   \]
3. If there is a contractive subsequence \(L_k\) with
   \(3^{s_{L_k}}/2^{L_k}\to1\), then
   \[
   x_{L_k}\to+\infty\quad\text{in }\mathbb R,
   \qquad
   x_{L_k}\to N\quad\text{in }\mathbb Q_2.
   \tag{8}
   \]

### Proof

The rational shadow \(x_L\) and \(N\) have the same length-\(L\) parity word.
The finite Terras bijection puts them in the same residue class modulo \(2^L\)
in \(\mathbb Z_2\). This proves (6).

The orbit is nonperiodic, so \(T^L(N)\ne N\). Condition (5) and integrality give
\(T^L(N)-N\ge1\). Apply Theorem 1 and divide by the positive factor
\(1-3^{s_L}/2^L\). This proves (7). The right side of (7) tends to \(+\infty\)
under the stated near-neutral condition, while (6) holds along every
subsequence. \(\square\)

## 5. What this changes

The theorem deletes three weak search requirements.

1. **Finite parity-cylinder scores are not evidence.** Every finite word already
   has a rational periodic impersonator. This statement does not cover
   real-valued orbit statistics that also depend on the starting state.
2. **Near-neutrality is not enough.** A contractive resonance must also pay the
   offset toll (7). A small \(D_L\) makes the toll larger.
3. **Chaos is not the arithmetic gate.** Expansive words make all positive
   starts rise for that finite segment. Only contractive words can prune a
   cylinder.

The remaining divergent-counterexample object must satisfy all of:

\[
\begin{gathered}
N\in\mathbb Z_{>0},\\
T^L(N)\ge N\quad\forall L,\\
x_L\to N\text{ in }\mathbb Q_2,\\
x_L\ge N+\frac{2^L}{2^L-3^{s_L}}
\quad\text{at every contractive prefix}.
\end{gathered}
\tag{9}
\]

The cycle branch stays separate. A cylinder removed from the divergent branch
can still contain a periodic point. If \(T^L(N)=N\), then \(x_L=N\), and the exact
gate is

\[
D_L\mid c_w
\]

with direct parity verification.

## 6. Engineering strategy after the deletion

The next search should operate on proof-carrying prefix records:

\[
(w,L,s,c_w,D_w,r_w^+,x_w).
\]

For each contractive prefix:

1. remove the cylinder from the divergent branch if (4) holds;
2. otherwise emit the finite list from (3);
3. extend only those exact starts or prove a transport rule for the surviving
   language;
4. reject any claim based only on a long excursion;
5. accept a counterexample only with an exact cycle or an infinite divergence
   invariant.

The universal leap remains a well-foundedness theorem:

> Every positive-integer path eventually enters a contractive cylinder that
> satisfies the deletion inequality.

The present theorem does not prove that statement. It identifies the exact
quantity that a proof must control: the affine offset relative to the
periodic-shadow barrier.

## 7. Verification

`collatz_shadow_barrier_verify.py` cross-checks the formulas through distinct
computations:

1. it builds the affine composite;
2. it finds each residue cylinder by direct integer iteration;
3. it iterates the rational shadow and checks exact return;
4. it compares the threshold prediction and formula count with observed direct
   integer rises.

These computations share utility code and are not three independent
implementations. The generated JSON is finite evidence for the implementation.
The symbolic proofs above carry the infinite statements.

## 8. Source boundary

- Bernstein's inverse \(2\)-adic conjugacy supplies the parity-cylinder
  framework.
- Niu's 2026 preprint gives an analytic finite count for paradoxical words. Its
  cutoff equals \(x_w\).
- López and Stoll study rational \(2\)-adic trajectories and the critical
  parity-density boundary.

This note proves its displayed identities directly. It does not depend on a
literature-priority claim or on an unproved statement in those papers.

Primary references:

- Daniel J. Bernstein, *A Non-Iterative 2-Adic Statement of the 3N+1
  Conjecture*: https://doi.org/10.2307/2160415
- Tong Niu, *Parity vectors and paradoxical sequences in the accelerated
  Collatz map*: https://arxiv.org/abs/2605.13886
- Josefina López and Peter Stoll, *The 3x+1 Periodicity Conjecture in
  \(\mathbb R\)*: https://arxiv.org/abs/2101.12747

## STATE

**Established:** periodic rational shadows are exact descent barriers; the
strict-rise candidate count is finite and exact; near-neutral contractive
prefixes force real shadow escape while preserving \(2\)-adic convergence.

**Not established:** an infinite-path exclusion, a new positive cycle, or a
divergent positive integer.

**Next cheapest theorem:** classify a structured critical language by proving
that every infinite path either triggers (4) or has infinitely many nonzero lift
digits.

## Public-atlas placement

The public atlas separates proved contributions from exploratory work. This
packet extends its affine-word, realizability, and lift-cocycle spine. It does
not alter the public repository. If imported, it belongs in `exploratory/`
until its proof review and verifier are recorded in the repository's
verification format.
