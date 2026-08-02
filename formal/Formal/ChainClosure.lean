/-
Collatz atlas — formal certificates.

# Chain closure for the Syracuse Fourier recursion

*Reference:* Collatz atlas, `contribution/packets/2026-07-22-syracuse-fourier/`,
Theorem 1 (proved Syracuse Fourier recursion): the coefficients evolve by

  `c_{n+1}(ξ) = Σ_{a≥1} 2^{-a} e(−ξ u_a / 3^{n+1}) c_n(ξ u_a mod 3^n)`

with `u_a = 2^{-a} mod 3^{n+1}`.  On the chain frequencies `ξ = 2^k` the
*chain closure identity* holds definitionally:

  `ξ · u_a ≡ 2^{k-a} (mod 3^{n+1})`,

so the recursion restricts to an exact finite dynamical system on the chain.

## Scope notes (mathlib-free setting)

This project is plain Lean 4 core (no mathlib), so there is no `ZMod`, no unit
group and no `ℂ`.  The following mechanical substitutions are forced, each a
definitional specialisation of the mathlib statement:

| mathlib draft                              | here (Lean 4 core)                          |
|--------------------------------------------|---------------------------------------------|
| `u_a = (2^a)⁻¹` in `(ℤ/3^{n+1}ℤ)ˣ`          | `invPow (3^(n+1)) a = ((3^(n+1)+1)/2)^a % …` |
| `2^k · u_a = 2^{k-a}` as units             | `(2^k * invPow q a) % q = 2^(k-a) % q` etc. |
| group hom `ℤ → (ℤ/3^nℤ)ˣ`, `k ↦ 2^k`       | `twoPowZ q k` with `twoPowZ_succ`/`_pred`   |
| complex coefficient functions              | `c : Nat → Int` with `w : Nat → Int` weights |
| `2` primitive root mod `3^n`               | Euler bound proved; primitivity in comments |

The inverse of `2` modulo an odd modulus `q` is the explicit `(q+1)/2`
(`2 * (q+1)/2 = q+1 ≡ 1`), so `invPow q a` is an explicit, computation-friendly
representative of `2^{-a} mod q`.  The analytic phase factor `e(−ξ u_a/3^{n+1})`
is *parameterized* into the branch weight `w a` in `chainStep`; everything
proved here is exact integer data — the index dynamics `k ↦ k − a` and the
residue `2^{k-a} mod 3^{n+1}`.

On the multiplicative order: `two_pow_euler_three_pow` proves the Euler bound
`2^{2·3^n} ≡ 1 (mod 3^{n+1})`, i.e. `ord_{3^{n+1}}(2) ∣ 2·3^n = φ(3^{n+1})`.
Equality (`2` is a primitive root mod `3^m`, so the period of the chain is
exactly `2·3^{n−1}` at level `n`) is classical but is *not* formalized here;
the chain window below uses the loose, proved bound and the dynamics is
well-defined independently of primitivity.

No `sorry`, no floats: every step is exact `Nat`/`Int` arithmetic checked by
the Lean kernel.
-/

namespace ChainClosure

/-! ## Small positivity / parity scaffolding -/

theorem pos_two_pow : ∀ n : Nat, 0 < 2 ^ n
  | 0 => by decide
  | n + 1 => by
      rw [Nat.pow_add_one]
      exact (Nat.mul_pos_iff_of_pos_left (pos_two_pow n)).2 (by decide)

theorem pos_three_pow : ∀ n : Nat, 0 < 3 ^ n
  | 0 => by decide
  | n + 1 => by
      rw [Nat.pow_add_one]
      exact (Nat.mul_pos_iff_of_pos_left (pos_three_pow n)).2 (by decide)

/-- Powers of 3 are odd. -/
theorem three_pow_mod_two : ∀ n : Nat, 3 ^ n % 2 = 1 := by
  intro n; induction n with
  | zero => decide
  | succ n ih => rw [Nat.pow_add_one, Nat.mul_mod, ih]

theorem one_lt_three_pow (m : Nat) (h : 1 ≤ m) : 1 < 3 ^ m := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le h
  rw [Nat.pow_add, Nat.pow_one]
  have hk := pos_three_pow k
  omega

