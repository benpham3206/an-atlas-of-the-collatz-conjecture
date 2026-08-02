import Formal.CollisionPrinciple

/-!
# Contraction onset: the Syracuse cocycle, Lemma 1, and the `M(h)` bound —
plain Lean 4 core, no mathlib

**Source.** `contribution/packets/2026-07-24-contraction-onset/`
`COLLATZ_CONTRACTION_ONSET.md` (memo) and `verify_contraction_onset.py`
(executable evidence: the affine identity checked on 600 000 instances,
Lemma 1 on 9 998 first descents, Lemma 2 on 24 611 prefixes, the `M(h)` table
to `h ≤ 1 000 000`).  Priority note: the packet itself records that its
content is Terras (1976), refreshed quantitatively à la Garner (1981); this
file formalizes the packet's *statements and proofs*, which are the atlas's
own coordinates for that classical material.

**Setup (packet §3).**  The accelerated Syracuse map on positive odd
integers, `S(x) = (3x+1) / 2^{v₂(3x+1)}`, with `a_i = v₂(3x_{i-1}+1)`,
`A_i = a₁+⋯+a_i`, `C₀ = 0`, `C_{i+1} = 3C_i + 2^{A_i}`.  The exact cocycle is
`S^h(x) = (3^h x + C_h) / 2^{A_h}`, used everywhere in its cross-multiplied
integer form `2^{A_h} · S^h(x) = 3^h · x + C_h` — exactly the identity the
verifier checks.

**What is formalized.**  Everything in the packet's proof chain that is pure
integer arithmetic:

* `v2`, `v2_spec` — a computable exact 2-adic valuation (fuel-bounded factor
  stripping) with its specification `n = 2^{v₂ n} · oddPart n`,
  `oddPart n % 2 = 1` for `n > 0`.
* `syracuse_eq_iterT` — one Syracuse step from an odd `x` is exactly
  `v₂(3x+1)` Terras steps (`iterT` from `Formal.TerrasBijection`), and
  `iterS_eq_iterT` — `h` Syracuse steps are `A_h` Terras steps.  This is the
  glue between the packet's accelerated coordinates and the atlas's Terras
  formalism.
* `cocycle_identity` — the telescoping cocycle `2^{A_h}·S^h(x) = 3^h·x + C_h`,
  by induction on `h`.  The packet restricts to odd `x`; the identity needs
  no parity hypothesis (for even `x` the definitional extension
  `S(x) = 3x+1` still satisfies it), so the formal statement is stronger.
