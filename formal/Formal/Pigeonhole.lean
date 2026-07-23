/-
Collatz atlas — formal certificates.

Bespoke pigeonhole principle for `Nat`-valued sequences.

This is a support module for `Formal.TwoBranchFamily`.  Lean 4 core
(v4.31.0) does not ship `Finset` cardinality bounds or a pigeonhole lemma
(those live in mathlib), so the exact statement needed by the two-branch
family certificate is proved here directly by induction on the number of
holes.  The proof uses only core tactics (`omega`, `split`, `rcases`) and no
classical axioms beyond those already inside core `Nat` decidability.

Exact integer arithmetic throughout; no floats, no `sorry`.
-/

namespace CollatzAtlas

/--
**Pigeonhole, sequence form.**  If `N + 1` values `g 0, g 1, …, g N` all land
in the `N`-element set `{0, …, N - 1}`, then two of them coincide.

Equivalently: no map `{0, …, N} → {0, …, N - 1}` is injective.

Proof idea (induction on `N`).  For `N = 0` the hypothesis `g 0 < 0` is
absurd.  For the step, either the value `N` is taken twice (and we are done)
or at most once; deleting the unique index that hits `N` (or the last index,
if none does) and reindexing yields a map `{0, …, N} → {0, …, N - 1}` to
which the induction hypothesis applies.
-/
theorem exists_eq_of_forall_lt :
    ∀ (N : Nat) (g : Nat → Nat), (∀ k, k ≤ N → g k < N) →
      ∃ i j, i < j ∧ j ≤ N ∧ g i = g j := by
  intro N
  induction N with
  | zero =>
    intro g hg
    have h0 := hg 0 (Nat.le_refl 0)
    omega
  | succ N ih =>
    intro g hg
    -- Case A: the value `N` is taken at two distinct indices; done.
    by_cases hA : ∃ i j, i < j ∧ j ≤ N + 1 ∧ g i = N ∧ g j = N
    · obtain ⟨i, j, hij, hj, hiN, hjN⟩ := hA
      exact ⟨i, j, hij, hj, hiN.trans hjN.symm⟩
    -- Otherwise the preimage of `N` is unique (when it exists).
    have huniq : ∀ i j, i ≤ N + 1 → j ≤ N + 1 → g i = N → g j = N → i = j := by
      intro i j hi hj hgi hgj
      rcases (by omega : i < j ∨ i = j ∨ j < i) with h | h | h
      · exact absurd ⟨i, j, h, hj, hgi, hgj⟩ hA
      · exact h
      · exact absurd ⟨j, i, h, hi, hgj, hgi⟩ hA
    -- Choose a pivot index `t`: the unique preimage of `N` if it exists,
    -- otherwise the last index `N + 1` (vacuous).  In both cases every
    -- index `m ≤ N + 1` different from `t` has `g m < N`.
    obtain ⟨t, ht, hkey⟩ : ∃ t, t ≤ N + 1 ∧ ∀ m, m ≤ N + 1 → m ≠ t → g m < N := by
      by_cases hE : ∃ t, t ≤ N + 1 ∧ g t = N
      · obtain ⟨t, ht, hgt⟩ := hE
        refine ⟨t, ht, fun m hm hmt => ?_⟩
        have hgm : g m < N + 1 := hg m hm
        rcases (by omega : g m < N ∨ g m = N) with h | h
        · exact h
        · exact absurd (huniq m t hm ht h hgt) hmt
      · refine ⟨N + 1, Nat.le_refl _, fun m hm _ => ?_⟩
        have hgm : g m < N + 1 := hg m hm
        rcases (by omega : g m < N ∨ g m = N) with h | h
        · exact h
        · exact absurd ⟨m, hm, h⟩ hE
    -- Reindex, skipping the pivot: `g'` maps `{0, …, N}` into `{0, …, N - 1}`.
    let g' : Nat → Nat := fun k => g (if k < t then k else k + 1)
    have hg'N : ∀ k, k ≤ N → g' k < N := by
      intro k hk
      have hm : (if k < t then k else k + 1) ≤ N + 1 := by split <;> omega
      have hne : (if k < t then k else k + 1) ≠ t := by split <;> omega
      exact hkey _ hm hne
    obtain ⟨i', j', hij', hj', hEq⟩ := ih g' hg'N
    -- Map the collision back to the original indexing; the shift is
    -- strictly monotone, so `i' < j'` lifts to `i < j`.
    refine ⟨if i' < t then i' else i' + 1, if j' < t then j' else j' + 1, ?_, ?_, ?_⟩
    · split <;> split <;> omega
    · split <;> omega
    · exact hEq

end CollatzAtlas
