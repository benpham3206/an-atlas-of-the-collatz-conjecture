# Complete research packet — 2026-07-22

Landmark-strategy + pointwise-theorem research packet for the fixed `3n+1`
Collatz / Terras map. **This packet does not claim a proof or counterexample
of the Collatz conjecture.**

## Artifact map

| Requested artifact | File(s) |
|---|---|
| Full landmark-strategy and pointwise-theorem memo | [`COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`](COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md) |
| Companion landmark-strategies write-up | [`LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md`](LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md) |
| Detailed proof/counterexample strategy machine | [`collatz_strategy_machine.dot`](collatz_strategy_machine.dot) · [`.svg`](collatz_strategy_machine.svg) · [`.png`](collatz_strategy_machine.png); flow: [`collatz_strategy_flow.*`](collatz_strategy_flow.dot) |
| Collatz resonance lattice | [`collatz_resonance_lattice.svg`](collatz_resonance_lattice.svg) · [`.png`](collatz_resonance_lattice.png); table: [`collatz_resonance_table.csv`](collatz_resonance_table.csv) · [`.txt`](collatz_resonance_table.txt) |
| Prefix-return barrier | [`COLLATZ_PREFIX_RETURN_BARRIER.md`](COLLATZ_PREFIX_RETURN_BARRIER.md) |
| Rational-state finite verifier | [`verify_rational_complexity_finite.py`](verify_rational_complexity_finite.py) · [`.out`](verify_rational_complexity_finite.out); Lean blueprint: [`COLLATZ_RATIONAL_COMPLEXITY_LEAN_BLUEPRINT.md`](COLLATZ_RATIONAL_COMPLEXITY_LEAN_BLUEPRINT.md) |
| Related finite checks | [`verify_complexity_pressure.py`](verify_complexity_pressure.py) · [`verify_dgg_counterexample.py`](verify_dgg_counterexample.py) |

## Related Codex best attempt (same research arc)

Exact odd-only cycle exclusion and rational-shadow work live next to the
existing fence code, not inside this packet directory:

| Result | Path |
|---|---|
| No nontrivial positive cycle with ≤ 18 odd members | [`../../proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`](../../proofs/EXACT_COUNTEREXAMPLE_SEARCH.md) |
| Engine + tests + JSON | [`../../code/fence/exact_cycle_search.py`](../../code/fence/exact_cycle_search.py) |
| Rational 2-adic shadows of aperiodic laws | [`../../proofs/RATIONAL_IRRATIONAL_SHADOW.md`](../../proofs/RATIONAL_IRRATIONAL_SHADOW.md) |
| Primitive uniform subcritical obstruction | [`../../proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md`](../../proofs/PRIMITIVE_UNIFORM_OBSTRUCTION.md) |

Kimi / external-agent one-pager: [`../../../COLLATZ_ONE_PAGE.md`](../../../COLLATZ_ONE_PAGE.md).
