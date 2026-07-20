"""
F4 tests — plain asserts, stdlib-runnable (also pytest-compatible).

Run:
    python3 fold/test_f4.py
    # or from fold/:
    python3 test_f4.py
"""

from __future__ import annotations

import os
import random
import sys
import time
import traceback

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from f4_feature_regression import (  # noqa: E402
    BASELINE_BUDGETS,
    budget_of_spaces,
    build_feature_registry,
    compute_labels,
    enumerate_feature_sets,
    leaderboard,
    run_baselines,
    run_experiment,
    run_feature_sets,
    sigma,
    sigma_direct_simulation,
    train_test_ranges,
    value_space_sizes,
)


class Results:
    def __init__(self) -> None:
        self.sections: list[dict] = []

    def record(self, name: str, status: str, runtime_s: float, detail: str = "") -> None:
        self.sections.append(
            {"name": name, "status": status, "runtime_s": runtime_s, "detail": detail}
        )
        print(f"[{status}] {name}  ({runtime_s:.3f}s)  {detail}")


def test_sigma_matches_direct(R: Results) -> None:
    """sigma(n) matches direct Terras simulation on 1000 random n."""
    t0 = time.perf_counter()
    rng = random.Random(20260718)
    N = 1 << 20
    mismatches = 0
    for _ in range(1000):
        n = rng.randrange(2, N)
        a = sigma(n)
        b = sigma_direct_simulation(n)
        if a != b:
            mismatches += 1
            raise AssertionError(f"sigma mismatch at n={n}: {a} vs {b}")
    # A few fixed hand checks
    # n=2: T(2)=1 < 2 → sigma=1
    assert sigma(2) == 1
    # n=3: T(3)=5, T(5)=8, T(8)=4, T(4)=2 < 3 → need check
    # 3 odd → (9+1)/2=5; 5→8; 8→4; 4→2 < 3 → sigma=4
    assert sigma(3) == 4
    # n=7: 7→11→17→26→13→20→10→5→8→4→2→1; first <7: ... 7→11→17→26→13→20→10→5 <7
    # 7→11,11→17,17→26,26→13,13→20,20→10,10→5; sigma=7
    assert sigma(7) == 7
    R.record(
        "sigma_matches_direct",
        "PASS",
        time.perf_counter() - t0,
        "1000 random n in [2, 2^20) + fixed checks n=2,3,7",
    )


def test_budget_hand_checked(R: Results) -> None:
    """Budget accounting correct on 3 hand-checked examples."""
    t0 = time.perf_counter()

    # Example 1: single mod 5 → space 5 → ceil(log2(5)) = 3
    b1 = budget_of_spaces([5])
    assert b1 == 3, f"expected 3, got {b1}"

    # Example 2: popcount space for N=2^20 is 21 → ceil(log2(21)) = 5
    sizes = value_space_sizes(1 << 20)
    assert sizes["popcount"] == 21, sizes["popcount"]
    b2 = budget_of_spaces([sizes["popcount"]])
    assert b2 == 5, f"expected 5, got {b2}"

    # Example 3: pair (mod_5, mod_7) → 5*7=35 → ceil(log2(35)) = 6
    b3 = budget_of_spaces([5, 7])
    assert b3 == 6, f"expected 6, got {b3}"

    # Extra sanity: product 4096 → ceil(log2(4096))=12; 4097 → 13
    assert budget_of_spaces([4096]) == 12
    assert budget_of_spaces([4097]) == 13
    assert budget_of_spaces([2, 2, 2]) == 3  # product 8

    R.record(
        "budget_hand_checked",
        "PASS",
        time.perf_counter() - t0,
        "mod5→3; popcount@2^20→5; mod5×mod7→6",
    )


def test_determinism(R: Results) -> None:
    """Two full runs produce the same leaderboard (names, budgets, accs)."""
    t0 = time.perf_counter()
    # Use N=2^14 for speed while exercising the full protocol
    N = 1 << 14
    r1 = run_experiment(N)
    r2 = run_experiment(N)

    def board_sig(res: dict) -> list:
        out = []
        for row in res["leaderboard"]:
            out.append(
                (
                    row["name"],
                    row["kind"],
                    row["budget"],
                    round(row["train_acc"], 10),
                    round(row["test_acc"], 10),
                    row.get("matched_B"),
                    bool(row["win"]) if row["kind"] == "feature" else None,
                )
            )
        return out

    s1, s2 = board_sig(r1), board_sig(r2)
    assert s1 == s2, f"leaderboard mismatch:\n{s1}\nvs\n{s2}"
    assert r1["verdict"] == r2["verdict"]
    assert r1["max_L_density_ge_log2_log3"] == r2["max_L_density_ge_log2_log3"]
    assert len(r1["excursion_top"]) == len(r2["excursion_top"])
    for a, b in zip(r1["excursion_top"], r2["excursion_top"]):
        assert a["n"] == b["n"] and a["L"] == b["L"] and a["a"] == b["a"]

    R.record(
        "determinism",
        "PASS",
        time.perf_counter() - t0,
        f"two runs N={N} identical leaderboard ({len(s1)} rows)",
    )


def test_pair_space_filter(R: Results) -> None:
    """Pairs with joint space > 2^12 are excluded; singles always present."""
    t0 = time.perf_counter()
    N = 1 << 20
    reg = build_feature_registry(N)
    fsets = enumerate_feature_sets(reg)
    names = {name for name, _, _, _ in fsets}
    # all singles present
    for name, _, _ in reg:
        assert name in names, f"missing single {name}"
    # mod_3^6 = 729; 729*7 = 5103 > 4096 → pair with mod_7 excluded
    assert "mod_3^6+mod_7" not in names
    # 729*5 = 3645 <= 4096 → included
    assert "mod_3^6+mod_5" in names
    for name, _, prod, bud in fsets:
        if "+" in name:
            assert prod <= 4096, (name, prod)
        # budget = ceil(log2(product of spaces)) = ceil(log2(prod))
        assert bud == budget_of_spaces([prod]), (name, prod, bud)

    R.record(
        "pair_space_filter",
        "PASS",
        time.perf_counter() - t0,
        f"{len(fsets)} feature sets; 3^6×7 excluded, 3^6×5 included",
    )


def main() -> int:
    R = Results()
    tests = [
        ("sigma_matches_direct", test_sigma_matches_direct),
        ("budget_hand_checked", test_budget_hand_checked),
        ("determinism", test_determinism),
        ("pair_space_filter", test_pair_space_filter),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn(R)
        except Exception as e:
            failed += 1
            R.record(name, "FAIL", 0.0, f"{e}")
            traceback.print_exc()
    print()
    n_pass = sum(1 for s in R.sections if s["status"] == "PASS")
    print(f"Summary: {n_pass}/{len(tests)} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
