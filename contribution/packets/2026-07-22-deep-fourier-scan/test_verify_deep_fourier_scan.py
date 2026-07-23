#!/usr/bin/env python3
"""Tests for verify_deep_fourier_scan.py controls."""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_deep_fourier_scan as v
import numpy as np


def test_unit_index_mapping():
    assert [v.unit_from_index(j) for j in range(8)] == [1, 2, 4, 5, 7, 8, 10, 11]
    arr = v.unit_index_array(6)
    assert arr.tolist() == [1, 2, 4, 5, 7, 8]
    assert arr.dtype == np.uint64


def test_chain_log_bsgs_matches_bruteforce():
    for n in range(1, 7):
        mod = 3 ** n
        for xi in (1, 2, 5, 7, 11, 64 % mod, mod - 1, mod - 2):
            assert v.chain_exponent(mod, xi) == v.chain_log_bruteforce(mod, xi)
        # multiples of 3 have no logarithm
        assert v.chain_exponent(mod, 3) is None
    # known chain exponent: 2^17 = 131072 is the peak at n = 14
    assert v.chain_log_bsgs(3 ** 14, 131072) == 17


def test_lemma2_bound_every_layer():
    r_prev = None
    for n, P in v.syracuse_float_layers(8):
        r = float(P.max())
        if r_prev is not None:
            bound = (2 / 3) * r_prev / (1.0 - 2.0 ** (-2 * 3 ** (n - 2)))
            assert r <= bound + 1e-15
        r_prev = r


def test_s1_identity_small():
    layers = dict(v.syracuse_float_layers(5))
    C3, C4 = np.fft.fft(layers[3]), np.fft.fft(layers[4])
    err = v.s1_second_moment_check(C3, C4, [1, 2, 5, 40, 3 ** 4 - 1], 3)
    assert err < 1e-9


def test_bad_set_regressions_match_scalar_phase_certificate():
    # values from scalar_phase_certificate.json (n = 6, 7, 8)
    expected = {6: (2, 4, 4, 6), 7: (2, 4, 4, 8), 8: (2, 2, 6, 9)}
    for n, P in v.syracuse_float_layers(8):
        if n < 6:
            continue
        mag = np.abs(np.fft.fft(P))
        mod = 3 ** n
        M = float(mag.reshape(mod // 3, 3)[:, 1:].max())
        counts = tuple(int(v.bad_indices(mag, M, eps).size)
                       for eps in (0.05, 0.1, 0.2))
        mag3 = mag.reshape(mod // 3, 3)
        peak_flat = int(mag3[:, 1:].argmax())
        xi_peak = 3 * (peak_flat // 2) + 1 + (peak_flat % 2)
        k = v.chain_exponent(mod, xi_peak)
        b05, b01, b02, kexp = expected[n]
        assert counts == (b05, b01, b02), (n, counts)
        assert k == kexp, (n, k)


def test_escape_weights_bounds():
    layers = dict(v.syracuse_float_layers(6))
    mag = np.abs(np.fft.fft(layers[6]))
    mod = 3 ** 6
    M = float(mag.reshape(mod // 3, 3)[:, 1:].max())
    idx = v.bad_indices(mag, M, 0.1)
    bad = np.zeros(mod, dtype=bool)
    bad[idx] = True
    U = v.unit_index_array(2 * (mod // 3))
    w = v.escape_weights(bad, U, mod)
    # the chain peak's own orbit stays on the bad set, so the MIN over all
    # units is small (this is exactly why S3 gives only e^{-c sqrt(n)});
    # the MEAN over units is ~1 (scalar-phase certificate: 0.9924 at n=6)
    assert 0.2 < w.min() < 0.5
    assert w.mean() >= 0.98
    assert w.max() <= 1.0 + 1e-15


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VDFS_N_MAX="8")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_deep_fourier_scan.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "deep_fourier_scan_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["kill_criteria_status"]["kc1_fired"] is False
    assert cert["kill_criteria_status"][
        "chain_law_k_in_n..n+3_holds_all_layers"] is True
    assert cert["s1_second_moment"]
    assert all(r["holds"] for r in cert["s3_escape_criterion"]
               if not r["sampled"])
