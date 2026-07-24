#!/usr/bin/env python3
"""Tests for verify_supercritical_closure.py.

Runs under pytest (`python3 -m pytest <this file> -q`) and standalone
(`python3 <this file>`).  Every assertion is exact integer / Fraction
arithmetic.  The tests attack the three places where this packet could be
wrong: the exact factor language, the two proved bounds it feeds into, and
the integer form of the kill certificate.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
MODPATH = os.path.join(HERE, "verify_supercritical_closure.py")

_spec = importlib.util.spec_from_file_location("vsac", MODPATH)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

# The packet's proved supercritical witness: sigma(0)=11, sigma(1)=10, seed 1
# (Witness 1 of 2026-07-22-automatic-transcript-rigidity, Theorem 3).
GAP_SIGMA = ((1, 1), (1, 0))
GAP_SEED = 1
GAP_CODING = (0, 1)


# ---------------------------------------------------------------------------
# exact language
# ---------------------------------------------------------------------------

def test_exact_factor_set_equals_observed_language():
    """The exact factor set must equal the set of factors actually seen in a
    long prefix -- neither missing a factor nor inventing one."""
    R = 9
    blocks = V.window_blocks(GAP_SIGMA, GAP_SEED, R)
    pref = bytes(V.fixed_point_prefix(GAP_SIGMA, GAP_SEED, 1 << 16))
    for n in (1, 2, 3, 5, 8, 13, 32, 64, 128, 256):
        exact = V.factors_exact(blocks, 2 ** R, n)
        brute = {pref[i:i + n] for i in range(len(pref) - n + 1)}
        assert brute <= exact, "exact set misses an observed factor at n=%d" % n
        assert exact == brute, "exact set invents a factor at n=%d" % n


def test_pairs_exact_is_closed_and_observed():
    """L_2 must be sigma-closed and must match the pairs seen in a prefix."""
    P = V.pairs_exact(GAP_SIGMA, GAP_SEED)
    pref = V.fixed_point_prefix(GAP_SIGMA, GAP_SEED, 1 << 14)
    seen = {(pref[i], pref[i + 1]) for i in range(len(pref) - 1)}
    assert seen == P
    for (a, b) in P:
        assert (GAP_SIGMA[a][-1], GAP_SIGMA[b][0]) in P
        for w in (GAP_SIGMA[a], GAP_SIGMA[b]):
            for i in range(len(w) - 1):
                assert (w[i], w[i + 1]) in P


# ---------------------------------------------------------------------------
# the two proved bounds
# ---------------------------------------------------------------------------

def test_complexity_bound_dominates_observed_ratio():
    """The proved bound C <= max p(m+1)/(m-1) must dominate p(n)/n for every
    n in the exactly computed range -- if it does not, the bound is wrong."""
    R = 10
    kR = 2 ** R
    blocks = V.window_blocks(GAP_SIGMA, GAP_SEED, R)
    bound, _ = V.complexity_bound(blocks, kR, 2, 96)
    for n in (200, 300, 512, 700, 1024):
        p = len(V.factors_exact(blocks, kR, n))
        assert Fraction(p, n) <= bound, (n, p, bound)


def test_complexity_nodes_cover_the_window():
    for k in (2, 3, 4):
        for m0 in (24, 96, 192):
            nodes = V.complexity_nodes(m0, k)
            assert nodes[0] == m0 and nodes[-1] == k * m0
            assert all(nodes[i] < nodes[i + 1] for i in range(len(nodes) - 1))


def test_max_factor_ones_is_subadditive():
    """f(a+b) <= f(a) + f(b): the Fekete input that makes f(ell)/ell a valid
    upper bound for the asymptotic maximal factor density."""
    R = 9
    kR = 2 ** R
    blocks = V.window_blocks(GAP_SIGMA, GAP_SEED, R)
    f = {n: V.max_factor_ones(blocks, kR, GAP_CODING, n)
         for n in (16, 32, 48, 64, 96, 128, 192, 256)}
    for a in (16, 32, 64):
        for b in (16, 32, 64, 128):
            if a + b in f:
                assert f[a + b] <= f[a] + f[b], (a, b)


def test_max_factor_density_exceeds_rho_and_tends_to_it():
    """B_ell = f(ell)/ell must sit above the exact Perron density rho and
    approach it; rho = 2/3 for the gap example."""
    R = 10
    kR = 2 ** R
    blocks = V.window_blocks(GAP_SIGMA, GAP_SEED, R)
    prev = None
    for ell in (64, 128, 256, 512, 1024):
        B = Fraction(V.max_factor_ones(blocks, kR, GAP_CODING, ell), ell)
        assert B >= Fraction(2, 3)
        if prev is not None:
            assert B <= prev
        prev = B
    assert prev < Fraction(7, 10)


# ---------------------------------------------------------------------------
# exact arithmetic of the kill certificates
# ---------------------------------------------------------------------------

def test_cmp_frac_alpha_against_known_witnesses():
    assert V.cmp_frac_alpha(Fraction(63, 100)) == -1      # 3^63 < 2^100
    assert V.cmp_frac_alpha(Fraction(631, 1000)) == 1     # 2^1000 < 3^631
    assert V.cmp_frac_alpha(Fraction(2, 3)) == 1          # 3^2 > 2^3
    assert V.cmp_frac_alpha(Fraction(1, 2)) == -1         # 3 < 4
    lo, hi = V.alpha_bracket()
    assert lo < hi
    assert V.cmp_frac_alpha(lo) == -1 and V.cmp_frac_alpha(hi) == 1


def test_kappa_identity_alpha_over_one_minus_alpha():
    """The endpoint identity that makes the density inequality contain the
    landmark memo's Corollary 4: alpha/(1-alpha) = kappa = 1.7095112913..."""
    klo, khi = V.kappa_bounds()
    assert klo < Fraction(17095112913, 10 ** 10) < khi


