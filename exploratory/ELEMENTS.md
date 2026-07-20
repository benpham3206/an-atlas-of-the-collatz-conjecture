# Elements of Collatz — A Euclid-Style Research Spine

> For readers who think in systems, not symbols.  
> Each section builds on the last. Jargon is defined before it is used.

---

## How to read this (Euclid's method)

Euclid did not jump to the hard claim. He built a chain:

1. **Definitions** — name the objects
2. **Common notions** — obvious truths everyone accepts
3. **Postulates** — rules you agree to assume
4. **Propositions** — statements proved step by step from (1–3)
5. **Corollaries** — easy consequences of a proposition

We do the same for Collatz. Hard modern work (Tao, cycles, carry problems) sits **inside** propositions — not at the front door.

**Your job as an engineer-reader:** check each link in the chain. If a step feels unmotivated, that is a research gap, not a personal failure.

---

## Book 0 — Definitions

**Definition 1 (Collatz step).**  
Start with a positive whole number `n`.

- If `n` is even → replace it with `n / 2` (halve it).
- If `n` is odd → replace it with `3n + 1` (triple and add one).

Repeat. This is one **step**. A sequence of steps is an **orbit**.

*Engineering picture:* a **state machine**. Even states transition by `/2`. Odd states transition by `3n+1`. No randomness — the next state is fixed.

**Definition 2 (Stopping).**  
An orbit **stops** (for our purposes) when it hits `1`. After that it loops `1 → 4 → 2 → 1` forever.

**Definition 3 (The conjecture).**  
**Collatz conjecture:** every starting number eventually hits `1`.

**Definition 4 (Counterexample).**  
If the conjecture is false, one of two things happened:

```text
counterexample
├── cycle     — you return to the same number (not the 1-loop)
└── divergent — values grow without bound forever
```

**Definition 5 (Shortcut form).**  
Engineers often prefer fewer states. Combine “odd then even” into one jump:

- Odd `n` → go to `(3n + 1) / 2` in one step (still a whole number).

This is the **odd-only / Syracuse** view. Same physics, fewer transitions.

**Definition 6 (Dangerous behavior).**  
Some symbolic patterns would let an orbit **avoid sinking** toward 1. We classify them:

```text
dangerous behavior
├── finite burst          — scary for a while, then recovers
├── periodic              — repeats a bad block forever
├── eventually periodic   — bad block repeats after a prefix
└── nonperiodic           — bad pattern never settles into a repeat
```

---

## Book 0 — Common notions

1. Halving makes a number smaller. Tripling-and-adding makes it larger.
2. On “average,” odd steps are followed by several halvings — like a pump that pushes up, then a relief valve that dumps down.
3. Checking millions of cases is evidence, not proof — like fatigue-testing parts: no failure yet ≠ infinite life.
4. A proof must cover **all** starting values, including ones never tested.

---

## Book 0 — Postulates (what we accept to start)

**Postulate 1.** The step rules are deterministic.  
**Postulate 2.** Every orbit is a sequence of positive integers (until you might diverge — that is what we are testing).  
**Postulate 3 (exhaustive classification).** Any counterexample is either a **cycle** or a **divergent** orbit. No third kind.

---

## Book I — Propositions already proved (firm ground)

### Proposition 1
`1` is a fixed point of the loop `1 → 4 → 2 → 1`.

*Proof sketch:* Apply the rules directly.

### Proposition 2
Every power of two (`2, 4, 8, 16, …`) reaches `1` by repeated halving only.

*Engineering picture:* pure drainage — no pump steps, only valves opening.

### Proposition 3 (empirical, not logical proof)
No counterexample has been found below roughly `2.36 × 10^21` in computer searches.

*Status:* strong **evidence**, like a huge test campaign with zero failures. Not a certificate for all sizes.

### Proposition 4 (Tao, 2019 — explained plainly)

**What Tao proved:**  
For **almost all** starting numbers (in a specific statistical sense called *logarithmic density*), the orbit eventually dips below **any** slowly-growing bound you name.

**Concrete example Tao gives:** for almost all `n`, the smallest value your orbit ever reaches is less than:

```text
log(log(log(log(n))))
```

That is absurdly tiny relative to `n` — four nested logarithms.

**What this does NOT prove:**

- Not **every** number — exceptions might exist (like a few bad parts in a batch that pass inspection but fail in the field).
- Not that you hit **exactly** `1` — only that the orbit gets very small somewhere.
- Not that divergent orbits are impossible.

**Engineering picture:** Tao showed that for a **measure-zero-but-still-huge** subset of the design space, trajectories **dissipate energy** into a small basin. The full conjecture requires **every** trajectory to drain to the same attractor (`1`).