/-- `2` is coprime to every power of `3`: the chain `{2^k}` is a well-defined
subset of the multiplicative units modulo `3^n`. -/
theorem gcd_two_three_pow (n : Nat) : Nat.gcd 2 (3 ^ n) = 1 := by
  rw [Nat.gcd_rec, three_pow_mod_two, Nat.gcd_one_left]

/-! ## Modular congruence helpers -/

theorem mul_mod_left (x y q : Nat) : (x % q * y) % q = (x * y) % q := by
  rw [Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod]

theorem mul_mod_right (x y q : Nat) : (x * (y % q)) % q = (x * y) % q := by
  rw [Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod]

theorem mul_mod_congr {a b c d q : Nat} (h1 : a % q = c % q) (h2 : b % q = d % q) :
    (a * b) % q = (c * d) % q := by
  rw [Nat.mul_mod, Nat.mul_mod c d q, h1, h2]

/-! ## The explicit inverse of `2^a` modulo an odd modulus -/

/-- The explicit inverse of `2` modulo an odd `q`: `2 * (q+1)/2 = q + 1 ≡ 1`. -/
def inv2 (q : Nat) : Nat := (q + 1) / 2

theorem two_mul_inv2 (q : Nat) (hq : q % 2 = 1) : 2 * inv2 q = q + 1 := by
  have h := Nat.mod_add_div q 2
  unfold inv2
  omega

theorem two_mul_inv2_mod (h1 : 1 < q) (hq : q % 2 = 1) : (2 * inv2 q) % q = 1 := by
  rw [two_mul_inv2 q hq, Nat.add_mod, Nat.mod_self, Nat.zero_add, Nat.mod_mod,
    Nat.mod_eq_of_lt h1]

/-- Multiplication by `2 * inv2 q ≡ 1` is invisible modulo `q`. -/
theorem mul_two_inv2 (h1 : 1 < q) (hq : q % 2 = 1) (x : Nat) :
    (x * (2 * inv2 q)) % q = x % q := by
  rw [Nat.mul_mod, two_mul_inv2_mod h1 hq, Nat.mul_one, Nat.mod_mod]

/-- `2` is a unit modulo `3^(n+1)`, with an explicit bounded inverse. -/
theorem two_is_unit_three_pow (n : Nat) :
    ∃ u, u < 3 ^ (n + 1) ∧ (2 * u) % 3 ^ (n + 1) = 1 := by
  refine ⟨inv2 (3 ^ (n + 1)), ?_, ?_⟩
  · show (3 ^ (n + 1) + 1) / 2 < 3 ^ (n + 1)
    have h := one_lt_three_pow (n + 1) (by omega)
    omega
  · exact two_mul_inv2_mod (one_lt_three_pow _ (by omega)) (three_pow_mod_two _)

/-- `u_a`, the explicit inverse of `2^a` modulo `q` (odd `q`). -/
def invPow (q a : Nat) : Nat := inv2 q ^ a % q

theorem invPow_mod (q a : Nat) : invPow q a % q = invPow q a := Nat.mod_mod _ _

theorem invPow_succ (q a : Nat) : invPow q (a + 1) = (invPow q a * inv2 q) % q := by
  unfold invPow
  rw [Nat.pow_add_one, ← mul_mod_left]

/-- `invPow q a` is a genuine inverse of `2^a` modulo `q`. -/
theorem twoPow_mul_invPow (h1 : 1 < q) (hq : q % 2 = 1) (a : Nat) :
    (2 ^ a * invPow q a) % q = 1 := by
  induction a with
  | zero =>
      rw [show invPow q 0 = 1 % q from rfl, Nat.pow_zero, Nat.one_mul, Nat.mod_mod,
        Nat.mod_eq_of_lt h1]
  | succ a ih =>
      have e1 : (2 ^ (a + 1) * invPow q (a + 1)) % q
          = ((2 ^ a * 2) * (invPow q a * inv2 q)) % q := by
        apply mul_mod_congr
        · rw [Nat.pow_add_one]
        · rw [invPow_succ, Nat.mod_mod]
      rw [e1,
        show (2 ^ a * 2) * (invPow q a * inv2 q) = (2 ^ a * invPow q a) * (2 * inv2 q) from
          by ac_rfl,
        Nat.mul_mod, ih, two_mul_inv2_mod h1 hq, Nat.one_mul, Nat.mod_eq_of_lt h1]

