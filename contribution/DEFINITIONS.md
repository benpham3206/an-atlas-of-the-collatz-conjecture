# DEFINITIONS — the fold program's ledger of primitives

**Rule (the Euclid discipline):** a term enters when a probe produces an object we
can only describe by circumlocution. Entry = name, tentative definition, and the
computation that forced it. A term earns **permanent** status only when
load-bearing in ≥ 2 independent results. At ~10 permanent entries, attempt the
axiomatization pass — as a Lean library (CollatzFormal/ skeleton exists), not prose.
Axioms are compressed hindsight; they come last.

| # | Name | Tentative definition | Forced by | Status |
|---|---|---|---|---|
| 1 | **drift** (Ben: "hyper-momentum") | for a parity word with a ones, b zeros: D = a·log(3/2) − b·log 2; the orbit's displacement in log-scale | F1 stopping-time spectrum; identical to Antihydra's halting statistic (odd-count vs even-count balance) | candidate |
| 2 | **inertia** (Ben: "hyper-inertia") | length of the maximal forced parity run from n; equals ν₂(n+1) for odd-run inertia (Mersenne n = 2^k−1 attains the max k at its scale) | F1 extremal-word atlas (D5) | candidate |
| 3 | **fold** | the operator (T, class r mod 2^k) ↦ induced first-return map, renormalized to ℕ; branches exact-affine | F2 spec; the object F3 found no literature name for | candidate |
| 4 | **unresolved mass** | Σ 2^(−s) over DFS leaves where return is undecided at cap; the exact measure of what a truncated fold does not see | F2 corrected spec (attempt-3 budget accounting) | candidate |
| 5 | **collapse** | two folds at different depths with identical resolved canonical forms (affine over ℤ, NOT merely topological — topological conjugacy is provably lossy: T on ℤ₂ is the full shift) | F2 collapse search; the topology-reframe discussion | candidate |
| 6 | **realizability** | the constraint selecting, from the free composition object, the single word per n that parity feedback executes; free versions (matrix semigroup of branch matrices `[[1/2,0],[0,1]]`, `[[3/2,1/2],[0,1]]`; grammar closure; tensor-train contraction; Berg–Meinardus linear functional equation) are each tame/charted — imposing realizability is what makes each one Collatz | every reframe attempted 2026-07-18 hit this same rock (eml genre, matrix semigroup, Koopman/Berg–Meinardus, tensor networks); Opfer 2011's failed proof died at its spectral avatar | candidate — **currently the strongest unifier in the ledger** |

Rejected vocabulary (named, not built — fonts): "hyper-fluid" as transfer-operator
density flow = the exhausted ergodic continent (CLAUDE.md §1); phenomenological
orbit-interiority = prose lane, routes to Meta-Writing.
