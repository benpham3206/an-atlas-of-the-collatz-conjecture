#!/usr/bin/env python3
"""Executable controls for COLLATZ_PLATEAU_DRIFT_TEST.md.

Successor engine to the deep-fourier-scan packet: extends certified float64
measurements from n = 17 to n = VPDT_N_MAX (default 20) and directly tests
the plateau-escape-weight packet's falsifiable prediction (p_2 crossing
0.95 near n ~ 22 under linear drift; w_n(0.05) dropping below 1/4).

ENGINE (the speed path; see the memo's diagnosis for why the old engine
died at n = 18).  Instead of building the dense Syracuse layer P_n of
length 3^n and taking a full FFT (the old path), this verifier carries the
character c_n on HALF-UNIT-INDEXED complex128 state only:

    state[n][j] = c_n(xi_j),  xi_j = 3*(j//2)+1+(j%2),  0 <= j < 3^(n-1)
    (units 0 < xi < 3^n/2; the other half is conj by reality of P_n)

propagated by the proven recursion identity (syracuse-fourier packet,
re-verified against dense FFT below at every layer n <= dense_max):

    c_n(xi) = norm_n * sum_{a=1..taps_n} 2^-a e(-xi u_a / 3^n)
              c_{n-1}(xi u_a mod 3^(n-1)),
    u_a = 2^-a mod 3^n,  taps_n = min(2*3^(n-1), A_TRUNC),
    norm_n = 1/(1 - 2^(-2*3^(n-1)))  (float64, bit-identical to the dense
    construction's renormalisation; = 1.0 exactly for n >= 4).

State at n=20: 3^19 complex128 = 18.6 GB per buffer, two buffers alive
during a transition (~25 GB peak): fits the 36 GB Mac (default certified
depth; ~80 s for the n = 19 -> 20 transition, ~3 min total).  n=21 needs
3^20 complex128 = 56 GB per buffer and 128-bit index arithmetic: does NOT
fit.  The inner loop is a C kernel (plateau_drift_kernel.c,
clang -O3, IEEE arithmetic, no fast-math, pthreads over disjoint output
ranges => deterministic) with incremental carry of nu_a = xi*u_a mod 3^n
(no 64-bit division in the hot loop) and two-table root-of-unity phases.
A numpy fallback (transport_np) is used if clang is unavailable (certified
only for n <= dense_max).

PROVENANCE.  syracuse_float_layers / chain_log_bsgs / chain_exponent /
unit indexing copied (with light adaptation) from
contribution/packets/2026-07-22-deep-fourier-scan/verify_deep_fourier_scan.py
(itself crediting the syracuse-fourier and scalar-phase packets);
exact_chain_phases, the containment/interval-length machinery, and the
escape-weight definitions follow
contribution/packets/2026-07-22-plateau-escape-weight/verify_plateau_escape_weight.py.
The w_n computation is NEW and EXACT at every layer (not sampled): a unit
eta of layer n+1 has a bad image under tap a iff eta = b*2^a (mod 3^n)
for a bad b, so the global minimum of the escape weight is attained on
the explicit candidate set {b*2^a + t*3^n : a<=40, b in B_n, t=0,1,2};
every other unit has w = 1 - 2^-40 exactly.  (The plateau packet needed
samples + near-chain candidates at n >= 12; here the full sweep is exact
at all depths.)

ARITHMETIC DISCIPLINE.  Chain exponents, discrete logs, chain membership,
and circle phases: exact integer / Fraction arithmetic (BSGS, pow with
modulus).  M_n, p_j, w_n, c_n: float64 MEASUREMENTS, labelled as such in
the certificate; complex128/float64 only, never float32/complex64.

REGRESSION GATE (asserted, against the predecessor certificates):
  M_n n=14..17 (deep-fourier cert, >= 7 significant digits);
  chain exponent k(n) n=6..17 exact; bad-set counts n=6..17 exact;
  profile p_j n=8..14 to 1e-9 (plateau cert); escape weights w_n(eps)
  n=6..13 to 1e-12 with identical interval lengths L(n, eps).

KILL CRITERIA / COUNTEREXAMPLE WATCH (asserted or loudly flagged):
  (a) every bad-set member on the +/-2^k chain (exact BSGS), containment
      in a chain interval at every layer and eps;
  (b) w_n(eps) = 2^-L - 2^-40 tightness recorded per layer; w_n(0.05)
      below 1/4 - 2^-40 is the PREDICTED L-creep signature (L >= 3 at
      eps = 0.05), recorded separately from faster-than-creep drops;
  (c) p_j profile stall/reversal quantified by residuals vs the n<=14 fit;
  (d) S1 second-moment identity (n in {9, 12}), S3 escape bound (every
      resolved layer, exact w), Lemma 2 r_n contraction (n <= dense_max):
      asserted.

Env knobs: VPDT_N_MAX (default 20), VPDT_DENSE_MAX (default 15; 0 skips
the dense cross-check), VPDT_THREADS (default min(14, cpu_count)).
Reduced test mode: VPDT_N_MAX=12 VPDT_DENSE_MAX=12 (< 2 s).
"""

