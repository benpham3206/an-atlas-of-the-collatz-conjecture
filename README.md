# An Atlas of the Collatz Conjecture

Reference map of the 3n+1 problem: principal results with source links, and one
original result on the first-return ("fold") structure of the map.

## Status

| Item | Status |
|---|---|
| Fold non-conjugacy theorem, depths k ≤ 10 | proved; machine-checked; independently verified |
| Realizability criterion Φ(q) ∈ ℤ_{>0} | proved |
| Bearing on the Collatz conjecture itself | none (see [Scope](#scope)) |

## Definition

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

## Contents

- [Landmarks](#landmarks) — principal results, with source links.
- [Structural obstruction](#structural-obstruction) — the 2-adic/3-adic conflict.
- [Original result](#original-result) — fold theorem and realizability criterion;
  full material in [`contribution/`](contribution/).
- [Scope](#scope) — claimed and not claimed.
- [Reproduction](#reproduction) — commands.
- [`exploratory/`](exploratory/) — speculative drafts; not results.

Papers are linked, not reproduced.

## Landmarks

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

## Structural obstruction

The 2-adic (halving) and 3-adic (3n+1) structures do not reconcile under known
reformulations. Each reformulation attempted in this repository reduces to a
free object plus one constraint: parity feedback assigns each integer exactly
one infinite word. On the 2-adic integers the map is the full shift
(Bernstein–Lagarias), so topological conjugacy carries no arithmetic
information. A reformulation preserves the problem only if it preserves this
constraint.

## Original result

Material: [`contribution/`](contribution/). Write-up:
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

**Verification.** Numeric claims are computed in exact arithmetic. The
counting-law screen was independently reimplemented; Lemma 2 matched enumeration
in 196/196 tested positions. See
[`contribution/reports/VERIFICATION.md`](contribution/reports/VERIFICATION.md).

## Scope

Claimed:
- The fold non-conjugacy theorem (k ≤ 10).
- The realizability criterion and its two consequences.

Not claimed:
- No result bears on the Collatz conjecture. All results concern the free side
  of the realizability constraint.
- Fibonacci growth of aggregate residue-tree level counts is prior/folklore. The
  result is the per-class counting law and its use as a conjugacy invariant.
- Divergent trajectories admit no finite certificate.

Closed with certificates: self-similarity shortcuts (the theorem); feature
grammars predicting stopping behavior beyond mod-2^k residues (none exceed the
baseline at matched information budget); sustained divergence-critical density
below 2^20 (longest run 217 steps).

## Reproduction

Python 3, standard library only, exact integer/rational arithmetic.

```
python3 contribution/code/test_f1.py                  # word calculus
python3 contribution/code/test_f2.py                  # fold operator (~11 min)
python3 contribution/code/f2b_analytic_screen.py 8    # counting-law screen (~1 s)
python3 contribution/code/test_f4.py                  # feature-regression null result
```

## Authorship

Direction and problem selection: Ben Pham. Formalization and computation: Claude
Fable 5. Independent verification: GPT-5.6 Sol. Each claim carries a status
label and traces to a committed artifact and a runnable check.

## License

Code: [MIT](LICENSE). Prose and mathematical exposition:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked papers remain
under their authors' copyrights.
