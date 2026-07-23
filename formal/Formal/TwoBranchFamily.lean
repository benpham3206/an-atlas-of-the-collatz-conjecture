/-
Collatz atlas — formal certificates.

# The `a = 1` two-branch Collatz-like family is non-universal

*Reference:* Collatz atlas, `contribution/proofs/PARTIAL_THEOREMS.md`,
Theorem 4 (internal exact-arithmetic-verified proof; solved variant of the
Collatz dynamics in the `a = 1` case of the two-branch family
`n ↦ n / 2`, `n ↦ (a·n + b) / 2`).

For a fixed positive shift `b`, every positive orbit of `S_b` enters the
finite invariant set `{1, …, b}` and is eventually periodic; hence `S_b`
cannot step-faithfully simulate an infinite machine run with pairwise
distinct configurations.  `a = 3` (the Collatz case) is the first multiplier
outside this elementary descent argument.

## Port provenance

Ported from `collatz-lean-assessment/TwoBranchFamily.lean` (the draft
statement file for a future `google-deepmind/formal-conjectures`
contribution) into this standalone, mathlib-free Lean 4 core project.
The mathematical content of each statement is identical; the following
mechanical substitutions were forced by the absence of mathlib from core
Lean 4 v4.31.0:

| formal-conjectures draft (mathlib)      | here (Lean 4 core)                    |
|-----------------------------------------|---------------------------------------|
| `if Even n then … else …`               | `if n % 2 = 0 then … else …`          |
| `S b^[k] n` (`Function.iterate`)        | `orbit b n k` (primitive recursion)   |
| `x ∈ Finset.Icc 1 b`                    | `1 ≤ x ∧ x ≤ b` (definitional unfold) |

Each substitution is a definitional equivalence in mathlib terms
(`Nat.even_iff`, `Function.iterate`, `Finset.mem_Icc`), so the statements
below are inter-translatable with the draft ones without change of meaning.
Quantifiers and positivity side conditions are unchanged.

The `@[category research solved, AMS 11 37]` / `@[category API, AMS 11 37]`
attributes on the draft theorems are defined in `FormalConjecturesUtil`
(mathlib-based) and are recorded here as comments; they must be restored
verbatim if this file is contributed to formal-conjectures.

No `sorry`, no floats: every step is exact `Nat` arithmetic checked by the
Lean kernel (`omega` and `split` only produce kernel-checked proof terms).
-/

import Formal.Pigeonhole

namespace TwoBranchFamily

open CollatzAtlas (exists_eq_of_forall_lt)

/-! ## The map and its one-step properties -/

/-- The two-branch map with shift `b`:
`S_b(n) = n / 2` if `n` is even, and `(n + b) / 2` if `n` is odd.

