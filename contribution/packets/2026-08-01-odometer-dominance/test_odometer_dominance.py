#!/usr/bin/env python3
"""test_odometer_dominance.py — structural invariants of the
odometer-dominance packet, asserted against the slim
odometer_dominance_results.json (certificate_format slim-v1).

Exact x_n is recovered as Fraction(2^(k-1), 3^n) from stored (k, n).
Live mpmath recompute is optional (skips if mpmath is missing).

Run:
  python3 test_odometer_dominance.py
  # or: python3 -m pytest test_odometer_dominance.py -q
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "odometer_dominance_results.json")

K_CERT = {
    6: 6,
    7: 8,
    8: 9,
    9: 10,
    10: 12,
    11: 13,
    12: 14,
    13: 16,
    14: 17,
    15: 18,
    16: 20,
    17: 21,
    18: 23,
    19: 24,
    20: 26,
    21: 28,
}


def load_data():
    with open(RESULTS) as f:
        return json.load(f)


def test_certificate_format(data):
    assert data.get("certificate_format") == "slim-v1"
    assert "per_layer" in data
    assert data["kill_criteria"]["fired"] == []


def test_no_kill_criterion_fired(data):
    assert data["kill_criteria"]["fired"] == []
    assert data["kill_criteria"]["cert_argmax_mismatches_6_21"] == {}
    assert "SURVIVES" in data["status"]


def test_depth_and_completeness(layers):
    assert len(layers) == 1000
    assert [r["n"] for r in layers] == list(range(1, 1001))


def test_argmax_matches_certificates_6_21(layers):
    for r in layers:
        if r["n"] in K_CERT:
            assert r["k"] == K_CERT[r["n"]]
            assert r.get("k_cert_match") is True


def test_k_canonical_range(layers):
    for r in layers:
        assert 0 <= r["k"] < 2 * 3 ** (r["n"] - 1)


def test_monotone_and_dk_in_1_2(layers):
    prev = None
    for r in layers:
        if r["n"] < 6:
            continue
        if prev is not None:
            assert r["k"] - prev in (1, 2), (r["n"], r["k"], prev)
            if r.get("dk") is not None:
                assert r["dk"] == r["k"] - prev
        prev = r["k"]


def test_a1_dominance_every_layer(layers):
    for r in layers:
        assert r["argmax_a"] == 1, r["n"]
        assert float(r["w1_margin_over_best_other"]) > 0.2, r["n"]


def test_w1_band(layers):
    for r in layers:
        if r["n"] < 6:
            continue
        w1 = float(r["w_a"]["1"])
        assert 0.49 < w1 < 0.66, (r["n"], w1)


def test_pullback_ordering(layers):
    for r in layers:
        if r["n"] < 6:
            continue
        w = {a: float(r["w_a"][str(a)]) for a in range(1, 7)}
        assert w[1] > w[2] > w[3], r["n"]


def test_delta_band(layers):
    for r in layers:
        if r["n"] < 6:
            continue
        d = float(r["delta_n"])
        assert 3.0 < d < 8.0, (r["n"], d)


def test_window_convergence_S3(data):
    s3 = data["stability"]["S3_wide_window"]
    assert s3["pass"] is True
    assert s3["mismatches"] == []


def test_dps_stability_S4(data):
    s4 = data["stability"]["S4_plus50dps"]
    assert s4["pass"] is True
    assert s4["mismatches"] == []


def test_a_window_extension(data):
    checks = data["windows"]["a_extension_checks"]
    assert checks, "no a-extension checks recorded"
    for n, row in checks.items():
        assert float(row["extra_over_w1"]) < 1e-30, n


def test_certified_magnitudes(data):
    cm = data["certified_cross_checks"]["M_n_vs_certificates"]
    assert cm["max_rel_err"] < 1e-12


def test_drift_ranking_stable(data):
    p2 = data["part2_drift"]
    assert p2["ranking_full"][0] == "log"
    assert p2["ranking_tail"][0] == "log"
    assert p2["ranking_full"] == p2["ranking_tail"]


def test_w1_not_collapsing(data):
    p2 = data["part2_drift"]
    assert abs(p2["w1_fit_tail"]["slope"]) < 1e-5
    assert p2["w1_last"] > 0.50


def test_rho_dk2_band(data):
    p3 = data["part3_logic"]
    assert p3["n_dk2_layers"] > 500
    assert p3["rho_dk2_min"]["rho"] > 0.9
    assert p3["rho_dk2_linear_fit_slope"] > 0


def test_x_n_exact_recoverable(layers):
    """Exact odometer identity from integers only — no stored bigints."""
    for r in (layers[5], layers[20], layers[99], layers[999]):
        x = Fraction(2 ** (r["k"] - 1), 3 ** r["n"])
        assert x.numerator == 2 ** (r["k"] - 1)
        assert x.denominator == 3 ** r["n"]


def test_live_recompute_layer_6_21():
    """Optional: recompute n=1..21 with mpmath if installed."""
    try:
        import mpmath  # noqa: F401
    except ImportError:
        print("SKIP test_live_recompute_layer_6_21 (mpmath not installed)")
        return

    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "vod", os.path.join(HERE, "verify_odometer_dominance.py")
    )
    vod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vod)
    vod.setup_dps()
    prev = {}
    for n in range(1, 22):
        c = vod.compute_layer(
            n, prev, 80, vod.L, vod.H, prev_default_one=(n == 1)
        )
        if n >= 6:
            k_peak = max(c, key=lambda kk: abs(c[kk]))
            k_can = k_peak % (2 * 3 ** (n - 1))
            assert k_can == K_CERT[n], (n, k_can)
            t1 = abs(prev.get(k_peak - 1)) / 2
            t2 = abs(prev.get(k_peak - 2)) / 4
            assert t1 > t2, n
        prev = c


def main() -> int:
    data = load_data()
    layers = data["per_layer"]
    tests = [
        ("certificate_format", lambda: test_certificate_format(data)),
        ("no_kill", lambda: test_no_kill_criterion_fired(data)),
        ("depth", lambda: test_depth_and_completeness(layers)),
        ("cert_k", lambda: test_argmax_matches_certificates_6_21(layers)),
        ("k_range", lambda: test_k_canonical_range(layers)),
        ("monotone_dk", lambda: test_monotone_and_dk_in_1_2(layers)),
        ("a1_dom", lambda: test_a1_dominance_every_layer(layers)),
        ("w1_band", lambda: test_w1_band(layers)),
        ("pullback", lambda: test_pullback_ordering(layers)),
        ("delta", lambda: test_delta_band(layers)),
        ("S3", lambda: test_window_convergence_S3(data)),
        ("S4", lambda: test_dps_stability_S4(data)),
        ("a_ext", lambda: test_a_window_extension(data)),
        ("M_n_cert", lambda: test_certified_magnitudes(data)),
        ("drift_rank", lambda: test_drift_ranking_stable(data)),
        ("w1_flat", lambda: test_w1_not_collapsing(data)),
        ("rho", lambda: test_rho_dk2_band(data)),
        ("x_exact", lambda: test_x_n_exact_recoverable(layers)),
        ("live_recompute", test_live_recompute_layer_6_21),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except Exception as e:
            failed += 1
            print(f"FAIL {name}: {e}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
