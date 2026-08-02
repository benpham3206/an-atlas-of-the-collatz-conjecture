# formal/ — Lean 4 certificates for the Collatz atlas

Machine-checked proofs of atlas results, in **plain Lean 4 core** (no
mathlib), pinned to toolchain `leanprover/lean4:v4.31.0`. Everything here is
exact integer (`Nat`) arithmetic; there are no floats, no `sorry`, and no
user-declared axioms.

## Layout

```
formal/
  lean-toolchain              # leanprover/lean4:v4.31.0 (via elan)
  lakefile.lean               # no dependencies whatsoever
  Formal.lean                 # library root
  Formal/
    Pigeonhole.lean           # bespoke pigeonhole for Nat sequences
    TwoBranchFamily.lean      # Theorem 4 of contribution/proofs/PARTIAL_THEOREMS.md
    TerrasBijection.lean      # Theorem 1 of contribution/proofs/PARTIAL_THEOREMS.md
    CollisionPrinciple.lean   # Lemmas 1-2 / Theorem 4.1 of the landmark packet
    ChainClosure.lean         # chain closure for the Syracuse Fourier recursion
    BeattyKill.lean           # Beatty kill triple for the chain-exponent law
    ContractionOnset.lean     # Syracuse cocycle, Lemma 1, and the M(h) onset bound
    CycleExclusion.lean       # cycle equation + verified per-word exclusion checker
```

## How to build

```bash
cd formal
lake build        # exit code 0; a cold build takes a few seconds
```

Requirements: `elan` with the `leanprover/lean4:v4.31.0` toolchain installed
(`elan toolchain install leanprover/lean4:v4.31.0`). The `lean-toolchain`
file selects it automatically; no `lake exe cache get` or dependency
download is needed because there are no dependencies.

To audit the proofs (as any skeptical outsider should), run:

```bash
grep -rn "sorry" Formal/    # matches only the English word in comments
lake env lean  # on a scratch file importing Formal, then:
#print axioms TwoBranchFamily.twoBranch_eventually_periodic
```

Axiom audit (output of `#print axioms`): the theorems depend only on
`[propext, Classical.choice, Quot.sound]` — the standard classical axiom
triple that ordinary mathlib proofs also carry; the `TerrasBijection`
theorems use only `[propext, Quot.sound]`. Crucially, **`sorryAx` does
not appear** anywhere. `twoBranch_enters_finite_set` and
`twoBranch_invariant` do not even use `Classical.choice`.

## What is proved (plain language)

Source: `contribution/proofs/PARTIAL_THEOREMS.md`, **Theorem 4** — the
`a = 1` two-branch family is non-universal under orbit embedding. Fix an
integer `b > 0` and iterate

```
S_b(n) = n / 2        if n even
S_b(n) = (n + b) / 2  if n odd
```

The file `Formal/TwoBranchFamily.lean` proves, for every positive starting
value `n`:

1. **`twoBranch_enters_finite_set`** — *the orbit reaches the band
   `{1, …, b}`.* Whenever `n > b`, one step strictly decreases the value
   (`S_lt_of_lt`: `n/2 < n`; `(n+b)/2 < n` since `b < n`) while keeping it
   positive (`S_pos`), so strong induction on `n` produces a hitting time
   `m` with `1 ≤ S_b^m(n) ≤ b`.
2. **`twoBranch_invariant`** — *the band is closed under the map.* From
   `1 ≤ n ≤ b` follows `1 ≤ S_b(n) ≤ b`: `n/2 ≤ n ≤ b`, and
   `(n+b)/2 ≤ (b+b)/2 = b`. Iterating (`orbit_in_band`), an orbit that
   enters the band never leaves.
3. **`twoBranch_eventually_periodic`** — *the orbit eventually repeats.*
   After the hitting time `m`, the `b + 1` states
   `S_b^m(n), …, S_b^(m+b)(n)` all lie in the `b`-element band, so two
   coincide (pigeonhole), giving `h` and a period `p > 0` with
   `S_b^(h+p)(n) = S_b^h(n)`.
