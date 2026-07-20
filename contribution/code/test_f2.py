"""
F2 tests — induced first-return correctness + exactness + mass partition.

Run:
    python3 fold/test_f2.py
    pytest fold/test_f2.py -q
"""

from __future__ import annotations

import os
import random
import sys
from fractions import Fraction

# Allow `python3 fold/test_f2.py` from repo root
_FOLDER = os.path.dirname(os.path.abspath(__file__))
if _FOLDER not in sys.path:
    sys.path.insert(0, _FOLDER)

from f2_fold_operator import (
    K_MAX,
    MASS_THRESHOLD,
    NODE_BUDGET,
    S_EXTRA,
    ClassResult,
    collapse_search,
    compute_all_classes,
    induced_first_return,
    mass_as_string,
    normalize_branch,
    predict_induced,
    r_prime,
    simulate_first_return,
)

# Shared cache so k=1..5 is not recomputed thrice (node budget is heavy).
_CLASS_CACHE: dict = {}


def get_class(k: int, r: int, **kwargs) -> ClassResult:
    if kwargs:
        return induced_first_return(k, r, **kwargs)
    key = (k, r)
    if key not in _CLASS_CACHE:
        _CLASS_CACHE[key] = induced_first_return(k, r)
    return _CLASS_CACHE[key]


def test_r_prime():
    assert r_prime(3, 0) == 8
    assert r_prime(3, 5) == 5
    assert r_prime(1, 1) == 1
    assert r_prime(1, 0) == 2


def test_normalize_branch_exact_ints():
    b = normalize_branch(3, 11, 5, -2)  # u=11 mod 8 → 3
    assert b == (3, 3, 5, -2)
    assert all(type(x) is int for x in b)


def test_small_class_k1_odd():
    """k=1, r=1: odds. Sanity: branches exist, no floats."""
    cr = get_class(1, 1)
    assert len(cr.branches) >= 1
    # tiny truncation mass at s-cap is budgeted; must be << 2^{-10}
    assert cr.unresolved_mass < Fraction(1, 1 << 10)
    assert cr.total_mass() == 1
    for s, u, alpha, beta, a, t in cr.branches:
        assert type(s) is int and type(u) is int
        assert type(alpha) is int and type(beta) is int
        assert type(a) is int and type(t) is int
        assert t >= 1
        assert 0 <= u < (1 << s)
        assert a <= t


def test_small_class_k1_even():
    cr = get_class(1, 0)
    assert len(cr.branches) >= 1
    for m in range(0, 40):
        n = r_prime(1, 0) + 2 * m
        m_img_sim, t_sim = simulate_first_return(n, 1, 0)
        m_img_pred, t_pred = predict_induced(cr, m)
        assert m_img_sim == m_img_pred, (m, m_img_sim, m_img_pred)
        assert t_sim == t_pred, (m, t_sim, t_pred)


def test_exactness_no_floats_in_branch_data():
    """(c) No floats in any branch data for k=1..5."""
    for k in range(1, K_MAX + 1):
        for r in range(1 << k):
            cr = get_class(k, r)
            for br in cr.branches:
                for x in br:
                    assert type(x) is int, f"non-int in branch {br} for ({k},{r})"
            can = cr.canonical()
            for item in can:
                for x in item:
                    assert type(x) is int
            for leaf in cr.unresolved:
                assert type(leaf.s) is int and type(leaf.u) is int
                assert type(leaf.t) is int
            assert isinstance(cr.unresolved_mass, Fraction)


def test_induced_matches_simulation_1000_samples():
    """
    (a) For ≥ 1000 random (class, m) samples with m inside a resolved branch:
    branch-predicted induced image == direct simulation of T to first return.
    """
    rng = random.Random(20260718)
    samples = 0
    class_pool = [(k, r) for k in range(1, K_MAX + 1) for r in range(1 << k)]
    # warm cache
    for kr in class_pool:
        get_class(kr[0], kr[1])

    attempts = 0
    max_attempts = 8000
    while samples < 1000 and attempts < max_attempts:
        attempts += 1
        k, r = rng.choice(class_pool)
        cr = get_class(k, r)
        m = rng.randrange(0, 1 << 16)
        try:
            m_pred, t_pred = predict_induced(cr, m)
        except RuntimeError:
            continue
        n = r_prime(k, r) + (1 << k) * m
        m_sim, t_sim = simulate_first_return(n, k, r)
        assert m_pred == m_sim, (
            f"mismatch image k={k} r={r} m={m}: pred={m_pred} sim={m_sim}"
        )
        assert t_pred == t_sim, (
            f"mismatch steps k={k} r={r} m={m}: pred={t_pred} sim={t_sim}"
        )
        samples += 1

    assert samples >= 1000, f"only got {samples} successful samples"
    print(f"  induced-vs-sim: {samples} samples OK (attempts={attempts})")


