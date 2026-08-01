# The Mahler tower of a uniform-morphic transcript, and where it breaks

> **Superseded target notice (2026-08-01).** The functional-system theorems
> below remain valid. The ten Collatz test words are no longer open: every
> uniform-morphic word is automatic, Bell 2020 makes its lower density
> rational, and López–Stoll 2021 require the irrational lower density
> `log₃2` for a rational non-cyclic trajectory. See
> `../2026-08-01-automatic-density-closure/AUTOMATIC_DENSITY_CLOSURE.md`.

**Date.** 2026-07-25.
**Branch served.** Rigidity.
**Target.** `TARGETS.md` § "The redirect that follows", bounded check 1 —
*is `Φ(q)` for a `k`-uniform morphic `q` the value at a specific point of a
solution of a Mahler-type functional equation? The mixed bases 2 and 3 are the
obstruction.*

---

## 1. The claim

> **Claim.** For every letter-coding `q = τ(u)` of the fixed point `u` of a
> `k`-uniform morphism `σ` on `d` letters, `Φ(q)` is the value at the rational
> point `(z, y) = (2, 3^{−τ})` of an explicit `d`-dimensional functional system
> with substitution `(z, y) ↦ (z^k, y^M)`, where `M` is the incidence matrix of
> `σ`. The mixed bases 2 and 3 do **not** obstruct the functional equation.
> They obstruct the **evaluation point**: the `y`-coordinates are 2-adic units,
> which is the boundary case excluded by every form of Mahler's method, and the
> induced one-variable tower converges only when `τ M^e → 0` in `ℤ₂^d`.
> **Six of the ten remaining supercritical survivors fail that condition; four
> satisfy it.**

The number in the claim is **6 of 10**. Every one of the ten verdicts is
proved, not measured — see §7.

**This does not prove or disprove the Collatz conjecture, and produces no
counterexample candidate.** The conjecture remains open.

---

## 2. Kill criteria, written before the build

| # | Criterion | Outcome |
|---|---|---|
| 1 | If no finite functional system exists, the redirect dies; report and stop. | **Did not fire.** The system exists for *every* uniform morphism (Theorem 1), verified on 240 random (morphism, point) pairs. |
| 2 | If a system exists but its `Φ` disagrees with the defining series anywhere mod `2^N`, the algebra is wrong; report and stop. | **Did not fire.** 240/240 agree mod `2^160`. |
| 3 | If a system exists but the evaluation point violates the convergence hypothesis of Mahler's method, that is the real obstruction and must be stated as such, not buried. | **FIRED.** This is the packet's main content. See §6. |

Kill criterion 3 firing is the result. The redirect is not dead, but it is not
what `TARGETS.md` described, and the reason it is blocked has moved.

---

## 3. Definitions

`σ` is a `k`-uniform morphism on the alphabet `A = {0, …, d−1}`, prolongable at
a seed, with fixed point `u`. `τ : A → {0,1}` is a letter-coding and
`q_n = τ(u_n)`. Write

- `s_n = #{i < n : q_i = 1}`, the accumulated one-count;
- `c_a(n) = #{i < n : u_i = a}`, the accumulated letter-counts;
- `M[a][b] = ` the number of occurrences of `a` in `σ(b)`, the incidence matrix.
  Every column of `M` sums to `k`.

`Φ` is the Bernstein–Lagarias conjugacy of `contribution/proofs/PARTIAL_THEOREMS.md`
Theorem 2: with `d_0 < d_1 < ⋯` the positions of the ones of `q`,

```
Φ(q) = − Σ_{j≥0} 2^{d_j} / 3^{j+1}   ∈ ℤ₂ .
```

Reindexing the sum by position rather than by rank of the one gives the form
used throughout below:

```
Φ(q) = − (1/3) Σ_{n≥0} q_n · 2^n · 3^{−s_n} .            (†)
```

`(†)` is where both bases become visible at once: `2^n` carries the position
and `3^{−s_n}` carries the accumulated one-count.

---

## 4. Theorem 1 — the functional system

