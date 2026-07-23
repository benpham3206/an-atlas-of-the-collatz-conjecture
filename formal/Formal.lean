/-
Collatz atlas — formal certificates (library root).

Plain Lean 4 core only; no mathlib.  Modules:

* `Formal.Pigeonhole` — bespoke pigeonhole principle for `Nat` sequences.
* `Formal.TwoBranchFamily` — the `a = 1` two-branch family `S_b` is
  non-universal (PARTIAL_THEOREMS.md, Theorem 4), fully proved.
* `Formal.TerrasBijection` — parity words of length `k` biject with
  residues mod `2^k` (PARTIAL_THEOREMS.md, Theorem 1), fully proved.
-/
import Formal.Pigeonhole
import Formal.TwoBranchFamily
import Formal.TerrasBijection