theorem invPow_mul_twoPow (h1 : 1 < q) (hq : q % 2 = 1) (a : Nat) :
    (invPow q a * 2 ^ a) % q = 1 := by
  rw [Nat.mul_comm]
  exact twoPow_mul_invPow h1 hq a

/-! ## The chain closure identity (natural exponents) -/

/-- **Chain closure identity.** For `a ≤ k`, the chain frequency `2^k` mapped
through the branch-`a` multiplier `u_a` lands exactly on the chain frequency
`2^{k-a}`: `2^k · u_a ≡ 2^{k-a} (mod q)`.  (Definitional in the packet's
setting since `u_a = 2^{-a}`.) -/
theorem chain_closure_nat (h1 : 1 < q) (hq : q % 2 = 1) {a k : Nat} (hak : a ≤ k) :
    (2 ^ k * invPow q a) % q = 2 ^ (k - a) % q := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hak
  rw [Nat.add_sub_cancel_left, Nat.pow_add,
    show 2 ^ a * 2 ^ d * invPow q a = 2 ^ d * (2 ^ a * invPow q a) from by ac_rfl,
    Nat.mul_mod, twoPow_mul_invPow h1 hq, Nat.mul_one, Nat.mod_mod]

/-! ## The exponent map `ℤ → units`, `k ↦ 2^k mod q` -/

/-- The chain-frequency map on integer exponents: `2^k mod q` for `k ≥ 0`, and
`(2^{-j}) mod q` for `k = -j < 0` (negative exponents via the explicit inverse).
This is the mathlib-free stand-in for the group homomorphism `ℤ → (ℤ/qℤ)ˣ`. -/
def twoPowZ (q : Nat) (k : Int) : Nat :=
  if 0 ≤ k then 2 ^ k.toNat % q else invPow q k.natAbs

theorem twoPowZ_ofNat (q : Nat) (j : Nat) : twoPowZ q ((j : Int)) = 2 ^ j % q := by
  unfold twoPowZ
  split
  · rfl
  · rename_i h
    exact absurd (Int.natCast_nonneg j) h

theorem twoPowZ_negSucc (q : Nat) (j : Nat) :
    twoPowZ q (Int.negSucc j) = invPow q (j + 1) := by
  unfold twoPowZ
  split
  · rename_i h
    exact ((Int.negSucc_not_nonneg j).1 h).elim
  · rfl

theorem twoPowZ_mod (q : Nat) (k : Int) : twoPowZ q k % q = twoPowZ q k := by
  unfold twoPowZ
  split
  · rw [Nat.mod_mod]
  · rw [invPow_mod]

/-- Homomorphism step (`k ↦ k + 1` corresponds to multiplication by `2`). -/
theorem twoPowZ_succ (h1 : 1 < q) (hq : q % 2 = 1) (k : Int) :
    twoPowZ q (k + 1) = (2 * twoPowZ q k) % q := by
  by_cases hk : 0 ≤ k
  · obtain ⟨j, rfl⟩ : ∃ j : Nat, k = (j : Int) := ⟨k.toNat, (Int.toNat_of_nonneg hk).symm⟩
    rw [show (j : Int) + 1 = ((j + 1 : Nat) : Int) from by omega,
      twoPowZ_ofNat, twoPowZ_ofNat, mul_mod_right, Nat.mul_comm 2 (2 ^ j),
      ← Nat.pow_add_one]
  · obtain ⟨j, rfl⟩ := Int.eq_negSucc_of_lt_zero (Int.lt_of_not_ge hk)
    cases j with
    | zero =>
        rw [show Int.negSucc 0 + 1 = (0 : Int) from by decide]
        show twoPowZ q ((0 : Nat) : Int) = (2 * twoPowZ q (Int.negSucc 0)) % q
        rw [twoPowZ_ofNat, twoPowZ_negSucc, Nat.pow_zero, Nat.mod_eq_of_lt h1,
          show 0 + 1 = (1 : Nat) from rfl,
          show invPow q 1 = inv2 q % q from by unfold invPow; rw [Nat.pow_one],
          mul_mod_right, two_mul_inv2_mod h1 hq]
    | succ j =>
        rw [show Int.negSucc (j + 1) + 1 = Int.negSucc j from by
            rw [Int.negSucc_eq, Int.negSucc_eq, Int.natCast_add, Int.ofNat_one]; omega,
          twoPowZ_negSucc, twoPowZ_negSucc,
          show invPow q (j + 1 + 1) = (invPow q (j + 1) * inv2 q) % q from invPow_succ q (j + 1),
          mul_mod_right,
          show 2 * (invPow q (j + 1) * inv2 q) = invPow q (j + 1) * (2 * inv2 q) from
            by ac_rfl,
          mul_two_inv2 h1 hq, invPow_mod]

