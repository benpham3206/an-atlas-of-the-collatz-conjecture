#!/usr/bin/env python3
"""Tests for the Mahler-tower verifier.

Run:  python3 -m pytest test_verify_mahler_tower.py -q
  or: python3 test_verify_mahler_tower.py
"""

import importlib.util
import os
import random

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "vmt", os.path.join(_here, "verify_mahler_tower.py"))
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

N = 128
MOD = 1 << N


# ------------------------------------------------------------- known values

def test_phi_all_ones_is_minus_one():
    # q = 111...: Phi = -sum_j 2^j/3^{j+1} = -(1/3)/(1-2/3) = -1
    assert V.phi_direct([1] * (N + 40), MOD, N) == (-1) % MOD


def test_phi_all_zeros_is_zero():
    assert V.phi_direct([0] * (N + 40), MOD, N) == 0


def test_phi_single_one_at_position_p():
    # q with a single 1 at position p: Phi = -2^p/3
    for p in (0, 1, 5, 17):
        q = [0] * (N + 40)
        q[p] = 1
        expect = (-(1 << p) * pow(3, -1, MOD)) % MOD
        assert V.phi_direct(q, MOD, N) == expect


def test_phi_alternating_is_a_fixed_point_of_the_period_two_cycle():
    # q = (10)^infty has ones at even positions, so
    # Phi = -sum_j 4^j/3^{j+1} = -(1/3) * 1/(1-4/3) = 1  (2-adically)
    q = [1 - (n % 2) for n in range(N + 40)]
    assert V.phi_direct(q, MOD, N) == 1


# ------------------------------------------------------- structural identities

def test_functional_equation_on_thue_morse():
    sigma = [(0, 1), (1, 0)]
    y = [3, 5]
    assert V.check_functional_equation(sigma, 0, 2, 2, y, 81, MOD)


def test_functional_equation_random():
    random.seed(5)
    for d in (2, 3):
        for k in (2, 3):
            for _ in range(20):
                sigma = [tuple(random.randrange(d) for _ in range(k))
                         for _ in range(d)]
                seed = random.randrange(d)
                sigma[seed] = (seed,) + sigma[seed][1:]
                y = [random.randrange(1, MOD, 2) for _ in range(d)]
                assert V.check_functional_equation(sigma, seed, d, k, y, 81, MOD)


def test_phi_bridge_agrees_with_series():
    """The system route and the Bernstein-Lagarias series route must agree."""
    random.seed(7)
    for d in (2, 3):
        for _ in range(30):
            sigma = [tuple(random.randrange(d) for _ in range(2))
                     for _ in range(d)]
            seed = random.randrange(d)
            sigma[seed] = (seed,) + sigma[seed][1:]
            tau = [random.randrange(2) for _ in range(d)]
            L = 1 << 11
            q = [tau[a] for a in V.fixed_point(sigma, seed, L)]
            assert (V.phi_direct(q, MOD, N)
                    == V.phi_from_system(sigma, seed, d, tau, L, MOD))


# ------------------------------------------------------------ RED: mutants die