Define, for each letter `b`, the generating function

```
f_b(z, y) = Σ_{n : u_n = b}  z^n · Π_a y_a^{c_a(n)} ,        y = (y_0, …, y_{d−1}).
```

**Theorem 1.** With `(y^M)_b := Π_a y_a^{M[a][b]}`,

```
f_b(z, y) = Σ_a  Q_{a,b}(z, y) · f_a(z^k, y^M) ,
```

where `Q_{a,b}(z, y) = Σ_{r < k, σ(a)_r = b} z^r · Π_c y_c^{γ_c(a,r)}` and
`γ_c(a,r) = #{t < r : σ(a)_t = c}`.

**Proof.** Write `n = km + r` with `0 ≤ r < k`; this is a bijection between
`ℕ` and `{(m,r)}`. Because `σ` is `k`-uniform, `u_n = σ(u_m)_r`, so the
condition `u_n = b` becomes `σ(u_m)_r = b`. The prefix `u_0 ⋯ u_{n−1}` is
`σ(u_0) ⋯ σ(u_{m−1})` followed by the first `r` letters of `σ(u_m)`, so

```
c_a(km + r) = Σ_{i < m} (number of a in σ(u_i))  +  γ_a(u_m, r)
            = Σ_b M[a][b] · c_b(m)  +  γ_a(u_m, r).
```

Hence `Π_a y_a^{c_a(km+r)} = (Π_a y_a^{γ_a(u_m,r)}) · Π_b (y^M)_b^{c_b(m)}`,
and `z^{km+r} = z^r · (z^k)^m`. Summing over `m` with `u_m = a` and over the
`r` with `σ(a)_r = b` gives the stated identity. ∎

**The point.** The base-3 weight is not eliminated and is not left dangling.
It is absorbed into a **monomial substitution** `y ↦ y^M` driven by the
incidence matrix. That is why the mixed bases do not obstruct the equation.

**Verified.** 240 random `(σ, y)` pairs over `d ∈ {2,3,4}`, `k ∈ {2,3}`, with
`y` a random vector of 2-adic units, all exact mod `2^160`. The verifier also
contains a RED test: dropping the `y ↦ y^M` substitution breaks the identity,
so the check is not passing vacuously.

---

## 5. Theorem 2 — the bridge to `Φ`

**Theorem 2.** Let `y*_a = 3^{−τ(a)}`. Then

```
Φ(q) = − (1/3) · Σ_{b : τ(b) = 1}  f_b(2, y*) .
```

**Proof.** `Π_a (y*_a)^{c_a(n)} = 3^{−Σ_a τ(a) c_a(n)} = 3^{−s_n}`, since
`Σ_a τ(a) c_a(n)` counts exactly the positions `i < n` with `q_i = 1`.
Restricting the sum to letters `b` with `τ(b) = 1` selects the `n` with
`q_n = 1`. The result is `(†)`. Convergence in `ℤ₂` is the convergence of `(†)`,
which is Theorem 2 of `PARTIAL_THEOREMS.md`. ∎

**Verified.** 240 random cases, `Φ` from the system versus `Φ` from the
Bernstein–Lagarias series over the first `2^12` letters, exact agreement mod
`2^160`. The series route is an **independent re-implementation**: it never
forms `M`, `Q`, or the letter-count vectors. Floor checks: the all-ones word
gives `Φ = −1`, the all-zeros word gives `Φ = 0`, a single one at position `p`
gives `Φ = −2^p/3`, and `(10)^∞` gives `Φ = 1`.

---

## 6. Where it actually breaks

Iterating the substitution from `(2, y*)` gives

```
z_e = 2^{k^e} ,        y_e(b) = 3^{−(τ M^e)_b} = 3^{−|τσ^e(b)|_1} .
```

`z_e → 0` in `ℤ₂`, always: the driving variable behaves. The `y`-coordinates do
not. **`3` is a 2-adic unit, so `|y_e(b)|_2 = 1` for every `e` and every `b`.**

