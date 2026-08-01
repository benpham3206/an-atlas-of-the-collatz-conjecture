#!/usr/bin/env python3
"""Tests for verify_chain_exponent_law.py (exact structural verdicts +
reduced-depth chain-recursion controls)."""

import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import verify_chain_exponent_law as v

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "chain_exponent_law_results.json")

K_CERT = {6: 6, 7: 8, 8: 9, 9: 10, 10: 12, 11: 13, 12: 14, 13: 16,
          14: 17, 15: 18, 16: 20, 17: 21, 18: 23, 19: 24, 20: 26, 21: 28}


# ---------------------------------------------------------- test 1

def test_beatty_interval_empty_exact():
    low, high, wit_low, wit_high = v.beatty_feasible_gamma_interval(K_CERT)
    assert isinstance(low, Fraction) and isinstance(high, Fraction)
    assert low == Fraction(3, 2) and high == Fraction(11, 8)
    assert not low < high  # empty open interval -> kill criterion (a)


def test_beatty_witness_pairs():
    # gamma > 3/2 is forced by (k(21), k(15)); gamma < 11/8 by (k(7), k(15))
    _, _, wit_low, wit_high = v.beatty_feasible_gamma_interval(K_CERT)
    assert set(wit_low) == {21, 15}
    assert set(wit_high) == {7, 15}


# ---------------------------------------------------------- test 2

def test_delta_word_two_valued_and_unbalanced():
    dk = v.delta_word(K_CERT)
    assert dk == [2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2]
    worst, witness = v.balance_report(dk)
    assert worst == 2                      # kill criterion (b)
    length, lo_f, hi_f, lo_s, hi_s = witness
    assert length == 2 and lo_f == [1, 1] and hi_f == [2, 2]
    assert lo_s == 2 and hi_s == 4


def test_slope_density_exact():
    dk = v.delta_word(K_CERT)
    assert Fraction(sum(dk), len(dk)) == Fraction(22, 15)
    assert v.cf_of_fraction(Fraction(22, 15)) == [1, 2, 7]


# ---------------------------------------------------------- test 3

def test_cf_log2_3_and_convergents():
    cf = v.cf_of_log2_3(terms=12)
    assert cf[:10] == [1, 1, 1, 2, 2, 3, 1, 5, 2, 23]
    conv = v.convergents(cf)
    assert conv[:5] == [Fraction(1), Fraction(2), Fraction(3, 2),
                        Fraction(8, 5), Fraction(19, 12)]
    semi = v.semiconvergents(cf)
    assert semi[:2] == [Fraction(5, 3), Fraction(11, 7)]
    # the empirical slope 22/15 is not in the CF tree of log2(3)
    assert Fraction(22, 15) not in conv
    assert Fraction(22, 15) not in semi


def test_round_laws_fail_for_all_candidate_slopes():
    import math
    log23 = math.log2(3)
    errs = {K_CERT[n] - int(n * log23 + 0.5) for n in K_CERT}
    assert len(errs) > 1  # k(n) != round(n*log2(3)) + const
    assert errs == {-3, -4, -5, -6}


# ---------------------------------------------------------- test 4

def test_chain_closure_identity_exact():
    # u_a * 2^k = 2^(k-a) mod 3^n for every small n, a, k (exact integers)
    for n in range(2, 10):
        m = 3 ** n
        for a in range(1, 8):
            ua = pow(pow(2, a, m), -1, m)
            for k in range(0, 12):
                lhs = (ua * pow(2, k, m)) % m
                rhs = pow(2, (k - a) % (2 * 3 ** (n - 1)), m)
                assert lhs == rhs, (n, a, k)


def test_chain_recursion_reproduces_k_reduced_depth():
    """Float64 evaluation of the exact-integer-phase chain recursion at
    reduced depth: argmax_k |c_n[k]| equals the certified k(n), n=6..12."""
    layers = v.chain_recursion(12)
    for n in range(6, 13):
        c, _ = layers[n]
        bk = max(range(0, 3 * n + 5), key=lambda kk: abs(c[kk]))
        assert bk == K_CERT[n], (n, bk, K_CERT[n])


def test_dominant_pullback_is_a1_reduced_depth():
    layers = v.chain_recursion(12)
    for n in range(7, 13):
        wa, (r, m), a_dom = v.dominant_pullback(layers, K_CERT, n)
        assert a_dom == 1, (n, a_dom)
        assert m == 3 ** n and 0 < r < m


def test_sawtooth_recursion_exact():
    # x_n = 2^(k(n)-1)/3^n obeys x_n = (2^dk/3) x_{n-1} exactly
    ns = sorted(K_CERT)
    xs = {n: Fraction(2 ** (K_CERT[n] - 1), 3 ** n) for n in ns}
    for i in range(1, len(ns)):
        n, p = ns[i], ns[i - 1]
        dk = K_CERT[n] - K_CERT[p]
        assert xs[n] == Fraction(2 ** dk, 3) * xs[p]


# --------------------------------------------- certificate consistency

def test_certificates_cross_agree():
    deep, drift, stream = v.load_certificates()
    k, M, L, p2 = v.assemble_table(deep, drift, stream)
    assert k == K_CERT
    assert abs(p2[21] - 0.8872812875738992) < 1e-12
    assert abs(M[21] - 0.007872132965024493) < 1e-15


def test_results_json_matches_verifier(tmp_path):
    out = tmp_path / "r.json"
    env = dict(os.environ)
    subprocess.run(
        [sys.executable, os.path.join(HERE, "verify_chain_exponent_law.py")],
        check=True, env=env, capture_output=True)
    with open(RESULTS) as f:
        d = json.load(f)
    assert d["test1_beatty"]["feasible"] is False
    assert d["test1_beatty"]["gamma_low"] == "3/2"
    assert d["test1_beatty"]["gamma_high"] == "11/8"
    assert d["test2_sturmian"]["max_imbalance"] == 2
    assert d["test2_sturmian"]["slope_density"] == "22/15"
    assert d["test3_cf_convergents"]["cf_log2_3_first12"][:6] == [1, 1, 1, 2, 2, 3]
    t4 = d["test4_chain_recursion"]
    assert t4["argmax_matches_certified_all_layers"] is True
    assert t4["M_n_max_rel_err_vs_certificates"] < 1e-12
    assert t4["threshold_separates_dk_tail"] is True
    kc = d["kill_criteria"]
    assert kc["(a)_feasible_interval_empty"] is True
    assert kc["(b)_delta_k_unbalanced"] is True
    assert kc["(c)_residual_drift_past_1"] is True
    assert max(kc["prior_fit_residuals"].values(),
               key=lambda s: float(s)) is not None
    assert float(kc["prior_fit_residuals"]["21"]) > 1