**Tao's tool (named once, then plain):** He studied the **Syracuse** (odd-only) map using **3-adic** structure — think of it as analyzing carry/borrow patterns in a number system based on powers of 3, the way digital logic analyzes bits in base 2.

```text
TAO_BRANCH
│
├── Almost all orbits get arbitrarily small (log density)
│   └── ✅ Closed (Tao 2019)
│
├── Every orbit hits exactly 1
│   └── ⏳ Open — not proved
│
└── Maps to master tree
    └── Divergent orbits — partial progress only
        Does NOT close W carry wall or nonperiodic branch
```

---

## Book II — The counterexample progress tree (your framework)

This is the **failure-mode analysis** diagram for Collatz.

```text
COLLATZ COUNTEREXAMPLES
│
├── 1. Nontrivial cycles
│   │
│   ├── Dangerous periodic cycles
│   │   └── ✅ Closed
│   │       Dangerous repeating blocks force a negative fixed point.
│   │
│   └── Safe/non-dangerous cycles
│       └── ⏳ Open
│           Only known cycle is 1 → 1 in odd-only form.
│
└── 2. Divergent orbits
    │
    ├── Finite dangerous bursts
    │   └── ✅ Clarified
    │       They can occur, but finite bursts alone do not threaten Collatz.
    │       The real issue is indefinite non-descent.
    │
    ├── Eventually periodic dangerous behavior
    │   └── ✅ Closed
    │       Same negative fixed-point obstruction.
    │
    └── Nonperiodic dangerous behavior
        └── ⏳ Main open frontier
            │
            ├── General case
            │   └── ⏳ Collatz-level hard
            │
            └── Specific candidate W
                W = (1,2),(1,1,2),(1,1,1,2),...
                │
                ├── ✅ If W is real, it diverges → Collatz false
                ├── ✅ Reduced to recurrence:
                │       s_{m+1} = (3^{m+1}s_m + 1) / 2^{m+3}
                ├── ✅ Reduced to carry problem:
                │       W realized ⇔ carries eventually vanish
                │       W eliminated ⇔ carries nonzero infinitely often
                └── ⏳ Current wall: do carries vanish or not?
```

**Status bar**

```text
Odd-only exponent model                ✅ done
Dangerous block idea                   ✅ done
Periodic dangerous paths               ✅ closed
Eventually periodic dangerous paths    ✅ closed
Finite bursts clarified                ✅ done
2-adic vs positive integer split       ✅ done
W candidate formalized                 ✅ done
W recurrence derived                   ✅ done
W carry obstruction                    ⏳ open
General nonperiodic dangerous paths    ⏳ open
Full Collatz proof/disproof            ⏳ open
```

**One-line checkpoint:** Periodic escape routes are closed. The serious branch is **nonperiodic dangerous behavior**. Candidate `W` reduces to: **do binary carries eventually stop happening?**

---

## Book III — How mathematicians kill “impossible” problems

Plain pattern language — no idol worship, just workflow.

### Pattern A — Change the question (reduction)

**Example: Wiles and Fermat (1995)**

- **Original problem:** “No three positive integers solve `a^n + b^n = c^n` for `n > 2`.”
- **What Wiles actually proved:** a deep statement about **elliptic curves** and **modular forms** — different objects entirely.
- **Bridge:** If Fermat had a counterexample, you could build a special curve that would break that deep statement. So proving the deep statement kills Fermat.

*Engineering analogy:* You cannot prove a bracket won't fail by staring at the bracket. You prove a **material constitutive law** that the bracket must obey. Violating the bracket would violate the law.

**Collatz lesson:** Look for a **master theorem** such that Collatz is a corollary. Tao's work is a **partial** master theorem (almost all orbits shrink).

### Pattern B — Prove “almost all,” then fight exceptions

**Example: Tao on Collatz (2019)**

- Prove a property for **99.999…%** of cases using probability + structure.
- The hard core is the **exception set** — often measure-zero but mathematically stubborn.

*Engineering analogy:* Six-sigma quality — the tail of the distribution is where failures live.

### Pattern C — Classify failures exhaustively

**Example: Your counterexample tree**

- List every way the system can fail (cycle vs diverge).
- Close branches one at a time (periodic dangerous paths ✅).
- Name the **one wall** left (W carry problem).

*Engineering analogy:* **FMEA** — Failure Mode and Effects Analysis. Same discipline.

### Pattern D — Build infrastructure for decades

**Example: Fermat took 350 years**

- New fields were invented (ideal numbers, modular forms) because the old tools broke.
- The final proof used machinery that did not exist when the problem was posed.

*Engineering analogy:* You cannot CFD a wing in 1903. You build the wind tunnel first.

### Pattern E — Formalize small lemmas (Elements style)

**Example: Euclid, modern Lean/proof assistants**

- Big claim = chain of small, checkable steps.
- Each proposition depends only on earlier propositions.