Every transcendence statement in Mahler's method — Mahler, Loxton–van der
Poorten, Nishioka, Adamczewski–Faverjon, and the recent `p`-adic work — requires
the evaluation point to lie **strictly inside** the unit disc of the relevant
absolute value. Our point lies exactly on the excluded boundary in the
`y`-directions, and this is not an artifact of the parametrisation: the
`y`-coordinates carry the base-3 weight, and base 3 is a unit in the base-2
metric. **This is the precise sense in which the mixed bases 2 and 3 are the
obstruction — an analytic one at the point, not an algebraic one at the
equation.**

What remains is the induced **one-variable tower**. Specialising `y` at level
`e` gives `f_b^{(e)}(z) := f_b(z, y_e)`, and Theorem 1 becomes

```
f^{(e)}(z) = Q^{(e)}(z) · f^{(e+1)}(z^k) ,        e = 0, 1, 2, … .
```

This is a genuine Mahler equation only if the tower is eventually constant, and
it is a *convergent deformation* of one only if `Q^{(e)}` converges. Both are
governed by a single condition:

> **`y_e → 1` if and only if `τ M^e → 0` in `ℤ₂^d`.**

When that holds, `Q^{(e)} → Q^{(∞)}` and `f^{(e)} → f^{(∞)}` coefficientwise
2-adically, and `f^{(∞)}` is exactly the classical Mahler system of the
automatic sequence `u` — the object the literature can handle. When it fails,
the coefficient matrices do not converge and there is no single Mahler
equation, even asymptotically.

**Dichotomy.** Over `ℤ₂`, Fitting gives `ℤ₂^d = N ⊕ U` with `M` topologically
nilpotent on `N` and invertible on `U`. Since `M|_U` preserves valuation,
`v_2(τ M^e)` is either **eventually constant** (nonzero `U`-component) or tends
to **infinity** (`τ ∈ N`). There is no third behaviour. So the tower either
converges or is pinned; it cannot drift.

---

## 7. The ten remaining supercritical survivors

The survivors are the ten ternary-coded automata left open by
[`2026-07-24-supercritical-automatic-closure`](../2026-07-24-supercritical-automatic-closure/) §8.

Three exact decision procedures are used. **Every answer any of them returns is
a proof.**

- **C1 (nilpotent).** If `M̄^d = 0` over `F₂` then `M^d = 2B`, so
  `M^{dj} = 2^j B_j → 0` and `τ M^e → 0` for *every* `τ`. Sufficient.
- **C2 (descent).** `τ M^e mod 2` lives in `F₂^d`, of size `2^d`, so its orbit
  is eventually periodic with preperiod plus period at most `2^d`. If zero is
  not reached within `2^d + d` steps it is never reached, so `v_2(τ M^e) = 0`
  for all `e` and the tower is pinned. Otherwise `τ M^{e_0} = 2v'` and the
  question reduces exactly to `v'`; recurse.
- **C3 (recurrence).** The descent is deterministic, so a repeated state proves
  it never halts, which proves `v_2 → ∞`.

| σ | seed | coding | ρ | verdict | decided by |
|---|---:|---|---|---|---|
| `01,02,10` | 0 | 110 | 5/6 | **STALLED** | C2, round 0 |
| `01,02,20` | 0 | 110 | 3/4 | ATTRACTED | C1 |
| `01,02,20` | 0 | 101 | 3/4 | ATTRACTED | C1 |
| `01,02,20` | 2 | 110 | 3/4 | ATTRACTED | C1 |
| `01,02,20` | 2 | 101 | 3/4 | ATTRACTED | C1 |
| `01,12,00` | 0 | 110 | 4/5 | **STALLED** | C2, round 0 |
| `01,12,00` | 1 | 110 | 4/5 | **STALLED** | C2, round 0 |
| `01,20,00` | 0 | 110 | 6/7 | **STALLED** | C2, round 0 |
| `01,20,10` | 0 | 110 | 5/6 | **STALLED** | C2, round 0 |
| `01,20,11` | 0 | 110 | 4/5 | **STALLED** | C2, round 0 |

