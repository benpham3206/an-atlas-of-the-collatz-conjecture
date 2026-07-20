# Transcript lift cocycle — first realizability probe

**Date:** 2026-07-19  
**Status:** exact finite theorem + independently checked finite oracle; no Collatz
proof, no automatic-sequence decision theorem, no novelty claim.

## One-read resume

The best current lead remains positive-integer **realizability** of structured
parity transcripts. Finite parity windows never obstruct anything: every word
is one Terras residue cylinder, and every nested transcript defines one 2-adic
state. The first nontrivial global datum is how those cylinders lift from depth
`L` to `L+1`.

For a transcript `q`, let `r_L` be the unique representative in `[0,2^L)`
realizing `q[0:L]`. Define

\[
r_{L+1}=r_L+\varepsilon_L2^L,
\qquad \varepsilon_L\in\{0,1\}.
\]

The sequence `epsilon` is exactly the ordinary binary expansion of the 2-adic
state `Phi(q)`. Therefore

\[
q\text{ is realized by }n\in\mathbb Z_{>0}
\iff
\varepsilon_L=0\text{ eventually and }r_L\text{ stabilizes above }0.
\]

The next theorem target is the obstruction

> If `q` is 2-automatic and `Phi(q)` is an ordinary integer, must `q` be
> eventually periodic?

This is a question, not a result. Kill it if the bridge from automaton-kernel
decimation to orbit shift requires Collatz-strength unbounded orbit control.

## Exact lift recurrence

For a finite word `w` of length `L`, write

\[
T_w^L(n)=\frac{3^{a_L}n+c_L}{2^L}.
\]

Let `r_L` be its canonical Terras residue and put

\[
z_L=\frac{3^{a_L}r_L+c_L}{2^L}\in\mathbb Z.
\]

If the next transcript bit is `b=q_L`, then divisibility at depth `L+1`
forces

\[
\boxed{\varepsilon_L\equiv z_L+b\pmod2},
\qquad
r_{L+1}=r_L+\varepsilon_L2^L.
\]

The quotient update is exact:

\[
z_{L+1}=\begin{cases}
(z_L+\varepsilon_L3^{a_L})/2,&b=0,\\
(3z_L+1+\varepsilon_L3^{a_L+1})/2,&b=1.
\end{cases}
\]

### Proof

For `b=0`, the new numerator is

\[
3^{a_L}(r_L+\varepsilon_L2^L)+c_L
=2^L(z_L+\varepsilon_L3^{a_L}).
\]

Because `3^a` is odd, divisibility by `2^(L+1)` requires
`epsilon_L = z_L mod 2`.

For `b=1`, the affine update gives `a_(L+1)=a_L+1` and
`c_(L+1)=3c_L+2^L`. The new numerator is

\[
2^L(3z_L+1+\varepsilon_L3^{a_L+1}).
\]

Its bracket is even exactly when `epsilon_L = z_L+1 mod 2`. Both cases are
`epsilon_L = z_L+b mod 2`, and division gives the stated quotient update. ∎

### Positive-integer criterion

Coherence says `r_(L+1) mod 2^L = r_L`, so the `epsilon_L` are the binary
digits of the inverse-limit state `Phi(q)`. A nonnegative ordinary integer has
finitely many nonzero binary digits, while a negative ordinary integer has
2-adic digits eventually equal to one. Thus eventual-zero lift bits plus a
positive stabilized residue are equivalent to membership in `Z_(>0)`.

This restates the existing `Phi(q) in Z_(>0)` wall in a form that is local,
incremental, and machine-checkable. It does not make the decision problem easy.

## Oracle

Files:

- `verify/transcript_lift_oracle.py` — quotient recurrence plus independent
  modular-series path;
- `verify/test_transcript_lift_oracle.py` — exhaustive direct Terras oracle for
  all words through length 10 and positive integers `1..1000`;
- `verify/lift_results.json` — exact structured-prefix readout.

The two production paths share only input bits:

1. quotient/lift recurrence above;
2. direct evaluation of
   `-sum 2^d_j / 3^(j+1) mod 2^L`.

A mismatch is a finding. Nonstabilization through a finite bound is evidence,
never a proof of non-integrality.

### Structured probes at `L=4096`

| Transcript | Status | Lift ones | Last lift one | Longest zero run |
| --- | --- | ---: | ---: | ---: |
| `(10)^omega` | exact positive integer `1` | 1 | 0 | 4095 |
| `(01)^omega` | exact positive integer `2` | 1 | 1 | 4094 |
| `1^omega` | exact negative integer `-1` | 4096 | 4095 | 0 |
| `10^omega` | exact noninteger `-1/3` | 2048 | 4094 | 1 |
| Thue-Morse | finite probe only | 2034 | 4093 | 10 |
| period-doubling | finite probe only | 2041 | 4095 | 13 |

