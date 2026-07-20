# Multi-Lens Collatz Research — Engineering & Physics Map

> Plain-language companion to your proof-search program.  
> **Current focus:** broad lenses + homomorphism checks.  
> **Deferred:** W carry wall, deep p-adic, nonperiodic frontier (see end).

Read first: [`ELEMENTS.md`](ELEMENTS.md) for definitions and Euclid-style spine.

---

## What “homomorphic” means here (no jargon)

Two systems are **homomorphic** (structure-preserving) if you can translate objects and rules so that **relationships stay true**.

| Engineering idea | Collatz translation | Homomorphic? |
|------------------|----------------------|--------------|
| State machine | `n` → next `n` | ✅ Yes — exact |
| Energy decay | `log n` decreasing each step | ⚠️ Almost — drift works on average, not every step |
| Rare failure batch | Tao’s “exceptional set” `E_C` | ✅ Yes — bad parts in a tested population |
| Backward flow graph | Inverse Collatz tree | ✅ Yes — exact rules |
| Quantum eigenstate | Sparse bad set → fixed measure | 🔍 Analogy only — must become finite matrix |
| Crystal defect | Local residue class that won’t anneal | 🔍 Metaphor — checkable via mod `2^a` certificates |

**Rule:** If a lens cannot produce **exact inequalities** or **finite verifiable data**, it stays 🔍 until translated.

---

## Strategic target (your Tao bridge)

**Tao black box (already proved):**  
For any cutoff `C`, the set of numbers whose entire orbit stays above `C` is **sparse** (logarithmic density → 0).

```text
TAO_BRIDGE_PROGRAM
│
├── ✅ Tao sparsity
│   └── Bad orbits above C are rare (log density → 0)
│
├── ⏳ Basin amplification (MISSING THEOREM)
│   └── If any bad orbit exists above C, bad set cannot be too sparse
│       i.e. lower log-density of E_C ≥ η > 0 when E_C nonempty
│
├── ✅ Conditional closure (logic only)
│   └── Tao sparsity + basin amplification + finite check below C ⇒ Collatz
│
└── 🔍 Attack via inverse-tree mass flow, transfer operators, certificates
```

*Engineering picture:* Tao says defective parts are **rare**. Amplification says: if **any** defect exists, defects must appear at a **minimum rate** in the population. Rare + minimum rate = **contradiction** ⇒ no defects.

---

## Core equations (odd-only form) — do not skip `C_s`

After `s` odd-only steps:

```text
U^s(n) = (3^s · n + C_s) / 2^K_s

K_s = k_0 + k_1 + ... + k_{s-1}    (total halvings)
C_s = additive offset from the +1 terms — NEVER ignore this
```

**Descent happens when:**

```text
U^s(n) < n   ⟺   (2^K_s - 3^s) · n > C_s
```

*Materials analogy:* `C_s` is **residual stress** from prior steps. You cannot prove relaxation using only the `3^s` multiplier — the offset matters like **Bauschinger effect** in cyclic loading.

---

## Lens catalog (progress trees)

### 1. Probability & chaos theory

```text
PROBABILITY_CHAOS_LENS
│
├── Random-walk heuristic (log n drifts down on average)
│   └── ✅ Explains why most orbits sink
│       Not a proof — assumes uncorrelated steps
│
├── Sensitive dependence / chaos
│   └── 🔍 Exploring
│       Small change in n → very different orbit shape
│       Like turbulence: predictable rule, unpredictable path
│       Does NOT imply divergence — chaos ≠ escape
│
├── Almost-all results (Terras, Korec, Tao chain)
│   └── ✅ Rigorous partial — measure on integers, not coin flips
│
├── Exceptional-set amplification (Tao bridge)
│   └── ⏳ Open — turn “almost none” into “none” via density contradiction
│
└── Homomorphism to Collatz
    └── ✅ Statistical mechanics of orbits — exact map for density statements
        ❌ Cannot use “random” as proof without uniform bounds
```

