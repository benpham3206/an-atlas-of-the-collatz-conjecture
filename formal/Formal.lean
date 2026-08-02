/-
Collatz atlas — formal certificates (library root).

Plain Lean 4 core only; no mathlib.  Modules:

* `Formal.Pigeonhole` — bespoke pigeonhole principle for `Nat` sequences.
* `Formal.TwoBranchFamily` — the `a = 1` two-branch family `S_b` is
  non-universal (PARTIAL_THEOREMS.md, Theorem 4), fully proved.
* `Formal.TerrasBijection` — parity words of length `k` biject with
  residues mod `2^k` (PARTIAL_THEOREMS.md, Theorem 1), fully proved.
* `Formal.CollisionPrinciple` — a repeated length-`k` parity block in an
  orbit that is not eventually periodic forces a state `≥ 2^k`
  (landmark packet, Lemmas 1–2 / Theorem 4.1), fully proved.
* `Formal.ChainClosure` — chain closure identity for the Syracuse Fourier
  recursion (packet `2026-07-22-syracuse-fourier`, Theorem 1): `2^k · u_a ≡
  2^{k-a} (mod 3^{n+1})`, the exponent homomorphism `ℤ → units`, the Euler
  period bound `2^{2·3^n} ≡ 1 (mod 3^{n+1})`, and support closure of the
  chain subsystem, all fully proved.
* `Formal.ContractionOnset` — Syracuse cocycle identity, descent-requires-
  contraction, correction-term bound, and the `M(h)` onset theorem
  (packet `2026-07-24-contraction-onset`), fully proved.
* `Formal.BeattyKill` — the Beatty kill triple for the chain-exponent law
  (packet `2026-08-01-chain-exponent-law`, §2–§4): rational-slope Beatty
  infeasibility with any phase (kill criterion (a)), Sturmian balance failure
  of the jump word `Δk` (kill criterion (b), specific finite check plus a
  general double-factor lemma), and the CF prefix `[1;1,1,2,2,3,1,5,2,23]` of
  `log₂ 3` certified by exact `Nat` exponent comparisons, all fully proved.
* `Formal.CycleExclusion` — the cycle equation `n·2^K = 3^m·n + C_m` for
  odd-only cycles proved from the definition of `U`, a sound Boolean
  per-word exclusion checker matching the external verifier's gate, and
  kernel-checked exclusion layers for word lengths m ≤ 4 (fence doc +
  packet `2026-07-23-cycle-exclusion-extension`), all fully proved.
-/
import Formal.Pigeonhole
import Formal.TwoBranchFamily
import Formal.TerrasBijection
import Formal.CollisionPrinciple
import Formal.ChainClosure
import Formal.ContractionOnset
import Formal.BeattyKill
import Formal.CycleExclusion
