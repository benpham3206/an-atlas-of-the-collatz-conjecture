# An Atlas of the Collatz Conjecture

Literature references and reproducible exact-arithmetic analysis of
first-return systems for the Terras-accelerated Collatz map. The Collatz
conjecture remains open.

## Status

| Statement | Evidence |
|---|---|
| No folds at distinct depths k, k′ ≤ 10 are affinely conjugate | proof, exact-arithmetic screen, and independent reimplementation |
| A parity transcript q is realized by a positive integer iff Φ(q) ∈ ℤ_{>0} | derivation in `contribution/proofs/PARTIAL_THEOREMS.md` |
| No nontrivial positive cycle with ≤ 20 odd members | exact search + independent oracle: `contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` and `contribution/packets/2026-07-23-cycle-exclusion-extension/` |
| Rational Φ with odd denominator forces complexity pressure; Sturmian excluded | pointwise memo in `contribution/packets/2026-07-22-landmark-pointwise/` |
| 99 of the 109 enumerated supercritical survivors have Φ(q) ∉ ℤ_{>0} | proved here, but **subsumed** by López–Stoll 2021 — see [`PRIORITY.md`](PRIORITY.md) |
| A minimal counterexample has 2^(A_h) ≤ 3^h for every h ≤ 10⁶ Syracuse steps | proved, but a **quantitative refresh** of Terras 1976 / Garner 1981 — see [`PRIORITY.md`](PRIORITY.md) |
| Terras bijection, two-branch-family non-universality, parity-block collision principle | zero-sorry Lean 4 certificates: `formal/` |
| Collatz conjecture | neither proved nor disproved; no reduction from these results is established |

**Start here for agent handoff:** [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md)  
**Repo frontier (established / blocked / next):** [`STATE.md`](STATE.md)  
**Ranked attack targets (odds, fallbacks, kill criteria):** [`TARGETS.md`](TARGETS.md)  
**Fresh-agent hail-mary brief:** [`HAIL_MARY_PROMPT.md`](HAIL_MARY_PROMPT.md)  
**What a counterexample must / cannot look like:** [`COUNTEREXAMPLE_SHAPE.md`](COUNTEREXAMPLE_SHAPE.md)  
**Agent conduct — read before working:** [`meta/AGENT_CONDUCT.md`](meta/AGENT_CONDUCT.md) — start with §"Hidden insights: the failure classes verification cannot catch"  
**Literature priority, and what it retired:** [`PRIORITY.md`](PRIORITY.md)  
**Who did what, and which check backs it:** [`PROVENANCE.md`](PROVENANCE.md) · [`CONTRIBUTORS.md`](CONTRIBUTORS.md)  
**Complete 2026-07-22 research packet:** [`contribution/packets/2026-07-22-landmark-pointwise/`](contribution/packets/2026-07-22-landmark-pointwise/)

## Maps and notation

Collatz map, standard form:

```
C(n) = n/2      if n even
C(n) = 3n + 1   if n odd
```

Terras-accelerated form, used throughout this repository:

```
T(n) = n/2        if n even
T(n) = (3n+1)/2   if n odd
```

