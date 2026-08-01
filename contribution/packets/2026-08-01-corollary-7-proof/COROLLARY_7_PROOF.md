# Corollary 7 proved: ones-capped factors force a larger complexity floor

**Date.** 2026-08-01.
**Branch served.** Rigidity (factor-complexity instrument).
**Atomic claim.** One number: if every length-`ℓ` factor of an aperiodic parity
word `q` has at most `βℓ + C` ones with `β > log₃2`, and `Φ(q) ∈ ℚ_odd`, then

```
limsup_k p_q(k)/k  ≥  1/g ,     g = β log₂ 3 − 1 > 0.
```

At `β = 1` this recovers Corollary 4 with `1/g = 1/log₂(3/2) = κ`.
**Status.** Proved. Closes the proof gap flagged 2026-07-25 in the landmark
memo and in `REFEREE_NOTE.md`.

This does **not** prove or disprove the Collatz conjecture.

---

## 0. Kill criteria (written before the build)

| # | Criterion | Outcome |
|---|---|---|
| 1 | If the ones-cap does not improve the homogeneous growth rate past `(3/2)^N`, the refinement is vacuous; stop. | **Did not fire.** Rate becomes `(3^β/2)^N = 2^{gN}` with `g = β log₂3 − 1`, strictly smaller exponent than `log₂(3/2)` whenever `β < 1`. |
| 2 | If the inhomogeneous sum is not absorbed into a polynomial times the same exponential, the rate is lost; stop. | **Did not fire.** At most `N` summands, each `O((3^β/2)^{N})`, total `O(N · 2^{gN})`. |
| 3 | If `β ≤ α = log₃2`, then `g ≤ 0` and the argument cannot produce a positive linear complexity floor; report and stop. | **Boundary correct.** The hypothesis requires `β > α` so that `g > 0`. At critical density the ones-cap method is vacuous — consistent with every frequency tool failing at `liminf = α`. |
| 4 | If an independent exact reimplementation of the segment growth bound disagrees with the recursive orbit on any tested word, the algebra is wrong; stop. | **Did not fire.** See `verify_corollary_7.py` (exact integers only). |

---

## 1. Statement

Let `T` be the Terras map on `ℤ₂`, and let `Φ` be the Bernstein–Lagarias
conjugacy (`PARTIAL_THEOREMS.md` Theorem 2). Write
`ℚ_odd := ℚ ∩ ℤ₂` and `α := log₃ 2`. Factor complexity is
`p_q(k) = #{distinct length-k factors of q}`.

> **Corollary 7.** Let `q ∈ {0,1}^ℕ` be not eventually periodic, and suppose
> `Φ(q) ∈ ℚ_odd`. Suppose there exist real constants `β > α` and `C ≥ 0` such
> that every finite factor of `q` of length `ℓ` contains at most `βℓ + C` ones.
> Put
> ```
> g = β log₂ 3 − 1 > 0.
> ```
> Then
> ```
> limsup_{k→∞} p_q(k)/k  ≥  1/g.
> ```

**Specialisation.** `β = 1` is always allowed (every factor has ≤ `ℓ` ones, take
`C = 0`). Then `g = log₂3 − 1 = log₂(3/2)` and `1/g = κ`, recovering
Corollary 4.

---

## 2. Setup (same as Corollary 4)

Write `Φ(q) = a/d` with `a ∈ ℤ` and `d ∈ ℤ_{>0}` odd. Put `x_j = T^j(a/d)` and
`y_j = d · x_j`. Then each `y_j ∈ ℤ`, `y_j ≡ q_j (mod 2)`, and

```
y_{j+1} = ( 3^{q_j} y_j + d · q_j ) / 2 ,     y_0 = a.          (2.1)
```

**Lemma 1 (equal factors force a congruence).** *If the length-`k` factors of
`q` beginning at `i` and `j` are equal, then `y_i ≡ y_j (mod 2^k)`.*

Proof: identical to Corollary 4 / `REFEREE_NOTE.md` §2. Fixed word `w` of
length `k` with `s` ones composes to `2^k y_{i+k} = 3^s y_i + d · c(w)`; same at
`j`; subtract; `3^s` odd ⇒ `2^k | (y_i − y_j)`. ∎

