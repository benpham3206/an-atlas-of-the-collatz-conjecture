#!/usr/bin/env python3
"""Executable controls for COLLATZ_SCALAR_PHASE_SECOND_MOMENT.md.

Verifies:
  (S1) the exact second-moment recursion against FFT;
  (S2) the conditional-contraction dichotomy on sampled frequencies;
  (S3) the bad-set escape criterion on ALL units, layers n <= 11;
  (4)  the measured bad-set structure: tiny size, conjugate symmetry,
       power-of-2 resonance chain, near-peak flatness, escape weights;
  (5)  the peak decomposition: dilution x phase spread = M_n/M_{n-1}.

Float64 statistics are numerical controls; the proved statements live in
the memo. Env knob VSP_N_MAX (default 14) shrinks the run for tests.
"""

import json
import math
import os
import sys

import numpy as np

A_TRUNC = 40  # geometric tail beyond a=40 has weight <= 2^-40


# ----------------------------------------------------------------------------
# Syracuse offset distributions (float), provenance: syracuse-fourier packet
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


def unit_residues(mod):
    r = np.arange(mod, dtype=np.uint64)
    return r[r % 3 != 0]


# ----------------------------------------------------------------------------
# (S1) exact second-moment identity
# ----------------------------------------------------------------------------

def s1_second_moment_check(Cn, Cn1, xis, n):
    """max ||c_{n+1}(xi)|^2 - (diagonal + cross-term sum from layer n)|."""
    mod_old, mod_new = 3 ** n, 3 ** (n + 1)
    us = [pow(2, -a, mod_new) for a in range(1, A_TRUNC + 1)]
    worst = 0.0
    for xi in xis:
        xi %= mod_new
        vals = [Cn[(xi * u) % mod_old] for u in us]
        rhs = sum(4.0 ** (-a) * abs(vals[a - 1]) ** 2
                  for a in range(1, A_TRUNC + 1))
        cross = 0j
        for a in range(1, A_TRUNC + 1):
            for b in range(a + 1, A_TRUNC + 1):
                frac = ((xi * (us[b - 1] - us[a - 1])) % mod_new) / mod_new
                cross += (2.0 ** (-a - b)
                          * np.exp(2j * np.pi * frac)
                          * vals[a - 1] * np.conj(vals[b - 1]))
        rhs += 2.0 * cross.real
        lhs = abs(Cn1[xi]) ** 2
        worst = max(worst, abs(lhs - rhs))
    return float(worst)


# ----------------------------------------------------------------------------
# (S2) conditional contraction: relative phase of the dominant (a=1,2) pair
# ----------------------------------------------------------------------------

def s2_relative_phase(Cn, xi, n):
    """Return (eta, phi) with phi = arg(A conj(B)), eta = 1 - cos(phi)."""
    mod_old, mod_new = 3 ** n, 3 ** (n + 1)
    xi %= mod_new
    terms = []
    for a in (1, 2):
        u = pow(2, -a, mod_new)
        z = np.exp(-2j * np.pi * ((xi * u) % mod_new) / mod_new)
        w = Cn[(xi * u) % mod_old]
        terms.append(z * w)
    phi = float(np.angle(terms[0] * np.conj(terms[1])))
    return 1.0 - math.cos(phi), phi


# ----------------------------------------------------------------------------
# (S3) escape weights over a given unit array
# ----------------------------------------------------------------------------

def escape_weight_profile(mag, M, eps, U):
    """Per-unit escape weight sum_{a: xi u_a not in B(eps)} 2^-a.

    Returns (weights, bad_count). B(eps) = {units: |c| > (1-eps) M}.
    """
    mod = mag.size
    bad = np.zeros(mod, dtype=bool)
    bad[U[mag[U] > (1.0 - eps) * M]] = True
    weights = np.zeros(U.size, dtype=np.float64)
    for a in range(1, A_TRUNC + 1):
        mapped = (U * pow(2, -a, mod)) % mod
        weights += 2.0 ** (-a) * (~bad[mapped])
    return weights, int(bad.sum())


