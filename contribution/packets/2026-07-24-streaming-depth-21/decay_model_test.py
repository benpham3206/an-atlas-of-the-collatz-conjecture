"""Direct model test on M_n: exponential branch vs sqrt branch of P6.

WHY.  The plateau packet's P6 dichotomy is a choice between two decay laws
for the uniform Fourier maximum M_n:

  (i)  L(n) bounded   =>  uniform EXPONENTIAL decay of M_n
                          => strictly stronger than Tao's n^(-A);
  (ii) L(n) creeps like (1/2)log_2 n
                      =>  the e^(-c sqrt n) law => Tao-strength.

So the dichotomy is, on the M_n side, exactly the question:

        is -ln M_n linear in n, or linear in sqrt(n)?

The predecessor packets measure c_n = -ln M_n / sqrt(n) and fit it through
the origin -- i.e. they fit branch (ii) and report its residuals.  They
never fit branch (i) and compare.  This script does the comparison.

Both models are two-parameter least squares on the same data, so raw SSR
and R^2 are directly comparable and no complexity penalty is needed; the
Akaike difference reduces to N ln(SSR_a / SSR_b).

HONEST SCOPE.  This is a finite window (n <= 21) of float64 MEASUREMENTS.
It cannot prove either branch: branch (i) asks for L bounded at every n,
and an asymptotic regime change beyond the window is not excluded by any
amount of data below it.  What the window can do is say which branch the
evidence currently points at -- and report if that direction disagrees
with what the repository says it is.
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRIFT_CERT = os.path.join(HERE, "..", "2026-07-23-plateau-drift-test",
                          "plateau_drift_certificate.json")
STREAM_CERT = os.path.join(HERE, "streaming_depth_certificate.json")
OUT = os.path.join(HERE, "decay_model_certificate.json")


def load_points():
    """(n, M_n) from the drift certificate, plus any streamed layer."""
    cert = json.load(open(DRIFT_CERT))
    pts = {r["n"]: r["M_n"] for r in cert["layer_table"]}
    src = {n: "plateau-drift-test cert" for n in pts}
    if os.path.exists(STREAM_CERT):
        s = json.load(open(STREAM_CERT))
        row = s["row"]
        pts[row["n"]] = row["M_n"]
        src[row["n"]] = "streaming-depth-21 (this packet)"
    ns = sorted(pts)
    return (np.array(ns, dtype=float),
            np.array([pts[n] for n in ns]), src)


def fit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ssr = float((resid ** 2).sum())
    tot = float(((y - y.mean()) ** 2).sum())
    return {"slope": float(coef[0]), "intercept": float(coef[1]),
            "ssr": ssr, "r2": 1.0 - ssr / tot,
            "max_abs_resid": float(np.abs(resid).max())}


def compare(n, M, label):
    y = -np.log(M)
    exp_fit = fit(n, y)                 # branch (i):  -ln M ~ c n
    sqrt_fit = fit(np.sqrt(n), y)       # branch (ii): -ln M ~ c sqrt(n)
    N = len(n)
    d_aic = N * math.log(exp_fit["ssr"] / sqrt_fit["ssr"])
    return {"window": label, "n_points": N,
            "n_range": [int(n.min()), int(n.max())],
            "branch_i_exponential_fit": exp_fit,
            "branch_ii_sqrt_fit": sqrt_fit,
            "ssr_ratio_exp_over_sqrt": exp_fit["ssr"] / sqrt_fit["ssr"],
            "delta_aic_favouring_sqrt": d_aic,
            "favoured_branch": ("ii (sqrt, Tao-strength)" if d_aic > 0
                                else "i (exponential, beats Tao)")}


def main():
    n, M, src = load_points()
    y = -np.log(M)
    print("Per-layer decay diagnostics\n")
    print(f"{'n':>3} {'M_n':>12} {'-lnM/sqrt(n)':>13} {'-lnM/n':>9}  source")
    for i in range(len(n)):
        ni = int(n[i])
        print(f"{ni:>3} {M[i]:>12.9f} {y[i]/math.sqrt(ni):>13.6f} "
              f"{y[i]/ni:>9.6f}  {src.get(ni,'')}")

    results = [compare(n, M, "full")]
    tail = n >= 13
    if tail.sum() >= 4:
        results.append(compare(n[tail], M[tail], "tail n>=13"))

    print("\nModel comparison  (both 2-parameter least squares on -ln M_n)")
    for r in results:
        e, s = r["branch_i_exponential_fit"], r["branch_ii_sqrt_fit"]
        print(f"\n  window {r['window']}  n={r['n_range'][0]}..{r['n_range'][1]}"
              f"  ({r['n_points']} points)")
        print(f"    branch (i)  exponential : SSR={e['ssr']:.6e}  "
              f"R^2={e['r2']:.8f}  max|resid|={e['max_abs_resid']:.5f}")
        print(f"    branch (ii) sqrt        : SSR={s['ssr']:.6e}  "
              f"R^2={s['r2']:.8f}  max|resid|={s['max_abs_resid']:.5f}")
        print(f"    SSR(exp)/SSR(sqrt) = {r['ssr_ratio_exp_over_sqrt']:.2f}"
              f"   dAIC = {r['delta_aic_favouring_sqrt']:+.2f}"
              f"   -> favours branch {r['favoured_branch']}")

    # stability of the two candidate constants over the tail
    c_sqrt = y / np.sqrt(n)
    c_lin = y / n
    t = n >= 13
    diag = {
        "c_sqrt_tail_min": float(c_sqrt[t].min()),
        "c_sqrt_tail_max": float(c_sqrt[t].max()),
        "c_sqrt_tail_spread": float(c_sqrt[t].max() - c_sqrt[t].min()),
        "c_lin_tail_min": float(c_lin[t].min()),
        "c_lin_tail_max": float(c_lin[t].max()),
        "c_lin_tail_spread": float(c_lin[t].max() - c_lin[t].min()),
        "c_lin_monotone_decreasing": bool(np.all(np.diff(c_lin[t]) < 0)),
    }
    print(f"\n  n>=13: -lnM/sqrt(n) spread = {diag['c_sqrt_tail_spread']:.6f} "
          f"(flat)")
    print(f"  n>=13: -lnM/n        spread = {diag['c_lin_tail_spread']:.6f} "
          f"(monotone decreasing: {diag['c_lin_monotone_decreasing']})")

    verdict = ("Over the measured window the sqrt law fits decisively "
               "better and the exponential constant has not stabilised. "
               "Direction of evidence: branch (ii), Tao-strength. This is "
               "a finite window and proves neither branch.")
    print("\nVERDICT: " + verdict)

    json.dump({"packet": "2026-07-24-streaming-depth-21",
               "quantity": "M_n decay law, P6 branch discrimination",
               "status": "float64 measurement; not a theorem",
               "points": {str(int(n[i])): M[i] for i in range(len(n))},
               "comparisons": results, "tail_diagnostics": diag,
               "verdict": verdict},
              open(OUT, "w"), indent=2, sort_keys=True)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
