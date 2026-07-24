"""Streaming layer engine: certify one Syracuse-character layer without ever
materialising it.

WHY THIS EXISTS.  The plateau-drift-test engine holds the layer state
resident: layer n costs 3^(n-1) complex128.  That is 17.3 GiB at n = 20 and
52.0 GiB at n = 21, and the transport step needs the old and new layers
simultaneously (69.3 GiB at n = 21).  The drift-test memo records n = 20 as
"the honest ceiling of this engine on this machine" (36 GB).  The wall is
memory, not arithmetic: the n = 21 transport is only ~3x the n = 20 work.

THE OBSERVATION.  Nothing downstream needs the layer as an array.  Per layer
the drift test consumes exactly four things:

  1. M_n and the peak unit          -- a max-reduction over the layer;
  2. the bad sets {|c| > (1-eps)M}  -- a threshold-reduction (tiny output);
  3. the near-peak profile p_j      -- 9 named units;
  4. the escape weights w_n(eps)    -- integer arithmetic on the bad set
                                       ONLY; no state values at all
                                       (see escape_weight_exact).

(1) and (2) are streamable in one chunk at a time.  (3) is a handful of
point evaluations.  So a layer can be certified with the PREVIOUS layer
resident and the current layer never allocated: peak memory drops from
3^(n-1) + 3^(n-2) to 3^(n-2) + one chunk.  At n = 21 that is 17.3 GiB
instead of 69.3 GiB.

BIT-IDENTITY.  transport_range() in plateau_drift_kernel.c computes output
element j from j alone (the nu_a carry is re-seeded by exact integer
arithmetic at each thread start, and the float accumulation runs over
a = 1..taps in a fixed order).  So chunking cannot perturb a single output
bit, and streamed results are bit-identical to resident ones.  This is not
assumed -- test_streaming_depth_21.py asserts exact equality of the full
complex arrays, of M_n, and of the bad sets, at every layer n <= 15.

ARITHMETIC DISCIPLINE.  Unchanged from the predecessor packets.  Chain
exponents, discrete logs, bad-set residues and escape weights are exact
integer / rational work; M_n, p_j and c_n are float64 MEASUREMENTS.  Nothing
is downgraded to complex64 to buy depth.
"""

import ctypes
import hashlib
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRIFT = os.path.join(HERE, "..", "2026-07-23-plateau-drift-test")
sys.path.insert(0, DRIFT)

import verify_plateau_drift_test as v  # noqa: E402

KERNEL_SRC = os.path.join(DRIFT, "plateau_drift_kernel.c")
_cache = {}


def load_range_kernel():
    """Compile the shared kernel and return the transport_range entry point.

    Same source file, same flags, and the same source-hash cache directory
    convention as the drift-test loader; only the exported symbol differs.
    """
    if "fn" in _cache:
        return _cache["fn"]
    fn = None
    try:
        with open(KERNEL_SRC, "rb") as f:
            src = f.read()
        key = hashlib.sha256(src).hexdigest()[:16]
        outdir = os.path.join(tempfile.gettempdir(), f"pdt_kernel_{key}")
        so = os.path.join(outdir, "plateau_drift_kernel.so")
        if not os.path.exists(so):
            os.makedirs(outdir, exist_ok=True)
            subprocess.run(
                ["clang", "-O3", "-fPIC", "-shared", "-o", so, KERNEL_SRC],
                check=True, capture_output=True)
        lib = ctypes.CDLL(so)
        fn = lib.transport_range
        fn.restype = None
        fn.argtypes = ([ctypes.c_void_p] * 2 + [ctypes.c_uint64] * 4 +
                       [ctypes.c_void_p] * 2 + [ctypes.c_int] +
                       [ctypes.c_void_p] * 2 +
                       [ctypes.c_uint64, ctypes.c_double, ctypes.c_int])
    except Exception:
        fn = None
    _cache["fn"] = fn
    return fn


