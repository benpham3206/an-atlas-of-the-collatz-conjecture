/-!
# Cycle exclusion — verified-checker architecture for the exact valuation-word search

**Source.** `contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` (the fence doc,
m ≤ 18) and `contribution/packets/2026-07-23-cycle-exclusion-extension/`
(extension to **m ≤ 20**). The external exact pipeline enumerates every ordered
positive valuation word in the exact window `3^m < 2^K ≤ (22/7)^m` and applies
an affine/divisibility gate to each word (≈ 6.20×10^8 words per phase at the
extension frontier, with an independent dual-enumerator cross-check). Verdict of
the packet: *there is no nontrivial positive Collatz cycle with at most 20 odd
members.* That scan cannot run inside the Lean kernel, so this file formalizes
the **verified-checker architecture** instead:

1. **The cycle equation.** For the odd-only map `U(n) = (3n+1)/2^{v2(3n+1)}`,
   a positive odd cycle of `m` states realizing the valuation word
   `a = (a_0, …, a_{m-1})` with total valuation `K = Σ a_i` satisfies the exact
   Diophantine identity

       n · 2^K = 3^m · n + C_m,      C_m = Σ_j 3^{m-1-j} · 2^{a_0 + … + a_{j-1}},

   i.e. `n · (2^K − 3^m) = C_m` whenever `2^K > 3^m`. This is the packet's
   equation (`U^m(n) = (3^m·n + C_m)/2^K`, fixed point `n = C_m/(2^K − 3^m)`).
   `cycle_equation` below proves it from the definition of the word dynamics by
   induction over the word, and `realizes_iterU` shows the word dynamics is
   exactly the iterate of `U` (via the 2-adic valuation `v2`).

2. **The verified exclusion checker.** `valuationWordExcluded : List Nat → Bool`
   is the exact negation of the external verifier's per-word fixed-point gate
   (`try_integral_fixed_point` in `contribution/code/fence/exact_cycle_search.py`):
   `2^K > 3^m`, exact divisibility `C_m % (2^K − 3^m) = 0`, odd quotient
   (quotient positivity is automatic for nonempty words since `C_m ≥ 1`).
   `valuationWordExcluded_sound` proves: if the checker returns `true`, no
   positive odd integer solves the cycle equation for that word, and
   `no_cycle_of_excluded` concludes that no positive odd `U`-cycle realizes the
   word. The checker is sound for **every** word, of any length, with any
   entries (including zeros — a stronger domain than the verifier's
   positive-composition enumeration).

3. **Kernel-checked layers.** `kernel_layer_m1/m2/m3/m4` run the checker
   *inside the Lean kernel* (by `decide`) on every word of length 1–4 with
   entries in `[1, 32]`, `[1, 16]`, `[1, 8]`, `[1, 8]` respectively: every
   word is excluded except the constant word `[2, …, 2]`, which is the
   valuation word of the *trivial* cycle `{1}` at every length (`U 1 = 1`,
   `v2(3·1+1) = 2`) and is exactly the external pipeline's `(1, 2)` control
   (`exact_cycle_search_results.json`). These are the first fully
   machine-verified exclusion layers of the atlas. Wall-clock measurements and
   the in-kernel feasibility boundary (m = 5 with 3×10⁴ words hits the
   elaborator heartbeat limit) are recorded in the §5 comment block.

4. **Depth m ≤ 20 is external, by design.** The exclusion
   "no nontrivial positive cycle with at most 20 odd members" is established by
   the external exact pipeline of packet `2026-07-23-cycle-exclusion-extension`
   (dual independent enumerators, per-pair word counts matching
   `binom(K−1, m−1)` exactly, closed-form audit `C_m = Σ_j 3^{m−1−j} 2^{S_j}`,
   regression against the fence results; 619,545,781 words per phase,
   zero divisibility hits beyond the trivial control). The Lean checker here is
   **sound but not yet run at that depth**: it is the kernel-side half of a
   future certificate-import architecture in which the external enumerator
   emits the word list and the kernel rechecks each `valuationWordExcluded`
   verdict. Nothing in this file claims the m ≤ 20 result; only the layers
   proved by `decide` below are kernel-verified.

