# Elements of Metadynamical Geometry

> A Euclid-style seed for a possible mathematics of changing laws.  
> Definitions come before metaphors; axioms are provisional until examples force them.

---

## How to read this

Ordinary dynamics asks how a state changes while its governing law stays fixed.
**Metadynamical geometry** asks what can be said when the state and the governing
law are both treated as mathematical coordinates.

This document is a founding sketch, not a novelty claim. Its terms must earn their
place by producing computable examples, invariants, and theorems that are not merely
old results with `hyper-` added to their names.

**Current audit status (2026-07-19):** the broad sketch does not yet clear that
bar. Most of its initial objects coincide with established parameterized dynamics,
fibered spaces, structural stability, and mechanics. Keep this document as a
research scaffold, not as evidence that a new field has been founded. The first
surviving candidate is the narrower study of how exact certificates persist or
fail under declared transports.

---

## Book 0 — Definitions

**Definition 1 (state space).**  
A **state space** `X` is a collection of possible states of a system.

**Definition 2 (law).**  
A **law** `λ` specifies which change of state is allowed. In discrete time it may
be a map `F_λ : X_λ → X_λ`. In continuous time it may specify a velocity at each
state.

**Definition 3 (law-space).**  
A **law-space** `L` is a collection of laws together with a declared notion of
when two laws are near, equivalent, or comparable.

Merely listing formulas does not make a law-space. The comparison rule is part of
the object.

**Definition 4 (hyperstate).**  
A **hyperstate** is a pair

```text
h = (λ, x)
```

where `λ ∈ L` is a law and `x ∈ X_λ` is a state governed by that law. Memory may be
included as a third coordinate when the next state depends on history.

**Definition 5 (hyperspace).**  
The **hyperspace** of the family is

```text
H = { (λ, x) : λ ∈ L and x ∈ X_λ }.
```

Each fixed law contributes one sheet `H_λ = {λ} × X_λ`. The whole hyperspace binds
the sheets into one object.

**Definition 6 (transport).**  
A **transport** from law `λ` to law `μ` is an explicit rule for comparing states,
orbits, observables, or proofs belonging to `λ` with those belonging to `μ`.

Without transport, the phrase “the same behavior under another law” has no fixed
meaning.

**Definition 7 (hypertrajectory).**  
A **hypertrajectory** is a path

```text
t ↦ (λ(t), x(t))
```

whose state component obeys the law currently named by `λ(t)`. An ordinary
trajectory is the special case in which `λ(t)` is constant.

**Definition 8 (observable and hypercollision).**  
An **observable** `O` records only the behavior an investigator chooses to see.
Two laws **hypercollide under O** when their recorded behavior is identical even
though the laws themselves are distinct.

**Definition 9 (structure).**  
A **structure** `S` is a declared property to be transported across law-space: a
cycle, invariant, terminating behavior, proof certificate, symmetry, or other
specified object.

**Definition 10 (hyper-inertia of a structure).**  
Given a distance `d` on law-space, the **hyper-inertia** of `S` at `λ` is the
smallest law-change that destroys `S`:

```text
I_S(λ) = inf { d(λ, μ) : the transported structure S fails at μ }.
```

Large hyper-inertia means structural robustness. Zero hyper-inertia means that
arbitrarily small changes of law can destroy the structure.

**Definition 11 (hypervelocity and hypermomentum).**  
The velocity of a differentiable hypertrajectory has a state part and a law part:

```text
V = (state change, law change).
```

If the hyperspace carries an inertia operator `G_h`, its candidate
**hypermomentum** is

```text
P = G_h(V, ·).
```

The name “momentum” is provisional. It becomes permanent only when a symmetry of
hyperspace yields a conservation or transport law for `P`.

**Definition 12 (hyperplane).**  
A **hyperplane** is a constraint sheet cut out by one admissible condition, such as
all hyperstates with a fixed coefficient, invariant, or conserved quantity. When
the ambient space is not linear, **constraint sheet** is the preferred term.

---

## Book 0 — Common notions

1. Different laws can produce the same finite observations.
2. A small change in a law can produce either a small or a catastrophic change in behavior.
3. Similar-looking trajectories do not by themselves justify transporting a proof.
4. A quantity depending only on arbitrary coordinates is not an intrinsic property of the system.
5. A general theory must recover fixed-law mathematics when movement through law-space is forbidden.
6. A new name earns its place only when it shortens a definition, exposes an invariant, or enables a theorem.

---

## Book 0 — Postulates

**Postulate 1 (declared family).**  
Every investigation declares its law-space, state spaces, and evolution rules.

**Postulate 2 (declared comparison).**  
Every comparison between different laws names the transport or observation that
makes the comparison meaningful.

**Postulate 3 (fixed-law reduction).**  
Holding the law coordinate fixed recovers the corresponding ordinary dynamical
system without modification.

**Postulate 4 (invariance under renaming).**  
Relabeling states or law coordinates cannot change an intrinsic metadynamical
statement.

**Postulate 5 (operational vocabulary).**  
Every proposed hyper-quantity must be computable in at least one finite example
or characterized by a precise existence statement.

---

## Book I — First propositions

### Proposition 1 — Ordinary dynamics is a fixed-law sheet