/-- Homomorphism step backwards (`k ↦ k − 1` corresponds to multiplication by
`2⁻¹`); this is the single-branch chain index dynamics. -/
theorem twoPowZ_pred (h1 : 1 < q) (hq : q % 2 = 1) (k : Int) :
    twoPowZ q (k - 1) = (twoPowZ q k * inv2 q) % q := by
  by_cases hk : 0 ≤ k
  · obtain ⟨j, rfl⟩ : ∃ j : Nat, k = (j : Int) := ⟨k.toNat, (Int.toNat_of_nonneg hk).symm⟩
    cases j with
    | zero =>
        rw [show ((0 : Nat) : Int) - 1 = Int.negSucc 0 from by decide,
          twoPowZ_negSucc, twoPowZ_ofNat,
          show 0 + 1 = (1 : Nat) from rfl,
          show invPow q 1 = inv2 q % q from by unfold invPow; rw [Nat.pow_one],
          Nat.pow_zero, Nat.mod_eq_of_lt h1, Nat.one_mul]
    | succ j =>
        rw [show ((j + 1 : Nat) : Int) - 1 = (j : Int) from by omega,
          twoPowZ_ofNat, twoPowZ_ofNat, mul_mod_left, Nat.pow_add_one, Nat.mul_assoc,
          mul_two_inv2 h1 hq]
  · obtain ⟨j, rfl⟩ := Int.eq_negSucc_of_lt_zero (Int.lt_of_not_ge hk)
    rw [show Int.negSucc j - 1 = Int.negSucc (j + 1) from by
        rw [Int.negSucc_eq, Int.negSucc_eq, Int.natCast_add, Int.ofNat_one]; omega,
      twoPowZ_negSucc, twoPowZ_negSucc,
      show invPow q (j + 1 + 1) = (invPow q (j + 1) * inv2 q) % q from invPow_succ q (j + 1)]

/-- **General chain closure identity.** For every integer exponent `k` and
branch valuation `a`, `2^k · u_a ≡ 2^{k-a} (mod q)`. -/
theorem twoPowZ_mul_invPow (h1 : 1 < q) (hq : q % 2 = 1) (k : Int) (a : Nat) :
    (twoPowZ q k * invPow q a) % q = twoPowZ q (k - (a : Int)) := by
  induction a with
  | zero =>
      rw [show invPow q 0 = 1 % q from rfl, mul_mod_right, Nat.mul_one, twoPowZ_mod,
        show k - ((0 : Nat) : Int) = k from by simp]
  | succ a ih =>
      rw [invPow_succ, mul_mod_right,
        show twoPowZ q k * (invPow q a * inv2 q) = (twoPowZ q k * invPow q a) * inv2 q from
          by ac_rfl,
        Nat.mul_mod, ih, mul_mod_right, ← twoPowZ_pred h1 hq]
      congr 1
      omega

/-- Forward closure: multiplying a chain frequency by `2^a` stays on the chain. -/
theorem twoPowZ_mul_twoPow (h1 : 1 < q) (hq : q % 2 = 1) (k : Int) (a : Nat) :
    (twoPowZ q k * 2 ^ a) % q = twoPowZ q (k + (a : Int)) := by
  induction a with
  | zero =>
      rw [Nat.pow_zero, Nat.mul_one, twoPowZ_mod,
        show k + ((0 : Nat) : Int) = k from by simp]
  | succ a ih =>
      rw [Nat.pow_add_one, ← Nat.mul_assoc, Nat.mul_mod, ih, mul_mod_right,
        Nat.mul_comm, ← twoPowZ_succ h1 hq]
      congr 1
      omega