4. **`twoBranch_periodic_tail`** (corollary added beyond the draft) — the
   whole tail is periodic: `S_b^(h+p+k)(n) = S_b^(h+k)(n)` for every `k`.
   Hence the orbit takes only finitely many distinct values and cannot
   step-faithfully encode an infinite machine run with pairwise distinct
   configurations — the non-universality conclusion of Theorem 4.

The supporting module `Formal/Pigeonhole.lean` proves the exact pigeonhole
principle needed (`CollatzAtlas.exists_eq_of_forall_lt`): no map
`{0, …, N} → {0, …, N−1}` is injective. Lean 4 core has no `Finset`
cardinality theory, so this is proved from scratch by induction on `N`.

## What is proved (plain language) — Terras bijection

Source: `contribution/proofs/PARTIAL_THEOREMS.md`, **Theorem 1**
(finite-cylinder saturation). The file `Formal/TerrasBijection.lean`
proves, in namespace `Terras`:

**`terras_bijection`** — for every binary word `w : List Bool` there exists
a residue `r < 2^w.length`, unique among such residues, with

```
parityWord w.length n = w  ↔  n % 2^w.length = r
```

where `parityWord k n` records the parities of the first `k` iterates of the
Terras map `T(n) = n/2` (even), `(3n+1)/2` (odd). Proof structure:

1. **`terras_affine`** — the affine cocycle: the first `k` parity bits of
   `r + 2^k·t` equal those of `r`, and the `k`-th iterate is
   `iterT k r + 3^(number of odd bits)·t` (induction on `k`; the odd step
   absorbs a factor of 3 via `3·2^k·t = 2^k·(3t)`).
2. **`rho` / `rho_spec`** — an explicit computable residue map built
   low-bit-first; each correction bit is set so the new iterate parity
   matches the appended word bit (uses that `3^o` is odd).
3. **`rho_correct` / uniqueness** — via `inj3mod` (injectivity of
   `x ↦ 3x + 2 mod 2^k`, the only point where invertibility of
   `3 mod 2^k` is needed) and `parityWord_eq_iff`
   (`parityWord k n = parityWord k m ↔ n ≡ m (mod 2^k)`).

Sanity checks closed by `decide`: explicit residues for all words at
`k = 1, 2, 3` (the `k = 3` residues `0,4,2,6,5,1,3,7` are visibly a
permutation of `0..7`), full-cylinder checks at `k ≤ 3`, and
`rho ∘ parityWord 3 = id` on `{0,…,7}`. Axiom base: `[propext, Quot.sound]`
only — not even `Classical.choice`.

This is the classical Terras (1976) bijection; the Lean proof is the
atlas's own formalization and matches the repository's `k ≤ 20`
computational verification (`contribution/code/F1_REPORT.md`, D2).

## What is proved (plain language) — collision principle

Source: `contribution/packets/2026-07-22-landmark-pointwise/`
`COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`, Lemmas 1–2, and
Theorem 4.1 of the strategy memo. The file `Formal/CollisionPrinciple.lean`
proves, in namespace `CollatzAtlas.Collision`:

1. **`states_eq_of_block_eq`** — if positions `i` and `j` of a Terras orbit
   carry the same length-`k` parity block and *both* states are below `2^k`,
   the two states are equal. Immediate from `Terras.parityWord_eq_iff` plus
   `Nat.mod_eq_of_lt`; this is the arithmetic content of Lemma 1 together
   with the small-height half of Lemma 2.
2. **`orbit_shift_eq`** — equal states make the two orbit tails identical
   (via `iterT_add`, proved here).
3. **`collision_forces_large_state`** — the form actually used downstream:
   if the tails from `i` and `j` differ anywhere, a repeated length-`k`
   parity block forces `2^k ≤ iterT i n` or `2^k ≤ iterT j n`.

This is the step that turns *symbolic repetition* into a *height excursion*,
and it is what the factor-complexity lower bounds
(`limsup p_q(k)/k ≥ κ`, and the density-refined version) are built on. It is
consumed by `contribution/packets/2026-07-24-supercritical-automatic-closure/`.

**Not formalized, and deliberately so:** the terminal statements of those
packets are asymptotic inequalities involving `limsup` and `log_3 2`. Plain
Lean 4 core has no reals, no limits and no logarithms, so they cannot be
stated here at all. The finite step above is the part with arithmetic
content. Axiom base: `[propext, Quot.sound]`.