def test_exhaustive_small_k_all_m():
    """Exhaustive check for k≤3, m in 0..64 (skip unresolved cones)."""
    for k in range(1, 4):
        for r in range(1 << k):
            cr = get_class(k, r)
            # Budgeted truncation: k=1 near-zero; k=2,3 may carry s-cap / node mass
            assert cr.unresolved_mass < Fraction(1, 4), (
                f"large unresolved at k={k} r={r}: "
                f"{mass_as_string(cr.unresolved_mass)}"
            )
            for m in range(65):
                try:
                    m_pred, t_pred = predict_induced(cr, m)
                except RuntimeError:
                    continue  # m in unresolved leaf
                n = r_prime(k, r) + (1 << k) * m
                m_sim, t_sim = simulate_first_return(n, k, r)
                assert (m_pred, t_pred) == (m_sim, t_sim), (
                    k, r, m, m_pred, m_sim, t_pred, t_sim
                )


def test_mass_partition_equals_one():
    """
    (b) Per-class: Σ 2^(−s) over resolved branches + unresolved mass == 1
    exactly (Fraction arithmetic).
    """
    for k in range(1, K_MAX + 1):
        for r in range(1 << k):
            cr = get_class(k, r)
            total = cr.total_mass()
            assert total == 1, (
                f"mass partition fail ({k},{r}): resolved="
                f"{cr.resolved_mass()} unres={cr.unresolved_mass} "
                f"total={total}"
            )
            # also check no float types
            assert isinstance(cr.unresolved_mass, Fraction)
            assert isinstance(cr.resolved_mass(), Fraction)


def test_canonical_sorted_and_stable():
    cr = get_class(4, 7)
    can = cr.canonical()
    assert can == tuple(sorted(can))
    cr2 = get_class(4, 7)
    assert cr2.canonical() == can


def test_signature_multiset():
    cr = get_class(3, 5)
    sig = cr.signature()
    assert sig == tuple(sorted(sig))
    assert len(sig) == len(cr.branches)
    for s, a, t in sig:
        assert type(s) is int and type(a) is int and type(t) is int
        assert a <= t


def test_domains_partition_unit_interval():
    """
    Resolved branches' domains must be pairwise disjoint (cylinder sets).
    Check pairwise: two domains m≡u1 mod 2^{s1}, m≡u2 mod 2^{s2} overlap
    iff u1 ≡ u2 (mod 2^{min(s1,s2)}).
    """
    for k in range(1, 4):
        for r in range(1 << k):
            cr = get_class(k, r)
            domains = [(s, u) for s, u, *_ in cr.branches]
            for i in range(len(domains)):
                s1, u1 = domains[i]
                for j in range(i + 1, len(domains)):
                    s2, u2 = domains[j]
                    m = min(s1, s2)
                    assert (u1 % (1 << m)) != (u2 % (1 << m)), (
                        f"overlap k={k} r={r}: ({s1},{u1}) vs ({s2},{u2})"
                    )
            # unresolved leaves must not nest inside a resolved domain either
            for leaf in cr.unresolved:
                for s, u in domains:
                    m = min(s, leaf.s)
                    assert (u % (1 << m)) != (leaf.u % (1 << m)), (
                        f"unres/resol overlap k={k} r={r}"
                    )


def test_collapse_search_runs():
    results = {}
    for k in range(1, 4):
        for r in range(1 << k):
            results[(k, r)] = get_class(k, r)
    sc = collapse_search(results, 3)
    assert "collapses" in sc and "shortlist" in sc
    assert len(results) == 2 + 4 + 8
    # k=1 always under threshold; k=2 partial; k=3 may exceed due to caps
    n_eligible = sum(
        1 for cr in results.values() if cr.unresolved_mass < MASS_THRESHOLD
    )
    assert n_eligible >= 2, f"expected ≥2 eligible classes, got {n_eligible}"


def test_unresolved_mass_reported_not_dropped():
    # With tiny s cap, should get unresolved and nonzero mass
    cr = induced_first_return(5, 1, max_s=2)
    assert isinstance(cr.unresolved_mass, Fraction)
    if cr.unresolved:
        assert cr.unresolved_mass > 0
        s = mass_as_string(cr.unresolved_mass)
        assert s != "0"
    # zero-mass string
    assert mass_as_string(Fraction(0)) == "0"
    # partition still holds under aggressive cap
    assert cr.total_mass() == 1
    cr2 = get_class(1, 1)
    assert cr2.total_mass() == 1


