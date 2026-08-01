# Automatic parity words cannot encode non-cyclic rational trajectories

**Date.** 2026-08-01.
**Branch served.** Rigidity.
**Status.** Proved corollary of López–Stoll (2021) and Bell (2020).
**Scope.** Rational 2-adic starting states, including all positive integers.

## Verdict

> **Theorem.** Let `x ∈ ℚ ∩ ℤ₂`. If the trajectory of `x` under the Terras
> map is not eventually cyclic, then its parity word is not `k`-automatic for
> any integer base `k ≥ 2`.

Consequently, no divergent positive Collatz orbit has an automatic parity
word. This closes the full automatic class. It also closes every
uniform-morphic parity-word target, because a coding of a fixed point of a
`k`-uniform morphism is `k`-automatic.

This does **not** prove the Collatz conjecture. The critical-density class for
arbitrary, non-automatic words remains open. Cycle exclusion remains a
separate obligation.

## Inputs

Let `q = (q_n)_{n≥0}` be the parity word and put

\[
s_L=\sum_{n<L}q_n,\qquad
\alpha=\frac{\log 2}{\log 3}=\log_3 2.
\]

1. **López–Stoll.** If a rational 2-adic integer has a non-cyclic
   `3x+1` trajectory, then
   \[
   \liminf_{L\to\infty}\frac{s_L}{L}=\alpha.
   \]
   Source: J. López and P. Stoll, [*The 3x+1 Periodicity Conjeture in
   \(\mathbb R\)*](https://arxiv.org/abs/2101.12747), arXiv:2101.12747
   (2021), abstract and stated constraint. Last checked: 2026-08-01.

2. **Bell.** If `S ⊆ ℕ` is `k`-automatic, then its lower
   and upper asymptotic densities are recursively computable rational numbers.
   Source: J. P. Bell, [*The upper density of an automatic set is
   rational*](https://doi.org/10.5802/jtnb.1135), J. Théorie des Nombres de
   Bordeaux 32 (2020), Corollary 1.2. Last checked: 2026-08-01.

3. **Elementary arithmetic.** `α` is irrational. If `α = a/b ∈ ℚ` with
   positive integers `a,b`, then `2^b = 3^a`, contrary to unique
   factorization.

## Proof

Assume that `x ∈ ℚ ∩ ℤ₂` has a non-cyclic trajectory and that its parity word
`q` is `k`-automatic. Define

\[
S=\{n\in\mathbb N:q_n=1\}.
\]

Because `q` is `k`-automatic, `S` is a `k`-automatic set. Bell's
Corollary 1.2 gives

\[
\underline d(S)
=\liminf_{L\to\infty}\frac{|S\cap[0,L)|}{L}
=\liminf_{L\to\infty}\frac{s_L}{L}
\in\mathbb Q.
\]

López–Stoll give the same lower density as `α = log₃2`. But `α ∉ ℚ`. This is
a contradiction. Therefore `q` is not `k`-automatic. The base `k ≥ 2` was
arbitrary. ∎

## What this changes

- `PRIORITY.md` §7 stopped at “a divergent 2-automatic transcript has no
  natural density.” Bell's theorem controls the **lower density even when the
  natural density does not exist**. That closes the residual case.
- The 26 three-state survivors and all larger bounded-DFAO censuses are no
  longer open Collatz candidates. Their lower density cannot equal
  `log₃2`.
- The ten ternary-coded uniform-morphic survivors are closed by this
  corollary. The Mahler tower remains useful machinery, but is not needed for
  their Collatz exclusion.
- The automatic-transcript target is complete for every base, not only base
  2 and not only bounded automaton size.

## Prior-art and novelty status

Both load-bearing theorems are published or publicly available prior work.
The contribution here is their direct synthesis at the exact Collatz parity
density. A targeted search on 2026-08-01 found Bell's theorem and found no
source stating this Collatz corollary. That negative search is not a priority
claim. A symbolic-dynamics referee should check novelty before publication.

## Acceptance check

The proof has four type checks:

1. A binary `k`-automatic word has a `k`-automatic support set.
2. Bell's lower density uses the same prefix count `s_L/L`.
3. López–Stoll's constraint applies to rational non-cyclic trajectories.
4. Every divergent positive-integer trajectory is rational and non-cyclic.

No finite computation, floating-point estimate, or unproved repository lemma
enters the proof.

## Corollary for general morphic words

> **Corollary.** Let `x ∈ ℚ ∩ ℤ₂` have a non-cyclic trajectory. If its parity
> word is morphic, then its natural one-frequency does not exist.

**Proof.** If the natural one-frequency exists, López–Stoll force it to equal
`α = log₃2`. The frequency of a letter in a morphic word, when it
exists, is algebraic (Allouche–Shallit, *Automatic Sequences*, Theorem 8.4.5;
last checked 2026-08-01). But `α` is transcendental: it is irrational by unique
factorization, and if it were algebraic irrational then the
Gelfond–Schneider theorem would make `3^α` transcendental, whereas `3^α = 2`.
Contradiction. ∎

This does not close all morphic words. A morphic word need not have a natural
letter frequency. Bell 2008, [Theorem 1.1](https://doi.org/10.5802/jtnb.625)
(last checked 2026-08-01), proves that its logarithmic letter frequency always
exists. López–Stoll constrain the lower natural frequency, not the logarithmic
frequency. Crossing that mismatch would require a new theorem.