def _layer_params(n):
    """Tap table, weights and root-of-unity tables for the (n-1) -> n step.

    Byte-for-byte the same construction as transport_c() in the drift-test
    verifier; factored out here so a streamed layer builds them once and
    reuses them across every chunk.
    """
    mod_new = 3 ** n
    mod_old = 3 ** (n - 1)
    period = 2 * mod_old
    taps = min(period, v.A_TRUNC)
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
    return dict(mod_new=mod_new, mod_old=mod_old, taps=taps, norm=norm,
                u=u, w=w, Tlo=Tlo, Thi=Thi, lo=lo)


def transport_chunk(fn, C_old, n, jlo, jhi, out, P, nthreads):
    """Fill out[0:jhi-jlo] with layer-n outputs j in [jlo, jhi)."""
    fn(C_old.ctypes.data, out.ctypes.data, P["mod_old"], P["mod_new"],
       int(jlo), int(jhi), P["u"].ctypes.data, P["w"].ctypes.data, P["taps"],
       P["Thi"].ctypes.data, P["Tlo"].ctypes.data, P["lo"], P["norm"],
       nthreads)
    return out[:jhi - jlo]


def stream_layer(C_old, n, epsilons, nthreads, chunk_pow=24, progress=None):
    """Certify layer n from layer n-1 without allocating layer n.

    Two streaming passes over the layer:
      pass 1 -- max |c| and its argmax (first-occurrence, matching
                np.argmax and v.half_mag_scan);
      pass 2 -- threshold scan |c| > (1-eps)M for each eps.
    A second pass is needed because the threshold is defined by M, which is
    only known after pass 1.  Both passes are compute-bound, not
    memory-bound, so this costs time (2x transport) and not footprint.

    Returns {"M": float, "jstar": int, "bad_idx": {eps: np.ndarray}}.
    """
    fn = load_range_kernel()
    if fn is None:
        raise RuntimeError("clang unavailable: streaming needs the C kernel")
    P = _layer_params(n)
    h_new = v.half_count(n)
    chunk = min(1 << chunk_pow, h_new)
    buf = np.empty(chunk, dtype=np.complex128)

    M = 0.0
    jstar = 0
    for s in range(0, h_new, chunk):
        e = min(s + chunk, h_new)
        a = np.abs(transport_chunk(fn, C_old, n, s, e, buf, P, nthreads))
        i = int(a.argmax())
        if a[i] > M:
            M = float(a[i])
            jstar = s + i
        if progress:
            progress("max", e, h_new)

    bad_idx = {}
    thr = {eps: (1.0 - eps) * M for eps in epsilons}
    parts = {eps: [] for eps in epsilons}
    for s in range(0, h_new, chunk):
        e = min(s + chunk, h_new)
        a = np.abs(transport_chunk(fn, C_old, n, s, e, buf, P, nthreads))
        for eps in epsilons:
            hit = np.nonzero(a > thr[eps])[0]
            if hit.size:
                parts[eps].append(hit + s)
        if progress:
            progress("bad", e, h_new)
    for eps in epsilons:
        bad_idx[eps] = (np.concatenate(parts[eps]) if parts[eps]
                        else np.empty(0, dtype=np.int64))

    return {"M": M, "jstar": jstar, "bad_idx": bad_idx}


def point_values(C_old, n, xis, nthreads=1):
    """Exact layer-n values at named units, via 1-element kernel calls.

    Uses the same kernel path as a full transport, so the returned values
    are bit-identical to the resident ones (rather than merely close, which
    a separate numpy phase evaluation would be).  Units at or above
    3^n / 2 are folded with the conjugate symmetry c(-xi) = conj(c(xi)),
    exactly as v.c_at does.
    """
    fn = load_range_kernel()
    if fn is None:
        raise RuntimeError("clang unavailable: streaming needs the C kernel")
    P = _layer_params(n)
    mod = P["mod_new"]
    buf = np.empty(1, dtype=np.complex128)
    out = []
    for xi in xis:
        mu = int(xi) % mod
        if mu == 0:
            raise ValueError("0 is not a unit")
        flip = 2 * mu > mod
        m2 = mod - mu if flip else mu
        j = v.half_index_of_unit(m2)
        val = complex(transport_chunk(fn, C_old, n, j, j + 1, buf,
                                      P, nthreads)[0])
        out.append(np.conj(val) if flip else val)
    return np.array(out, dtype=np.complex128)