def test_kill_certificates_agree_with_rational_comparison():
    """The integer witnesses 3^x < 2^y must agree with the inequality they
    stand for, checked independently through the certified alpha bracket."""
    lo, hi = V.alpha_bracket()
    for c in (Fraction(3, 2), Fraction(109, 64), Fraction(2), Fraction(4),
              Fraction(217, 64), Fraction(6)):
        fired, _ = V.kill_kappa(c)
        # c < kappa  <=>  c/(1+c) < alpha
        t = c / (1 + c)
        if t < lo:
            assert fired
        elif t > hi:
            assert not fired
        for beta in (Fraction(2, 3), Fraction(3, 4), Fraction(5, 6),
                     Fraction(6, 7)):
            fired, _ = V.kill_density(c, beta)
            s = beta * c / (1 + c)
            if s < lo:
                assert fired
            elif s > hi:
                assert not fired


def test_kappa_route_is_the_beta_equals_one_instance():
    """Corollary 4 is literally Corollary 7 at beta = 1 (every length-l
    factor trivially has at most l ones).  The two code paths must agree."""
    for c in (Fraction(1, 2), Fraction(3, 2), Fraction(27, 16),
              Fraction(109, 64), Fraction(2), Fraction(95, 16), Fraction(9)):
        assert V.kill_kappa(c)[0] == V.kill_density(c, Fraction(1))[0]


def test_fekete_bound_is_valid_for_every_length():
    """f(m) <= (f(ell)/ell)*m + f(ell) -- the step that makes a single ell
    an admissible beta for Corollary 7."""
    R = 9
    kR = 2 ** R
    blocks = V.window_blocks(GAP_SIGMA, GAP_SEED, R)
    ell = 128
    f_ell = V.max_factor_ones(blocks, kR, GAP_CODING, ell)
    for m in (1, 7, 64, 127, 128, 129, 200, 256, 400, 512):
        f_m = V.max_factor_ones(blocks, kR, GAP_CODING, m)
        assert ell * f_m <= f_ell * m + f_ell * ell, (m, f_m, f_ell)


