#!/usr/bin/env python3
"""Tests for verify_plateau_drift_test.py controls."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_plateau_drift_test as v
import numpy as np
import pytest


def dense_stack(n_max):
    return {n: np.fft.fft(P)
            for n, P in v.syracuse_float_layers(n_max)}


def test_transport_np_matches_dense_fft():
    """The recursion identity, numpy path, against dense FFT ground truth
    at every layer n <= 9 (full unit vectors, both signs)."""
    Cn = dense_stack(9)
    C = np.array([1 + 0j], dtype=np.complex128)
    for n in range(1, 10):
        C = v.transport_np(C, n)
        mod = 3 ** n
        r = np.arange(mod, dtype=np.uint64)
        U = r[r % 3 != 0]
        d = np.abs(np.abs(Cn[n][U])
                   - np.abs(v.c_at_many(C, n, U))).max()
        assert d < 1e-11, (n, d)


def test_c_kernel_matches_numpy():
    """The C transport kernel agrees with the numpy reference to 1e-13 at
    every layer n <= 10 (multithreaded; determinism is exercised by the
    certificate test below)."""
    fn = v.load_c_kernel()
    if fn is None:
        pytest.skip("clang unavailable")
    C_ref = np.array([1 + 0j], dtype=np.complex128)
    C_c = np.array([1 + 0j], dtype=np.complex128)
    for n in range(1, 11):
        C_ref = v.transport_np(C_ref, n)
        C_c = v.transport_c(fn, C_c, n, 4)
        assert np.abs(C_c - C_ref).max() < 1e-13, n


def test_half_unit_indexing_roundtrip():
    for n in (3, 6, 9):
        mod = 3 ** n
        h = v.half_count(n)
        assert h == 3 ** (n - 1)
        us = [v.unit_from_half_index(j) for j in range(h)]
        assert all(u % 3 != 0 and 2 * u < mod for u in us)
        assert [v.half_index_of_unit(u) for u in us] == list(range(h))
        # conjugate partner maps to the same slot with the flip
        C = np.arange(h) + 1j * np.arange(h)
        for u in (us[0], us[-1], us[h // 2]):
            assert v.c_at(C, n, u) == complex(
                C[v.half_index_of_unit(u)])
            assert v.c_at(C, n, mod - u) == complex(
                C[v.half_index_of_unit(u)].conjugate())


def test_chain_exponent_bsgs_vs_bruteforce():
    """Exact discrete-log certificate against a brute-force reference
    (provenance: chain_log_bruteforce of the deep-fourier packet)."""
    mod = 3 ** 7
    want = {}
    p = 1
    for k in range(2 * (mod // 3)):
        want.setdefault(p, k)
        p = (2 * p) % mod
    for xi in (1, 5, 64, pow(2, 10, mod), (-pow(2, 7, mod)) % mod,
               mod - 1):
        k = v.chain_exponent(mod, xi)
        assert k is not None
        assert pow(2, k, mod) in (xi % mod, (-xi) % mod)
        if xi % mod in want:
            assert k <= want[xi % mod]
    assert v.chain_exponent(mod, 3) is None      # non-unit
    assert v.chain_log_bsgs(mod, 0) is None


def test_exact_chain_phases_no_wrap():
    ph = v.exact_chain_phases(12, 1, 10)
    for a, (frac, res) in ph.items():
        assert res == 2 ** (12 - a)
        assert frac == Fraction(res, 3 ** 10)
    rel = (ph[1][0] - ph[2][0]) % 1
    assert min(rel, 1 - rel) == Fraction(2 ** 10, 3 ** 10)
    ph = v.exact_chain_phases(12, -1, 10)
    assert ph[1][1] == 3 ** 10 - 2 ** 11


def test_exact_escape_weights_match_full_sweep():
    """The candidate-set minimum (new, used at all depths) equals the
    brute-force minimum over ALL next-layer units, n = 6..8."""
    Cn = dense_stack(9)
    for n in range(6, 9):
        mod = 3 ** n
        mag = np.abs(Cn[n])
        mag3 = mag.reshape(mod // 3, 3)
        M = float(mag3[:, 1:].max())
        for eps in (0.05, 0.2):
            over = mag3[:, 1:] > (1.0 - eps) * M
            rows = np.nonzero(over.ravel())[0]
            bad = {int(3 * (r // 2) + 1 + (r % 2)) for r in rows}
            # brute force over all units of the next layer
            mod_next = 3 * mod
            U = np.arange(mod_next, dtype=np.uint64)
            U = U[U % 3 != 0]
            bad_arr = np.zeros(mod, dtype=bool)
            bad_arr[list(bad)] = True
            w = np.zeros(U.size, dtype=np.float64)
            for a in range(1, v.A_TRUNC + 1):
                mapped = (U * pow(2, -a, mod)) % mod
                w += 2.0 ** (-a) * (~bad_arr[mapped])
            w_brute = float(w.min())
            # candidate-set (exact) path used by the verifier
            u_inv = [pow(2, -a, mod) for a in range(1, v.A_TRUNC + 1)]
            cand = v.escape_weight_candidates(bad, mod)
            w_cand = min(v.escape_weight_exact(bad, u_inv, mod, eta)
                         for eta in cand)
            assert w_cand == w_brute, (n, eps, w_cand, w_brute)


def test_w_tightness_synthetic():
    """Synthetic bad block of length L on the chain: w = 2^-L - 2^-40
    exactly, attained at the chain successor (P4 tightness)."""
    n = 5
    mod = 3 ** n
    m = 20
    u_inv = [pow(2, -a, mod) for a in range(1, v.A_TRUNC + 1)]
    for L in (1, 2, 3):
        bad = set()
        for j in range(L):
            bad.add(pow(2, m - j, mod))
            bad.add((-pow(2, m - j, mod)) % mod)
        cand = v.escape_weight_candidates(bad, mod)
        w_min = min(v.escape_weight_exact(bad, u_inv, mod, eta)
                    for eta in cand)
        assert abs(w_min - (2.0 ** (-L) - 2.0 ** (-v.A_TRUNC))) < 1e-12


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VPDT_N_MAX="12", VPDT_DENSE_MAX="12")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here,
                                          "verify_plateau_drift_test.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "plateau_drift_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)

    # regression gate against the predecessor certificates
    assert cert["regression_vs_predecessors"]["all_passed"]
    # dense FFT cross-check of the recursion engine
    assert cert["dense_cross_check"]
    assert max(r["max_abs_mag_diff"] for r in cert["dense_cross_check"]) \
        < 1e-9
    # counterexample watch: no off-chain bad frequency, no S3 violation
    assert cert["counterexample_watch"]["(a)_off_chain_bad_frequency"][
        "fired"] is False
    esc = cert["escape_weight_table"]
    assert all(r["holds"] for r in esc if r["holds"] is not None)
    # P4 tightness: w = 2^-L - 2^-40 exactly at every row
    for r in esc:
        L = r["interval_length_L"]
        assert abs(r["escape_weight_min"]
                   - (2.0 ** (-L) - 2.0 ** (-40))) < 1e-12
        assert r["mode"] == "exact"
    # certified anchor values (deep-fourier packet)
    rows = {r["n"]: r for r in cert["layer_table"]}
    assert abs(rows[12]["M_n"] - 0.02645816923038526) < 1e-9
    assert rows[12]["chain_log_k"] == 14
    # drift machinery present and self-consistent
    drift = cert["drift_test"]
    assert drift["p2_prediction_threshold"] == 0.95
    fit = drift["profile_fits"]["p2"]
    row12 = [r for r in drift["p2_vs_extrapolation"] if r["n"] == 12][0]
    assert abs(row12["p2_extrapolated_from_n<=14_fit"]
               - (fit["slope_per_layer_fit_n8..14"] * 12
                  + fit["intercept_fit_n8..14"])) < 1e-12
    assert abs(row12["residual"]
               - (row12["p2_measured"]
                  - row12["p2_extrapolated_from_n<=14_fit"])) < 1e-15
    # T1 exact phases present at the final layer
    assert rows[12]["t1_dominant_pair_misalignment_exact"] == \
        [str(2 ** (rows[12]["chain_log_k"] - 2)), str(3 ** 12)]