**Lemma 2 (height–complexity collision).** *Let `H_N = max_{0 ≤ j ≤ N} |y_j|`.
If `q` is not eventually periodic and `2^k > 2 H_N`, then `p_q(k) ≥ N+1`.*

Proof: identical to Corollary 4. The `N+1` factors of length `k` starting at
`0,…,N` are pairwise distinct, else Lemma 1 and `|y_i − y_j| ≤ 2 H_N < 2^k`
force `y_i = y_j` and eventual periodicity. ∎

---

## 3. Segment unrolling

Fix a starting index `i ≥ 0` and a length `N ≥ 1`. Write the parity segment
`w = q_i … q_{i+N−1}`, let `s = #{ones in w}`, and for `0 ≤ r ≤ N` write
`s(r)` for the number of ones in the first `r` symbols of `w` (so `s(0) = 0`,
`s(N) = s`).

Unrolling (2.1) along `w` gives the exact identity

```
2^N y_{i+N} = 3^s y_i + d · Σ_{t=0}^{N−1} q_{i+t} · 3^{s − s(t+1)} · 2^t .     (3.1)
```

(Proof by induction on `N`: one step of (2.1) is the `N = 1` case; the
inductive step multiplies by `3^{q}` and adds the new inhomogeneous term.)

Hence

```
|y_{i+N}| ≤ 3^s 2^{−N} |y_i|
          + d · Σ_{t : q_{i+t}=1} 3^{s − s(t+1)} 2^{t−N} .                    (3.2)
```

---

## 4. Ones-cap ⇒ exponential rate `2^{gN}`

By hypothesis, every factor of length `ℓ` has ≤ `βℓ + C` ones. Applied to `w`
itself:

```
s ≤ β N + C.                                                                    (4.1)
```

Applied to the suffix of `w` of length `N − t − 1` (the symbols strictly after
position `t` in the segment), when that length is positive:

```
s − s(t+1) ≤ β(N − t − 1) + C.                                                  (4.2)
```

When `N − t − 1 = 0` the left side is `0` and the right side is `C ≥ 0`, so
(4.2) still holds.

**Homogeneous term.** From (4.1),

```
3^s 2^{−N} ≤ 3^{βN + C} 2^{−N} = 3^C (3^β / 2)^N = 3^C · 2^{g N},
```

where `g = β log₂ 3 − 1`. The hypothesis `β > α = log₃ 2` is exactly
`3^β > 2`, i.e. `g > 0`.

**Inhomogeneous terms.** For each `t` with `q_{i+t} = 1`,

```
3^{s − s(t+1)} 2^{t−N}
  ≤ 3^{β(N−t−1) + C} 2^{t−N}
  = 3^C · 3^{β(N−t−1)} · 2^{−(N−t)}
  = 3^C · 2^{−1} · (3^β / 2)^{N−t−1} ,
```

using `2^{−(N−t)} = 2^{−1} · 2^{−(N−t−1)}`. Since `3^β/2 > 1`,

```
(3^β / 2)^{N−t−1} ≤ (3^β / 2)^{N−1} ,
```

and there are at most `N` ones in the segment, so the sum in (3.2) is

```
≤ d · N · 3^C · (1/2) · (3^β / 2)^{N−1}
 = d · 3^C · (N/2) · 2^{g(N−1)} .
```

**Combined.** From (3.2), for every `i` and every `N ≥ 1`,

```
|y_{i+N}| ≤ 3^C · 2^{g N} |y_i|
          + d · 3^C · (N/2) · 2^{g(N−1)} .                                      (4.3)
```

Starting at `i = 0` with `y_0 = a`, and writing `H_N = max_{0≤j≤N} |y_j|`, a
trivial induction on (4.3) yields a constant `K = K(a,d,β,C)` (independent of
`N`) such that for all `N ≥ 1`,

```
H_N  ≤  K · (N + 1) · 2^{g N} .                                                 (4.4)
```

(Explicitly: the `N = 0` height is `|a|`; for `j ≤ N` write `j` as a single
segment from `0`, apply (4.3) with `i = 0`, and absorb `2^{−g}` into `K`.)

---

## 5. Proof of Corollary 7

