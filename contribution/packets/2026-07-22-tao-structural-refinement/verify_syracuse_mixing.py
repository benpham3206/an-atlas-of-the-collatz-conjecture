#!/usr/bin/env python3
"""Executable controls for COLLATZ_TAO_STRUCTURAL_REFINEMENT.md.

Computes the exact distributions of Tao's Syracuse random variables
Syrac(Z/3^n Z) via his Lemma 1.12 recursion, cross-checks against the
paper's own tabulated vectors (n = 1, 2), then measures — in float64,
openly numerical — the decay of

  max_{3 ∤ ξ} |E e^{-2πi ξ Syrac(Z/3^n Z)/3^n}|   and   Osc_{m,n}

up to n = 14. Tao's Proposition 1.17 proves superpolynomial decay
(≪_A n^{−A}); the random-map heuristic (his Remark 1.15) predicts
exp(−c m). These measurements are a hypothesis generator, not a proof.
"""

from fractions import Fraction
import json
import os
import sys

import numpy as np

# Paper's tabulated vectors (Tao, §1, after Lemma 1.12)
PAPER_P1 = [Fraction(0), Fraction(1, 3), Fraction(2, 3)]
PAPER_P2 = [Fraction(0), Fraction(8, 63), Fraction(16, 63),
            Fraction(0), Fraction(11, 63), Fraction(4, 63),
            Fraction(0), Fraction(2, 63), Fraction(22, 63)]


# ----------------------------------------------------------------------------
# Exact recursion (Fraction), small n only
# ----------------------------------------------------------------------------

def syracuse_exact_layer(P, n):
    """One step of Lemma 1.12: P on Z/3^n -> Q on Z/3^{n+1}, exact."""
    mod_new = 3 ** (n + 1)
    mod_old = 3 ** n
    period = 2 * mod_old
    Q = [Fraction(0)] * mod_new
    pow2 = [pow(2, a, mod_new) for a in range(1, period + 1)]
    for x in range(mod_new):
        acc = Fraction(0)
        for a in range(1, period + 1):
            t = (pow2[a - 1] * x) % mod_new
            if t % 3 == 1:
                acc += Fraction(1, 1 << a) * P[(t - 1) // 3]
        Q[x] = acc / (1 - Fraction(1, 1 << period))
    return Q


def syracuse_exact(n):
    P = [Fraction(1)]
    for k in range(n):
        P = syracuse_exact_layer(P, k)
    return P


# ----------------------------------------------------------------------------
# Float recursion (numerical), up to n = 14
# ----------------------------------------------------------------------------

A_TRUNC = 40  # tail beyond a=40 has total weight <= 2^-40 per cell per layer


def syracuse_float_layers(n_max):
    """Yield (n, P) float64 distributions for n = 1..n_max."""
    P = np.ones(1, dtype=np.float64)
    for n in range(n_max):
        mod_old = 3 ** n
        mod_new = 3 ** (n + 1)
        period = 2 * mod_old
        a_range = range(1, min(period, A_TRUNC) + 1)
        X = np.arange(mod_new, dtype=np.uint64)
        Q = np.zeros(mod_new, dtype=np.float64)
        for a in a_range:
            p2 = pow(2, a, mod_new)
            t = (p2 * X) % mod_new
            mask = t % 3 == 1
            idx = (t[mask] - 1) // 3
            Q[mask] += 2.0 ** (-a) * P[idx]
        Q /= 1.0 - 2.0 ** (-period)
        P = Q
        yield n + 1, P


def char_function_max(P):
    """max |sum_x P(x) e^{-2πi ξ x / 3^n}| over ξ not divisible by 3."""
    n = round(np.log(P.size) / np.log(3))
    C = np.fft.fft(P)
    mag = np.abs(C)
    mag[np.arange(P.size) % 3 == 0] = 0.0
    xi = int(np.argmax(mag))
    return float(mag[xi]), xi


def oscillation(P, m):
    """Osc_{m,n} of the distribution tuple (Tao's (1.27)).

    Coset of Y is {Y' == Y mod 3^m}; the coset average divides by the
    coset size 3^{n-m}.
    """
    n = round(np.log(P.size) / np.log(3))
    B = 3 ** m
    G = P.reshape(-1, B)
    return float(np.abs(G - G.mean(axis=0, keepdims=True)).sum())


def decay_table(n_max):
    rows = []
    for n, P in syracuse_float_layers(n_max):
        total = float(P.sum())
        row = {
            "n": n,
            "mass_sum_error": abs(total - 1.0),
            "max_char_nondiv3": None,
            "argmax_xi": None,
            "osc": {},
            "zero_mass_on_multiples_of_3": bool(
                np.all(P[np.arange(P.size) % 3 == 0] == 0.0)),
        }
        mc, xi = char_function_max(P)
        row["max_char_nondiv3"] = mc
        row["argmax_xi"] = xi
        for m in (2, 4, 6, 8, 10):
            if m < n:
                row["osc"][f"m={m}"] = oscillation(P, m)
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    cert = {"packet": "2026-07-22-tao-structural-refinement",
            "scope": "exact distributions n<=5; float64 statistics n<=14; "
                     "decay measurements are hypothesis generators"}

    exact_n = int(os.environ.get("VSM_EXACT_N", 5))
    exact = {}
    P = [Fraction(1)]
    for k in range(exact_n):
        P = syracuse_exact_layer(P, k)
        exact[str(k + 1)] = P
    cert["exact_matches_paper_n1"] = exact["1"] == PAPER_P1
    cert["exact_matches_paper_n2"] = exact["2"] == PAPER_P2
    assert cert["exact_matches_paper_n1"] and cert["exact_matches_paper_n2"]
    cert["exact_distribution_top"] = {"n": exact_n,
                                      "values": [str(p) for p in exact[str(exact_n)]]}

    n_max = int(os.environ.get("VSM_N_MAX", 14))
    rows = decay_table(n_max)
    cert["decay_table"] = rows

    # float vs exact cross-check at small n
    cross = []
    float_small = {}
    for n, Pf in syracuse_float_layers(exact_n):
        float_small[n] = Pf
    for n in range(1, exact_n + 1):
        diff = float(np.abs(float_small[n]
                            - np.array([float(p) for p in exact[str(n)]])).max())
        cross.append({"n": n, "max_abs_diff": diff})
        assert diff < 1e-9, (n, diff)
    cert["float_vs_exact"] = cross

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("syracuse_mixing_certificate.json", "w") as f:
        f.write(out + "\n")
    table = [{"n": r["n"], "max_char": round(r["max_char_nondiv3"], 6)}
             for r in rows]
    import math
    fit = [{"n": r["n"],
            "neg_ln_over_sqrt_n": round(
                -math.log(r["max_char_nondiv3"]) / math.sqrt(r["n"]), 4)}
           for r in rows]
    print(json.dumps({"status": "ok",
                      "exact_matches_paper": True,
                      "decay": table,
                      "stretched_exp_fit": fit}, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