## What is proved (plain language) — chain closure

Source: `contribution/packets/2026-07-22-syracuse-fourier/`, Theorem 1 (the
proved Syracuse Fourier recursion). The file `Formal/ChainClosure.lean`
proves, in namespace `ChainClosure`, for every odd modulus `q > 1`
(instantiated at `q = 3^{n+1}`):

1. **Explicit inverse** — `inv2 q = (q+1)/2` satisfies `2 * inv2 q ≡ 1
   (mod q)` (`two_mul_inv2_mod`), so `2` is a unit modulo `3^{n+1}`
   (`two_is_unit_three_pow`) and `gcd 2 (3^n) = 1` (`gcd_two_three_pow`).
2. **Chain closure identity** — with `invPow q a = (inv2 q)^a mod q` as the
   explicit representative of `u_a = 2^{-a}`: for `a ≤ k`,
   `(2^k * invPow q a) % q = 2^(k-a) % q` (`chain_closure_nat`), and for
   arbitrary integer exponents, `(twoPowZ q k * invPow q a) % q = twoPowZ q
   (k - a)` (`twoPowZ_mul_invPow`), where `twoPowZ q k` is `2^k mod q` for
   `k ≥ 0` and uses the explicit inverse for negative `k`.
3. **Exponent homomorphism** — `k ↦ 2^k mod q` is a group homomorphism
   `ℤ → (ℤ/qℤ)ˣ`, expressed mathlib-free by the step laws `twoPowZ_succ`,
   `twoPowZ_pred` and the bundled `twoPowZ_is_hom`.
4. **Euler period bound** — `2^(2·3^n) ≡ 1 (mod 3^{n+1})`
   (`two_pow_euler_three_pow`, induction with the cube-lifting step), i.e.
   the order of `2` mod `3^{n+1}` divides `φ(3^{n+1}) = 2·3^n`. The
   classical strengthening to equality (`2` is a primitive root mod `3^m`)
   is documented but not formalized.
5. **Chain subsystem closure** — `ChainSupported` coefficient functions are
   mapped to `ChainSupported` ones by the one-step update `chainStep`
   (`chainSupported_chainStep`): if the updated value at `ξ` is nonzero,
   some branch term is nonzero, so `ξ · u_a` is a chain residue and hence
   `ξ` itself is one (`chainResidue_of_mul_invPow`). The index dynamics
   `k ↦ k − a` is also given on a finite window `ChainState n = Fin
   (2·3^{n+1})` (`chainIndexStep`).
6. **Mass half of the dominance target** — the exact Syracuse branch masses
   `W a = 2^{A-a}` satisfy `Σ_{a=2}^A 2^{A-a} = 2^{A-1} − 1`
   (`syracuse_tail_mass`), so the tail misses the `a = 1` mass by exactly
   one unit (`syracuse_mass_slack`). The full `a = 1` dominance (odometer)
   conjecture — that this single unit of slack survives the analytic phase
   factors — is stated as the documented predicate `IsOdometerDominant`
   plus a comment block, and remains an **open target** (no `sorry`).

**Scoping:** the complex phase factor `e(−ξ u_a / 3^{n+1})` is parameterized
into the branch weight function `w`; everything proved here is exact integer
data (indices and residues). Plain Lean 4 core has no `ℂ` and no `ZMod`, so
the analytic recursion itself cannot be stated here; see the file header for
the substitution table. Axiom base: `[propext, Classical.choice, Quot.sound]`
(`Classical.byContradiction` is used once, in `chainSupported_chainStep`).

## What is proved (plain language) — the Beatty kill triple

Source: `contribution/packets/2026-08-01-chain-exponent-law/`
`COLLATZ_CHAIN_EXPONENT_LAW.md`, §2–§4 (kill criteria (a) and (b), and the CF
test of §4), cross-checked against `verify_chain_exponent_law.py`. The file
`Formal/BeattyKill.lean` proves, in namespace `BeattyKill`, over the certified
table `k(n)`, `n = 6..21` = `6,8,9,10,12,13,14,16,17,18,20,21,23,24,26,28`:

1. **No Beatty line fits, with any slope and any phase (kill criterion (a)).**
   * `beatty_phase_free_infeasible` — the phase-free core: no rational
     `γ = N/D` satisfies `k(n) ≤ γ·n < k(n) + 1` at all sixteen layers. The
     `n = 21` constraint forces `γ ≥ 4/3` and the `n = 15` constraint forces
     `γ < 19/15`; since `4/3 > 19/15`, two constraints already contradict and
     the full 16-constraint statement comes free.
   * `gamma_gt_three_halves_of_pair` / `gamma_lt_eleven_eighths_of_pair` — the
     memo's exact witnesses: the phase-eliminated pair condition at
     `(k(21), k(15)) = (28, 18)` forces `γ > 3/2`, and at
     `(k(7), k(15)) = (8, 18)` forces `γ < 11/8`.
   * `beatty_pairwise_infeasible` — the memo §2 statement verbatim: all
     `16 × 15` pairwise phase-eliminated conditions together are infeasible
     (`3/2 > 11/8`). Because subtracting the two margin-1 constraints
     eliminates *any* phase (including a real one), this kills every phase at
     once.
   * `beatty_infeasible_with_phase` — the strongest rational form: no
     rational slope `γ = N/D` and rational phase `φ = A/D` (common
     denominator, w.l.o.g.) satisfy `k(n) ≤ γ·n + φ < k(n) + 1` on the table;
     the phase cancels and the witnesses chain to `36·D < 33·D`.
   All proofs are cross-multiplied `Int` linear arithmetic closed by `omega`.
2. **The jump word is not balanced (kill criterion (b)).** For
   `Δk = (2,1,1,2,1,1,2,1,1,2,1,2,1,2,2)`:
   * `not_balanced_of_double_factors` — general lemma: any word containing
     both double factors `(x,x)` and `(y,y)` with `x ≠ y` is unbalanced
     (their sums `2x`, `2y` differ by at least 2). Hence no balanced
     two-valued word — in particular no Sturmian/Beatty difference word —
     contains both `(1,1)` and `(2,2)`.
   * `deltaK_not_balanced` (via the general lemma) and
     `deltaK_not_balanced_direct` (the specific finite check, exhibiting the
     factors `(1,1)` at offset 1 and `(2,2)` at offset 13 and evaluating by
     `decide`) — both forms are proved.
   * `deltaK_max_imbalance_is_two` — the maximal imbalance over all factor
     pairs is exactly 2: a bounded `decide` check over `ℓ, s, t < 16` in both
     directions, plus the attaining witness.
3. **The CF of `log₂ 3` begins `[1; 1, 1, 2, 2, 3, 1, 5, 2, 23]`, certified
   by exact integer arithmetic.** Plain Lean 4 core has no reals and no
   logarithms, so the enclosure `p/q < log₂ 3 < p'/q'` is *defined* as the
   `Nat` exponent comparisons `2^p < 3^q ∧ 3^q' < 2^p'` (`Encloses` — exact
   by monotonicity of `log₂`).
   * `log2Three_convergents` — the convergents of the prefix, computed by the
     exact recurrence, are `1, 2, 3/2, 8/5, 19/12, 65/41, 84/53, 485/306,
     1054/665, 24727/15601`.
   * `log2Three_cf_certified` — the nine convergent brackets (each between
     consecutive convergents) plus the semiconvergent refinement
     `25781/16266 < log₂ 3 < 24727/15601`, all proved by `decide` — the
     largest compares `2^25781` with `3^16266` (~7,800 decimal digits), using
     only the kernel's accelerated `Nat` arithmetic (no `Lean.ofReduceBool`).
     Classical CF cylinder theory (documented in the file header) turns these
     ten exact enclosures into the exact CF prefix: each bracket pins one more
     partial quotient, and the semiconvergent bracket forces `a₉ = 23` rather
     than merely `a₉ ≥ 23`.

**Scoping:** the memo's test 4 (the chain-restricted recursion reproducing
`k(n)` and `M_n`) is a float64 *measurement*, not exact arithmetic, and is
deliberately not formalized — as is the real-slope LP itself (only its exact
rational/pairwise content). Axiom bases: `[propext, Quot.sound]` for the LP
theorems and `deltaK_not_balanced`; **no axioms at all** for
`deltaK_max_imbalance_is_two`, `log2Three_convergents` and
`log2Three_cf_certified`.