The generated JSON is authoritative for every row. The table records the two
aperiodic 2-automatic probes only as nonstabilized through the bound.

## Reasoning ledger for future models

| Mode | Role here | Promotion rule |
| --- | --- | --- |
| Abduction | propose realizability as a gluing/transport problem | retain only if it names a new testable object |
| Induction | inspect lift patterns in automatic transcripts | finite patterns remain evidence with explicit cap |
| Deduction | prove the lift recurrence and positive-integer criterion | only this layer enters the theorem ledger |

Abduction chooses the search direction. Induction maps examples and failures.
Deduction is the only truth gate.

## What the supplied sources changed

### Cycle Double Cover prompt and proof

The [prompt](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf)
contributes portfolio independence, approach-family tracking, and adversarial
acceptance. The [proof](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf)
has a genuine local-to-global mechanism: local set assignments disagree across
edges by defects `d_e`; global compatibility becomes a linear image-membership
problem; dual annihilators cancel by counting each edge twice.

That mechanism does **not** transplant directly. Collatz finite windows already
glue exactly, so there is no remaining finite overlap defect for linear algebra
to kill. The legitimate transfer is methodological: express the residual global
condition as exact membership and search for an annihilator or rigidity theorem.

### IMO 2026 repository

The linked [README](https://github.com/AxiomMath/IMO2026/blob/main/README.md)
attributes the six Lean solutions to **AxiomProver**, an autonomous multi-agent
Lean system; the inspected source does not attribute them to ChatGPT. The useful
transfer is artifact discipline: exact theorem statements, compositional proof
files, pinned Lean version, and independent verification. The smallest honest
Lean target here is the lift recurrence—not the Collatz conjecture.

### Collatz Master Compilation

Retained:

1. local-to-global compatibility as the mechanism to test;
2. compositional certificates rather than one giant insight;
3. an explicit failure database and adversarial audit;
4. deduction/induction/abduction kept as separate evidence layers.

Rejected as proof steps: phenomenology, metaphysics, unsupported independence
claims, general-Collatz undecidability transferred to fixed `3n+1`, and a demand
for an “alien” formal language. Those are heuristics or category errors until
they produce exact lemmas.

## Metadynamical Geometry audit

The first adversarial audit found that the initial field sketch largely renames
parameterized dynamics, fibered total spaces, structural stability, and ordinary
momentum. The document therefore fails its own novelty gate **at present**.

The lift cocycle is a useful stress test, not evidence of a new field. It fits
better as transport across a tower of finite-resolution constraint sheets. The
potentially useful general object is narrower:

> a machine-checkable certificate together with the exact radius or domain over
> which it transports without losing validity.

Call this **certificate persistence**, not hyper-inertia, until it produces a
coordinate-independent theorem in at least two unrelated systems.

## Grok 4.5/high registry

Eight independent read-only packets were launched. Four returned substantive
work: gluing formulation, finite oracle design, adversarial novelty audit, and
structured-family ranking. Four returned only setup/status text and supplied no
accepted mathematical content.

```text
run-mrriwrth-acils2  substantive — gluing/section formulation
run-mrriwrtu-eugnts  substantive — dual-path oracle design
run-mrriwru9-aaggrg  substantive — novelty rejection/salvage
run-mrriwrvd-tm20de  substantive — 2-automatic family ranking
run-mrriwrur-x50yro  incomplete  — CDC transfer
run-mrriwrto-8sbnbb  incomplete  — IMO/Lean target
run-mrriwruc-f6nixr  incomplete  — compilation audit
run-mrriwrv1-gf664u  incomplete  — independent prefix derivation
```

Incomplete worker output is a failure, not evidence. CDC, IMO, compilation, and
prefix conclusions in this note were independently derived by Codex from the
supplied sources and checked against the local oracle.

## Next exact packet

**Conjecture A (automatic-transcript obstruction).** If `q` is 2-automatic and
`Phi(q)` is an ordinary integer, then `q` is eventually periodic.

Before attempting a proof:

1. state a DFAO and its finite 2-kernel exactly;
2. formalize how orbit shift `sigma` acts on that kernel;
3. find a bridge from kernel decimation (`n -> 2n, 2n+1`) to orbit shift;
4. kill the route if that bridge assumes unbounded orbit control equivalent to
   Collatz;
5. search the literature specifically for automatic parity transcripts and the
   Bernstein-Lagarias conjugacy before claiming novelty.

The finite oracle remains useful even if Conjecture A dies: it produces exact,
independently checked lift certificates and preserves mismatches.
