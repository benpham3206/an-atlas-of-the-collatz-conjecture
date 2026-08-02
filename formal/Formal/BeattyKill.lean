/-
Collatz atlas — formal certificates.

# The Beatty kill triple for the chain-exponent law

*Reference:* Collatz atlas, `contribution/packets/2026-08-01-chain-exponent-law/`
(`COLLATZ_CHAIN_EXPONENT_LAW.md`, §2–§4, and `verify_chain_exponent_law.py`).
The certified input is the exact exponent table `k(n)`, `n = 6, …, 21`:

  `k = 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 26, 28`

assembled from three predecessor certificates (deep-fourier `n = 6..17`,
plateau-drift `n = 6..20`, streaming `n = 21`) and cross-checked exactly on the
overlap.  This module machine-checks the three pre-registered kill tests whose
content is exact integer arithmetic:

1. **Beatty/LP infeasibility (memo §2, kill criterion (a)).**  No rational
   slope `γ` — with *any* phase — satisfies `k(n) ≤ γ·n + φ < k(n) + 1` over
   the whole table.  The memo's phase elimination leaves the pairwise condition
   `k_i − γ·i < k_j + 1 − γ·j` on `γ` alone, and two witness pairs already
   contradict: `(k(21), k(15)) = (28, 18)` forces `γ > 3/2` while
   `(k(7), k(15)) = (8, 18)` forces `γ < 11/8`, and `3/2 = 12/8 > 11/8`.
2. **Sturmian balance failure (memo §3, kill criterion (b)).**  The jump word
   `Δk = (2,1,1,2,1,1,2,1,1,2,1,2,1,2,2)` is two-valued but not balanced: it
   contains the length-2 factors `(1,1)` (sum 2, at offset 1) and `(2,2)`
   (sum 4, at offset 13), an imbalance of 2 — and 2 is the *maximal* imbalance
   over all factor pairs.  A general lemma shows any word containing both
   double factors `(x,x)` and `(y,y)` with `x ≠ y` is unbalanced; a Beatty
   difference word would be balanced, so this is an independent kill.
3. **CF of `log₂ 3` (memo §4).**  The continued fraction of `log₂ 3` begins
   `[1; 1, 1, 2, 2, 3, 1, 5, 2, 23]`, certified by exact `Nat` exponent
   comparisons only (see below).

## Scope notes (mathlib-free setting)

Plain Lean 4 core has no `Rat`-valued floors, no reals, and no logarithms, so
the statements are re-phrased in exact integer form; each is a definitional
specialisation of the memo's statement:

| memo statement                              | here (Lean 4 core)                              |
|---------------------------------------------|-------------------------------------------------|
| `γ : ℚ`                                     | `N / D` with `N : Int`, `D : Nat`, `0 < D`      |
| `k(n) ≤ γ·n + φ < k(n)+1`                   | cross-multiplied `Int` inequalities over `N,D,A`|
| phase `φ : ℚ`                               | `A / D` over the *common* denominator (w.l.o.g.)|
| `p/q < log₂ 3 < p'/q'`                      | `2^p < 3^q ∧ 3^q' < 2^p'` (see `Encloses`)      |