/-- `k ↦ 2^k mod q` is a group homomorphism `ℤ → (ℤ/qℤ)ˣ` (for odd `q > 1`),
expressed mathlib-free as its two multiplicative laws. -/
theorem twoPowZ_is_hom (h1 : 1 < q) (hq : q % 2 = 1) (k : Int) (a : Nat) :
    (twoPowZ q k * 2 ^ a) % q = twoPowZ q (k + (a : Int))
    ∧ (twoPowZ q k * invPow q a) % q = twoPowZ q (k - (a : Int)) :=
  ⟨twoPowZ_mul_twoPow h1 hq k a, twoPowZ_mul_invPow h1 hq k a⟩

/-! ## Euler bound: the order of `2` modulo `3^(n+1)` divides `2·3^n` -/

theorem one_add_pow_three (x : Nat) : (1 + x) ^ 3 = 1 + 3 * x + 3 * x ^ 2 + x ^ 3 := by
  simp only [Nat.pow_succ, Nat.pow_zero, Nat.one_mul, Nat.mul_add, Nat.add_mul, Nat.mul_one]
  omega

/-- **Euler bound for the chain period.** `2^{2·3^n} ≡ 1 (mod 3^{n+1})`, i.e.
the multiplicative order of `2` modulo `3^{n+1}` divides `φ(3^{n+1}) = 2·3^n`.
Proved by induction with the cube-lifting step.  (The classical strengthening —
equality, i.e. `2` is a primitive root modulo `3^m` — is not formalized here;
see the file header.) -/
theorem two_pow_euler_three_pow (n : Nat) :
    2 ^ (2 * 3 ^ n) % 3 ^ (n + 1) = 1 % 3 ^ (n + 1) := by
  induction n with
  | zero => decide
  | succ n ih =>
      rw [show n + 1 + 1 = n + 2 from rfl]
      have hm1 : 1 < 3 ^ (n + 1) := one_lt_three_pow _ (by omega)
      rw [Nat.mod_eq_of_lt hm1] at ih
      have e1 : 2 ^ (2 * 3 ^ (n + 1)) = (2 ^ (2 * 3 ^ n)) ^ 3 := by
        have h2 : 2 * 3 ^ (n + 1) = 2 * 3 ^ n * 3 := by
          rw [Nat.pow_add_one]; ac_rfl
        rw [h2, Nat.pow_mul]
      obtain ⟨s, hs⟩ : ∃ s, 2 ^ (2 * 3 ^ n) = 1 + 3 ^ (n + 1) * s := by
        refine ⟨2 ^ (2 * 3 ^ n) / 3 ^ (n + 1), ?_⟩
        have h := Nat.mod_add_div (2 ^ (2 * 3 ^ n)) (3 ^ (n + 1))
        rw [ih] at h
        omega
      have m3 : 3 ^ (n + 2) = 3 * 3 ^ (n + 1) := by rw [Nat.pow_add_one, Nat.mul_comm]
      have T1 : 3 * (3 ^ (n + 1) * s) = 3 ^ (n + 2) * s := by rw [m3]; ac_rfl
      have mm : 3 ^ (n + 1) * 3 ^ (n + 1) = 3 ^ (n + 2) * 3 ^ n := by
        rw [← Nat.pow_add, show (n + 1) + (n + 1) = (n + 2) + n from by omega, Nat.pow_add]
      have T2 : 3 * (3 ^ (n + 1) * s) ^ 2 = 3 ^ (n + 2) * (3 ^ (n + 1) * (s * s)) := by
        rw [Nat.mul_pow, Nat.pow_two, Nat.pow_two, mm, m3, Nat.pow_add_one]
        ac_rfl
      have mmm : 3 ^ (n + 1) * (3 ^ (n + 1) * 3 ^ (n + 1)) = 3 ^ (n + 2) * 3 ^ (2 * n + 1) := by
        rw [show 3 ^ (n + 1) * (3 ^ (n + 1) * 3 ^ (n + 1))
              = (3 ^ (n + 1) * 3 ^ (n + 1)) * 3 ^ (n + 1) from by ac_rfl,
          ← Nat.pow_add, ← Nat.pow_add,
          show (n + 1) + (n + 1) + (n + 1) = (n + 2) + (2 * n + 1) from by omega,
          Nat.pow_add]
      have T3 : (3 ^ (n + 1) * s) ^ 3 = 3 ^ (n + 2) * (3 ^ (2 * n + 1) * (s * (s * s))) := by
        rw [Nat.mul_pow,
          show (3 ^ (n + 1)) ^ 3 = 3 ^ (n + 1) * (3 ^ (n + 1) * 3 ^ (n + 1)) from by
            rw [Nat.pow_add_one, Nat.pow_two]; ac_rfl,
          show s ^ 3 = s * (s * s) from by rw [Nat.pow_add_one, Nat.pow_two]; ac_rfl,
          mmm]
        ac_rfl
      have factor : 1 + 3 ^ (n + 2) * s + 3 ^ (n + 2) * (3 ^ (n + 1) * (s * s))
            + 3 ^ (n + 2) * (3 ^ (2 * n + 1) * (s * (s * s)))
          = 1 + 3 ^ (n + 2) * (s + (3 ^ (n + 1) * (s * s) + 3 ^ (2 * n + 1) * (s * (s * s)))) := by
        rw [Nat.mul_add, Nat.mul_add]; ac_rfl
      rw [e1, hs, one_add_pow_three, T1, T2, T3, factor, Nat.add_mod, Nat.mul_mod_right,
        Nat.add_zero, Nat.mod_mod]