(Parity is tested as `n % 2 = 0`; in mathlib terms this is `Even n` via
`Nat.even_iff`.) -/
def S (b n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else (n + b) / 2

/-- **Descent above the band.**  For `n > b` the map strictly decreases:
the even branch gives `n / 2 < n`, and the odd branch gives
`(n + b) / 2 < n` because `b < n`. -/
theorem S_lt_of_lt {b n : Nat} (h : b < n) : S b n < n := by
  unfold S
  split <;> omega

/-- **Positivity is preserved.**  For `b > 0` and `n > 0` the next state is
still positive: an even positive `n` is at least `2`, so `n / 2 ≥ 1`, and
`(n + b) / 2 ≥ (0 + 1) / 2`, in fact `≥ 1` since `n + b ≥ 2`. -/
theorem S_pos {b n : Nat} (hb : 0 < b) (hn : 0 < n) : 0 < S b n := by
  unfold S
  split <;> omega

-- In formal-conjectures this carries `@[category API, AMS 11 37]`.
/-- **The band is invariant** (draft: `twoBranch_invariant`).
For `n ∈ {1, …, b}`, `S_b(n)` stays in `{1, …, b}`: the even branch gives
`n / 2 ≤ n ≤ b`, and the odd branch gives `(n + b) / 2 ≤ (b + b) / 2 = b`;
positivity is preserved by `S_pos`.

(`1 ≤ x ∧ x ≤ b` is `x ∈ Finset.Icc 1 b` unfolded via `Finset.mem_Icc`.) -/
theorem twoBranch_invariant {b : Nat} (hb : 0 < b) {n : Nat}
    (hn : 1 ≤ n ∧ n ≤ b) : 1 ≤ S b n ∧ S b n ≤ b := by
  obtain ⟨h1, h2⟩ := hn
  exact ⟨S_pos hb h1, by unfold S; split <;> omega⟩

/-! ## Iteration -/

/-- The `k`-fold iterate of `S_b` applied to `n`:
`orbit b n k = S_b^k(n)` (`Function.iterate` `S b^[k] n` in mathlib
notation), defined by primitive recursion so that both unfolding steps hold
definitionally. -/
def orbit (b n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => S b (orbit b n k)

/-- Iterates compose by addition of counts:
`S_b^(h+k)(n) = S_b^k(S_b^h(n))`. -/
theorem orbit_add (b n h k : Nat) :
    orbit b n (h + k) = orbit b (orbit b n h) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    show S b (orbit b n (h + k)) = S b (orbit b (orbit b n h) k)
    rw [ih]

/-- One step can be peeled off the front of an iterate:
`S_b^(k+1)(n) = S_b^k(S_b(n))`. -/
theorem orbit_succ (b n k : Nat) : orbit b n (k + 1) = orbit b (S b n) k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    show S b (orbit b n (k + 1)) = S b (orbit b (S b n) k)
    rw [ih]

/-- Once an orbit is inside the band `{1, …, b}` it never leaves:
invariance (`twoBranch_invariant`) lifted through iteration. -/
theorem orbit_in_band {b n : Nat} (hb : 0 < b) (hn : 1 ≤ n ∧ n ≤ b) (k : Nat) :
    1 ≤ orbit b n k ∧ orbit b n k ≤ b := by
  induction k with
  | zero => exact hn
  | succ k ih =>
    show 1 ≤ S b (orbit b n k) ∧ S b (orbit b n k) ≤ b
    exact twoBranch_invariant hb ih

/-! ## The three theorems of the draft, fully proved -/

-- In formal-conjectures this carries `@[category research solved, AMS 11 37]`.
/-- **Every positive orbit enters the finite band** (draft:
`twoBranch_enters_finite_set`).  By strong induction on `n`: if `n ≤ b`
the orbit is already there; otherwise `S_b(n) < n` (`S_lt_of_lt`) is still
positive (`S_pos`), and one more step prepended to the inductively obtained
hitting time of `S_b(n)` works. -/
theorem twoBranch_enters_finite_set {b : Nat} (hb : 0 < b) {n : Nat}
    (hn : 0 < n) : ∃ m, 1 ≤ orbit b n m ∧ orbit b n m ≤ b := by
  revert hn
  refine
    Nat.strongRecOn
      (motive := fun n => 0 < n → ∃ m, 1 ≤ orbit b n m ∧ orbit b n m ≤ b) n ?_
  intro n ih hn
  by_cases hnb : n ≤ b
  · exact ⟨0, hn, hnb⟩
  · have hbn : b < n := by omega
    have hlt : S b n < n := S_lt_of_lt hbn
    have hpos : 0 < S b n := S_pos hb hn
    obtain ⟨m, hm1, hm2⟩ := ih (S b n) hlt hpos
    exact ⟨m + 1, by rw [orbit_succ]; exact ⟨hm1, hm2⟩⟩

-- In formal-conjectures this carries `@[category research solved, AMS 11 37]`.
/-- **Every positive orbit is eventually periodic** (draft:
`twoBranch_eventually_periodic`).  After the hitting time `m` from
`twoBranch_enters_finite_set`, the shifted orbit `k ↦ S_b^(m+k)(n)` takes
`b + 1` values `k = 0, …, b` inside the `b`-element band, so the bespoke
pigeonhole `exists_eq_of_forall_lt` (applied to `k ↦ S_b^(m+k)(n) - 1`)
produces `i < j` with equal states; `h = m + i` and `p = j - i` close the
statement. -/
theorem twoBranch_eventually_periodic {b : Nat} (hb : 0 < b) {n : Nat}
    (hn : 0 < n) : ∃ h p, 0 < p ∧ orbit b n (h + p) = orbit b n h := by
  obtain ⟨m, hm1, hm2⟩ := twoBranch_enters_finite_set hb hn
  have hband : ∀ k, 1 ≤ orbit b n (m + k) ∧ orbit b n (m + k) ≤ b := fun k => by
    rw [orbit_add]
    exact orbit_in_band hb ⟨hm1, hm2⟩ k
  obtain ⟨i, j, hij, -, hEq⟩ :=
    exists_eq_of_forall_lt b (fun k => orbit b n (m + k) - 1) (fun k _ => by
      show orbit b n (m + k) - 1 < b
      have hk := hband k
      omega)
  refine ⟨m + i, j - i, by omega, ?_⟩
  have hEq' : orbit b n (m + i) = orbit b n (m + j) := by
    have hi := (hband i).1
    have hj := (hband j).1
    omega
  have hsum : m + i + (j - i) = m + j := by omega
  rw [hsum, hEq']

/-- **Corollary (addition beyond the draft): the whole tail is periodic.**
From time `h` on, every state repeats with period `p`, so the orbit assumes
only finitely many distinct values — the precise sense in which `S_b`
cannot step-faithfully embed an infinite run with pairwise distinct
configurations. -/
theorem twoBranch_periodic_tail {b : Nat} (hb : 0 < b) {n : Nat} (hn : 0 < n) :
    ∃ h p, 0 < p ∧ ∀ k, orbit b n (h + p + k) = orbit b n (h + k) := by
  obtain ⟨h, p, hp, heq⟩ := twoBranch_eventually_periodic hb hn
  refine ⟨h, p, hp, fun k => ?_⟩
  calc orbit b n (h + p + k) = orbit b (orbit b n (h + p)) k :=
        orbit_add b n (h + p) k
    _ = orbit b (orbit b n h) k := by rw [heq]
    _ = orbit b n (h + k) := (orbit_add b n h k).symm

end TwoBranchFamily
