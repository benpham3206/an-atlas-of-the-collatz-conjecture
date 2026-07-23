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

**None.** All four TwoBranchFamily theorems, all six support lemmas, and
the Terras bijection (`terras_bijection`, `rho_correct`, `terras_affine`
plus the induction chain) compile with empty axiom bases beyond the
classical triple. Not-yet-formalized parts of
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