**Proof sketch (cycle equation).** `affGo_spec` computes the packet's affine
recurrence (`C ↦ 3C + 2^S`, `S ↦ S + a`) in closed form:
`affGo as c s = (3^|as|·c + 2^s·affC as, s + valSum as)`, by induction on the
word. `wordIter_affine` then lifts one step `n ↦ (3n+1)/2^a` to the whole word:
exactness of each division gives `n'·2^a = 3n+1`, so induction yields
`wordIter a n · 2^K = 3^m·n + affC a`; imposing the return condition
`wordIter a n = n` gives `cycle_equation`. The connection to the real map is
`wordStep_eq_U`: a prescribed exponent is the exact valuation
(`2^a ∣ 3n+1` with odd quotient) iff it equals `v2 (3n+1)` (`v2_unique`), so a
realized word is precisely a `U`-orbit segment (`wordIter_eq_iterU`).

**Sanity checks.** `U` values on `1, 3, 5, 7`, the trivial-cycle words
`[2]`, `[2, 2]` are *not* excluded (matching the external control), `[]`,
`[1]` are excluded, and `affC`/`valSum` spot values are pinned by `decide`.
`#print axioms` audits the main theorems at the end.

**Exactness note.** All arithmetic is exact `Nat` arithmetic; there are no
floats anywhere in this file, matching the verifier's "no floats in decisions"
policy.

**Verification.** From the `formal/` directory:
`~/.elan/bin/lean Formal/CycleExclusion.lean`  (Lean v4.31.0 via elan).
This file has no imports; it compiles standalone.

**Counterexample watch.** This file *is* the counterexample watch on the cycle
branch: an excluded word provably cannot be realized by any positive odd cycle.
The kernel-verified layers found no excluded-`false` word other than the
trivial-cycle words `[2, …, 2]` — consistent with the external pipeline's zero
nontrivial divisibility hits. No anomaly observed.
-/

namespace CycleExclusion

/-! ## 1. The 2-adic valuation and the odd-only map -/

/-- Fuel-bounded 2-adic valuation: structural recursion, hence kernel-reducible
(`v2Fuel fuel n` is exact whenever `n ≤ fuel`, because each step at least
halves the input). Only positive even inputs recurse. -/
def v2Fuel : Nat → Nat → Nat
  | 0, _ => 0
  | fuel + 1, n => if n % 2 = 0 ∧ 0 < n then 1 + v2Fuel fuel (n / 2) else 0

/-- The 2-adic valuation `v2 n`: the exact count of factors of 2 in `n`
(`v2 0 = 0` by convention; only positive inputs are used below). -/
def v2 (n : Nat) : Nat := v2Fuel n n

/-- Specification of the fuel-bounded valuation: `2^{v2 n}` divides `n`, and
the cofactor is odd for positive `n`. -/
theorem v2Fuel_spec : ∀ (fuel n : Nat), n ≤ fuel →
    2 ^ v2Fuel fuel n ∣ n ∧ (0 < n → (n / 2 ^ v2Fuel fuel n) % 2 = 1) := by
  intro fuel
  induction fuel with
  | zero =>
    intro n hn
    have hn0 : n = 0 := by omega
    subst hn0
    refine ⟨⟨0, rfl⟩, ?_⟩
    intro h; omega
  | succ fuel ih =>
    intro n hn
    by_cases h : n % 2 = 0 ∧ 0 < n
    · have hlt : n / 2 ≤ fuel := by omega
      obtain ⟨hdvd, hodd⟩ := ih (n / 2) hlt
      have hpos2 : 0 < n / 2 := by omega
      have hval : v2Fuel (fuel + 1) n = 1 + v2Fuel fuel (n / 2) := by
        show (if n % 2 = 0 ∧ 0 < n then 1 + v2Fuel fuel (n / 2) else 0) = _
        rw [if_pos h]
      constructor
      · obtain ⟨q, hq⟩ := hdvd
        have hpow : 2 ^ v2Fuel (fuel + 1) n = 2 * 2 ^ v2Fuel fuel (n / 2) := by
          rw [hval, show 1 + v2Fuel fuel (n / 2) = v2Fuel fuel (n / 2) + 1 from
            Nat.add_comm _ _, Nat.pow_succ, Nat.mul_comm]
        have hn2 : n = 2 * (n / 2) := by
          have hmod := Nat.mod_add_div n 2
          omega
        refine ⟨q, ?_⟩
        rw [hpow]
        exact hn2.trans ((congrArg (2 * ·) hq).trans (Nat.mul_assoc 2 _ q).symm)
      · intro _
        have hdiv : n / 2 ^ v2Fuel (fuel + 1) n
            = (n / 2) / 2 ^ v2Fuel fuel (n / 2) := by
          rw [hval, show 1 + v2Fuel fuel (n / 2) = v2Fuel fuel (n / 2) + 1 from
            Nat.add_comm _ _, Nat.pow_succ, Nat.mul_comm (2 ^ v2Fuel fuel (n / 2)) 2,
            ← Nat.div_div_eq_div_mul]
        rw [hdiv]
        exact hodd hpos2
    · have hval : v2Fuel (fuel + 1) n = 0 := by
        show (if n % 2 = 0 ∧ 0 < n then 1 + v2Fuel fuel (n / 2) else 0) = 0
        rw [if_neg h]
      constructor
      · rw [hval]
        exact ⟨n, (Nat.one_mul n).symm⟩
      · intro hnpos
        rw [hval]
        have hoddn : n % 2 = 1 := by
          have h2 : ¬ n % 2 = 0 := fun hh => h ⟨hh, hnpos⟩
          omega
        show (n / 1) % 2 = 1
        rw [Nat.div_one]
        exact hoddn

