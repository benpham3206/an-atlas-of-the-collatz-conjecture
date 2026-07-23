#!/usr/bin/env python3
"""Executable controls for COLLATZ_PLATEAU_ESCAPE_WEIGHT.md.

Verifies / measures:
  (T1) exact scalar phases on the resonance chain: for the peak frequency
       xi* = +/- 2^K (mod 3^n) with 2^K < 3^n (exact integer certificate,
       no modular wrap), the recursion phase factor is
       z_a = e(-s * 2^{K-a} / 3^n) EXACTLY (Fraction arithmetic);
       the dominant-pair scalar misalignment is exactly 2^{K-2}/3^n.
  (T2) no phase-blind supersolution: the same-layer magnitude transport T is
       doubly stochastic on units (up to the 2^-40 tail), so min_xi Tq/q <= 1.
  (T3) S3's escape bound is the epsilon-quantization of the triangle bound:
       (1 - eps*w) * M_n >= sum_a 2^-a |c_n(xi* u_a)| >= M_{n+1} at the peak.
  (T4) containment => explicit escape weight: when B_n(eps) is contained in
       +/- {2^K, 2^{K-1}}, every unit has bad-image weight <= 3/4, hence
       w_n(eps) >= 1/4 - 2^-40 (checked against the exact computed w).
  (M1) chain profile table p_j(n), j = 0..8, n = 8..n_max, with plateau
       statistics (drift slope, max deviation) and the phase profile psi_j.
  (M2) escape-weight table w_n(eps), eps in {0.05, 0.1, 0.2}, S3-faithful
       (min over units of the NEXT layer), full units for n <= 11,
       seeded sample + exact near-chain for n = 12..n_max-1; quantized
       values; fit of w_n(0.05) against const and against c/sqrt(n).
  (M3) the dichotomy crossover n* at which a sustained w >= 1/4 would force
       M_n below the measured exp(-1.06 sqrt n) law.

Float64 statistics are numerical controls / hypothesis-generators only;
the proved statements live in the memo. Exact-arithmetic certificate paths
(chain phases) use Python ints and Fractions, never float logs.

Env knobs: VEW_N_MAX (default 14), VEW_SAMPLE (default 200000).
"""

import json
import math
import os
import sys
from fractions import Fraction

import numpy as np

A_TRUNC = 40  # geometric tail beyond a=40 has weight <= 2^-40
SEED = 20260722


# ----------------------------------------------------------------------------
# Syracuse offset distributions (float), provenance: copied from
# contribution/packets/2026-07-22-syracuse-fourier/verify_syracuse_fourier.py
# (same construction as the scalar-phase packet).
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


def peak_chain_data(mag, U, mod):
    """Return (xi_peak, K, sign) with xi_peak = sign * 2^K (mod 3^n)."""
    xi = int(U[int(mag[U].argmax())])
    k = chain_log(mod, xi)
    assert k is not None
    sign = 1 if pow(2, k, mod) == xi % mod else -1
    assert (sign * pow(2, k, mod)) % mod == xi % mod
    return xi, k, sign


def chain_point(xi_peak, j, mod):
    """j-th predecessor of the peak along the walk: xi* * 2^{-j} (mod 3^n)."""
    return int((xi_peak * pow(2, -j, mod)) % mod)


# ----------------------------------------------------------------------------
# (T1) exact chain phases (integer / Fraction arithmetic only)
# ----------------------------------------------------------------------------

def exact_chain_phases(K, sign, n, a_max=6):
    """Exact circle points {xi* u_a / 3^n} on the chain as Fractions.

    Requires 2^K < 3^n (checked, exact): then xi* u_a mod 3^n is the integer
    s*2^{K-a} for s=+1 (resp. 3^n - 2^{K-a} for s=-1), no wrap.
    Returns dict a -> (Fraction circle point, exact residue int).
    """
    mod = 3 ** n
    assert 2 ** K < mod, "canonical representative wraps; formula needs care"
    out = {}
    for a in range(1, a_max + 1):
        assert K - a >= 0
        res = pow(2, K - a, mod)          # exact integer 2^{K-a}
        assert res == 2 ** (K - a)        # no modular wrap, exact certificate
        r = (sign * res) % mod
        out[a] = (Fraction(r, mod), r)
    return out


# ----------------------------------------------------------------------------
# (T2) same-layer magnitude transport is doubly stochastic (up to tail)
# ----------------------------------------------------------------------------

