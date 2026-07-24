import Formal.TerrasBijection

/-!
# The height–complexity collision principle — plain Lean 4 core, no mathlib

**Source.** `contribution/packets/2026-07-22-landmark-pointwise/`
`COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`, Lemmas 1–2, and
`LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md`, Theorem 4.1.  This is the
finite arithmetic backbone that
`contribution/packets/2026-07-24-supercritical-automatic-closure/` rests on.

**What is formalized.** Everything in the packet's proof chain that is a
statement about integers:

* `states_eq_of_block_eq` — if two orbit positions carry the *same* length-`k`
  parity block and *both* states are below `2 ^ k`, the states are equal.
  (Lemma 1 + the small-height half of Lemma 2.)
* `orbit_shift_eq` — equal states make the two orbit tails identical.
* `collision_forces_large_state` — the contrapositive actually used: in an
  orbit whose tails from `i` and `j` ever differ, a repeated length-`k`
  parity block forces one of the two states to be at least `2 ^ k`.

**What is NOT formalized, and why.** The packet's terminal statement is an
asymptotic inequality between `limsup p_q(k)/k` and `log_3 2`.  Plain Lean 4
core (v4.31.0, no mathlib) has no reals, no `limsup`, and no logarithms, so
that statement cannot even be written here.  The finite step above is the
part that carries arithmetic content; the remainder is real-number
bookkeeping done in the memo and checked numerically by the verifier.  This
file makes no claim about the Collatz conjecture.

**Exactness note.** All arithmetic is exact `Nat` arithmetic; no floats.

**Verification.** From `formal/`: `lake build`, or standalone
`~/.elan/bin/lean Formal/CollisionPrinciple.lean` after `Formal/
TerrasBijection.lean` is built.  `#print axioms` at the end audits that no
`sorry` axiom is used.
-/

namespace CollatzAtlas.Collision

open Terras

/-- Iterating `a + b` times is iterating `b` times and then `a` times. -/
theorem iterT_add (a b n : Nat) : iterT (a + b) n = iterT a (iterT b n) := by
  induction a with
  | zero =>
      show iterT (0 + b) n = iterT b n
      rw [Nat.zero_add]
  | succ a ih =>
      have h : a + 1 + b = (a + b) + 1 := by omega
      rw [h]
      show T (iterT (a + b) n) = T (iterT a (iterT b n))
      rw [ih]

/-- **Lemma 1 + small-height Lemma 2.**  Equal length-`k` parity blocks make
the two states congruent mod `2 ^ k`; if both states are below `2 ^ k` the
congruence is an equality. -/
theorem states_eq_of_block_eq {k i j n : Nat}
    (hpar : parityWord k (iterT i n) = parityWord k (iterT j n))
    (hi : iterT i n < 2 ^ k) (hj : iterT j n < 2 ^ k) :
    iterT i n = iterT j n := by
  have h : (iterT i n) % 2 ^ k = (iterT j n) % 2 ^ k :=
    (parityWord_eq_iff k _ _).1 hpar
  rwa [Nat.mod_eq_of_lt hi, Nat.mod_eq_of_lt hj] at h

/-- Equal states at two positions make the whole orbit tails agree. -/
theorem orbit_shift_eq {i j n : Nat} (h : iterT i n = iterT j n) :
    ∀ t, iterT (i + t) n = iterT (j + t) n := by
  intro t
  have hi : i + t = t + i := Nat.add_comm i t
  have hj : j + t = t + j := Nat.add_comm j t
  rw [hi, hj, iterT_add t i n, iterT_add t j n, h]

/-- **The collision principle (Theorem 4.1, finite form).**  If the orbit
tails from `i` and from `j` differ somewhere, then a repeated length-`k`
parity block at those two positions forces one of the two states to reach
`2 ^ k`.

This is the exact step that converts *symbolic repetition* into a *height
excursion*: it is why an aperiodic realizable transcript must have at least
`p_q(k)` positions before its orbit passes `2 ^ k`, and hence why factor
complexity is bounded below by the orbit's growth rate. -/
theorem collision_forces_large_state {k i j n : Nat}
    (hpar : parityWord k (iterT i n) = parityWord k (iterT j n))
    (hdiff : ∃ t, iterT (i + t) n ≠ iterT (j + t) n) :
    2 ^ k ≤ iterT i n ∨ 2 ^ k ≤ iterT j n := by
  rcases Nat.lt_or_ge (iterT i n) (2 ^ k) with hi | hi
  · rcases Nat.lt_or_ge (iterT j n) (2 ^ k) with hj | hj
    · obtain ⟨t, ht⟩ := hdiff
      exact absurd (orbit_shift_eq (states_eq_of_block_eq hpar hi hj) t) ht
    · exact Or.inr hj
  · exact Or.inl hi

/-- Restatement used by the memo: an orbit that is *not* eventually periodic
with period `j - i` cannot have both states small under a block repetition.
Phrased without subtraction, for `i < j`. -/
theorem block_repeat_of_bounded_orbit {k i j n : Nat}
    (hpar : parityWord k (iterT i n) = parityWord k (iterT j n))
    (hi : iterT i n < 2 ^ k) (hj : iterT j n < 2 ^ k) :
    ∀ t, iterT (i + t) n = iterT (j + t) n :=
  orbit_shift_eq (states_eq_of_block_eq hpar hi hj)

end CollatzAtlas.Collision

/-! ## Sanity checks (all closed by `decide`) -/

namespace CollatzAtlas.Collision

open Terras

-- The trivial cycle 1 → 2 → 1 under `T`: a genuine small-state collision.
example : iterT 0 1 = 1 ∧ iterT 1 1 = 2 ∧ iterT 2 1 = 1 := by decide

-- Positions 0 and 2 of the orbit of 1 carry the same length-3 parity block
-- and both states are below 2^3, so the states coincide — as the lemma says.
example : parityWord 3 (iterT 0 1) = parityWord 3 (iterT 2 1) := by decide
example : iterT 0 1 < 2 ^ 3 ∧ iterT 2 1 < 2 ^ 3 := by decide
example : iterT 0 1 = iterT 2 1 := by decide

-- A non-collision control: positions 0 and 1 of the orbit of 7 carry
-- different length-4 parity blocks, so no conclusion is drawn.
example : parityWord 4 (iterT 0 7) ≠ parityWord 4 (iterT 1 7) := by decide

-- `iterT_add` on a concrete instance.
example : iterT (3 + 2) 7 = iterT 3 (iterT 2 7) := by decide

end CollatzAtlas.Collision

-- Axiom audit: must not list `sorryAx`.
#print axioms CollatzAtlas.Collision.states_eq_of_block_eq
#print axioms CollatzAtlas.Collision.orbit_shift_eq
#print axioms CollatzAtlas.Collision.collision_forces_large_state
