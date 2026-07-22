# An Atlas of the Collatz Conjecture

Literature references and reproducible exact-arithmetic analysis of
first-return systems for the Terras-accelerated Collatz map. The Collatz
conjecture remains open.

## Status

| Statement | Evidence |
|---|---|
| No folds at distinct depths k, k′ ≤ 10 are affinely conjugate | proof, exact-arithmetic screen, and independent reimplementation |
| A parity transcript q is realized by a positive integer iff Φ(q) ∈ ℤ_{>0} | derivation in `contribution/proofs/PARTIAL_THEOREMS.md` |
| No nontrivial positive cycle with ≤ 18 odd members | exact search + independent oracle: `contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` |
| Rational Φ with odd denominator forces complexity pressure; Sturmian excluded | pointwise memo in `contribution/packets/2026-07-22-landmark-pointwise/` |
| Collatz conjecture | neither proved nor disproved; no reduction from these results is established |

**Start here for agent handoff:** [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md)  
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
n < 2^68.

## Repository layout

| Path | Contents |
|---|---|
| [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md) | One-page attack brief (proved toolkit + open targets) |
| [`contribution/README.md`](contribution/README.md) | Index of definitions, proofs, programs, and verification reports |
| [`contribution/note/NOTE.md`](contribution/note/NOTE.md) | Fold theorem, proof outline, and limitations |
| [`contribution/proofs/`](contribution/proofs/) | Detailed proofs and formal statements |
| [`contribution/code/`](contribution/code/) | Exact-arithmetic implementations and executable checks |
| [`contribution/packets/2026-07-22-landmark-pointwise/`](contribution/packets/2026-07-22-landmark-pointwise/) | Landmark strategy, strategy machine, resonance lattice, prefix-return barrier, rational finite verifier |
| [`contribution/reports/`](contribution/reports/) | Recorded outputs and independent verification |
| [`exploratory/README.md`](exploratory/README.md) | Index of drafts that are not cited as results |

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
| 2-adic extension conjugate to the shift map | Bernstein–Lagarias, 1996 | [Canad. J. Math. 48](https://doi.org/10.4153/CJM-1996-060-x) |

### Statistical results

| Result | Source | Link |
|---|---|---|
| Almost all orbits attain almost bounded values | Tao, 2019/2022 | [arXiv:1909.03562](https://arxiv.org/abs/1909.03562) · [notes](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/) |
| Density lower bound #{n ≤ x reaching 1} ≥ x^0.84 | Krasikov–Lagarias, 2003 | [arXiv:math/0205306](https://arxiv.org/abs/math/0205306) |

Statistical methods control almost all orbits and do not reach a measure-zero
exceptional set.

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
| BB(6) reduces to a Collatz-like machine (Antihydra) | bbchallenge, 2024 | [wiki](https://wiki.bbchallenge.org/wiki/BB%286%29) |

Decidability of the fixed 3n+1 map is open. See
[`contribution/proofs/FENCE.md`](contribution/proofs/FENCE.md).

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
- Exact exclusion of nontrivial positive cycles with at most 18 odd members
  (local finite window; not the global cycle bound from the literature).
- Pointwise complexity-pressure consequences for rational Φ, prefix-return
  barrier, rational-shadow deletion, and a primitive-uniform subcritical
  obstruction class (see packet + fence proofs).

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

Python 3, standard library only, exact integer/rational arithmetic.

```
python3 contribution/code/test_f1.py                  # word calculus
python3 contribution/code/test_f2.py                  # fold operator (~11 min)
python3 contribution/code/f2b_analytic_screen.py 8    # counting-law screen (~1 s)
python3 contribution/code/test_f4.py                  # feature-regression null result
python3 -m pytest contribution/code/fence/test_exact_cycle_search.py -q
python3 contribution/packets/2026-07-22-landmark-pointwise/verify_rational_complexity_finite.py
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
