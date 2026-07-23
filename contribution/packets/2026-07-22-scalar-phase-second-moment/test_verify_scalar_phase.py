#!/usr/bin/env python3
"""Tests for verify_scalar_phase.py controls."""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_scalar_phase as v
import numpy as np


def test_s1_identity_small():
    layers = dict(v.syracuse_float_layers(7))
    C3, C4 = np.fft.fft(layers[3]), np.fft.fft(layers[4])
    err = v.s1_second_moment_check(C3, C4, [1, 2, 5, 40, 3 ** 4 - 1], 3)
    assert err < 1e-9


def test_s2_conditional_contraction():
    layers = dict(v.syracuse_float_layers(7))
    Cn = {n: np.fft.fft(P) for n, P in layers.items()}
    n = 6
    U = v.unit_residues(3 ** n)
    M = float(np.abs(Cn[n])[U].max())
    for xi in (1, 2, 5, 128, 1024, 2048):
        eta, _ = v.s2_relative_phase(Cn[n], xi, n)
        c_next = abs(Cn[n + 1][xi])
        assert c_next <= (1 - eta / 6) * M + 1e-12


def test_s3_escape_criterion_small_layers():
    layers = dict(v.syracuse_float_layers(8))
    Cn = {n: np.fft.fft(P) for n, P in layers.items()}
    for n in range(3, 8):
        U = v.unit_residues(3 ** n)
        mag = np.abs(Cn[n])
        M = float(mag[U].max())
        M_next = float(np.abs(Cn[n + 1])[v.unit_residues(3 ** (n + 1))].max())
        for eps in (0.05, 0.1, 0.2):
            w, _ = v.escape_weight_profile(mag, M, eps, U)
            assert M_next <= (1 - eps * float(w.min())) * M + 1e-12


def test_bad_set_conjugate_symmetry():
    layers = dict(v.syracuse_float_layers(8))
    P = layers[8]
    mag = np.abs(np.fft.fft(P))
    mod = P.size
    U = v.unit_residues(mod)
    M = float(mag[U].max())
    bad = U[mag[U] > 0.9 * M]
    bad_set = set(int(x) for x in bad)
    assert all((mod - x) % mod in bad_set for x in bad_set)
    assert len(bad_set) % 2 == 0


def test_chain_log():
    assert v.chain_log(3 ** 5, 2 ** 7 % 3 ** 5) == 7
    assert v.chain_log(3 ** 5, (-2 ** 7) % 3 ** 5) == 7
    # 3 is not a unit, hence not +/- a power of 2 mod 3^5
    assert v.chain_log(3 ** 5, 3) is None


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VSP_N_MAX="10")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_scalar_phase.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "scalar_phase_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["s1_second_moment"]["max_abs_err"] < 1e-8
    assert all(r["holds"] for r in cert["s3_escape_criterion"])
    assert all(t["chain_log_k"] <= 3 * t["n"] for t in cert["bad_set_table"])
    assert cert["peak_decomposition"]["identity_err"] < 1e-9
