#!/usr/bin/env python3
"""Tests for verify_syracuse_fourier.py controls."""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_syracuse_fourier as v
import numpy as np


def test_char_recursion_exact_small():
    layers = dict(v.syracuse_float_layers(4))
    err = v.char_recursion_check(layers[3], layers[4], [1, 2, 40, 3**4 - 1], 3)
    assert err < 1e-9


def test_lemma2_bound_every_layer():
    layers = dict(v.syracuse_float_layers(8))
    r_prev = None
    for n in range(1, 9):
        r = float(layers[n].max())
        if r_prev is not None:
            bound = (2 / 3) * r_prev / (1.0 - 2.0 ** (-2 * 3 ** (n - 2)))
            assert r <= bound + 1e-15
        r_prev = r


def test_parseval_identity():
    layers = dict(v.syracuse_float_layers(5))
    P = layers[5]
    lhs = float((np.abs(np.fft.fft(P)) ** 2).sum() / P.size)
    rhs = float((P ** 2).sum())
    assert abs(lhs - rhs) < 1e-9
    assert rhs <= float(P.max())


def test_primitive_root_2():
    assert all(v.is_primitive_root_2(n) for n in range(1, 6))


def test_walk_eigenvalue_formula():
    for n in (1, 2, 3):
        res = v.walk_eigenvalue_check(n)
        assert res["formula_max_abs_err"] < 1e-9
        assert 0 < res["spectral_gap"] < 1


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VSF_N_MAX="10")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_syracuse_fourier.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "syracuse_fourier_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["char_recursion_check"]
    assert all(r.get("lemma2_bound_holds", True) for r in cert["r_n_table"])
