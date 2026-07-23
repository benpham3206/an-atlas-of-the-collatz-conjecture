/-!
# Terras bijection (finite-cylinder saturation) — plain Lean 4 core, no mathlib

**Source.** `contribution/proofs/PARTIAL_THEOREMS.md`, Theorem 1 (finite-cylinder
saturation): for every `k ≥ 1` and every binary word `w` of length `k` there is
exactly one residue `ρ(w) mod 2^k` such that

    n begins with parity word w  ⇔  n ≡ ρ(w) (mod 2^k).

**Formal statement.** `terras_bijection` below, phrased for an arbitrary word
`w : List Bool` with `k = w.length`. Since this toolchain's core has no
`ExistsUnique`/`∃!`, "exactly one" is spelled out as the conjunction of
existence and pairwise uniqueness. The formal statement is slightly stronger
than the prose one: it also covers the degenerate case `k = 0` (empty word,
modulus `2^0 = 1`), which is harmless. Bit convention: bit `i` of the parity
word of `n` is the parity of the `i`-th Terras iterate of `n`, with
`true = odd`, `false = even`. The Terras map is `T n = n/2` (even),
`T n = (3n+1)/2` (odd).

**Proof sketch (classical Terras argument, by induction on k).**

* `terras_affine` — the affine cocycle over a cylinder: on the arithmetic
  progression `r + 2^k·t`, the first `k` parity bits are constant
  (`parityWord k (r + 2^k·t) = parityWord k r`) and the `k`-th iterate is
  affine in `t` with slope `3^(#ones of the common parity word)`:
  `iterT k (r + 2^k·t) = iterT k r + 3^(countOnes (parityWord k r))·t`.
  Induction on `k`; each step divides by 2 (even case) or maps
  `x ↦ (3x+1)/2` (odd case), and `3·2^k·t = 2^k·(3t)`.
* `rho` — an explicit, computable residue map, built bit-by-bit from the low
  end: after processing a prefix `w` with residue `ρ`, appending bit `b` sets
  `ρ' = ρ + 2^|w|·c` where the correction bit `c ∈ {0,1}` flips the parity of
  the current iterate iff it does not already equal `b`. The affine lemma
  shows `ρ'` has parity word `w ++ [b]` and stays `< 2^(|w|+1)` (`rho_spec`).
* `inj3mod` — injectivity of `x ↦ (3x+2) mod 2^k` on residues, proved by
  induction on `k`: reduce mod `2^k`, then compare the parity of the
  `2^k`-digits of `3u+2` and `3u'+2`. This is the only place where the
  invertibility of `3 mod 2^k` is needed.
* `keyCRT` — the CRT-style gluing: equal parity plus equal `T`-image mod
  `2^k` iff equal mod `2^(k+1)`. Combined with `parityWord_eq_iff`
  (`parityWord k n = parityWord k m ⇔ n % 2^k = m % 2^k`, induction on `k`),
  this yields `rho_correct` and the existence+uniqueness package
  `terras_bijection`.

**Sanity checks.** All `k = 1, 2, 3` residues are computed and pinned by
`decide`; full cylinder checks over `n < 2^k` for the extremal words; and
`rho ∘ parityWord 3 = id` on `{0,…,7}` is verified. `#print axioms` at the end
audits that no `sorry` axiom is used.

**Exactness note.** All arithmetic is exact `Nat` arithmetic; there are no
floats anywhere in this file.

**Verification.** From the `formal/` directory:
`~/.elan/bin/lean Formal/TerrasBijection.lean`  (Lean v4.31.0 via elan).
This file has no imports; it compiles standalone.

**Counterexample watch.** Nothing in this file bears on the existence of
Collatz counterexamples; it is a structural fact about parity cylinders. The
`decide` checks are consistency witnesses, not search results. No anomaly
observed.
-/

namespace Terras

/-- The Terras map: `n/2` for even `n`, `(3n+1)/2` for odd `n`. -/
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem T_even {n : Nat} (h : n % 2 = 0) : T n = n / 2 := if_pos h

theorem T_odd {n : Nat} (h : ¬ n % 2 = 0) : T n = (3 * n + 1) / 2 := if_neg h

/-- On an odd input, one Terras step is `n ↦ 3·(n/2) + 2`. -/
theorem T_eq_three_div_add_two {n : Nat} (h : n % 2 = 1) : T n = 3 * (n / 2) + 2 := by
  have hn0 : ¬ n % 2 = 0 := by omega
  rw [T_odd hn0]
  have e := Nat.mod_add_div n 2
  omega

/-- `k`-fold iterate of `T`. -/
def iterT : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => T (iterT k n)

theorem iterT_succ' (k : Nat) (n : Nat) : iterT (k + 1) n = iterT k (T n) := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
      show T (iterT (k + 1) n) = T (iterT k (T n))
      rw [ih]