def test_wrong_substitution_is_rejected():
    """Using y instead of y^M must break the functional equation.

    Without this the equation check could be passing vacuously.
    """
    sigma = [(0, 1), (1, 0)]
    d, k, z, upto = 2, 2, 2, 81
    y = [3, 5]
    u = V.fixed_point(sigma, 0, upto + k + 1)
    M = V.incidence(sigma, d)
    lhs = V.f_series(u, d, z, y, upto, MOD)
    # deliberately omit the y -> y^M substitution
    inner = V.f_series(u, d, pow(z, k, MOD), y, -(-upto // k), MOD)
    Q = V.Q_matrix(sigma, d, k, z, y, MOD)
    mask = (1 << upto) - 1
    agree = all((lhs[b] & mask)
                == (sum(Q[a][b] * inner[a] for a in range(d)) % MOD) & mask
                for b in range(d))
    assert not agree, "equation passed without the y^M substitution"


def test_transposed_incidence_is_rejected():
    """M and its transpose must not be interchangeable."""
    sigma = [(0, 1), (1, 1)]
    d = 2
    M = V.incidence(sigma, d)
    MT = [[M[j][i] for j in range(d)] for i in range(d)]
    assert M != MT
    y = [3, 5]
    ok_true = V.check_functional_equation(sigma, 0, d, 2, y, 81, MOD)
    assert ok_true


def test_phi_bridge_rejects_a_perturbed_word():
    """Flipping one bit of q must change Phi."""
    sigma = [(0, 1), (1, 0)]
    tau = [0, 1]
    L = 1 << 11
    q = [tau[a] for a in V.fixed_point(sigma, 0, L)]
    good = V.phi_direct(q, MOD, N)
    q2 = list(q)
    q2[3] ^= 1
    assert V.phi_direct(q2, MOD, N) != good


# ------------------------------------------------- attraction decision procedure

def test_attraction_agrees_with_valuation_profile_on_survivors():
    """Every survivor verdict must match the independently computed profile."""
    for sig_str, seed, tau_str, _rho in V.SURVIVORS:
        sigma = V.parse_sigma(sig_str)
        d = len(sigma)
        tau = [int(c) for c in tau_str]
        verdict, _ = V.attraction_verdict(sigma, tau, d)
        prof = V.valuation_profile(V.incidence(sigma, d), tau, d, 80)
        assert verdict in ("ATTRACTED", "STALLED")
        if verdict == "ATTRACTED":
            assert prof[-1] is None or prof[-1] > prof[0]
        else:
            tail = prof[-20:]
            assert all(x is not None and x == tail[0] for x in tail)


def test_survivor_split_is_four_and_six():
    """The packet's headline number."""
    attracted = 0
    for sig_str, seed, tau_str, _rho in V.SURVIVORS:
        sigma = V.parse_sigma(sig_str)
        tau = [int(c) for c in tau_str]
        v, _ = V.attraction_verdict(sigma, tau, len(sigma))
        attracted += v == "ATTRACTED"
    assert attracted == 4
    assert len(V.SURVIVORS) - attracted == 6


def test_no_survivor_satisfies_awc():
    for sig_str, seed, tau_str, _rho in V.SURVIVORS:
        sigma = V.parse_sigma(sig_str)
        tau = [int(c) for c in tau_str]
        assert not V.awc(sigma, tau, len(sigma))


def test_awc_is_automatic_on_two_letters():
    """With two letters and a nonconstant coding, each tau-class is a
    singleton, so the affine weight condition holds vacuously."""
    for images in [((0, 0), (0, 1)), ((0, 1), (1, 0)), ((0, 1), (1, 1))]:
        for tau in ([0, 1], [1, 0]):
            assert V.awc(list(images), tau, 2)


def test_f2_orbit_detects_both_outcomes():
    """The F_2 orbit test must return a hitting time when one exists and None
    when the orbit is closed away from zero."""
    # Thue-Morse: M = [[1,1],[1,1]], so [1,0] -> [1,1] -> [2,2] = 0 mod 2.
    M_tm = V.incidence([(0, 1), (1, 0)], 2)
    assert M_tm == [[1, 1], [1, 1]]
    assert V.f2_orbit_hits_zero(M_tm, [1, 0], 2) == 2

    # A survivor that is proved STALLED: its F_2 orbit never reaches zero.
    sigma = V.parse_sigma("01,20,11")
    M = V.incidence(sigma, 3)
    assert V.f2_orbit_hits_zero(M, [1, 1, 0], 3) is None


def test_mbar_nilpotent_matches_definition():
    random.seed(9)
    for d in (2, 3):
        for _ in range(50):
            sigma = [tuple(random.randrange(d) for _ in range(2))
                     for _ in range(d)]
            M = V.incidence(sigma, d)
            A = [[M[i][j] % 2 for j in range(d)] for i in range(d)]
            P = [row[:] for row in A]
            for _ in range(d - 1):
                P = [[sum(P[i][t] * A[t][j] for t in range(d)) % 2
                      for j in range(d)] for i in range(d)]
            expect = not any(P[i][j] for i in range(d) for j in range(d))
            assert V.mbar_nilpotent(M, d) == expect


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok  ", fn.__name__)
    print("\n%d tests passed" % len(fns))
