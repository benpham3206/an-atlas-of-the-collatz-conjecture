#!/usr/bin/env python3
"""Verifier for the Mahler-tower packet (2026-07-25).

Every acceptance decision on this path is exact integer arithmetic in Z/2^N or
in F_2.  No float appears anywhere in this file.

What is verified, in order:

  A. The functional system.  For a k-uniform morphism sigma on d letters with
     incidence matrix M, the vector of generating functions

         f_b(z, y) = sum_{n : u_n = b}  z^n * prod_a y_a^{c_a(n)}
         c_a(n)    = #{i < n : u_i = a}

     satisfies      f_b(z, y) = sum_a Q[a][b](z, y) * f_a(z^k, y^M)

     with (y^M)_b = prod_a y_a^{M[a][b]} and Q[a][b] an explicit polynomial.
     Checked at z = 2 against random 2-adic unit vectors y, exactly.

  B. The bridge to Phi.  Phi(q) = -(1/3) * sum_{b : tau(b)=1} f_b(2, y*) with
     y*_a = 3^{-tau(a)}.  Checked against the defining Bernstein-Lagarias
     series Phi(q) = - sum_j 2^{d_j} / 3^{j+1}, which is an independent
     re-implementation: it never forms M, Q, or the letter-count vectors.

  C. The attraction verdict.  Iterating the substitution sends the parameter to
     y_e(b) = 3^{-(tau M^e)_b}.  These are 2-adic units for every e, so y_e -> 1
     iff tau M^e -> 0 in Z_2^d.  Two independent exact decision procedures:

       C1  PROOF-NILPOTENT.  If Mbar^d = 0 over F_2 then M^d = 2B, hence
           M^{dj} = 2^j B_j -> 0, so tau M^e -> 0 for EVERY tau.  Sufficient.
       C2  PROOF-CYCLE.  tau M^e mod 2 lives in the finite set F_2^d, so the
           sequence is eventually periodic with preperiod + period <= 2^d.
           If it is nonzero for every e <= 2^d + d then it is nonzero forever,
           so v_2(tau M^e) = 0 for all e and y_e does NOT converge.  Decisive.

     C1 and C2 are exhaustive on the survivors: each of the ten is settled by
     one of them, so no verdict in this packet is an extrapolation.

  D. The class census over all 2-uniform morphisms on d <= 4 letters.

Usage:  python3 verify_mahler_tower.py [--precision N] [--dmax 4]
"""

import argparse
import json
import os
import platform
import random
import sys
from itertools import product

# --------------------------------------------------------------------------
# the ten remaining supercritical survivors
# source: 2026-07-24-supercritical-automatic-closure, section 8 table
# fields: sigma images (letters 0,1,2), prolongable seed, coding tau, rho
# --------------------------------------------------------------------------
SURVIVORS = [
    ("01,02,10", 0, "110", "5/6"),
    ("01,02,20", 0, "110", "3/4"),
    ("01,02,20", 0, "101", "3/4"),
    ("01,02,20", 2, "110", "3/4"),
    ("01,02,20", 2, "101", "3/4"),
    ("01,12,00", 0, "110", "4/5"),
    ("01,12,00", 1, "110", "4/5"),
    ("01,20,00", 0, "110", "6/7"),
    ("01,20,10", 0, "110", "5/6"),
    ("01,20,11", 0, "110", "4/5"),
]


# ------------------------------------------------------------------ morphisms

def parse_sigma(s):
    return [tuple(int(c) for c in part) for part in s.split(",")]


def fixed_point(sigma, seed, length):
    """Prefix of the fixed point of sigma starting at `seed`."""
    if sigma[seed][0] != seed:
        raise ValueError("seed is not prolongable")
    u = [seed]
    while len(u) < length:
        u = [c for a in u for c in sigma[a]]
    return u[:length]


def incidence(sigma, d):
    """M[a][b] = number of a's in sigma(b)."""
    return [[sigma[b].count(a) for b in range(d)] for a in range(d)]


def vecmat(v, M, d):
    return [sum(v[t] * M[t][j] for t in range(d)) for j in range(d)]


# ------------------------------------------------------- A: the functional system

def counts(u, d):
    """c[n][a] = #{i < n : u_i = a}."""
    cur = [0] * d
    out = [tuple(cur)]
    for a in u:
        cur[a] += 1
        out.append(tuple(cur))
    return out


