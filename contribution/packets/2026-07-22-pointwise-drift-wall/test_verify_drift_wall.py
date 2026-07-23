#!/usr/bin/env python3
"""Tests for verify_drift_wall.py controls."""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_drift_wall as v


# --- word generators against hardcoded classical prefixes -------------------

def test_thue_morse_prefix():
    assert v.thue_morse(16) == [0, 1, 1, 0, 1, 0, 0, 1,
                                1, 0, 0, 1, 0, 1, 1, 0]


def test_rudin_shapiro_prefix():
    # OEIS A020985 (with a(0)=0 convention)
    assert v.rudin_shapiro(16) == [0, 0, 0, 1, 0, 0, 1, 0,
                                   0, 0, 0, 1, 1, 1, 0, 1]


def test_paperfolding_prefix():
    # OEIS A014577
    assert v.paperfolding(16) == [1, 1, 0, 1, 1, 0, 0, 1,
                                  1, 1, 0, 0, 1, 0, 0, 1]


def test_period_doubling_prefix():
    assert v.period_doubling(8) == [0, 1, 0, 0, 0, 1, 0, 1]


def test_fibonacci_word_prefix():
    assert v.fibonacci_word(13) == [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]


def test_champernowne_prefix():
    # binary(1), binary(2), ... = 1 10 11 100 ...
    assert v.champernowne_binary(10) == [1, 1, 0, 1, 1, 1, 0, 0, 1, 0]


# --- exact certificates ------------------------------------------------------

def test_alpha_bounds():
    b = v.certify_alpha_bounds()
    assert b["lower_63_over_100"] and b["upper_631_over_1000"]


def test_lemma1_and_lemma3_small_orbits():
    for n in range(1, 33):
        orbit = v.terras_orbit(n)
        assert orbit[-1] == 1
        ok1, _ = v.check_lemma1_identity(orbit)
        ok3, _ = v.check_lemma3_envelope(orbit)
        assert ok1 and ok3


def test_lemma1_orbit_27():
    orbit = v.terras_orbit(27)
    ok1, _ = v.check_lemma1_identity(orbit)
    assert ok1
    assert len(orbit) == 71 and max(orbit) == 4616  # Terras-form 27 record


# --- density machinery -------------------------------------------------------

def test_density_control_detects_violation():
    bad = [1] * 20000  # density 1, must fail the 63/100 bound
    ctl = v.density_control(bad, warm=1 << 10)
    assert not ctl["final_below_63_over_100"]
    assert not ctl["max_tail_below_63_over_100"]


def test_named_words_pass_bound():
    for gen in v.WORDS.values():
        ctl = v.density_control(gen(1 << 16))
        assert ctl["final_below_63_over_100"]
        assert ctl["max_tail_below_63_over_100"]


# --- end-to-end determinism --------------------------------------------------

def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VDW_N=str(1 << 18))
    out1 = subprocess.run(
        [sys.executable, os.path.join(here, "verify_drift_wall.py")],
        capture_output=True, text=True, cwd=tmp_path, env=env)
    assert out1.returncode == 0, out1.stderr
    first = (tmp_path / "drift_wall_certificate.json").read_text()
    out2 = subprocess.run(
        [sys.executable, os.path.join(here, "verify_drift_wall.py")],
        capture_output=True, text=True, cwd=tmp_path, env=env)
    second = (tmp_path / "drift_wall_certificate.json").read_text()
    assert first == second
    cert = json.loads(first)
    assert cert["alpha_bounds"]["lower_63_over_100"]
    assert all(c["lemma1_identity_exact"] and c["lemma3_envelope_exact"]
               for c in cert["orbit_exact_checks"].values())
