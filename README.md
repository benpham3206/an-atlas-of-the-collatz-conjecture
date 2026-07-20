# An Atlas of the Collatz Conjecture

A map of the 3n+1 problem: its major landmarks with links to the sources, and
one original contribution — a structural theorem about the map's first-return
("fold") behavior — placed on that map. The atlas is honest about scale. The
conjecture is open; nothing here changes that. What an atlas offers is
orientation: where the hard part lives, which approaches are charted, and where
a small new result sits relative to the giants.

> **Status of the original work:** one theorem `PROVEN` (with a machine-checked
> proof and three independent computational verifications), one exact wall
> formula `PROVEN`, several approach families closed `WITH CERTIFICATES`, and
> **no progress on the conjecture itself**. See [Not claimed](#not-claimed).

---

## The problem in one paragraph

The Collatz map sends n to n/2 when n is even and 3n+1 when n is odd; the
conjecture asserts every positive integer eventually reaches 1. It is elementary
to state and, in Lagarias's words, "completely out of reach of present day
mathematics." The difficulty is not computational — orbits are verified past
2^68 — but structural: the halving (2-adic) structure grinds against the 3n+1
(3-adic) structure, and no reformulation found so far removes that grinding
without also removing the problem.

## How to read this atlas

- **[Landmarks](#landmarks)** — the major results, with links. Start here.
- **[The obstruction](#the-obstruction)** — why the problem is hard, precisely.
- **[Original contribution](#original-contribution)** — the fold theorem and the
  realizability formula, with full proofs, code, and verification in
  [`contribution/`](contribution/).
- **[Not claimed](#not-claimed)** — the scope discipline. Read before citing.
- **[Exploratory](#exploratory)** — speculative "new field" sketches, clearly
  labeled as such, in [`exploratory/`](exploratory/).

---

## Landmarks

Links go to open-access sources (arXiv, author pages, publisher DOIs) where
available. Papers are linked, not reproduced — the copyrights are the authors'.

### Surveys and bibliography (start here)

| Work | Author | Link |
|---|---|---|
| *The 3x+1 Problem: An Overview* | Lagarias, 2021 | [arXiv:2111.02635](https://arxiv.org/abs/2111.02635) |
| *The 3x+1 Problem: An Annotated Bibliography (1963–1999)* | Lagarias | [arXiv:math/0309224](https://arxiv.org/abs/math/0309224) |
| *…Annotated Bibliography, II (2000–2009)* | Lagarias | [arXiv:math/0608208](https://arxiv.org/abs/math/0608208) |
| 3x+1 problem resource page | Lagarias | [umich.edu/~lagarias/3x+1.html](https://websites.umich.edu/~lagarias//3x+1.html) |

### Foundational structure

| Result | Source | Link |
|---|---|---|
| Parity words ↔ residues mod 2^k (bijection); stopping times | Terras, 1976, *Acta Arith.* 30 | [journal](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers) |
| Almost all n have finite stopping time | Everett, 1977, *Adv. Math.* 25 | [DOI](https://doi.org/10.1016/0001-8708(77)90087-1) |
| 2-adic extension conjugate to the shift map | Lagarias 1985; Bernstein–Lagarias, *Canad. J. Math.* 48 (1996) | [survey (JSTOR)](https://www.jstor.org/stable/2322189) |

### The statistical frontier

| Result | Source | Link |
|---|---|---|
| Almost all orbits attain almost bounded values | Tao, 2019/2022 | [arXiv:1909.03562](https://arxiv.org/abs/1909.03562) · [blog](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/) |
| Density lower bound (#{n ≤ x reaching 1} ≥ x^0.84) | Krasikov–Lagarias, 2003 | [arXiv:math/0205306](https://arxiv.org/abs/math/0205306) |

The statistical method is, in effect, complete: it controls the behavior of
*almost all* orbits. It cannot reach a measure-zero exceptional set by
construction, and a counterexample — if one exists — would live there.

### Cycles and the 2-vs-3 race

| Result | Source | Link |
|---|---|---|
| No nontrivial cycle with ≤ 91 local minima | Hercher, 2023, *J. Integer Seq.* 26 | [arXiv:2201.00406](https://arxiv.org/abs/2201.00406) |
| Cycle bounds via linear forms in logarithms | Simons–de Weger, 2005, *Acta Arith.* 117 | [DOI](https://doi.org/10.4064/aa117-1-3) |
| Nontrivial cycle length bound | Eliahou, 1993, *Discrete Math.* 118 | [DOI](https://doi.org/10.1016/0012-365X(93)90048-X) |

Cycle exclusion is the one theorem-producing bridge: a nontrivial cycle forces
2^b ≈ 3^a, which Baker-type transcendence bounds constrain. A cycle would be a
finite, checkable certificate; divergence would not.

### Semigroup and algebraic reformulations

| Result | Source | Link |
|---|---|---|
| The 3x+1 semigroup contains every positive integer (weak conjecture, proved) | Applegate–Lagarias, 2006 | [arXiv:math/0411140](https://arxiv.org/abs/math/0411140) |
| Two-operator calculus for arithmetic-progression paths | Angermund, 2025 | [arXiv:2506.19115](https://arxiv.org/abs/2506.19115) |
| Functional-equation (holomorphic) reformulation | Berg–Meinardus, 1994–95 | [semantic scholar](https://www.semanticscholar.org/paper/d7fe421b03e01d7f6dc0a41e9493f95f6a2784bf) |
| Holomorphic-dynamics extension to ℂ | Letherman–Schleicher–Wood, 1999, *Exp. Math.* 8 | [DOI](https://doi.org/10.1080/10586458.1999.10504402) |

### The undecidability fence

| Result | Source | Link |
|---|---|---|
| Generalized Collatz maps are undecidable | Conway, 1972, "Unpredictable Iterations" | [mirror (PDF)](https://gwern.net/doc/cs/computable/1972-conway.pdf) |
| Generalized Collatz problem is Π⁰₂-complete (not the fixed 3n+1 map) | Kurtz–Simon, 2007, TAMC | [PDF](https://people.cs.uchicago.edu/~simon/RES/collatz.pdf) |
| BB(6) hinges on a Collatz-like machine (Antihydra) | bbchallenge, 2024 | [wiki](https://wiki.bbchallenge.org/wiki/BB%286%29) · [Cryptids](https://wiki.bbchallenge.org/wiki/Cryptids) |

Whether the *specific* 3n+1 map can encode computation is open in both
directions. This atlas's [fence notes](contribution/proofs/FENCE.md) map exactly
where that boundary sits.

---

## The obstruction

Every reformulation attempted in this project — grammar closure, matrix
semigroups, tensor networks, feature regression, topological conjugacy — reduces
to the same shape: **a tame, fully-charted free object, plus one constraint.**
The constraint is that parity feedback assigns each integer exactly one infinite
word; the free object always forgets it. Topological conjugacy to the shift
(Bernstein–Lagarias) is the sharpest example: on the 2-adic integers the map is
the full shift, so pure topology carries no arithmetic information at all.

A good reformulation must preserve the 2-adic/3-adic grinding, not quotient it
away. That single test explains why decades of embeddings produced beautiful
mathematics and left the conjecture untouched.

---

## Original contribution

Full write-up: [`contribution/note/NOTE.md`](contribution/note/NOTE.md).
Guide to the folder: [`contribution/README.md`](contribution/README.md).

**The fold operator.** Restrict the Terras map to a residue class mod 2^k and
take its first-return map; the result is again an exact system of affine
branches — the map examining itself at depth k. Ask whether the map is
self-similar: can two folds at different depths be affinely conjugate?

**Theorem (`PROVEN`).** No two folds at different depths k, k′ ≤ 10 are affinely
conjugate. The proof: conjugacy preserves branch slopes 3^a/2^L, which encode
return-word lengths, so conjugate folds have identical branch-count sequences;
the exact counting laws of all 2,046 classes through depth 10 give 85 distinct
laws, none shared across depths. Branch counts obey the counting law of the
class window's pattern-avoidance automaton, which is why consecutive Fibonacci
numbers (F₂₄ = 46368, F₂₅ = 75025) appear verbatim in the depth-2 data.

**The realizability formula (`PROVEN`).** A parity transcript q with odd steps at
positions d₀ < d₁ < … is realized by a positive integer if and only if

```
Φ(q) = −Σ_{j≥0} 2^(d_j) / 3^(j+1)  ∈  ℤ_{>0}      (converges 2-adically)
```

This states the central obstruction as a single condition. Two consequences are
proved: eventually-periodic transcripts form a decidable island that cannot
carry an infinite computation, and the entire (n+b)/2 map family below 3n+1 is
non-universal by elementary descent.

**Verification.** Every numeric claim is machine-checked in exact arithmetic; the
counting-law screen was independently reimplemented and Lemma 2's formula matched
enumeration in 196/196 tested positions (see
[`contribution/reports/VERIFICATION.md`](contribution/reports/VERIFICATION.md),
by GPT-5.6 Sol).

---

## Not claimed

- **No progress on the Collatz conjecture.** Every result here concerns the free
  side of the realizability constraint. The conjecture is exactly as open as
  before.
- **Fibonacci growth of aggregate residue-tree level counts is folklore.** The
  contribution is the *per-class* counting law, its proof, and its use as a
  conjugacy invariant — not the appearance of Fibonacci.
- **Divergent trajectories admit no finite certificate**; no computation here
  could witness one.
- Closed with certificates during the work: self-similarity shortcuts (the
  theorem); arithmetic feature grammars predicting stopping behavior beyond
  mod-2^k residues (none beat the baseline at matched information budget);
  sustained divergence-critical density below 2^20 (longest run 217 steps).

---

## Exploratory

The [`exploratory/`](exploratory/) folder holds speculative sketches toward a
"mathematics of changing laws" (metadynamical geometry) produced during the
project. These are **not results** — they are founding-document drafts whose
terms have not yet earned their place by producing theorems. Labeled as such so
no reader mistakes a sketch for a claim.

---

## Reproducing the computations

Python 3, standard library only, exact integer/rational arithmetic throughout.

```
python3 contribution/code/test_f1.py            # word calculus (Terras bijection, cycle sweep)
python3 contribution/code/test_f2.py            # fold operator (induced maps, ~11 min)
python3 contribution/code/f2b_analytic_screen.py 8   # counting-law screen (0.64 s)
python3 contribution/code/test_f4.py            # feature-regression null result
```

## Provenance and method

This atlas was produced in a human-directed, AI-assisted collaboration: problem
selection, framing, and the key observations (the fold question, the Fibonacci
catch) by Ben Pham; formalization, computation, and verification by Claude Fable
5, with independent proof-checking by GPT-5.6 Sol. Every claim carries a status
label; every number traces to a committed artifact and a runnable check. That
audit trail — not the prose — is the evidence.

## License

Code under [MIT](LICENSE). Prose and mathematical exposition under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked papers remain
under their authors' copyrights.