## What is proved (plain language) — contraction onset

Source: `contribution/packets/2026-07-24-contraction-onset/`
`COLLATZ_CONTRACTION_ONSET.md`, §3–§7 (the setup, Lemmas 1–2, the onset
Theorem, and the logical form of the Corollary), cross-checked against
`verify_contraction_onset.py`. The packet itself records (its 25 July 2026
priority correction) that this content is Terras (1976) refreshed à la
Garner (1981); what is formalized is the packet's own statement/proof chain.
The file `Formal/ContractionOnset.lean` proves, in namespace
`CollatzAtlas.ContractionOnset`:

1. **A computable exact 2-adic valuation.** `v2 n` (fuelled factor
   stripping) with `v2_spec`: `n = 2^(v2 n) · (n / 2^(v2 n))` and the
   cofactor is odd, for every `n > 0`. The accelerated Syracuse map is
   `syracuse x = (3x+1) / 2^(v2 (3x+1))`, with `syracuse_spec`
   (`2^(v2(3x+1)) · S(x) = 3x+1`) and `syracuse_odd` (it lands on odd
   numbers).
2. **Glue with the Terras formalism.** `syracuse_eq_iterT` — one Syracuse
   step from an odd `x` is exactly `v2(3x+1)` Terras steps (the odd branch
   `x ↦ (3x+1)/2` followed by halvings), and `iterS_eq_iterT` — `h`
   accelerated steps are exactly `A_h(x)` Terras steps (reusing
   `Terras.iterT` and `CollatzAtlas.Collision.iterT_add`).
3. **The telescoping cocycle** (`cocycle_identity`) — the packet's central
   identity in the exact integer form the verifier checks 600 000 times:
   `2^(valA h x) * iterS h x = 3^h * x + corrC h x`, where `valA`/`corrC`
   are the cumulative valuation `A_h` and the offset recurrence
   `C₀ = 0, C_{h+1} = 3C_h + 2^(A_h)`. Induction on `h`; the packet's
   oddness restriction is unnecessary and dropped.
