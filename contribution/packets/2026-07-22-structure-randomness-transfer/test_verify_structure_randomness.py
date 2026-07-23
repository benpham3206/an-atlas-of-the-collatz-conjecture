#!/usr/bin/env python3
"""Tests for verify_structure_randomness.py controls."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_structure_randomness as v


def test_critical_line():
    assert all(v.certify_critical_line().values())


def test_qstar_prefix():
    # base-3 reps of 1..6: 1,2,10,11,12,20 -> digits 1,2,1,0,1,1,1,2,2,0
    # mapped by phi: 0,1 -> 1, 2 -> 0
    w, used = v.biased_champernowne(17)
    assert w == [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1]
    assert used >= 6


def test_phi_mod_crosscheck_fraction():
    # independent Fraction computation of Phi(q) mod 2^N on a random prefix
    import random
    rng = random.Random(20260722)
    N = 64
    word = [rng.randint(0, 1) for _ in range(N)]
    got, _ = v.phi_mod(word, N)
    num, den = 0, 1
    j = 0
    for pos, bit in enumerate(word):
        if bit:
            num = num * 3 + (1 << pos)
            den *= 3
            j += 1
    # Phi = -num/den exactly (finite sum); reduce mod 2^N
    M = 1 << N
    expect = (-num * pow(den, -1, M)) % M
    assert got == expect


def test_periodic_control_realizable():
    N = 1 << 12
    phi, _ = v.phi_mod([1, 0] * (N // 2), N)
    assert phi == 1  # Phi((10)^inf) = 1, lift digits eventually zero


def test_full_complexity_small():
    cert = v.full_complexity_certificate(k_max=6)
    assert cert["full_complexity_certified"]
    for k, rec in cert["per_k"].items():
        assert rec["distinct_factors"] == rec["expected"]


def test_density_above_wall():
    word, _ = v.biased_champernowne(1 << 16)
    ctl = v.density_control(word)
    assert ctl["above_631_over_1000"]


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VSR_DENSITY_N=str(1 << 16),
               VSR_KMAX="8", VSR_LIFT_N=str(1 << 14))
    for contents in ("first", "second"):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_structure_randomness.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        if contents == "first":
            first = (tmp_path / "structure_randomness_certificate.json").read_text()
        else:
            assert (tmp_path / "structure_randomness_certificate.json").read_text() == first
    cert = json.loads(first)
    assert cert["lift_digits"]["periodic_control"]["phi_equals_1"]
    assert cert["lift_digits"]["test_object"]["has_set_digit_above_N_over_2"]
    assert cert["full_complexity"]["full_complexity_certified"]