def test_density_kill_is_monotone_in_the_bound():
    """A weaker (larger) complexity bound must never kill more."""
    beta = Fraction(2, 3)
    prev = True
    for c in (Fraction(1), Fraction(2), Fraction(4), Fraction(8),
              Fraction(16), Fraction(18), Fraction(32)):
        fired, _ = V.kill_density(c, beta)
        assert not (fired and not prev)
        prev = fired
    # beta = 2/3 needs C >= alpha/(2/3 - alpha) = 17.65..., so C <= 17 kills
    # and C = 32 does not.
    assert V.kill_density(Fraction(17), Fraction(2, 3))[0]
    assert not V.kill_density(Fraction(32), Fraction(2, 3))[0]


# ---------------------------------------------------------------------------
# Phi engine and the collision principle
# ---------------------------------------------------------------------------

def test_phi_engines_agree_with_each_other_and_with_orbits():
    for n in range(1, 400):
        _, q = V.terras_orbit(n, 64)
        assert V.phi_mod_lift(q, 64) == V.phi_mod_series(q, 64) == n


def test_collision_principle_on_true_orbits():
    out = V.check_collision_principle(300, 10)
    assert out["equal_block_pairs_checked"] > 0
    assert out["small_state_collisions_forced_equal"] > 0


def test_real_transcripts_are_eventually_periodic():
    """Sanity that the theorem's hypothesis excludes every actual orbit: a
    positive integer that reaches 1 has an eventually periodic transcript,
    so no true Collatz transcript is in the class this packet kills."""
    for n in range(1, 500):
        x = n
        for _ in range(2000):
            x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
            if x == 1:
                break
        assert x == 1, n


# ---------------------------------------------------------------------------
# end-to-end
# ---------------------------------------------------------------------------

def test_gap_example_is_killed():
    """Witness 1 of the rigidity packet -- the memo's named example -- must
    be killed, and by the kappa route (its complexity constant is 3/2)."""
    rec = {"length": 2, "rho": "2/3", "sigma": "11,10", "seed": GAP_SEED,
           "coding": None, "_sigma": GAP_SIGMA, "_seed": GAP_SEED,
           "_coding": GAP_CODING}
    out = V.analyse(rec)
    assert out["killed_by_kappa_corollary4"], out
    assert out["killed_by_density_selfcontained"], out
    assert Fraction(out["C_upper_bound_used"]) < Fraction(7, 4)


def test_verifier_is_deterministic_and_self_consistent():
    tmp = tempfile.mkdtemp()
    outs = []
    for i in range(2):
        dest = os.path.join(tmp, "cert%d.json" % i)
        env = dict(os.environ, VSAC_REDUCED="1", VSAC_OUT=dest)
        subprocess.run([sys.executable, MODPATH], cwd=HERE, env=env,
                       check=True, capture_output=True)
        with open(dest, "rb") as fh:
            outs.append(fh.read())
    shutil.rmtree(tmp, ignore_errors=True)
    assert outs[0] == outs[1], "certificate is not deterministic"
    cert = json.loads(outs[0])
    assert cert["result"]["not_killed"] + \
        cert["result"]["killed_with_unique_ergodicity_total"] == \
        cert["result"]["supercritical_primitive_words"]
    for rec in cert["records"]:
        # every listed word is certified supercritical by an exact witness
        assert V.cmp_frac_alpha(Fraction(rec["rho"])) == 1
        # and its self-contained density bound sits above its exact density
        assert Fraction(rec["B_ell"]) >= Fraction(rec["rho"])


def _main():
    fns = [(k, v) for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    bad = 0
    for name, fn in fns:
        try:
            fn()
            print("PASS %s" % name)
        except AssertionError as exc:
            bad += 1
            print("FAIL %s: %s" % (name, exc))
    print("%d/%d passed" % (len(fns) - bad, len(fns)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(_main())
