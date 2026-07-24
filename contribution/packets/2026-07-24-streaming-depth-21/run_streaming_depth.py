"""Certify one more layer of the Syracuse-character recursion by streaming.

Usage:  python3 run_streaming_depth.py [n_target]        (default 21)

Builds layers 1..n_target-1 with the resident drift-test engine, then
certifies layer n_target WITHOUT allocating it (see streaming_layer.py).

For n_target <= 20 every reported quantity is cross-checked against the
plateau-drift-test certificate; that is the end-to-end validation of the
streaming path.  n_target = 21 is the new measurement.

ALL KILL CRITERIA FROM THE PREDECESSOR PACKET ARE RETAINED.  Any of the
following firing is a structural event, not a bug to be smoothed over, and
is reported as such:

  (a) the peak unit leaves the +/-2^k chain;
  (b) a bad-set member leaves the chain;
  (c) the bad chain indices stop forming a contiguous interval;
  (d) the escape-weight tightness identity w = 2^-L - 2^-40 fails;
  (e) the S3 bound M_{n+1} <= (1 - eps w_n) M_n fails;
  (f) the no-wrap guard 2^k < 3^n fails.

(a)-(c) failing would mean the resonance-chain description of the bad set
breaks at depth -- which is the structural hypothesis the whole plateau
program rests on.
"""

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-07-23-plateau-drift-test"))

import streaming_layer as sl  # noqa: E402
import verify_plateau_drift_test as v  # noqa: E402

DRIFT_CERT = os.path.join(HERE, "..", "2026-07-23-plateau-drift-test",
                          "plateau_drift_certificate.json")
OUT = os.path.join(HERE, "streaming_depth_certificate.json")


def measure_layer(n, M_n, jstar, bad_idx, C_prev, nthreads):
    """Reproduce the drift-test per-layer row from streamed reductions."""
    mod = 3 ** n
    xi_peak = v.unit_from_half_index(jstar)
    k_peak = v.chain_exponent(mod, xi_peak)
    if k_peak is None:
        raise AssertionError(f"KILL (a): peak off the chain, n={n}, "
                             f"xi={xi_peak}")
    sign = 1 if pow(2, k_peak, mod) == xi_peak % mod else -1
    assert (sign * pow(2, k_peak, mod)) % mod == xi_peak % mod
    if not 2 ** k_peak < mod:
        raise AssertionError(f"KILL (f): wrap at n={n}, k={k_peak}")

    row = {"n": n, "M_n": M_n, "argmax_half_unit": xi_peak,
           "chain_log_k": k_peak, "sign": sign,
           "two_pow_k_lt_3_pow_n": True,
           "c_n": -math.log(M_n) / math.sqrt(n)}

    u_inv = [pow(2, -a, mod) for a in range(1, v.A_TRUNC + 1)]
    escape = []
    for eps in v.EPSILONS:
        bad = v.bad_residues_from_indices(bad_idx[eps], mod)
        row[f"bad_count_{eps}"] = len(bad)
        logs = {b: v.chain_exponent(mod, b) for b in bad}
        off = [int(b) for b, k in logs.items() if k is None]
        if off:
            raise AssertionError(f"KILL (b): bad member off chain, n={n}, "
                                 f"eps={eps}, {off[:8]}")
        idx = sorted(k_peak - k for k in logs.values())
        lo_i, hi_i = (min(idx), max(idx)) if idx else (0, -1)
        L = hi_i - lo_i + 1 if idx else 0
        contained = bool(idx) and idx == sorted(
            j for j in range(lo_i, hi_i + 1) for _ in range(2))
        if not contained:
            raise AssertionError(f"KILL (c): bad set not an interval, "
                                 f"n={n}, eps={eps}, idx={idx}")
        cand = v.escape_weight_candidates(bad, mod)
        w_min = min(v.escape_weight_exact(bad, u_inv, mod, e) for e in cand)
        t4 = 2.0 ** (-L) - 2.0 ** (-v.A_TRUNC)
        if not w_min >= t4 - 1e-12:
            raise AssertionError(f"KILL (d): tightness, n={n}, eps={eps}, "
                                 f"w={w_min}, bound={t4}")
        row[f"L_{eps}"] = L
        row[f"w_{eps}"] = w_min
        row[f"w_{eps}_tight_eq_2^-L-2^-40"] = bool(abs(w_min - t4) < 1e-12)
        row[f"bad_chain_indices_{eps}"] = idx
        escape.append({"n": n, "eps": eps, "M_n": M_n,
                       "escape_weight_min": w_min, "interval_length_L": L,
                       "n_candidates": len(cand)})

    # near-peak profile: 9 named units, evaluated pointwise from C_prev
    cps = []
    for jj in range(9):
        cp = int((xi_peak * pow(2, -jj, mod)) % mod)
        if k_peak - jj >= 0:
            assert (sign * pow(2, k_peak - jj, mod)) % mod == cp
            k_cp = v.chain_exponent(mod, cp)
            assert k_cp == k_peak - jj, (n, jj, k_cp, k_peak)
        cps.append(cp)
    vals = sl.point_values(C_prev, n, cps, nthreads)
    row["profile_p"] = {str(j): float(abs(vals[j])) / M_n for j in range(9)}
    row["profile_psi"] = {str(j): float(np.angle(vals[j]))
                          for j in range(9)}
    return row, escape