On the phase: any two rationals `γ, φ` can be written over a common positive
denominator `D`, so `beatty_infeasible_with_phase` is the full rational
statement.  For a *real* phase the same kill goes through: subtracting the two
margin-1 constraints at `i` and `j` eliminates `φ` and yields the pairwise
condition on `γ` alone, which `beatty_pairwise_infeasible` refutes using only
the memo's two witness pairs — so no phase of any kind can rescue any rational
slope.  (A real *slope* cannot be stated here at all; the memo's LP is over
`ℚ`-data, and the pairwise contradiction is a statement about the table, not
about the slope's number system.)

On the CF: `log₂` is strictly increasing, so for `q, q' > 0`,

  `p/q < log₂ 3  ⟺  p < log₂ (3^q)  ⟺  2^p < 3^q`,
  `log₂ 3 < p'/q'  ⟺  3^q' < 2^p'`.

The enclosure `Encloses p q p' q'` is therefore exactly `p/q < log₂ 3 < p'/q'`,
stated without reals.  Between consecutive convergents `c_j, c_{j+1}` of the
candidate CF, every irrational has a CF agreeing with the shared prefix; the
nine convergent brackets (`Log2ThreeEnclosures.enc0`–`enc8`) pin `log₂ 3`
inside each successive cylinder, forcing the prefix `[1; 1,1,2,2,3,1,5,2]` and
`a₉ ≥ 23`, and the semiconvergent bracket `encSemi` (against the intermediate
fraction `(24·p₈+p₇)/(24·q₈+q₇) = 25781/16266`) forces `a₉ < 24`, hence
`a₉ = 23` exactly.  This determination argument is classical CF theory and is
documented here in comments; what is *proved* is the exact `Nat` arithmetic —
the nine convergent enclosures plus the semiconvergent refinement, and the
exact convergent computation `log2Three_convergents`.

No `sorry`, no floats: every step is exact `Nat`/`Int` arithmetic checked by
the Lean kernel (`by decide` for the finite decidable checks, `omega` for the
cross-multiplied linear integer arithmetic).
-/

namespace BeattyKill

/-! ## The certified table -/

/-- The certified chain exponent `k(n)` for `n = 6, …, 21` (exact BSGS discrete
logs of the peak Fourier frequency of the Syracuse distribution at layer `n`;
value `0` outside the certified window is a dummy). -/
def chainK : Nat → Nat
  | 6 => 6 | 7 => 8 | 8 => 9 | 9 => 10 | 10 => 12 | 11 => 13 | 12 => 14
  | 13 => 16 | 14 => 17 | 15 => 18 | 16 => 20 | 17 => 21 | 18 => 23 | 19 => 24
  | 20 => 26 | 21 => 28 | _ => 0

/-- The certified window `n = 6, …, 21`. -/
def chainNs : List Nat :=
  [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

/-- The jump word `Δk` of the memo, length 15: `Δk[t] = k(n_{t+1}) − k(n_t)`. -/
def deltaK : List Nat := [2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2]

/-- Sanity: the table really is the certified one (memo §1). -/
theorem chainK_certified : chainNs.map chainK =
    [6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 26, 28] := by decide

/-- Sanity: `deltaK` really is the gap word of the certified table. -/
theorem deltaK_eq_table_gaps :
    (chainNs.zip chainNs.tail).map (fun p => chainK p.2 - chainK p.1) = deltaK := by
  decide

/-! ## Test 1 — Beatty/LP infeasibility (kill criterion (a)) -/

/-- **Phase-free core, full 16-constraint infeasibility.**  There is no
rational slope `γ = N/D` (`D > 0`) with `k(n) ≤ γ·n < k(n) + 1` at every
certified layer.  Two constraints already contradict: `n = 21` gives
`28·D ≤ 21·N` (i.e. `γ ≥ 4/3`) and `n = 15` gives `15·N < 19·D`
(i.e. `γ < 19/15`), but `4/3 = 20/15 > 19/15`.  The remaining fourteen
constraints are irrelevant — the strengthened statement comes free. -/
theorem beatty_phase_free_infeasible (N : Int) (D : Nat) (hD : 0 < D)
    (h : ∀ n ∈ chainNs, (chainK n : Int) * (D : Int) ≤ N * (n : Int) ∧
        N * (n : Int) < ((chainK n : Int) + 1) * (D : Int)) : False := by
  obtain ⟨h21, -⟩ := h 21 (by decide)
  obtain ⟨-, h15⟩ := h 15 (by decide)
  have e21 : chainK 21 = 28 := by decide
  have e15 : chainK 15 = 18 := by decide
  rw [e21] at h21; rw [e15] at h15
  omega

/-- The memo's lower witness (pair `(k(21), k(15)) = (28, 18)`): the pairwise
phase-eliminated condition at `(i, j) = (21, 15)` forces `γ > 3/2`. -/
theorem gamma_gt_three_halves_of_pair (N : Int) (D : Nat) (_hD : 0 < D)
    (h : N * ((15 : Int) - 21) <
        (((chainK 15 : Int) + 1) - (chainK 21 : Int)) * (D : Int)) :
    3 * (D : Int) < 2 * N := by
  have e21 : chainK 21 = 28 := by decide
  have e15 : chainK 15 = 18 := by decide
  rw [e21, e15] at h
  omega

/-- The memo's upper witness (pair `(k(7), k(15)) = (8, 18)`): the pairwise
phase-eliminated condition at `(i, j) = (7, 15)` forces `γ < 11/8`. -/
theorem gamma_lt_eleven_eighths_of_pair (N : Int) (D : Nat) (_hD : 0 < D)
    (h : N * ((15 : Int) - 7) <
        (((chainK 15 : Int) + 1) - (chainK 7 : Int)) * (D : Int)) :
    8 * N < 11 * (D : Int) := by
  have e7 : chainK 7 = 8 := by decide
  have e15 : chainK 15 = 18 := by decide
  rw [e7, e15] at h
  omega

/-- **Pairwise (phase-eliminated) infeasibility, memo §2 verbatim.**  Beatty
feasibility with some phase is equivalent to
`max_i (k_i − γ·i) < min_j (k_j + 1 − γ·j)`, i.e. to the `16 × 15` pairwise
conditions `N·(j − i) < (k_j + 1 − k_i)·D`.  All of them together are
infeasible: the two memo witnesses give `γ > 3/2` and `γ < 11/8`, and
`3/2 > 11/8`.  Since any real phase would satisfy the same pairwise conditions
on `γ` (subtract the margin-1 constraints), this kills every phase at once. -/
theorem beatty_pairwise_infeasible (N : Int) (D : Nat) (hD : 0 < D)
    (h : ∀ i ∈ chainNs, ∀ j ∈ chainNs, N * ((j : Int) - (i : Int)) <
        (((chainK j : Int) + 1) - (chainK i : Int)) * (D : Int)) : False := by
  have w1 : 3 * (D : Int) < 2 * N :=
    gamma_gt_three_halves_of_pair N D hD (h 21 (by decide) 15 (by decide))
  have w2 : 8 * N < 11 * (D : Int) :=
    gamma_lt_eleven_eighths_of_pair N D hD (h 7 (by decide) 15 (by decide))
  omega

/-- **Full infeasibility with a phase.**  No rational slope `γ = N/D` and no
rational phase `φ = A/D` (common denominator, w.l.o.g.) satisfy the margin-1
Beatty condition `k(n) ≤ γ·n + φ < k(n) + 1` at all sixteen certified layers.
The phase cancels between layers `21` and `15` (giving `9·D < 6·N`) and
between `7` and `15` (giving `8·N < 11·D`); chaining yields `36·D < 33·D`. -/
theorem beatty_infeasible_with_phase (N A : Int) (D : Nat) (hD : 0 < D)
    (h : ∀ n ∈ chainNs, (chainK n : Int) * (D : Int) ≤ N * (n : Int) + A ∧
        N * (n : Int) + A < ((chainK n : Int) + 1) * (D : Int)) : False := by
  obtain ⟨h21, -⟩ := h 21 (by decide)
  obtain ⟨-, h15⟩ := h 15 (by decide)
  obtain ⟨h7, -⟩ := h 7 (by decide)
  have e21 : chainK 21 = 28 := by decide
  have e15 : chainK 15 = 18 := by decide
  have e7 : chainK 7 = 8 := by decide
  rw [e21] at h21; rw [e15] at h15; rw [e7] at h7
  omega

/-! ## Test 2 — Sturmian balance failure (kill criterion (b)) -/

/-- Sum of the length-`ℓ` contiguous factor of `w` starting at offset `s`
(shorter than `ℓ` if the factor runs off the end of the word). -/
def factorSum (w : List Nat) (s ℓ : Nat) : Nat := ((w.drop s).take ℓ).sum

/-- A word is *balanced* if any two contiguous factors of the same length have
sums differing by at most `1`.  For a two-valued word this is the Sturmian /
mechanical-word balance property; every Beatty difference word is balanced. -/
def Balanced (w : List Nat) : Prop :=
  ∀ ℓ s t : Nat, s + ℓ ≤ w.length → t + ℓ ≤ w.length →
    factorSum w s ℓ ≤ factorSum w t ℓ + 1 ∧ factorSum w t ℓ ≤ factorSum w s ℓ + 1

/-- Two length-`ℓ` factors whose sums differ by at least `2` destroy balance.
This is the contrapositive form used by every unbalance witness below. -/
theorem not_balanced_of_factorSum_gap (w : List Nat) (ℓ s t : Nat)
    (hs : s + ℓ ≤ w.length) (ht : t + ℓ ≤ w.length)
    (hgap : factorSum w s ℓ + 2 ≤ factorSum w t ℓ) : ¬ Balanced w := by
  intro hb
  have h := (hb ℓ s t hs ht).2
  omega

/-- A length-2 factor listed explicitly has the listed sum. -/
theorem sum_take_two (w : List Nat) (s x y : Nat)
    (h : (w.drop s).take 2 = [x, y]) : factorSum w s 2 = x + y := by
  unfold factorSum
  rw [h, List.sum_cons, List.sum_cons, List.sum_nil, Nat.add_zero]

/-- **General lemma.**  A word containing both double factors `(x,x)` and
`(y,y)` with `x ≠ y` is not balanced: the two factors have sums `2x` and `2y`,
differing by at least `2`.  In particular no balanced two-valued word
(e.g. no Sturmian or Beatty difference word) can contain both `(1,1)` and
`(2,2)`. -/
theorem not_balanced_of_double_factors (w : List Nat) (s t x y : Nat)
    (hs : s + 2 ≤ w.length) (ht : t + 2 ≤ w.length)
    (hx : (w.drop s).take 2 = [x, x]) (hy : (w.drop t).take 2 = [y, y])
    (hxy : x < y) : ¬ Balanced w :=
  not_balanced_of_factorSum_gap w 2 s t hs ht (by
    rw [sum_take_two w s x x hx, sum_take_two w t y y hy]
    omega)

/-- The factor `(1,1)` occurs in `Δk` at offset 1 (memo: "first at `n = 7`"). -/
theorem deltaK_factor_11 : (deltaK.drop 1).take 2 = [1, 1] := by decide

/-- The factor `(2,2)` occurs in `Δk` at offset 13 (memo: "at `n = 20`"). -/
theorem deltaK_factor_22 : (deltaK.drop 13).take 2 = [2, 2] := by decide

/-- The specific finite witness: sums 2 and 4 at factor length 2, an imbalance
of exactly 2.  Pure finite check, closed by `decide`. -/
theorem deltaK_imbalance_witness :
    factorSum deltaK 1 2 + 2 = factorSum deltaK 13 2 := by decide

/-- **`Δk` is not balanced — specific finite check.**  Exhibiting the pair of
length-2 factors directly and evaluating by `decide`. -/
theorem deltaK_not_balanced_direct : ¬ Balanced deltaK := by
  intro hb
  exact absurd (hb 2 1 13 (by decide) (by decide)).2 (by decide)

/-- **`Δk` is not balanced — via the general double-factor lemma.** -/
theorem deltaK_not_balanced : ¬ Balanced deltaK :=
  not_balanced_of_double_factors deltaK 1 13 1 2
    (by decide) (by decide) deltaK_factor_11 deltaK_factor_22 (by decide)

/-- One direction of the maximal-imbalance bound (finite check over
`ℓ, s, t < 16`, closed by `decide`). -/
theorem deltaK_imbalance_le_two :
    ∀ ℓ : Nat, ℓ < 16 → ∀ s : Nat, s < 16 → ∀ t : Nat, t < 16 →
      s + ℓ ≤ 15 → t + ℓ ≤ 15 →
      factorSum deltaK s ℓ ≤ factorSum deltaK t ℓ + 2 := by decide

/-- **The maximal imbalance of `Δk` is exactly 2** (memo §3: "the maximal
imbalance over all factor pairs, all 120 pairs enumerated exactly").  The first
conjunct bounds every valid factor pair (via `deltaK_imbalance_le_two`, applied
in both directions); the second exhibits a pair attaining 2. -/
theorem deltaK_max_imbalance_is_two :
    (∀ ℓ : Nat, ℓ < 16 → ∀ s : Nat, s < 16 → ∀ t : Nat, t < 16 →
        s + ℓ ≤ 15 → t + ℓ ≤ 15 →
        factorSum deltaK s ℓ ≤ factorSum deltaK t ℓ + 2 ∧
        factorSum deltaK t ℓ ≤ factorSum deltaK s ℓ + 2) ∧
    factorSum deltaK 1 2 + 2 = factorSum deltaK 13 2 :=
  ⟨fun ℓ hℓ s hs t ht h1 h2 =>
      ⟨deltaK_imbalance_le_two ℓ hℓ s hs t ht h1 h2,
       deltaK_imbalance_le_two ℓ hℓ t ht s hs h2 h1⟩,
   deltaK_imbalance_witness⟩

/-! ## Test 3 — the CF of `log₂ 3` by exact exponent comparisons -/

/-- `Encloses p q p' q'` is the exact-integer form of the enclosure
`p/q < log₂ 3 < p'/q'` (for `q, q' > 0`): monotonicity of `log₂` turns each
rational comparison into one `Nat` exponent comparison.  This project has no
reals, so this *is* the formal statement of the enclosure; see the header.
(`abbrev` so that `decide` can see through it to the decidable `Nat`
comparisons.) -/
abbrev Encloses (p q p' q' : Nat) : Prop := 2 ^ p < 3 ^ q ∧ 3 ^ q' < 2 ^ p'

/-- The first ten partial quotients of `log₂ 3` (memo §4):
`[1; 1, 1, 2, 2, 3, 1, 5, 2, 23]`. -/
def log2ThreeCFPrefix : List Nat := [1, 1, 1, 2, 2, 3, 1, 5, 2, 23]

/-- The convergents `(p, q)` of a continued-fraction prefix, computed by the
exact recurrence `pₖ = aₖ·pₖ₋₁ + pₖ₋₂`, `qₖ = aₖ·qₖ₋₁ + qₖ₋₂`. -/
def cfConvergents (cf : List Nat) : List (Nat × Nat) :=
  loop cf 0 1 1 0
where
  loop : List Nat → Nat → Nat → Nat → Nat → List (Nat × Nat)
    | [], _, _, _, _ => []
    | a :: rest, pm2, pm1, qm2, qm1 =>
        let p := a * pm1 + pm2
        let q := a * qm1 + qm2
        (p, q) :: loop rest pm1 p qm1 q

/-- The convergents of the prefix are exactly
`1, 2, 3/2, 8/5, 19/12, 65/41, 84/53, 485/306, 1054/665, 24727/15601`
(the memo lists the first eight; the last two pin `a₈ = 2` and `a₉ = 23`). -/
theorem log2Three_convergents :
    cfConvergents log2ThreeCFPrefix =
      [(1, 1), (2, 1), (3, 2), (8, 5), (19, 12), (65, 41), (84, 53),
       (485, 306), (1054, 665), (24727, 15601)] := by decide

/-- **The enclosure certificate.**  The nine convergent brackets of memo §4
(each between consecutive convergents `c_j, c_{j+1}`), plus the semiconvergent
refinement against `25781/16266 = (24·p₈ + p₇)/(24·q₈ + q₇)`.  Classical CF
cylinder theory (documented in the header) turns these ten exact enclosures
into the statement that the CF of `log₂ 3` begins `[1; 1,1,2,2,3,1,5,2,23]`
*exactly* — not merely up to `a₉ ≥ 23`. -/
structure Log2ThreeEnclosures : Prop where
  /-- `1/1 < log₂ 3 < 2/1`: the cylinder of prefix `[1]`. -/
  enc0 : Encloses 1 1 2 1
  /-- `3/2 < log₂ 3 < 2/1`: the cylinder of prefix `[1; 1]`. -/
  enc1 : Encloses 3 2 2 1
  /-- `3/2 < log₂ 3 < 8/5`: the cylinder of prefix `[1; 1, 1]`. -/
  enc2 : Encloses 3 2 8 5
  /-- `19/12 < log₂ 3 < 8/5`: the cylinder of prefix `[1; 1, 1, 2]`. -/
  enc3 : Encloses 19 12 8 5
  /-- `19/12 < log₂ 3 < 65/41`: the cylinder of prefix `[1; 1, 1, 2, 2]`. -/
  enc4 : Encloses 19 12 65 41
  /-- `84/53 < log₂ 3 < 65/41`: the cylinder of prefix `[1; 1, 1, 2, 2, 3]`. -/
  enc5 : Encloses 84 53 65 41
  /-- `84/53 < log₂ 3 < 485/306`: prefix `[1; 1, 1, 2, 2, 3, 1]`. -/
  enc6 : Encloses 84 53 485 306
  /-- `1054/665 < log₂ 3 < 485/306`: prefix `[1; 1, 1, 2, 2, 3, 1, 5]`. -/
  enc7 : Encloses 1054 665 485 306
  /-- `1054/665 < log₂ 3 < 24727/15601`: prefix `[1; 1,1,2,2,3,1,5,2]`,
  `a₉ ≥ 23`. -/
  enc8 : Encloses 1054 665 24727 15601
  /-- `25781/16266 < log₂ 3 < 24727/15601`: semiconvergent refinement forcing
  `a₉ < 24`, hence `a₉ = 23` exactly. -/
  encSemi : Encloses 25781 16266 24727 15601

set_option exponentiation.threshold 30000 in
set_option exponentiation.threshold 30000 in
/-- **The CF of `log₂ 3` begins `[1; 1, 1, 2, 2, 3, 1, 5, 2, 23]`** — proved as
exact `Nat` exponent comparisons.  Every field is a finite decidable check
closed by `decide`; the largest (`encSemi`) compares `2^25781` with `3^16266`
and `3^15601` with `2^24727`, about 7,800 decimal digits, evaluated by the
kernel's accelerated `Nat` arithmetic (no `Lean.ofReduceBool` anywhere in this
module).  The `exponentiation.threshold` option only lifts the elaborator's
evaluation guard so that `decide` is willing to evaluate the large `Nat.pow`s;
the proof is still kernel-checked `decide`. -/
theorem log2Three_cf_certified : Log2ThreeEnclosures where
  enc0 := by decide
  enc1 := by decide
  enc2 := by decide
  enc3 := by decide
  enc4 := by decide
  enc5 := by decide
  enc6 := by decide
  enc7 := by decide
  enc8 := by decide
  encSemi := by decide

end BeattyKill

#print axioms BeattyKill.beatty_phase_free_infeasible
#print axioms BeattyKill.beatty_pairwise_infeasible
#print axioms BeattyKill.beatty_infeasible_with_phase
#print axioms BeattyKill.deltaK_not_balanced
#print axioms BeattyKill.deltaK_max_imbalance_is_two
#print axioms BeattyKill.log2Three_convergents
#print axioms BeattyKill.log2Three_cf_certified