/-! ## The chain subsystem (index dynamics) -/

/-- One Syracuse branch of valuation `a` shifts the chain exponent `k ↦ k − a`. -/
def chainExponentStep (a : Nat) (k : Int) : Int := k - (a : Int)

/-- Length of one exponent window at level `n + 1`.  By `two_pow_euler_three_pow`
the order of `2` mod `3^(n+1)` divides `2·3^n`; the window `2·3^(n+1)` strictly
contains a full period, and the chain dynamics below is well-defined
independently of the (unformalized) primitivity of `2` modulo `3^m`. -/
def ChainWindow (n : Nat) : Nat := 2 * 3 ^ (n + 1)

theorem chainWindow_pos (n : Nat) : 0 < ChainWindow n :=
  (Nat.mul_pos_iff_of_pos_left (by decide : 0 < 2)).2 (pos_three_pow _)

/-- The finite chain state space at level `n + 1`: exponents taken in one window. -/
def ChainState (n : Nat) : Type := Fin (ChainWindow n)

/-- One-step chain update on the finite state space: subtraction of the branch
valuation `a`, modulo the window. -/
def chainIndexStep (n : Nat) (a : Nat) (s : ChainState n) : ChainState n :=
  ⟨(s.val + a * ChainWindow n - a) % ChainWindow n, Nat.mod_lt _ (chainWindow_pos n)⟩

/-- A residue `ξ mod q` lies on the chain when it is `2^k mod q` for some
integer exponent `k`. -/
def ChainResidue (q : Nat) (ξ : Nat) : Prop :=
  ∃ k : Int, ξ % q = twoPowZ q k

/-- Forward support closure at the residue level: if `ξ` is a chain residue,
then so is `ξ · u_a mod q` — the phase factor of the recursion stays exact
integer chain data. -/
theorem chainResidue_mul_invPow (h1 : 1 < q) (hq : q % 2 = 1) {ξ : Nat}
    (hξ : ChainResidue q ξ) (a : Nat) : ChainResidue q ((ξ * invPow q a) % q) := by
  obtain ⟨k, hk⟩ := hξ
  refine ⟨k - (a : Int), ?_⟩
  rw [Nat.mod_mod, Nat.mul_mod, hk, mul_mod_right, twoPowZ_mul_invPow h1 hq]

