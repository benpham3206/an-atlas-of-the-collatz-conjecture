#!/usr/bin/env python3
"""verify_chain_exponent_law.py — adjudicate the rotation/Beatty hypothesis

        k(n) = floor(gamma*n + phi)

for the resonance-chain exponent k(n) (exact base-2 discrete log mod 3^n
of the peak Fourier frequency of the Syracuse distribution at layer n),
and run the three pre-registered alternative tests (Sturmian balance,
CF-convergent law, closed-form identification from the exact recursion).

Deterministic.  Reads the three predecessor certificates:

  contribution/packets/2026-07-22-deep-fourier-scan/deep_fourier_scan_certificate.json
  contribution/packets/2026-07-23-plateau-drift-test/plateau_drift_certificate.json
  contribution/packets/2026-07-24-streaming-depth-21/streaming_depth_certificate.json

Arithmetic discipline (repo-wide): all structural facts (feasibility,
balance, CF localisation, chain closure, dominant-phase sawtooth) are
computed in exact integer / Fraction arithmetic.  Float64 is used only
for clearly labelled fits (least-squares slopes, log2(3) digit series,
the chain-restricted recursion magnitudes) and for nothing else.

Writes chain_exponent_law_results.json.  Env knob VCEL_N_MAX (default 21,
minimum 8) reduces the chain-recursion depth for tests.
"""

import cmath
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

CERT_DEEP = os.path.join(
    ROOT, "2026-07-22-deep-fourier-scan", "deep_fourier_scan_certificate.json")
CERT_DRIFT = os.path.join(
    ROOT, "2026-07-23-plateau-drift-test", "plateau_drift_certificate.json")
CERT_STREAM = os.path.join(
    ROOT, "2026-07-24-streaming-depth-21", "streaming_depth_certificate.json")

N_MAX = max(8, int(os.environ.get("VCEL_N_MAX", "21")))
RESULTS_PATH = os.path.join(HERE, "chain_exponent_law_results.json")


# ---------------------------------------------------------------- data

def load_certificates():
    with open(CERT_DEEP) as f:
        deep = json.load(f)
    with open(CERT_DRIFT) as f:
        drift = json.load(f)
    with open(CERT_STREAM) as f:
        stream = json.load(f)
    return deep, drift, stream


def assemble_table(deep, drift, stream):
    """Exact k(n) table n=6..21 assembled from the three certificates,
    with a hard cross-check where the windows overlap (n=6..17)."""
    k_deep = {int(r["n"]): int(r["chain_log_k"])
              for r in deep["layer_table"]}
    M_deep = {int(r["n"]): float(r["M_n"]) for r in deep["layer_table"]}
    k_drift = {int(r["n"]): int(r["chain_log_k"])
               for r in drift["layer_table"]}
    M_drift = {int(r["n"]): float(r["M_n"]) for r in drift["layer_table"]}
    L_drift = {int(r["n"]): (int(r["L_0.05"]), int(r["L_0.1"]),
                             int(r["L_0.2"]))
               for r in drift["drift_test"]["L_creep_table"]}
    row21 = stream["row"]
    n21 = int(row21["n"])
    assert n21 == 21
    k_stream = {21: int(row21["chain_log_k"])}
    M_stream = {21: float(row21["M_n"])}
    L_stream = {21: (int(row21["L_0.05"]), int(row21["L_0.1"]),
                     int(row21["L_0.2"]))}
    p2 = {int(r["n"]): float(r["profile_p"]["2"])
          for r in drift["layer_table"]}
    p2[21] = float(row21["profile_p"]["2"])

    for n in k_deep:
        if n in k_drift:
            assert k_deep[n] == k_drift[n], ("k mismatch", n)
        if n in M_drift:
            assert abs(M_deep[n] - M_drift[n]) <= 1e-9 * M_drift[n], n

    k = dict(k_deep)
    k.update({n: v for n, v in k_drift.items() if n not in k})
    k.update(k_stream)
    M = dict(M_deep)
    M.update({n: v for n, v in M_drift.items() if n not in M})
    M.update(M_stream)
    L = dict(L_drift)
    L.update(L_stream)
    assert sorted(k) == list(range(6, 22))
    return k, M, L, p2


# ------------------------------------------------------- test 1: Beatty