4. **Lemma 1, descent requires contraction** (`descent_requires_contraction`,
   Terras's `κ(n) ≤ σ(n)`): for `h ≥ 1`, `S^h(x) < x` forces
   `3^h < 2^(A_h)` — the offset `C_h ≥ 1` (`one_le_corrC`) is strictly
   positive, so a descent puts the homogeneous multiplier below `1`.
5. **Lemma 2, the offset bound before onset** (`corrC_bound`): if no
   `j < h` is contracting then `C_h ≤ h·3^(h-1)`, by direct induction on the
   offset recurrence.
6. **The onset bound** (`aStar`, `aStar_spec`, `aStar_min`, `M`, `M_le`,
   `onset_bound`): `A*(h)` is the least exponent with `3^h < 2^(A*(h))`
   (the packet's `bit_length(3^h)`), specified by minimality;
   `M h = h·3^(h-1) / (2^(A*(h)) − 3^h)`; and the Theorem — if `h` is the
   *first* contracting index of `x` and `S^h(x) ≥ x`, then `x ≤ M(h)` —
   proved exactly as the memo does: the cocycle gives
   `x·(2^(A_h) − 3^h) ≤ C_h ≤ h·3^(h-1)` and minimality of `A*` gives
   `2^(A_h) − 3^h ≥ 2^(A*(h)) − 3^h > 0`.
7. **The Corollary's logical skeleton** (`no_contracting_in_window`): if
   `x` never descends below itself on a window `1 ≤ j ≤ H` and `M(j) < x`
   there, no index in the window is contracting — strong induction extracts
   the first contracting index and the Theorem contradicts `M(h) < x`.

**Sanity checks closed by `decide`:** the named controls `x = 3` (descends
and contracts at `h = 2`) and `x = 7` (at `h = 4`) with non-contraction at
all earlier indices; a concrete cocycle instance (`x = 27`, `h = 6`); and
the packet's exact `A*(h)`/`M(h)` tables pinned up to `h = 15 601`
(`aStar 15601 = 24727`, `M 15601 = 285814986`; `M(9616) + 1` is exactly the
verifier's scan bound `7 795 715`).

**Not formalized, and deliberately so:** the Corollary's numeric input
`max_{h ≤ 10^6} M(h) = 984 572 779 224 < 2^71` (a `10^6`-entry exact
computation owned by the Python verifier; the record row `h = 190 537` is
too slow for a kernel `decide`); Bařina's external `2^71` verification;
the Diophantine reading (`θ_h`, `log₂3`, irrationality measures) and the
"one-density ≥ log₃2" equivalence (real analysis, unstateable in plain
core); and the odd-`x` scan to `1.45 × 10⁹` (a finite computation, not a
proof). Axiom bases: `[propext, Quot.sound]` for the cocycle, both lemmas
and the Terras glue; the full classical triple for `onset_bound` and
`no_contracting_in_window` (`Classical.choice` enters through
`Nat.strongRecOn` and the well-founded machinery behind `Nat` division).

## What is proved (plain language) — cycle exclusion (verified-checker architecture)

Source: `contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md` (the fence doc,
m ≤ 18) and `contribution/packets/2026-07-23-cycle-exclusion-extension/`
(extension to m ≤ 20). The external exact pipeline scans ≈ 6.2×10⁸ valuation
words per phase with a dual-enumerator cross-check and finds no nontrivial
positive cycle with at most 20 odd members; that scan cannot run inside the
Lean kernel, so `Formal/CycleExclusion.lean` formalizes the
**verified-checker architecture**, in namespace `CycleExclusion`:

1. **The cycle equation.** `v2` / `U` / `iterU` define the 2-adic valuation
   and the odd-only map `U(n) = (3n+1)/2^{v2(3n+1)}` (fuel-bounded structural
   recursion, so everything is kernel-reducible); `v2_unique` pins the
   valuation by its divisibility-plus-odd-cofactor characterization.
   `affGo_spec` gives the closed form of the packet's affine recurrence
   (`C ↦ 3C + 2^S`, `S ↦ S + a`), and `wordIter_affine` lifts it along a
   realized valuation word. The main identity:
   * **`cycle_equation`** — any positive odd cycle of `U` with valuation word
     `a` (predicate `IsUCycleWord`) satisfies the exact Diophantine identity
     `n · 2^valSum a = 3^a.length · n + affC a`, i.e. the packet's
     `n = C_m / (2^K − 3^m)` cleared of denominators. `affC a` is exactly
     `Σ_j 3^{m−1−j}·2^{S_j}` and equals the verifier's accumulator
     (`affC_eq_affGo`, `valSum_eq_affGo`).
   * **`wordIter_eq_iterU` / `realizes_iterU`** — a realized word is literally
     a `U`-orbit segment, so the identity is proved *from the definition of
     the odd map*, not from an abstract surrogate.
2. **The verified exclusion checker.** `valuationWordExcluded : List Nat →
   Bool` is the exact negation of the external verifier's per-word
   fixed-point gate (`try_integral_fixed_point`: `2^K > 3^m`,
   `C_m % (2^K − 3^m) = 0`, odd quotient).
   * **`fixedPoint_of_equation`** — any positive odd solution of the cycle
     equation passes the gate.
   * **`valuationWordExcluded_sound`** — if the checker returns `true`, no
     positive odd integer solves the cycle equation for that word.
   * **`no_cycle_of_excluded`** — hence no positive odd `U`-cycle realizes an
     excluded word. Soundness holds for *every* word, of any length, with any
     entries (zeros included — a superset of the verifier's
     positive-composition domain).
3. **Kernel-checked layers.** `kernel_layer_m1/m2/m3/m4` evaluate the checker
   by `decide` on *every* word of length 1–4 with entries in `[1,32]`,
   `[1,16]`, `[1,8]`, `[1,8]`: each word is excluded except the constant word
   `[2,…,2]`, the valuation word of the trivial cycle `{1}` at every length —
   matching the external pipeline's `(1,2)` control. These are the atlas's
   first fully machine-verified exclusion layers. Measured wall-clock
   (toolchain v4.31.0, 2026-08-01): the three mission layers run in ≈ 0.2 s
   each; the m = 4 bonus layer (4,096 words) in ≈ 3.5 s; in-kernel `decide`
   stays feasible to ≈ 2×10⁴ words (m = 4, entries ≤ 12: 20,736 words in
   ≈ 17 s with `maxRecDepth 131072`) and hits the default 200,000-heartbeat
   elaborator wall at ≈ 3×10⁴ words (m = 5, entries ≤ 8). The full table is
   in the file's §5 comment block.
4. **Depth m ≤ 20 is external, by design** — documented in the file header:
   the packet's exclusion is established by the external exact pipeline with
   an independent dual-enumerator cross-check; the Lean checker is
   sound-but-not-yet-run at that depth, i.e. it is the kernel-side half of a
   future certificate-import architecture. Only the `decide` layers above are
   kernel-verified here.

Axiom bases: `cycle_equation` uses `[propext]` only; the checker/soundness
chain uses `[propext, Quot.sound]`; all four kernel layers use **no axioms at
all** (`decide` only, no `Lean.ofReduceBool`).

## Provenance: relationship to the formal-conjectures draft

`Formal/TwoBranchFamily.lean` is a port of
`collatz-lean-assessment/TwoBranchFamily.lean`, the draft statement file for
a future `google-deepmind/formal-conjectures` contribution. The draft
targets mathlib and uses `sorry` for all proofs; here every `sorry` is
replaced by a real, compiling proof. Statement content is unchanged; the
port required only these mechanical, meaning-preserving substitutions
(because mathlib symbols do not exist in Lean 4 core):

| draft (mathlib)                  | here (core)                          | equivalence (mathlib lemma) |
|----------------------------------|--------------------------------------|-----------------------------|
| `if Even n then … else …`        | `if n % 2 = 0 then … else …`         | `Nat.even_iff`              |
| `S b^[k] n` (`Function.iterate`) | `orbit b n k` (primitive recursion)  | `Function.iterate`          |
| `x ∈ Finset.Icc 1 b`             | `1 ≤ x ∧ x ≤ b`                      | `Finset.mem_Icc`            |

The draft's `@[category research solved, AMS 11 37]` and
`@[category API, AMS 11 37]` attributes (defined in `FormalConjecturesUtil`)
are recorded as comments above each theorem and must be restored verbatim on
contribution. Note also that the draft's theorems assume only `0 < b` —
oddness of `b` is part of the surrounding narrative (the family mimics
Collatz for odd `b`), not of the proved statements; the proofs here are
valid for every positive `b`.

## Remaining `sorry`s

**None.** All four TwoBranchFamily theorems, all six support lemmas, the
Terras bijection (`terras_bijection`, `rho_correct`, `terras_affine` plus
the induction chain) and the three collision-principle theorems compile with
empty axiom bases beyond the classical triple.

This is now **machine-checked rather than asserted**: every one of the 16
public declarations carries a `#print axioms` line, so `lake build` prints
the full audit and any future `sorry` would surface as `sorryAx` in the
build log. Measured on toolchain v4.31.0, 2026-07-24:

| Axiom base | Declarations |
|---|---|
| none at all | `orbit_add`, `orbit_succ` |
| `[propext, Quot.sound]` | `terras_bijection`, `rho_correct`, `terras_affine`, `states_eq_of_block_eq`, `orbit_shift_eq`, `collision_forces_large_state`, `S_lt_of_lt`, `S_pos`, `twoBranch_invariant`, `orbit_in_band`, `twoBranch_enters_finite_set` |
| full classical triple | `twoBranch_eventually_periodic`, `twoBranch_periodic_tail`, `exists_eq_of_forall_lt` |

Note that most of the file is *stronger* than the README previously
claimed: only the three pigeonhole-dependent results reach for
`Classical.choice` at all, and two results use no axioms whatsoever. Not-yet-formalized parts of
Theorem 4's prose (decidability of point-to-point reachability; the
machine-simulation definition behind "step-faithfully simulates") are
documentation-level claims, not statements in the draft file; they are
tracked as future work in the atlas, not hidden as `sorry`s here.

## Counterexample watch

Nothing in the TwoBranchFamily certificate bears on the `a = 3` (Collatz)
case: the descent lemma `S_lt_of_lt` rests on multiplier `1 < 2`, and the
file contains no claim about `3n + 1`. The Terras bijection is a structural
fact about parity cylinders — it constrains where a counterexample could
live (every parity word is realized by exactly one residue class), not
whether one exists. No anomaly observed.
