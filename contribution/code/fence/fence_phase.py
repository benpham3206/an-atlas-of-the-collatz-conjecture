"""Exact finite phase scan for two-branch maps T_{a,b}.

This is an empirical classifier, not a convergence or divergence prover.  Every
reported transition and cycle uses Python integers; the only unresolved exits
are the explicit step and bit-length caps below.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


GRID = (1, 3, 5, 7, 9)
SEED_STOP = 1_000_000
STEP_CAP = 10_000
BIT_LENGTH_CAP = 64
MEMO_VALUE_CAP = 1_000_000_000
WITNESS_LIMIT = 3

HIT_ONE = 1
HIT_NONTRIVIAL_CYCLE = 2
UNRESOLVED = 3


def step(n: int, a: int, b: int) -> int:
    """Apply T_{a,b} on the positive integers."""
    if n < 1:
        raise ValueError(f"n must be positive, got {n}")
    if a < 1 or b < 1 or a % 2 == 0 or b % 2 == 0:
        raise ValueError(f"a and b must be positive odd integers, got {(a, b)}")
    if n % 2 == 0:
        return n // 2
    numerator = a * n + b
    if numerator % 2:
        raise AssertionError("odd branch was not integral")
    return numerator // 2


def canonical_cycle(cycle: Iterable[int]) -> tuple[int, ...]:
    """Return the lexicographically least rotation of a nonempty cycle."""
    values = tuple(cycle)
    if not values:
        raise ValueError("cycle must be nonempty")
    return min(values[i:] + values[:i] for i in range(len(values)))


def verify_cycle(cycle: Iterable[int], a: int, b: int) -> bool:
    values = tuple(cycle)
    return bool(values) and all(
        step(values[i], a, b) == values[(i + 1) % len(values)]
        for i in range(len(values))
    )


def trace_unresolved_witness(
    seed: int,
    a: int,
    b: int,
    *,
    step_cap: int,
    bit_length_cap: int,
) -> dict:
    """Re-run an unresolved seed without memo shortcuts and record its exact exit."""
    x = seed
    peak = x
    seen: dict[int, int] = {}
    for steps in range(step_cap + 1):
        if x == 1:
            raise AssertionError(f"purported unresolved seed {seed} reaches 1")
        if x in seen:
            raise AssertionError(f"purported unresolved seed {seed} repeats at {x}")
        if x.bit_length() > bit_length_cap:
            return {
                "seed": seed,
                "reason": "bit_length_cap",
                "steps": steps,
                "cutoff_value": x,
                "cutoff_bit_length": x.bit_length(),
                "peak": peak,
            }
        if steps == step_cap:
            return {
                "seed": seed,
                "reason": "step_cap",
                "steps": steps,
                "cutoff_value": x,
                "cutoff_bit_length": x.bit_length(),
                "peak": peak,
            }
        seen[x] = steps
        x = step(x, a, b)
        if x > peak:
            peak = x
    raise AssertionError("unreachable witness exit")


def classify_system(
    a: int,
    b: int,
    *,
    seed_stop: int = SEED_STOP,
    step_cap: int = STEP_CAP,
    bit_length_cap: int = BIT_LENGTH_CAP,
    memo_value_cap: int = MEMO_VALUE_CAP,
    witness_limit: int = WITNESS_LIMIT,
) -> dict:
    """Classify every seed in [1, seed_stop) under explicit finite caps."""
    if seed_stop <= 1:
        raise ValueError("seed_stop must exceed 1")

    # Reaching 1 is the target event, even when 1 is not fixed for this (a,b).
    memo: dict[int, int] = {1: HIT_ONE}
    counts = {HIT_ONE: 0, HIT_NONTRIVIAL_CYCLE: 0, UNRESOLVED: 0}
    cycles: set[tuple[int, ...]] = set()
    unresolved_seeds: list[int] = []

    for seed in range(1, seed_stop):
        x = seed
        path: list[int] = []
        positions: dict[int, int] = {}
        outcome = UNRESOLVED

        for _ in range(step_cap):
            known = memo.get(x)
            if known is not None:
                outcome = known
                break
            repeat_at = positions.get(x)
            if repeat_at is not None:
                cycle = canonical_cycle(path[repeat_at:])
                if not verify_cycle(cycle, a, b):
                    raise AssertionError(f"invalid cycle for {(a, b)}: {cycle}")
                cycles.add(cycle)
                outcome = HIT_NONTRIVIAL_CYCLE
                break
            if x.bit_length() > bit_length_cap:
                outcome = UNRESOLVED
                break
            positions[x] = len(path)
            path.append(x)
            x = step(x, a, b)
        else:
            outcome = UNRESOLVED

        counts[outcome] += 1
        if outcome == UNRESOLVED and len(unresolved_seeds) < witness_limit:
            unresolved_seeds.append(seed)
        for value in path:
            if value <= memo_value_cap:
                memo[value] = outcome

    witnesses = [
        trace_unresolved_witness(
            seed,
            a,
            b,
            step_cap=step_cap,
            bit_length_cap=bit_length_cap,
        )
        for seed in unresolved_seeds
    ]
    cycle_rows = [
        {"length": len(cycle), "values": list(cycle)} for cycle in sorted(cycles)
    ]

    if counts[UNRESOLVED]:
        label = "apparent-divergence"
    elif counts[HIT_NONTRIVIAL_CYCLE]:
        label = "cycles"
    else:
        label = "all-converge"

    return {
        "a": a,
        "b": b,
        "label": label,
        "seed_count": seed_stop - 1,
        "hit_one_count": counts[HIT_ONE],
        "nontrivial_cycle_basin_count": counts[HIT_NONTRIVIAL_CYCLE],
        "unresolved_count": counts[UNRESOLVED],
        "cycles": cycle_rows,
        "unresolved_witnesses": witnesses,
    }


def scan_grid(
    *,
    grid: tuple[int, ...] = GRID,
    seed_stop: int = SEED_STOP,
    step_cap: int = STEP_CAP,
    bit_length_cap: int = BIT_LENGTH_CAP,
    memo_value_cap: int = MEMO_VALUE_CAP,
) -> dict:
    rows = [
        classify_system(
            a,
            b,
            seed_stop=seed_stop,
            step_cap=step_cap,
            bit_length_cap=bit_length_cap,
            memo_value_cap=memo_value_cap,
        )
        for a in grid
        for b in grid
    ]
    return {
        "schema_version": 1,
        "map": "T(n)=n/2 if n even; T(n)=(a*n+b)/2 if n odd",
        "grid_a": list(grid),
        "grid_b": list(grid),
        "seed_interval": [1, seed_stop],
        "seed_interval_right_open": True,
        "step_cap": step_cap,
        "bit_length_cap": bit_length_cap,
        "memo_value_cap": memo_value_cap,
        "classification": {
            "all-converge": "all tested seeds reached 1 within the explicit caps",
            "cycles": "all tested seeds resolved and at least one entered a cycle not containing 1",
            "apparent-divergence": "at least one tested seed was unresolved at an explicit cap",
        },
        "finite_bound_caveat": (
            "No row proves convergence or divergence beyond the tested seeds and caps."
        ),
        "rows": rows,
    }


def markdown_table(result: dict) -> str:
    lines = [
        "# Exact finite phase table for two-branch affine maps",
        "",
        "For positive odd `a,b`, this scan applies `T(n)=n/2` on even `n` and "
        "`T(n)=(a*n+b)/2` on odd `n`. Every integer `1 <= n < 1,000,000` was "
        "classified with exact integer arithmetic.",
        "",
        "The labels are observations at the recorded caps, not asymptotic theorems:",
        "",
        "- `all-converge`: all tested seeds reached `1`.",
        "- `cycles`: every seed resolved, but some entered a cycle not containing `1`.",
        "- `apparent-divergence`: some seed exceeded the step or bit-length cap; this "
        "  does not prove divergence.",
        "",
        f"Caps: `{result['step_cap']}` new steps per path; current value unresolved "
        f"when bit length exceeds `{result['bit_length_cap']}`. The memoization cap "
        f"`{result['memo_value_cap']}` changes performance only, not classification.",
        "",
        "| a | b | label | hit 1 | nontrivial-cycle basin | unresolved | cycles (lengths) |",
        "|---:|---:|---|---:|---:|---:|---|",
    ]
    for row in result["rows"]:
        lengths = ", ".join(str(c["length"]) for c in row["cycles"]) or "none"
        lines.append(
            f"| {row['a']} | {row['b']} | {row['label']} | "
            f"{row['hit_one_count']} | {row['nontrivial_cycle_basin_count']} | "
            f"{row['unresolved_count']} | {lengths} |"
        )

    lines.extend(["", "## Exact cycle certificates", ""])
    for row in result["rows"]:
        if not row["cycles"]:
            continue
        lines.append(f"- `(a,b)=({row['a']},{row['b']})`: " + "; ".join(
            "(" + ", ".join(str(v) for v in cycle["values"]) + ")"
            for cycle in row["cycles"]
        ))

    lines.extend(["", "## Unresolved witnesses", ""])
    for row in result["rows"]:
        if not row["unresolved_witnesses"]:
            continue
        rendered = []
        for witness in row["unresolved_witnesses"]:
            rendered.append(
                f"seed {witness['seed']}: {witness['reason']} after "
                f"{witness['steps']} steps at {witness['cutoff_value']} "
                f"({witness['cutoff_bit_length']} bits), peak {witness['peak']}"
            )
        lines.append(f"- `(a,b)=({row['a']},{row['b']})`: " + "; ".join(rendered))

    lines.extend([
        "",
        "## Audit boundary",
        "",
        "The `(3,1)` row is only a bounded empirical `all-converge` row. Finite "
        "enumeration cannot establish the Collatz conjecture. Likewise, an unresolved "
        "orbit is only a cap witness, never a divergence certificate.",
        "",
    ])
    return "\n".join(lines)


def contains_float(value: object) -> bool:
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(contains_float(k) or contains_float(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return any(contains_float(item) for item in value)
    return False


def write_outputs(result: dict, output_dir: Path) -> None:
    if contains_float(result):
        raise AssertionError("float found in exact result")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "phase_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "PHASE_TABLE.md").write_text(markdown_table(result), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="scan seeds 1..999")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    result = scan_grid(seed_stop=1_000 if args.quick else SEED_STOP)
    write_outputs(result, args.output_dir)
    labels: dict[str, int] = {}
    for row in result["rows"]:
        labels[row["label"]] = labels.get(row["label"], 0) + 1
    print(
        f"rows={len(result['rows'])} seeds_per_row={result['rows'][0]['seed_count']} "
        f"labels={json.dumps(labels, sort_keys=True)} floats={contains_float(result)}"
    )


if __name__ == "__main__":
    main()
