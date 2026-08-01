# What a counterexample must look like — and what it cannot

Every constraint this repository has proved, collected in one place. The
question "what can a Collatz counterexample *not* look like?" was answered
piecemeal across eight packets and three proof files; this is the consolidated
identikit.

**Nothing here proves the conjecture.** Each row narrows the search. The
residual class is still infinite and still contains the answer, whichever way
it goes.

Two conventions throughout. `T(n) = n/2` for even `n`, `(3n+1)/2` for odd —
the Terras form. `α = log₃2 = 0.6309297535…`, the critical one-density.
`κ = 1/log₂(3/2) = 1.7095112913…`, the critical factor-complexity slope.

---

## 0. There are exactly two shapes

A counterexample is a positive integer whose orbit does not reach 1. Its orbit
is either bounded or unbounded, and nothing else:

- **bounded** ⟹ it repeats a state ⟹ **a nontrivial cycle**;
- **unbounded** ⟹ **a divergent orbit**.

These have completely different certificate types, and confusing them is the
most common way a search wastes itself.

| | cycle | divergence |
|---|---|---|
| certificate | **finite** — a valuation word plus an exact divisibility check | **infinite** — needs a proved monotone invariant |
| verifiable in one session? | yes, if you found one | no; only the invariant is |
| current exclusion | > 1.375 × 10¹¹ odd members | none — no lower bound on a divergent start exists |

---

## 1. If it is a cycle

Let the cycle have `m` odd members, total 2-adic valuation `K`, offset `C_m`
from the recurrence `C_{j+1} = 3C_j + 2^{S_j}`.

**Must satisfy, exactly:**

1. `n = C_m / (2^K − 3^m)`, a positive **odd** integer — divisibility, not
   near-divisibility. A non-integer quotient is a *ghost shadow*, not a
   counterexample (`proofs/RATIONAL_IRRATIONAL_SHADOW.md`).
2. `2^K > 3^m`, hence one-density `m/K < α`. The cycle equation forces the
   period to be **subcritical**.
3. `3^m < 2^K ≤ (22/7)^m` — because every state is ≥ 7, since 1, 3 and 5 all
   reach 1 (`proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`).
4. `m/K` must be a near-resonance: `2^K ≈ 3^m` puts `K/m` at a continued-fraction
   convergent or semiconvergent of `log₂3`.
5. Direct iteration must reproduce the proposed valuations exactly, and close.

**Cannot be:**

- fewer than 92 local minima (Hercher 2023), hence — combined with Bařina's
  `2^71` verification — **not fewer than about 1.375 × 10¹¹ odd members**;
- anything with ≤ 20 odd members (this repo's own exhaustive search — dominated
  by the above by ~11 orders of magnitude, and retained only as an oracle).

---

## 2. If it is a divergent orbit

Let `q` be its parity word, `s_L` the number of ones in the first `L` symbols,
`p_q(k)` the number of distinct length-`k` factors.

**Must satisfy, all simultaneously:**