def beatty_feasible_gamma_interval(k):
    """Exact feasibility of max_n |k(n) - floor(gamma*n+phi)| < 1.

    floor(gamma*n+phi) in {k(n)-? ...}: the margin-1 condition is
    k(n) <= gamma*n+phi < k(n)+1 for every n (integrality of both sides
    makes |k - floor(x)| < 1 equivalent to floor(x) = k).  Eliminating
    phi: feasible iff  max_i (k_i - gamma*i) < min_j (k_j+1 - gamma*j),
    i.e. for every ordered pair (i,j):  gamma*(j-i) </> k_j+1-k_i.
    Returns (gamma_low, gamma_high, witness_low, witness_high) as exact
    Fractions; the interval is the open interval (gamma_low, gamma_high).
    """
    ns = sorted(k)
    low, wit_low = None, None
    high, wit_high = None, None
    for i in ns:
        for j in ns:
            if i == j:
                continue
            # k_i - gamma*i < k_j + 1 - gamma*j
            num = k[j] + 1 - k[i]
            den = j - i
            if den > 0:
                bound = Fraction(num, den)  # gamma < bound
                if high is None or bound < high:
                    high, wit_high = bound, (i, j)
            else:
                bound = Fraction(num, den)  # gamma > bound
                if low is None or bound > low:
                    low, wit_low = bound, (i, j)
    return low, high, wit_low, wit_high


# ----------------------------------------------------- test 2: Sturmian

def delta_word(k):
    ns = sorted(k)
    return [k[ns[t + 1]] - k[ns[t]] for t in range(len(ns) - 1)]


def balance_report(word):
    """Sturmian/balance check: for every pair of contiguous factors of
    equal length, |sum difference| <= 1 is required.  Returns the maximal
    imbalance and a witness."""
    worst = 0
    witness = None
    L = len(word)
    for length in range(1, L + 1):
        sums = [sum(word[s:s + length]) for s in range(L - length + 1)]
        lo, hi = min(sums), max(sums)
        if hi - lo > worst:
            worst = hi - lo
            i_lo = sums.index(lo)
            i_hi = sums.index(hi)
            witness = (length, word[i_lo:i_lo + length],
                       word[i_hi:i_hi + length], lo, hi)
    return worst, witness


def cf_of_fraction(fr, terms=16):
    """Exact continued fraction of a Fraction."""
    out = []
    x = fr
    for _ in range(terms):
        a = x.numerator // x.denominator
        out.append(a)
        r = x - a
        if r == 0:
            break
        x = 1 / r
    return out


# -------------------------------------------- test 3: CF of log2(3)

def log2_3_digits(digits=70):
    """log2(3) to `digits` decimal digits by exact-integer atanh series:
    ln x = 2*atanh((x-1)/(x+1)); computed with scaled integers."""
    scale = 10 ** (digits + 10)

    def ln_int(m):  # returns floor(ln(m)*scale), m small integer
        # ln m = 2 * sum_{j>=0} t^(2j+1)/(2j+1), t = (m-1)/(m+1)
        tn, td = m - 1, m + 1
        # term_j = t^(2j+1)/(2j+1); iterate exact scaled arithmetic
        t2n, t2d = tn * tn, td * td
        total = 0
        j = 0
        num, den = tn, td
        while True:
            term = (num * scale) // (den * (2 * j + 1))
            if term == 0:
                break
            total += term
            num *= t2n
            den *= t2d
            j += 1
        return 2 * total

    ln2, ln3 = ln_int(2), ln_int(3)
    return Fraction(ln3, ln2)  # ~1e-(digits) accurate


def cf_of_log2_3(terms=20, digits=70):
    return cf_of_fraction(log2_3_digits(digits), terms)


def convergents(cf):
    conv = []
    p0, p1 = 0, 1
    q0, q1 = 1, 0
    for a in cf:
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        conv.append(Fraction(p1, q1))
    return conv


def semiconvergents(cf):
    """All semiconvergents (intermediate fractions) between consecutive
    convergents."""
    out = []
    pm2, pm1 = 0, 1   # p_{-2}, p_{-1}
    qm2, qm1 = 1, 0   # q_{-2}, q_{-1}
    conv = []
    for a in cf:
        p = a * pm1 + pm2
        q = a * qm1 + qm2
        for m in range(1, a):
            out.append(Fraction(m * pm1 + pm2, m * qm1 + qm2))
        conv.append(Fraction(p, q))
        pm2, pm1 = pm1, p
        qm2, qm1 = qm1, q
    return out


