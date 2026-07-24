# Collatz attack packet — one page for Kimi K3 (and peers)

**Date:** 2026-07-22 (cycle-exclusion figures updated 2026-07-23)  
**Repo:** [an-atlas-of-the-collatz-conjecture](https://github.com/benpham3206/an-atlas-of-the-collatz-conjecture)  
**Status:** Collatz on positive integers remains **open**. Nothing below is a full proof or a counterexample.

Use this file as the entry brief. Proofs and verifiers are linked; do not invent
certificates.

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

Sturmian words (`p_q(k)=k+1`) are excluded from this rational class.  
Full memo: [`contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`](contribution/packets/2026-07-22-landmark-pointwise/COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md).

### 2.7 Rational shadows of aperiodic laws

Every finite aperiodic prefix has an odd-denominator rational periodic state with that prefix; these converge **2-adically** to the full law.  
⇒ Finite “strange” behavior never separates irrational 2-adic states from rational shadows.  
Proof + verifier: [`contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md`](contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md) · code under `contribution/code/fence/rational_shadow*`.

### 2.8 Primitive uniform subcritical obstruction

Primitive constant-length binary substitutions that are non-eventually-periodic with one-density `β < log₃ 2` cannot have `Φ(q)` in the odd-denominator rationals (hence not positive-integer transcripts).  
Proof: [`contribution/proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md`](contribution/proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md).

### 2.9 Supercritical primitive uniform words: complexity, not density

The supercritical half of that class is attacked with factor complexity instead. For aperiodic `q` with `Φ(q) ∈ ℚ_odd`,

```
C := limsup_k p_q(k)/k  ≥  α/(β − α)   for any β with  f(ℓ) ≤ βℓ + O(1)
```

(landmark memo Corollary 7; `β = 1` recovers Corollary 4's `C ≥ κ = 1.7095…`). `C` is *finitely computable* for a coding of a uniform-morphism fixed point, from the exact factor language — that is the whole content of the 2026-07-24 packet. It closes **99 of the 109** enumerated supercritical 2-automatic survivors, all 56 binary ones; **10 named ternary-coded automata remain**, and their complexity constants are exactly computed and genuinely above threshold.  
Proof + certificates: [`contribution/packets/2026-07-24-supercritical-automatic-closure/`](contribution/packets/2026-07-24-supercritical-automatic-closure/).

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

- Tao almost-all almost-bounded orbits: [arXiv:1909.03562](https://arxiv.org/abs/1909.03562)
- Hercher cycle theorem: [arXiv:2201.00406](https://arxiv.org/abs/2201.00406)
- Bařina verification limit: [DOI 10.1007/s11227-025-07337-0](https://doi.org/10.1007/s11227-025-07337-0)
- Bernstein–Lagarias 2-adic conjugacy to the shift (realizability wall is the leftover)

---

## 6. What to attempt (highest EV)

1. **Parser-density amplification:** if one positive survivor exists, force a positive log-density set of survivors → contradict Tao.
2. **Realizability for one named nonperiodic class** beyond eventual periodicity and beyond the subcritical primitive substitutions already excluded — prove `Φ(q) ∉ ℤ_{>0}`. Sharpest concrete target: the **ten** ternary-coded automata left open in §2.9. They need a mechanism that *consumes* high factor complexity rather than requiring it; sharpening the complexity bound provably cannot reach them.
3. **Divergence certificate** for a single explicit positive integer (infinite invariant / monotone certificate) — if you claim a counterexample.
4. **Cycle certificate** as a finite positive list verified under the acceptance gate in `EXACT_COUNTEREXAMPLE_SEARCH.md` — if you claim a counterexample.

**Delete (low EV / already closed here):**

- Short-cycle search with m ≤ 20 (and any further extension — dominated)  
- Forbidding finite parity words  
- Treating 2-adic / rational shadow orbits as positive-integer counterexamples  
- “Looks high for a long time” as divergence  

---

## 7. Hard rules for any agent run

1. State confidence and the exact remaining gap after every claim.  
2. Prefer one atomic lemma with a number in it and **kill criteria** before build criteria.  
3. Persist exact JSON / Lean certificates; never promote a finite cap-exit to a global theorem.  
4. Positive integers only for Collatz counterexamples.  
5. Reproduce with:

```bash
python3 -m pytest contribution/code/fence/test_exact_cycle_search.py -q
python3 contribution/packets/2026-07-22-landmark-pointwise/verify_rational_complexity_finite.py
python3 contribution/code/fence/rational_shadow.py   # if __main__ present
```

---

*Scope: internal research brief for follow-on agents. No Collatz proof or counterexample is claimed.*
