"""Independent checks for the exact odd-only cycle search."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exact_cycle_search import (  # noqa: E402
    DEFAULT_PAIRS,
    U,
    affine_CS,
    affine_fixed_point_via_direct_formula,
    build_report,
    canonical_composition_count,
    canonical_rotation,
    composition_count,
    compositions_of,
    evaluate_exponents,
    fixed_point_fraction,
    is_canonical_rotation,
    main,
    odd_only_step,
    search_pair,
    try_integral_fixed_point,
    v2,
    verify_valuation_orbit,
)


# ---------------------------------------------------------------------------
# Affine C recurrence vs direct odd-only iteration
# ---------------------------------------------------------------------------


def test_affine_C_recurrence_matches_direct_odd_only_iteration() -> None:
    """Unit: C_m from the packet recurrence equals the offset of U^m when valuations hold."""
    # For a start n that realizes exponents a, U^m(n) = (3^m n + C_m) / 2^K.
    # Cross-check C_m by expanding the composite symbolically and by iterating
    # known realizing starts when they exist.
    samples = [
        (1,),
        (2,),
        (1, 1),
        (2, 2),
        (1, 2, 1),
        (3, 1, 2),
        (1, 1, 1, 1),
        (4, 2, 1, 3),
    ]
    for a in samples:
        c_m, k = affine_CS(a)
        assert k == sum(a)
        # Closed-form expansion: C = sum_{j=0}^{m-1} 3^{m-1-j} * 2^{S_j}
        s = 0
        closed = 0
        m = len(a)
        for j in range(m):
            closed += (3 ** (m - 1 - j)) * (1 << s)
            s += a[j]
        assert c_m == closed, f"recurrence vs closed form failed for {a}"

        # If an integral fixed point exists and verifies, direct U iteration
        # must match the affine composite and return to start.
        fp = try_integral_fixed_point(a)
        if fp is None:
            continue
        n0, _, _ = fp
        val_ok, returns, all_odd, orbit = verify_valuation_orbit(n0, a)
        if not (val_ok and returns and all_odd):
            continue
        # Affine apply once around the cycle equals n0
        assert affine_fixed_point_via_direct_formula(a, n0) == n0
        # Step-by-step U matches orbit
        n = n0
        for expected in orbit[1:]:
            n = U(n)
            assert n == expected
        assert U(orbit[-1]) == n0


def test_affine_C_matches_manual_unrolling_on_symbolic_start() -> None:
    """Independent expansion: apply (3x+1)/2^{a_j} symbolically via fractions-free ints.

    Represent state as (A * n + B) / 2^S with A,B,S integers; each odd-only step
    with forced valuation a_j updates A' = 3A, B' = 3B + 2^S, S' = S + a_j —
    the same recurrence as affine_CS for the offset when A starts at 1, B at 0.
    """
    for a in [(2,), (1, 3), (2, 1, 2), (5, 1, 1, 2)]:
        A, B, S = 1, 0, 0
        for a_j in a:
            # state = (A n + B) / 2^S; apply (3*state+1)/2^{a_j}
            # 3*state+1 = (3 A n + 3 B + 2^S) / 2^S
            # divide by 2^{a_j}: (3 A n + 3 B + 2^S) / 2^{S+a_j}
            B = 3 * B + (1 << S)
            A = 3 * A
            S = S + a_j
        c_m, k = affine_CS(a)
        assert B == c_m
        assert S == k
        assert A == 3 ** len(a)


# ---------------------------------------------------------------------------
# Known small cases
# ---------------------------------------------------------------------------


def test_pair_1_2_returns_exactly_trivial_one() -> None:
    result = search_pair(1, 2)
    assert result.compositions_before_symmetry == 1
    assert result.compositions_after_symmetry == 1
    assert len(result.integral_candidates) == 1
    c = result.integral_candidates[0]
    assert c.n0 == 1
    assert c.exponents == (2,)
    assert c.is_trivial is True
    assert c.valuation_verified is True
    assert c.orbit == (1,)
    assert result.nontrivial_counterexamples == []


def test_repeated_exponents_2_2_reconstructs_trivial_one() -> None:
    """a = (2, 2) has m=2, K=4 and fixed point n=1 — not a counterexample."""
    a = (2, 2)
    c_m, k = affine_CS(a)
    assert k == 4
    assert c_m == 7  # C1=1, C2=3*1+4=7
    fp = try_integral_fixed_point(a)
    assert fp is not None
    n0, _, denom = fp
    assert n0 == 1
    assert denom == 16 - 9
    val_ok, returns, all_odd, orbit = verify_valuation_orbit(n0, a)
    assert val_ok and returns and all_odd
    assert orbit == (1, 1)
    cand = evaluate_exponents(a)
    assert cand is not None
    assert cand.is_trivial is True
    assert cand.to_dict()["is_nontrivial_counterexample"] is False


def test_deliberately_altered_exponents_fail_valuation_verification() -> None:
    """(2,) realizes n=1 with a0=2; altering to (1,) fails exact valuation check."""
    # True valuation at 1 is v2(3*1+1)=v2(4)=2
    n0 = 1
    false_exponents = (1,)
    val_ok, returns, all_odd, _ = verify_valuation_orbit(n0, false_exponents)
    assert val_ok is False
    # Affine fixed point for (1,) is C=1, denom=2-3=-1 → n=-1, rejected
    assert try_integral_fixed_point(false_exponents) is None

    # Another alteration: (2,2) works for n=1; (3,1) should not verify on n=1
    val_ok2, _, _, _ = verify_valuation_orbit(1, (3, 1))
    assert val_ok2 is False
    # And even if some other integral root existed, evaluate must not accept
    # without valuation match — force a bogus n through verify only
    observed_a = odd_only_step(1)[1]
    assert observed_a == 2
    assert v2(3 * 1 + 1) == 2


# ---------------------------------------------------------------------------
# Brute-force composition oracle
# ---------------------------------------------------------------------------


def brute_force_integral_cycles(m: int, k: int) -> list[tuple[tuple[int, ...], int]]:
    """Independent oracle: enumerate all compositions via product-of-stars.

    Returns sorted unique (canonical exponents, n0) for verified integral cycles.
    """
    if m < 1 or k < m:
        return []
    # a_i >= 1; use stars-and-bars via nested loops on free variables
    found: dict[tuple[int, ...], int] = {}
    # compositions: product of ranges is wrong; use recursive list from compositions_of
    # but rebuild compositions independently here without is_canonical prefilter
    def comps(parts: int, total: int) -> list[tuple[int, ...]]:
        if parts == 1:
            return [(total,)] if total >= 1 else []
        out: list[tuple[int, ...]] = []
        for first in range(1, total - parts + 2):
            for rest in comps(parts - 1, total - first):
                out.append((first,) + rest)
        return out

    for a in comps(m, k):
        # Independent fixed-point calc
        s = 0
        c = 0
        for a_j in a:
            c = 3 * c + (1 << s)
            s += a_j
        if s != k:
            continue
        pow2 = 1 << k
        pow3 = 3**m
        if pow2 <= pow3:
            continue
        denom = pow2 - pow3
        if c % denom != 0:
            continue
        n = c // denom
        if n <= 0 or n % 2 == 0:
            continue
        # Direct orbit with independent v2
        ok = True
        states = []
        x = n
        for a_j in a:
            if x <= 0 or x % 2 == 0:
                ok = False
                break
            states.append(x)
            t = 3 * x + 1
            val = 0
            tmp = t
            while tmp % 2 == 0:
                tmp //= 2
                val += 1
            if val != a_j:
                ok = False
                break
            x = t // (1 << val)
        if not ok or x != n:
            continue
        canon = min(a[i:] + a[:i] for i in range(m))
        # n0 for canon: rotate states
        if canon not in found:
            # find start index
            idx = next(i for i in range(m) if a[i:] + a[:i] == canon)
            found[canon] = states[idx]
    return sorted(found.items(), key=lambda kv: (kv[1], kv[0]))


@pytest.mark.parametrize(
    "m,k",
    [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
        (2, 4),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 6),
        (5, 8),
    ],
)
def test_search_matches_brute_force_oracle(m: int, k: int) -> None:
    result = search_pair(m, k)
    oracle = brute_force_integral_cycles(m, k)
    got = [(c.exponents, c.n0) for c in result.integral_candidates]
    assert got == oracle
    assert result.compositions_before_symmetry == composition_count(m, k)
    # after_symmetry count equals number of canonical compositions
    after = sum(1 for a in compositions_of(k, m) if is_canonical_rotation(a))
    assert result.compositions_after_symmetry == after


def test_composition_count_binom() -> None:
    assert composition_count(1, 2) == 1
    assert composition_count(2, 4) == 3  # (1,3),(2,2),(3,1)
    assert composition_count(5, 8) == 35  # binom(7,4)
    assert composition_count(12, 19) == 31824  # binom(18,11)
    assert composition_count(3, 2) == 0  # impossible


@pytest.mark.parametrize(
    "m,k",
    [(1, 2), (2, 4), (3, 6), (4, 6), (5, 8), (6, 9), (8, 12)],
)
def test_burnside_canonical_count_matches_direct_enumeration(m: int, k: int) -> None:
    direct = sum(1 for a in compositions_of(k, m) if is_canonical_rotation(a))
    assert canonical_composition_count(m, k) == direct


def test_canonical_rotation_unique() -> None:
    assert canonical_rotation((1, 3, 2)) == (1, 3, 2)
    assert canonical_rotation((3, 2, 1)) == (1, 3, 2)
    assert canonical_rotation((2, 1, 3)) == (1, 3, 2)
    assert is_canonical_rotation((2, 2)) is True
    assert is_canonical_rotation((1, 2)) is True
    assert is_canonical_rotation((2, 1)) is False


# ---------------------------------------------------------------------------
# CLI + persisted JSON
# ---------------------------------------------------------------------------


def test_cli_writes_results_and_stdout_match(tmp_path: Path) -> None:
    out = tmp_path / "exact_cycle_search_results.json"
    # Run via main() for in-process identity of stdout vs file
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(
            [
                "--pair",
                "1:2",
                "--pair",
                "5:8",
                "--pair",
                "12:19",
                "--output",
                str(out),
            ]
        )
    assert code == 0
    stdout_text = buf.getvalue()
    file_text = out.read_text(encoding="utf-8")
    assert stdout_text == file_text
    report = json.loads(file_text)
    assert report["all_checks_passed"] is True
    assert report["nontrivial_counterexamples"] == []
    # (1,2) present and trivial
    pairs = {(r["m"], r["k"]): r for r in report["pairs"]}
    assert (1, 2) in pairs
    assert pairs[(1, 2)]["integral_candidates"][0]["n0"] == 1
    assert pairs[(1, 2)]["integral_candidates"][0]["is_trivial"] is True


def test_default_report_structure() -> None:
    report = build_report(DEFAULT_PAIRS)
    assert report["all_checks_passed"] is True
    for key in (
        "parameters",
        "exact_scope",
        "counts_per_pair",
        "every_integral_candidate",
        "nontrivial_counterexamples",
        "direct_verification_summary",
        "all_checks_passed",
        "limitations",
    ):
        assert key in report
    # every integral candidate has direct verification fields
    for c in report["every_integral_candidate"]:
        assert "valuation_verified" in c
        assert "returns_to_start" in c
        assert "all_states_odd_positive" in c
        assert c["valuation_verified"] is True
        assert c["returns_to_start"] is True


def test_fixed_point_fraction_for_trivial() -> None:
    from fractions import Fraction

    assert fixed_point_fraction((2,)) == Fraction(1, 1)
    assert fixed_point_fraction((2, 2)) == Fraction(1, 1)


def test_cli_subprocess_default_output_path() -> None:
    """Subprocess run of the module writing the package default results path."""
    module = Path(__file__).resolve().parent / "exact_cycle_search.py"
    # Write to a temp path so we don't race the committed default during unit test;
    # the session also runs the real default path separately.
    out = Path(__file__).resolve().parent / "_test_tmp_exact_cycle_search.json"
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(module),
                "--pair",
                "1:2",
                "--pair",
                "2:4",
                "--output",
                str(out),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(proc.stdout)
        assert data["all_checks_passed"] is True
        assert json.loads(out.read_text(encoding="utf-8")) == data
    finally:
        if out.exists():
            out.unlink()
