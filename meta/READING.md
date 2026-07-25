# Reading list, with verdicts

External material, each entry carrying an honest judgement of whether it
supplies a *tool* or only a *mood*. Full audits live in
[`TRANSFER_AUDITS.md`](TRANSFER_AUDITS.md).

## Read these

| Work | Why | Verdict |
|---|---|---|
| Lagarias, *The 3x+1 Problem: An Overview* ([arXiv:2111.02635](https://arxiv.org/abs/2111.02635)) | The map of the whole subject. Reading it is the cheapest way to avoid rediscovering a dominated result. | essential |
| Tao, *Almost all Collatz orbits attain almost bounded values* ([arXiv:1909.03562](https://arxiv.org/abs/1909.03562)) | The ceiling of every density method. The amplification branch is defined against it. | essential |
| Hercher (2023), Bařina (2025) | The two numbers that dominate every cycle bound. | essential |
| Hofstadter, *GEB*, **Ch. XIII + "Aria with Diverse Variations"** | Collatz by name; BlooP/FlooP and the Π₁ vs Π₂ distinction. Explains what an independence result would and would not buy. | real tool |
| Hofstadter, *GEB*, **Ch. III "Figure and Ground"** | r.e. sets whose complement is not r.e. The formal reason "characterise the counterexamples" is not symmetric with "characterise the survivors". | real tool |
| Allouche & Shallit, *Automatic Sequences* | Ch. 6 and §8.4 underpin every substitutive exclusion here; Thm 10.3.1 is Lemma D's prior art. | essential for the rigidity branch |
| **López & Stoll, *The 3x+1 Periodicity Conjecture in ℝ*** ([arXiv:2101.12747](https://arxiv.org/abs/2101.12747)) | Closes `liminf > log₃2` entirely. Subsumes this repo's supercritical work and defines the remaining gap. Should have been read first. | **essential** |
| Monks & Yazinski, *The Autoconjugacy of the 3x+1 Function* ([PDF](https://monks.scranton.edu/files/pubs/AutoConjV13.pdf)) | Thm 2.7(b) is the drift wall, for rationals, and predates it. | essential |
| Terras (1976), Garner (1981) | Coefficient stopping time. Read before touching the contraction-onset line. | essential for that line |
| bbchallenge wiki: [BB(5)](https://wiki.bbchallenge.org/wiki/BB%285%29), [BB(6)](https://wiki.bbchallenge.org/wiki/BB%286%29), [Antihydra](https://wiki.bbchallenge.org/wiki/Antihydra) | Accurate, current, and the model for distributed formally-verified work. Read for the method as much as the content. | real tool |

## Read only for a specific purpose

| Work | Purpose | Verdict |
|---|---|---|
| Hofstadter, *GEB*, Ch. I "The MU-puzzle" | The invariant-hunting move: the conserved quantity lives *outside* the rewriting system. | method, not content |
| Deng–Hani–Ma, kinetic limits ([arXiv:2408.07818](https://arxiv.org/abs/2408.07818)) | The best external analogue for amplification: ensemble behaviour derived from microscopic dynamics, as a theorem. Blocker: needs proved decorrelation, and the 2–3 lattice supplies persistent correlations. | best outside probe |
| Simons–de Weger; Rhin | Effective bounds on `\|K log 2 − m log 3\|`. Correct tool for the cycle branch only. | capped, see `TARGETS.md` §6 |

## Do not read for this purpose

| Work | Why not |
|---|---|
| Hofstadter, *GEB*, Ch. XX "Strange Loops" and the Introduction | Self-reference-as-aesthetic. Collatz has no self-referential encoding and Gödel's diagonal does not port to it. The famous part of GEB is the decorative part here. |
| Hofstadter, *GEB*, Ch. XV "Jumping out of the System" | Rhetorically appealing, technically thin. Ch. I already gives the usable half. |
| Bui-Thanh's inverse-problems corpus | Audited 2026-07-25: nothing transfers. Every method presumes a differentiable forward map with low-rank structure — a *low-complexity* requirement, pointed the wrong way. |
| Anything invoking "chaos" without an invariant measure | The 2-adic shift already has full topological entropy. Chaos is free here and explains nothing. `RATIONAL_IRRATIONAL_SHADOW.md` says so with a proof. |
| Antihydra as evidence about Collatz | It iterates `⌊3a/2⌋`, not `3n+1`. It shows BB(6) is hard. It says nothing about the fixed map. `COLLATZ_ONE_PAGE.md` §8. |

## The pattern in the negatives

Two independent methods have now saturated for the *same* reason: the
factor-complexity inequality and the low-rank/Hessian toolkit both require
their object to be **simple**, and the surviving counterexample candidates are
exactly the complex ones.

When evaluating any new external method, ask first: **does it consume
complexity, or require simplicity?** If the latter, it will hit the same wall,
and the audit can stop there.
