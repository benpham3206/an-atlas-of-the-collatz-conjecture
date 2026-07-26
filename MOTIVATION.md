# Motivation

This document states why this work exists. It uses controlled technical
language: short sentences, plain terms, one statement at a time.

## 1. Purpose

This repository is a test case. The goal is a repeatable method to attack
hard problems. The Collatz conjecture is the first problem under test. The
method is the product. Collatz is the sandbox.

## 2. Why Collatz

The Collatz rule is simple. A check of one example is simple. A general proof
is hard. This gap is the reason to use Collatz.

- A simple rule keeps the setup clear.
- A hard proof exposes the true cost of proof search.

A problem with this gap shows what real proof work requires. It does not hide
that cost behind a complex definition.

## 3. Why the problem is worth proving

The value of the Collatz conjecture comes from what it represents. It does
not come from the statement alone.

### 3.1 A simple problem that resists every known technique

State the rule in one sentence:

- If `n` is even, divide by 2.
- If `n` is odd, compute `3n+1`.
- Repeat.

The claim is that every positive integer reaches 1.

Most famous problems need years of background before a reader can understand
them. Collatz does not. A middle-school student can understand it in minutes.
No proof and no counterexample exists after decades of work. This mismatch
between simplicity and difficulty is unusual.

### 3.2 It shows the limits of current mathematics

Researchers have studied Collatz from many directions. Examples: number
theory, dynamical systems, probability, ergodic theory, graph theory,
computation, symbolic dynamics, and 2-adic analysis.

Many methods find partial structure. No method controls every trajectory.

A proof needs one of the following:

- a powerful new theorem;
- a new way to analyse discrete dynamical systems;
- an unexpected synthesis of known ideas.

### 3.3 A model problem for deterministic complexity

The map is deterministic. Every integer has exactly one next step. The
trajectories still look almost random:

- nearby integers behave very differently;
- trajectories rise and fall without a visible pattern;
- stopping times vary by large amounts.

Simple rules that make complicated behaviour are a recurring subject in
mathematics and in theoretical computer science.

### 3.4 It connects many areas

The statement is simple. The problem still touches modular arithmetic, powers
of two, binary representations, Diophantine equations, dynamical systems,
graph theory, symbolic sequences, p-adic and 2-adic analysis, and
computational complexity.

A proof can show new relations between these subjects.

### 3.5 It tests methods for hard problems

Treat Collatz as a laboratory, not as an isolated puzzle. The questions are
general:

- How do you organise a search through infinitely many cases?
- How do you classify all possible behaviours?
- How do you remove whole families of counterexamples?

Methods that succeed here can transfer to other problems. This holds even if
the conjecture itself has no consequence.

### 3.6 It teaches care about intuition

Most people expect the problem to be easy at first. Then they find three
facts:

- computation confirms the conjecture over very large ranges (`n < 2^71`);
- many convincing heuristic arguments exist;
- no heuristic argument is a proof.

This gives a central lesson. **Strong evidence is not proof.** The same
lesson governs this repository: a measurement is labelled a measurement.

### 3.7 Either outcome adds knowledge

Two results are possible.

- If the conjecture is true, the proof can show a hidden invariant or a
  monotone quantity. Researchers have looked for such a quantity for decades.
- If the conjecture is false, an explicit positive integer never reaches 1.
  That result overturns the common expectation. It also raises a new
  question: why was computation so misleading?

Each outcome increases understanding.

### 3.8 Applications are not the reason

Collatz has no expected direct application. Compare it with problems that
led to public-key cryptography or to error-correcting codes. Nobody works on
Collatz for a technical benefit.

The value is intellectual:

- the problem is exceptionally clean;
- it sits at the boundary of current proof methods;
- it tests our understanding of simple deterministic systems.

For these reasons many mathematicians treat Collatz as a benchmark. A
solution does more than answer one question. It shows that we have learned a
new way to reason about a class of problems that current methods cannot
reach.

## 3.9 The shape of what is left, measured

The 2026-07-25 priority search collapsed the remaining symbolic gap to a
single number. Write `s_L` for the number of ones in the first `L` symbols of
a parity word and `α = log₃2`. The band `liminf s_L/L < α` is closed
(drift wall; Monks–Yazinski) and the band `liminf s_L/L > α` is closed
(López–Stoll 2021). What survives is the set

```
G = { q ∈ {0,1}^ℕ  :  liminf_L s_L(q)/L = α }.
```

`G` can be measured, and the measurement is worth stating because it explains
the failure of an entire class of method.

**It is null.** Under the uniform Bernoulli measure on `{0,1}^ℕ` — equivalently
Lebesgue measure on `[0,1]` under binary expansion — almost every word has
one-density `1/2 ≠ α`. So `G` has measure zero.

**It is nearly full-dimensional.** `G` contains the Besicovitch–Eggleston level
set `{q : lim s_L/L = α}`, whose Hausdorff dimension is the binary entropy
`H(α)` (Besicovitch 1934; Eggleston 1949). Hence

```
dim_H(G)  ≥  H(α)  ∈  ( 0.949952152 , 0.949957233 ).
```

Those bounds are exact rationals, each certified by a single integer
comparison — `a/b < log₃2 ⟺ 3^a < 2^b` for `α`, and
`−log₂(p/q) ≥ c/d ⟺ p^d·2^c ≤ q^d` for the entropy terms. The decimals are
renderings of the exact bounds, not the certificate.
Verifier: [`contribution/code/dimension_bracket.py`](contribution/code/dimension_bracket.py).

**Why this matters.** The two facts together are a structural diagnosis, not a
curiosity:

- **Density and measure methods are blind to `G` by construction.** Tao's
  theorem is a statement about logarithmic density; `G` is null. No sharpening
  of a density estimate can ever see a null set. This is a category mismatch,
  not a weak constant — and it is the precise reason the amplification branch
  of the proof architecture has never been entered.
- **`G` is not thin enough to dismiss.** Dimension at least `0.9499…` out of a
  possible `1`. One cannot argue that the survivors are degenerate or
  exceptional in any dimensional sense.

A set that is invisible to measure and nearly full in dimension is exactly the
kind of object for which one needs a pointwise, arithmetic instrument rather
than a statistical one. That is the whole reason this repository's surviving
result constrains factor complexity rather than letter frequency.

**Not established.** Results on irregular sets (Barreira–Schmeling 2000) suggest
`dim_H(G)` may be exactly `1`, since `G` contains words whose Birkhoff average
does not exist. This repository has not verified a citation giving that for
this specific level set. The lower bound `H(α)` is the part that is solid.


## 4. Origin

The problem first appeared on a whiteboard. The place was a multivariable
calculus workshop. The contrast between the simple rule and the hard proof
started this work.

## 5. Method principle

Treat a proof as a constraint system. Every definition, lemma, and result
must agree with every other one. One mismatch breaks the whole structure.

The following rules follow from this principle:

- Each result uses exact integer or rational arithmetic.
- Each result carries an independent check.
- Each result records its provenance.
- A measurement is labelled as a measurement, not as a theorem.

## 6. Working rule

Progress is the target. A single breakthrough is not the target.

- Add small results. Each result must be rigorous and verifiable.
- Enough verified progress raises the chance of a breakthrough.
- In some cases, enough verified progress forces a breakthrough.

## 7. Scope beyond Collatz

The method matters more than the single problem. The same method applies to
other hard problems. Examples:

- P versus NP.
- Proof search.
- Counterexample classification.
- A record of the reasoning process.

Collatz is the current test. The method is the transferable result.
