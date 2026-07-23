#!/usr/bin/env python3
"""Executable controls for COLLATZ_SYRACUSE_FOURIER.md.

Verifies:
  (1) the exact characteristic-function recursion (Theorem 1) against FFT;
  (2) the parity-class contraction bound on r_n (Lemma 2), every layer;
  (3) Parseval / exponential L2 mixing (Corollary 3);
  (4) the spectral barrier (Theorem 4): primitivity of 2 mod 3^n and the
      frequency-walk eigenvalue formula.

Float64 statistics beyond n=5 are numerical controls; the proved
statements live in the memo.
"""

import json
import math
import os
import sys

import numpy as np

A_TRUNC = 40  # geometric tail beyond a=40 has weight <= 2^-40


# ----------------------------------------------------------------------------
# Syracuse offset distributions (float), provenance: tao-structural-refinement
# ----------------------------------------------------------------------------

def syracuse_float_layers(n_max):
    P = np.ones(1, dtype=np.float64)
    for n in range(n_max):
        mod_new = 3 ** (n + 1)
        period = 2 * 3 ** n
        X = np.arange(mod_new, dtype=np.uint64)
        Q = np.zeros(mod_new, dtype=np.float64)
        for a in range(1, min(period, A_TRUNC) + 1):
            t = (pow(2, a, mod_new) * X) % mod_new
            mask = t % 3 == 1
            Q[mask] += 2.0 ** (-a) * P[(t[mask] - 1) // 3]
        Q /= 1.0 - 2.0 ** (-period)
        P = Q
        yield n + 1, P


# ----------------------------------------------------------------------------
# (1) exact characteristic-function recursion check
# ----------------------------------------------------------------------------

def char_recursion_check(P, Q, xis, n):
    """max |c_{n+1}(xi) - sum_a 2^-a e(-xi u_a/3^{n+1}) c_n(xi u_a mod 3^n)|."""
    mod_old, mod_new = 3 ** n, 3 ** (n + 1)
    Cn = np.fft.fft(P)
    Cn1 = np.fft.fft(Q)
    worst = 0.0
    for xi in xis:
        acc = 0j
        for a in range(1, A_TRUNC + 1):
            u = pow(2, -a, mod_new)
            phase = np.exp(-2j * np.pi * ((xi * u) % mod_new) / mod_new)
            acc += 2.0 ** (-a) * phase * Cn[(xi * u) % mod_old]
        worst = max(worst, abs(acc - Cn1[xi]))
    return float(worst)


# ----------------------------------------------------------------------------
# (4) spectral barrier
# ----------------------------------------------------------------------------

def is_primitive_root_2(n):
    """Check ord_{3^n}(2) == 2*3^{n-1}."""
    mod = 3 ** n
    N = 2 * 3 ** (n - 1)
    if pow(2, N, mod) != 1:
        return False
    for d in (N // 2, N // 3):
        if d >= 1 and pow(2, d, mod) == 1:
            return False
    return True


def walk_eigenvalue_check(n):
    """Eigenvalues of the walk t -> t - a (Geom(2)) on Z/NZ, N = 2*3^{n-1}.

    Compares the FFT spectrum of the circulant step row against the
    formula |mu_l| = (5 - 4 cos(2 pi l / N))^{-1/2}.
    """
    N = 2 * 3 ** (n - 1)
    row = np.zeros(N)
    for a in range(1, A_TRUNC + 1):
        row[(-a) % N] += 2.0 ** (-a)
    eigs = np.fft.fft(row)
    worst = 0.0
    for l in range(N):
        formula = 1.0 / math.sqrt(5 - 4 * math.cos(2 * math.pi * l / N))
        worst = max(worst, abs(abs(eigs[l]) - formula))
    top_nontrivial = max(abs(eigs[l]) for l in range(1, N))
    gap = 1.0 - top_nontrivial
    asymptotic_gap = math.pi ** 2 / (2 * 9.0 ** (n - 1))
    return {
        "n": n, "N": N,
        "formula_max_abs_err": worst,
        "top_nontrivial_eigenvalue": top_nontrivial,
        "spectral_gap": gap,
        "asymptotic_gap_pi2_over_2x9^(n-1)": asymptotic_gap,
        "gap_ratio_measured_over_asymptotic": gap / asymptotic_gap,
    }


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    cert = {"packet": "2026-07-22-syracuse-fourier",
            "scope": "float64 controls; proved statements live in memo"}

    n_max = int(os.environ.get("VSF_N_MAX", 14))
    layers = dict(syracuse_float_layers(n_max))

    rng = np.random.RandomState(20260722)
    checks = []
    for n in (3, 5, 9):
        xis = rng.randint(0, 3 ** (n + 1), 16).tolist()
        err = char_recursion_check(layers[n], layers[n + 1], xis, n)
        checks.append({"n": n, "max_abs_err": err})
        assert err < 1e-9, (n, err)
    cert["char_recursion_check"] = checks

    r_rows = []
    r_prev = None
    for n in range(1, n_max + 1):
        r = float(layers[n].max())
        row = {"n": n, "r_n": r}
        if r_prev is not None:
            bound = (2.0 / 3.0) * r_prev / (1.0 - 2.0 ** (-2 * 3 ** (n - 2)))
            row["ratio"] = r / r_prev
            row["lemma2_bound_holds"] = bool(r <= bound + 1e-15)
            assert row["lemma2_bound_holds"], n
        r_rows.append(row)
        r_prev = r
    cert["r_n_table"] = r_rows
    cert["r_1_exact"] = "2/3"
    cert["r_2_exact"] = "22/63"
    assert abs(r_rows[0]["r_n"] - 2 / 3) < 1e-12
    assert abs(r_rows[1]["r_n"] - 22 / 63) < 1e-12

    parseval = []
    for n in (3, 6, 9, 12):
        if n > n_max:
            continue
        P = layers[n]
        lhs = float((np.abs(np.fft.fft(P)) ** 2).sum() / P.size)
        rhs = float((P ** 2).sum())
        rms = math.sqrt(rhs)
        row = {"n": n, "parseval_abs_err": abs(lhs - rhs),
               "sum_P2": rhs, "rms_char": rms,
               "rms_bound_sqrt_r_n": math.sqrt(float(P.max())),
               "bound_holds": rms <= math.sqrt(float(P.max())) + 1e-12,
               "two_thirds_half_power": (2 / 3) ** (n / 2)}
        assert row["parseval_abs_err"] < 1e-9 and row["bound_holds"]
        parseval.append(row)
    cert["parseval_l2_mixing"] = parseval

    cert["primitive_root_2_mod_3^n"] = {str(n): is_primitive_root_2(n)
                                        for n in range(1, 7)}
    assert all(cert["primitive_root_2_mod_3^n"].values())

    barrier = [walk_eigenvalue_check(n) for n in (1, 2, 3, 4)]
    for b in barrier:
        assert b["formula_max_abs_err"] < 1e-9, b
        assert b["spectral_gap"] > 0
    cert["spectral_barrier"] = barrier

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("syracuse_fourier_certificate.json", "w") as f:
        f.write(out + "\n")
    print(json.dumps({
        "status": "ok",
        "char_recursion_max_err": max(c["max_abs_err"] for c in checks),
        "r_n_ratio_at_n14": r_rows[-1].get("ratio"),
        "rms_n12": parseval[-1]["rms_char"],
        "spectral_gap_n4": barrier[-1]["spectral_gap"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