*Chaos in plain terms:* The rule is simple; trajectories **look** chaotic in plots. That is **evidence of complexity**, not a counterexample. Proof needs **every** trajectory, not typical ones.

---

### 2. Engineering — control, stability, FMEA

```text
ENGINEERING_LENS
│
├── Feedback: odd = excitation, even = damping
│   └── ✅ Heuristic average gain < 1
│
├── Worst-case stability (every initial state)
│   └── ⏳ Open — this IS Collatz
│
├── FMEA / counterexample tree
│   └── ✅ Framework — cycle vs diverge classification
│
├── Finite verification below C
│   └── ✅ Computational fatigue test — evidence below bound
│
├── Certificate library (Babel engine)
│   └── 🔍 Exploring — finite data + verifier = proof chunk
│
└── Homomorphism
    └── ✅ State machine, FMEA, certificates map exactly
        ❌ Laplace-domain shortcuts do not
```

---

### 3. Physics — least energy / Lyapunov

```text
LYAPUNOV_LENS
│
├── Naive energy E₀(n) = log n
│   └── ❌ Dead for uniform proof
│       Odd step can increase log n
│
├── Corrected energy E(n) = log n + φ(n mod 2^a)
│   └── 🔍 Exploring
│       Search bounded correction φ for finite modulus
│
├── Finite-residue certificate
│   └── 🔍 If exists: verifier checks inequalities mod M only
│
└── Homomorphism
    └── ⚠️ Energy methods map to descent inequalities
        Requires exact C_s control — approximate drift fails
```

*Thermodynamics analogy:* Collatz wants a **Lyapunov free energy** that drops every cycle. No simple global potential is known — like a system with **hidden internal variables** (`C_s`).

---

### 4. Physics — Dirac / Schrödinger / transfer operator

```text
TRANSFER_OPERATOR_LENS
│
├── Two-component system: even state | odd state
│   └── ✅ Exact — parity is the quantum number
│
├── Odd-only compression U = D^k ∘ O
│   └── ✅ Exact — k = v₂(3n+1)
│
├── Backward transfer operator L on predecessors
│   └── 🔍 Exploring
│       (Lf)(m) = Σ f(predecessor of m) over valid inverse branches
│
├── Weighted graph on residues mod M = 2^a · 3^b
│   └── 🔍 Finite certificate target
│
├── “Bad eigenmeasure” with eigenvalue ≥ 1
│   └── 🔍 Move 37 — sparse bad set ⇒ invariant mass distribution
│       Must be finite-dimensional matrix, not metaphor
│
└── Homomorphism
    └── ✅ Markov/transfer operators on discrete states — exact
        ❌ Continuous Hilbert space without finite reduction
```

*Engineering translation:* Build a **sparse transition matrix** `T` on residue classes. A persistent bad orbit ⇒ **stationary distribution** concentrated on bad states. Prove no such distribution exists under constraints.

---

### 5. Inverse-tree harmonic mass flow

```text
INVERSE_TREE_MASS_LENS
│
├── Forward: n → T(n)
│   └── ✅ Unique next state
│
├── Backward: m ← 2m always; m ← (m-1)/3 when valid
│   └── ✅ Exact inverse rules
│
├── E_C closure: if m is bad above C, all predecessors staying >C are bad
│   └── ✅ Proved — backward basin ⊆ E_C
│
├── One-generation harmonic mass S₁(m)
│   └── ✅ For m ≢ 0 (mod 3): S₁(m) > 1/m or > 2/m by residue class
│
├── Multi-generation mass amplification
│   └── ⏳ Main attack for basin amplification
│       Need scale control: child ≈ 2^k m/3 jump size
│
├── Sterile states (m ≡ 0 mod 3)
│   └── ✅ Odd-only inverse stops — branch ends
│
├── Collisions in inverse tree
│   └── 🔍 Must bound overcounting if paths merge
│
└── Homomorphism
    └── ✅ Electrical network / flow conservation on inverse graph
        Mass = 1/n weights — exact discrete potential theory
```