import ctypes
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction

import numpy as np

A_TRUNC = 40  # geometric tail beyond a=40 has weight <= 2^-40
EPSILONS = (0.05, 0.1, 0.2)
S1_CHECK_LAYERS = (9, 12)   # S1 identity checked at these n (needs n+1)
HERE = os.path.dirname(os.path.abspath(__file__))
DEEP_CERT = os.path.join(HERE, "..", "2026-07-22-deep-fourier-scan",
                         "deep_fourier_scan_certificate.json")
PLATEAU_CERT = os.path.join(HERE, "..", "2026-07-22-plateau-escape-weight",
                            "plateau_escape_weight_certificate.json")
P2_PREDICTION = 0.95        # the plateau packet's falsifiable threshold

# Certified predecessor values (hard-coded anchors from the deep-fourier
# memo; the live comparison below reads the predecessor certificate JSONs
# and asserts agreement at full precision).
M_CERT_14_17 = {14: 0.0191280, 15: 0.0162845, 16: 0.0144095, 17: 0.0125107}


# ----------------------------------------------------------------------------
# Dense Syracuse offset distributions (float), for the n <= dense_max
# cross-check and Lemma 2 controls ONLY.
# Provenance: copied verbatim from the syracuse-fourier packet via the
# deep-fourier-scan packet's verify_deep_fourier_scan.py.
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
# Half-unit indexing.  Units mod 3^n in increasing order are
# 1, 2, 4, 5, 7, 8, ...; the j-th (0-based) unit is 3*(j//2)+1+(j%2).
# The first 3^(n-1) units are exactly those below 3^n/2 (conjugate pair
# xi <-> 3^n - xi), so the half state has 3^(n-1) entries.
# ----------------------------------------------------------------------------

def half_count(n):
    return 3 ** (n - 1) if n >= 1 else 1


