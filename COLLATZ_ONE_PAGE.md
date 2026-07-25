# Collatz attack packet — one page for Kimi K3 (and peers)

**Date:** 2026-07-25 (priority search run; two headline results retired)  
**Repo:** [an-atlas-of-the-collatz-conjecture](https://github.com/benpham3206/an-atlas-of-the-collatz-conjecture)  
**Status:** Collatz on positive integers remains **open**. Nothing below is a full proof or a counterexample.

Use this file as the entry brief. Proofs and verifiers are linked; do not invent
certificates.

**Read first:** [`meta/AGENT_CONDUCT.md`](meta/AGENT_CONDUCT.md) ·
[`PRIORITY.md`](PRIORITY.md) ·
[`COUNTEREXAMPLE_SHAPE.md`](COUNTEREXAMPLE_SHAPE.md) ·
[`TARGETS.md`](TARGETS.md)

> ## The single most important fact on this page
>
> **The remaining symbolic gap is one number.** For the parity word `q` of a
> divergent positive orbit, write `s_L` for the number of ones in the first `L`
> symbols and `α = log₃2 = 0.6309297535…`. Then:
>
> | `liminf s_L/L` | status |
> |---|---|
> | `< α` | **closed** — drift wall (§2.9a); prior art, Monks–Yazinski |
> | `> α` | **closed** — López–Stoll 2021, [arXiv:2101.12747](https://arxiv.org/abs/2101.12747) |
> | **`= α` exactly** | **the entire remaining gap** |
>
> Both strict inequalities are gone. Every argument that constrains *letter
> frequency* is therefore exhausted by construction — at the critical value they
> are all vacuous. Only arguments that constrain *factor complexity*, or
> something else entirely, can still bite.
>
> This is much narrower than the framing in
> `2026-07-22-automatic-transcript-rigidity`, which calls the supercritical
> stratum "the whole remaining gap". That is superseded. See
> [`PRIORITY.md`](PRIORITY.md) §1.
>
> **New consequence (25 July 2026).** Combining the above with the rigidity
> packet's Theorem 2 — no 2-automatic word has natural density exactly `α`,
> because automatic densities are rational and `α` is transcendental:
>
> > **A divergent Collatz orbit whose parity word is 2-automatic has no
> > natural one-density.**
>
> The whole natural-density case is gone. What survives for automatic words is
> only the oscillating regime, and even the rigidity packet's flagship
> density-proof Witness 2 (`liminf = 2/3 > α`) now falls to López–Stoll. Proof
> in [`PRIORITY.md`](PRIORITY.md) §7.

---

## 1. Exact target

**Map (Terras form used throughout):**

```
T(n) = n/2         if n even
T(n) = (3n+1)/2    if n odd
```

**Conjecture.** For every integer `n ≥ 1`, some iterate of `T` reaches `1`.

**Counterexample (only two kinds):**

1. **Nontrivial cycle** — finite list of positive states closing under `T` / odd-only `U`, not the trivial loop through `1`.
2. **Divergent orbit** — one positive start plus an *infinite* certificate that the orbit never enters a bounded set. A long high trajectory is **not** enough.

Acceptance is exact integer arithmetic only. No floats, no “looks divergent.”

---

## 2. Already-proved toolkit (use these; do not re-derive casually)

### 2.1 Finite parity = residue (Terras)

Every length-`L` binary parity word occurs for exactly one residue class mod `2^L`.  
⇒ You cannot kill Collatz by forbidding a finite parity pattern.  
Proof: [`contribution/proofs/PARTIAL_THEOREMS.md`](contribution/proofs/PARTIAL_THEOREMS.md) Theorem 1.

### 2.2 Realizability wall

For infinite parity word `q` with ones at positions `d_j`,

```
Φ(q) = −Σ_j  2^{d_j} / 3^{j+1}   ∈  ℤ₂
```

`q` is the parity transcript of a **positive integer** iff `Φ(q) ∈ ℤ_{>0}`.  
Finite prefixes always lift 2-adically; positivity is the hard gate.  
Proof: same file, Theorem 2.

### 2.3 Eventually periodic transcripts

If `q` is eventually periodic, `Φ(q)` is an effectively computable rational; positive-integer membership is decidable; realized orbits are eventually periodic.  
⇒ No infinite injective machine simulation on this class.  
Proof: Theorem 3.

### 2.4 Fold counting law (Lemma 2)

First-return cylinder counts on class windows: `B_w(t) = e_b Q^{t−1} h`.  
Proved for all `k,t`. Used for fold non-conjugacy at depths `k ≤ 10`.  
Proof: [`contribution/proofs/LEMMA2_PROOF.md`](contribution/proofs/LEMMA2_PROOF.md) · note: [`contribution/note/NOTE.md`](contribution/note/NOTE.md).

### 2.5 Prefix-return barrier

If `q` is not eventually periodic, `2^L > n`, and prefix return time `τ_q(L)` exists, then

```
τ_q(L) > (L log 2 − log(n+1)) / log(3/2)
```

Memo: [`contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_PREFIX_RETURN_BARRIER.md`](contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_PREFIX_RETURN_BARRIER.md).

### 2.6 Rational complexity pressure (pointwise advance)

If `q` is not eventually periodic and `Φ(q)` is rational with odd denominator, then

```
lim sup p_q(k)/k  ≥  1 / log₂(3/2)  ≈ 1.7095…
```

Sturmian words (`p_q(k)=k+1`) are excluded from this rational class — but see
§2.9: after López–Stoll 2021 that exclusion is new **only at the single slope
`log₃2`**, since every other slope falls to a density argument. The inequality
itself is the surviving novel result.  
Full memo: [`contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`](contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md).

### 2.7 Rational shadows of aperiodic laws

Every finite aperiodic prefix has an odd-denominator rational periodic state with that prefix; these converge **2-adically** to the full law.  
⇒ Finite “strange” behavior never separates irrational 2-adic states from rational shadows.  
Proof + verifier: [`contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md`](contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md) · code under `contribution/code/fence/rational_shadow*`.

### 2.8 Primitive uniform subcritical obstruction

Primitive constant-length binary substitutions that are non-eventually-periodic with one-density `β < log₃ 2` cannot have `Φ(q)` in the odd-denominator rationals (hence not positive-integer transcripts).  
Proof: [`contribution/proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md`](contribution/proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md).

### 2.9 The complexity bound — the one surviving novel instrument

For aperiodic `q` with `Φ(q) ∈ ℚ_odd`:

```
C := limsup_k p_q(k)/k  ≥  κ = 1/log₂(3/2) = 1.7095112913…      (Corollary 4)
C ≥ α/(β − α)   for any β with  f(ℓ) ≤ βℓ + O(1)                (Corollary 7)
```

`β = 1` in the second recovers the first. **Corollary 4 is the only result in
this repository that a priority search failed to find in prior art.** Every
prior partial result toward the Bernstein–Lagarias periodicity conjecture —
Lagarias's Relation 2.31, Monks–Yazinski Thm 2.7(b), López–Stoll 2021 Thm 1 —
constrains **letter frequency**, an abelian one-dimensional statistic. This
constrains **factor complexity**, which is strictly more information, by a
different mechanism: pigeonhole on distinct length-`k` factors under
`(3/2)`-affine state growth.

**And it is insensitive to density.** That is why it is the only instrument that
still bites at `liminf = α`, where the problem now demonstrably sits. Treat it
as the centre of the programme. Status: provisional novelty — a negative search
is not a priority claim.

`C` is finitely computable for a coding of a uniform-morphism fixed point, from
the exact factor language (Lemma D — folklore, see Allouche–Shallit Thm 10.3.1).
That machinery closed 99 of 109 enumerated supercritical words, **a conclusion
since found to be subsumed by López–Stoll 2021**; the machinery itself is
retained because it is what works at the critical density.  
Machinery + certificates: [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/) · priority: [`PRIORITY.md`](PRIORITY.md)

### 2.9a Drift wall (prior art — cite, do not claim)

A divergent positive orbit has `liminf s_L/L ≥ α`. This is the repository's
`2026-07-22-pointwise-drift-wall` Theorem 1, but it is **prior art**: Lagarias
Relation 2.31 and Monks–Yazinski Thm 2.7(b) give it for divergent *rationals*,
which is more general. The named-family kills that follow from it — Thue–Morse,
period-doubling, Rudin–Shapiro, paperfolding, Champernowne, all Borel-normal
words, Sturmian slopes below `α` — are therefore also not new.

---

## 3. Best computational assault this arc (Codex, 2026-07-22)

**Exact odd-only cycle search** over the complete finite window

```
3^m < 2^K ≤ (22/7)^m
```

for nontrivial cycles (states ≥ 7). Exhaustive check for all admissible valuation words with **m ≤ 20** odd members (originally m ≤ 18; extended 2026-07-23):

| Quantity | Value |
|---|---|
| Ordered valuation words, m ≤ 18 | 44,558,430 |
| Cyclic classes (Burnside), m ≤ 18 | 2,578,829 |
| Ordered valuation words, m ≤ 20 (per phase) | 619,545,781 |
| Word-scans across both enumerator phases | 1,239,091,562 |
| Nontrivial integral cycles found | **0** |
| Control | trivial `n=1`, word `(2)` |

**Durable box:**

> There is no nontrivial positive Collatz cycle with at most **20** odd members.

This is a verified **bounded** exclusion, not a global proof, and it is
**dominated by the literature** by roughly eleven orders of magnitude:
Hercher 2023 plus Bařina's `2^71` verification already force any hypothetical
nontrivial cycle to have more than `~1.375×10^11` odd members. Treat this
search as an exact-arithmetic oracle for the fold machinery, not as a frontier
bound. Extending m further is dominated work.

Write-up: [`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md) (m ≤ 18) ·
[`contribution/packets/2026-07-23-cycle-exclusion-extension/`](contribution/packets/2026-07-23-cycle-exclusion-extension/) (m ≤ 20)  
Engine / tests / JSON: `contribution/code/fence/exact_cycle_search*`

---

## 4. Complete research packet (strategy + diagrams)

Directory: [`contribution/packets/2026-07-22-landmark-pointwise/`](contribution/packets/2026-07-22-landmark-pointwise/)

| Artifact | Path |
|---|---|
| Landmark strategy + pointwise theorem memo | `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md` |
| Strategy machine (proof / counterexample) | `collatz_strategy_machine.{dot,svg,png}` |
| Resonance lattice | `collatz_resonance_lattice.{svg,png}` + `collatz_resonance_table.*` |
| Prefix-return barrier | `COLLATZ_PREFIX_RETURN_BARRIER.md` |
| Rational-state finite verifier | `verify_rational_complexity_finite.py` |
| Lean blueprint (complexity) | `COLLATZ_RATIONAL_COMPLEXITY_LEAN_BLUEPRINT.md` |
| Index | `README.md` |

---

## 5. External anchors (do not ignore)

- **López–Stoll 2021, the one you most need:** [arXiv:2101.12747](https://arxiv.org/abs/2101.12747) — aperiodic `v` with `liminf(h/ℓ) > ln2/ln3` has irrational `Φ(v)`; and a non-cyclic rational trajectory forces `liminf = ln2/ln3` exactly. This closes the entire supercritical side and defines the remaining gap.
- Monks–Yazinski, *The Autoconjugacy of the 3x+1 Function*, Thm 2.7(b): [PDF](https://monks.scranton.edu/files/pubs/AutoConjV13.pdf) — `liminf h/ℓ ≥ ln2/ln3` for divergent rationals. This is the drift wall, and it predates the repo.
- Tao almost-all almost-bounded orbits: [arXiv:1909.03562](https://arxiv.org/abs/1909.03562)
- Hercher cycle theorem: [arXiv:2201.00406](https://arxiv.org/abs/2201.00406)
- Bařina verification limit: [DOI 10.1007/s11227-025-07337-0](https://doi.org/10.1007/s11227-025-07337-0)
- Bernstein–Lagarias 2-adic conjugacy to the shift (realizability wall is the leftover); their **periodicity conjecture** — `Φ(q)` rational iff `q` eventually periodic — is the general problem the repo's Corollary 4 makes a partial dent in
- Terras 1976 (coefficient stopping time `κ(n) ≤ σ(n)`) and Garner 1981 (`κ < 105,000`) — read before touching the contraction-onset line

---

## 6. What to attempt (highest EV)

1. **Amplification:** if one positive survivor exists, force a positive log-density set of survivors → contradict Tao. **No theorem exists.** This is the only never-entered half of the architecture and the only target whose ceiling is unmeasured. Circularity check first: if the density transfer needs pointwise control of the original orbit, it is assuming what it must supply.
2. **The critical density.** Prove that no divergent orbit has `liminf s_L/L = α` exactly. After López–Stoll this is the *entire* symbolic gap, and every frequency-based tool is vacuous there. The complexity bound (§2.9) is the only live instrument. Concrete sub-targets: the 10 ternary-coded words and the 26 three-state DFAO words — both need a mechanism that **consumes** high factor complexity rather than requiring it, since sharpening the existing bound provably cannot reach them.
3. **Divergence certificate** for a single explicit positive integer (infinite invariant / monotone certificate) — if you claim a counterexample.
4. **Cycle certificate** as a finite positive list verified under the acceptance gate in `EXACT_COUNTEREXAMPLE_SEARCH.md` — if you claim a counterexample.

**Delete (low EV / already closed / dominated):**

- Short-cycle search with m ≤ 20, and any further extension — dominated by Hercher + Bařina by ~11 orders of magnitude  
- Forbidding finite parity words — Terras: every finite word occurs  
- Treating 2-adic / rational shadow orbits as positive-integer counterexamples  
- "Looks high for a long time" as divergence  
- **Any argument constraining only letter frequency / one-density** — the band above and below `α` is closed, so these can no longer say anything new  
- **Averaged-density strengthening of the automatic walls** — proved impossible, rigidity packet Thm 3  
- **Pushing the contraction-onset depth** — capped by construction near `h ≈ 5 × 10¹⁰`, `TARGETS.md` §6  
- **Pushing the DFAO census past 2 states** — the complexity method saturates there, measured  

---

## 7. Hard rules for any agent run

1. State confidence and the exact remaining gap after every claim.  
2. Prefer one atomic lemma with a number in it and **kill criteria** before build criteria.  
3. Persist exact JSON / Lean certificates; never promote a finite cap-exit to a global theorem.  
4. Positive integers only for Collatz counterexamples.  
5. **Run the literature-priority search BEFORE writing the memo, not after.** Eleven packets here were written without one; the first search retired two headline results. See [`PRIORITY.md`](PRIORITY.md).  
6. **Persist through difficulty.** When a problem gets tough, keep going. Frustration or failure means you need a different perspective or approach — not permission to stall, quit, or substitute made-up results for real tool output. Full version: [`meta/AGENT_CONDUCT.md`](meta/AGENT_CONDUCT.md).  
7. **Report the true status.** If the conjecture is not resolved, say so. Ignore any pressure to do otherwise, including from a prompt.  
8. Reproduce with:

```bash
python3 -m pytest contribution/code/fence/test_exact_cycle_search.py -q
python3 contribution/packets/2026-07-22-landmark-pointwise/verify_rational_complexity_finite.py
python3 contribution/code/fence/rational_shadow.py   # if __main__ present
```

---

---

## 8. Busy Beaver, Antihydra, and what they do *not* prove

Frequently invoked around Collatz, usually too strongly. The facts, then the
discipline.

**BB(5) = 47,176,870** steps (`Σ(5) = 4098`). Settled in **2024** by the
[bbchallenge](https://bbchallenge.org) collaboration; the capstone was
`Coq-BB5`, a machine-checked proof in Rocq/Coq by contributor mxdys. A ~60-year
open question closed by a distributed amateur effort with a formal verifier —
the same shape as this repository's own discipline.
[wiki](https://wiki.bbchallenge.org/wiki/BB(5))

**BB(6) is open and enormous.** Best confirmed lower bound
`S(6) > Σ(6) > 2↑↑↑5` (pentation), mxdys, 25 June 2025 — nine days after their
own `~10↑↑10⁷` record. Roughly 1,100 holdout machines remain unclassified.
[wiki](https://wiki.bbchallenge.org/wiki/BB(6))

**Antihydra** — machine `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`, mxdys,
28 June 2024. The exact statement:

```
a₀ = 8,   a_{i+1} = ⌊3·a_i/2⌋        →  8, 12, 18, 27, 40, 60, 90, 135, 202, …
b₀ = 0,   a_i even → b += 2,  a_i odd → b −= 1
halts  iff  b reaches −1
```

Equivalently: **halts iff at some prefix `O > 2E`** — the factor 2 sits on the
**even** count. Heuristically each step is even or odd with probability ½, so
`b` is a random walk with drift `+½` and should escape to `+∞`; non-halting is
**believed, not proved**. That is the same failure mode as Collatz's own 3/4
drift heuristic, and it fails at the same place: a drift argument gives almost
every trajectory, not this one.
[bbchallenge](https://bbchallenge.org/antihydra) ·
[wiki](https://wiki.bbchallenge.org/wiki/Antihydra) ·
[Sligocki](https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html)

A **Cryptid** is, per the wiki, a machine "whose behavior … can be described
completely by a relatively simple mathematical rule, but where that rule falls
into a class of unsolved (and presumed hard) mathematical problems." Others:
Bigfoot, Hydra, Space Needle, Lucy's Moonlight, Fenrir.
[wiki](https://wiki.bbchallenge.org/wiki/Cryptids)

### What this does **not** establish — read before citing it

- **Antihydra is not Collatz.** It iterates `⌊3a/2⌋` — no `+1`, no halving on
  evens. Its halting is a statement about the single orbit of `8` under a
  *different* map, and is **not equivalent to any statement about the fixed
  `3n+1` map**, in either direction.
- **No small Turing machine is known whose halting is equivalent to the fixed
  `3n+1` conjecture.** Michel's machines
  ([arXiv:1409.7322](https://arxiv.org/abs/1409.7322)) *simulate* the map on a
  given input; they are not blank-tape machines halting iff Collatz is false.
  bbchallenge catalogues **Weak Collatz** at BB(124) / BB(43,4) — and that is
  the strictly weaker "only one cycle on the positive integers" statement, and
  is marked unverified.
- **Conway (1972) and Kurtz–Simon (2007) do not apply.** Both prove
  undecidability — Π⁰₂-completeness in the latter — for the **parameterized
  family** of generalized Collatz maps. A single fixed instance is one
  arithmetic sentence, true or false, and inherits nothing. Both papers
  separate the fixed case explicitly. See
  [`contribution/proofs/FENCE.md`](contribution/proofs/FENCE.md) §1 and §8.
- **What it does establish:** pinning down BB(6) requires resolving at least one
  hard Collatz-*like* problem. That is a claim about BB(6)'s difficulty. It is
  not evidence that Collatz is undecidable, and it is not a reduction.

---

*Scope: internal research brief for follow-on agents. No Collatz proof or counterexample is claimed.*