*Engineering analogy:* **Drawing tree + BOM** — every part traceable to a spec.

---

## Book IV — Engineering lenses on Collatz

Each lens is an **attack angle**. Rendered as a progress subtree.

### Lens 1 — Dynamical systems (your strongest native language)

```text
DYNAMICAL_SYSTEMS_LENS
│
├── State x_n, update rule f(x)
│   └── ✅ Collatz is a discrete-time dynamical system
│
├── Attractor at x = 1
│   └── ⏳ Open — prove every orbit enters basin of 1
│
├── Lyapunov / energy function V(n) with V decreasing
│   └── ❌ Dead for simple V
│       No known simple "energy" that drops every step
│       (stmt_modular_obstruction in project)
│
└── Tao's almost-all dissipation
    └── ✅ Partial — statistical descent, not universal
```

*Plain language:* You want a **Lyapunov function** — like total energy that always drops. Collatz refuses a simple one. That is the heart of the difficulty.

**3D picture you asked for:** Plot `(n, step index k, log n)` — a **phase-space trajectory**. Most paths look like a ball bouncing down a staircase. A counterexample would be a trajectory that climbs forever or cycles in a weird loop.

### Lens 2 — Control / feedback

```text
CONTROL_LENS
│
├── Odd step = positive feedback (gain > 1)
├── Even steps = negative feedback (gain < 1)
│   └── ✅ Heuristic average gain < 1 explains why most paths sink
│
├── Worst-case stability (every trajectory)
│   └── ⏳ Open — average-case ≠ worst-case
│
└── Connection to W
    └── ⏳ Nonperiodic dangerous path = sustained bad feedback schedule
```

*Plain language:* Odd steps are **excitation**; even halvings are **damping**. Collatz asks: can damping always win? W is a candidate **persistent excitation pattern**.

### Lens 3 — Graph theory

```text
GRAPH_LENS
│
├── Forward graph: n → next(n)
│   └── ✅ Well-defined directed graph on positive integers
│
├── Reverse tree from 1
│   └── ⏳ Open — if reverse tree covers all n, conjecture true
│
├── Collatz as functional graph with out-degree 1
│   └── ✅ Every node has exactly one forward edge
│
└── 3D graph visualization
    └── 🔍 Exploring — layout (n, depth, log n) for intuition only
```

*Plain language:* Draw arrows from each number to its next value. The question is whether **all roads lead to Rome (1)**. The **reverse** picture — work backward from 1 — is often easier to imagine.

### Lens 4 — Number theory (integers and divisibility)

```text
NUMBER_THEORY_LENS
│
├── mod 2 behavior (parity)
│   └── ✅ Even/odd split is the whole game
│
├── mod 2^k patterns (carry structure)
│   └── 🔍 Exploring — linked to W carry wall
│
├── 2-adic vs positive integer
│   └── ✅ Split understood
│       Every symbolic path has a 2-adic story;
│       hard part is realizing it as a positive integer orbit
│
└── Weak Collatz (cycle-only variant)
    └── ⏳ Open — cycles tied to equations with 2^a and 3^k
```

*Plain language:* Collatz is a **divisibility machine** — when does `/2` fire, how many times, and what carries propagate? W asks whether carries **die out** or **keep firing forever**.

### Lens 5 — Topology (careful — not always the right word)

```text
TOPOLOGY_LENS
│
├── Classical shapes (holes, genus, manifolds)
│   └── ❌ Dead as direct approach
│       No one has a natural manifold whose topology encodes Collatz
│
├── Dynamical topology / attractors
│   └── 🔍 Exploring — basin of attraction around 1
│
├── Profinite / p-adic topology (Tao's actual turf)
│   └── ✅ Framework exists
│       "Closeness" defined by congruence mod 3^n, not distance in R³
│
└── Engineering honesty
    └── 3D plots are visualization, not the proof object
```

*Plain language:* When mathematicians say "topology" here, they often mean **which points are near each other in a number-theoretic sense** (same remainder mod `3^n`), not rubber-sheet geometry. Your 3D plots help **intuition**, not certification.

### Lens 6 — Group theory

```text
GROUP_LENS
│
├── Collatz map is not a group homomorphism
│   └── ❌ Dead for naive group actions
│
├── 3-adic cyclic groups in Tao's proof
│   └── ✅ Used in serious analysis (Syracuse random variables)
│
└── Symmetry hunting
    └── 🔍 Exploring — limited symmetries beyond parity
```

### Lens 7 — Calculus / analysis

```text
ANALYSIS_LENS
│
├── Continuous analogue of Collatz
│   └── 🔍 Exploring — smooth maps can have different behavior;
│       discrete problem stays harder
│
├── Log-space random walk heuristic
│   └── ✅ Explains almost-all descent heuristically
│
└── Tao's rigorous analysis
    └── ✅ Almost-all bound via renewal processes + characteristic functions
```