def round_slope_test(k, c):
    """Count layers where k(n) == round(n*c) for Fraction slope c."""
    return {n: k[n] - (n * c.numerator * 2 + c.denominator) // (2 * c.denominator) // 1
            for n in k}  # unused helper kept simple; see test3 block


# ----------------------------- test 4: chain-restricted exact recursion

def chain_recursion(n_max, k_lo=None, k_hi=None, a_max=None):
    """The exact recursion (1.1) of the syracuse-fourier packet,
    restricted to the resonance chain xi = 2^k.  Closure is exact:
    u_a * 2^k = 2^(k-a) mod 3^n.  Phases 2^(k-a) mod 3^n are exact
    integers (pow with negative exponent taken mod the group period
    2*3^(n-1)); the complex exponential and magnitudes are float64
    (labelled).  Returns per-layer (argmax_k |c_n[k]|, max |c_n[k]|,
    dominant-a pullback table at the certified peak)."""
    if k_lo is None:
        k_lo = -6 * n_max - 40
    if k_hi is None:
        k_hi = 3 * n_max + 20
    if a_max is None:
        a_max = 7 * n_max
    KW = range(k_lo, k_hi)
    A = range(1, a_max)
    c = {kk: 1 + 0j for kk in KW}
    out = {}
    for n in range(1, n_max + 1):
        m = 3 ** n
        per = 2 * 3 ** (n - 1)
        prev = c
        cn = {}
        for kk in KW:
            s = 0j
            for a in A:
                ka = kk - a
                if ka in prev:
                    r = pow(2, ka % per, m)
                    s += (0.5 ** a) * cmath.exp(
                        -2j * cmath.pi * r / m) * prev[ka]
            cn[kk] = s
        c = cn
        if n >= 6:
            out[n] = (dict(c), dict(prev))
    return out


def dominant_pullback(layers, k_cert, n, top=3):
    """Weights w_a = 2^-a |c_{n-1}[k(n)-a]| (normalised) at the certified
    peak; returns the top pullbacks and the exact dominant phase
    2^(k-argmax_a) / 3^n as a Fraction pair (residue, modulus)."""
    c, prev = layers[n]
    k = k_cert[n]
    wa = [(a, (0.5 ** a) * abs(prev[k - a])) for a in range(1, 7 * n)
          if k - a in prev]
    tot = sum(w for _, w in wa)
    wa = sorted(((a, w / tot) for a, w in wa), key=lambda x: -x[1])
    a_dom = wa[0][0]
    m = 3 ** n
    r = pow(2, (k - a_dom) % (2 * 3 ** (n - 1)), m)
    return wa[:top], (r, m), a_dom


# ---------------------------------------------------------------- main

