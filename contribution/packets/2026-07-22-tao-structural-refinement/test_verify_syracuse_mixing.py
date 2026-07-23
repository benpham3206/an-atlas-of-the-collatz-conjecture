#!/usr/bin/env python3
"""Tests for verify_syracuse_mixing.py controls."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_syracuse_mixing as v
import numpy as np


def test_exact_matches_paper_vectors():
    assert v.syracuse_exact(1) == v.PAPER_P1
    assert v.syracuse_exact(2) == v.PAPER_P2


def test_exact_distribution_properties():
    P = v.syracuse_exact(3)
    assert sum(P) == 1
    assert all(P[x] == 0 for x in range(27) if x % 3 == 0)
    assert all(p >= 0 for p in P)


def test_float_matches_exact_small_n():
    exact = {n: v.syracuse_exact(n) for n in (1, 2, 3)}
    for n, Pf in v.syracuse_float_layers(3):
        diff = float(np.abs(Pf - np.array([float(p) for p in exact[n]])).max())
        assert diff < 1e-9
    assert abs(float(Pf.sum()) - 1.0) < 1e-9


def test_multiples_of_3_carry_no_mass_float():
    for n, P in v.syracuse_float_layers(6):
        assert np.all(P[np.arange(P.size) % 3 == 0] == 0.0)


def test_char_function_bounded_by_one():
    for n, P in v.syracuse_float_layers(4):
        mc, _ = v.char_function_max(P)
        assert 0.0 <= mc <= 1.0 + 1e-9


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VSM_EXACT_N="3", VSM_N_MAX="8")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_syracuse_mixing.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "syracuse_mixing_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["exact_matches_paper_n1"] and cert["exact_matches_paper_n2"]
    assert all(r["zero_mass_on_multiples_of_3"] for r in cert["decay_table"])
