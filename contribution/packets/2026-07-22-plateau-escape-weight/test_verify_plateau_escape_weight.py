#!/usr/bin/env python3
"""Tests for verify_plateau_escape_weight.py controls."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_plateau_escape_weight as v
import numpy as np


def small_stack(n_max=9):
    layers = dict(v.syracuse_float_layers(n_max))
    Cn = {n: np.fft.fft(P) for n, P in layers.items()}
    units = {n: v.unit_residues(3 ** n) for n in layers}
    mag = {n: np.abs(Cn[n]) for n in layers}
    M = {n: float(mag[n][units[n]].max()) for n in layers}
    peak = {n: v.peak_chain_data(mag[n], units[n], 3 ** n) for n in layers}
    return Cn, units, mag, M, peak


def test_exact_chain_phases_small():
    _, _, _, _, peak = small_stack(9)
    n = 9
    xi, K, sign = peak[n]
    assert K <= n + 3 and 2 ** K < 3 ** n
    ph = v.exact_chain_phases(K, sign, n)
    # residues are the exact integers 2^{K-a}, no wrap
    for a, (frac, res) in ph.items():
        assert res == 2 ** (K - a)
        assert frac == Fraction((sign * 2 ** (K - a)) % 3 ** n, 3 ** n)
    rel = (ph[1][0] - ph[2][0]) % 1
    assert min(rel, 1 - rel) == Fraction(2 ** (K - 2), 3 ** n)
    assert Fraction(2 ** (K - 2), 3 ** n) <= Fraction(2 ** (n + 1), 3 ** n)


def test_chain_recursion_identity():
    Cn, _, _, _, peak = small_stack(9)
    n = 9
    xi = peak[n][0]
    mod_old, mod_new = 3 ** (n - 1), 3 ** n
    rec = 0j
    for a in range(1, v.A_TRUNC + 1):
        u = pow(2, -a, mod_new)
        frac = ((xi * u) % mod_new) / mod_new
        rec += 2.0 ** (-a) * np.exp(-2j * np.pi * frac) * Cn[n - 1][(xi * u) % mod_old]
    assert abs(rec - Cn[n][xi]) < 1e-12


def test_t2_no_supersolution_control():
    rng = np.random.RandomState(1)
    mod = 3 ** 6
    q = rng.rand(mod) + 0.5
    q[np.arange(mod) % 3 == 0] = 0.0
    Tq = v.transport_same_layer(q, mod)
    U = v.unit_residues(mod)
    tail = 1.0 - 2.0 ** (-v.A_TRUNC)
    assert abs(Tq[U].sum() - tail * q[U].sum()) < 1e-9 * q[U].sum()
    assert float((Tq[U] / q[U]).min()) <= tail + 1e-12


def test_t4_containment_escape_bound_synthetic():
    # synthetic bad set = +/- two consecutive powers of 2 mod 3^5:
    # every unit of the next layer has bad-image weight <= 3/4, and the
    # bound is attained (tight), so w = 1/4 - 2^-40 exactly.
    n = 5
    mod_n = 3 ** n
    m = 20
    bad = np.zeros(mod_n, dtype=bool)
    for j in (0, 1):
        bad[pow(2, m - j, mod_n)] = True
        bad[(-pow(2, m - j, mod_n)) % mod_n] = True
    U_next = v.unit_residues(3 ** (n + 1))
    w, bw = v.escape_weights_next_layer(bad, mod_n, U_next)
    assert float(bw.max()) <= 1.0 - 2.0 ** (-2) + 1e-12
    assert abs(float(w.min()) - (0.25 - 2.0 ** (-v.A_TRUNC))) < 1e-9
    # three-block: w = 1/8 - 2^-40
    bad3 = np.zeros(mod_n, dtype=bool)
    for j in (0, 1, 2):
        bad3[pow(2, m - j, mod_n)] = True
        bad3[(-pow(2, m - j, mod_n)) % mod_n] = True
    w3, bw3 = v.escape_weights_next_layer(bad3, mod_n, U_next)
    assert float(bw3.max()) <= 1.0 - 2.0 ** (-3) + 1e-12
    assert abs(float(w3.min()) - (0.125 - 2.0 ** (-v.A_TRUNC))) < 1e-9


def test_t3_quantization_gap_and_s3():
    _, units, mag, M, peak = small_stack(9)
    for n in range(6, 9):
        mod_n = 3 ** n
        for eps in (0.05, 0.1, 0.2):
            bad = v.bad_mask(mag[n], M[n], eps, units[n])
            w, _ = v.escape_weights_next_layer(bad, mod_n, units[n + 1])
            w_min = float(w.min())
            xi_next = peak[n + 1][0]
            tri = sum(2.0 ** (-a) * mag[n][(xi_next * pow(2, -a, 3 ** (n + 1))) % mod_n]
                      for a in range(1, v.A_TRUNC + 1))
            assert tri >= M[n + 1] - 1e-12          # triangle bound
            assert (1 - eps * w_min) * M[n] >= tri - 1e-12  # S3 dominates it
            assert M[n + 1] <= (1 - eps * w_min) * M[n] + 1e-12


def test_t5_phaseblind_propagation_gap_positive():
    _, units, mag, M, _ = small_stack(9)
    for n in range(6, 9):
        mod_n = 3 ** n
        eps = 0.05
        bad = v.bad_mask(mag[n], M[n], eps, units[n])
        _, bw = v.escape_weights_next_layer(bad, mod_n, units[n + 1])
        bw_max = float(bw.max())
        cert_bound = (1 - eps * (1 - bw_max)) * M[n]
        threshold = (1 - eps) * M[n + 1]
        assert cert_bound > threshold  # phase-blind certification always fails
        assert M[n + 1] <= M[n] + 1e-15


def test_bad_set_containment_guard():
    _, units, mag, M, peak = small_stack(9)
    for n in range(8, 10):
        mod_n = 3 ** n
        K = peak[n][1]
        for eps in (0.05, 0.1, 0.2):
            bad = v.bad_mask(mag[n], M[n], eps, units[n])
            pts = np.nonzero(bad)[0]
            assert 0 < len(pts) <= 8
            for x in pts:
                k = v.chain_log(mod_n, int(x))
                assert k is not None and -1 <= K - k <= 2  # on the chain


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VEW_N_MAX="8")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_plateau_escape_weight.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "plateau_escape_weight_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["chain_recursion_identity_err"] < 1e-12
    assert all(r["contained_in_chain_interval"] for r in cert["escape_weight_table"])
    assert all(r["holds"] for r in cert["escape_weight_table"])
    assert all(r["t5_propagation_gap_over_M"] > 0 for r in cert["escape_weight_table"])
    t1 = cert["t1_exact_chain_phases"][-1]
    num, den = t1["dominant_pair_misalignment_exact"]
    assert Fraction(int(num), int(den)) == Fraction(2 ** (t1["K"] - 2), 3 ** t1["n"])
    assert cert["dichotomy_crossover"]["n_star"] > 1000