def transport_same_layer(q, mod):
    """(Tq)(xi) = sum_a 2^-a q(xi 2^-a mod 3^n) on unit-indexed vector q.

    q is a full array of length mod; only unit entries are used.
    """
    Tq = np.zeros(mod, dtype=np.float64)
    for a in range(1, A_TRUNC + 1):
        Tq += 2.0 ** (-a) * q[(np.arange(mod, dtype=np.uint64)
                               * pow(2, -a, mod)) % mod]
    return Tq


# ----------------------------------------------------------------------------
# escape weights, S3-faithful: min over units xi of the NEXT layer of
# sum_{a: xi u_a mod 3^n not in B_n(eps)} 2^-a  (bounds M_{n+1}/M_n via S3)
# ----------------------------------------------------------------------------

def bad_mask(mag, M, eps, U):
    mod = mag.size
    bad = np.zeros(mod, dtype=bool)
    bad[U[mag[U] > (1.0 - eps) * M]] = True
    return bad


def escape_weights_next_layer(bad, mod_n, query_units_next):
    """Per-query-unit escape weight into the layer-n bad set."""
    w = np.zeros(query_units_next.size, dtype=np.float64)
    bw = np.zeros(query_units_next.size, dtype=np.float64)
    for a in range(1, A_TRUNC + 1):
        mapped = (query_units_next * pow(2, -a, mod_n)) % mod_n
        w += 2.0 ** (-a) * (~bad[mapped])
        bw += 2.0 ** (-a) * bad[mapped]
    return w, bw