**ATTRACTED 4 / STALLED 6.** The six stalled words have `v_2(τ M^e) = 0` for
every `e`: the tower parameter never moves off the unit sphere at all. The four
attracted words have `v_2` growing linearly (`0, 0, 1, 2, 3, …`), so
`y_e → 1` at rate `2^{−(e−2)}`.

Each verdict is cross-checked in the verifier against an independently computed
exact valuation profile, which never consults C1, C2 or C3.

**What the split means.** For the four attracted survivors, the object is a
convergent deformation of the classical automatic Mahler system, so a `p`-adic
Mahler theorem — if one existed covering the boundary point — would be pointed
at the right object. For the six stalled ones, there is no limiting Mahler
system to point it at. **The stalled six are the harder half, and they were not
previously distinguished from the other four by any instrument in this
repository.**

---

## 8. The two-variable collapse, and why it never happens here

The `(d+1)`-variable system of Theorem 1 collapses to **two** variables exactly
when the weight `w(a) = |τσ(a)|_1` is an affine function of `τ(a)`, i.e. when

> **(AWC)** `|τσ(a)|_1` depends only on `τ(a)`.

If `w(a) = λτ(a) + μ` then `S_m = λ s_m + μ m`, so `z^{km} y^{S_m}` equals
`(z^k y^μ)^m (y^λ)^{s_m}` and the system closes under
`(z,y) ↦ (z^k y^μ, y^λ)` in two variables.

- On a **two-letter** alphabet with a nonconstant coding, AWC holds
  automatically: each `τ`-class is a singleton, so the condition is vacuous.
  Measured: **24/24** at `d = 2`.
- **None of the ten survivors satisfies AWC** — 0/10. They are ternary-coded,
  and in each case the two letters sharing a `τ`-value carry different weights.

So the survivors require the full `(d+1)`-variable form. The convenient
two-variable case is exactly the case that was already closed.

---

## 9. Class census

All 2-uniform morphisms on `d` letters with at least one prolongable seed, all
nonconstant codings, deduplicated by `(σ, τ)`:

| `d` | words | attracted | stalled | undecided | `M̄` nilpotent | AWC |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 24 | 12 | 12 | 0 | 12 | 24 |
| 3 | 3,078 | 1,122 | 1,956 | 0 | 798 | 1,278 |
| 4 | 627,200 | 166,280 | 459,480 | 1,440 | 89,600 | 124,736 |

`undecided` means the descent survived 64 rounds without a repeat. By the
dichotomy of §6, such a word is either attracted or pinned at valuation `≥ 64`;
the procedure has not separated the two. Undecided words are reported, never
counted as either verdict. At `d = 4` they are 0.23% of the class.

Two readings, both worth stating:

- **The stalled fraction grows with alphabet size** — 50%, 64%, 73%. The
  obstruction gets *more* common as the automaton grows, in the same direction
  as every other saturation recorded in `TARGETS.md` §3.
- `M̄` nilpotent is strictly sufficient, not necessary: 798 versus 1,122 at
  `d = 3`. The gap is real and is why C2 and C3 are needed.

---

## 10. Prior art

Searched 2026-07-25, before this memo was written, per `meta/AGENT_CONDUCT.md`
instrument 2.