* `descent_requires_contraction` — **Lemma 1** (Terras's `κ(n) ≤ σ(n)`):
  `S^h(x) < x` forces `3^h < 2^{A_h}`: the offset `C_h ≥ 1` is strictly
  positive, so descent puts the homogeneous multiplier below `1`.  As with
  the cocycle, the oddness hypothesis of the prose is unnecessary and
  dropped.
* `corrC_bound` — **Lemma 2**: if no `j < h` is contracting then
  `C_h ≤ h·3^{h-1}` (direct induction on the offset recurrence; each step
  contributes at most one extra power of `3`).
* `aStar`, `aStar_spec`, `aStar_min` — `A*(h)`, the least exponent with
  `3^h < 2^{A*(h)}` (the packet's `bit_length(3^h)`), computed by a fuelled
  search and specified by minimality.
* `M`, `M_le` — the onset bound `M(h) = ⌊ h·3^{h-1} / (2^{A*(h)} − 3^h) ⌋`
  and the trivial arithmetic bound `M(h) ≤ h·3^{h-1}`.
* `onset_bound` — **the Theorem** (Terras's method: bound `β`, lower-bound
  `1−α`, conclude `x ≤ β/(1−α)`): if `h` is the *first* contracting index of
  `x` and `S^h(x) ≥ x`, then `x ≤ M(h)`.  The proof follows the memo line by
  line: Lemma 2 supplies `C_h ≤ h·3^{h-1}` and minimality of `A*(h)` supplies
  `2^{A_h} − 3^h ≥ 2^{A*(h)} − 3^h > 0`.
* `no_contracting_in_window` — the logical skeleton of the §7 Corollary: if
  `x` never descends below itself on a window `1 ≤ j ≤ H` and `M(j) < x`
  throughout the window, then **no** index in the window is contracting for
  `x` (strong induction extracts the first contracting index, the Theorem
  bounds `x ≤ M(h)`, contradiction).

**What is NOT formalized, and why.**

* The Corollary's numeric input `max_{h ≤ 1 000 000} M(h) = 984 572 779 224
  < 2^71`.  This is an exact but `10^6`-entry computation; it lives in the
  Python verifier and its certificate, not in the Lean kernel.  Sample rows
  of the table are pinned by `decide` below up to `h = 15 601`
  (`M(15601) = 285 814 986`); the record row `h = 190 537` is computable in
  principle but too slow for a kernel `decide`.  `no_contracting_in_window`
  takes the window bound as a hypothesis, so the day the table is certified
  the corollary plugs in verbatim.
* Bařina's verification (`n < 2^71` reaches 1) — an external computational
  result the packet consumes; it appears here only as the informal reading of
  `no_contracting_in_window`.
* The Diophantine reading (`θ_h`, `log₂3`, irrationality measures) and the
  equivalent "one-density ≥ log₃2" formulation of the Claim — real analysis,
  unstateable in plain core.
* The odd-`x` scan (`first contracting = first descent` for every odd
  `1 < x ≤ 1 447 674 322`) — a finite computation, not a proof; named
  controls (`x = 3, 7`) are pinned by `decide` as sanity checks.

**Exactness note.**  All arithmetic is exact `Nat` arithmetic; there are no
floats anywhere in this file.

**Verification.**  From `formal/`: `lake build`, or standalone
`~/.elan/bin/lean Formal/ContractionOnset.lean` after the other modules are
built.  `#print axioms` at the end audits that no `sorry` axiom is used.

**Counterexample watch.**  This file constrains a *hypothetical* object: it
proves that a non-descending orbit cannot contract before depth `h` unless
`x ≤ M(h)`.  It neither proves nor refutes the Collatz conjecture, and the
odd-`x` scan is not formalized here.  No anomaly observed.
-/

namespace CollatzAtlas.ContractionOnset

open Terras

/-! ## 1. The exact 2-adic valuation -/

/-- Auxiliary fuelled valuation: strip factors of `2` from `n`, at most `fuel`
times.  `v2Go fuel n` is the exact 2-adic valuation of `n` whenever
`0 < n ≤ fuel`. -/
def v2Go : Nat → Nat → Nat
  | 0, _ => 0
  | fuel + 1, n => if n % 2 = 0 then v2Go fuel (n / 2) + 1 else 0

/-- Specification of the fuelled valuation: the odd part of `n` is odd and
`n` splits as `2^{v₂} · oddPart`. -/
theorem v2Go_spec (fuel : Nat) : ∀ n, 0 < n → n ≤ fuel →
    2 ^ v2Go fuel n * (n / 2 ^ v2Go fuel n) = n ∧ (n / 2 ^ v2Go fuel n) % 2 = 1 := by
  induction fuel with
  | zero => intro n hpos hle; omega
  | succ fuel ih =>
      intro n hpos hle
      by_cases hpar : n % 2 = 0
      · -- even: strip one factor and apply the induction hypothesis
        have h2 : n = 2 * (n / 2) := by omega
        have hpos' : 0 < n / 2 := by omega
        have hle' : n / 2 ≤ fuel := by omega
        obtain ⟨hmul, hodd⟩ := ih (n / 2) hpos' hle'
        have hstep : v2Go (fuel + 1) n = v2Go fuel (n / 2) + 1 := by
          show (if n % 2 = 0 then v2Go fuel (n / 2) + 1 else 0) = _
          rw [if_pos hpar]
        rw [hstep]
        have hpow : (2 : Nat) ^ (v2Go fuel (n / 2) + 1) = 2 * 2 ^ v2Go fuel (n / 2) :=
          (Nat.pow_succ 2 _).trans (Nat.mul_comm _ _)
        have hdiv : n / 2 ^ (v2Go fuel (n / 2) + 1) = n / 2 / 2 ^ v2Go fuel (n / 2) := by
          have e := congrArg (· / (2 * 2 ^ v2Go fuel (n / 2))) h2
          rw [hpow, e, Nat.mul_div_mul_left _ _ (by decide : 0 < 2)]
        constructor
        · have e : 2 ^ (v2Go fuel (n / 2) + 1) * (n / 2 ^ (v2Go fuel (n / 2) + 1))
              = 2 * (2 ^ v2Go fuel (n / 2) * (n / 2 / 2 ^ v2Go fuel (n / 2))) := by
            rw [hdiv, hpow, Nat.mul_assoc]
          rw [e, hmul]
          exact h2.symm
        · rw [hdiv]; exact hodd
      · -- odd: the valuation is 0 and the odd part is `n` itself
        have hstep : v2Go (fuel + 1) n = 0 := by
          show (if n % 2 = 0 then v2Go fuel (n / 2) + 1 else 0) = 0
          rw [if_neg hpar]
        rw [hstep]
        have hlt2 : n % 2 < 2 := Nat.mod_lt n (by decide : 0 < 2)
        constructor
        · rw [Nat.pow_zero, Nat.one_mul, Nat.div_one]
        · rw [Nat.pow_zero, Nat.div_one]; omega

/-- The exact 2-adic valuation of a positive natural (computable). -/
def v2 (n : Nat) : Nat := v2Go n n

/-- Specification: `n = 2^{v₂ n} · (n / 2^{v₂ n})` with odd cofactor. -/
theorem v2_spec (n : Nat) (h : 0 < n) :
    2 ^ v2 n * (n / 2 ^ v2 n) = n ∧ (n / 2 ^ v2 n) % 2 = 1 :=
  v2Go_spec n n h (Nat.le_refl n)

/-- A positive even number has positive valuation. -/
theorem v2_pos_of_even {n : Nat} (hpos : 0 < n) (hpar : n % 2 = 0) : 1 ≤ v2 n := by
  obtain ⟨hmul, hodd⟩ := v2_spec n hpos
  cases hv : v2 n with
  | zero =>
      rw [hv, Nat.pow_zero, Nat.one_mul, Nat.div_one] at hmul
      rw [hv, Nat.pow_zero, Nat.div_one] at hodd
      omega
  | succ k => exact Nat.succ_le_succ (Nat.zero_le k)

/-! ## 2. The Syracuse map and its Terras form -/

/-- The accelerated Syracuse map: divide `3x+1` by its full 2-adic valuation.
For odd `x` this is the packet's `S(x)`; the definition makes sense (and the
cocycle below remains true) for all `x`. -/
def syracuse (x : Nat) : Nat := (3 * x + 1) / 2 ^ v2 (3 * x + 1)

/-- One Syracuse step consumes exactly the valuation of `3x+1`. -/
theorem syracuse_spec (x : Nat) : 2 ^ v2 (3 * x + 1) * syracuse x = 3 * x + 1 :=
  (v2_spec (3 * x + 1) (by omega)).1

/-- The Syracuse map lands on odd numbers. -/
theorem syracuse_odd (x : Nat) : syracuse x % 2 = 1 :=
  (v2_spec (3 * x + 1) (by omega)).2

/-- The Syracuse map lands on positive numbers. -/
theorem syracuse_pos (x : Nat) : 0 < syracuse x := by
  have h := syracuse_odd x
  omega

/-- **Syracuse step = `v₂(3x+1)` Terras steps.**  From an odd `x`, the first
Terras step is the odd branch `x ↦ (3x+1)/2`, and the remaining
`v₂(3x+1) − 1` steps are halvings, since `2^{v₂(3x+1)} ∣ 3x+1`. -/
theorem syracuse_eq_iterT {x : Nat} (hx : x % 2 = 1) :
    syracuse x = iterT (v2 (3 * x + 1)) x := by
  have hspec := v2_spec (3 * x + 1) (by omega)
  have htpar : (3 * x + 1) % 2 = 0 := by omega
  have ha1 : 1 ≤ v2 (3 * x + 1) := v2_pos_of_even (by omega) htpar
  have hdvd : 2 ^ v2 (3 * x + 1) ∣ 3 * x + 1 := ⟨_, hspec.1.symm⟩
  -- for every `1 ≤ k ≤ v₂(3x+1)`, `k` Terras steps halve `3x+1` exactly `k` times
  have key : ∀ k, 1 ≤ k → k ≤ v2 (3 * x + 1) → iterT k x = (3 * x + 1) / 2 ^ k := by
    intro k
    induction k with
    | zero => intro h1; omega
    | succ k ih =>
        intro _ hle
        cases k with
        | zero =>
            show iterT 1 x = (3 * x + 1) / 2 ^ 1
            rw [Nat.pow_one]
            show T x = (3 * x + 1) / 2
            exact T_odd (by omega)
        | succ m =>
            have ih' := ih (by omega) (by omega)
            show T (iterT (m + 1) x) = (3 * x + 1) / 2 ^ (m + 1 + 1)
            rw [ih']
            obtain ⟨q, hq⟩ := Nat.dvd_trans
              (Nat.pow_dvd_pow 2 (show m + 1 + 1 ≤ v2 (3 * x + 1) by omega)) hdvd
            have hpow : (2 : Nat) ^ (m + 1 + 1) = 2 ^ (m + 1) * 2 := Nat.pow_succ 2 (m + 1)
            have hq' : 3 * x + 1 = 2 * q * 2 ^ (m + 1) := by
              rw [hq, hpow, Nat.mul_assoc, Nat.mul_comm (2 ^ (m + 1)) (2 * q)]
            have hdiv : (3 * x + 1) / 2 ^ (m + 1) = 2 * q := by
              rw [hq', Nat.mul_div_left _ (Nat.pow_pos (by decide : 0 < 2))]
            rw [hdiv]
            have hpar2 : (2 * q) % 2 = 0 := Nat.mul_mod_right 2 q
            rw [T_even hpar2]
            have halve : 2 * q / 2 = q := by omega
            rw [halve, hq, Nat.mul_comm (2 ^ (m + 1 + 1)) q,
              Nat.mul_div_left _ (Nat.pow_pos (by decide : 0 < 2))]
  have hmain := key (v2 (3 * x + 1)) ha1 (Nat.le_refl _)
  rw [hmain]
  rfl

/-- Iterates of the Syracuse map. -/
def iterS : Nat → Nat → Nat
  | 0, x => x
  | h + 1, x => syracuse (iterS h x)

/-- Syracuse iterates of an odd start stay odd. -/
theorem iterS_odd {x : Nat} (hx : x % 2 = 1) (h : Nat) : iterS h x % 2 = 1 := by
  induction h with
  | zero => exact hx
  | succ h _ => exact syracuse_odd _

/-- The cumulative 2-adic valuation `A_h(x) = a₁ + ⋯ + a_h` along the
Syracuse orbit of `x`. -/
def valA : Nat → Nat → Nat
  | 0, _ => 0
  | h + 1, x => valA h x + v2 (3 * iterS h x + 1)

/-- **Syracuse orbit = Terras orbit at the valuation clock**: `h` accelerated
steps from an odd `x` are exactly `A_h(x)` Terras steps. -/
theorem iterS_eq_iterT {x : Nat} (hx : x % 2 = 1) (h : Nat) :
    iterS h x = iterT (valA h x) x := by
  induction h with
  | zero => rfl
  | succ h ih =>
      show syracuse (iterS h x) = iterT (valA h x + v2 (3 * iterS h x + 1)) x
      calc syracuse (iterS h x)
          = iterT (v2 (3 * iterS h x + 1)) (iterS h x) :=
            syracuse_eq_iterT (iterS_odd hx h)
        _ = iterT (v2 (3 * iterS h x + 1)) (iterT (valA h x) x) := by rw [ih]
        _ = iterT (v2 (3 * iterS h x + 1) + valA h x) x :=
            (CollatzAtlas.Collision.iterT_add _ _ _).symm
        _ = iterT (valA h x + v2 (3 * iterS h x + 1)) x := by rw [Nat.add_comm]

/-! ## 3. The offset `C_h` and the telescoping cocycle -/

/-- The packet's offset recurrence: `C₀ = 0`, `C_{h+1} = 3·C_h + 2^{A_h}`. -/
def corrC : Nat → Nat → Nat
  | 0, _ => 0
  | h + 1, x => 3 * corrC h x + 2 ^ valA h x

/-- **The telescoping cocycle identity** (packet §3, checked by the verifier
on 600 000 instances): `2^{A_h} · S^h(x) = 3^h · x + C_h`.  Proof by
induction on `h`: one step contributes
`2^{A_h}(2^{a}·S(x_h)) = 2^{A_h}(3x_h + 1) = 3(3^h x + C_h) + 2^{A_h}`. -/
theorem cocycle_identity (x h : Nat) :
    2 ^ valA h x * iterS h x = 3 ^ h * x + corrC h x := by
  induction h with
  | zero => rfl
  | succ h ih =>
      have hspec := syracuse_spec (iterS h x)
      show 2 ^ (valA h x + v2 (3 * iterS h x + 1)) * syracuse (iterS h x)
          = 3 ^ (h + 1) * x + (3 * corrC h x + 2 ^ valA h x)
      have e2 : 2 ^ valA h x * (3 * iterS h x + 1)
          = 3 * (2 ^ valA h x * iterS h x) + 2 ^ valA h x := by
        rw [Nat.mul_add, Nat.mul_one, Nat.mul_left_comm]
      have e3 : 3 ^ h * 3 * x = 3 * (3 ^ h * x) :=
        (Nat.mul_assoc _ _ _).trans (Nat.mul_left_comm _ _ _)
      rw [Nat.pow_add, Nat.mul_assoc, hspec, Nat.pow_succ, e2, ih, e3]
      omega

/-- The offset is positive at every positive depth: `C_h ≥ C₁ = 1`. -/
theorem one_le_corrC {x h : Nat} (hh : 1 ≤ h) : 1 ≤ corrC h x := by
  cases h with
  | zero => omega
  | succ k =>
      show 1 ≤ 3 * corrC k x + 2 ^ valA k x
      have hpow : 1 ≤ 2 ^ valA k x := Nat.one_le_pow _ _ (by decide)
      omega

/-- **Lemma 1 (descent requires contraction; Terras's `κ(n) ≤ σ(n)`).**
For every `h ≥ 1`, `S^h(x) < x` implies `3^h < 2^{A_h}`: from the cocycle,
`3^h x + C_h = 2^{A_h} S^h(x)`, and if `2^{A_h} ≤ 3^h` then
`2^{A_h} S^h(x) ≤ 3^h S^h(x) < 3^h x < 3^h x + C_h`, contradiction.  The
packet's oddness hypothesis is not needed and is dropped. -/
theorem descent_requires_contraction {x h : Nat} (hh : 1 ≤ h)
    (hd : iterS h x < x) : 3 ^ h < 2 ^ valA h x := by
  have hid := cocycle_identity x h
  have hC := one_le_corrC hh (x := x)
  by_cases hcon : 3 ^ h < 2 ^ valA h x
  · exact hcon
  · exfalso
    have hcon' : 2 ^ valA h x ≤ 3 ^ h := Nat.le_of_not_lt hcon
    have hmul : 2 ^ valA h x * iterS h x ≤ 3 ^ h * iterS h x :=
      Nat.mul_le_mul_right _ hcon'
    have hpos3 : 0 < 3 ^ h := Nat.pow_pos (by decide)
    have hlt : 3 ^ h * iterS h x < 3 ^ h * x := by
      have e : 3 ^ h * x = 3 ^ h * iterS h x + 3 ^ h * (x - iterS h x) := by
        rw [← Nat.mul_add, Nat.add_sub_cancel' (Nat.le_of_lt hd)]
      have hpos : 0 < 3 ^ h * (x - iterS h x) := Nat.mul_pos hpos3 (by omega)
      omega
    omega

/-- **Lemma 2 (offset bound before onset).**  If no `j < h` is contracting
(`2^{A_j} ≤ 3^j`), then `C_h ≤ h · 3^{h-1}`: each step of the recurrence
`C_{j+1} = 3C_j + 2^{A_j}` adds at most one further power `3^j`. -/
theorem corrC_bound {x : Nat} (h : Nat)
    (hpre : ∀ j, j < h → 2 ^ valA j x ≤ 3 ^ j) : corrC h x ≤ h * 3 ^ (h - 1) := by
  induction h with
  | zero => exact Nat.le_refl _
  | succ k ih =>
      have hpre' : ∀ j, j < k → 2 ^ valA j x ≤ 3 ^ j :=
        fun j hj => hpre j (Nat.lt_trans hj (by omega))
      have hAk : 2 ^ valA k x ≤ 3 ^ k := hpre k (by omega)
      have ih' := ih hpre'
      show 3 * corrC k x + 2 ^ valA k x ≤ (k + 1) * 3 ^ (k + 1 - 1)
      have hk : k + 1 - 1 = k := rfl
      rw [hk]
      cases k with
      | zero =>
          show 3 * 0 + 2 ^ 0 ≤ (0 + 1) * 3 ^ 0
          decide
      | succ m =>
          have h3 : 3 * ((m + 1) * 3 ^ (m + 1 - 1)) = (m + 1) * 3 ^ (m + 1) := by
            have e1 : m + 1 - 1 = m := rfl
            have e2 : 3 ^ (m + 1) = 3 * 3 ^ m := (Nat.pow_succ 3 m).trans (Nat.mul_comm _ _)
            rw [e1, e2, Nat.mul_left_comm]
          have e3 : (m + 1 + 1) * 3 ^ (m + 1) = (m + 1) * 3 ^ (m + 1) + 3 ^ (m + 1) := by
            rw [Nat.add_mul, Nat.one_mul]
          rw [e3]
          omega

/-! ## 4. The minimal exponent `A*(h)` and the onset bound `M(h)` -/

/-- Fuelled search for the least `b ≥ a` with `target < 2^b`.
Invariant: `p2 = 2^a`, and no exponent below `a` works. -/
def aStarFrom (target a p2 : Nat) : Nat → Nat
  | 0 => a
  | fuel + 1 => if target < p2 then a else aStarFrom target (a + 1) (2 * p2) fuel

/-- Specification of the fuelled search: within fuel it finds an exponent that
works, and it is minimal among all exponents that work. -/
theorem aStarFrom_spec (target a p2 fuel : Nat)
    (hp2 : p2 = 2 ^ a) (hlow : ∀ b, b < a → ¬ target < 2 ^ b)
    (hex : ∃ b, a ≤ b ∧ b < a + fuel ∧ target < 2 ^ b) :
    target < 2 ^ aStarFrom target a p2 fuel ∧
    ∀ b, target < 2 ^ b → aStarFrom target a p2 fuel ≤ b := by
  induction fuel generalizing a p2 with
  | zero =>
      exfalso
      obtain ⟨b, hba, hbf, -⟩ := hex
      omega
  | succ fuel ih =>
      show target < 2 ^ (if target < p2 then a else aStarFrom target (a + 1) (2 * p2) fuel) ∧
        ∀ b, target < 2 ^ b →
          (if target < p2 then a else aStarFrom target (a + 1) (2 * p2) fuel) ≤ b
      by_cases htp : target < p2
      · rw [if_pos htp]
        constructor
        · rwa [hp2] at htp
        · intro b hb
          by_cases hba : a ≤ b
          · exact hba
          · exfalso
            exact hlow b (by omega) hb
      · rw [if_neg htp]
        refine ih (a + 1) (2 * p2) ?_ ?_ ?_
        · rw [hp2]
          exact ((Nat.pow_succ 2 a).trans (Nat.mul_comm _ _)).symm
        · intro b hb htb
          rcases (Nat.lt_succ_iff_lt_or_eq).1 hb with hlt | heq
          · exact hlow b hlt htb
          · subst heq
            exact htp (hp2.symm ▸ htb)
        · obtain ⟨b, hba, hbf, htb⟩ := hex
          have hbne : b ≠ a := by
            intro hbeq
            subst hbeq
            exact htp (hp2.symm ▸ htb)
          exact ⟨b, by omega, by omega, htb⟩

/-- An explicit exponent that works: `3^h < 2^{2h+1}` (since `3 < 4`). -/
theorem pow3_lt (h : Nat) : 3 ^ h < 2 ^ (2 * h + 1) := by
  induction h with
  | zero => decide
  | succ k ih =>
      have e1 : 3 ^ (k + 1) = 3 ^ k * 3 := Nat.pow_succ 3 k
      have e2 : 2 ^ (2 * (k + 1) + 1) = 4 * 2 ^ (2 * k + 1) := by
        have hidx : 2 * (k + 1) + 1 = (2 * k + 1) + 2 := by omega
        rw [hidx, Nat.pow_add, show (2 : Nat) ^ 2 = 4 from rfl, Nat.mul_comm]
      rw [e1, e2]
      omega

/-- **`A*(h)`**: the least exponent `A` with `3^h < 2^A`.  This is the
packet's `bit_length(3^h)`, computed here by fuelled search (fuel `2h+2`
suffices by `pow3_lt`). -/
def aStar (h : Nat) : Nat := aStarFrom (3 ^ h) 0 1 (2 * h + 2)

theorem aStar_bundled (h : Nat) :
    3 ^ h < 2 ^ aStar h ∧ ∀ b, 3 ^ h < 2 ^ b → aStar h ≤ b :=
  aStarFrom_spec (3 ^ h) 0 1 (2 * h + 2) rfl
    (fun b hb => absurd hb (Nat.not_lt_zero b))
    ⟨2 * h + 1, Nat.zero_le _, by omega, pow3_lt h⟩

/-- `A*(h)` works: `3^h < 2^{A*(h)}`. -/
theorem aStar_spec (h : Nat) : 3 ^ h < 2 ^ aStar h := (aStar_bundled h).1

/-- `A*(h)` is minimal: any working exponent is at least `A*(h)`. -/
theorem aStar_min (h : Nat) {b : Nat} (hb : 3 ^ h < 2 ^ b) : aStar h ≤ b :=
  (aStar_bundled h).2 b hb

/-- **The onset bound** `M(h) = ⌊ h·3^{h-1} / (2^{A*(h)} − 3^h) ⌋`
(packet §6): one exact integer computation per depth. -/
def M (h : Nat) : Nat := h * 3 ^ (h - 1) / (2 ^ aStar h - 3 ^ h)

/-- Trivial arithmetic bound: dividing by `2^{A*(h)} − 3^h ≥ 1` only shrinks
the numerator. -/
theorem M_le (h : Nat) : M h ≤ h * 3 ^ (h - 1) := Nat.div_le_self _ _

/-- **Theorem (the onset bound; Terras's method).**  Let `h` be the *first*
contracting index of `x` and suppose `S^h(x) ≥ x`.  Then `x ≤ M(h)`.

(The memo's standing assumption `h ≥ 1` is not a hypothesis: `h = 0` is never
contracting, since `3^0 = 1 = 2^{A_0}`, so `hcontr` already forces `h ≥ 1`.)

Proof, following the memo: `S^h(x) ≥ x` and the cocycle give
`x(2^{A_h} − 3^h) ≤ C_h`; Lemma 2 applies because `h` is the first
contracting index, so `C_h ≤ h·3^{h-1}`; and `A_h ≥ A*(h)` by minimality of
`A*`, so `2^{A_h} − 3^h ≥ 2^{A*(h)} − 3^h > 0`. -/
theorem onset_bound {x h : Nat}
    (hfirst : ∀ j, j < h → 2 ^ valA j x ≤ 3 ^ j)
    (hcontr : 3 ^ h < 2 ^ valA h x)
    (hnd : x ≤ iterS h x) :
    x ≤ M h := by
  have hid := cocycle_identity x h
  have hC := corrC_bound h hfirst
  have hA : aStar h ≤ valA h x := aStar_min h hcontr
  have hspec := aStar_spec h
  have h2le : 2 ^ aStar h ≤ 2 ^ valA h x := Nat.pow_le_pow_right (by decide) hA
  have hstep : x * (2 ^ valA h x - 3 ^ h) ≤ corrC h x := by
    have h1 : 2 ^ valA h x * x ≤ 2 ^ valA h x * iterS h x :=
      Nat.mul_le_mul_left _ hnd
    have e : x * (2 ^ valA h x - 3 ^ h) = x * 2 ^ valA h x - x * 3 ^ h :=
      Nat.mul_sub_left_distrib _ _ _
    have h2 : x * 2 ^ valA h x = 2 ^ valA h x * x := Nat.mul_comm _ _
    have h3 : x * 3 ^ h = 3 ^ h * x := Nat.mul_comm _ _
    omega
  have hdst : 0 < 2 ^ aStar h - 3 ^ h := by omega
  have hle : x * (2 ^ aStar h - 3 ^ h) ≤ h * 3 ^ (h - 1) := by
    have hsub : 2 ^ aStar h - 3 ^ h ≤ 2 ^ valA h x - 3 ^ h :=
      Nat.sub_le_sub_right h2le _
    have h1 : x * (2 ^ aStar h - 3 ^ h) ≤ x * (2 ^ valA h x - 3 ^ h) :=
      Nat.mul_le_mul_left _ hsub
    omega
  show x ≤ (h * 3 ^ (h - 1)) / (2 ^ aStar h - 3 ^ h)
  exact (Nat.le_div_iff_mul_le hdst).2 hle

/-- **Corollary skeleton (packet §7), with the computed window bound left as
a hypothesis.**  If `x` never descends below itself at any accelerated depth
`1 ≤ j ≤ H`, and `M(j) < x` throughout that window, then no index in the
window is contracting for `x`.  (Instantiate the `M` hypothesis with the
packet's computed `max_{h ≤ 10^6} M(h) = 984 572 779 224` and read `x` as a
minimal counterexample: Bařina's `2^71` verification — external to this
file — then rules out every contracting prefix of depth `≤ 10^6`, which is
the packet's Corollary.) -/
theorem no_contracting_in_window {x H : Nat}
    (hnd : ∀ j, 1 ≤ j → j ≤ H → x ≤ iterS j x)
    (hM : ∀ j, 1 ≤ j → j ≤ H → M j < x)
    (j : Nat) (hj1 : 1 ≤ j) (hjH : j ≤ H) :
    ¬ 3 ^ j < 2 ^ valA j x := by
  revert hj1 hjH
  refine Nat.strongRecOn
    (motive := fun j => 1 ≤ j → j ≤ H → ¬ 3 ^ j < 2 ^ valA j x) j ?_
  intro j ih hj1 hjH hconj
  have hfirst : ∀ k, k < j → 2 ^ valA k x ≤ 3 ^ k := by
    intro k hkj
    cases k with
    | zero =>
        show (2 : Nat) ^ 0 ≤ 3 ^ 0
        decide
    | succ k =>
        by_cases hle : 2 ^ valA (k + 1) x ≤ 3 ^ (k + 1)
        · exact hle
        · have hlt : 3 ^ (k + 1) < 2 ^ valA (k + 1) x := Nat.lt_of_not_ge hle
          exact absurd hlt (ih (k + 1) hkj (by omega) (by omega))
  have hb := onset_bound hfirst hconj (hnd j hj1 hjH)
  have hMlt := hM j hj1 hjH
  omega

end CollatzAtlas.ContractionOnset

/-! ## Sanity checks (all closed by `decide`) -/

namespace CollatzAtlas.ContractionOnset

open Terras

-- the valuation and one Syracuse step
example : v2 40 = 3 ∧ syracuse 13 = 5 ∧ syracuse 27 = 41 := by decide

-- one Syracuse step is `v₂(3x+1)` Terras steps (named values)
example : syracuse 7 = iterT (v2 (3 * 7 + 1)) 7 := by decide
example : syracuse 27 = iterT (v2 (3 * 27 + 1)) 27 := by decide

-- the cocycle on a concrete orbit segment: `x = 27`, `h = 6`
example : 2 ^ valA 6 27 * iterS 6 27 = 3 ^ 6 * 27 + corrC 6 27 := by decide

-- named controls from the packet (§8): `x = 3` descends and contracts at
-- `h = 2`; `x = 7` at `h = 4`; earlier indices are not contracting
example : iterS 2 3 < 3 ∧ 3 ^ 2 < 2 ^ valA 2 3
    ∧ 2 ^ valA 0 3 ≤ 3 ^ 0 ∧ 2 ^ valA 1 3 ≤ 3 ^ 1 := by decide
example : iterS 4 7 < 7 ∧ 3 ^ 4 < 2 ^ valA 4 7
    ∧ 2 ^ valA 1 7 ≤ 3 ^ 1 ∧ 2 ^ valA 2 7 ≤ 3 ^ 2 ∧ 2 ^ valA 3 7 ≤ 3 ^ 3 := by decide

-- the packet's `A*(h)` table (§6), pinned exactly
set_option exponentiation.threshold 2048 in
set_option maxRecDepth 1000000 in
example : aStar 5 = 8 ∧ aStar 41 = 65 ∧ aStar 53 = 85
    ∧ aStar 306 = 485 ∧ aStar 665 = 1055 := by decide

-- the packet's `M(h)` table (§6), pinned exactly
set_option exponentiation.threshold 2048 in
set_option maxRecDepth 1000000 in
example : M 5 = 31 ∧ M 41 = 1185 ∧ M 53 = 17
    ∧ M 306 = 99729 ∧ M 665 = 221 := by decide

-- deeper rows of the same table (`M(9616) + 1` is exactly the packet's
-- verifier scan bound `7 795 715`)
set_option exponentiation.threshold 32768 in
set_option maxRecDepth 1000000 in
set_option maxHeartbeats 4000000 in
example : aStar 9616 = 15241 ∧ M 9616 = 7795714 := by decide
set_option exponentiation.threshold 32768 in
set_option maxRecDepth 1000000 in
set_option maxHeartbeats 4000000 in
example : aStar 15601 = 24727 ∧ M 15601 = 285814986 := by decide

end CollatzAtlas.ContractionOnset

-- Axiom audit: must not list `sorryAx`.
#print axioms CollatzAtlas.ContractionOnset.cocycle_identity
#print axioms CollatzAtlas.ContractionOnset.descent_requires_contraction
#print axioms CollatzAtlas.ContractionOnset.corrC_bound
#print axioms CollatzAtlas.ContractionOnset.syracuse_eq_iterT
#print axioms CollatzAtlas.ContractionOnset.iterS_eq_iterT
#print axioms CollatzAtlas.ContractionOnset.onset_bound
#print axioms CollatzAtlas.ContractionOnset.no_contracting_in_window