### Lens 8 — Complex analysis

```text
COMPLEX_ANALYSIS_LENS
│
├── Extend n to complex plane
│   └── 🔍 Exploring — beautiful pictures, unclear proof path
│
├── Direct line to Collatz resolution
│   └── ❌ No known bridge theorem
│
└── Role in project
    └── Intuition / visualization only unless a reduction appears
```

---

## Book V — Building on Tao (your next steps as an engineer)

Tao gave you a **downhill guarantee for almost all starts**. Your tree says the **remaining threat** is **nonperiodic dangerous behavior**, especially candidate **W** and its **carry wall**.

**Sensible build order:**

1. **Accept Book I** — do not re-prove Tao; cite it as Proposition 4.
2. **Work the tree bottom-up** — only ⏳ leaves get effort.
3. **Connect Tao ↔ W (open research question):**

```text
TAO_TO_W_BRIDGE
│
├── Does Tao's 3-adic mixing force carries to stay nonzero?
│   └── 🔍 Exploring — if yes, W dies and a huge branch closes
│
├── Does Tao's bound exclude divergent orbits?
│   └── ❌ Known no — almost-all ≠ all
│
└── Next falsifiable lemma
    └── Compute carry statistics along W-prefixes to high depth
        Compare to Syracuse mod-3^n predictions
```

4. **Elements discipline:** every new claim is a **Proposition** with **Depends on:** lines — never a leap.

---

## Book VI — Proposed Elements table of contents (living)

| Book | Topic | Status |
|------|-------|--------|
| 0 | Definitions, notions, postulates | ✅ This document |
| I | Proved / cited facts (incl. Tao) | ✅ Ground floor |
| II | Counterexample tree + W wall | ⏳ Active frontier |
| III | How hard problems fall (patterns) | ✅ Methodology |
| IV | Engineering lenses (subtrees) | 🔍 Ongoing |
| V | Tao → W bridge | 🔍 Next research |
| VI | Missing theorem (when found) | ⏳ Not yet |

**Missing theorem (placeholder):**

```text
MISSING_THEOREM
└── ⏳ Open
    A statement T such that:
    closed branches + T ⇒ Collatz true
    OR
    ¬T ⇒ explicit counterexample
    Candidate neighborhood: W carry nonvanishing
```

---

## Glossary (jargon → plain)

| Term | Plain meaning |
|------|----------------|
| Orbit | Sequence you get by repeating the rule |
| Syracuse map | Odd-only accelerated Collatz step |
| Logarithmic density | A way to say "almost all" that weights small numbers more |
| 2-adic / 3-adic | Number systems that track remainders mod `2^n` or `3^n` — carry/borrow logic |
| Carry | Binary addition overflow bit — "does division leave a remainder?" |
| Lyapunov function | Energy-like quantity that always decreases along trajectories |
| Attractor | State the system keeps falling toward (here: `1`) |
| Reduction | Prove theorem B instead; theorem A follows automatically |

---

## Book VII — Multi-lens proof search (broad focus)

Chaos, probability, physics, materials science, transfer operators, Ramanujan-style series, and the **Tao bridge** — see **[`LENSES.md`](LENSES.md)**.

## Book VIII — Pure language standpoint (primary)

Orbits are **words**, integers are **speakers**, ghosts are **syntax without positive meaning** — see **[`LANGUAGE.md`](LANGUAGE.md)**.  
Other lenses are translations of this. Euclid’s Elements **is** a language textbook.

**Priority:** finite grammar cover (certificates) + parser-density (Tao bridge).  
**Deferred:** W carry wall, deep nonperiodic.

---

## How this project uses the Elements method

- [`LENSES.md`](LENSES.md) — Book VII multi-lens map + proof-search prompt
- [`domains/collatz/lenses.yaml`](../domains/collatz/lenses.yaml) — lens registry
- [`domains/collatz/statements.yaml`](../domains/collatz/statements.yaml) — Book I facts
- [`domains/collatz/progress_tree.yaml`](../domains/collatz/progress_tree.yaml) — Book II counterexample tree
- [`tools/collatz.py`](../tools/collatz.py) — computational experiments (evidence, not proof)
- [`CollatzFormal/`](../CollatzFormal/) — future formal propositions (Lean)
- [`moo/orchestrators/critic.py`](../moo/orchestrators/critic.py) — blocks overclaims (scope claims to what is proved)

**Encouragement (same spirit as AGENTS.md):**  
Tao reached `log(log(log(log(n))))` when experts said the problem was untouchable. Your counterexample tree already **closed** whole branches. Close one more leaf, name one wall, prove one lemma — that is how impossible problems fall.