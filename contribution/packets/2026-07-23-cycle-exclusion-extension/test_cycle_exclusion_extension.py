#!/usr/bin/env python3
"""Tests for the cycle-exclusion-extension packet.

Fast structural tests (enumerator independence, exact windows, chunk
partition integrity, closed-form vs recurrence) plus consistency gates on the
persisted results of the full exact scan.  The heavy scans themselves were
run once by run_cycle_exclusion_extension.py and are asserted here from
cycle_exclusion_extension_results.json (like the plateau-drift packet's
certificate test).
"""

import json
import os
import sys
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "code", "fence"
    ),
)

import exact_cycle_search as ecs  # noqa: E402
import pytest  # noqa: E402
import run_cycle_exclusion_extension as rx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "cycle_exclusion_extension_results.json")

ALL_PAIRS = list(rx.REGRESSION_PAIRS) + list(rx.EXTENSION_PAIRS)


# ---------------------------------------------------------------------------
# Exact window
# ---------------------------------------------------------------------------


def test_exact_window_reproduces_fence_table():
    """The integer-inequality window 3^m < 2^K <= (22/7)^m reproduces exactly
    the eleven surviving m<=18 pairs of the fence proof doc.  The nontrivial
    window is empty at m=1; the pair (1,2) scanned here is the trivial-cycle
    control (denom = 2^2 - 3 = 1), not a window member."""
    doc_pairs = [
        (5, 8), (8, 13), (10, 16), (11, 18), (13, 21), (14, 23),
        (15, 24), (16, 26), (17, 27), (17, 28), (18, 29),
    ]
    mine = [(m, k) for m in range(1, 19) for k in rx.exact_window(m)]
    assert mine == doc_pairs
    assert rx.exact_window(1) == []
    assert (1 << 2) - 3 == 1  # control pair denominator


def test_exact_window_extension_boundaries():
    """m=19,20 windows with exact integer boundary checks (no floats)."""
    assert rx.exact_window(19) == [31]
    assert rx.exact_window(20) == [32, 33]
    # lower boundary: 2^30 <= 3^19 < 2^31 and 2^31 <= 3^20 < 2^32
    assert (1 << 30) <= 3**19 < (1 << 31)
    assert (1 << 31) <= 3**20 < (1 << 32)
    # upper boundary: 2^33 * 7^20 <= 22^20 < 2^34 * 7^20
    assert (1 << 33) * 7**20 <= 22**20
    assert 22**20 < (1 << 34) * 7**20
    # no m in 1..20 is skipped: every window member is one of the scanned pairs
    scanned = set(ALL_PAIRS)
    for m in range(1, 21):
        for k in rx.exact_window(m):
            assert (m, k) in scanned


# ---------------------------------------------------------------------------
# Enumerator independence and chunk integrity
# ---------------------------------------------------------------------------


def test_independent_enumerator_matches_repo_oracle():
    """The packet's iterative enumerator and the fence module's recursive
    enumerator generate identical sets (different order) through (13,21)."""
    for (k, m) in [(8, 5), (13, 8), (16, 10), (18, 11), (21, 13)]:
        a = list(ecs.compositions_of(k, m))
        b = list(rx.iter_compositions_independent(k, m))
        assert len(a) == len(b) == comb(k - 1, m - 1)
        assert set(a) == set(b)
        assert a != b  # genuinely different enumeration order


def test_chunk_partition_covers_every_pair_exactly():
    """Prefix-chunking never drops or duplicates a word: sizes sum to
    binom(K-1, m-1) for all fifteen scanned pairs."""
    for (m, k) in ALL_PAIRS:
        chunks = rx.build_chunks(m, k, rx.DEFAULT_MAX_CHUNK)
        assert sum(s for (_p, _rs, _rp, s) in chunks) == comb(k - 1, m - 1)
        assert all(s > 0 for s in (*[c[3] for c in chunks],))


