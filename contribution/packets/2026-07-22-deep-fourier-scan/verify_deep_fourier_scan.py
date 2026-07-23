#!/usr/bin/env python3
"""Executable controls for COLLATZ_DEEP_FOURIER_SCAN.md.

Extends the float64 measurements of the tao-structural-refinement,
syracuse-fourier, and scalar-phase-second-moment packets from n <= 14 to
n = VDFS_N_MAX (default 17; n = 18 is reachable but behind the env flag
because of runtime), STREAMING: at most two Syracuse layers and one FFT
are alive at any moment.

Verifies (proved statements, asserted):
  (L2) the parity-class contraction bound on r_n (syracuse-fourier
       Lemma 2), every layer;
  (S1) the exact second-moment recursion (scalar-phase Theorem S1)
       against FFT at sampled frequencies, layers n in {6, 9, 12};
  (S3) the bad-set escape criterion (scalar-phase Theorem S3) on ALL
       units, layers 6 <= n <= 11 (full-unit escape weights as in the
       scalar-phase packet).

Measures (float64 hypothesis-generators, recorded, never asserted):
  per layer n = 6..n_max: M_n and the e^{-c sqrt(n)} fit; bad-set counts
  |B(0.05/0.1/0.2)|; argmax and its chain exponent k(n) (exact BSGS
  discrete log: smallest k with 2^k == +/- xi mod 3^n); chain membership
  of EVERY B(0.1) member (kill criterion 1 of the scalar-phase packet);
  flat1/flat2 near-peak profile; escape-weight average over >= 4000
  seeded random units (eps = 0.1); conjugate symmetry of B(0.1);
  sampled S3 bound above n = 11; max |c_n| at NONZERO multiples of 3
  (sanity: should equal M_1 for all n by the layer marginalisation).

Env knobs: VDFS_N_MAX (default 17), VDFS_SAMPLES (default 8192 seeded
random units per layer). Reduced test mode: VDFS_N_MAX=10.
"""

import json
import math
import os
import sys
import time

import numpy as np

A_TRUNC = 40  # geometric tail beyond a=40 has weight <= 2^-40
SEED = 20260722
S1_CHECK_LAYERS = (6, 9, 12)   # S1 identity checked at these n (needs n+1)
S3_FULL_MAX = 11               # full-unit escape weights up to this layer
FIT_MIN = 6                    # decay fit window start


# ----------------------------------------------------------------------------
# Syracuse offset distributions (float).
# Provenance: copied verbatim from the syracuse-fourier packet
# (contribution/packets/2026-07-22-syracuse-fourier/verify_syracuse_fourier.py),
# which credits the tao-structural-refinement packet.
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
# Unit residues without materialising the unit list at depth.
# The units mod 3^n in increasing order are 1, 2, 4, 5, 7, 8, ...; the
# j-th (0-based) unit is 3*(j//2) + 1 + (j%2), for 0 <= j < 2*3^(n-1).
# ----------------------------------------------------------------------------