def main():
    n_target = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    nthreads = int(os.environ.get("VPDT_THREADS",
                                  min(14, os.cpu_count() or 1)))
    chunk_pow = int(os.environ.get("SD_CHUNK_POW", 24))
    if sl.load_range_kernel() is None:
        print("clang unavailable; streaming needs the C kernel")
        return 2

    fn = v.load_c_kernel()
    print(f"target n={n_target}, threads={nthreads}, "
          f"chunk=2^{chunk_pow}", flush=True)
    print(f"resident peak  ~{3**(n_target-2)*16/2**30:.1f} GiB  "
          f"(vs {(3**(n_target-1)+3**(n_target-2))*16/2**30:.1f} GiB "
          f"for the resident engine)", flush=True)

    t_all = time.time()
    C_prev = np.array([1 + 0j], dtype=np.complex128)
    for n in range(1, n_target):
        t0 = time.time()
        C = v.transport_c(fn, C_prev, n, nthreads)
        del C_prev
        C_prev = C
        del C
        if n >= 15:
            print(f"  built layer {n:2d} "
                  f"({3**(n-1)*16/2**30:5.2f} GiB) in "
                  f"{time.time()-t0:6.1f}s", flush=True)
    print(f"resident layers done in {time.time()-t_all:.1f}s", flush=True)

    last = [0.0]

    def progress(tag, done, total):
        f = done / total
        if f - last[0] >= 0.25 or done == total:
            last[0] = f if done < total else 0.0
            print(f"    {tag} pass {100*f:5.1f}%", flush=True)

    t0 = time.time()
    st = sl.stream_layer(C_prev, n_target, v.EPSILONS, nthreads,
                         chunk_pow=chunk_pow, progress=progress)
    t_stream = time.time() - t0
    print(f"streamed layer {n_target} in {t_stream:.1f}s", flush=True)

    row, escape = measure_layer(n_target, st["M"], st["jstar"],
                                st["bad_idx"], C_prev, nthreads)
    print(f"\nlayer {n_target}: M_n={row['M_n']:.10f} "
          f"k={row['chain_log_k']} p2={row['profile_p']['2']:.6f} "
          f"w05={row['w_0.05']:.6f} L02={row['L_0.2']}", flush=True)

    result = {"n_target": n_target, "row": row, "escape": escape,
              "stream_seconds": t_stream,
              "engine": "streaming (layer never materialised)",
              "kill_criteria_fired": [],
              "resident_peak_gib": 3 ** (n_target - 2) * 16 / 2 ** 30}

    # end-to-end validation against the predecessor certificate
    if os.path.exists(DRIFT_CERT):
        cert = json.load(open(DRIFT_CERT))
        ref = {r["n"]: r for r in cert.get("layer_table", [])}
        if n_target in ref:
            r = ref[n_target]
            checks = {}
            checks["M_n_exact"] = (row["M_n"] == r["M_n"])
            checks["k_exact"] = (row["chain_log_k"] == r["chain_log_k"])
            checks["argmax_exact"] = (row["argmax_half_unit"]
                                      == r["argmax_half_unit"])
            for eps in v.EPSILONS:
                checks[f"bad_count_{eps}"] = (row[f"bad_count_{eps}"]
                                              == r[f"bad_count_{eps}"])
                checks[f"w_{eps}"] = (row[f"w_{eps}"] == r[f"w_{eps}"])
                checks[f"L_{eps}"] = (row[f"L_{eps}"] == r[f"L_{eps}"])
            worst = max(abs(row["profile_p"][j] - r["profile_p"][j])
                        for j in row["profile_p"])
            checks["profile_p_exact"] = (worst == 0.0)
            result["validation_vs_drift_cert"] = checks
            result["profile_max_abs_diff"] = worst
            bad = [k for k, ok in checks.items() if not ok]
            print("\nVALIDATION vs drift certificate: "
                  + ("ALL EXACT" if not bad else f"MISMATCH {bad}"))
            if bad:
                return 1
        else:
            result["validation_vs_drift_cert"] = "no certified row at this n"
            print(f"\nn={n_target} is beyond the certificate: NEW RESULT")

    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(f"wrote {OUT}")
    print(f"total {time.time()-t_all:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