def near_chain_units(mod, K, sign, jmax=12):
    """Units +/- 2^{K+j} and +/- 2^{K-1+j} (mod) for j in [-2, jmax]:
    the candidates for minimal escape weight (their low-a images are bad)."""
    pts = set()
    for s in (1, -1):
        for j in range(-2, jmax + 1):
            pts.add((s * pow(2, K + j, mod)) % mod)
    return np.array(sorted(pts), dtype=np.uint64)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    n_max = int(os.environ.get("VEW_N_MAX", 14))
    n_sample = int(os.environ.get("VEW_SAMPLE", 200000))
    assert n_max >= 8
    cert = {"packet": "2026-07-22-plateau-escape-weight",
            "scope": "float64 controls; proved statements live in memo",
            "n_max": n_max, "a_trunc": A_TRUNC}

    layers = dict(syracuse_float_layers(n_max))
    Cn = {n: np.fft.fft(P) for n, P in layers.items()}
    units = {n: unit_residues(3 ** n) for n in layers}
    mag = {n: np.abs(Cn[n]) for n in layers}
    M = {n: float(mag[n][units[n]].max()) for n in layers}
    peak = {n: peak_chain_data(mag[n], units[n], 3 ** n) for n in layers}

    rng = np.random.RandomState(SEED)

    # -- chain exponent law and exactness guard ------------------------------
    chain_law = []
    for n in range(6, n_max + 1):
        xi, K, sign = peak[n]
        # exact certificate: 2^K does not wrap mod 3^n (needed for T1 formula)
        no_wrap = bool(2 ** K < 3 ** n)
        assert no_wrap, (n, K)
        chain_law.append({"n": n, "xi_peak": xi, "K": K, "sign": sign,
                          "K_minus_n": K - n, "two_pow_K_lt_3_pow_n": no_wrap})
        assert K <= n + 3, (n, K)  # measured law, flagged loudly if it breaks
    cert["chain_exponent_law"] = chain_law

    # -- (T1) exact chain phases ---------------------------------------------
    t1_rows = []
    for n in range(8, n_max + 1):
        xi, K, sign = peak[n]
        ph = exact_chain_phases(K, sign, n)
        rel = (ph[1][0] - ph[2][0]) % 1      # exact relative scalar circle pt
        rel_expected = Fraction(2 ** (K - 2), 3 ** n) if sign == 1 \
            else 1 - Fraction(2 ** (K - 2), 3 ** n)
        # alignment distance of the dominant pair from exact phase lock
        misalign = min(rel, 1 - rel)
        assert misalign == Fraction(2 ** (K - 2), 3 ** n)
        bound = Fraction(2 ** (n + 1), 3 ** n)  # from K <= n + 3
        assert misalign <= bound
        # float control: circle points match the FFT-side phase factors
        z1 = np.exp(-2j * np.pi * float(ph[1][0]))
        u1 = pow(2, -1, 3 ** n)
        z1_direct = np.exp(-2j * np.pi * ((xi * u1) % (3 ** n)) / 3 ** n)
        assert abs(z1 - z1_direct) < 1e-12
        t1_rows.append({
            "n": n, "K": K, "sign": sign,
            "circle_points_exact": {str(a): [str(ph[a][0].numerator),
                                             str(ph[a][0].denominator)]
                                    for a in ph},
            "circle_points_float": {str(a): float(ph[a][0]) for a in ph},
            "dominant_pair_misalignment_exact": [str(misalign.numerator),
                                                 str(misalign.denominator)],
            "dominant_pair_misalignment_float": float(misalign),
            "misalignment_bound_(2/3-style)": float(bound),
        })
    cert["t1_exact_chain_phases"] = t1_rows

    # recursion identity re-check on the chain peak (Theorem 1 of packet 4)
    n_id = min(9, n_max)
    xi, K, sign = peak[n_id]
    mod_old, mod_new = 3 ** (n_id - 1), 3 ** n_id
    rec = 0j
    for a in range(1, A_TRUNC + 1):
        u = pow(2, -a, mod_new)
        frac = ((xi * u) % mod_new) / mod_new
        rec += 2.0 ** (-a) * np.exp(-2j * np.pi * frac) * Cn[n_id - 1][(xi * u) % mod_old]
    id_err = abs(rec - Cn[n_id][xi])
    assert id_err < 1e-12, id_err
    cert["chain_recursion_identity_err"] = id_err

    # -- (T2) no phase-blind supersolution: stochasticity control ------------
    m = 6
    mod_t2 = 3 ** m
    q = rng.rand(mod_t2) + 0.5
    q[ np.arange(mod_t2) % 3 == 0] = 0.0
    Tq = transport_same_layer(q, mod_t2)
    U_t2 = unit_residues(mod_t2)
    mass_in = float(q[U_t2].sum())
    mass_out = float(Tq[U_t2].sum())
    tail = 1.0 - 2.0 ** (-A_TRUNC)
    assert abs(mass_out - tail * mass_in) < 1e-9 * mass_in
    ratio = Tq[U_t2] / q[U_t2]
    min_ratio = float(ratio.min())
    assert min_ratio <= tail + 1e-12  # some unit always fails to contract
    cert["t2_supersolution_barrier"] = {
        "modulus": mod_t2, "mass_in": mass_in, "mass_out": mass_out,
        "mass_ratio_exact_tail": tail, "min_Tq_over_q": min_ratio,
        "conclusion": "min_xi (Tq)(xi)/q(xi) <= 1 - 2^-40 < 1: no nonzero "
                      "phase-blind supersolution with strict contraction"}

    # -- (M1) chain profile table and plateau statistics ----------------------
    J = 8
    profile = []
    for n in range(8, n_max + 1):
        xi, K, sign = peak[n]
        mod = 3 ** n
        row = {"n": n, "K": K, "sign": sign,
               "p": {str(j): float(mag[n][chain_point(xi, j, mod)] / M[n])
                     for j in range(J + 1)},
               "psi": {str(j): float(np.angle(Cn[n][chain_point(xi, j, mod)]))
                       for j in range(J + 1)}}
        profile.append(row)
    cert["profile_table"] = profile

    plateau_stats = []
    ns = np.array([r["n"] for r in profile], dtype=np.float64)
    for j in range(J + 1):
        vals = np.array([r["p"][str(j)] for r in profile])
        slope = float(np.polyfit(ns, vals, 1)[0]) if ns.size >= 3 else None
        plateau_stats.append({"j": j, "min": float(vals.min()),
                              "max": float(vals.max()),
                              "mean": float(vals.mean()),
                              "slope_per_layer": slope,
                              "max_abs_dev": float(np.abs(vals - vals.mean()).max())})
    # phase plateau: circular spread of psi_j over the window
    for j in range(J + 1):
        psis = np.array([r["psi"][str(j)] for r in profile])
        z = np.exp(1j * psis).mean()
        plateau_stats[j]["psi_circular_concentration"] = float(abs(z))
        plateau_stats[j]["psi_mean"] = float(np.angle(z))
    cert["plateau_stats"] = plateau_stats

    # delta-K sequence (chain exponent increments)
    dK = [{"n": n, "dK": peak[n + 1][1] - peak[n][1],
           "sign_flip": peak[n + 1][2] != peak[n][2]}
          for n in range(8, n_max)]
    cert["delta_K"] = dK

    # phase-blind slack at the peak: triangle bound vs actual ratio
    slack = []
    for n in range(8, n_max):
        xi_next, K_next, s_next = peak[n + 1]
        mod_n, mod_next = 3 ** n, 3 ** (n + 1)
        tri = 0.0
        for a in range(1, A_TRUNC + 1):
            tri += 2.0 ** (-a) * mag[n][(xi_next * pow(2, -a, mod_next)) % mod_n]
        tri /= M[n]
        rho = M[n + 1] / M[n]
        assert tri >= rho - 1e-12
        slack.append({"n": n, "triangle_bound_at_peak": tri, "rho": rho,
                      "phase_factor_at_peak": rho / tri})
    cert["peak_phase_bite"] = slack

    # total term phases theta_a at the peak (float control over the exact
    # scalar part + intrinsic arg of c): theta_a = arg(z_a * c_n(image_a))
    term_phase_rows = []
    for n in range(8, n_max):
        xi_next, K_next, s_next = peak[n + 1]
        mod_n, mod_next = 3 ** n, 3 ** (n + 1)
        thetas = []
        for a in range(1, 7):
            u = pow(2, -a, mod_next)
            frac = ((xi_next * u) % mod_next) / mod_next
            term = np.exp(-2j * np.pi * frac) * Cn[n][(xi_next * u) % mod_n]
            thetas.append(float(np.angle(term)))
        # spread of the dominant (weight 15/16) terms a = 1..4, circular
        z = np.exp(1j * np.array(thetas[:4]))
        spread = float(np.angle(np.exp(1j * thetas[0]) *
                                np.conj(np.exp(1j * thetas[1]))))
        term_phase_rows.append({
            "n": n, "theta_a_deg": [float(np.degrees(t)) for t in thetas],
            "dominant4_circular_concentration": float(abs(z.mean())),
            "theta12_gap_deg": float(np.degrees(spread))})
    cert["peak_term_phases"] = term_phase_rows

    # -- (M2)+(T3)+(T4) escape weights, S3-faithful ---------------------------
    epsilons = (0.05, 0.1, 0.2)
    esc_rows = []
    for n in range(6, n_max):
        mod_n = 3 ** n
        full = 3 ** (n + 1) <= 5_000_000  # next-layer units enumerable
        for eps in epsilons:
            bad = bad_mask(mag[n], M[n], eps, units[n])
            bad_pts = np.nonzero(bad)[0]
            logs = sorted(chain_log(mod_n, int(x)) for x in bad_pts)
            K = peak[n][1]
            idx = sorted(K - k for k in logs)  # indices j of bad chain points
            # containment: bad set = {+/-2^{K-j} : j in [lo, hi]} exactly
            lo, hi = (min(idx), max(idx)) if idx else (0, -1)
            L = hi - lo + 1 if idx else 0
            contained = bool(idx) and idx == sorted(
                j for j in range(lo, hi + 1) for _ in range(2))
            # query units of the next layer
            if full:
                Q = units[n + 1]
            else:
                Q = rng.randint(0, 3 ** (n + 1), n_sample).astype(np.uint64)
                Q = Q[Q % 3 != 0]
                Q = np.unique(np.concatenate(
                    [Q, near_chain_units(3 ** (n + 1), peak[n + 1][1],
                                         peak[n + 1][2])]))
            w, bw = escape_weights_next_layer(bad, mod_n, Q)
            w_min = float(w.min())
            bw_max = float(bw.max())
            # (T4) containment in an L-interval => bad weight <= 1 - 2^-L
            if contained:
                assert bw_max <= 1.0 - 2.0 ** (-L) + 1e-9, (n, eps, bw_max, L)
                assert w_min >= 2.0 ** (-L) - 2.0 ** (-A_TRUNC) - 1e-9
            else:  # kill criterion: a bad frequency off the chain interval
                raise AssertionError(("containment failed", n, eps, idx))
            # (T5) phase-blind propagation margin: the best phase-blind
            # certificate at the worst next-layer unit is (1-eps(1-bw))M_n,
            # which EXCEEDS the next-layer bad threshold (1-eps)M_{n+1}
            # whenever M_{n+1}/M_n < (1-eps(1-bw))/(1-eps) -- always, here.
            cert_bound = (1.0 - eps * (1.0 - bw_max)) * M[n]
            threshold = (1.0 - eps) * M[n + 1]
            gap = cert_bound - threshold
            assert gap > 0, (n, eps, gap)  # phase-blind propagation fails
            bound = (1.0 - eps * w_min) * M[n]
            tri = 0.0
            xi_next = peak[n + 1][0]
            for a in range(1, A_TRUNC + 1):
                tri += 2.0 ** (-a) * mag[n][(xi_next * pow(2, -a, 3 ** (n + 1))) % mod_n]
            # (T3) quantization gap: S3 bound dominates triangle bound at peak
            assert bound >= tri - 1e-9, (n, eps, bound, tri)
            row = {"n": n, "eps": eps, "mode": "full" if full else "sampled",
                   "bad_count": int(bad.sum()), "bad_chain_indices": idx,
                   "interval_span": [lo, hi] if idx else None,
                   "interval_length_L": L, "contained_in_chain_interval": contained,
                   "escape_weight_min": w_min,
                   "bad_weight_max": bw_max,
                   "t4_lower_bound": 2.0 ** (-L) - 2.0 ** (-A_TRUNC) if contained else None,
                   "t5_phaseblind_certificate": cert_bound,
                   "t5_next_layer_threshold": threshold,
                   "t5_propagation_gap_over_M": gap / M[n],
                   "s3_bound": bound, "triangle_bound_at_peak": tri,
                   "M_ratio": M[n + 1] / M[n],
                   "holds": bool(M[n + 1] <= bound + 1e-12)}
            assert row["holds"], row
            esc_rows.append(row)
    cert["escape_weight_table"] = esc_rows

    # w-shape analysis: constant vs c/sqrt(n), eps = 0.05, full layers only
    w05 = [(r["n"], r["escape_weight_min"]) for r in esc_rows
           if r["eps"] == 0.05 and r["mode"] == "full" and r["n"] >= 6]
    ns_w = np.array([x[0] for x in w05], dtype=np.float64)
    ws = np.array([x[1] for x in w05])
    inv_sqrt = 1.0 / np.sqrt(ns_w)
    corr_inv_sqrt = (float(np.corrcoef(ws, inv_sqrt)[0, 1])
                     if ws.size >= 2 and ws.std() > 0 else None)
    w_shape = {"n": [int(x) for x in ns_w], "w_0.05": [float(x) for x in ws],
               "min": float(ws.min()), "max": float(ws.max()),
               "mean": float(ws.mean()), "std": float(ws.std()),
               "corr_with_1_over_sqrt_n": corr_inv_sqrt,
               "note": "w is quantized (dyadic sums); a c/sqrt(n) law would "
                       "require interval-length creep, not seen in window"}
    cert["w_shape_analysis"] = w_shape

    # -- (M3) dichotomy crossover ---------------------------------------------
    # If w_n(0.05) >= 1/4 - 2^-40 for all n >= n0, S3 gives M decay with rate
    # 1 - 0.05/4 = 79/80 per layer. The measured law M ~ exp(-1.06 sqrt n)
    # has ratio exp(-1.06/(2 sqrt n)) which EXCEEDS 79/80 for n > n*.
    c_meas = 1.06  # measured sqrt-decay constant, packet 3 / packet 5 (float64)
    eps_d, w_d = 0.05, 0.25
    rate = 1.0 - eps_d * w_d
    assert abs(rate - float(Fraction(79, 80))) < 1e-18
    n_star = (c_meas / (-2.0 * math.log(rate))) ** 2
    cert["dichotomy_crossover"] = {
        "eps": eps_d, "w": w_d, "rate_exact": "79/80", "rate_float": rate,
        "c_measured_sqrt_law": c_meas,
        "n_star": n_star, "n_star_ceil": math.ceil(n_star),
        "statement": "w_n(0.05) >= 1/4 for all n and M_n ~ exp(-1.06 sqrt n) "
                     "are incompatible beyond n*; one of the two empirical "
                     "laws must break"}

    out = json.dumps(cert, indent=1, sort_keys=True)
    with open("plateau_escape_weight_certificate.json", "w") as f:
        f.write(out + "\n")

    summary = {
        "status": "ok", "n_max": n_max,
        "chain_K": {r["n"]: r["K"] for r in chain_law},
        "misalignment_last": t1_rows[-1]["dominant_pair_misalignment_float"],
        "p2_range": [min(r["p"]["2"] for r in profile),
                     max(r["p"]["2"] for r in profile)],
        "p2_slope": [s["slope_per_layer"] for s in plateau_stats if s["j"] == 2][0],
        "w005_values": w_shape["w_0.05"],
        "t2_min_ratio": min_ratio,
        "n_star": n_star,
        "peak_phase_factor_last": slack[-1]["phase_factor_at_peak"] if slack else None,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
