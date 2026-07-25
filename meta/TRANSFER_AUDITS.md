# Transfer audits

Assessments of outside methods proposed for the Collatz program. Mostly
negative, and kept for that reason: a recorded "does not transfer" stops the
next agent from spending a session rediscovering it.

**Standing rule: analogy is not transfer.** A method transfers when it
produces a theorem about a deterministic arithmetic system that retains
positive-integer realizability. Structural resemblance is a prompt for a
probe, never a result.

---

## Tan Bui-Thanh (Oden Institute, UT Austin) — 2026-07-25

**Verdict: nothing transfers.**

His work is computational applied mathematics for PDE-governed systems:
infinite-dimensional Bayesian inverse problems (Gaussian/Besov priors on
function space, Laplace approximation at the MAP point, low-rank
prior-preconditioned Hessians, adjoint gradients), model reduction, and
model-constrained scientific deep learning.

| Method | Verdict | Reason |
|---|---|---|
| Infinite-dim Bayesian inverse problems | does not transfer | needs a prior ensemble as *input*; Collatz needs an ensemble as *output*, and an imposed prior carries no arithmetic content |
| rMAP sampling | does not transfer | its theorems are about sampler accuracy under a posited measure, not realizability in ℤ |
| Hessian low-rank / model reduction | does not transfer | works because the Hessian spectrum decays — a *low effective complexity* requirement, the exact assumption that must be dropped here |
| Model-constrained DL (TAEN) | does not transfer | rigorous only for linear Hilbert-space operators; the Collatz map is discrete, non-smooth, non-Hilbert |
| Chaotic-dynamics Jacobian matching (Kang–Nguyen–Bui-Thanh, arXiv:2606.01596) | speculative probe, weak | structurally nearest — single trajectories constraining an invariant measure — but purely empirical, so it is analogy; strictly dominated by Deng's kinetic limits, which are theorems |
| Adjoint framework | does not transfer | adjoints need a linear operator between inner-product spaces; parity words carry no such structure |

**The general reason, and it generalises past this one researcher.** The
entire toolkit presumes a *differentiable forward map with low-rank
informative structure*. The Collatz obstruction is 2-adic positivity:
non-smooth, non-continuum, and **high-complexity by necessity** — the
surviving counterexample candidates are exactly the ones with high factor
complexity. Any method whose power comes from low effective dimension is
pointed the wrong way.

That is the same wall the factor-complexity inequality hit from the symbolic
side. Two independent methods, both requiring simplicity, both saturating.
**The missing instrument consumes complexity rather than requiring it**, and
no amount of searching in low-dimensional-structure literature will supply it.

**Keep instead:** Yu Deng's kinetic limits remain the best external analogue
for the amplification branch, because they are theorems that derive
ensemble-level behaviour from microscopic dynamics. The blocker there is
stated and real — kinetic limits need a proved decorrelation mechanism, and
the 2–3 resonance lattice supplies persistent correlations.

---

## Gödel, Escher, Bach — 2026-07-25

**Verdict: two chapters transfer, the famous part does not.**

Hofstadter discusses Collatz *by name* — as "wondrous numbers" — in the
Dialogue "Aria with Diverse Variations" and Chapter XIII, "BlooP and FlooP and
GlooP". That pair is not a metaphor for this program; it is about it.

**Read (real content):**

- **Chapter XIII + the preceding Aria — the totality point.** BlooP has only
  bounded loops (every program terminates by construction); FlooP has the
  unbounded `MU-LOOP` (termination is a claim). Collatz is writable in FlooP
  trivially and in BlooP not at all, because the halting bound is exactly what
  is unknown. The sharp consequence: **Goldbach is Π₁** — each instance is
  settled by a bounded search — so independence from PA would imply truth.
  **Collatz is Π₂** (`∀n ∃k, T^k(n) = 1`) and that argument does not run. A
  Collatz independence result would not settle it. Anyone in this project
  flirting with "maybe it's undecidable" should read this chapter first to see
  what that would and would not buy.
- **Chapter III, "Figure and Ground" — the complement point.** The real
  theorem: there are recursively enumerable sets whose complement is not r.e.
  The set of `n` reaching 1 is r.e. — just run the map. The counterexample set
  is its complement. Cycle counterexamples have finite certificates;
  **divergent ones do not.** So "characterise the survivors" and
  "characterise the counterexamples" are *not symmetric*, and any method
  assuming they are has a hole. This is the chapter that disciplines the
  phrase "prove no counterexample exists" — and it is the formal reason
  `COUNTEREXAMPLE_SHAPE.md` has to treat its two branches separately.
- **Chapter I, "The MU-puzzle"** — only as method: solved by finding a
  conserved quantity mod 3, and the invariant lives *outside* the rewriting
  system. That is the invariant-hunting move, stated as mechanism.

**Skip for this purpose:** Chapter XX (Strange Loops / Tangled Hierarchies)
and the Introduction. Self-reference-as-aesthetic gives nothing operational on
a number-theoretic dynamical system — Collatz has no self-referential
encoding, and Gödel's diagonal does not port to it. Also skip XV ("Jumping out
of the System"), rhetorically appealing and technically thin here; the
MU-puzzle already delivers the usable half.

**If one chapter: XIII. If three: XIII, III, I.**

This audit was commissioned partly to test the "strange loop" framing that
appears in several external notes about this project. The finding is that the
strange-loop material is the *decorative* part of GEB, and the genuinely
useful part — Π₁ versus Π₂, and r.e. sets versus their complements — is
ordinary computability theory that happens to be well explained there.

---

## Bayesian methods — 2026-07-25

See [`BAYESIAN.md`](BAYESIAN.md). Summary: legitimate for **resource
allocation and search ordering**, never for acceptance. One live defect found
and fixed.