*Materials science analogy:* **Reverse diffusion** — if a “defect” site `m` persists, flux of predecessors into it must sustain the defect concentration. Amplification = **minimum inbound flux** forces **detectable bulk concentration** (positive density).

---

### 6. Ramanujan-style global identities

```text
RAMANUJAN_LENS
│
├── B = set of n that reach 1
│   └── Collatz: B = all positive integers
│
├── Generating function G(x) = Σ_{n∈B} x^n
│   └── 🔍 If B = ℕ, G(x) = x/(1-x) — tautology, not progress
│
├── Dirichlet series D_B(s) = Σ_{n∈B} n^{-s}
│   └── 🔍 Inverse branches give functional relations
│       Doubling: Σ (2m)^{-s} = 2^{-s} D_B(s)
│       Odd inverse: residue-filtered sums
│
├── Bad-set series D_E(s) for E_C
│   └── 🔍 Positive log-density ↔ pole behavior at s=1
│
└── Homomorphism
    └── ⚠️ Analytic number theory — exact if identities close
        ❌ Many formal solutions without positive-integer constraint
```

*Honest status:* Beautiful global bookkeeping. Obstruction = **exotic solutions** that look valid in series but fail **positivity / integrality**.

---

### 7. Binary residue descent certificates

```text
RESIDUE_CERTIFICATE_LENS
│
├── Valuation word w = (k₀,…,k_{s-1}) fixes affine map on one residue class mod 2^{K+1}
│   └── ✅ Word-to-residue lemma (reproducible)
│
├── Descent when (2^K - 3^s)n > C_w on that class
│   └── ✅ Finite check per class
│
├── Known families: even n; odd ≡ 1 (mod 4); odd ≡ 3 (mod 16)
│   └── ✅ Nontrivial safe families exist
│
├── Cover all odd residues mod 2^a with finite certificate list
│   └── 🔍 Babel engine target — finite cover ⇒ huge partial theorem
│
└── Homomorphism
    └── ✅ FEM mesh / tolerance stack — exact on finite moduli
        Each residue = cell; certificate = proof cell shrinks
```

*Materials QC analogy:* Each residue class is a **microstructure class**. Certificate = **this grain orientation always work-hardens (descends)** under the loading sequence `w`.

---

### 8. Material science — microstructure & annealing

```text
MATERIALS_SCIENCE_LENS
│
├── Microstructure = n mod 2^a (binary texture) + mod 3^b (ternary texture)
│   └── 🔍 Exploring — coupled textures under U
│
├── Annealing = repeated halving (even steps)
│   └── ✅ Smooths binary texture — divides by 2
│
├── Work hardening = odd 3n+1 steps
│   └── ✅ Can increase “stored energy” (magnitude)
│
├── Defect site = m in E_C (never anneals below C)
│   └── ⏳ Prove defect density impossible via flux argument
│
├── Grain boundary (sterile mod 3)
│   └── ✅ Inverse branching terminates — no odd parent
│
├── Phase transformation analog
│   └── 🔍 Dangerous residue classes = metastable phases
│       Certificates = prove metastable cannot persist infinitely
│
└── Homomorphism
    └── ⚠️ Metaphor guides search; proofs need residue certificates
        Best map: inverse mass flow = defect flux balance
```

---

## Certificate library (Babel engine) — engineer’s proof BOM

Each certificate = **finite data + verifier**. Like a **mill test report** — anyone can re-check.

| ID | Certificate type | Proves (if verified) |
|----|------------------|----------------------|
| C1 | Residue descent `(a, r, s, K, C_w)` | All `n ≡ r (mod 2^a)` descend in `s` odd steps |
| C2 | Finite odd cover mod `2^a` | All odd residues covered ⇒ global odd descent |
| C3 | Lyapunov mod `M` with rational `φ_r` | Energy drops in bounded steps per residue |
| C4 | Harmonic mass-flow mod `2^a 3^b` | Backward flux forces density lower bound on `E_C` |
| C5 | 2-adic ghost (periodic word) | Infinite pattern has no positive integer realization |
| C6 | Cycle sieve on exponent word | `2^K - 3^s ∤ C_w` for word family |