Conjecture: for every integer n ≥ 1, some iterate reaches 1. Verified for
n < 2^71 (Bařina 2025, [DOI](https://doi.org/10.1007/s11227-025-07337-0)).

## Repository layout

| Path | Contents |
|---|---|
| [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md) | One-page attack brief (proved toolkit + open targets) |
| [`STATE.md`](STATE.md) | Repository frontier: established results, blocked routes, next packets |
| [`contribution/README.md`](contribution/README.md) | Index of definitions, proofs, programs, and verification reports |
| [`contribution/note/NOTE.md`](contribution/note/NOTE.md) | Fold theorem, proof outline, and limitations |
| [`contribution/proofs/`](contribution/proofs/) | Detailed proofs and formal statements |
| [`contribution/code/`](contribution/code/) | Exact-arithmetic implementations and executable checks |
| [`contribution/packets/2026-07-22-landmark-pointwise/`](contribution/packets/2026-07-22-landmark-pointwise/) | Landmark strategy, strategy machine, resonance lattice, prefix-return barrier, rational finite verifier |
| [`contribution/packets/2026-07-22-automatic-transcript-rigidity/`](contribution/packets/2026-07-22-automatic-transcript-rigidity/) | Automatic-transcript trichotomy, density-wall impossibility witnesses, 514-word exact hunt |
| [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/) | Exact factor-language complexity bound (Lemma D). Its **conclusion is subsumed** by López–Stoll 2021; the machinery is retained because it is the only tool that bites at the critical density |
| [`contribution/packets/2026-07-24-contraction-onset/`](contribution/packets/2026-07-24-contraction-onset/) | Descent requires contraction; onset bound M(h). A **quantitative refresh** of Terras 1976 / Garner 1981, not a new theorem |
| [`contribution/packets/2026-07-25-mahler-tower/`](contribution/packets/2026-07-25-mahler-tower/) | Φ(q) as the value of an explicit Mahler-type system for uniform-morphic q. The mixed bases 2 and 3 obstruct the **evaluation point**, not the equation; splits the ten remaining survivors 4/6 and closes none |
| [`contribution/packets/2026-07-22-plateau-escape-weight/`](contribution/packets/2026-07-22-plateau-escape-weight/) | Decay reduced to layer loss L(n), phase-blind impossibility, dichotomy edge n* = 1776 |
| [`contribution/packets/2026-07-22-deep-fourier-scan/`](contribution/packets/2026-07-22-deep-fourier-scan/) | Resonance-chain measurements to n = 17, window-law boundary at n = 16 |
| [`contribution/packets/2026-07-23-plateau-drift-test/`](contribution/packets/2026-07-23-plateau-drift-test/) | C-kernel scan to n = 20, n ≈ 22 crossing prediction falsified on trend |
| [`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/) | Exact cycle exclusion extended to ≤ 20 odd members (6.20 × 10⁸ words per phase; 1.24 × 10⁹ word-scans across both phases) |
| [`contribution/packets/2026-07-24-streaming-depth-21/`](contribution/packets/2026-07-24-streaming-depth-21/) | Streaming layer engine (breaks the n = 20 memory ceiling at 4× lower footprint, bit-identity gated) + direct P6 branch discrimination on the M_n decay law |
| [`contribution/packets/2026-07-22-tao-structural-refinement/`](contribution/packets/2026-07-22-tao-structural-refinement/) | Structural refinement of Tao's exceptional set — description, **not** size; explicitly not a stronger density statement |
| [`contribution/packets/2026-07-22-syracuse-fourier/`](contribution/packets/2026-07-22-syracuse-fourier/) | Exact Syracuse Fourier recursion, exponential L² mixing, computed spectral barrier to "all" |
| [`contribution/packets/2026-07-22-scalar-phase-second-moment/`](contribution/packets/2026-07-22-scalar-phase-second-moment/) | Three exact reductions; uniform Fourier decay reduced to one 1-parameter profile on the 2–3 resonance chain |
| [`contribution/packets/2026-07-22-structure-randomness-transfer/`](contribution/packets/2026-07-22-structure-randomness-transfer/) | Structure–randomness crosswalk; one proved theorem plus an isolated open test object |
| [`contribution/packets/2026-07-22-pointwise-drift-wall/`](contribution/packets/2026-07-22-pointwise-drift-wall/) | Pointwise exclusion at critical drift α = log₃2, no structural hypothesis; two-wall transcript screen |
| [`formal/`](formal/) | Zero-sorry Lean 4 certificates (Terras bijection; two-branch family; parity-block collision principle) |
| [`contribution/reports/`](contribution/reports/) | Recorded outputs and independent verification |
| [`exploratory/README.md`](exploratory/README.md) | Index of drafts that are not cited as results |
| [`exploratory/shadow-barrier/`](exploratory/shadow-barrier/) | Two-metric rational-shadow barrier — **KILLED 2026-07-25**: its Theorem 2 restates its own hypothesis, so it excludes nothing. Retained as a correct note on the affine identity |
| [`meta/`](meta/README.md) | Strategy research, not proofwork: session ledger, simple questions, agent conduct, transfer audits. **Never cited as evidence for a mathematical claim** |
| [`quarantine/README.md`](quarantine/README.md) | Untrusted / disproven / high-risk material — **not evidence** |
| [`graphify-out/`](graphify-out/) | Shareable agent map (report + interactive graph); rebuild after corpus changes. **Read [`graphify-out/README.md`](graphify-out/README.md) first** — the map does not separate `contribution/` from `exploratory/` and `quarantine/`, so its connectivity ranking puts non-evidence drafts near the top |

External papers are linked below and are not included in the repository.

## Literature references

### Surveys and bibliography

| Work | Author, year | Link |
|---|---|---|
| The 3x+1 Problem: An Overview | Lagarias, 2021 | [arXiv:2111.02635](https://arxiv.org/abs/2111.02635) |
| Annotated Bibliography (1963–1999) | Lagarias | [arXiv:math/0309224](https://arxiv.org/abs/math/0309224) |
| Annotated Bibliography, II (2000–2009) | Lagarias | [arXiv:math/0608208](https://arxiv.org/abs/math/0608208) |
| 3x+1 resource page | Lagarias | [umich.edu/~lagarias](https://websites.umich.edu/~lagarias//3x+1.html) |

### Foundational structure

| Result | Source | Link |
|---|---|---|
| Parity words ↔ residues mod 2^k (bijection); stopping times | Terras, 1976 | [Acta Arith. 30](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers) |
| Almost all n have finite stopping time | Everett, 1977 | [DOI](https://doi.org/10.1016/0001-8708(77)90087-1) |
| Coefficient stopping time κ(n) ≤ σ(n); κ = σ for κ ≤ 2593 | Terras, 1976 | Acta Arith. 30 |
| κ = σ for κ < 105,000 via convergents of log₂3 | Garner, 1981 | [DOI](https://doi.org/10.1090/S0002-9939-1981-0603593-2) |
| **Aperiodic q with liminf s_L/L > log₃2 ⟹ Φ(q) irrational**; a non-cyclic rational trajectory forces liminf = log₃2 exactly | López–Stoll, 2021 | [arXiv:2101.12747](https://arxiv.org/abs/2101.12747) |
| liminf h/ℓ ≥ log₃2 for divergent rationals | Monks–Yazinski | [PDF](https://monks.scranton.edu/files/pubs/AutoConjV13.pdf) |
| 2-adic continued-fraction expansion of Φ over a Sturmian word | López–Stoll, 2009 | [INTEGERS 9, A13](https://math.colgate.edu/~integers/j13/j13.pdf) |
| 2-adic extension conjugate to the shift map | Bernstein–Lagarias, 1996 | [Canad. J. Math. 48](https://doi.org/10.4153/CJM-1996-060-x) |

### Statistical results

| Result | Source | Link |
|---|---|---|
| Almost all orbits attain almost bounded values | Tao, 2019/2022 | [arXiv:1909.03562](https://arxiv.org/abs/1909.03562) · [notes](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/) |
| Density lower bound #{n ≤ x reaching 1} ≥ x^0.84 | Krasikov–Lagarias, 2003 | [arXiv:math/0205306](https://arxiv.org/abs/math/0205306) |

Statistical methods control almost all orbits and do not reach a measure-zero
exceptional set.

### Structure and randomness (methodology)

| Work | Author, year | Link |
|---|---|---|
| Structure and randomness in combinatorics | Tao, 2007 | [arXiv:0707.4269](https://arxiv.org/abs/0707.4269) |
| Structure and randomness in the prime numbers | Tao, 2009 | [PDF](https://terrytao.wordpress.com/wp-content/uploads/2009/09/primes_paper.pdf) |

These two expository papers frame the structure/randomness dichotomy used by
the 2026-07-22 packets: model an orbit statistic as a structured component
plus a pseudorandom residual, then bound each part separately. They are method
references, not results about the 3n+1 map.

### Cycles

| Result | Source | Link |
|---|---|---|
| No nontrivial cycle with ≤ 91 local minima | Hercher, 2023 | [arXiv:2201.00406](https://arxiv.org/abs/2201.00406) |
| Cycle bounds via linear forms in logarithms | Simons–de Weger, 2005 | [Acta Arith. 117](https://doi.org/10.4064/aa117-1-3) |
| Nontrivial cycle length bound | Eliahou, 1993 | [Discrete Math. 118](https://doi.org/10.1016/0012-365X(93)90048-X) |

A nontrivial cycle forces 2^b ≈ 3^a, bounded by transcendence results. A cycle
is a finite certificate; divergence is not.

### Algebraic and analytic reformulations

| Result | Source | Link |
|---|---|---|
| 3x+1 semigroup contains every positive integer | Applegate–Lagarias, 2006 | [arXiv:math/0411140](https://arxiv.org/abs/math/0411140) |
| Two-operator calculus for arithmetic-progression paths | Angermund, 2025 | [arXiv:2506.19115](https://arxiv.org/abs/2506.19115) |
| Functional-equation (holomorphic) reformulation | Berg–Meinardus, 1994 | [Semantic Scholar](https://www.semanticscholar.org/paper/d7fe421b03e01d7f6dc0a41e9493f95f6a2784bf) |
| Holomorphic-dynamics extension to ℂ | Letherman–Schleicher–Wood, 1999 | [Exp. Math. 8](https://doi.org/10.1080/10586458.1999.10504402) |

### Undecidability

| Result | Source | Link |
|---|---|---|
| Generalized Collatz maps undecidable | Conway, 1972 | [PDF](https://gwern.net/doc/cs/computable/1972-conway.pdf) |
| Generalized Collatz problem Π⁰₂-complete (not the fixed 3n+1 map) | Kurtz–Simon, 2007 | [PDF](https://people.cs.uchicago.edu/~simon/RES/collatz.pdf) |
| BB(5) = 47,176,870, settled with a Rocq/Coq proof | bbchallenge (mxdys), 2024 | [wiki](https://wiki.bbchallenge.org/wiki/BB%285%29) |
| BB(6) open; S(6) > Σ(6) > 2↑↑↑5 | mxdys, June 2025 | [wiki](https://wiki.bbchallenge.org/wiki/BB%286%29) |
| Antihydra: a₀=8, a←⌊3a/2⌋, halts iff O > 2E. **Iterates ⌊3a/2⌋, not 3n+1** | mxdys, 2024 | [bbchallenge](https://bbchallenge.org/antihydra) · [wiki](https://wiki.bbchallenge.org/wiki/Antihydra) |
| TMs simulating 3x+1 on a given input (not blank-tape halting) | Michel, 2014 | [arXiv:1409.7322](https://arxiv.org/abs/1409.7322) |

Decidability of the fixed 3n+1 map is open. **No small Turing machine is known
whose halting is equivalent to the fixed 3n+1 conjecture**; Antihydra iterates a
different map, and Conway / Kurtz–Simon concern the parameterized family.
See [`contribution/proofs/FENCE.md`](contribution/proofs/FENCE.md) §1 and §8,
and [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md) §8.

## Constraint retained by reformulations

In every reformulation tested in this repository, the symbolic system can be
described independently of the condition that a transcript come from a
positive integer. Parity feedback assigns each positive integer exactly one
infinite word. On the 2-adic integers the map is conjugate to the full shift
(Bernstein–Lagarias), but that conjugacy alone does not preserve membership in
the positive integers. A reformulation of the Collatz conjecture must therefore
retain the positive-integer realizability condition.

## Fold non-conjugacy theorem

Definitions and proof details are indexed in
[`contribution/README.md`](contribution/README.md). The consolidated write-up is
[`contribution/note/NOTE.md`](contribution/note/NOTE.md).

**Fold operator.** For a residue class mod 2^k, the first-return map of T on the
class, renormalized, is an exact system of affine branches indexed by
first-return words.

**Theorem.** No two folds at distinct depths k, k′ ≤ 10 are affinely conjugate.

Proof outline:
1. Affine conjugacy preserves branch slopes 3^a/2^L; a slope determines the
   return length L by unique factorization.
2. Conjugate folds therefore have identical branch-count sequences.
3. Branch counts obey the counting law of the class window's pattern-avoidance
   automaton (Lemma 2). The exact laws of all 2,046 classes through depth 10
   give 85 distinct laws, none shared between depths.

The depth-2 branch counts are F₂₄ = 46368 and F₂₅ = 75025.

**Realizability criterion.** A parity transcript q with odd-step positions
d₀ < d₁ < … is realized by a positive integer iff

```
Φ(q) = −Σ_{j≥0} 2^(d_j) / 3^(j+1)  ∈  ℤ_{>0}
```

(the series converges 2-adically). Consequences proved: eventually-periodic
transcripts are decidable and cannot carry an infinite computation; the family
n/2, (n+b)/2 for odd b > 0 is non-universal by descent.

**Verification.** The programs use exact integer and rational arithmetic. An
independent implementation reproduced the counting-law screen, and direct
enumeration matched Lemma 2 in 196 of 196 tested positions. See
[`contribution/reports/VERIFICATION.md`](contribution/reports/VERIFICATION.md).

## Claim boundaries

Established in the repository:

- The fold non-conjugacy theorem (k ≤ 10).
- The realizability criterion and its two consequences.
- Exact exclusion of nontrivial positive cycles with at most 20 odd members
  (local finite window; not the global cycle bound from the literature, which
  dominates this bound — Hercher 2023 excludes ≤ 91 local minima).
- Pointwise complexity-pressure consequences for rational Φ, prefix-return
  barrier, rational-shadow deletion, and a primitive-uniform subcritical
  obstruction class (see packet + fence proofs).
- Non-realizability of 99 of the 109 enumerated supercritical 2-automatic
  words, via an exact computable bound on factor complexity. This shrinks a
  listed-open stratum; it does not close it (10 named words remain) and does
  not settle the general 2-automatic question.

Not established:

- These results do not imply that every positive integer reaches 1.
- The appearance of Fibonacci growth in aggregate residue-tree counts is not
  new. The repository derives a per-class counting law and uses it as an affine
  conjugacy invariant.
- The computations do not exclude a divergent trajectory; no finite search can
  certify the absence of a later return.
- No unconditional positive-integer counterexample is present.

The negative computational results are recorded in `contribution/reports/`:
the tested affine self-similarity condition fails across distinct depths up to
10; tested feature grammars do not outperform the mod-2^k baseline at equal
information budget; and the longest observed divergence-critical density run
below 2^20 is 217 steps.

## Verification commands

Python 3. The core fold programs (`contribution/code/`, including
`code/fence/`) use the standard library only and exact integer/rational
arithmetic. The packet verifiers under `contribution/packets/` additionally
require `numpy` for their float64 *measurements*; no proved statement depends
on it. Running the `test_*.py` files requires `pytest`. The plateau-drift
kernel uses `clang` when available and falls back to numpy otherwise.

```
python3 contribution/code/test_f1.py                  # word calculus
python3 contribution/code/test_f2.py                  # fold operator (~11 min)
python3 contribution/code/f2b_analytic_screen.py 8    # counting-law screen (~1 s)
python3 contribution/code/test_f4.py                  # feature-regression null result
python3 -m pytest contribution/code/fence/test_exact_cycle_search.py -q
python3 contribution/packets/2026-07-22-landmark-pointwise/verify_rational_complexity_finite.py
python3 contribution/packets/2026-07-24-supercritical-automatic-closure/verify_supercritical_closure.py       # ~16 s
python3 contribution/packets/2026-07-24-supercritical-automatic-closure/test_verify_supercritical_closure.py  # runs standalone or under pytest
python3 contribution/packets/2026-07-24-contraction-onset/verify_contraction_onset.py                         # ~5.5 min (VCO_HMAX=300000 for ~23 s)
python3 contribution/packets/2026-07-24-contraction-onset/test_verify_contraction_onset.py
python3 contribution/packets/2026-07-25-mahler-tower/verify_mahler_tower.py                                    # ~40 s (--dmax 3 for ~4 s)
python3 contribution/packets/2026-07-25-mahler-tower/test_verify_mahler_tower.py                               # 16 tests, 4 RED mutants
```

`test_f2.py`'s runtime is dominated by the `k ≤ 5` class-cache warm-up
(~11 min); its cylinder-disjointness check is an O(n log n) laminar sweep, not
a pairwise scan, because the branch lists reach 367,684 entries at `k = 3`.

Lean certificates (toolchain pinned in `formal/lean-toolchain`; no mathlib):

```
cd formal && lake build
```

## Attribution

Direction and problem selection: Ben Pham. Formalization and computation:
Claude Fable 5. Independent verification: GPT-5.6 Sol. The files supporting
each stated result are listed above, and the executable checks are listed under
Verification commands.

## License

Code: [MIT](LICENSE). Prose and mathematical exposition:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked papers remain
under their authors' copyrights.