/-- Backward support closure: if `ξ · u_a mod q` is a chain residue, so is `ξ`
(multiply back by `2^a`). -/
theorem chainResidue_of_mul_invPow (h1 : 1 < q) (hq : q % 2 = 1) {ξ : Nat} (a : Nat)
    (h : ChainResidue q ((ξ * invPow q a) % q)) : ChainResidue q ξ := by
  obtain ⟨k, hk⟩ := h
  refine ⟨k + (a : Int), ?_⟩
  have hk2 : (ξ * invPow q a) % q = twoPowZ q k := by
    rw [← Nat.mod_mod]; exact hk
  have e1 : ξ % q = ((ξ * invPow q a) % q * 2 ^ a) % q := by
    rw [mul_mod_left,
      show ξ * invPow q a * 2 ^ a = ξ * (invPow q a * 2 ^ a) from by ac_rfl,
      Nat.mul_mod, invPow_mul_twoPow h1 hq, Nat.mul_one, Nat.mod_mod]
  rw [e1, hk2, twoPowZ_mul_twoPow h1 hq]

/-- A coefficient function (on residues mod `q`) is chain-supported when it
vanishes off chain residues.  (Scoped to the index/residue level: the analytic
phase factor is carried by the weight function `w`, see `chainStep`.) -/
def ChainSupported (q : Nat) (c : Nat → Int) : Prop :=
  ∀ ξ, c ξ ≠ 0 → ChainResidue q ξ

/-- One step of the chain-restricted Syracuse recursion at the index level:
branches `a = 0, …, A` with integer weights `w a` (the packet's `2^{-a}` times
the parameterized phase factor) applied to the argument `ξ · u_a mod q`. -/
def chainStep (q : Nat) (w : Nat → Int) (A : Nat) (c : Nat → Int) (ξ : Nat) : Int :=
  (List.range (A + 1)).foldl (fun acc a => acc + w a * c ((ξ * invPow q a) % q)) 0

theorem foldl_branch_eq_zero (q : Nat) (w : Nat → Int) (c : Nat → Int) (ξ : Nat)
    (l : List Nat) (h : ∀ a ∈ l, w a * c ((ξ * invPow q a) % q) = 0) :
    (l.foldl (fun acc a => acc + w a * c ((ξ * invPow q a) % q)) 0) = 0 := by
  induction l with
  | nil => rfl
  | cons b t ih =>
      simp only [List.foldl_cons]
      have hb := h b (List.mem_cons.mpr (Or.inl rfl))
      rw [hb, Int.add_zero]
      exact ih (fun a ha => h a (List.mem_cons.mpr (Or.inr ha)))

/-- **Chain subsystem closure.** The one-step update maps chain-supported
coefficient functions to chain-supported coefficient functions: if
`chainStep q w A c ξ ≠ 0` then some branch term is nonzero, so `ξ · u_a` is a
chain residue (by `hc`), hence `ξ` itself is one (by `chainResidue_of_mul_invPow`). -/
theorem chainSupported_chainStep (h1 : 1 < q) (hq : q % 2 = 1) (w : Nat → Int) (A : Nat)
    {c : Nat → Int} (hc : ChainSupported q c) : ChainSupported q (chainStep q w A c) := by
  intro ξ hξ
  apply Classical.byContradiction
  intro hcon
  apply hξ
  unfold chainStep
  apply foldl_branch_eq_zero
  intro a _
  apply Decidable.by_contra
  intro hterm
  have hc_arg : c ((ξ * invPow q a) % q) ≠ 0 := fun hz => hterm (by rw [hz, Int.mul_zero])
  exact hcon (chainResidue_of_mul_invPow h1 hq a (hc _ hc_arg))

/-! ## OPEN TARGET: the `a = 1` dominance (odometer) conjecture

The packet's branch weights are `w_a = 2^{-a}`.  At scale `2^A` these are the
integer masses `W a = 2^{A-a}` for `1 ≤ a ≤ A`.  The **a = 1 dominance
conjecture (odometer target)** asserts that along the chain subsystem the
`a = 1` branch asymptotically controls the recursion: its mass `2^{A-1}`
exceeds the combined tail `Σ_{a≥2} 2^{A-a} = 2^{A-1} − 1`, and — the open
analytic content — the single unit of mass slack survives the interference of
the phase factors `e(−ξ u_a / 3^{n+1})` so that no cancellation can flip the
dominance along any chain orbit.

`IsOdometerDominant` below is the precise mass-level predicate; the mass
identity itself is *proved* (`syracuse_tail_mass`, `syracuse_mass_slack`), and
the phase-resilience statement is the remaining open conjecture, deliberately
left as a documented `Prop` rather than a `sorry`-ed theorem. -/