def test_budgets_enforced():
    """k>5 rejected; s_cap = k+22 by default; node budget respected."""
    try:
        induced_first_return(6, 0)
        assert False, "expected ValueError for k=6"
    except ValueError:
        pass
    cr = get_class(2, 1)
    assert cr.max_s_cap == 2 + S_EXTRA
    assert cr.nodes_visited <= NODE_BUDGET
    # forced tiny node budget produces truncation accounting
    cr2 = induced_first_return(5, 3, node_budget=50)
    assert cr2.total_mass() == 1
    if cr2.truncated:
        assert cr2.unresolved_mass > 0


def _write_report_from_cache() -> None:
    """Build F2_REPORT.md from the warmed class cache (no recompute)."""
    import time
    from f2_fold_operator import (
        collapse_search,
        mass_as_string,
        per_k_stats,
        write_report,
    )

    # Ensure full k=1..5 is warm
    t0 = time.perf_counter()
    per_k_times = {}
    results = {}
    for k in range(1, K_MAX + 1):
        tk = time.perf_counter()
        for r in range(1 << k):
            results[(k, r)] = get_class(k, r)
        per_k_times[k] = time.perf_counter() - tk
    total_time = time.perf_counter() - t0
    stats = {k: per_k_stats(results, k) for k in range(1, K_MAX + 1)}
    search = collapse_search(results, K_MAX)
    max_unres = max(
        (cr.unresolved_mass for cr in results.values()), default=Fraction(0)
    )
    min_resolved = min(
        (cr.resolved_mass() for cr in results.values()), default=Fraction(1)
    )
    out = {
        "k_max": K_MAX,
        "results": results,
        "stats": stats,
        "search": search,
        "per_k_times": per_k_times,
        "total_time": total_time,
        "max_unresolved_mass": max_unres,
        "min_resolved_mass": min_resolved,
        "note": f"Completed full search for k=1..{K_MAX} (from test cache).",
    }
    report_path = os.path.join(_FOLDER, "F2_REPORT.md")
    write_report(out, report_path)
    print(f"Wrote {report_path}")
    print(f"per_k_times: { {k: round(v, 3) for k, v in per_k_times.items()} }")
    print(f"total_time (cache warm+stats): {total_time:.3f}s")
    if search["collapses"]:
        pairs = ", ".join(
            f"{c['class1']}↔{c['class2']}" for c in search["collapses"]
        )
        print(f"COLLAPSE FOUND: {pairs}")
    else:
        print(
            f"NO COLLAPSE at k ≤ {K_MAX}, min resolved mass = "
            f"{mass_as_string(min_resolved)}"
        )


def _warm_all_classes() -> None:
    """Precompute all k=1..5 classes with progress (shared cache)."""
    import time

    print("Warming class cache k=1..5 ...", flush=True)
    t0 = time.perf_counter()
    for k in range(1, K_MAX + 1):
        tk = time.perf_counter()
        for r in range(1 << k):
            get_class(k, r)
        print(
            f"  k={k}: {1 << k} classes in {time.perf_counter() - tk:.2f}s",
            flush=True,
        )
    print(f"  total warm: {time.perf_counter() - t0:.2f}s", flush=True)


def run_all():
    tests = [
        test_r_prime,
        test_normalize_branch_exact_ints,
        test_small_class_k1_odd,
        test_small_class_k1_even,
        test_budgets_enforced,
        test_unresolved_mass_reported_not_dropped,
        # warm once before the heavy exactness / mass / sample suite
        test_exactness_no_floats_in_branch_data,
        test_exhaustive_small_k_all_m,
        test_mass_partition_equals_one,
        test_induced_matches_simulation_1000_samples,
        test_canonical_sorted_and_stable,
        test_signature_multiset,
        test_domains_partition_unit_interval,
        test_collapse_search_runs,
    ]
    failed = []
    # lightweight tests first
    light = tests[:6]
    heavy = tests[6:]
    for fn in light:
        name = fn.__name__
        try:
            fn()
            print(f"OK  {name}", flush=True)
        except Exception as e:
            import traceback
            print(f"FAIL {name}: {e}", flush=True)
            traceback.print_exc()
            failed.append((name, e))
    if not failed:
        _warm_all_classes()
    for fn in heavy:
        name = fn.__name__
        try:
            fn()
            print(f"OK  {name}", flush=True)
        except Exception as e:
            import traceback
            print(f"FAIL {name}: {e}", flush=True)
            traceback.print_exc()
            failed.append((name, e))
    print()
    if failed:
        print(f"{len(failed)} FAILED out of {len(tests)}", flush=True)
        for name, e in failed:
            print(f"  - {name}: {e}", flush=True)
        sys.exit(1)
    print(f"All {len(tests)} tests passed.", flush=True)
    _write_report_from_cache()
    sys.exit(0)


if __name__ == "__main__":
    run_all()
