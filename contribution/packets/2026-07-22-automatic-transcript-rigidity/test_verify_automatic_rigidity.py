#!/usr/bin/env python3
"""Tests for verify_automatic_rigidity.py controls."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_automatic_rigidity as v


def test_phi_engine_trivial_cycles():
    assert v.phi_mod([1, 0] * 32, 64) == 1
    assert v.phi_mod([0, 1] * 32, 64) == 2
    assert v.phi_periodic_fraction([1, 0]) == 1
    assert v.phi_periodic_fraction([0, 1]) == 2
    assert v.phi_periodic_fraction([1, 1, 0]) == -5  # supercritical period
    for word, frac in (([1, 0], 1), ([0, 1], 2), ([1, 1, 0], -5)):
        w = (word * 64)[:64]
        assert v.phi_mod(w, 64) == v.fraction_to_mod(Fraction(frac), 64)


def test_orbit_cross_check_small():
    for n in range(1, 201):
        q = v.terras_transcript(n, 64)
        assert v.phi_mod(q, 64) == n % (1 << 64)


def test_comparator_exact():
    # rho < log_3 2  iff  3^a < 2^b for rho = a/b
    assert v.cmp_fraction_vs_alpha(Fraction(1, 2)) == -1
    assert v.cmp_fraction_vs_alpha(Fraction(2, 3)) == 1
    assert v.cmp_fraction_vs_alpha(Fraction(63, 100)) == -1
    assert v.cmp_fraction_vs_alpha(Fraction(64, 100)) == 1
    assert 3 ** 63 < 2 ** 100
    assert 12500 > 7569  # sqrt5 > 87/50, the Fibonacci-word witness


def test_freq_vector_binary_gap_example():
    M = v.incidence(((1, 1), (1, 0)), 2)
    assert v.is_primitive(M, 2)
    freq = v.freq_vector_exact(M, 2, 2)
    assert freq == [Fraction(1, 3), Fraction(2, 3)]
    assert v.cmp_fraction_vs_alpha(freq[1]) == 1  # 2/3 > log_3 2


def test_period_witness_exact():
    # sigma(0)=sigma(1)=01 has fixed point (01)^omega: witness must pass
    sigma = ((0, 1), (0, 1))
    word = v.fixed_point_prefix(sigma, 0, 64)
    assert v.period_witness_check(sigma, 0, 2, word)
    assert v.phi_periodic_fraction(word[:2]) == 2
    # Thue-Morse morphism: no small exact period witness
    tm = ((0, 1), (1, 0))
    tw = v.fixed_point_prefix(tm, 0, 256)
    assert not any(v.period_witness_check(tm, 0, p, tw) for p in range(1, 9))


def test_gap_example_self_similarity():
    u = v.gap_example_word(1 << 10)
    for i in range(200):
        assert u[2 * i] == 1
        assert u[4 * i + 1] == 0
        assert u[4 * i + 3] == u[i]


def test_named_families_densities_numeric():
    n = 1 << 12
    assert abs(sum(v.thue_morse(n)) / n - 0.5) < 0.02
    assert abs(sum(v.period_doubling(n)) / n - 1 / 3) < 0.02
    assert abs(sum(v.rudin_shapiro(n)) / n - 0.5) < 0.02
    assert abs(sum(v.paperfolding(n)) / n - 0.5) < 0.02
    assert abs(sum(v.fibonacci_word(n)) / n - 0.381966) < 0.01


def test_oscillator_controls():
    sup = v.supercritical_oscillator(1 << 12)
    s = 0
    ratios = []
    for L in range(1, len(sup) + 1):
        s += sup[L - 1]
        if L >= 64:
            ratios.append(s / L)
    assert min(ratios) > 0.66            # liminf = 2/3 > alpha
    osc = v.block_oscillator(1 << 13)
    assert sum(osc[:4 ** 6]) / 4 ** 6 < 0.34
    assert sum(osc[:2 * 4 ** 6]) / (2 * 4 ** 6) > 0.66


def test_certificate_deterministic(tmp_path):
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, VATR_REDUCED="1")
    first = None
    for _ in range(2):
        out = subprocess.run(
            [sys.executable, os.path.join(here, "verify_automatic_rigidity.py")],
            capture_output=True, text=True, cwd=tmp_path, env=env)
        assert out.returncode == 0, out.stderr
        text = (tmp_path / "automatic_rigidity_certificate.json").read_text()
        if first is None:
            first = text
        else:
            assert text == first
    cert = json.loads(first)
    assert cert["candidate_scan"]["aperiodic_window_stabilized_candidates"] == 0
    assert cert["candidate_scan"]["periodic_words_with_positive_integral_Phi"] == ["1", "2"]
    assert cert["engine_validation_orbits"]["all_passed"]