def unit_from_index(j):
    return 3 * (j // 2) + 1 + (j % 2)


def unit_index_array(count):
    j = np.arange(count, dtype=np.uint64)
    return 3 * (j // 2) + 1 + (j % 2)


# ----------------------------------------------------------------------------
# Exact chain exponent: smallest k with 2^k == +/- xi (mod 3^n).
# Baby-step giant-step discrete log, exact integer arithmetic
# (pow with modulus only; no floats). 2 is a primitive root mod 3^n
# (syracuse-fourier packet, verified n <= 6), so a unit always has a
# base-2 logarithm; None means xi is off the +2^k chain entirely.
# ----------------------------------------------------------------------------

def chain_log_bsgs(mod, xi):
    """Smallest k >= 0 with 2^k == xi (mod 3^n), or None. Exact."""
    xi %= mod
    if xi == 0 or math.gcd(xi, mod) != 1:
        return None
    order = 2 * (mod // 3)
    m = math.isqrt(order) + 1
    baby = {}
    p = 1
    for j in range(m):
        if p not in baby:
            baby[p] = j
        p = (2 * p) % mod
    inv_m = pow(pow(2, m, mod), -1, mod)
    g = xi
    for i in range(m + 1):
        j = baby.get(g)
        if j is not None:
            k = i * m + j
            if k < order:
                return k
        g = (g * inv_m) % mod
    return None


def chain_exponent(mod, xi):
    """Smallest k with 2^k == +xi or 2^k == -xi (mod 3^n), or None."""
    k1 = chain_log_bsgs(mod, xi)
    k2 = chain_log_bsgs(mod, (-xi) % mod)
    cands = [k for k in (k1, k2) if k is not None]
    return min(cands) if cands else None


def chain_log_bruteforce(mod, xi):
    """Reference: smallest k with 2^k == +/- xi (mod 3^n), or None.

    Provenance: logic of chain_log() in the scalar-phase packet's
    verify_scalar_phase.py, used here only to cross-check the BSGS.
    """
    p = 1
    want = {xi % mod, (-xi) % mod}
    period = 2 * (mod // 3)
    for k in range(period):
        if p in want:
            return k
        p = (2 * p) % mod
    return None


# ----------------------------------------------------------------------------
# (S1) exact second-moment identity.
# Provenance: s1_second_moment_check copied from the scalar-phase packet's
# verify_scalar_phase.py (Theorem S1), unchanged except for the name.
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
# Escape weights (scalar-phase packet, Theorem S3).
# Provenance: escape_weight_profile in verify_scalar_phase.py, refactored
# to take a precomputed bad-set boolean array (identical semantics).
# ----------------------------------------------------------------------------

def escape_weights(bad, U, mod):
    """Per-unit escape weight sum_{a: xi u_a not in B} 2^-a."""
    weights = np.zeros(U.size, dtype=np.float64)
    for a in range(1, A_TRUNC + 1):
        mapped = (U * pow(2, -a, mod)) % mod
        weights += 2.0 ** (-a) * (~bad[mapped])
    return weights


def bad_indices(mag, M, eps):
    """Flat indices of unit frequencies with |c| > (1-eps) M, via the
    reshape trick: residues mod 3 are the columns of a (-1, 3) view, so
    units are columns 1 and 2 and no unit index array is materialised."""
    mod = mag.size
    mag3 = mag.reshape(mod // 3, 3)
    over = mag3[:, 1:] > (1.0 - eps) * M
    rows = np.nonzero(over.ravel())[0]
    return 3 * (rows // 2) + 1 + (rows % 2)


# ----------------------------------------------------------------------------
# Decay fit: -ln M_n vs sqrt(n)
# ----------------------------------------------------------------------------

def decay_fit(ns, Ms):
    x = np.array([math.sqrt(n) for n in ns], dtype=np.float64)
    y = np.array([-math.log(m) for m in Ms], dtype=np.float64)
    c_origin = float((x * y).sum() / (x * x).sum())
    resid = y - c_origin * x
    # with-intercept least squares
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    resid2 = y - (slope * x + intercept)
    ss_res = float((resid2 ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return {
        "window": [int(ns[0]), int(ns[-1])],
        "per_layer_c_n": {str(int(n)): float(-math.log(m) / math.sqrt(n))
                          for n, m in zip(ns, Ms)},
        "c_fit_through_origin": c_origin,
        "max_abs_residual_origin_fit": float(np.abs(resid).max()),
        "c_fit_with_intercept": float(slope),
        "intercept": float(intercept),
        "max_abs_residual_intercept_fit": float(np.abs(resid2).max()),
        "r_squared_intercept_fit": 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0,
        "reference_c_from_prior_packets": 1.06,
    }


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    n_max = int(os.environ.get("VDFS_N_MAX", 17))
    n_samples = int(os.environ.get("VDFS_SAMPLES", 8192))
    if n_samples < 4000:
        raise SystemExit("VDFS_SAMPLES must be >= 4000")
    cert = {"packet": "2026-07-22-deep-fourier-scan",
            "scope": "float64 hypothesis-generators beyond proved items; "
                     "proved statements (asserted) are Lemma 2 of "
                     "syracuse-fourier and S1/S3 of scalar-phase",
            "n_max": n_max, "seed": SEED, "unit_samples_per_layer": n_samples}

    rng = np.random.RandomState(SEED)
    M = {}
    mult3_max = {}
    r_rows = []
    r_prev = None
    layer_rows = []
    s1_rows = []
    s3_rows = []
    pending_s3 = None  # dict with n, M_n, w_min per eps, sampled flag
    C_prev = None
    t_start = time.time()

    for n, P in syracuse_float_layers(n_max):
        t0 = time.time()
        mod = 3 ** n
        # (L2) parity-class contraction of r_n (proved Lemma 2), asserted
        r = float(P.max())
        row_r = {"n": n, "r_n": r}
        if r_prev is not None:
            bound = (2.0 / 3.0) * r_prev / (1.0 - 2.0 ** (-2 * 3 ** (n - 2)))
            row_r["ratio"] = r / r_prev
            row_r["lemma2_bound_holds"] = bool(r <= bound + 1e-15)
            assert row_r["lemma2_bound_holds"], n
        r_rows.append(row_r)
        r_prev = r

        C = np.fft.fft(P)
        mag = np.abs(C)
        del P
        mag3 = mag.reshape(mod // 3, 3)
        M[n] = float(mag3[:, 1:].max())
        # sanity on the M_n definition: excluding xi = 0, the max over
        # multiples of 3 should equal M_1 for every n, because
        # c_n(3 xi') = c_{n-1}(xi') by the layer marginalisation, so
        # max_{3|xi, xi!=0} |c_n(xi)| = max_{xi'!=0} |c_{n-1}(xi')|
        # = max(M_{n-1}, same quantity at n-1) = ... = M_1.
        col0 = mag3[:, 0]
        mult3_max[n] = float(col0[1:].max()) if col0.size > 1 else 0.0

        # resolve last layer's pending S3 bound now that M[n] exists
        if pending_s3 is not None and pending_s3["n"] == n - 1:
            for eps, w_min in pending_s3["w_min"].items():
                bound = (1.0 - eps * w_min) * pending_s3["M_n"]
                row = {"n": pending_s3["n"], "eps": eps,
                       "sampled": pending_s3["sampled"],
                       "escape_weight_min": w_min,
                       "M_next": M[n], "s3_bound": bound,
                       "holds": bool(M[n] <= bound + 1e-12)}
                if not pending_s3["sampled"]:
                    assert row["holds"], row  # proved Theorem S3, full units
                s3_rows.append(row)
            pending_s3 = None

        # (S1) second-moment identity at layers in S1_CHECK_LAYERS
        if (n - 1) in S1_CHECK_LAYERS and C_prev is not None and n - 1 <= 12:
            n1 = n - 1
            mod1 = 3 ** (n1 + 1)
            xis = sorted(
                {pow(2, k, mod1) for k in (0, 1, 7, 10, 11)}
                | {5 % mod1}
                | {int(x) for x in rng.randint(0, mod1, 12)})
            err = s1_second_moment_check(C_prev, C, xis, n1)
            assert err < 1e-8, (n1, err)
            s1_rows.append({"n": n1, "n_sampled_xis": len(xis),
                            "max_abs_err": err})

        # deep per-layer measurements
        if n >= FIT_MIN:
            row = {"n": n, "M_n": M[n],
                   "max_abs_char_at_nonzero_multiples_of_3": mult3_max[n],
                   "ratio_nonzero_mult3_max_over_M_1": mult3_max[n] / M[1]}
            mag3 = mag.reshape(mod // 3, 3)
            unit_view = mag3[:, 1:]
            peak_flat = int(unit_view.argmax())
            xi_peak = int(3 * (peak_flat // 2) + 1 + (peak_flat % 2))
            row["argmax"] = xi_peak
            k_peak = chain_exponent(mod, xi_peak)
            row["chain_log_k"] = k_peak
            row["chain_law_k_in_n..n+3"] = (
                bool(k_peak is not None and n <= k_peak <= n + 3))
            # bad sets
            bad = {}
            for eps in (0.05, 0.1, 0.2):
                idx = bad_indices(mag, M[n], eps)
                row[f"bad_count_{eps}"] = int(idx.size)
                b = np.zeros(mod, dtype=bool)
                b[idx] = True
                bad[eps] = (idx, b)
            # kill criterion 1: chain membership of EVERY B(0.1) member
            members = []
            off_chain = []
            for xi in bad[0.1][0].tolist():
                k = chain_exponent(mod, xi)
                members.append({"xi": int(xi), "chain_log_k": k})
                if k is None:
                    off_chain.append(int(xi))
            row["bad_set_0.1_members"] = members
            row["bad_set_0.1_off_chain"] = off_chain
            # conjugate symmetry of B(0.1)
            idx01 = bad[0.1][0]
            conj_idx = (-idx01) % mod
            row["bad_set_0.1_conjugate_max_asym"] = float(
                np.abs(mag[idx01] - mag[conj_idx]).max()) if idx01.size else 0.0
            row["bad_set_0.1_conjugate_symmetric"] = bool(
                idx01.size == 0
                or (mag[conj_idx] > (1.0 - 0.1) * M[n]).all())
            # near-peak profile
            row["flat1_a1"] = float(
                mag[(xi_peak * pow(2, -1, mod)) % mod] / M[n])
            row["flat2_a2"] = float(
                mag[(xi_peak * pow(2, -2, mod)) % mod] / M[n])
            # escape-weight average over seeded random units (eps = 0.1)
            j = rng.randint(0, 2 * (mod // 3), size=n_samples)
            U = 3 * (j // 2) + 1 + (j % 2)
            w = escape_weights(bad[0.1][1], U, mod)
            row["escape_weight_avg_eps0.1"] = float(w.mean())
            row["escape_weight_min_sampled_eps0.1"] = float(w.min())
            # S3 for next layer: full units up to S3_FULL_MAX, sampled above
            if n <= S3_FULL_MAX and n >= 3:
                Uall = unit_index_array(2 * (mod // 3))
                w_min = {}
                for eps in (0.05, 0.1, 0.2):
                    wall = escape_weights(bad[eps][1], Uall, mod)
                    w_min[eps] = float(wall.min())
                pending_s3 = {"n": n, "M_n": M[n], "w_min": w_min,
                              "sampled": False}
            elif n > S3_FULL_MAX:
                pending_s3 = {"n": n, "M_n": M[n],
                              "w_min": {0.1: float(w.min())},
                              "sampled": True}
            layer_rows.append(row)

        C_prev = C if n in S1_CHECK_LAYERS else None
        del mag
        if C_prev is None:
            del C
        print(f"layer {n:2d} done in {time.time() - t0:6.1f}s  "
              f"M_n={M[n]:.6e}", flush=True)

    cert["r_n_table"] = r_rows
    cert["s1_second_moment"] = s1_rows
    cert["s3_escape_criterion"] = s3_rows
    cert["layer_table"] = layer_rows

    ns = [r["n"] for r in layer_rows]
    Ms = [r["M_n"] for r in layer_rows]
    cert["decay_fit"] = decay_fit(ns, Ms)

    ks = [r["chain_log_k"] for r in layer_rows]
    if all(k is not None for k in ks):
        slope, intercept = np.polyfit(np.array(ns, dtype=np.float64),
                                      np.array(ks, dtype=np.float64), 1)
        cert["chain_exponent_fit"] = {
            "window": [int(ns[0]), int(ns[-1])],
            "k_over_n_slope": float(slope),
            "intercept": float(intercept),
            "k_minus_n": {str(int(n)): int(k - n) for n, k in zip(ns, ks)},
            "note": "2 is a primitive root mod 3^n, so k < 2*3^(n-1) is "
                    "automatic; the structural content is k = O(n)"}

    off_chain_all = {str(r["n"]): r["bad_set_0.1_off_chain"]
                     for r in layer_rows if r["bad_set_0.1_off_chain"]}
    cert["kill_criteria_status"] = {
        "kc1_bad_set_off_chain_frequencies": off_chain_all,
        "kc1_fired": bool(off_chain_all),
        "chain_law_k_in_n..n+3_holds_all_layers": all(
            r["chain_law_k_in_n..n+3"] for r in layer_rows),
        "chain_law_k_in_n..n+3_first_violation": next(
            (r["n"] for r in layer_rows
             if not r["chain_law_k_in_n..n+3"]), None),
        "nonzero_mult3_max_equals_M_1_all_layers": all(
            abs(mult3_max[n] - M[1]) < 1e-9 for n in mult3_max if n >= 2),
        "nonzero_mult3_max_deviation_from_M_1": max(
            (abs(mult3_max[n] - M[1]) for n in mult3_max if n >= 2),
            default=0.0),
        "s3_full_unit_violations": [
            r for r in s3_rows if not r["sampled"] and not r["holds"]],
        "s1_identity_max_err": max(r["max_abs_err"] for r in s1_rows),
        "counterexample_candidate": bool(off_chain_all),
    }
    cert["wall_clock_note"] = "timings are printed to stdout only, not certified"

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("deep_fourier_scan_certificate.json", "w") as f:
        f.write(out + "\n")
    summary = {
        "status": "ok",
        "n_max": n_max,
        "M_n_last": Ms[-1],
        "c_fit_through_origin": cert["decay_fit"]["c_fit_through_origin"],
        "chain_law_holds": cert["kill_criteria_status"][
            "chain_law_k_in_n..n+3_holds_all_layers"],
        "chain_law_first_violation": cert["kill_criteria_status"][
            "chain_law_k_in_n..n+3_first_violation"],
        "chain_k_slope": cert.get("chain_exponent_fit", {}).get(
            "k_over_n_slope"),
        "kc1_fired": cert["kill_criteria_status"]["kc1_fired"],
        "s1_max_err": cert["kill_criteria_status"]["s1_identity_max_err"],
        "peak_chain_k_last": layer_rows[-1]["chain_log_k"],
        "bad_counts_last_layer": {k: v for k, v in layer_rows[-1].items()
                                  if k.startswith("bad_count")},
        "escape_avg_last": layer_rows[-1]["escape_weight_avg_eps0.1"],
        "wall_clock_seconds_total": round(time.time() - t_start, 1),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