/-- `2^{v2 n}` divides `n`. -/
theorem two_pow_v2_dvd (n : Nat) : 2 ^ v2 n ∣ n :=
  (v2Fuel_spec n n (Nat.le_refl n)).1

/-- The cofactor of `2^{v2 n}` in a positive `n` is odd. -/
theorem odd_div_two_pow_v2 {n : Nat} (hn : 0 < n) : (n / 2 ^ v2 n) % 2 = 1 :=
  (v2Fuel_spec n n (Nat.le_refl n)).2 hn

/-- **Uniqueness of the valuation decomposition**: if `2^a` divides a positive
`m` with odd cofactor, then `a` *is* the 2-adic valuation of `m`. -/
theorem v2_unique {m a : Nat} (hm : 0 < m) (hdvd : 2 ^ a ∣ m)
    (hodd : (m / 2 ^ a) % 2 = 1) : v2 m = a := by
  obtain ⟨q, hq⟩ := hdvd
  have hqodd : q % 2 = 1 := by
    have hdiv : m / 2 ^ a = q := by
      rw [hq]
      exact Nat.mul_div_cancel_left q (Nat.pow_pos (show 0 < 2 by decide))
    rwa [hdiv] at hodd
  obtain ⟨q', hq'⟩ := two_pow_v2_dvd m
  have hq'odd : q' % 2 = 1 := by
    have hdiv : m / 2 ^ v2 m = q' :=
      Nat.mul_right_cancel (Nat.pow_pos (show 0 < 2 by decide))
        ((Nat.div_mul_cancel (two_pow_v2_dvd m)).trans (hq'.trans (Nat.mul_comm _ _)))
    have h2 := odd_div_two_pow_v2 hm
    rwa [hdiv] at h2
  -- `m = 2^a·q = 2^(v2 m)·q'` with both cofactors odd forces `a = v2 m`.
  have heq : 2 ^ a * q = 2 ^ v2 m * q' := by rw [← hq, ← hq']
  rcases Nat.lt_trichotomy a (v2 m) with hlt | heq' | hgt
  · -- a < v2 m: then `q = 2^(v2 m − a)·q'` is even, contradiction
    have h1 : v2 m = a + (v2 m - a) := (Nat.add_sub_of_le (Nat.le_of_lt hlt)).symm
    have h2 : 2 ^ v2 m = 2 ^ a * 2 ^ (v2 m - a) := by
      have hpa := Nat.pow_add 2 a (v2 m - a)
      rwa [← h1] at hpa
    rw [h2, Nat.mul_assoc] at heq
    have h3 : q = 2 ^ (v2 m - a) * q' :=
      Nat.mul_left_cancel (Nat.pow_pos (show 0 < 2 by decide)) heq
    have h4 : q % 2 = 0 := by
      rw [h3]
      have h5 : 2 ^ (v2 m - a) = 2 * 2 ^ (v2 m - a - 1) := by
        have h6 : v2 m - a = (v2 m - a - 1).succ := by omega
        have hps := Nat.pow_succ 2 (v2 m - a - 1)
        rw [← h6] at hps
        rw [hps, Nat.mul_comm]
      rw [h5, Nat.mul_assoc]
      exact Nat.mul_mod_right 2 _
    omega
  · exact heq'.symm
  · -- v2 m < a: symmetric, `q'` would be even
    have h1 : a = v2 m + (a - v2 m) := (Nat.add_sub_of_le (Nat.le_of_lt hgt)).symm
    have h2 : 2 ^ a = 2 ^ v2 m * 2 ^ (a - v2 m) := by
      have hpa := Nat.pow_add 2 (v2 m) (a - v2 m)
      rwa [← h1] at hpa
    rw [h2, Nat.mul_assoc] at heq
    have h3 : 2 ^ (a - v2 m) * q = q' :=
      Nat.mul_left_cancel (Nat.pow_pos (show 0 < 2 by decide)) heq
    have h4 : q' % 2 = 0 := by
      rw [← h3]
      have h5 : 2 ^ (a - v2 m) = 2 * 2 ^ (a - v2 m - 1) := by
        have h6 : a - v2 m = (a - v2 m - 1).succ := by omega
        have hps := Nat.pow_succ 2 (a - v2 m - 1)
        rw [← h6] at hps
        rw [hps, Nat.mul_comm]
      rw [h5, Nat.mul_assoc]
      exact Nat.mul_mod_right 2 _
    omega

/-- The odd-only (Syracuse) map on positive odd integers:
`U(n) = (3n+1) / 2^{v2(3n+1)}`. Defined on all of `Nat`; meaningful on
positive odd inputs. -/
def U (n : Nat) : Nat := (3 * n + 1) / 2 ^ v2 (3 * n + 1)

/-- `k`-fold iterate of `U`. -/
def iterU : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => U (iterU k n)

theorem iterU_succ' (k : Nat) (n : Nat) : iterU (k + 1) n = iterU k (U n) := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
    show U (iterU (k + 1) n) = U (iterU k (U n))
    rw [ih]

/-! ## 2. The affine constant of a valuation word -/

/-- Sum of a valuation word: the total valuation `K = Σ a_i`. -/
def valSum : List Nat → Nat
  | [] => 0
  | a :: as => a + valSum as

/-- The affine constant of a valuation word, in closed recursive form:
`affC [] = 0` and `affC (a :: as) = 3^|as| + 2^a · affC as`. Unrolling the
recursion shows this is exactly the packet's closed form
`C_m = Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{S_j}` with `S_j = a_0 + … + a_{j-1}`:
the `j`-th summand picks up one factor `2^{a_i}` for each `i < j`. -/
def affC : List Nat → Nat
  | [] => 0
  | a :: as => 3 ^ as.length + 2 ^ a * affC as

/-- The packet's affine accumulator: `C ↦ 3C + 2^S`, `S ↦ S + a` per step,
starting from `(0, 0)` (`affine_CS` in the verifier). -/
def affGo : List Nat → Nat → Nat → Nat × Nat
  | [], c, s => (c, s)
  | a :: as, c, s => affGo as (3 * c + 2 ^ s) (s + a)

/-- **Closed form of the affine accumulator.** -/
theorem affGo_spec (as : List Nat) (c s : Nat) :
    affGo as c s = (3 ^ as.length * c + 2 ^ s * affC as, s + valSum as) := by
  induction as generalizing c s with
  | nil =>
    show (c, s) = (3 ^ 0 * c + 2 ^ s * 0, s + 0)
    rw [Nat.pow_zero, Nat.one_mul, Nat.mul_zero, Nat.add_zero, Nat.add_zero]
  | cons a as ih =>
    show affGo as (3 * c + 2 ^ s) (s + a) = _
    rw [ih]
    show (3 ^ as.length * (3 * c + 2 ^ s) + 2 ^ (s + a) * affC as,
        s + a + valSum as)
      = (3 ^ (as.length + 1) * c + 2 ^ s * (3 ^ as.length + 2 ^ a * affC as),
        s + (a + valSum as))
    rw [Nat.pow_succ, Nat.pow_add]
    apply Prod.ext_iff.2
    constructor
    · rw [Nat.mul_add, Nat.mul_add, ← Nat.mul_assoc (3 ^ as.length) 3 c,
        Nat.mul_assoc (2 ^ s) (2 ^ a) (affC as), Nat.mul_comm (2 ^ s) (3 ^ as.length),
        ← Nat.add_assoc]
    · rw [Nat.add_assoc]

/-- The recursive `affC` agrees with the packet's accumulator: the verifier's
`C_m` is `(affGo a 0 0).1` and its `K` is `(affGo a 0 0).2 = valSum a`. -/
theorem affC_eq_affGo (a : List Nat) : affC a = (affGo a 0 0).1 := by
  rw [affGo_spec a 0 0]
  show affC a = 3 ^ a.length * 0 + 2 ^ 0 * affC a
  rw [Nat.mul_zero, Nat.pow_zero, Nat.one_mul, Nat.zero_add]

theorem valSum_eq_affGo (a : List Nat) : valSum a = (affGo a 0 0).2 := by
  rw [affGo_spec a 0 0]
  show valSum a = 0 + valSum a
  rw [Nat.zero_add]

/-- The affine constant of a nonempty word is positive. -/
theorem affC_pos {a : List Nat} (hne : a ≠ []) : 0 < affC a := by
  cases a with
  | nil => exact absurd rfl hne
  | cons a as =>
    show 0 < 3 ^ as.length + 2 ^ a * affC as
    have h : 0 < 3 ^ as.length := Nat.pow_pos (by decide)
    omega

/-! ## 3. Word dynamics and the cycle equation -/

/-- One prescribed word step from state `n`: divide `3n+1` by `2^a`. This
equals one application of `U` exactly when `a = v2(3n+1)`
(`wordStep_eq_U`). -/
def wordStep (a n : Nat) : Nat := (3 * n + 1) / 2 ^ a

/-- Iterate the prescribed steps of a valuation word. -/
def wordIter : List Nat → Nat → Nat
  | [], n => n
  | a :: as, n => wordIter as (wordStep a n)

/-- Exact realization predicate: every prescribed division is exact and every
quotient is odd, so each `a_j` really is `v2(3·state+1)` and each step really
is one application of `U`. (For odd `n`, `3n+1` is even, so exactness also
forces every `a_j ≥ 1` automatically.) -/
def WordExact : List Nat → Nat → Prop
  | [], _ => True
  | a :: as, n => 2 ^ a ∣ 3 * n + 1 ∧ ((3 * n + 1) / 2 ^ a) % 2 = 1 ∧
      WordExact as ((3 * n + 1) / 2 ^ a)

/-- **Affine form of a realized word.** If the word `a` is exactly realized
from `n`, then the terminal state satisfies
`wordIter a n · 2^K = 3^m · n + C_m` with `K = valSum a`, `m = a.length`. -/
theorem wordIter_affine (a : List Nat) (n : Nat) (h : WordExact a n) :
    wordIter a n * 2 ^ valSum a = 3 ^ a.length * n + affC a := by
  induction a generalizing n with
  | nil =>
    show n * 2 ^ 0 = 3 ^ 0 * n + 0
    rw [Nat.pow_zero, Nat.mul_one, Nat.one_mul, Nat.add_zero]
  | cons a as ih =>
    obtain ⟨hdvd, -, hrest⟩ := h
    have key := ih ((3 * n + 1) / 2 ^ a) hrest
    have hstep : (3 * n + 1) / 2 ^ a * 2 ^ a = 3 * n + 1 := Nat.div_mul_cancel hdvd
    have e1 : 2 ^ a * (3 ^ as.length * ((3 * n + 1) / 2 ^ a))
        = 3 ^ as.length * (3 * n + 1) := by
      rw [← Nat.mul_assoc (2 ^ a) (3 ^ as.length) ((3 * n + 1) / 2 ^ a),
        Nat.mul_comm (2 ^ a) (3 ^ as.length),
        Nat.mul_assoc (3 ^ as.length) (2 ^ a) ((3 * n + 1) / 2 ^ a),
        Nat.mul_comm (2 ^ a) ((3 * n + 1) / 2 ^ a), hstep]
    show wordIter as ((3 * n + 1) / 2 ^ a) * 2 ^ (a + valSum as)
      = 3 ^ (as.length + 1) * n + (3 ^ as.length + 2 ^ a * affC as)
    rw [Nat.pow_add,
      Nat.mul_left_comm (wordIter as ((3 * n + 1) / 2 ^ a)) (2 ^ a) (2 ^ valSum as),
      key, Nat.mul_add, e1, Nat.mul_add, ← Nat.mul_assoc (3 ^ as.length) 3 n,
      Nat.mul_one, Nat.pow_succ, Nat.add_assoc]

/-- `n` lies on a positive odd cycle of `U` whose valuation word is `a`:
the word is nonempty (a cycle has at least one odd member), `n` is a positive
odd integer, every step is exactly one `U`-step with the prescribed valuation,
and after the whole word the orbit returns to `n`. -/
def IsUCycleWord (a : List Nat) (n : Nat) : Prop :=
  a ≠ [] ∧ 0 < n ∧ n % 2 = 1 ∧ WordExact a n ∧ wordIter a n = n

/-- **The cycle equation.** Any positive odd cycle of `U` with valuation word
`a` satisfies the exact Diophantine identity
`n · 2^K = 3^m · n + C_m` — the packet's fixed-point equation
`n = C_m / (2^K − 3^m)` cleared of denominators. -/
theorem cycle_equation {a : List Nat} {n : Nat} (h : IsUCycleWord a n) :
    n * 2 ^ valSum a = 3 ^ a.length * n + affC a := by
  obtain ⟨-, -, -, hexact, hreturn⟩ := h
  have key := wordIter_affine a n hexact
  rwa [hreturn] at key

/-- A prescribed step with the *exact* valuation is one `U`-step. -/
theorem wordStep_eq_U {a n : Nat} (hdvd : 2 ^ a ∣ 3 * n + 1)
    (hodd : ((3 * n + 1) / 2 ^ a) % 2 = 1) : wordStep a n = U n := by
  have hv : v2 (3 * n + 1) = a := v2_unique (by omega) hdvd hodd
  show (3 * n + 1) / 2 ^ a = (3 * n + 1) / 2 ^ v2 (3 * n + 1)
  rw [hv]

/-- A realized word is precisely a `U`-orbit segment. -/
theorem wordIter_eq_iterU {a : List Nat} {n : Nat} (h : WordExact a n) :
    wordIter a n = iterU a.length n := by
  induction a generalizing n with
  | nil => rfl
  | cons a as ih =>
    obtain ⟨hdvd, hodd, hrest⟩ := h
    show wordIter as ((3 * n + 1) / 2 ^ a) = iterU (as.length + 1) n
    rw [iterU_succ', ← wordStep_eq_U hdvd hodd]
    exact ih hrest

/-- Hence a cycle word is an actual cycle of the odd-only map:
`U^m(n) = n`. -/
theorem realizes_iterU {a : List Nat} {n : Nat} (h : IsUCycleWord a n) :
    iterU a.length n = n := by
  obtain ⟨-, -, -, hexact, hreturn⟩ := h
  rw [← wordIter_eq_iterU hexact]
  exact hreturn

/-! ## 4. The verified exclusion checker -/

/-- The per-word fixed-point predicate of the external verifier
(`try_integral_fixed_point` in `contribution/code/fence/exact_cycle_search.py`):
`2^K > 3^m`, exact divisibility `C_m % (2^K − 3^m) = 0`, and an odd quotient.
(Quotient positivity is automatic for nonempty words, since `C_m ≥ 1`; the
verifier's `k == sum(a)` side condition is `valSum_eq_affGo` here.) -/
def WordAdmitsFixedPoint (a : List Nat) : Prop :=
  0 < 2 ^ valSum a - 3 ^ a.length ∧
  affC a % (2 ^ valSum a - 3 ^ a.length) = 0 ∧
  (affC a / (2 ^ valSum a - 3 ^ a.length)) % 2 = 1

instance (a : List Nat) : Decidable (WordAdmitsFixedPoint a) := by
  unfold WordAdmitsFixedPoint
  infer_instance

/-- **The per-word exclusion test** — exactly the negation of the verifier's
fixed-point gate, as a `Bool`. `true` means: no positive odd integer satisfies
the cycle equation for this word (`valuationWordExcluded_sound`). -/
def valuationWordExcluded (a : List Nat) : Bool :=
  !decide (WordAdmitsFixedPoint a)

/-- **Equation-level soundness of the gate**: any positive odd solution of the
cycle equation for a nonempty word passes the verifier's fixed-point gate. -/
theorem fixedPoint_of_equation {a : List Nat} (hne : a ≠ []) {n : Nat}
    (_hnpos : 0 < n) (hnodd : n % 2 = 1)
    (heq : n * 2 ^ valSum a = 3 ^ a.length * n + affC a) :
    WordAdmitsFixedPoint a := by
  have hcpos : 0 < affC a := affC_pos hne
  have hgt : 3 ^ a.length < 2 ^ valSum a := by
    have hnn : ¬ 2 ^ valSum a ≤ 3 ^ a.length := by
      intro hle
      have h1 : n * 2 ^ valSum a ≤ n * 3 ^ a.length := Nat.mul_le_mul_left n hle
      rw [Nat.mul_comm n (3 ^ a.length)] at h1
      omega
    omega
  have hd : 0 < 2 ^ valSum a - 3 ^ a.length := Nat.sub_pos_of_lt hgt
  have hsum : 3 ^ a.length + (2 ^ valSum a - 3 ^ a.length) = 2 ^ valSum a :=
    Nat.add_sub_of_le (Nat.le_of_lt hgt)
  have hmul : n * (2 ^ valSum a - 3 ^ a.length) = affC a := by
    have e := heq
    rw [← hsum, Nat.mul_add, Nat.mul_comm n (3 ^ a.length)] at e
    omega
  refine ⟨hd, ?_, ?_⟩
  · have hdvd : (2 ^ valSum a - 3 ^ a.length) ∣ affC a :=
      ⟨n, hmul.symm.trans (Nat.mul_comm n _)⟩
    exact Nat.mod_eq_zero_of_dvd hdvd
  · rw [← hmul, Nat.mul_div_cancel n hd]
    exact hnodd

/-- **Soundness of the exclusion checker**: if the checker returns `true` for a
nonempty word, no positive odd integer satisfies the cycle equation for it. -/
theorem valuationWordExcluded_sound {a : List Nat}
    (hex : valuationWordExcluded a = true) (hne : a ≠ []) {n : Nat}
    (hnpos : 0 < n) (hnodd : n % 2 = 1)
    (heq : n * 2 ^ valSum a = 3 ^ a.length * n + affC a) : False := by
  have hf : decide (WordAdmitsFixedPoint a) = false := by
    have h := hex
    unfold valuationWordExcluded at h
    revert h
    cases decide (WordAdmitsFixedPoint a) with
    | true => intro h; exact absurd h (by decide)
    | false => intro _; rfl
  exact of_decide_eq_false hf (fixedPoint_of_equation hne hnpos hnodd heq)

/-- **Excluded words carry no cycles.** If `valuationWordExcluded a = true`,
no positive odd cycle of `U` realizes the word `a`. -/
theorem no_cycle_of_excluded {a : List Nat} {n : Nat}
    (hex : valuationWordExcluded a = true) (h : IsUCycleWord a n) : False :=
  valuationWordExcluded_sound hex h.1 h.2.1 h.2.2.1 (cycle_equation h)

/-! ## 5. Kernel-checked exclusion layers

The checker is evaluated *inside the Lean kernel* (`decide`) on every word of
the bounded sample spaces below. The constant word `[2, …, 2]` — the valuation
word of the trivial cycle `{1}` at every length — is the unique
non-excluded word in each layer, matching the external pipeline's `(1, 2)`
control. Layers m ≤ 3 are the mission target; m = 4 is included as a bonus
since it is still cheap.

Measured wall-clock on toolchain v4.31.0, 2026-08-01 (this machine; standalone
`lean` on each layer theorem, cold; the default `maxRecDepth 2048` suffices up
to the 512-word layer):

| layer | words | wall | notes |
|---|---:|---:|---|
| m = 1, entries ≤ 32 | 32 | ≈ 0.2 s | default options |
| m = 2, entries ≤ 16 | 256 | ≈ 0.2 s | default options |
| m = 3, entries ≤ 8 | 512 | ≈ 0.2 s | default options |
| m = 3, entries ≤ 12 | 1,728 | ≈ 1.4 s | needs `maxRecDepth 16384` |
| m = 4, entries ≤ 8 | 4,096 | ≈ 3.5 s | in this file |
| m = 5, entries ≤ 6 | 7,776 | ≈ 6.2 s | `maxRecDepth 32768` |
| m = 4, entries ≤ 12 | 20,736 | ≈ 17.3 s | `maxRecDepth 131072` |
| m = 5, entries ≤ 8 | 32,768 | — | elaborator heartbeat timeout (200,000) |

So in-kernel `decide` is comfortable up to roughly 2×10⁴ words (seconds to
tens of seconds, raised recursion limits); at ~3×10⁴ words it hits the default
elaborator heartbeat wall. The external exact pipeline evaluates 6.20×10⁸
words per phase in minutes — that is where the kernel hands off to the
external engine (packet `2026-07-23-cycle-exclusion-extension`), with this
checker as the sound kernel-side recheck for a future certificate import. -/

/-- All length-`m` valuation words with entries in `[1, B]`: the bounded
sample space for the in-kernel exclusion layers. -/
def sampleWords : Nat → Nat → List (List Nat)
  | 0, _ => [[]]
  | m + 1, B => (List.range' 1 B).flatMap fun a =>
      (sampleWords m B).map fun w => a :: w

/-- **Kernel layer m = 1** (32 words, entries in `[1, 32]`): every length-1
word is excluded except the trivial-cycle word `[2]`. -/
theorem kernel_layer_m1 :
    (sampleWords 1 32).all (fun w => (w == [2]) || valuationWordExcluded w)
      = true := by
  decide

set_option maxRecDepth 16384 in
/-- **Kernel layer m = 2** (256 words, entries in `[1, 16]`): every length-2
word is excluded except the trivial-cycle word `[2, 2]`. -/
theorem kernel_layer_m2 :
    (sampleWords 2 16).all (fun w => (w == [2, 2]) || valuationWordExcluded w)
      = true := by
  decide

set_option maxRecDepth 16384 in
/-- **Kernel layer m = 3** (512 words, entries in `[1, 8]`): every length-3
word is excluded except the trivial-cycle word `[2, 2, 2]`. -/
theorem kernel_layer_m3 :
    (sampleWords 3 8).all
      (fun w => (w == [2, 2, 2]) || valuationWordExcluded w) = true := by
  decide

set_option maxRecDepth 16384 in
/-- **Kernel layer m = 4** (4,096 words, entries in `[1, 8]`; bonus layer):
every length-4 word is excluded except the trivial-cycle word `[2, 2, 2, 2]`. -/
theorem kernel_layer_m4 :
    (sampleWords 4 8).all
      (fun w => (w == [2, 2, 2, 2]) || valuationWordExcluded w) = true := by
  decide

end CycleExclusion

/-! ## Sanity checks (all closed by `decide`) -/

namespace CycleExclusion

-- the odd-only map on small inputs: `U 1 = 1`, `3 ↦ 5 ↦ 1`, `U 7 = 11`
example : U 1 = 1 ∧ U 3 = 5 ∧ U 5 = 1 ∧ U 7 = 11 := by decide

-- a `U`-orbit segment: `7 ↦ 11 ↦ 17 ↦ 13`
example : iterU 3 7 = 13 := by decide

-- affine constants against the packet recurrence
example : affC [2] = 1 ∧ affC [1, 4] = 5 ∧ valSum [1, 4] = 5 := by decide

-- the affine constant agrees with the packet's accumulator on samples
example : affC [3, 2, 5] = (affGo [3, 2, 5] 0 0).1
    ∧ valSum [3, 2, 5] = (affGo [3, 2, 5] 0 0).2 := by decide

-- the cycle equation instance for the trivial cycle: `1 · 2^2 = 3^1 · 1 + 1`
example : (1 : Nat) * 2 ^ valSum [2] = 3 ^ [2].length * 1 + affC [2] := by decide

-- trivial-cycle control: `[2]`, `[2, 2]` are NOT excluded (they are the
-- valuation words of `{1}`), matching the external verifier's `(1, 2)` control
example : valuationWordExcluded [2] = false ∧ valuationWordExcluded [2, 2] = false
    ∧ valuationWordExcluded [2, 2, 2] = false := by decide

-- the empty word and `[1]` are excluded
example : valuationWordExcluded [] = true ∧ valuationWordExcluded [1] = true := by
  decide

-- the trivial cycle really is a cycle word, and it passes the gate
example : IsUCycleWord [2] 1 ∧ WordAdmitsFixedPoint [2] :=
  ⟨⟨by decide, by decide, by decide, ⟨⟨1, rfl⟩, by decide, True.intro⟩, by decide⟩,
    by decide⟩

end CycleExclusion

-- Axiom audit: must not list `sorryAx`.
#print axioms CycleExclusion.cycle_equation
#print axioms CycleExclusion.realizes_iterU
#print axioms CycleExclusion.fixedPoint_of_equation
#print axioms CycleExclusion.valuationWordExcluded_sound
#print axioms CycleExclusion.no_cycle_of_excluded
#print axioms CycleExclusion.kernel_layer_m1
#print axioms CycleExclusion.kernel_layer_m2
#print axioms CycleExclusion.kernel_layer_m3
#print axioms CycleExclusion.kernel_layer_m4
