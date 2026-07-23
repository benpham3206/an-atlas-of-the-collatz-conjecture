# Provenance — shadow-barrier packet

- **Source:** chatgpt-thread-1784792218410 (ChatGPT 5.6 Sol, two-metric shadow-barrier note + exact verifier). Copied verbatim from `/Users/benjaminpham/Documents/Codex/2026-07-23/referenced-chatgpt-conversation-this-is-untrusted/outputs/` on 2026-07-23; originals unmodified. The `.DS_Store` in the source directory is not an artifact and was skipped.
- **Status:** EXPLORATORY. Not a proved contribution to the atlas. The main theorem (Theorem 2) is conditional on the existence of a nonperiodic orbit with `T^L(N) >= N` for every `L`, and the packet constructs no orbit, no cycle, and no infinite-path exclusion.
- **Date integrated:** 2026-07-23.

## Independent rerun verdict

Reran `collatz_shadow_barrier_verify.py --max-length 12` with the managed
Python 3.12.13 interpreter on 2026-07-23. Wall time 13.6 s. Exit code 0,
`all_checks_passed: true`, `failures: []`. The regenerated JSON is
byte-identical to the committed `collatz_shadow_barrier_results.json`:
8,190 parity words through length 12 (sum of `2^L`, L = 1..12), 6,423
contractive, 1,767 expansive, counts consistent (6,423 + 1,767 = 8,190).
The memo's claims about what the verifier does match what the code actually
does. All arithmetic in the verifier is exact (`int` / `fractions.Fraction`);
no floats anywhere in the certified path.

## Adversarial read-back: gaps between this theorem and Collatz progress

- **Conditional, not constructive.** Theorem 2 assumes an `N` with a nonperiodic orbit satisfying `T^L(N) >= N` for all `L`. No such `N` is constructed or shown to exist; every conclusion about `x_L` is vacuous unless a divergent least counterexample exists.
- **Cylinder pruning is not orbit control.** Equation (4) removes an arithmetic progression from the *divergent least-counterexample search* only. It does not remove the parity word (the Terras bijection guarantees every word occurs), and it bounds nothing about excursions of surviving starts.
- **Parity shadows preserve parity, not statistics.** The shadow shares the finite parity word but does not preserve real-valued record height, stopping time, or Benford data — the memo itself concedes this. So `x_L -> N` 2-adically says nothing about orbit statistics of `N`.
- **The two-metric split is the realizability wall restated.** Any rational with odd denominator can impersonate any finite parity prefix (Bernstein/Terras bijection). "Real blow-up vs 2-adic convergence" of the shadow sequence is a consequence of the *assumed* counterexample, not new control over actual integer orbits.
- **Near-neutrality is assumed, not proved.** The blow-up (8) requires a contractive subsequence with `3^{s_L}/2^{L} -> 1`. Whether any hypothetical divergent orbit has such a subsequence is open; the theorem does not establish it.
- **No improvement on known exclusion bounds.** Verifying all words through length 12 does not extend the classical lower bounds on nontrivial cycle length (via continued fractions of `log 3 / log 2`) or the verified convergence range; the pruning criterion is a finite restatement of Terras-style descent.
- **Cycle branch untouched.** The gate `D_L | c_w` for periodic points is the standard fixed-point congruence; no new cycle is excluded and no existing cycle result is sharpened.
- **Verifier is one implementation, not three.** The cross-checks share utility code (the memo states this openly). The JSON is finite evidence that the code implements the formulas; the symbolic proof carries the infinite claims, and that proof has not been independently re-reviewed here.
- **Exponential coverage ceiling.** Exact verification cost grows as `2^L`; length 12 already takes ~13.6 s, so this exact-verifier path does not scale toward the infinite-path statement ("every path eventually enters a deletable cylinder") that the memo itself names as the missing well-foundedness theorem.