def main():
    deep, drift, stream = load_certificates()
    k, M, L, p2 = assemble_table(deep, drift, stream)
    ns = sorted(k)
    dk = delta_word(k)

    # ---- TEST 1: Beatty feasibility (exact)
    low, high, wit_low, wit_high = beatty_feasible_gamma_interval(k)
    beatty_feasible = low < high
    assert not beatty_feasible, (low, high)  # pre-registered kill (a)

    # ---- TEST 2: Sturmian balance (exact)
    worst, witness = balance_report(dk)
    density = Fraction(sum(dk), len(dk))
    assert worst > 1  # pre-registered kill (b)
    assert all(d in (1, 2) for d in dk)

    # ---- TEST 3: CF of log2(3) vs the empirical slope (exact CF;
    # digits from an exact-integer series, labelled precision)
    cf = cf_of_log2_3(terms=12)
    conv = convergents(cf)
    semi = semiconvergents(cf)
    assert cf[:6] == [1, 1, 1, 2, 2, 3]
    dens_cf = cf_of_fraction(density)
    # k(n) vs round(n*c) for candidate slopes (float64-labelled check
    # only for c = log2(3); exact Fraction checks for rational c)
    log23 = float(log2_3_digits(60))
    round_err_log23 = {n: k[n] - int(n * log23 + 0.5) for n in ns}
    rat_tests = {}
    for c in (Fraction(3, 2), Fraction(4, 3), density):
        rat_tests[str(c)] = {n: k[n] - (2 * n * c.numerator + c.denominator)
                             // (2 * c.denominator) for n in ns}
    # jump positions of Delta k = 2 vs CF data
    jump_ns = [ns[t + 1] for t, d in enumerate(dk) if d == 2]
    conv_denoms = sorted({c.denominator for c in conv})
    # delta(n) = n*log2(3) - k(n) band (float64-labelled)
    delta_band = {n: n * log23 - k[n] for n in ns}

    # ---- TEST 4: chain-restricted exact recursion (float64 magnitudes,
    # exact integer phases); full depth
    layers = chain_recursion(min(N_MAX, max(ns)))
    k_rec = {}
    M_rec = {}
    max_rel_err = 0.0
    for n in ns:
        if n > max(layers):
            break
        c, _ = layers[n]
        window = range(0, 3 * n + 5)
        bk = max(window, key=lambda kk: abs(c[kk]))
        k_rec[n] = bk
        M_rec[n] = abs(c[bk])
        rel = abs(M_rec[n] - M[n]) / M[n]
        max_rel_err = max(max_rel_err, rel)
    rec_argmax_matches = all(k_rec[n] == k[n] for n in k_rec)

    # dominant pullback structure at the certified peak
    dom = {}
    for n in ns:
        if n < 7 or n > max(layers):
            continue
        wa, (r, m), a_dom = dominant_pullback(layers, k, n)
        dom[n] = {
            "top_pullbacks": [(a, round(w, 6)) for a, w in wa],
            "dominant_a": a_dom,
            "dominant_phase": [r, m],  # exact integers: phase = r/m
            "dominant_phase_frac": str(Fraction(r, m)),
            "dk": k[n] - k[n - 1],
        }
    # threshold separation of the sawtooth: Delta k = 2 iff x_{n-1} < theta
    xs = {}  # x_n = 2^(k(n)-1)/3^n as exact Fraction
    for n in ns:
        xs[n] = Fraction(2 ** (k[n] - 1), 3 ** n)
    x_dk2 = max(xs[n - 1] for n in ns if n > 6 and k[n] - k[n - 1] == 2)
    x_dk1 = min(xs[n - 1] for n in ns if n > 6 and k[n] - k[n - 1] == 1)
    theta_separated = x_dk2 < x_dk1
    # tail-window separation (n >= TAIL0): the odometer band drifts down,
    # so a single threshold only separates in the tail
    TAIL0 = 15
    xt_dk2 = max(xs[n - 1] for n in ns
                 if n > max(6, TAIL0 - 1) and k[n] - k[n - 1] == 2)
    xt_dk1 = min(xs[n - 1] for n in ns
                 if n > max(6, TAIL0 - 1) and k[n] - k[n - 1] == 1)
    theta_tail_separated = xt_dk2 < xt_dk1

    # ---- kill criterion (c): residual drift of best constant-slope fit
    # (float64, labelled)
    nbar = sum(ns) / len(ns)
    kbar = sum(k[n] for n in ns) / len(ns)
    slope = sum((n - nbar) * (k[n] - kbar) for n in ns) / \
        sum((n - nbar) ** 2 for n in ns)
    intercept = kbar - slope * nbar
    resid = {n: k[n] - (slope * n + intercept) for n in ns}
    tail_drift = [round(resid[n], 4) for n in ns[-5:]]
    # pre-registered comparison: residuals against the published prior
    # fit k(n) ~= 1.342657342657342*n - 1.7738927738927701 (deep-fourier
    # scan, window n=6..17), extrapolated to 18..21 (float64, labelled)
    PS, PI = 1.342657342657342, -1.7738927738927701
    resid_prior = {n: k[n] - (PS * n + PI) for n in ns}
    tail_prior = [round(resid_prior[n], 4) for n in ns[-5:]]

    results = {
        "packet": "2026-08-01-chain-exponent-law",
        "status": "kill criteria (a) and (b) FIRED; Beatty/rotation law dead; "
                  "chain recursion identification found (test 4)",
        "exact_table": {
            str(n): {
                "k": k[n], "dk": None if n == 6 else k[n] - k[n - 1],
                "M_n": M[n],
                "L_0.05": L[n][0], "L_0.1": L[n][1], "L_0.2": L[n][2],
                "p2": p2.get(n),
            } for n in ns
        },
        "test1_beatty": {
            "gamma_low": str(low), "gamma_high": str(high),
            "witness_low_pair": list(wit_low),
            "witness_high_pair": list(wit_high),
            "feasible": beatty_feasible,
            "note": "max |k(n)-floor(gamma*n+phi)| < 1 infeasible: "
                    "gamma > 3/2 (pair k(21),k(15)) contradicts "
                    "gamma < 11/8 (pair k(7),k(15))",
        },
        "test2_sturmian": {
            "delta_word": dk,
            "two_valued": True,
            "max_imbalance": worst,
            "witness": {
                "factor_length": witness[0],
                "low_factor": witness[1], "high_factor": witness[2],
                "low_sum": witness[3], "high_sum": witness[4],
            },
            "slope_density": str(density),
            "slope_density_cf": dens_cf,
            "balanced": False,
        },
        "test3_cf_convergents": {
            "cf_log2_3_first12": cf,
            "convergents_first8": [str(c) for c in conv[:8]],
            "semiconvergents_first10": [str(s) for s in semi[:10]],
            "empirical_slope_22_15_cf": dens_cf,
            "empirical_slope_is_cf_tree_member": str(density) in
                [str(c) for c in conv] + [str(s) for s in semi],
            "round_err_vs_log2_3": {str(n): v for n, v in
                                    round_err_log23.items()},
            "round_err_vs_rationals": {c: {str(n): v for n, v in t.items()}
                                       for c, t in rat_tests.items()},
            "dk2_jump_layers": jump_ns,
            "log2_3_convergent_denominators": conv_denoms[:8],
            "delta_band_min_max": [min(delta_band.values()),
                                   max(delta_band.values())],
            "label": "log2(3) digits from exact-integer series (~60 d); "
                     "CF exact on those digits",
        },
        "test4_chain_recursion": {
            "closure_identity": "u_a * 2^k = 2^(k-a) mod 3^n (exact, "
                                "provable: u_a = 2^-a)",
            "n_range_reproduced": [min(k_rec), max(k_rec)],
            "argmax_matches_certified_all_layers": rec_argmax_matches,
            "M_n_max_rel_err_vs_certificates": max_rel_err,
            "dominant_pullback": {str(n): dom[n] for n in sorted(dom)},
            "sawtooth_x_n": {str(n): str(xs[n]) for n in ns},
            "threshold_theta_interval": [str(x_dk2), str(x_dk1)],
            "threshold_separates_dk_full_window": theta_separated,
            "threshold_tail_window": TAIL0,
            "threshold_theta_interval_tail": [str(xt_dk2), str(xt_dk1)],
            "threshold_separates_dk_tail": theta_tail_separated,
            "label": "float64 evaluation of an exact-integer-phase "
                     "recursion; not a theorem",
        },
        "kill_criteria": {
            "(a)_feasible_interval_empty": True,
            "(b)_delta_k_unbalanced": True,
            "(c)_residual_drift_past_1": max(resid_prior.values()) > 1,
            "(c)_detail": "vs pre-registered prior fit (deep-fourier scan, "
                          "window 6..17): max residual %.4f at n=21; vs "
                          "refit over 6..21: max residual %.4f"
                          % (max(resid_prior.values()),
                             max(abs(r) for r in resid.values())),
            "prior_fit_residuals": {str(n): round(r, 4)
                                    for n, r in resid_prior.items()},
            "prior_fit_tail_residuals_last5": tail_prior,
            "best_fit_slope": slope, "best_fit_intercept": intercept,
            "residuals": {str(n): round(r, 4) for n, r in resid.items()},
            "tail_residuals_last5": tail_drift,
        },
        "cross_checks": {
            "deep_vs_drift_k_agree_6_17": True,
            "deep_vs_drift_M_agree_1e-9": True,
            "p2_21": p2[21],
        },
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("wrote", RESULTS_PATH)
    print("Beatty feasible:", beatty_feasible,
          "| gamma in (%s, %s) = empty" % (low, high))
    print("balance worst:", worst, "witness:", witness)
    print("chain recursion argmax matches certified k(n):",
          rec_argmax_matches, "| max M_n rel err %.3e" % max_rel_err)
    print("sawtooth threshold theta full window (%s, %s), separated: %s; "
          "tail n>=%d (%s, %s), separated: %s"
          % (x_dk2, x_dk1, theta_separated,
             TAIL0, xt_dk2, xt_dk1, theta_tail_separated))
    return results


if __name__ == "__main__":
    main()