Choose

```
k_N = ⌈ g N + log₂( 2 K (N+1) ) ⌉ + 1 .
```

Then `2^{k_N} > 2 K (N+1) 2^{g N} ≥ 2 H_N` by (4.4). Lemma 2 gives
`p_q(k_N) ≥ N + 1`. Since `k_N → ∞` and

```
k_N / N  →  g ,
```

we obtain

```
limsup_k p_q(k)/k
  ≥ limsup_N (N+1)/k_N
  = 1/g .
```

∎

---

## 6. What this does and does not do

**Does.**

- Supplies the missing proof that the supercritical-automatic-closure packet
  used for **114 of 116** exact kills (those routed through Corollary 7 rather
  than Corollary 4). Those kills are now on a fully proved inequality, not an
  unproved citation.
- Makes the density-refined complexity floor a theorem. Monotonicity:
  as `β ↓ α^+`, `g ↓ 0^+` and `1/g → +∞`; as `β ↑ 1`, `1/g ↓ κ`. A
  *tighter* ones-cap (smaller `β`) forces a *larger* complexity floor.
  That is the pressure refinement.
- Recovers Corollary 4 at `β = 1` with no extra hypothesis.

**Does not.**

- Does **not** close the critical-density gap `liminf s_L/L = α`. At `β = α`
  one has `g = 0` and the exponential becomes a constant; the argument produces
  no positive linear complexity floor. This is the same structural wall every
  frequency instrument hits.
- Does **not** consume high complexity. It remains a *lower* bound on
  `limsup p_q(k)/k`. Words whose complexity already exceeds `1/g` are
  untouched — including the former ternary-coded survivors, which the
  2026-08-01 automatic-density corollary closed by a different route.
- Does **not** imply Collatz. The residual class is still: aperiodic
  non-automatic `q` with `Φ(q) ∈ ℤ_{>0}`, `liminf s_L/L = α`, and
  `limsup p_q(k)/k ≥ κ`.

---

## 7. Prior art

Searched 2026-08-01 against the same shelf as `PRIORITY.md` (López–Stoll 2009
and 2021, Bernstein–Lagarias 1996, Monks–Yazinski, Lagarias overview and both
annotated bibliographies) plus Allouche–Shallit Ch. 8–10. No source found that
states this density-refined complexity lower bound for rational Terras states.
The mechanism is the same pigeonhole-plus-unit as Corollary 4, with the
ones-cap inserted into the unrolled Green formula (3.1). **Provisional
novelty** — a negative search is not a priority claim.

---

## 8. Acceptance

| Check | Path |
|---|---|
| Exact unrolling identity (3.1) vs recursive (2.1) | `verify_corollary_7.py` §A |
| Ones-cap growth bound (4.3) on enforced-cap words | `verify_corollary_7.py` §B |
| Rate recovery: `β=1` ⇒ `1/g = κ` by integer witness | `verify_corollary_7.py` §C |
| Independent reimplementation of (3.1) | `verify_corollary_7.py` §D (no shared unroller) |
| Boundary: `β ≤ α` rejected as `g ≤ 0` | `verify_corollary_7.py` §E |

No float on any acceptance path. float64 appears only as a non-load-bearing
display of `κ` and `1/g`.

**Correction (2026-08-01, independent audit).** The first version of
`bound_4_3` dropped a factor 2 when clearing the inhomogeneous term to the
common denominator `2^{N+1}`; it tested `|y| ≤ T1 + T2/2`, a bound *stronger*
than (4.3). The direction was benign — a stricter test passing still
validates (4.3) on those instances — and an adversarial hunt (~38,000
full-cap instances, including cap-saturating all-ones words; max ratio to the
true bound 0.884) never made the stricter bound fail. Fixed at source; the
coded formula now equals (4.3) exactly. The proof itself was not affected.
The audit also independently re-checked (3.1) on 4,000 adversarial words and
Lemma 1 on 465,868 equal-factor pairs, with zero failures.

Reproduce:

```bash
python3 contribution/packets/2026-08-01-corollary-7-proof/verify_corollary_7.py
python3 -m pytest contribution/packets/2026-08-01-corollary-7-proof/test_verify_corollary_7.py -q
```