/-- The parity bit of `n`: `true` iff `n` is odd. -/
def parityOf (n : Nat) : Bool := (n % 2 == 1)

/-- The length-`k` parity word of `n`: bit `i` is the parity of `iterT i n`. -/
def parityWord : Nat → Nat → List Bool
  | 0, _ => []
  | k+1, n => parityOf n :: parityWord k (T n)

theorem parityWord_length (k n : Nat) : (parityWord k n).length = k := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
      show (parityOf n :: parityWord k (T n)).length = k + 1
      rw [List.length_cons, ih]

/-- Equality of parity bits is equality mod 2. -/
theorem parityOf_eq_iff {n m : Nat} : parityOf n = parityOf m ↔ n % 2 = m % 2 := by
  have hn : n % 2 < 2 := Nat.mod_lt _ (show 0 < 2 by decide)
  have hm : m % 2 < 2 := Nat.mod_lt _ (show 0 < 2 by decide)
  show ((n % 2 == 1) = (m % 2 == 1)) ↔ n % 2 = m % 2
  have h0or1 : n % 2 = 0 ∨ n % 2 = 1 := by omega
  have g0or1 : m % 2 = 0 ∨ m % 2 = 1 := by omega
  obtain h0 | h1 := h0or1
  · obtain g0 | g1 := g0or1
    · rw [h0, g0]; decide
    · rw [h0, g1]; decide
  · obtain g0 | g1 := g0or1
    · rw [h1, g0]; decide
    · rw [h1, g1]; decide