def chain_log(mod, xi):
    """Smallest k with 2^k == +/- xi (mod 3^n), or None."""
    p = 1
    want = {xi % mod, (-xi) % mod}
    period = 2 * (mod // 3)
    for k in range(period):
        if p in want:
            return k
        p = (2 * p) % mod
    return None


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    cert = {"packet": "2026-07-22-scalar-phase-second-moment",
            "scope": "float64 controls; proved statements live in memo"}

    n_max = int(os.environ.get("VSP_N_MAX", 14))
    layers = dict(syracuse_float_layers(n_max))
    Cn = {n: np.fft.fft(P) for n, P in layers.items()}
    units = {n: unit_residues(3 ** n) for n in layers}
    mag = {n: np.abs(Cn[n]) for n in layers}
    M = {n: float(mag[n][units[n]].max()) for n in layers}

    rng = np.random.RandomState(20260722)

    # (S1) exact second-moment identity --------------------------------------
    n_s1 = min(6, n_max - 1)
    mod_s1 = 3 ** (n_s1 + 1)
    xis = sorted({pow(2, k, mod_s1) for k in (0, 1, 7, 10, 11)} | {5 % mod_s1})
    err = s1_second_moment_check(Cn[n_s1], Cn[n_s1 + 1], xis, n_s1)
    assert err < 1e-8, err
    cert["s1_second_moment"] = {"n": n_s1, "xis": xis, "max_abs_err": err}

    # (S2) conditional contraction on samples --------------------------------
    n_s2 = min(6, n_max - 1)
    mod_s2 = 3 ** (n_s2 + 1)
    rand_units = [int(x) for x in rng.randint(0, mod_s2, 24)
                  if x % 3 != 0][:12]
    sample = sorted({pow(2, k, mod_s2) for k in (0, 1, 7, 10, 11)}
                    | {5 % mod_s2} | set(rand_units))
    rows = []
    for xi in sample:
        eta, phi = s2_relative_phase(Cn[n_s2], xi, n_s2)
        c_next = abs(Cn[n_s2 + 1][xi])
        bound = (1.0 - eta / 6.0) * M[n_s2]
        rows.append({"xi": int(xi), "eta": eta, "phi": phi,
                     "c_next": c_next, "bound": bound,
                     "holds": bool(c_next <= bound + 1e-12)})
        assert rows[-1]["holds"], rows[-1]
    cert["s2_conditional_contraction"] = {"n": n_s2, "samples": rows}

    # (S3) escape criterion over ALL units, small layers ---------------------
    s3_rows = []
    for n in range(3, min(11, n_max - 1) + 1):
        for eps in (0.05, 0.1, 0.2):
            w, bad_count = escape_weight_profile(mag[n], M[n], eps, units[n])
            w_min = float(w.min())
            bound = (1.0 - eps * w_min) * M[n]
            row = {"n": n, "eps": eps, "bad_count": bad_count,
                   "escape_weight_min": w_min,
                   "M_next": M[n + 1], "s3_bound": bound,
                   "holds": bool(M[n + 1] <= bound + 1e-12)}
            assert row["holds"], row
            s3_rows.append(row)
    cert["s3_escape_criterion"] = s3_rows

    # (4) bad-set structure table --------------------------------------------
    table = []
    for n in range(6, n_max + 1):
        U = units[n]
        row = {"n": n, "M_n": M[n]}
        for eps in (0.05, 0.1, 0.2):
            row[f"bad_count_{eps}"] = int((mag[n][U] > (1 - eps) * M[n]).sum())
        assert row["bad_count_0.05"] <= 4, row
        assert row["bad_count_0.1"] <= 6, row
        assert row["bad_count_0.2"] <= 8, row
        xi_peak = int(U[int(mag[n][U].argmax())])
        row["argmax"] = xi_peak
        k = chain_log(3 ** n, xi_peak)
        row["chain_log_k"] = k
        # 2 is a primitive root mod 3^n, so k always exists; the structural
        # claim is that k is SMALL: k ~ K(n) ~ n + 2.5 << 2*3^(n-1).
        assert k is not None and k <= 3 * n, row
        mod = 3 ** n
        row["flat1_a1"] = float(mag[n][(xi_peak * pow(2, -1, mod)) % mod] / M[n])
        row["flat2_a2"] = float(mag[n][(xi_peak * pow(2, -2, mod)) % mod] / M[n])
        sampleU = U[rng.randint(0, U.size, min(4000, U.size))]
        w, _ = escape_weight_profile(mag[n], M[n], 0.1, sampleU)
        row["escape_weight_avg_eps0.1"] = float(w.mean())
        if n >= 8:
            assert row["escape_weight_avg_eps0.1"] >= 0.95, row
            assert row["flat1_a1"] >= 0.5, row
        table.append(row)
    cert["bad_set_table"] = table

    # (5) peak decomposition: dilution x phase spread -------------------------
    if n_max >= 8:
        n = n_max
        mod_old, mod_new = 3 ** (n - 1), 3 ** n
        U = units[n]
        xi = int(U[int(mag[n][U].argmax())])
        terms = []
        for a in range(1, A_TRUNC + 1):
            u = pow(2, -a, mod_new)
            frac = ((xi * u) % mod_new) / mod_new
            z = np.exp(-2j * np.pi * frac)
            val = Cn[n - 1][(xi * u) % mod_old]
            terms.append({"a": a, "w": 2.0 ** (-a), "z_circle_frac": frac,
                          "val_abs_over_Mprev": float(abs(val) / M[n - 1]),
                          "val_arg": float(np.angle(val)),
                          "term": 2.0 ** (-a) * z * val})
        tot_abs = sum(t["w"] * abs(Cn[n - 1][(xi * pow(2, -t["a"], mod_new))
                                           % mod_old]) for t in terms)
        tot = sum(t["term"] for t in terms)
        dilution = float(tot_abs / M[n - 1])
        phase_factor = float(abs(tot) / tot_abs)
        ratio = M[n] / M[n - 1]
        ident_err = abs(dilution * phase_factor - ratio)
        assert ident_err < 1e-9, ident_err
        assert dilution < 1.0 and phase_factor < 1.0
        top = sorted(terms, key=lambda t: -abs(t["term"]))[:6]
        for t in top:
            t["term"] = [t["term"].real, t["term"].imag]
        u1, u2 = pow(2, -1, mod_new), pow(2, -2, mod_new)
        circle_point = ((xi * (u2 - u1)) % mod_new) / mod_new
        k = chain_log(mod_new, xi)
        if k is not None:
            assert circle_point >= 0.9 or circle_point <= 0.1, circle_point
        cert["peak_decomposition"] = {
            "n": n, "xi_peak": xi, "chain_log_k": k,
            "dilution": dilution, "phase_factor": phase_factor,
            "product": dilution * phase_factor,
            "M_ratio": ratio, "identity_err": ident_err,
            "scalar_circle_point_at_peak": circle_point,
            "top_terms": top}

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("scalar_phase_certificate.json", "w") as f:
        f.write(out + "\n")
    summary = {
        "status": "ok",
        "n_max": n_max,
        "s1_max_err": err,
        "s3_min_escape_weight": min(r["escape_weight_min"] for r in s3_rows),
        "bad_counts_last_layer": {k: v for k, v in table[-1].items()
                                  if k.startswith("bad_count")},
        "peak_chain_k": table[-1]["chain_log_k"],
        "escape_avg_last": table[-1]["escape_weight_avg_eps0.1"],
    }
    if "peak_decomposition" in cert:
        pd = cert["peak_decomposition"]
        summary["dilution"] = pd["dilution"]
        summary["phase_factor"] = pd["phase_factor"]
        summary["M_ratio"] = pd["M_ratio"]
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
