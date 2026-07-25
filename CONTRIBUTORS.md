# Contributors

This repository is human-directed and model-executed. That split is the point,
not an embarrassment, and it is recorded precisely so that an external reader
knows which quality guarantee applies to which artifact.

## Roles

| Role | Who | What it covers |
|---|---|---|
| **Direction, target selection, acceptance** | Ben Pham | Which problem, which target, which route to kill. Every decision about what counts as progress. Final gate on every claim. |
| **Certificate generation, formalization, enumeration** | Claude (Anthropic), GPT-5.x (OpenAI) | Proof drafting, exact-arithmetic verifiers, Lean formalization, exhaustive enumeration, packet prose. |
| **Independent verification** | a second model, or a second implementation | Re-derivation of load-bearing formulas, second implementations that share only input bits, adversarial audit of a completed packet. |

Model contributions are recorded per commit with a `Co-Authored-By` trailer
and per packet in [`PROVENANCE.md`](PROVENANCE.md).

## What this means for a reader

**The human is the acceptance gate, not the prover.** Direction, scope, kill
criteria and the decision to publish are human. Most derivation and all
implementation are model work.

**Therefore the primary quality guarantees are mechanical, not authorial:**

1. every acceptance decision runs on exact integer or rational arithmetic;
2. every load-bearing computation has an independent re-implementation;
3. every packet states kill criteria *before* the build and reports whether
   they fired;
4. certificates are deterministic and replayable from inputs, not from stored
   values;
5. Lean certificates carry `#print axioms` output, so a `sorry` would surface
   in the build log;
6. float64 output is labelled a measurement everywhere it appears.

An external reader should weight those six mechanisms, and the recorded
provenance, above the authorship of any prose.

**What none of that replaces.** Expert review, a novelty comparison against
the literature, and a referee. The repository has internal validation only.
Several results are re-derivations of classical facts (Terras, the
Bernstein–Lagarias conjugacy); novelty is claimed only for the new
consequences and screens, and only where a priority search is recorded — which
so far it is not, anywhere.

## Attribution norms

- Classical results are cited to their authors, never claimed.
- A model-drafted proof that a human accepted is still model-drafted; the
  commit trailer says so.
- "Independent verification" means a *different implementation path or a
  different model*, and the packet says which. Re-running the same script is
  not verification.
- No packet may claim multi-agent effort, elapsed time, or an independent
  check that was not actually performed. This has its own kill-criterion entry
  in [`HAIL_MARY_PROMPT.md`](HAIL_MARY_PROMPT.md) §7 because it is a live
  failure mode for model-written research.

## Citation

If you cite this repository, cite it as a *research programme with an exact
certificate layer*, not as a peer-reviewed result. The Collatz conjecture
remains open; nothing here proves or disproves it.
