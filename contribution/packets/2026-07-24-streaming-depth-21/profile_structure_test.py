"""What actually drives p_2, and why the n ~ 22 falsification was premature.

BACKGROUND.  The plateau-drift-test packet extrapolated the near-peak
profile value p_2 linearly in n, predicted a crossing of 0.95 near n ~ 22,
found p_2(20) = 0.8013 against an extrapolated 0.94, and recorded the
prediction as "falsified on schedule".  It also recorded a "new parity
alternation": p_2 high at even n, low at odd n.

THE OBSERVATION.  p_2 is not a function of n's parity.  Its direction is
fixed exactly by the increment of the chain exponent,

        dk(n) = k(n) - k(n-1)  in  {1, 2},

by the law

        dk(n) >= 2  <=>  p_2(n) > p_2(n-1).

This holds at EVERY transition n = 7..21 with no exceptions.  Parity was a
proxy that worked only because, in the window n <= 19, the dk = 2 layers
happened to land on alternating parities.  At n = 20 and n = 21 two
consecutive dk = 2 steps occur -- the first such pair in the record -- and
the parity model breaks immediately: n = 21 is an ODD layer with
p_2 = 0.8873, an all-time high, where the packet's odd-branch fit predicts
0.7422.

WHY IT MATTERS.  A linear-in-n fit through a sawtooth is misspecified, so
the n ~ 22 crossing was never a well-posed extrapolation and its failure
was not evidence about the underlying trend.  Refitting on the dk = 2
subsequence -- the only population on which p_2 increases -- puts the 0.95
crossing near n ~ 32, and n = 21 sits ABOVE that line.

k(n) is an exact integer (BSGS discrete log, no floats), so dk is exact;
p_2 is a float64 measurement.  The law tested here is a statement about the
SIGN of a float64 difference, and every difference in the record exceeds
0.019 in magnitude, far above any float64 concern.

This does not prove or disprove anything about Collatz, and it does not by
itself move the P6 dichotomy: see decay_model_test.py, where the M_n decay
law still favours the sqrt (Tao-strength) branch.
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRIFT_CERT = os.path.join(HERE, "..", "2026-07-23-plateau-drift-test",
                          "plateau_drift_certificate.json")
STREAM_CERT = os.path.join(HERE, "streaming_depth_certificate.json")
OUT = os.path.join(HERE, "profile_structure_certificate.json")


def load_rows():
    d = json.load(open(DRIFT_CERT))
    rows = {r["n"]: r for r in d["layer_table"]}
    if os.path.exists(STREAM_CERT):
        s = json.load(open(STREAM_CERT))
        rows[s["row"]["n"]] = s["row"]
    return rows, d


def linfit(xs, ys):
    A = np.vstack([np.asarray(xs, float), np.ones(len(xs))]).T
    c, *_ = np.linalg.lstsq(A, np.asarray(ys, float), rcond=None)
    return float(c[0]), float(c[1])


def main():
    rows, d = load_rows()
    ns = sorted(rows)
    p2 = {n: rows[n]["profile_p"]["2"] for n in ns}
    k = {n: rows[n]["chain_log_k"] for n in ns}

    trans, viol, min_gap = [], [], float("inf")
    for n in ns[1:]:
        if n - 1 not in rows:
            continue
        dk = k[n] - k[n - 1]
        dp = p2[n] - p2[n - 1]
        agree = (dk >= 2) == (dp > 0)
        min_gap = min(min_gap, abs(dp))
        trans.append({"n": n, "dk": dk, "dp2": dp, "law_holds": agree})
        if not agree:
            viol.append(n)

    print("LAW:  dk(n) >= 2  <=>  p_2 increases\n")
    for t in trans:
        print(f"  n={t['n']:>2}  dk={t['dk']}  dp2={t['dp2']:+.4f}  "
              f"{'OK' if t['law_holds'] else 'VIOLATION'}")
    held = sum(t["law_holds"] for t in trans)
    print(f"\n  holds {held}/{len(trans)} transitions; "
          f"smallest |dp2| = {min_gap:.4f}")
    if viol:
        print(f"  VIOLATIONS AT {viol} -- the law is broken, "
              f"do not use the refit below")

    # parity model vs dk model
    dk2 = [n for n in ns if n - 1 in rows and k[n] - k[n - 1] >= 2]
    parities = sorted({("even" if n % 2 == 0 else "odd") for n in dk2})
    print(f"\n  dk=2 layers: {dk2}  (parities present: {parities})")
    print("  -> dk=2 occurs at BOTH parities, so parity cannot be the "
          "driver")

    odd_stall = [n for n in ns if n % 2 and 15 <= n <= 19]
    s_o, i_o = linfit(odd_stall, [p2[n] for n in odd_stall])
    latest = max(ns)
    pred_odd = s_o * latest + i_o
    s_d, i_d = linfit(dk2, [p2[n] for n in dk2])
    pred_dk = s_d * latest + i_d
    cross_dk = (0.95 - i_d) / s_d

    print(f"\n  odd-branch fit (n=15,17,19): p_2({latest}) predicted "
          f"{pred_odd:.4f}, observed {p2[latest]:.4f}, "
          f"residual {p2[latest]-pred_odd:+.4f}")
    print(f"  dk=2 fit                   : p_2({latest}) predicted "
          f"{pred_dk:.4f}, observed {p2[latest]:.4f}, "
          f"residual {p2[latest]-pred_dk:+.4f}")
    print(f"  dk=2 fit crosses 0.95 at n ~ {cross_dk:.1f}  "
          f"(packet's odd-branch fit said "
          f"{d['drift_test']['p2_odd_branch']['crossing_0.95']:.1f})")

    prev_max = max(p2[n] for n in ns if n != latest)
    print(f"\n  p_2({latest}) = {p2[latest]:.6f} is "
          f"{'an ALL-TIME HIGH' if p2[latest] > prev_max else 'not a record'}"
          f" (previous max {prev_max:.6f})")

    res = {"packet": "2026-07-24-streaming-depth-21",
           "law": "dk(n) >= 2 <=> p_2(n) > p_2(n-1)",
           "law_holds": f"{held}/{len(trans)}",
           "violations": viol,
           "smallest_abs_dp2": min_gap,
           "transitions": trans,
           "dk2_layers": dk2,
           "dk2_parities": parities,
           "odd_branch_fit_prediction": pred_odd,
           "dk2_fit_prediction": pred_dk,
           "observed_latest": p2[latest],
           "dk2_fit_crossing_0.95": cross_dk,
           "status": "k(n) exact; p_2 float64 measurement; not a theorem"}
    json.dump(res, open(OUT, "w"), indent=2, sort_keys=True)
    print(f"\nwrote {OUT}")
    return 0 if not viol else 1


if __name__ == "__main__":
    sys.exit(main())