/-- Mass-level dominance predicate: the `a = 1` branch mass strictly exceeds
the combined mass of all higher branches `a ≥ 2` in the window `a ≤ A`. -/
def IsOdometerDominant (A : Nat) (W : Nat → Nat) : Prop :=
  (((List.range (A + 1)).filter fun a => decide (2 ≤ a)).map W).sum < W 1

theorem sum_map_pow_sub (l : List Nat) (A : Nat) (h : ∀ a ∈ l, a ≤ A) :
    (l.map fun a => 2 ^ (A + 1 - a)).sum = 2 * (l.map fun a => 2 ^ (A - a)).sum := by
  induction l with
  | nil => rfl
  | cons b t ih =>
      have hb : b ≤ A := h b (List.mem_cons.mpr (Or.inl rfl))
      have ht : ∀ a ∈ t, a ≤ A := fun a ha => h a (List.mem_cons.mpr (Or.inr ha))
      rw [List.map_cons, List.sum_cons, List.map_cons, List.sum_cons,
        show A + 1 - b = (A - b) + 1 from by omega, Nat.pow_add_one, Nat.mul_add, ih ht]
      ac_rfl

/-- The tail mass list sum, factored out so the two-step induction below uses
syntactically consistent terms. -/
private def tailMass (A : Nat) : Nat :=
  (((List.range (A + 1)).filter fun a => decide (2 ≤ a)).map fun a => 2 ^ (A - a)).sum

/-- The exact tail mass of the Syracuse branch weights at scale `2^A`:
`Σ_{a=2}^{A} 2^{A-a} = 2^{A-1} − 1`. -/
theorem syracuse_tail_mass (A : Nat) :
    (((List.range (A + 1)).filter fun a => decide (2 ≤ a)).map fun a => 2 ^ (A - a)).sum
      = 2 ^ (A - 1) - 1 := by
  have key : ∀ A : Nat, tailMass A = 2 ^ (A - 1) - 1 ∧ tailMass (A + 1) = 2 ^ (A + 1 - 1) - 1 := by
    intro A; induction A with
    | zero => constructor <;> decide
    | succ A ih =>
        obtain ⟨ih0, ih1⟩ := ih
        refine ⟨ih1, ?_⟩
        show tailMass (A + 1 + 1) = 2 ^ (A + 1 + 1 - 1) - 1
        unfold tailMass
        rw [List.range_succ, List.filter_append, List.map_append, List.sum_append_nat,
          List.filter_cons_of_pos (p := fun a => decide (2 ≤ a))
            (decide_eq_true (by omega : 2 ≤ A + 1 + 1)),
          List.filter_nil, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
          show A + 1 + 1 - (A + 1 + 1) = 0 from by omega, Nat.pow_zero]
        have hmem : ∀ a ∈ (List.range (A + 1 + 1)).filter (fun a => decide (2 ≤ a)),
            a ≤ A + 1 := by
          intro a ha
          have h1 := (List.mem_filter.1 ha).1
          rw [List.range_eq_range'] at h1
          have h2 := (List.mem_range'_1.1 h1).2
          omega
        rw [sum_map_pow_sub _ (A + 1) hmem]
        show 2 * tailMass (A + 1) + (1 + 0) = 2 ^ (A + 1 + 1 - 1) - 1
        rw [ih1]
        have hpos := pos_two_pow (A + 1 - 1)
        rw [show A + 1 + 1 - 1 = (A + 1 - 1) + 1 from by omega, Nat.pow_add_one]
        omega
  exact (key A).1

/-- For the exact Syracuse branch masses `W a = 2^{A-a}`, the higher-branch
tail misses the `a = 1` mass `W 1 = 2^{A-1}` by exactly one unit.  The open
odometer conjecture is that this single unit of slack survives the phase
factors (see the comment block above). -/
theorem syracuse_mass_slack (A : Nat) (_hA : 1 ≤ A) :
    (((List.range (A + 1)).filter fun a => decide (2 ≤ a)).map fun a => 2 ^ (A - a)).sum + 1
      = 2 ^ (A - 1) := by
  rw [syracuse_tail_mass A]
  have := pos_two_pow (A - 1)
  omega

end ChainClosure