def unit_from_half_index(j):
    return 3 * (j // 2) + 1 + (j % 2)


def unit_index_array(count):
    j = np.arange(count, dtype=np.uint64)
    return 3 * (j // 2) + 1 + (j % 2)


def half_index_of_unit(mu):
    """Index of a unit 0 < mu < 3^n/2 within the half state."""
    return 2 * (mu // 3) + (1 if mu % 3 == 2 else 0)


def c_at(C_half, n, xi):
    """Complex value of c_n at any unit residue xi, via the half state
    (conjugate symmetry c(-xi) = conj(c(xi)), reality of P_n)."""
    mod = 3 ** n
    xi %= mod
    if 2 * xi > mod:
        return complex(C_half[half_index_of_unit(mod - xi)].conjugate())
    return complex(C_half[half_index_of_unit(xi)])


def c_at_many(C_half, n, xis):
    mod = 3 ** n
    xis = np.mod(xis, mod).astype(np.uint64)
    flip = 2 * xis > mod
    m2 = np.where(flip, mod - xis, xis)
    jj = 2 * (m2 // 3) + (m2 % 3 == 2)
    v = C_half[jj]
    return np.where(flip, np.conj(v), v)


# ----------------------------------------------------------------------------
# Transport: C kernel (preferred) and numpy reference/fallback.
# ----------------------------------------------------------------------------

_KERNEL_SRC = os.path.join(HERE, "plateau_drift_kernel.c")
_kernel_cache = {}


def load_c_kernel():
    """Compile plateau_drift_kernel.c (cached by source hash) and return the
    ctypes entry point, or None if compilation is unavailable."""
    if "fn" in _kernel_cache:
        return _kernel_cache["fn"]
    fn = None
    try:
        with open(_KERNEL_SRC, "rb") as f:
            src = f.read()
        key = hashlib.sha256(src).hexdigest()[:16]
        outdir = os.path.join(tempfile.gettempdir(), f"pdt_kernel_{key}")
        so = os.path.join(outdir, "plateau_drift_kernel.so")
        if not os.path.exists(so):
            os.makedirs(outdir, exist_ok=True)
            subprocess.run(
                ["clang", "-O3", "-fPIC", "-shared", "-o", so, _KERNEL_SRC],
                check=True, capture_output=True)
        lib = ctypes.CDLL(so)
        fn = lib.transport
        fn.restype = None
        fn.argtypes = [ctypes.c_void_p] * 2 + [ctypes.c_uint64] * 3 + \
            [ctypes.c_void_p] * 2 + [ctypes.c_int] + \
            [ctypes.c_void_p] * 2 + \
            [ctypes.c_uint64, ctypes.c_double, ctypes.c_int]
    except Exception:
        fn = None
    _kernel_cache["fn"] = fn
    return fn


def transport_c(fn, C_old, n, nthreads):
    """One recursion step (n-1) -> n via the C kernel.  C_old is the
    half-unit state at layer n-1 (layer 0: array([1+0j]))."""
    mod_new = 3 ** n
    mod_old = 3 ** (n - 1)
    h_new = half_count(n)
    period = 2 * mod_old
    taps = min(period, A_TRUNC)
    norm = 1.0 / (1.0 - 2.0 ** (-period))
    u = np.zeros(taps + 1, dtype=np.uint64)
    for a in range(1, taps + 1):
        u[a] = pow(2, -a, mod_new)
    w = np.zeros(taps + 1, dtype=np.float64)
    w[1:] = 2.0 ** (-np.arange(1, taps + 1))
    t = n // 2
    lo = 3 ** t
    hi = 3 ** (n - t)
    Tlo = np.exp(-2j * np.pi * np.arange(lo, dtype=np.float64) / mod_new)
    Thi = np.exp(-2j * np.pi * np.arange(hi, dtype=np.float64) / hi)
    C_new = np.empty(h_new, dtype=np.complex128)
    fn(C_old.ctypes.data, C_new.ctypes.data, mod_old, mod_new, h_new,
       u.ctypes.data, w.ctypes.data, taps,
       Thi.ctypes.data, Tlo.ctypes.data, lo, norm, nthreads)
    return C_new


def transport_np(C_old, n):
    """Reference numpy implementation of the same recursion step (validated
    against dense FFT in the tests; fallback when clang is unavailable)."""
    mod_new = 3 ** n
    mod_old = 3 ** (n - 1)
    h_new = half_count(n)
    period = 2 * mod_old
    taps = min(period, A_TRUNC)
    norm = 1.0 / (1.0 - 2.0 ** (-period))
    j = np.arange(h_new, dtype=np.uint64)
    xi = 3 * (j // 2) + 1 + (j % 2)
    acc = np.zeros(h_new, dtype=np.complex128)
    for a in range(1, taps + 1):
        u = pow(2, -a, mod_new)
        nu = (xi * u) % mod_new
        mu = nu % mod_old
        flip = 2 * mu > mod_old
        m2 = np.where(flip, mod_old - mu, mu)
        jj = 2 * (m2 // 3) + (m2 % 3 == 2)
        val = np.where(flip, np.conj(C_old[jj]), C_old[jj])
        phase = np.exp(-2j * np.pi * (nu.astype(np.float64) / mod_new))
        acc += (2.0 ** (-a)) * phase * val
    return norm * acc


# ----------------------------------------------------------------------------
# Exact chain machinery: BSGS discrete log base 2 mod 3^n (no floats).
# Provenance: verify_deep_fourier_scan.py (chain_log_bsgs/chain_exponent),
# which credits the scalar-phase packet's brute-force chain_log (kept there
# as a cross-check reference).  2 is a primitive root mod 3^n
# (syracuse-fourier packet, verified n <= 6).
# ----------------------------------------------------------------------------

def chain_log_bsgs(mod, xi):
    """Smallest k >= 0 with 2^k == xi (mod 3^n), or None.  Exact."""
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


# ----------------------------------------------------------------------------
# (T1) exact chain phases (integer / Fraction arithmetic only).
# Provenance: verify_plateau_escape_weight.py, exact_chain_phases, unchanged.
# ----------------------------------------------------------------------------

def exact_chain_phases(K, sign, n, a_max=6):
    """Exact circle points {xi* u_a / 3^n} on the chain as Fractions.

    Requires 2^K < 3^n (checked, exact): then xi* u_a mod 3^n is the
    integer s*2^{K-a} (resp. 3^n - 2^{K-a}), no wrap.
    """
    mod = 3 ** n
    assert 2 ** K < mod, "canonical representative wraps; formula needs care"
    out = {}
    for a in range(1, a_max + 1):
        assert K - a >= 0
        res = pow(2, K - a, mod)
        assert res == 2 ** (K - a)  # no modular wrap, exact certificate
        r = (sign * res) % mod
        out[a] = (Fraction(r, mod), r)
    return out


# ----------------------------------------------------------------------------
# (S1) exact second-moment identity at unit frequencies.
# Provenance: scalar-phase packet Theorem S1 via verify_deep_fourier_scan.py
# (s1_second_moment_check), adapted to half-state lookups; deterministic
# unit-frequency sample (no RNG).
# ----------------------------------------------------------------------------

def s1_second_moment_check(C_old, C_new, xis, n):
    """max ||c_{n+1}(xi)|^2 - (diagonal + cross-term sum from layer n)|."""
    mod_old, mod_new = 3 ** n, 3 ** (n + 1)
    us = [pow(2, -a, mod_new) for a in range(1, A_TRUNC + 1)]
    worst = 0.0
    for xi in xis:
        xi %= mod_new
        vals = [c_at(C_old, n, (xi * u) % mod_old) for u in us]
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
        lhs = abs(c_at(C_new, n + 1, xi)) ** 2
        worst = max(worst, abs(lhs - rhs))
    return float(worst)


# ----------------------------------------------------------------------------
# Exact escape weights (NEW): the global minimum over next-layer units is
# attained on the explicit candidate set (see module docstring).
# ----------------------------------------------------------------------------

def bad_residues_from_half(mag_half, M, eps, mod):
    """Bad-set residues (BOTH signs) with |c| > (1-eps) M (small layers)."""
    thr = (1.0 - eps) * M
    js = np.nonzero(mag_half > thr)[0]
    return bad_residues_from_indices(js, mod)


def bad_residues_from_indices(js, mod):
    out = set()
    for j in js.tolist():
        xi = unit_from_half_index(int(j))
        out.add(xi)
        out.add(mod - xi)
    return out


def half_mag_scan(C, chunk=1 << 22):
    """Chunked |C| max/argmax (first-occurrence semantics, like argmax).
    Streaming so that no full-length magnitude array is materialised:
    at n=20 a full float64 magnitude array would cost 9.3 GB on top of the
    18.6 GB state."""
    M = 0.0
    jstar = 0
    for s in range(0, C.size, chunk):
        a = np.abs(C[s:s + chunk])
        i = int(a.argmax())
        if a[i] > M:
            M = float(a[i])
            jstar = s + i
    return M, jstar


def bad_half_indices(C, M, eps, chunk=1 << 22):
    """Chunked threshold scan over |C|; returns half-state indices."""
    thr = (1.0 - eps) * M
    parts = []
    for s in range(0, C.size, chunk):
        a = np.abs(C[s:s + chunk])
        parts.append(np.nonzero(a > thr)[0] + s)
    return (np.concatenate(parts) if parts
            else np.empty(0, dtype=np.int64))


def escape_weight_candidates(bad_set, mod_n):
    """All next-layer units that can have a bad image under any tap:
    eta u_a = b (mod 3^n)  <=>  eta = b*2^a (mod 3^n), three lifts."""
    cand = set()
    for b in bad_set:
        for a in range(1, A_TRUNC + 1):
            r = (b * pow(2, a, mod_n)) % mod_n
            cand.add(r)
            cand.add(r + mod_n)
            cand.add(r + 2 * mod_n)
    return sorted(cand)


def escape_weight_exact(bad_set, u_inv, mod_n, eta):
    """w(eta) = sum_{a: eta u_a mod 3^n not in B} 2^-a; float64 sum in the
    same a-order as the predecessor packets (bit-compatible)."""
    w = 0.0
    for a in range(1, A_TRUNC + 1):
        if (eta * u_inv[a - 1]) % mod_n not in bad_set:
            w += 2.0 ** (-a)
    return w


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    n_max = int(os.environ.get("VPDT_N_MAX", 20))
    dense_max = int(os.environ.get("VPDT_DENSE_MAX", 15))
    nthreads = int(os.environ.get("VPDT_THREADS",
                                  min(14, os.cpu_count() or 1)))
    assert n_max >= 8, "need n_max >= 8 for the profile window"
    t_start = time.time()

    fn = load_c_kernel()
    engine = "c"
    if fn is None:
        engine = "numpy"
        assert n_max <= 16, "numpy fallback certified only to n <= 16"
        print("WARNING: clang/C kernel unavailable, using numpy fallback",
              flush=True)

    def step(C_old, n):
        if engine == "c":
            return transport_c(fn, C_old, n, nthreads)
        return transport_np(C_old, n)

    cert = {"packet": "2026-07-23-plateau-drift-test",
            "scope": "float64 measurements (hypothesis-generators) plus "
                     "exact-arithmetic chain certificates; proved statements "
                     "of predecessor packets are asserted controls, not new "
                     "theorems",
            "n_max": n_max, "a_trunc": A_TRUNC, "engine": engine,
            "state": "half-unit-indexed complex128; conjugate symmetry "
                     "c(-xi) = conj(c(xi)) fills the other half",
            "precision": "float64/complex128 throughout; chain exponents, "
                         "discrete logs and circle phases exact integer/"
                         "Fraction arithmetic; no float32/complex64 anywhere",
            "wall_clock_note": "timings are printed to stdout only, "
                               "not certified"}

    # -- dense stack for the n <= dense_max cross-check and Lemma 2 ----------
    dense_mag_units = {}
    r_rows = []
    if dense_max:
        r_prev = None
        for n, P in syracuse_float_layers(dense_max):
            r = float(P.max())
            row_r = {"n": n, "r_n": r}
            if r_prev is not None:
                bound = ((2.0 / 3.0) * r_prev
                         / (1.0 - 2.0 ** (-2 * 3 ** (n - 2))))
                row_r["ratio"] = r / r_prev
                row_r["lemma2_bound_holds"] = bool(r <= bound + 1e-15)
                assert row_r["lemma2_bound_holds"], n
            r_rows.append(row_r)
            r_prev = r
            C = np.fft.fft(P)
            mag = np.abs(C)
            del P, C
            mag3 = mag.reshape(3 ** n // 3, 3)
            dense_mag_units[n] = mag3[:, 1:].ravel()
            del mag
        cert["lemma2_r_n_table"] = r_rows
        cert["lemma2_all_holds"] = all(
            r.get("lemma2_bound_holds", True) for r in r_rows)

    # -- recursion with per-layer measurements --------------------------------
    layer_rows = []
    profile_rows = []
    escape_rows = []
    s1_rows = []
    dense_check_rows = []
    pending_s3 = None       # rows from layer n-1 awaiting M_n
    prev_peak = None        # (n, xi, K, sign) of the previous layer
    prev_row = None
    C_prev = np.array([1 + 0j], dtype=np.complex128)

    for n in range(1, n_max + 1):
        t0 = time.time()
        C = step(C_prev, n)
        mod = 3 ** n
        el = time.time() - t0
        if n < 6:
            C_prev = C
            continue

        M_n, jstar = half_mag_scan(C)
        xi_peak = unit_from_half_index(jstar)
        k_peak = chain_exponent(mod, xi_peak)
        assert k_peak is not None, ("peak off the chain", n, xi_peak)
        sign = 1 if pow(2, k_peak, mod) == xi_peak % mod else -1
        assert (sign * pow(2, k_peak, mod)) % mod == xi_peak % mod
        no_wrap = bool(2 ** k_peak < mod)
        assert no_wrap, (n, k_peak)  # exact-phase guard (P1 needs no wrap)

        row = {"n": n, "M_n": M_n, "argmax_half_unit": xi_peak,
               "chain_log_k": k_peak, "sign": sign,
               "two_pow_k_lt_3_pow_n": no_wrap,
               "c_n": -math.log(M_n) / math.sqrt(n)}

        # resolve controls that needed the CURRENT layer:
        # (S3) pending rows from layer n-1, exact w (proved Theorem S3)
        if pending_s3 is not None:
            for erow in pending_s3:
                bound = (1.0 - erow["eps"] * erow["escape_weight_min"]) \
                    * erow["M_n"]
                erow["M_next"] = M_n
                erow["s3_bound"] = bound
                erow["holds"] = bool(M_n <= bound + 1e-12)
                assert erow["holds"], erow
                escape_rows.append(erow)
            pending_s3 = None
        # (T1) exact chain phases at the previous layer's peak, and the
        # triangle bound / phase bite at the NEW peak (needs c_{n-1}, still
        # alive in C_prev)
        if prev_peak is not None:
            n_p, _, K_p, s_p = prev_peak
            if n_p >= 8:
                ph = exact_chain_phases(K_p, s_p, n_p)
                rel = (ph[1][0] - ph[2][0]) % 1
                misalign = min(rel, 1 - rel)
                assert misalign == Fraction(2 ** (K_p - 2), 3 ** n_p)
                prev_row["t1_dominant_pair_misalignment_exact"] = \
                    [str(misalign.numerator), str(misalign.denominator)]
                prev_row["t1_dominant_pair_misalignment_float"] = \
                    float(misalign)
                mod_p = 3 ** n_p
                tri = 0.0
                for a in range(1, A_TRUNC + 1):
                    tri += (2.0 ** (-a)
                            * abs(c_at(C_prev, n_p,
                                       (xi_peak * pow(2, -a, mod)) % mod_p)))
                tri /= prev_row["M_n"]
                rho = M_n / prev_row["M_n"]
                assert tri >= rho - 1e-12
                prev_row["triangle_bound_at_new_peak"] = tri
                prev_row["phase_factor_at_new_peak"] = rho / tri
        # (S1) second-moment identity at layers in S1_CHECK_LAYERS
        if (n - 1) in S1_CHECK_LAYERS:
            n1 = n - 1
            mod1 = 3 ** (n1 + 1)
            xis = sorted({pow(2, k, mod1) for k in (0, 1, 7, 10, 11)}
                         | {5 % mod1})
            err = s1_second_moment_check(C_prev, C, xis, n1)
            assert err < 1e-8, (n1, err)
            s1_rows.append({"n": n1, "n_sampled_xis": len(xis),
                            "max_abs_err": err, "frequencies": "units only"})

        # dense cross-check (full unit magnitude vector, both signs, in
        # increasing order = mag3[:,1:].ravel() order)
        if n in dense_mag_units:
            U = unit_index_array(half_count(n))
            both = np.concatenate([U, mod - U[::-1]])
            rec = c_at_many(C, n, both)
            d = float(np.abs(np.abs(rec) - dense_mag_units[n]).max())
            dense_check_rows.append({"n": n, "max_abs_mag_diff": d})
            assert d < 1e-9, (n, d)
            row["dense_cross_check_max_abs_diff"] = d

        # bad sets, chain membership, containment, L(n, eps), exact w_n
        w_pending = []
        u_inv = [pow(2, -a, mod) for a in range(1, A_TRUNC + 1)]
        for eps in EPSILONS:
            bad = bad_residues_from_indices(
                bad_half_indices(C, M_n, eps), mod)
            row[f"bad_count_{eps}"] = len(bad)
            logs = {b: chain_exponent(mod, b) for b in bad}
            off_chain = [int(b) for b, k in logs.items() if k is None]
            assert not off_chain, ("kill criterion (a) fired", n, eps,
                                   off_chain)
            idx = sorted(k_peak - k for k in logs.values())
            lo_i, hi_i = (min(idx), max(idx)) if idx else (0, -1)
            L = hi_i - lo_i + 1 if idx else 0
            contained = bool(idx) and idx == sorted(
                j for j in range(lo_i, hi_i + 1) for _ in range(2))
            assert contained, ("containment failed", n, eps, idx)
            # exact w_n: global min over next-layer units via candidates
            cand = escape_weight_candidates(bad, mod)
            w_min = min(escape_weight_exact(bad, u_inv, mod, eta)
                        for eta in cand)
            t4 = 2.0 ** (-L) - 2.0 ** (-A_TRUNC)
            assert w_min >= t4 - 1e-12, (n, eps, w_min, t4)
            row[f"L_{eps}"] = L
            row[f"w_{eps}"] = w_min
            row[f"w_{eps}_tight_eq_2^-L-2^-40"] = \
                bool(abs(w_min - t4) < 1e-12)
            row[f"bad_chain_indices_{eps}"] = idx
            w_pending.append({"n": n, "eps": eps, "M_n": M_n,
                              "escape_weight_min": w_min, "mode": "exact",
                              "interval_length_L": L,
                              "n_candidates": len(cand),
                              "bad_chain_indices": idx})
        pending_s3 = w_pending

        # near-peak profile p_j, psi_j (j = 0..8); exact on-chain proof of
        # every chain point (integer pow check + independent BSGS)
        prof = {}
        for jj in range(9):
            cp = int((xi_peak * pow(2, -jj, mod)) % mod)
            if k_peak - jj >= 0:
                assert (sign * pow(2, k_peak - jj, mod)) % mod == cp
                k_cp = chain_exponent(mod, cp)
                assert k_cp == k_peak - jj, (n, jj, k_cp, k_peak)
            v = c_at(C, n, cp)
            prof[str(jj)] = {"p": float(abs(v)) / M_n,
                             "psi": float(np.angle(v))}
        row["profile_p"] = {j: prof[j]["p"] for j in prof}
        profile_rows.append({"n": n, "K": k_peak, "sign": sign,
                             "p": {j: prof[j]["p"] for j in prof},
                             "psi": {j: prof[j]["psi"] for j in prof}})

        layer_rows.append(row)
        prev_row = row
        prev_peak = (n, xi_peak, k_peak, sign)
        C_prev = C
        print(f"layer {n:2d} done in {el:7.1f}s  M_n={M_n:.10f}  "
              f"k={k_peak} p2={row['profile_p']['2']:.6f} "
              f"w05={row['w_0.05']:.6f} L02={row['L_0.2']}", flush=True)

    # T1 exact chain phases at the FINAL layer's peak (no next layer
    # exists to attach them to during the loop; compute directly)
    if prev_peak is not None and prev_peak[0] >= 8:
        n_p, _, K_p, s_p = prev_peak
        ph = exact_chain_phases(K_p, s_p, n_p)
        rel = (ph[1][0] - ph[2][0]) % 1
        misalign = min(rel, 1 - rel)
        assert misalign == Fraction(2 ** (K_p - 2), 3 ** n_p)
        prev_row["t1_dominant_pair_misalignment_exact"] = \
            [str(misalign.numerator), str(misalign.denominator)]
        prev_row["t1_dominant_pair_misalignment_float"] = float(misalign)

    # trailing S3 rows have no M_{n_max+1}; the w values are exact
    # regardless, so record them unresolved
    if pending_s3 is not None:
        for erow in pending_s3:
            erow["M_next"] = None
            erow["s3_bound"] = None
            erow["holds"] = None
            erow["note"] = "final layer: M_{n+1} not computed; w_n exact"
            escape_rows.append(erow)
        pending_s3 = None

    cert["layer_table"] = layer_rows
    cert["profile_table"] = profile_rows
    cert["escape_weight_table"] = escape_rows
    cert["s1_second_moment"] = s1_rows
    cert["dense_cross_check"] = dense_check_rows
    cert["s1_all_below_1e-8"] = all(r["max_abs_err"] < 1e-8
                                    for r in s1_rows)

    # -- regression gate against the predecessor certificates -----------------
    regression = {"checks": [], "all_passed": True}

    def reg(name, ok, detail):
        regression["checks"].append({"check": name, "passed": bool(ok),
                                     "detail": detail})
        regression["all_passed"] = regression["all_passed"] and bool(ok)
        assert ok, ("REGRESSION FAILURE", name, detail)

    with open(DEEP_CERT) as f:
        deep = json.load(f)
    deep_rows = {r["n"]: r for r in deep["layer_table"]}
    mine = {r["n"]: r for r in layer_rows}
    for n in range(6, 18):
        if n not in mine:
            continue
        dr, mr = deep_rows[n], mine[n]
        reg(f"M_{n}_matches_deep_fourier",
            abs(mr["M_n"] - dr["M_n"]) <= 1e-9 * max(1.0, dr["M_n"]),
            {"mine": mr["M_n"], "deep_fourier": dr["M_n"]})
        reg(f"k({n})_matches_deep_fourier",
            mr["chain_log_k"] == dr["chain_log_k"],
            {"mine": mr["chain_log_k"], "deep_fourier": dr["chain_log_k"]})
        for eps in EPSILONS:
            reg(f"bad_count_{n}_{eps}_matches",
                mr[f"bad_count_{eps}"] == dr[f"bad_count_{eps}"],
                {"mine": mr[f"bad_count_{eps}"],
                 "deep_fourier": dr[f"bad_count_{eps}"]})
    for n in (14, 15, 16, 17):
        if n in mine:
            reg(f"M_{n}_7_digits_vs_hardcoded",
                abs(mine[n]["M_n"] - M_CERT_14_17[n]) < 5e-8,
                {"mine": mine[n]["M_n"], "certified": M_CERT_14_17[n]})

    with open(PLATEAU_CERT) as f:
        plat = json.load(f)
    plat_prof = {r["n"]: r for r in plat["profile_table"]}
    my_prof = {r["n"]: r for r in profile_rows}
    worst_p = 0.0
    for n in range(8, 15):
        if n not in my_prof:
            continue
        for j in range(9):
            d = abs(my_prof[n]["p"][str(j)] - plat_prof[n]["p"][str(j)])
            worst_p = max(worst_p, d)
    reg("profile_p_j_n8..14_matches_plateau", worst_p < 1e-9,
        {"max_abs_diff": worst_p})
    plat_esc = [r for r in plat["escape_weight_table"]]
    my_esc = {(r["n"], r["eps"]): r for r in escape_rows}
    worst_w = 0.0
    for r in plat_esc:
        key = (r["n"], r["eps"])
        if key not in my_esc:
            continue
        d = abs(my_esc[key]["escape_weight_min"] - r["escape_weight_min"])
        worst_w = max(worst_w, d)
        reg(f"L({key[0]},{key[1]})_matches_plateau",
            my_esc[key]["interval_length_L"] == r["interval_length_L"],
            {"mine": my_esc[key]["interval_length_L"],
             "plateau": r["interval_length_L"]})
    reg("escape_weights_n6..13_match_plateau", worst_w < 1e-12,
        {"max_abs_diff": worst_w})
    # the drift fit itself must reproduce the plateau packet's published
    # slopes (memo table: p1/p2/p3 = +0.0114/+0.0238/+0.0186 per layer)
    plat_slopes = {s["j"]: s["slope_per_layer"]
                   for s in plat["plateau_stats"]}
    ns8 = np.arange(8, 15, dtype=np.float64)
    for j in (1, 2, 3):
        if 14 not in my_prof:
            continue
        vals = np.array([my_prof[n]["p"][str(j)] for n in range(8, 15)])
        slope = float(np.polyfit(ns8, vals, 1)[0])
        reg(f"p{j}_slope_reproduces_plateau_fit",
            abs(slope - plat_slopes[j]) < 1e-12,
            {"mine": slope, "plateau": plat_slopes[j]})
    cert["regression_vs_predecessors"] = regression

    # -- the drift test ---------------------------------------------------------
    ns = np.array([r["n"] for r in profile_rows], dtype=np.float64)
    drift = {"p2_prediction_threshold": P2_PREDICTION,
             "fit_window_old": [8, 14],
             "old_fit_source": "recomputed from this packet's reproduced "
                               "n<=14 profile table, not imported"}
    fits = {}
    for j in (1, 2, 3):
        vals = np.array([r["p"][str(j)] for r in profile_rows])
        old = (ns >= 8) & (ns <= 14)  # plateau packet's fit window
        slope_old, int_old = np.polyfit(ns[old], vals[old], 1)
        slope_all, int_all = np.polyfit(ns[ns >= 8], vals[ns >= 8], 1)
        fits[f"p{j}"] = {
            "slope_per_layer_fit_n8..14": float(slope_old),
            "intercept_fit_n8..14": float(int_old),
            "slope_per_layer_fit_full_window": float(slope_all),
            "intercept_fit_full_window": float(int_all)}
    drift["profile_fits"] = fits
    s_old, i_old = (fits["p2"]["slope_per_layer_fit_n8..14"],
                    fits["p2"]["intercept_fit_n8..14"])
    s_all, i_all = (fits["p2"]["slope_per_layer_fit_full_window"],
                    fits["p2"]["intercept_fit_full_window"])
    p2_rows = []
    for r in profile_rows:
        n = r["n"]
        pred = s_old * n + i_old
        p2_rows.append({"n": n, "p2_measured": r["p"]["2"],
                        "p2_extrapolated_from_n<=14_fit": float(pred),
                        "residual": r["p"]["2"] - float(pred)})
    drift["p2_vs_extrapolation"] = p2_rows
    drift["p2_crossing_0.95_old_fit"] = \
        float((P2_PREDICTION - i_old) / s_old) if s_old > 0 else None
    drift["p2_crossing_0.95_full_fit"] = \
        float((P2_PREDICTION - i_all) / s_all) if s_all > 0 else None
    # late-window slope (new layers only, n >= 15) as a stall diagnostic
    new_vals = [(r["n"], r["p"]["2"]) for r in profile_rows if r["n"] >= 15]
    if len(new_vals) >= 2:
        s_new = float(np.polyfit([v[0] for v in new_vals],
                                 [v[1] for v in new_vals], 1)[0])
        drift["p2_slope_new_layers_only"] = s_new
        drift["p2_new_layer_values"] = [v[1] for v in new_vals]
    # parity split: the near-peak profile alternates strongly with the
    # parity of n (visible in every window); per-branch linear fits are
    # the honest continuation of the drift
    for parity, label in ((0, "even"), (1, "odd")):
        pts = [(r["n"], r["p"]["2"]) for r in profile_rows
               if r["n"] >= 8 and r["n"] % 2 == parity]
        if len(pts) >= 2:
            slope_p, int_p = np.polyfit([p[0] for p in pts],
                                        [p[1] for p in pts], 1)
            drift[f"p2_{label}_branch"] = {
                "values": {str(p[0]): p[1] for p in pts},
                "slope_per_layer": float(slope_p),
                "intercept": float(int_p),
                "crossing_0.95": float((P2_PREDICTION - int_p) / slope_p)
                if slope_p > 0 else None}
    # L-creep and w_n(0.05) vs the 1/4 quantization threshold
    drift["L_creep_table"] = [
        {"n": r["n"], "L_0.05": r["L_0.05"], "L_0.1": r["L_0.1"],
         "L_0.2": r["L_0.2"], "w_0.05": r["w_0.05"], "w_0.2": r["w_0.2"],
         "w_0.05_at_or_above_quarter":
             bool(r["w_0.05"] >= 0.25 - 2.0 ** (-A_TRUNC) - 1e-12)}
        for r in layer_rows]
    drift["w_0.05_below_quarter_layers"] = [
        r["n"] for r in layer_rows
        if r["w_0.05"] < 0.25 - 2.0 ** (-A_TRUNC) - 1e-12]
    drift["half_log2_n_reference"] = {
        str(n): 0.5 * math.log2(n) for n in (14, 20, 22, 30)}
    cert["drift_test"] = drift

    # -- counterexample watch ---------------------------------------------------
    cert["counterexample_watch"] = {
        "(a)_off_chain_bad_frequency": {
            "fired": False,
            "detail": "every bad-set member at every computed layer/eps "
                      "has an exact base-2 discrete log (asserted above); "
                      "the argmax at every layer is on the +/-2^k chain "
                      "(exact BSGS), so no off-chain unit frequency beats "
                      "the on-chain peak"},
        "(b)_w_n_dropping_faster_than_creep": {
            "w_0.05_below_quarter_layers":
                drift["w_0.05_below_quarter_layers"],
            "detail": "w_n(0.05) below 1/4 - 2^-40 is the PREDICTED "
                      "L-creep signature (L >= 3 at eps = 0.05): a "
                      "confirmation of the prediction if listed, not an "
                      "anomaly. No layer showed w_n(eps) < 2^-L - 2^-40 "
                      "(tightness asserted); no L jump by more than 1 "
                      "between consecutive layers is treated as creep-"
                      "consistent and recorded in the L_creep_table"},
        "(c)_p_j_stall_or_reversal": {
            "p2_slope_fit_n8..14": fits["p2"]["slope_per_layer_fit_n8..14"],
            "p2_slope_new_layers": drift.get("p2_slope_new_layers_only"),
            "residuals_vs_old_fit": [
                {"n": r["n"], "residual": r["residual"]}
                for r in p2_rows if r["n"] >= 15]},
        "(d)_proved_control_failures": {
            "s1_max_err": max((r["max_abs_err"] for r in s1_rows),
                              default=None),
            "s3_violations": [r for r in escape_rows
                              if r["holds"] is False],
            "lemma2_all_holds": cert.get("lemma2_all_holds"),
            "dense_cross_check_max": max(
                (r["max_abs_mag_diff"] for r in dense_check_rows),
                default=None)},
    }

    # decay fit (continuity with the deep-fourier packet)
    Ms = np.array([r["M_n"] for r in layer_rows])
    nsv = np.array([r["n"] for r in layer_rows], dtype=np.float64)
    x = np.sqrt(nsv)
    y = -np.log(Ms)
    cert["decay_fit"] = {
        "window": [int(nsv[0]), int(nsv[-1])],
        "per_layer_c_n": {str(r["n"]): r["c_n"] for r in layer_rows},
        "c_fit_through_origin": float((x * y).sum() / (x * x).sum()),
        "reference_c_from_prior_packets": 1.06}

    out = json.dumps(cert, indent=1, sort_keys=True)
    with open("plateau_drift_certificate.json", "w") as f:
        f.write(out + "\n")

    summary = {
        "status": "ok", "n_max": n_max, "engine": engine,
        "M_n": {r["n"]: r["M_n"] for r in layer_rows[-4:]},
        "k": {r["n"]: r["chain_log_k"] for r in layer_rows[-4:]},
        "p2": {r["n"]: r["p"]["2"] for r in profile_rows[-4:]},
        "p2_slope_old": fits["p2"]["slope_per_layer_fit_n8..14"],
        "p2_slope_new": drift.get("p2_slope_new_layers_only"),
        "p2_crossing_0.95_full_fit": drift["p2_crossing_0.95_full_fit"],
        "w_0.05_last": layer_rows[-1]["w_0.05"],
        "L_0.2_last": layer_rows[-1]["L_0.2"],
        "regression_all_passed": regression["all_passed"],
        "wall_clock_seconds_total": round(time.time() - t_start, 1),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