def test_closed_form_matches_recurrence():
    """Closed form C_m = sum_j 3^{m-1-j} 2^{S_j} equals the fence recurrence.
    Full sweep on small pairs; bounded strided sample on large ones (the
    large pairs are additionally covered by the strided audits recorded in
    the persisted scan results, asserted below)."""
    small = [(m, k) for (m, k) in ALL_PAIRS if comb(k - 1, m - 1) <= 1_000_000]
    for (m, k) in small:
        for w in ecs.compositions_of(k, m):
            assert rx.affine_cs_closed_form(w) == ecs.affine_CS(w)
    import itertools

    for (m, k) in [(16, 26), (18, 29), (19, 31), (20, 32), (20, 33)]:
        for w in itertools.islice(ecs.compositions_of(k, m), 0, 3000, 7):
            assert rx.affine_cs_closed_form(w) == ecs.affine_CS(w)


# ---------------------------------------------------------------------------
# Acceptance-gate behavior on known cases
# ---------------------------------------------------------------------------


def test_control_pair_yields_exactly_trivial_one():
    cand = ecs.evaluate_exponents((2,))
    assert cand is not None
    assert cand.n0 == 1 and cand.is_trivial and cand.exponents == (2,)
    assert not cand.to_dict()["is_nontrivial_counterexample"]


def test_nontrivial_cycle_states_exclude_1_3_5():
    """The window's premise: 1, 3, 5 cannot lie on a nontrivial cycle
    (3 -> 5 -> 1 and 5 -> 1 under U), so min state >= 7 gives the
    2^K <= (22/7)^m bound used by the window."""
    assert ecs.U(1) == 1
    assert ecs.U(3) == 5 and ecs.U(5) == 1


# ---------------------------------------------------------------------------
# Persisted full-scan results
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def results():
    with open(RESULTS, encoding="utf-8") as fh:
        return json.load(fh)


def test_results_counts_and_phases(results):
    """Every scanned pair: both phases complete, counts equal binom(K-1,m-1),
    phase cross-validation passed, zero audit mismatches."""
    for (m, k) in ALL_PAIRS:
        rec = results["pairs"][f"{m}:{k}"]
        for phase in ("primary", "independent"):
            ph = rec["phases"][phase]
            assert ph["partial"] is False
            assert ph["words_enumerated"] == comb(k - 1, m - 1)
            assert ph["count_matches_formula"] is True
        cv = rec["cross_validation"]
        assert cv["counts_equal_both_phases"] is True
        assert cv["hit_word_sets_equal"] is True
        assert cv["closed_form_audit_mismatches"] == []
    # strided closed-form audits actually ran on the large pairs
    big = results["pairs"]["20:33"]["phases"]["independent"]
    assert big["closed_form_audits"] >= 10


def test_results_no_counterexample_and_candidates_verified(results):
    assert results["counterexample_watch"]["fired"] is False
    assert results["counterexample_watch"]["verified_nontrivial_cycles"] == []
    for key, rec in results["pairs"].items():
        assert rec["nontrivial_counterexamples"] == [], key
        for c in rec["verified_candidates"]:
            assert c["valuation_verified"] and c["returns_to_start"]
            assert c["all_states_odd_positive"]
            assert c["is_nontrivial_counterexample"] is False


def test_results_regression_matches_fence(results):
    reg = results["regression_vs_fence_m18"]
    assert reg["all_match"] is True
    assert len(reg["pairs_checked"]) == len(rx.REGRESSION_PAIRS)
    # the only verified candidate through m<=18 is the trivial n=1 at (1,2)
    nontrivial_rows = [
        row for row in reg["pairs_checked"] if row["fresh_verified_candidates"]
    ]
    assert len(nontrivial_rows) == 1
    only = nontrivial_rows[0]
    assert only["pair"] == [1, 2]
    assert only["fresh_verified_candidates"] == [{"exponents": [2], "n0": 1}]


def test_results_verdict_and_coverage(results):
    assert results["window_coverage_complete_through_m20"] is True
    assert "incomplete_pairs" not in results
    assert "at most 20 odd members" in results["verdict"]
    assert results["verdict"].startswith("no nontrivial positive Collatz cycle")
    windows = {row["m"]: row["k_window"] for row in results["exact_windows_m1_to_m20"]}
    assert windows[19] == [31]
    assert windows[20] == [32, 33]