Every trajectory of `F_λ` is a hypertrajectory contained entirely in `H_λ`.

*Proof.* Choose `λ(t) = λ` for all time and let the state component follow `F_λ`.
The resulting pair satisfies Definition 7. ∎

### Proposition 2 — Finite observational collision is an equivalence relation

Fix one observation rule `O`. Define `λ ~ μ` when `O(λ) = O(μ)`. Then `~` is
reflexive, symmetric, and transitive.

*Proof.* These are the three corresponding properties of equality. ∎

**Corollary.** A finite collection of laws is partitioned into observationally
indistinguishable classes.

### Proposition 3 — Positive hyper-inertia gives a stable neighborhood

If `I_S(λ) > r`, then `S` survives under every law `μ` satisfying `d(λ, μ) ≤ r`.

*Proof.* If `S` failed at such a `μ`, the infimum in Definition 10 would be at most
`r`, contradicting `I_S(λ) > r`. ∎

### Proposition 4 — Zero hyper-inertia is structural fragility

If `I_S(λ) = 0`, then for every positive scale `ε` there are laws within `ε` of
`λ` at which the transported structure fails, provided the failure set is
nonempty.

*Proof.* This is the defining property of the infimum being zero. ∎

---

## Book II — First proving ground: Collatz-type laws

Consider the family

```text
T_(a,b)(n) = n / 2          when n is even
             (a n + b) / 2  when n is odd,
```

with positive odd parameters chosen so that the map remains on positive whole
numbers. The accelerated Collatz rule is the fixed-law sheet `(a,b) = (3,1)`.

This family supplies immediate metadynamical questions:

1. Which orbit structures persist as `(a,b)` changes?
2. When do different laws hypercollide under a bounded observation?
3. How far is `(3,1)` from a law with a new cycle?
4. Which proof certificates transport between neighboring laws?
5. Which symbolic paths are imaginable but not realizable by any positive integer?

The fold program already uses two local terms:

- **drift** — Ben's “hyper-momentum”: net displacement encoded by a parity word;
- **run inertia** — Ben's “hyper-inertia”: the length of a forced parity run.

These remain Collatz-specific quantities. They are examples for the broader theory,
not yet identified with Definitions 10–11. Any identification must be proved.

---

## Book III — Founding problems

1. **Transport:** construct a non-arbitrary way to move states and proofs between laws.
2. **Rigidity:** decide when observable behavior determines the underlying law.
3. **Stability:** compute or bound hyper-inertia for a named structure.
4. **Collision:** classify distinct laws with identical bounded behavior.
5. **Curvature:** determine whether transporting a structure around a loop changes it.
6. **Conservation:** find a law-space symmetry that earns hypermomentum its name.
7. **Realizability:** distinguish formally describable paths from paths produced by actual states.

**First theorem target.** Build a finite family of deterministic laws for which
hypercollisions can be classified exactly and a nonzero hyper-inertia can be
computed without choosing arbitrary coordinates.

---

## Book IV — Kill criteria

Metadynamical geometry has not become a distinct field if:

1. every definition is merely a renamed result from parameterized dynamical systems;
2. its quantities change under harmless relabeling;
3. no hyper-inertia can be computed outside a hand-picked example;
4. transport means only that two pictures look similar;
5. hypermomentum has no symmetry, conservation, or composition law;
6. the framework produces vocabulary but no shorter proof or new theorem.

---

## Definition ledger

| Term | Status | What would make it permanent |
| --- | --- | --- |
| law-space | provisional | supports a coordinate-free comparison theorem |
| hyperstate | provisional | simplifies at least two independent systems |
| transport | required | admits composition and identity laws |
| hypercollision | provisional | yields a useful classification result |
| certificate persistence | candidate | computed intrinsically in two unrelated systems |
| hyper-inertia | historical nickname only | replace with a precise domain-specific quantity |
| hypermomentum | rejected for now | reconsider only after a symmetry yields conservation |
| hyperplane | existing term | use only for a genuine codimension-one constraint |

**One-line checkpoint:** The proposed subject studies which behaviors, structures,
and proofs survive when the governing law itself becomes a variable.

---

## Book V — Reasoning discipline and first stress test

Metadynamical work separates three modes of reasoning:

1. **Abduction** proposes the best current explanatory mechanism.
2. **Induction** maps examples, patterns, failures, and empirical boundaries.
3. **Deduction** proves what follows and controls promotion into the permanent ledger.

No inductive pattern becomes a theorem, and no abductive vocabulary becomes a
field merely because it is evocative.

The first stress test is the Collatz transcript lift tower. A length-`L` parity
prefix determines one residue `r_L mod 2^L`. Neighboring levels transport by

```text
r_(L+1) = r_L + epsilon_L * 2^L,  epsilon_L in {0,1}.
```

The lift bits are the binary digits of the associated 2-adic state. Positive
ordinary realization is exactly eventual-zero lift support with a positive
stabilized residue. This is proved and probed in
[`fold/fence/LIFT_COCYCLE.md`](../fold/fence/LIFT_COCYCLE.md).

This example does not establish a new geometry. It demonstrates the required
workflow: a metaphor is reduced to an exact transport, the transport produces a
computable object, and the object survives only if it supports a theorem or a
falsifiable next question.