/-- Snoc decomposition of a parity word: the last bit is the parity of the
`k`-th iterate. -/
theorem parityWord_snoc (k : Nat) (n : Nat) :
    parityWord (k + 1) n = parityWord k n ++ [parityOf (iterT k n)] := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
      show parityOf n :: parityWord (k + 1) (T n)
          = (parityOf n :: parityWord k (T n)) ++ [parityOf (iterT (k + 1) n)]
      rw [ih (T n), iterT_succ', List.cons_append]

/-- Number of `true` bits of a parity word (count of odd steps taken). -/
def countOnes : List Bool → Nat
  | [] => 0
  | true :: l => 1 + countOnes l
  | false :: l => countOnes l

/-- Powers of 3 are odd. -/
theorem odd3pow (o : Nat) : 3 ^ o % 2 = 1 := by
  induction o with
  | zero => rfl
  | succ o ih => rw [Nat.pow_succ, Nat.mul_mod, ih]

/-- Halving decomposition for even `x`: residues mod `2^(k+1)` are twice the
halved residue mod `2^k`. -/
theorem mod_two_pow_succ_of_even (k : Nat) {x : Nat} (hx : x % 2 = 0) :
    x % 2 ^ (k + 1) = 2 * ((x / 2) % 2 ^ k) := by
  have hpos : 0 < 2 ^ k := Nat.pow_pos (by decide)
  have e1 : x = 2 * (x / 2) := by
    have hda := Nat.mod_add_div x 2
    omega
  have e2 : x / 2 = (x / 2) % 2 ^ k + 2 ^ k * ((x / 2) / 2 ^ k) := (Nat.mod_add_div _ _).symm
  have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
  have e4 : 2 ^ (k + 1) * ((x / 2) / 2 ^ k) = 2 * (2 ^ k * ((x / 2) / 2 ^ k)) := by
    rw [hp2, Nat.mul_assoc]
  have e3 : x = 2 * ((x / 2) % 2 ^ k) + 2 ^ (k + 1) * ((x / 2) / 2 ^ k) := by
    have e1' : x = 2 * ((x / 2) % 2 ^ k + 2 ^ k * ((x / 2) / 2 ^ k)) := e2 ▸ e1
    omega
  have hcong : x % 2 ^ (k + 1)
      = (2 * ((x / 2) % 2 ^ k) + 2 ^ (k + 1) * ((x / 2) / 2 ^ k)) % 2 ^ (k + 1) :=
    congrArg (fun a => a % 2 ^ (k + 1)) e3
  rw [hcong, Nat.add_mul_mod_self_left]
  exact Nat.mod_eq_of_lt (by
    have hlt := Nat.mod_lt (x / 2) hpos
    omega)

/-- Doubling-plus-one decomposition for odd `x`. -/
theorem mod_two_pow_succ_of_odd (k : Nat) {x : Nat} (hx : x % 2 = 1) :
    x % 2 ^ (k + 1) = 2 * ((x / 2) % 2 ^ k) + 1 := by
  have hpos : 0 < 2 ^ k := Nat.pow_pos (by decide)
  have e1 : x = 2 * (x / 2) + 1 := by
    have hda := Nat.mod_add_div x 2
    omega
  have e2 : x / 2 = (x / 2) % 2 ^ k + 2 ^ k * ((x / 2) / 2 ^ k) := (Nat.mod_add_div _ _).symm
  have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
  have e4 : 2 ^ (k + 1) * ((x / 2) / 2 ^ k) = 2 * (2 ^ k * ((x / 2) / 2 ^ k)) := by
    rw [hp2, Nat.mul_assoc]
  have e3 : x = (2 * ((x / 2) % 2 ^ k) + 1) + 2 ^ (k + 1) * ((x / 2) / 2 ^ k) := by
    have e1' : x = 2 * ((x / 2) % 2 ^ k + 2 ^ k * ((x / 2) / 2 ^ k)) + 1 := e2 ▸ e1
    omega
  have hcong : x % 2 ^ (k + 1)
      = ((2 * ((x / 2) % 2 ^ k) + 1) + 2 ^ (k + 1) * ((x / 2) / 2 ^ k)) % 2 ^ (k + 1) :=
    congrArg (fun a => a % 2 ^ (k + 1)) e3
  rw [hcong, Nat.add_mul_mod_self_left]
  exact Nat.mod_eq_of_lt (by
    have hlt := Nat.mod_lt (x / 2) hpos
    omega)

/-- **Affine cocycle over a cylinder.** On the progression `r + 2^k·t`, the
first `k` parity bits agree with those of `r`, and the `k`-th iterate is affine
in `t` with slope `3` raised to the number of odd steps. -/
theorem terras_affine (k r t : Nat) :
    parityWord k (r + 2 ^ k * t) = parityWord k r ∧
    iterT k (r + 2 ^ k * t) = iterT k r + 3 ^ countOnes (parityWord k r) * t := by
  induction k generalizing r t with
  | zero =>
      constructor
      · rfl
      · show r + 2 ^ 0 * t = r + 3 ^ 0 * t
        rw [Nat.pow_zero, Nat.one_mul]
  | succ k ih =>
      have h02 : 0 < 2 := by decide
      have hshape : r + 2 ^ (k + 1) * t = r + 2 * (2 ^ k * t) := by
        have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
        rw [hp2, Nat.mul_assoc]
      have hpar : (r + 2 ^ (k + 1) * t) % 2 = r % 2 := by
        rw [hshape, Nat.add_mul_mod_self_left]
      have hrlt : r % 2 < 2 := Nat.mod_lt _ h02
      have hcases : r % 2 = 0 ∨ r % 2 = 1 := by omega
      obtain heven | hodd := hcases
      · -- r even: one step divides by 2
        have hs : (r + 2 ^ (k + 1) * t) % 2 = 0 := by rw [hpar]; exact heven
        have hTs : T (r + 2 ^ (k + 1) * t) = T r + 2 ^ k * t := by
          rw [T_even hs, T_even heven, hshape, Nat.add_mul_div_left _ _ h02]
        have hcount : countOnes (parityWord (k + 1) r) = countOnes (parityWord k (T r)) := by
          have hpf : parityOf r = false := by
            show (r % 2 == 1) = false; rw [heven]; rfl
          show countOnes (parityOf r :: parityWord k (T r)) = countOnes (parityWord k (T r))
          rw [hpf]; rfl
        constructor
        · show parityOf (r + 2 ^ (k + 1) * t) :: parityWord k (T (r + 2 ^ (k + 1) * t))
              = parityOf r :: parityWord k (T r)
          have hhead : parityOf (r + 2 ^ (k + 1) * t) = parityOf r := by
            show ((r + 2 ^ (k + 1) * t) % 2 == 1) = (r % 2 == 1)
            rw [hpar]
          rw [hhead, hTs, (ih (T r) t).1]
        · rw [iterT_succ', hTs, (ih (T r) t).2, ← iterT_succ', hcount]
      · -- r odd: one step is x ↦ (3x+1)/2, absorbing a factor 3
        have hs : (r + 2 ^ (k + 1) * t) % 2 = 1 := by rw [hpar]; exact hodd
        have hTs : T (r + 2 ^ (k + 1) * t) = T r + 2 ^ k * (3 * t) := by
          rw [T_odd (by rw [hs]; decide), T_odd (by rw [hodd]; decide), hshape]
          have e1 : 3 * (r + 2 * (2 ^ k * t)) + 1 = (3 * r + 1) + 2 * (3 * (2 ^ k * t)) := by
            omega
          rw [e1, Nat.add_mul_div_left _ _ h02, Nat.mul_left_comm]
        have hcount : countOnes (parityWord (k + 1) r) = countOnes (parityWord k (T r)) + 1 := by
          have hpt : parityOf r = true := by
            show (r % 2 == 1) = true; rw [hodd]; rfl
          show countOnes (parityOf r :: parityWord k (T r)) = countOnes (parityWord k (T r)) + 1
          rw [hpt]; exact Nat.add_comm _ _
        constructor
        · show parityOf (r + 2 ^ (k + 1) * t) :: parityWord k (T (r + 2 ^ (k + 1) * t))
              = parityOf r :: parityWord k (T r)
          have hhead : parityOf (r + 2 ^ (k + 1) * t) = parityOf r := by
            show ((r + 2 ^ (k + 1) * t) % 2 == 1) = (r % 2 == 1)
            rw [hpar]
          rw [hhead, hTs, (ih (T r) (3 * t)).1]
        · have hp3 : 3 ^ (countOnes (parityWord k (T r)) + 1)
              = 3 ^ countOnes (parityWord k (T r)) * 3 := Nat.pow_succ 3 _
          rw [iterT_succ', hTs, (ih (T r) (3 * t)).2, ← iterT_succ', hcount, hp3, Nat.mul_assoc]

/-- **Injectivity of `x ↦ 3x+2` modulo `2^k`.** The only place where the
invertibility of `3 mod 2^k` is used; proved by induction on `k` comparing the
parity of the `2^k`-digits of `3u+2` and `3u'+2`. -/
theorem inj3mod (k u u' : Nat) (h : (3 * u + 2) % 2 ^ k = (3 * u' + 2) % 2 ^ k) :
    u % 2 ^ k = u' % 2 ^ k := by
  induction k generalizing u u' with
  | zero => rw [Nat.pow_zero, Nat.mod_one, Nat.mod_one]
  | succ k ih =>
      have h02 : 0 < 2 := by decide
      have hpos : 0 < 2 ^ k := Nat.pow_pos h02
      have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
      have hp2' : 2 ^ (k + 1) = 2 ^ k * 2 := Nat.pow_succ 2 k
      have hdvd : 2 ^ k ∣ 2 ^ (k + 1) := ⟨2, hp2'⟩
      have hlo : (3 * u + 2) % 2 ^ k = (3 * u' + 2) % 2 ^ k := by
        have e := Nat.mod_mod_of_dvd (3 * u + 2) hdvd
        have e' := Nat.mod_mod_of_dvd (3 * u' + 2) hdvd
        rw [← e, h, e']
      have hv : u % 2 ^ k = u' % 2 ^ k := ih u u' hlo
      -- strip the `2^k`-digit of `3·+2`
      have hdu : (3 * u + 2) / 2 ^ k = (3 * (u % 2 ^ k) + 2) / 2 ^ k + 3 * (u / 2 ^ k) := by
        have e1 : 3 * u + 2 = (3 * (u % 2 ^ k) + 2) + 2 ^ k * (3 * (u / 2 ^ k)) := by
          have hda := Nat.mod_add_div u (2 ^ k)
          have h3 : 2 ^ k * (3 * (u / 2 ^ k)) = 3 * (2 ^ k * (u / 2 ^ k)) :=
            Nat.mul_left_comm _ _ _
          rw [h3]
          omega
        rw [e1, Nat.add_mul_div_left _ _ hpos]
      have hdu' : (3 * u' + 2) / 2 ^ k = (3 * (u % 2 ^ k) + 2) / 2 ^ k + 3 * (u' / 2 ^ k) := by
        have e1 : 3 * u' + 2 = (3 * (u % 2 ^ k) + 2) + 2 ^ k * (3 * (u' / 2 ^ k)) := by
          have hda := Nat.mod_add_div u' (2 ^ k)
          have h3 : 2 ^ k * (3 * (u' / 2 ^ k)) = 3 * (2 ^ k * (u' / 2 ^ k)) :=
            Nat.mul_left_comm _ _ _
          rw [← hv] at hda
          rw [h3]
          omega
        rw [e1, Nat.add_mul_div_left _ _ hpos]
      -- the parity of the `2^k`-digits of `3u+2` and `3u'+2` agree, via `h`
      have hdiv : ((3 * u + 2) / 2 ^ k) % 2 = ((3 * u' + 2) / 2 ^ k) % 2 := by
        have key : ∀ X R : Nat, ((2 ^ (k + 1) * X + R) / 2 ^ k) % 2 = (R / 2 ^ k) % 2 := by
          intro X R
          have e1 : 2 ^ (k + 1) * X = 2 ^ k * (2 * X) := by rw [hp2', Nat.mul_assoc]
          rw [e1, Nat.add_comm, Nat.add_mul_div_left _ _ hpos, Nat.add_mul_mod_self_left]
        rw [← Nat.div_add_mod (3 * u + 2) (2 ^ (k + 1))]
        rw [← Nat.div_add_mod (3 * u' + 2) (2 ^ (k + 1))]
        rw [h, key, key]
      rw [hdu, hdu'] at hdiv
      have hq : (u / 2 ^ k) % 2 = (u' / 2 ^ k) % 2 := by omega
      -- final gluing: a residue mod `2^(k+1)` is determined by its mod-`2^k`
      -- part plus the parity of its `2^k`-digit
      have fin : ∀ x : Nat, x % 2 ^ k = u % 2 ^ k →
          x % 2 ^ (k + 1) = u % 2 ^ k + 2 ^ k * ((x / 2 ^ k) % 2) := by
        intro x hx
        have e2 : x / 2 ^ k = 2 * ((x / 2 ^ k) / 2) + (x / 2 ^ k) % 2 :=
          (Nat.div_add_mod _ _).symm
        have e4 : 2 ^ (k + 1) * ((x / 2 ^ k) / 2) = 2 ^ k * (2 * ((x / 2 ^ k) / 2)) := by
          rw [hp2', Nat.mul_assoc]
        have e3 : x = (u % 2 ^ k + 2 ^ k * ((x / 2 ^ k) % 2))
            + 2 ^ (k + 1) * ((x / 2 ^ k) / 2) := by
          have e1' : x = u % 2 ^ k + 2 ^ k * (x / 2 ^ k) := by
            have e := (Nat.mod_add_div x (2 ^ k)).symm
            rwa [hx] at e
          rw [e2, Nat.mul_add] at e1'
          omega
        have hcong : x % 2 ^ (k + 1)
            = ((u % 2 ^ k + 2 ^ k * ((x / 2 ^ k) % 2))
              + 2 ^ (k + 1) * ((x / 2 ^ k) / 2)) % 2 ^ (k + 1) :=
          congrArg (fun a => a % 2 ^ (k + 1)) e3
        rw [hcong, Nat.add_mul_mod_self_left]
        apply Nat.mod_eq_of_lt
        have h1 : u % 2 ^ k < 2 ^ k := Nat.mod_lt _ hpos
        have h2 : (x / 2 ^ k) % 2 < 2 := Nat.mod_lt _ h02
        have hqc : (x / 2 ^ k) % 2 = 0 ∨ (x / 2 ^ k) % 2 = 1 := by omega
        obtain hq0 | hq1 := hqc
        · rw [hq0]; omega
        · rw [hq1]; omega
      rw [fin u rfl, fin u' hv.symm, hq]

/-- **CRT step.** Same parity and same `T`-image mod `2^k` iff same value mod
`2^(k+1)`. -/
theorem keyCRT (k n m : Nat) :
    (n % 2 = m % 2 ∧ T n % 2 ^ k = T m % 2 ^ k) ↔ n % 2 ^ (k + 1) = m % 2 ^ (k + 1) := by
  have h02 : 0 < 2 := by decide
  constructor
  · intro h
    obtain ⟨hpar, hT⟩ := h
    have hn2 : n % 2 < 2 := Nat.mod_lt _ h02
    have hc : n % 2 = 0 ∨ n % 2 = 1 := by omega
    obtain h0 | h1 := hc
    · have hm0 : m % 2 = 0 := by omega
      rw [T_even h0, T_even hm0] at hT
      rw [mod_two_pow_succ_of_even k h0, mod_two_pow_succ_of_even k hm0, hT]
    · have hm1 : m % 2 = 1 := by omega
      have hTn : T n = 3 * (n / 2) + 2 := T_eq_three_div_add_two h1
      have hTm : T m = 3 * (m / 2) + 2 := T_eq_three_div_add_two hm1
      rw [hTn, hTm] at hT
      have hs : (n / 2) % 2 ^ k = (m / 2) % 2 ^ k := inj3mod k _ _ hT
      rw [mod_two_pow_succ_of_odd k h1, mod_two_pow_succ_of_odd k hm1, hs]
  · intro h
    have hdvd2 : (2 : Nat) ∣ 2 ^ (k + 1) :=
      ⟨2 ^ k, (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)⟩
    have hpar : n % 2 = m % 2 := by
      rw [← Nat.mod_mod_of_dvd n hdvd2, h, Nat.mod_mod_of_dvd m hdvd2]
    refine ⟨hpar, ?_⟩
    have hn2 : n % 2 < 2 := Nat.mod_lt _ h02
    have hc : n % 2 = 0 ∨ n % 2 = 1 := by omega
    obtain h0 | h1 := hc
    · have hm0 : m % 2 = 0 := by omega
      rw [T_even h0, T_even hm0]
      have e1 := Nat.div_add_mod n (2 ^ (k + 1))
      have e2 := Nat.div_add_mod m (2 ^ (k + 1))
      rw [← e1, ← e2, h]
      have key : ∀ X R : Nat, ((2 ^ (k + 1) * X + R) / 2) % 2 ^ k = (R / 2) % 2 ^ k := by
        intro X R
        have eX : 2 ^ (k + 1) * X = 2 * (2 ^ k * X) := by
          have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
          rw [hp2, Nat.mul_assoc]
        rw [eX, Nat.add_comm, Nat.add_mul_div_left _ _ h02, Nat.add_mul_mod_self_left]
      rw [key, key]
    · have hm1 : m % 2 = 1 := by omega
      have hn0 : ¬ n % 2 = 0 := by omega
      have hm0' : ¬ m % 2 = 0 := by omega
      rw [T_odd hn0, T_odd hm0']
      have e1 := Nat.div_add_mod n (2 ^ (k + 1))
      have e2 := Nat.div_add_mod m (2 ^ (k + 1))
      rw [← e1, ← e2, h]
      have key : ∀ X R : Nat,
          ((3 * (2 ^ (k + 1) * X + R) + 1) / 2) % 2 ^ k = ((3 * R + 1) / 2) % 2 ^ k := by
        intro X R
        have hp2 : 2 ^ (k + 1) = 2 * 2 ^ k := (Nat.pow_succ 2 k).trans (Nat.mul_comm _ _)
        have eX1 : 2 ^ (k + 1) * X = 2 * (2 ^ k * X) := by rw [hp2, Nat.mul_assoc]
        have eX2 : 2 ^ k * (3 * X) = 3 * (2 ^ k * X) := Nat.mul_left_comm _ _ _
        have eX : 3 * (2 ^ (k + 1) * X + R) + 1 = (3 * R + 1) + 2 * (2 ^ k * (3 * X)) := by
          rw [eX1, eX2]; omega
        rw [eX, Nat.add_mul_div_left _ _ h02, Nat.add_mul_mod_self_left]
      rw [key, key]

/-- **Two-sided Terras congruence.** The length-`k` parity word of `n`
determines and is determined by `n mod 2^k`. -/
theorem parityWord_eq_iff (k n m : Nat) :
    parityWord k n = parityWord k m ↔ n % 2 ^ k = m % 2 ^ k := by
  induction k generalizing n m with
  | zero =>
      constructor
      · intro _; rw [Nat.pow_zero, Nat.mod_one, Nat.mod_one]
      · intro _; rfl
  | succ k ih =>
      show ((parityOf n :: parityWord k (T n)) = (parityOf m :: parityWord k (T m))) ↔ _
      rw [List.cons.injEq, parityOf_eq_iff, ih (T n) (T m)]
      exact keyCRT k n m

/-- The correction bit: `0` if the current iterate already has the target
parity `b`, else `1` (which flips the parity, since the slope `3^o` is odd). -/
def corrBit (k r : Nat) (b : Bool) : Nat :=
  if (parityOf (iterT k r) == b) then 0 else 1

/-- One step of the residue fold: extend the modulus from `2^k` to `2^(k+1)`. -/
def rhoStep (p : Nat × Nat) (b : Bool) : Nat × Nat :=
  (p.1 + 1, p.2 + 2 ^ p.1 * corrBit p.1 p.2 b)

/-- **The residue map.** `rho w` is the unique residue mod `2^w.length` whose
parity word is `w`, computed low-bit-first. -/
def rho (w : List Bool) : Nat := (w.foldl rhoStep (0, 0)).2

theorem foldl_fst (w : List Bool) (p : Nat × Nat) :
    (w.foldl rhoStep p).1 = p.1 + w.length := by
  induction w generalizing p with
  | nil => rfl
  | cons b l ih =>
      show (l.foldl rhoStep (rhoStep p b)).1 = p.1 + (l.length + 1)
      rw [ih]
      show (p.1 + 1) + l.length = p.1 + (l.length + 1)
      omega

theorem foldl_fst_zero (w : List Bool) : (w.foldl rhoStep (0, 0)).1 = w.length := by
  have h := foldl_fst w (0, 0)
  rwa [show (0, 0).1 + w.length = w.length from Nat.zero_add _] at h

theorem rho_snoc (w : List Bool) (b : Bool) :
    rho (w ++ [b]) = rho w + 2 ^ w.length * corrBit w.length (rho w) b := by
  show ((w ++ [b]).foldl rhoStep (0, 0)).2 = _
  rw [List.foldl_append]
  show (rhoStep (w.foldl rhoStep (0, 0)) b).2 = _
  show (w.foldl rhoStep (0, 0)).2
      + 2 ^ (w.foldl rhoStep (0, 0)).1 * corrBit (w.foldl rhoStep (0, 0)).1 (w.foldl rhoStep (0, 0)).2 b
      = (w.foldl rhoStep (0, 0)).2 + 2 ^ w.length * corrBit w.length (w.foldl rhoStep (0, 0)).2 b
  rw [foldl_fst_zero]

/-- Snoc induction for Boolean words (core has no `List.reverseRecOn`). -/
theorem snoc_ind {motive : List Bool → Prop} (h0 : motive [])
    (hs : ∀ (l : List Bool) (b : Bool), motive l → motive (l ++ [b])) :
    ∀ (l : List Bool), motive l := by
  intro l
  rw [← List.reverse_reverse l]
  induction l.reverse with
  | nil => exact h0
  | cons b t ih =>
      rw [List.reverse_cons]
      exact hs _ _ ih

/-- **Correctness of the residue map**: `rho w` has parity word `w` and lies
below the modulus `2^w.length`. -/
theorem rho_spec (w : List Bool) :
    parityWord w.length (rho w) = w ∧ rho w < 2 ^ w.length := by
  induction w using snoc_ind with
  | h0 =>
      constructor
      · rfl
      · decide
  | hs l b ih =>
      obtain ⟨ihpar, ihlt⟩ := ih
      have hlen : (l ++ [b]).length = l.length + 1 := by
        rw [List.length_append, List.length_singleton]
      have h02 : 0 < 2 := by decide
      have hpos : 0 < 2 ^ l.length := Nat.pow_pos h02
      have hp2 : 2 ^ (l.length + 1) = 2 * 2 ^ l.length :=
        (Nat.pow_succ 2 _).trans (Nat.mul_comm _ _)
      rw [hlen, rho_snoc]
      have hc2 : corrBit l.length (rho l) b < 2 := by
        show (if (parityOf (iterT l.length (rho l)) == b) then 0 else 1) < 2
        split <;> decide
      -- the new last bit is `b`: the correction bit flips the parity iff needed
      have hbit : parityOf (iterT l.length (rho l)
          + 3 ^ countOnes l * corrBit l.length (rho l) b) = b := by
        have h3odd : 3 ^ countOnes l % 2 = 1 := odd3pow _
        have hc22 : corrBit l.length (rho l) b % 2 < 2 := Nat.mod_lt _ h02
        have e3 : (iterT l.length (rho l) + 3 ^ countOnes l * corrBit l.length (rho l) b) % 2
            = (iterT l.length (rho l) + corrBit l.length (rho l) b) % 2 := by
          rw [Nat.add_mod, Nat.mul_mod, h3odd, Nat.one_mul, Nat.mod_eq_of_lt hc22,
            ← Nat.add_mod]
        have hlt2 : iterT l.length (rho l) % 2 < 2 := Nat.mod_lt _ h02
        have hcases : iterT l.length (rho l) % 2 = 0 ∨ iterT l.length (rho l) % 2 = 1 := by
          omega
        show ((iterT l.length (rho l) + 3 ^ countOnes l * corrBit l.length (rho l) b) % 2 == 1)
            = b
        rw [e3]
        cases b with
        | false =>
            obtain h0 | h1 := hcases
            · have hpf : parityOf (iterT l.length (rho l)) = false := by
                show (iterT l.length (rho l) % 2 == 1) = false; rw [h0]; rfl
              have hc : corrBit l.length (rho l) false = 0 := by
                show (if (parityOf (iterT l.length (rho l)) == false) then 0 else 1) = 0
                rw [hpf]; decide
              rw [hc, Nat.add_zero, h0]; rfl
            · have hpf : parityOf (iterT l.length (rho l)) = true := by
                show (iterT l.length (rho l) % 2 == 1) = true; rw [h1]; rfl
              have hc : corrBit l.length (rho l) false = 1 := by
                show (if (parityOf (iterT l.length (rho l)) == false) then 0 else 1) = 1
                rw [hpf]; decide
              have hz : (iterT l.length (rho l) + 1) % 2 = 0 := by omega
              rw [hc, hz]; rfl
        | true =>
            obtain h0 | h1 := hcases
            · have hpf : parityOf (iterT l.length (rho l)) = false := by
                show (iterT l.length (rho l) % 2 == 1) = false; rw [h0]; rfl
              have hc : corrBit l.length (rho l) true = 1 := by
                show (if (parityOf (iterT l.length (rho l)) == true) then 0 else 1) = 1
                rw [hpf]; decide
              have hz : (iterT l.length (rho l) + 1) % 2 = 1 := by omega
              rw [hc, hz]; rfl
            · have hpf : parityOf (iterT l.length (rho l)) = true := by
                show (iterT l.length (rho l) % 2 == 1) = true; rw [h1]; rfl
              have hc : corrBit l.length (rho l) true = 0 := by
                show (if (parityOf (iterT l.length (rho l)) == true) then 0 else 1) = 0
                rw [hpf]; decide
              rw [hc, Nat.add_zero, h1]; rfl
      constructor
      · rw [parityWord_snoc,
          (terras_affine l.length (rho l) (corrBit l.length (rho l) b)).1, ihpar,
          (terras_affine l.length (rho l) (corrBit l.length (rho l) b)).2, ihpar,
          hbit]
      · rw [hp2]
        have h2kc : 2 ^ l.length * corrBit l.length (rho l) b ≤ 2 ^ l.length := by
          have hc1 : corrBit l.length (rho l) b ≤ 1 := by
            show (if (parityOf (iterT l.length (rho l)) == b) then 0 else 1) ≤ 1
            split <;> decide
          have hml := Nat.mul_le_mul_left (2 ^ l.length) hc1
          rwa [Nat.mul_one] at hml
        omega

/-- **Pointwise characterization of the cylinder**: `n` begins with parity
word `w` iff `n ≡ rho w (mod 2^w.length)`. -/
theorem rho_correct (w : List Bool) (n : Nat) :
    parityWord w.length n = w ↔ n % 2 ^ w.length = rho w := by
  obtain ⟨h1, h2⟩ := rho_spec w
  have hmod : rho w % 2 ^ w.length = rho w := Nat.mod_eq_of_lt h2
  constructor
  · intro h
    have h3 : parityWord w.length n = parityWord w.length (rho w) := h.trans h1.symm
    exact ((parityWord_eq_iff _ _ _).1 h3).trans hmod
  · intro h
    have h3 : parityWord w.length n = parityWord w.length (rho w) :=
      (parityWord_eq_iff _ _ _).2 (h.trans hmod.symm)
    exact h3.trans h1

/-- **Theorem 1 (finite-cylinder saturation / Terras bijection).** For every
binary word `w` there is exactly one residue `r` mod `2^w.length` such that
`n` begins with parity word `w` iff `n ≡ r (mod 2^w.length)`. "Exactly one"
is existence plus pairwise uniqueness (core has no `ExistsUnique`). -/
theorem terras_bijection (w : List Bool) :
    (∃ r : Nat, r < 2 ^ w.length ∧
        ∀ n : Nat, parityWord w.length n = w ↔ n % 2 ^ w.length = r) ∧
    (∀ r₁ r₂ : Nat,
      (r₁ < 2 ^ w.length ∧ ∀ n : Nat, parityWord w.length n = w ↔ n % 2 ^ w.length = r₁) →
      (r₂ < 2 ^ w.length ∧ ∀ n : Nat, parityWord w.length n = w ↔ n % 2 ^ w.length = r₂) →
      r₁ = r₂) := by
  refine ⟨⟨rho w, ⟨(rho_spec w).2, fun n => rho_correct w n⟩⟩, ?_⟩
  intro r₁ r₂ h₁ h₂
  obtain ⟨h1lt, h1iff⟩ := h₁
  obtain ⟨h2lt, h2iff⟩ := h₂
  have e1 : r₁ = rho w := by
    have hw : parityWord w.length r₁ = w := (h1iff r₁).2 (by rw [Nat.mod_eq_of_lt h1lt])
    have hm : r₁ % 2 ^ w.length = rho w := (rho_correct w r₁).1 hw
    rwa [Nat.mod_eq_of_lt h1lt] at hm
  have e2 : r₂ = rho w := by
    have hw : parityWord w.length r₂ = w := (h2iff r₂).2 (by rw [Nat.mod_eq_of_lt h2lt])
    have hm : r₂ % 2 ^ w.length = rho w := (rho_correct w r₂).1 hw
    rwa [Nat.mod_eq_of_lt h2lt] at hm
  rw [e1, e2]

end Terras

/-! ## Sanity checks (all closed by `decide`) -/

namespace Terras

-- Terras map and iterates
example : T 7 = 11 ∧ iterT 2 7 = 17 ∧ iterT 3 7 = 26 := by decide

-- k = 1: explicit residues
example : rho [false] = 0 := by decide
example : rho [true] = 1 := by decide

-- k = 2: explicit residues
example : rho [false, false] = 0 := by decide
example : rho [false, true] = 2 := by decide
example : rho [true, false] = 1 := by decide
example : rho [true, true] = 3 := by decide

-- k = 3: explicit residues (a permutation of 0..7, as the bijection requires)
example : rho [false, false, false] = 0 := by decide
example : rho [false, false, true] = 4 := by decide
example : rho [false, true, false] = 2 := by decide
example : rho [false, true, true] = 6 := by decide
example : rho [true, false, false] = 5 := by decide
example : rho [true, false, true] = 1 := by decide
example : rho [true, true, false] = 3 := by decide
example : rho [true, true, true] = 7 := by decide

-- full-cylinder checks for the extremal words at k = 1, 2, 3
example : ∀ n : Nat, n < 2 → (parityWord 1 n = [true] ↔ n % 2 = 1) := by decide
example : ∀ n : Nat, n < 4 → (parityWord 2 n = [true, false] ↔ n % 4 = 1) := by decide
example : ∀ n : Nat, n < 8 → (parityWord 3 n = [true, true, true] ↔ n % 8 = 7) := by decide

-- `rho` is a section of the parity-word map on residues mod 8
example : (List.range 8).map (fun n => rho (parityWord 3 n))
    = [0, 1, 2, 3, 4, 5, 6, 7] := by decide

end Terras

-- Axiom audit: must not list `sorryAx`.
#print axioms Terras.terras_bijection
#print axioms Terras.rho_correct
#print axioms Terras.terras_affine