def monomial(y, exps, mod):
    v = 1
    for ya, e in zip(y, exps):
        if e:
            v = v * pow(ya, e, mod) % mod
    return v


def f_series(u, d, z, y, upto, mod):
    """f_b(z, y) truncated to n < upto, exactly, for every b."""
    c = counts(u, d)
    out = [0] * d
    for n in range(upto):
        out[u[n]] = (out[u[n]] + pow(z, n, mod) * monomial(y, c[n], mod)) % mod
    return out


def y_substituted(y, M, d, mod):
    """(y^M)_b = prod_a y_a^{M[a][b]}."""
    return [monomial(y, [M[a][b] for a in range(d)], mod) for b in range(d)]


def Q_matrix(sigma, d, k, z, y, mod):
    """Q[a][b](z, y) = sum_{r<k, sigma(a)[r]=b} z^r prod_c y_c^{gamma_c(a,r)}."""
    out = [[0] * d for _ in range(d)]
    for a in range(d):
        gamma = [0] * d
        for r in range(k):
            b = sigma[a][r]
            out[a][b] = (out[a][b] + pow(z, r, mod) * monomial(y, gamma, mod)) % mod
            gamma[b] += 1
    return out


def check_functional_equation(sigma, seed, d, k, y, upto, mod):
    """f_b(2,y) == sum_a Q[a][b] f_a(2^k, y^M), truncated honestly.

    Truncating the left side at n < upto constrains it modulo 2^upto only, and
    n = k*m + r means the right side needs m < ceil(upto/k).  The comparison is
    therefore made modulo 2^min(upto, N), which is exactly what the truncation
    licenses.
    """
    z = 2
    u = fixed_point(sigma, seed, upto + k + 1)
    M = incidence(sigma, d)
    lhs = f_series(u, d, z, y, upto, mod)
    inner = f_series(u, d, pow(z, k, mod), y_substituted(y, M, d, mod),
                     -(-upto // k), mod)
    Q = Q_matrix(sigma, d, k, z, y, mod)
    mask = (1 << min(upto, mod.bit_length() - 1)) - 1
    for b in range(d):
        rhs = sum(Q[a][b] * inner[a] for a in range(d)) % mod
        if (lhs[b] & mask) != (rhs & mask):
            return False
    return True


# -------------------------------------------------------------- B: bridge to Phi

def phi_direct(q, mod, N):
    """Phi(q) = -sum_j 2^{d_j}/3^{j+1} mod 2^N.  Independent of the system."""
    inv3 = pow(3, -1, mod)
    acc, j = 0, 0
    for n, bit in enumerate(q):
        if bit:
            if n < N:
                acc = (acc + (1 << n) * pow(inv3, j + 1, mod)) % mod
            j += 1
    return (-acc) % mod


def phi_from_system(sigma, seed, d, tau, upto, mod):
    """Phi(q) via f_b(2, y*), y*_a = 3^{-tau(a)}."""
    inv3 = pow(3, -1, mod)
    u = fixed_point(sigma, seed, upto)
    y = [inv3 if tau[a] else 1 for a in range(d)]
    f = f_series(u, d, 2, y, upto, mod)
    return (-inv3 * sum(f[b] for b in range(d) if tau[b])) % mod


# ------------------------------------------------------------ C: attraction

def mbar_nilpotent(M, d):
    """Is M nilpotent over F_2?  Exact; decides C1."""
    A = [[M[i][j] % 2 for j in range(d)] for i in range(d)]
    P = [row[:] for row in A]
    for _ in range(d - 1):
        P = [[sum(P[i][t] * A[t][j] for t in range(d)) % 2 for j in range(d)]
             for i in range(d)]
    return not any(P[i][j] for i in range(d) for j in range(d))


def f2_orbit_hits_zero(M, v, d):
    """Least e >= 1 with v M^e = 0 mod 2, or None if no such e exists.

    v M^e mod 2 ranges over F_2^d, of size 2^d, so the sequence is eventually
    periodic with preperiod + period at most 2^d.  Testing e = 1 .. 2^d + d
    therefore settles all e: a zero not seen in that window never occurs.
    """
    w = [x % 2 for x in v]
    for e in range(1, 2 ** d + d + 1):
        w = [x % 2 for x in vecmat(w, M, d)]
        if not any(w):
            return e
    return None


def v2(n):
    return None if n == 0 else (n & -n).bit_length() - 1


def valuation_profile(M, tau, d, steps):
    """min_b v_2((tau M^e)_b) for e = 1..steps.  Exact; reported as evidence."""
    v, prof = list(tau), []
    for _ in range(steps):
        v = vecmat(v, M, d)
        vals = [v2(x) for x in v if x != 0]
        prof.append(None if not vals else min(vals))
    return prof


def attraction_verdict(sigma, tau, d, max_rounds=64):
    """Decide whether tau M^e -> 0 in Z_2^d.  Every answer returned is a proof.

    C1  Mbar^d = 0 over F_2  =>  M^d = 2B  =>  M^{dj} = 2^j B_j -> 0, so
        tau M^e -> 0 for every tau.  Sufficient, not necessary.

    C2  Descent.  Let v = tau.
          * if the F_2 orbit of v never reaches 0, then v_2(v M^e) = 0 for all
            e, so v M^e does NOT tend to 0            -> STALLED, proved;
          * if v M^{e0} = 0 mod 2, write v M^{e0} = 2 v'.  Then v M^e -> 0 iff
            v' M^e -> 0, so recurse on v'             -> exact reduction;
          * if v M^{e0} = 0 exactly, the tail is zero -> ATTRACTED, proved.

    C3  Recurrence.  The descent state evolves deterministically, so if a state
        repeats, the descent provably never halts.  Surviving round R proves
        v_2(v M^e) >= R eventually, so a repeat proves v_2 -> infinity.
                                                      -> ATTRACTED, proved.

    Each round is an equivalence, so a terminating run is a proof either way.
    A run that exhausts max_rounds returns UNDECIDED rather than a guess: by
    the dichotomy such a word is either attracted or pinned at valuation
    >= max_rounds, and this procedure has not separated the two.  UNDECIDED is
    reported, never counted as either verdict.
    """
    M = incidence(sigma, d)
    if mbar_nilpotent(M, d):
        return "ATTRACTED", "C1 proof-nilpotent (Mbar^d = 0 over F_2)"
    v = list(tau)
    seen = {tuple(v)}
    for rnd in range(max_rounds):
        e0 = f2_orbit_hits_zero(M, v, d)
        if e0 is None:
            return "STALLED", ("C2 descent, round %d: F_2 orbit closed away "
                               "from 0, so v_2 is pinned" % rnd)
        for _ in range(e0):
            v = vecmat(v, M, d)
        if not any(v):
            return "ATTRACTED", "C2 descent, round %d: orbit is exactly 0" % rnd
        v = [x // 2 for x in v]
        key = tuple(v)
        if key in seen:
            return "ATTRACTED", ("C3 recurrence at round %d: descent state "
                                 "repeats, so it never halts" % rnd)
        seen.add(key)
    return "UNDECIDED", "C2 descent did not terminate in %d rounds" % max_rounds


def awc(sigma, tau, d):
    """Affine weight condition: does |tau sigma(a)|_1 depend only on tau(a)?

    This is exactly when the (d+1)-variable system collapses to 2 variables.
    """
    w = [sum(tau[c] for c in sigma[a]) for a in range(d)]
    by = {}
    for a in range(d):
        by.setdefault(tau[a], set()).add(w[a])
    return all(len(s) == 1 for s in by.values())


# ------------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--precision", type=int, default=160)
    ap.add_argument("--dmax", type=int, default=4)
    ap.add_argument("--profile-steps", type=int, default=80)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    N = args.precision
    mod = 1 << N
    cert = {
        "packet": "2026-07-25-mahler-tower",
        "scope": ("exact integer arithmetic in Z/2^N and F_2 on every "
                  "certificate path; no proved statement depends on a float"),
        "precision_bits": N,
        "knobs": {
            "precision": args.precision,
            "dmax": args.dmax,
            "profile_steps": args.profile_steps,
            "descent_max_rounds": 64,
        },
        "env": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }

    # ---- negative controls: the screens must be able to FAIL.
    # A verifier that can only pass is not evidence.  These run first, so a
    # vacuous check is caught before any claim is printed.
    controls = {}

    #  (i) the functional equation must break without the y -> y^M substitution
    sigma_c, d_c, k_c, upto_c = [(0, 1), (1, 0)], 2, 2, 81
    y_c = [3, 5]
    u_c = fixed_point(sigma_c, 0, upto_c + k_c + 1)
    lhs_c = f_series(u_c, d_c, 2, y_c, upto_c, mod)
    inner_c = f_series(u_c, d_c, pow(2, k_c, mod), y_c, -(-upto_c // k_c), mod)
    Q_c = Q_matrix(sigma_c, d_c, k_c, 2, y_c, mod)
    mask_c = (1 << upto_c) - 1
    controls["equation_fails_without_y_substitution"] = not all(
        (lhs_c[b] & mask_c)
        == (sum(Q_c[a][b] * inner_c[a] for a in range(d_c)) % mod) & mask_c
        for b in range(d_c))

    #  (ii) Phi must change when one bit of q is flipped
    q_c = [a for a in fixed_point([(0, 1), (1, 0)], 0, 1 << 11)]
    good = phi_direct(q_c, mod, N)
    q_flip = list(q_c)
    q_flip[3] ^= 1
    controls["phi_changes_on_a_flipped_bit"] = phi_direct(q_flip, mod, N) != good

    #  (iii) a word known to be ATTRACTED must not be reported STALLED
    v_ctl, _ = attraction_verdict(parse_sigma("01,02,20"), [1, 1, 0], 3)
    controls["known_attracted_word_is_not_stalled"] = v_ctl == "ATTRACTED"

    print("negative controls:", controls)
    cert["negative_controls"] = controls
    if not all(controls.values()):
        raise SystemExit("negative control did not fire: the screens are vacuous")

    # ---- A: functional equation over random morphisms and random unit points
    print("=" * 74)
    print("A. functional equation  f = Q . (f o subst)   [exact, mod 2^%d]" % N)
    print("=" * 74)
    random.seed(11)
    trials = fails = 0
    for d in (2, 3, 4):
        for k in (2, 3):
            for _ in range(40):
                sigma = [tuple(random.randrange(d) for _ in range(k))
                         for _ in range(d)]
                seed = random.randrange(d)
                sigma[seed] = (seed,) + sigma[seed][1:]
                y = [random.randrange(1, mod, 2) for _ in range(d)]
                trials += 1
                if not check_functional_equation(sigma, seed, d, k, y, 81, mod):
                    fails += 1
                    print("  FAIL", d, k, sigma, seed)
    print("  %d/%d random (morphism, unit point) pairs satisfy it exactly"
          % (trials - fails, trials))
    cert["functional_equation"] = {"trials": trials, "failures": fails}
    assert fails == 0

    # ---- B: Phi from the system vs Phi from the defining series
    print()
    print("=" * 74)
    print("B. Phi via the system  vs  Phi via the Bernstein-Lagarias series")
    print("=" * 74)
    random.seed(23)
    trials = fails = 0
    for d in (2, 3, 4):
        for k in (2, 3):
            for _ in range(40):
                sigma = [tuple(random.randrange(d) for _ in range(k))
                         for _ in range(d)]
                seed = random.randrange(d)
                sigma[seed] = (seed,) + sigma[seed][1:]
                tau = [random.randrange(2) for _ in range(d)]
                L = 1 << 12
                q = [tau[a] for a in fixed_point(sigma, seed, L)]
                trials += 1
                if phi_direct(q, mod, N) != phi_from_system(sigma, seed, d, tau,
                                                            L, mod):
                    fails += 1
                    print("  FAIL", d, k, sigma, seed, tau)
    print("  %d/%d agree mod 2^%d" % (trials - fails, trials, N))
    cert["phi_bridge"] = {"trials": trials, "failures": fails}
    assert fails == 0

    # closed forms, as a floor under the whole computation
    closed = {
        "all_ones_is_minus_one": phi_direct([1] * (N + 40), mod, N) == (-1) % mod,
        "all_zeros_is_zero": phi_direct([0] * (N + 40), mod, N) == 0,
    }
    print("  closed forms:", closed)
    cert["closed_forms"] = closed
    assert all(closed.values())

    # ---- C: the ten survivors
    print()
    print("=" * 74)
    print("C. attraction verdict for the ten remaining supercritical survivors")
    print("=" * 74)
    print("%-10s %4s %5s %5s  %-9s %-4s %s"
          % ("sigma", "seed", "tau", "rho", "verdict", "AWC", "decided by"))
    print("-" * 74)
    records, n_attr, n_awc = [], 0, 0
    for sig_str, seed, tau_str, rho in SURVIVORS:
        sigma = parse_sigma(sig_str)
        d = len(sigma)
        tau = [int(c) for c in tau_str]
        verdict, route = attraction_verdict(sigma, tau, d)
        a = awc(sigma, tau, d)
        prof = valuation_profile(incidence(sigma, d), tau, d, args.profile_steps)
        n_attr += verdict == "ATTRACTED"
        n_awc += a
        # independent cross-check: the proof route must agree with the exact
        # valuation profile, which is computed without reference to C1 or C2.
        tail = prof[-max(4, len(prof) // 3):]
        if verdict == "ATTRACTED":
            assert prof[-1] is None or prof[-1] > prof[0], (sig_str, seed, tau_str)
        elif verdict == "STALLED":
            assert all(x is not None and x == tail[0] for x in tail), \
                (sig_str, seed, tau_str)
        else:
            raise AssertionError("undecided survivor: " + sig_str)
        records.append({
            "sigma": sig_str, "seed": seed, "coding": tau_str, "rho": rho,
            "verdict": verdict, "decided_by": route,
            "awc_collapse_to_two_variables": a,
            "v2_profile_first_16": prof[:16],
        })
        print("%-10s %4d %5s %5s  %-9s %-4s %s"
              % (sig_str, seed, tau_str, rho, verdict, a, route))
    print("-" * 74)
    print("  ATTRACTED %d/10    STALLED %d/10    AWC %d/10"
          % (n_attr, 10 - n_attr, n_awc))
    cert["survivors"] = {
        "records": records,
        "attracted": n_attr,
        "stalled": 10 - n_attr,
        "awc": n_awc,
    }

    # ---- D: class census
    print()
    print("=" * 74)
    print("D. census over all 2-uniform morphisms, d <= %d" % args.dmax)
    print("=" * 74)
    print("%2s %8s %11s %9s %10s %11s %8s"
          % ("d", "words", "attracted", "stalled", "undecided", "Mbar nilp", "AWC"))
    print("-" * 74)
    census = []
    for d in range(2, args.dmax + 1):
        seen = set()
        tot = attr = und = nilp = awc_n = 0
        for images in product(product(range(d), repeat=2), repeat=d):
            sigma = list(images)
            if not any(sigma[s][0] == s for s in range(d)):
                continue
            nil = mbar_nilpotent(incidence(sigma, d), d)
            for mask in range(1, 2 ** d - 1):
                tau = [(mask >> a) & 1 for a in range(d)]
                key = (tuple(sigma), tuple(tau))
                if key in seen:
                    continue
                seen.add(key)
                tot += 1
                v, _ = attraction_verdict(sigma, tau, d)
                attr += v == "ATTRACTED"
                und += v == "UNDECIDED"
                nilp += nil
                awc_n += awc(sigma, tau, d)
        row = {"d": d, "words": tot, "attracted": attr,
               "stalled": tot - attr - und, "undecided": und,
               "mbar_nilpotent": nilp, "awc": awc_n}
        census.append(row)
        print("%2d %8d %11d %9d %10d %11d %8d"
              % (d, tot, attr, tot - attr - und, und, nilp, awc_n))
    cert["census"] = census

    cert["conclusion"] = (
        "For every letter-coding of a fixed point of a k-uniform morphism, "
        "Phi(q) is the value at (z,y)=(2,3^{-tau}) of an explicit d-dimensional "
        "functional system with substitution (z,y) -> (z^k, y^M). The mixed "
        "bases 2 and 3 do not obstruct the equation. They obstruct the "
        "evaluation point: the y-coordinates are 2-adic units, so the point "
        "lies on the boundary excluded by every form of Mahler's method, and "
        "the induced one-variable tower converges only when tau M^e -> 0. "
        "Six of the ten remaining supercritical survivors fail that condition."
    )

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "mahler_tower_certificate.json")
    with open(out, "w") as fh:
        json.dump(cert, fh, indent=1, sort_keys=True)
    print()
    print("certificate written:", out)


if __name__ == "__main__":
    main()
