# Provenance

Per-packet record of who directed the work, which model executed it, what
independent check was run, and over which commits. Roles are defined in
[`CONTRIBUTORS.md`](CONTRIBUTORS.md).

**Why this file exists.** The repository is model-executed. An external reader
cannot weigh a claim without knowing which mechanical guarantee stands behind
it. "Verified" here always means a named check that was actually run, never a
reassurance.

## Verification vocabulary

Use these terms exactly. Anything else is not a verification claim.

| Term | Means |
|---|---|
| `exact` | every acceptance decision is integer or `Fraction` arithmetic; no float on the certificate path |
| `independent re-implementation` | a second computation of the same quantity sharing only input bits with the first — a different algorithm, not a re-run |
| `second model` | a different model family re-derived the formula or audited the packet |
| `machine-checked` | Lean 4 build with `#print axioms`; `sorryAx` absent from the build log |
| `measurement` | float64 output; never a premise for any later claim |
| `cited` | a classical result used as input, not proved here |

## Packet record

| Packet | Direction | Executed by | Independent check | Commits |
|---|---|---|---|---|
| `proofs/` (fold, Terras, realizability, fence) | Ben Pham | Claude Fable 5 | second implementation of the counting-law screen; 196/196 direct enumeration match | pre-`8861f9e` |
| `2026-07-22-landmark-pointwise` | Ben Pham | Claude Fable 5 | DGG counterexample certificate independently verified | pre-`8861f9e` |
| `2026-07-22-automatic-transcript-rigidity` | Ben Pham | Claude Fable 5 | exact `Fraction` eigenvectors; Φ-engine cross-checked against true orbits mod 2⁶⁴ | pre-`8861f9e` |
| `2026-07-22` analytic packets (drift wall, Fourier, plateau, structure–randomness) | Ben Pham | Claude Fable 5 | exact controls per packet; all disclaim beating Tao | pre-`8861f9e` |
| `2026-07-23-cycle-exclusion-extension` | Ben Pham | Codex / GPT-5.6 | dual-enumerator scan, two phases, 1.24 × 10⁹ word-scans | `eb81928` |
| `2026-07-23-plateau-drift-test` | Ben Pham | Claude Fable 5 | C kernel vs numpy fallback, bit-identity gated | `6541c48` |
| `2026-07-24-streaming-depth-21` | Ben Pham | Claude Fable 5 | bit-identity against the n = 18 and n = 20 certificates | `be1b001` |
| `formal/` Lean certificates | Ben Pham | Claude Fable 5 | `lake build` + `#print axioms` on all 16 public declarations | `a9aba08`, `c1aa86c` |
| `2026-07-24-supercritical-automatic-closure` | Ben Pham | Claude Opus 5 | exact factor sets cross-checked against brute-force prefix enumeration; two independent Φ engines (lift cocycle vs modular series) agreeing on 2 000 orbits | `c1aa86c` |
| `2026-07-24-contraction-onset` | Ben Pham | Claude Opus 5 | Lemma 1 checked on 9 998 observed first descents; cocycle identity on 600 000 instances; `M(h)` recomputed to 10⁶ in a separate run | `ae60d4a` |
| `TARGETS.md`, target-3 saturation probe | Ben Pham | Claude Opus 5 | probe reuses the packet's exact factor-language machinery; result contradicted the author's own prior estimate and is recorded as such | `f1e26e7`, `e29eb09` |
| `test_f2.py` cylinder-check rewrite | Ben Pham | Claude Opus 5 | new predicate compared against the old one on 4 000 random families, 3 255 containing a genuine overlap | `9353bdf` |
| Attribution layer, `COUNTEREXAMPLE_SHAPE.md`, `meta/` | Ben Pham | Claude Opus 5 | four independent subagents: literature transfer, Bayesian audit, GEB audit, code-quality skill | this commit |

## External inputs consumed, not proved

| Result | Source | Used by |
|---|---|---|
| every `n < 2^71` reaches 1 | Bařina 2025 | contraction-onset corollary |
| no nontrivial cycle with ≤ 91 local minima | Hercher 2023 | every cycle-branch bound |
| almost all orbits attain almost bounded values | Tao 2019/2022 | the amplification target |
| parity words ↔ residues mod 2^L | Terras 1976 | everything |
| 2-adic conjugacy to the shift | Bernstein–Lagarias 1996 | the realizability wall |
| uniform frequencies of primitive substitutions | Queffélec; Allouche–Shallit §8.4 | the ρ-variant of the supercritical closure |
| rationality of automatic letter frequencies | Cobham 1972 | rigidity packet Lemma B |

## Known provenance defects

Recorded rather than quietly fixed, because a claim-sensitive project should
show its corrections.

1. **The "2-automatic" label is too broad.** The rigidity packet enumerates
   uniform morphisms of length ℓ ≤ 4 on two letters and calls the whole sweep
   2-automatic. For ℓ = 3 those fixed points are 3-automatic, and by Cobham's
   1969 theorem not 2-automatic unless eventually periodic. The *exclusions*
   are unaffected — Corollaries 4 and 7 need aperiodicity, `Φ(q) ∈ ℚ_odd` and a
   complexity bound, never automaticity — but the class label needs repair in
   that packet and in the headline phrase "99 of 109 supercritical 2-automatic
   survivors".
2. **ΔAIC was reported as model-selection evidence.** `ΔAIC = N·ln(SSR ratio)`
   identically, so the number was the residual ratio in a likelihood costume,
   over 16 highly correlated points from a deterministic computation with no
   sampling noise. `STATE.md` now reports the SSR ratio and the caveat.
   Corrected this commit.
3. **`STATE.md` dates drifted** — it was headed 2026-07-23 while carrying
   2026-07-24 results.
4. **No priority search has been run for any result.** Every packet says so
   individually. Novelty is therefore unestablished, not established.

## Rule for future packets

A packet is not complete until it appears in this table with a named
independent check. "Ran the verifier twice" is not a check. If no independent
check exists, write `none` — an honest gap is auditable, an implied check is
not.