- **Nothing found connecting `Φ` to Mahler functions or to a functional
  equation of any kind.** Searched the Mahler-method literature
  (Nishioka's *Mahler Functions and Transcendence*; Adamczewski's survey and
  *Mahler's method* selecta; Adamczewski–Faverjon), the 3x+1 conjugacy
  literature (Bernstein–Lagarias, Monks–Yazinski, López–Stoll 2009 and 2021),
  and the `p`-adic Mahler work.
- **The unit-disc hypothesis is uniform across the literature.** Every
  statement found — real or `p`-adic — restricts to nonzero algebraic points
  strictly inside the unit disc. This is independent confirmation of §6 rather
  than a construction of this packet.
- **`TARGETS.md` bounded check 2 is not closed by anything found.** The nearest
  hits are
  [arXiv:2503.16330](https://arxiv.org/abs/2503.16330) (a `p`-adic dichotomy —
  but for `p`-adic *continued fractions*, a different object) and
  [arXiv:2512.14077](https://arxiv.org/abs/2512.14077) (Mahler's method with
  unbounded coefficients governed by `ν_p(n)`, at points inside the unit disc).
  Neither covers a boundary point.

**Status: provisional.** A negative search result is not a priority claim.
Only abstracts and introductions were read; no review database was consulted.

---

## 11. What this does not do

- It does **not** prove transcendence or irrationality of `Φ(q)` for any word.
  Theorem 1 supplies a functional equation; it supplies no transcendence
  machine, and §6 is the statement that the available machines do not apply.
- It does **not** close any of the ten survivors. It splits them 4/6 by a
  property none of them was known to have, and closes none.
- For the four attracted survivors it does **not** follow that `Φ(q) ∉ ℤ_{>0}`.
  A convergent deformation of a Mahler system is not a Mahler system, and the
  value in question is the `e = 0` member of the tower, not the limit.
- It does **not** touch the amplification branch, the critical density
  `liminf s_L/L = log₃2`, or Witness 2.
- It says nothing about non-automatic words. Theorem 1 needs `k`-uniformity.

---

## 12. Adversarial self-audit

**The quantifier doing the work.** In the claim it is *for every letter-coding
of a fixed point of a `k`-uniform morphism*. That quantifier is **proved**
(Theorem 1, by the `n = km + r` bijection), not assumed, and it is verified on
240 random instances. In §7 the quantifier is *for every `e`*, over
`τ M^e mod 2`; it is **proved** by the `F₂` pigeonhole bound `2^d + d`, which is
finite — this is why the six stalled verdicts are proofs and not
extrapolations from an 80-step window.

**Could the conclusion fail on some input?** Yes, and that is checked. The
functional-equation test fails when the `y ↦ y^M` substitution is removed
(RED test present). The `Φ` bridge fails when one bit of `q` is flipped.
The survivor split is asserted at exactly 4 and 6, so any drift breaks a test.

**Circularity.** Theorem 1 is an identity of formal series; it cannot imply
Collatz and does not restate its hypothesis. §6 is a negative statement about
applicability of existing theorems and carries no Collatz content.

**Positivity and integrality.** Untouched. Nothing here bears on
`Φ(q) ∈ ℤ_{>0}`; that wall is exactly where it was.

**Density read as emptiness.** The census percentages in §9 are ratios over an
enumerated finite class, not densities, and no conclusion is drawn from them
beyond the direction of the trend.

**Floating point.** None. Every path is `ℤ/2^N` or `F₂` integer arithmetic.
The rate `2^{−(e−2)}` in §7 is read off an exact integer valuation profile.

**Dominated results.** §10. No bound is claimed.

**The honest weak point.** §6 asserts that the unit-disc hypothesis is
essential to Mahler's method rather than a convenience of the proofs found. That
is a reading of the literature, not a theorem, and it is the load-bearing
non-computational step in this packet. If a Mahler-type theorem tolerating
boundary points in the non-driving variables exists, the four attracted
survivors become live targets immediately and this packet's framing is wrong.

---

## 13. Reproduce

```bash
python3 contribution/packets/2026-07-25-mahler-tower/verify_mahler_tower.py
```

Runtime about 40 seconds, dominated by the `d = 4` census. Output recorded in
`verify_mahler_tower.out`, certificate in `mahler_tower_certificate.json`
(replayable from the inputs: the survivor table is the only stored data, and
every verdict is recomputed).

```bash
python3 contribution/packets/2026-07-25-mahler-tower/test_verify_mahler_tower.py
```

16 tests, including four RED mutants.

**Lean.** Not attempted. `formal/` is plain Lean 4 core with no mathlib, and
Theorem 1 needs formal power series over a Laurent polynomial ring while §6
needs `ℤ₂`. Both are out of scope there, and scoping them out is deliberate
rather than an omission.