| # | constraint | source |
|---|---|---|
| 1 | `q` is **not eventually periodic** — an eventually periodic transcript gives an eventually periodic orbit, i.e. a cycle | `PARTIAL_THEOREMS.md` Thm 3 |
| 2 | `Φ(q) ∈ ℤ_{>0}` — the lift digits `ε_L` are eventually zero and the residue stabilises above 0 | `PARTIAL_THEOREMS.md` Thm 2, `LIFT_COCYCLE.md` |
| 3 | `liminf_L s_L/L` **= α exactly** — not merely ≥. Below α: drift wall. Strictly above α: López–Stoll 2021. Only the critical value survives | drift wall Thm 1 + [arXiv:2101.12747](https://arxiv.org/abs/2101.12747) |
| 4 | `limsup_k p_q(k)/k ≥ κ = 1.7095112913…` | landmark memo, Cor 4 |
| 5 | if its one-density `β` exists and its complexity constant `C` is finite: `(β − α)·C ≥ α` | landmark memo, Cor 7 |
| 6 | if its critical block discrepancy is bounded: **full binary factor entropy**, `limsup log₂p_q(k)/k = 1` | landmark memo, Cor 6 |
| 7 | at its tail minima, the blow-up limit lies in `S_ρ` — every prefix expansive, `3^{s_L} > 2^L` for all `L` | landmark memo, Thm 6.1 |
| 8 | `q` is **not automatic in any base** | `2026-08-01-automatic-density-closure` |

And, for a **least** counterexample specifically:

| 9 | `2^{A_h} ≤ 3^h` for every `h ≤ 10⁶` Syracuse steps — every prefix supercritical over the first ~1.58 × 10⁶ Terras steps | `2026-07-24-contraction-onset` |

Constraint 9 is the strongest finite-window statement available and is
unconditional: not a liminf, not almost-all, no structural hypothesis. It is
the reason "wins the 3-vs-2 tug-of-war at every single step" is the right
mental picture.

---

## 3. What it explicitly cannot be

Every entry is a proved exclusion, not a heuristic.

**By density (drift wall).** Any aperiodic word with `liminf s_L/L < α`:

- Thue–Morse (`½`), period-doubling (`⅓`), Rudin–Shapiro (`½`),
  regular paperfolding (`½`);
- the Fibonacci word and every Sturmian word of slope `< α`;
- binary Champernowne, and **every Borel-normal word** — full entropy does not
  save you;
- the block oscillator `[bitlength(n) odd]`, whose natural density does not
  even exist — the liminf form of the wall still reaches it.

**By complexity.** Any aperiodic word with `limsup p_q(k)/k < κ`:

- every Sturmian word (`p(k) = k+1`), hence all Fibonacci and golden-angle
  mechanical codings, at any slope;
- every quasi-Sturmian word (`p(k) = k + c`).

**By complexity + density together.**

- every primitive constant-length substitution fixed point with one-density
  `β < α` — the whole subcritical uniform-substitutive class, and not merely
  `Φ(q) ∉ ℤ_{>0}` but `Φ(q) ∉ ℚ_odd` (`PRIMITIVE_UNIFORM_OBSTRUCTION.md`);
- **99 of the 109** enumerated *supercritical* uniform-morphism survivors,
  including the rigidity packet's own proved witness `σ(0)=11, σ(1)=10`
  (`ρ = 2/3`), which dies on the single comparison `3²⁷ < 2⁴³`;
- every 2-automatic word generated by a DFAO with **at most two states**.

**By automatic lower density.** Every automatic word in every base, including
all uniform-morphism fixed points and codings. Bell 2020 makes its lower
density rational; López–Stoll require the irrational value `log₃2` for a
rational non-cyclic trajectory.

**By arithmetic.**

- anything realized only as a 2-adic integer, or only as an odd-denominator
  rational. The full shift on `ℤ₂` is free; positivity is the entire content
  (Bernstein–Lagarias, and `FENCE.md`).

**The band collapses.** Constraint 3 is the strongest single statement in this
file: combining the repository's drift wall with López–Stoll 2021, a divergent
orbit's parity word must have `liminf s_L/L` equal to `log₃2` **exactly**. Both
strict inequalities are closed. Every frequency-based argument is therefore
exhausted, and only complexity-based ones can still bite.

### Still open, and now named

- non-automatic words at the **exact critical density**
  `liminf s_L/L = log₃2` with high factor complexity;
- non-uniform morphic words whose natural one-frequency does not exist;
- the arithmetic amplification branch needed to turn one hypothetical
  divergent orbit into a positive-logarithmic-density exceptional family.

---

## 3a. How big is the surviving set?

Not a constraint on the counterexample, but a measurement of the space it must
live in — and it explains which methods can never find it.

The surviving symbolic set is `G = { q : liminf s_L/L = α }`.

| property | value | consequence |
|---|---|---|
| Bernoulli(1/2) measure | **0** | density and measure arguments, including Tao's, are structurally blind to it |
| Hausdorff dimension | **≥ H(α) ∈ (0.949952152, 0.949957233)** | it is not thin; it cannot be dismissed as degenerate |

Lower bound via Besicovitch (1934) / Eggleston (1949): `G` contains the level
set on which the frequency exists and equals `α`, whose dimension is the binary
entropy `H(α)`. Bounds are exact rationals certified by integer comparisons;
verifier [`contribution/code/dimension_bracket.py`](contribution/code/dimension_bracket.py).

**The reading.** A counterexample transcript lives in a set that is invisible to
measure and nearly full in dimension. Any instrument that finds it must be
pointwise and arithmetic. Statistical instruments are not weak here — they are
looking at a null set.


## 4. What a *proof* cannot look like

The dual question, and the more useful one for allocating effort. Each of these
is closed by a theorem, not by fashion.

| Shape of attempted proof | Why it cannot work |
|---|---|
| Forbid a finite parity word, or use a proper finite-window subshift | Terras: every finite word occurs, for a full residue class mod `2^L`. There is no forbidden local pattern. |
| Any computation to a finite bound | A finite check has no global quantifier. `n < 2^71` is already done. |
| Any almost-all or positive-density statement | Tao already proved the strongest known one. A counterexample lives in a measure-zero exceptional set by construction. |
| Averaged-density information alone for arbitrary critical words | The required condition is the lower natural density `liminf s_L/L = log₃2`; logarithmic, Cesàro or Abel values do not determine that liminf. |
| Phase-blind propagation from one layer | Plateau packet P2/P5: proved impossible. Phase-aware control at every layer is required. |
| Transfer of undecidability from generalized Collatz maps | Conway and Kurtz–Simon are about a *parameterized family*; both explicitly separate the fixed `3n+1` map. |
| Fold renormalization / self-similarity across depths | No two folds at distinct depths `k, k′ ≤ 10` are affinely conjugate. `FENCE.md` closes it. |
| A bounded correction to logarithmic size: `V(n) = log(n+1) + h(n)`, `h` bounded | Mersenne numbers `2^p − 1` rise by `p·log(3/2)` in `p` steps while `h` moves `O(1)`. No such Lyapunov function exists. |
| The 2-adic conjugacy alone | `T` on `ℤ₂` is conjugate to the full shift. Everything is realizable there. The conjugacy *is* the problem, not the solution. |
| Sharpening the contraction-onset depth | Capped by construction near `h ≈ 5 × 10¹⁰` regardless of Diophantine input (`TARGETS.md` §6). |
| Sharpening the factor-complexity constant | It is a **lower** bound on complexity, so it only ever kills *simple* objects. Saturates at two-state automata. |

**The residue.** After all of the above, a proof must supply one of exactly
two things:

1. **Rigidity**: every divergent orbit with zero-entropy symbolic closure
   violates positive-integer lift stabilization. *Entered; several strata
   closed.*
2. **Amplification**: every divergent orbit with positive-entropy symbolic
   closure contradicts logarithmic-density descent. *No theorem exists.*

Work that does not attach to one of those two statements is not on the
critical path.

---

## 5. The one-line version

> A counterexample is either a cycle whose period is a subcritical
> near-resonance of `log₂3` with more than 10¹¹ odd members, or a divergent
> orbit whose parity word is aperiodic, supercritical at every prefix for at
> least a million steps, of factor-complexity slope at least 1.71, of full
> entropy if its discrepancy is bounded, not any named low-complexity word,
> and whose 2-adic lift digits nevertheless switch off forever.
>
> Nobody has shown that object cannot exist.
