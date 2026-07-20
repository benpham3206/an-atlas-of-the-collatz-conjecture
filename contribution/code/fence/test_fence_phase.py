"""Targeted checks for the exact finite fence phase scan."""

from __future__ import annotations

import json
from pathlib import Path

from fence_phase import (
    BIT_LENGTH_CAP,
    GRID,
    SEED_STOP,
    STEP_CAP,
    canonical_cycle,
    classify_system,
    contains_float,
    step,
    verify_cycle,
)


HERE = Path(__file__).parent


def naive_label(a: int, b: int, seed: int, *, step_cap: int, bit_cap: int) -> int:
    x = seed
    seen: set[int] = set()
    for _ in range(step_cap):
        if x == 1:
            return 1
        if x in seen:
            return 2
        if x.bit_length() > bit_cap:
            return 3
        seen.add(x)
        x = step(x, a, b)
    return 3


def test_integrality_and_positivity() -> None:
    for a in GRID:
        for b in GRID:
            for n in range(1, 2_000, 2):
                got = step(n, a, b)
                assert got == (a * n + b) // 2
                assert got > 0


def test_canonical_cycle_and_closure() -> None:
    assert canonical_cycle((6, 3)) == (3, 6)
    assert canonical_cycle((5, 8, 4, 2, 1)) == (1, 5, 8, 4, 2)
    assert verify_cycle((1,), 1, 1)
    assert verify_cycle((3,), 1, 3)
    assert not verify_cycle((3, 6), 1, 3)


def test_small_optimized_counts_match_naive() -> None:
    seed_stop = 500
    for a, b in ((1, 7), (3, 5), (5, 1), (9, 9)):
        result = classify_system(
            a,
            b,
            seed_stop=seed_stop,
            step_cap=500,
            bit_length_cap=40,
            memo_value_cap=10_000,
        )
        expected = {1: 0, 2: 0, 3: 0}
        for seed in range(1, seed_stop):
            expected[naive_label(a, b, seed, step_cap=500, bit_cap=40)] += 1
        assert result["hit_one_count"] == expected[1]
        assert result["nontrivial_cycle_basin_count"] == expected[2]
        assert result["unresolved_count"] == expected[3]


def test_full_result_readback() -> None:
    path = HERE / "phase_results.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["grid_a"] == list(GRID)
    assert result["grid_b"] == list(GRID)
    assert result["seed_interval"] == [1, SEED_STOP]
    assert result["step_cap"] == STEP_CAP
    assert result["bit_length_cap"] == BIT_LENGTH_CAP
    assert len(result["rows"]) == 25
    assert not contains_float(result)
    assert {(row["a"], row["b"]) for row in result["rows"]} == {
        (a, b) for a in GRID for b in GRID
    }
    for row in result["rows"]:
        assert row["seed_count"] == 999_999
        assert (
            row["hit_one_count"]
            + row["nontrivial_cycle_basin_count"]
            + row["unresolved_count"]
            == row["seed_count"]
        )
        expected_label = (
            "apparent-divergence"
            if row["unresolved_count"]
            else "cycles"
            if row["nontrivial_cycle_basin_count"]
            else "all-converge"
        )
        assert row["label"] == expected_label
        for cycle in row["cycles"]:
            values = tuple(cycle["values"])
            assert cycle["length"] == len(values)
            assert values == canonical_cycle(values)
            assert verify_cycle(values, row["a"], row["b"])


def main() -> None:
    tests = [
        test_integrality_and_positivity,
        test_canonical_cycle_and_closure,
        test_small_optimized_counts_match_naive,
        test_full_result_readback,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} tests")


if __name__ == "__main__":
    main()