**Verifier rule:** No certificate promoted without runnable check (Python, Lean, or hand inequality).

---

## Move 37 — Collatz Hamiltonian (make it mathematical)

```text
MOVE_37_HAMILTONIAN
│
├── States: residue classes r mod M = 2^a · 3^b
│
├── Weights: q_r > 0 (harmonic mass per state)
│
├── Operator: (Lq)_r = Σ_{predecessors} w_{r→r'} · q_{r'}
│
├── Claim: persistent bad set ⇒ eigenvector q with eigenvalue λ ≥ 1
│   └── 🔍 To prove or refute under finite M
│
├── Obstruction if fails:
│   └── Sterile mod 3 + scale drift breaks uniform λ bound
│
└── Homomorphism
    └── ✅ Finite Markov chain — exact linear algebra
        ❌ Infinite-dimensional without finite truncation proof
```

---

## Proof-search session prompt (reuse template)

Save this for focused sessions (no web, honest audit):

```text
Role: Proof-search engine, not explainer.
Goal: Attack the Tao bridge (basin amplification) using lenses in docs/LENSES.md.
Deferred: W carry, deep nonperiodic (unless homomorphism forces revisit).

Required outputs:
1. Restate conditional: Tao sparsity + amplification + finite C ⇒ Collatz.
2. Pick ONE primary lens this session.
3. Produce progress tree with ✅/⏳/🔍/❌ leaves.
4. Attempt sharpest partial theorem OR name exact obstruction.
5. Self-audit: randomness? ignored C_s? assumed Collatz? ghosts vs integers?
6. Final class: A/B/C/D/E (see LENSES.md audit).

Core descent: U^s(n) = (3^s n + C_s)/2^K_s; descent iff (2^K_s - 3^s)n > C_s.
```

---

## Self-audit checklist (every session)

- [ ] Used randomness only as heuristic, not proof?
- [ ] Kept additive `C_s` / `+1` terms?
- [ ] Uniform claim vs tested examples only?
- [ ] Assumed Collatz anywhere?
- [ ] Separated positive integers from 2-adic ghosts?
- [ ] Bounded inverse-tree overcounting?
- [ ] Handled sterile `m ≡ 0 (mod 3)`?
- [ ] Controlled scale drift in mass sums?
- [ ] Stated cutoff `C` explicitly?
- [ ] Density statement vs infinite branching only?
- [ ] Physics analogy translated to matrix/inequality?

**Final classification:** A complete proof | B eventual descent | C disproof | **D partial + obstruction** | E failed with sharp reason

---

## Deferred branches (not current focus)

```text
DEFERRED
│
├── W carry wall
├── Deep nonperiodic dangerous paths
└── Full 2-adic ghost separation for aperiodic paths
```

Revisit when a broad lens **homomorphs** onto these — e.g. residue certificates covering dangerous classes.

---

## Suggested session order (mechanical engineer path)

1. **Inverse-tree mass flow** — closest to Tao bridge  
2. **Residue certificates** — finite, checkable, like tolerance analysis  
3. **Transfer operator / Move 37** — linear algebra on finite graph  
4. **Lyapunov search** — automated scan of small `φ` mod `2^a`  
5. **Probability** — only to interpret Tao, not to prove  
6. **Ramanujan / complex** — only if certificate approach stalls  

---

## Links in this repo

| Artifact | Role |
|----------|------|
| [`ELEMENTS.md`](ELEMENTS.md) | Euclid spine, Book I facts |
| [`progress_tree.yaml`](../domains/collatz/progress_tree.yaml) | Counterexample tree + lens registry |
| [`tools/collatz.py`](../tools/collatz.py) | Orbit / sweep computation |
| [`CollatzFormal/`](../CollatzFormal/) | Future formal certificates |