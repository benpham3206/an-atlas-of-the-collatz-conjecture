"""RED/GREEN gate for the streaming layer engine.

The whole claim of streaming_layer.py is that consuming a layer in chunks
changes nothing.  That is asserted here as BIT-IDENTITY, not as closeness:
if any of these fail, no depth-21 number produced by the streaming engine
may be reported.
"""

import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-07-23-plateau-drift-test"))

import streaming_layer as sl  # noqa: E402
import verify_plateau_drift_test as v  # noqa: E402

pytestmark = pytest.mark.skipif(sl.load_range_kernel() is None,
                                reason="clang unavailable")


def resident_layers(n_max, nthreads=4):
    """Reference: the drift-test engine, layers materialised as usual."""
    fn = v.load_c_kernel()
    C = np.array([1 + 0j], dtype=np.complex128)
    out = {0: C}
    for n in range(1, n_max + 1):
        C = v.transport_c(fn, C, n, nthreads)
        out[n] = C
    return out


@pytest.fixture(scope="module")
def layers():
    return resident_layers(13)


def test_transport_range_matches_full_transport(layers):
    """Chunked transport reproduces the full-width transport exactly."""
    fn = sl.load_range_kernel()
    for n in (6, 9, 12, 13):
        C_old = layers[n - 1]
        ref = layers[n]
        P = sl._layer_params(n)
        h = v.half_count(n)
        for chunk in (1, 7, 1024, h):
            got = np.empty(h, dtype=np.complex128)
            buf = np.empty(min(chunk, h), dtype=np.complex128)
            for s in range(0, h, chunk):
                e = min(s + chunk, h)
                got[s:e] = sl.transport_chunk(fn, C_old, n, s, e, buf, P, 3)
            assert np.array_equal(got, ref), (n, chunk)


def test_thread_count_does_not_change_results(layers):
    """Output j depends only on j, so threading is not a source of drift."""
    fn = sl.load_range_kernel()
    n = 12
    C_old = layers[n - 1]
    P = sl._layer_params(n)
    h = v.half_count(n)
    base = None
    for nt in (1, 2, 5, 8):
        got = np.empty(h, dtype=np.complex128)
        buf = np.empty(h, dtype=np.complex128)
        got[:] = sl.transport_chunk(fn, C_old, n, 0, h, buf, P, nt)
        if base is None:
            base = got
        else:
            assert np.array_equal(got, base), nt


def test_stream_layer_matches_resident_reductions(layers):
    """M_n, argmax and every bad set agree exactly with the resident scan."""
    for n in (8, 10, 12, 13):
        C_old = layers[n - 1]
        C = layers[n]
        M_ref, j_ref = v.half_mag_scan(C)
        got = sl.stream_layer(C_old, n, v.EPSILONS, nthreads=3, chunk_pow=10)
        assert got["M"] == M_ref, (n, got["M"], M_ref)
        assert got["jstar"] == j_ref, (n, got["jstar"], j_ref)
        for eps in v.EPSILONS:
            ref = v.bad_half_indices(C, M_ref, eps)
            assert np.array_equal(np.sort(got["bad_idx"][eps]),
                                  np.sort(ref)), (n, eps)


def test_point_values_match_resident(layers):
    """Named-unit evaluation equals the resident value bit for bit."""
    for n in (7, 10, 13):
        C_old = layers[n - 1]
        C = layers[n]
        mod = 3 ** n
        rng = np.random.default_rng(20260724)
        xis = [int(x) for x in rng.integers(1, mod, size=40) if x % 3]
        # include both halves and the conjugate-fold boundary
        xis += [1, 2, mod - 1, mod - 2, (mod - 1) // 2, (mod + 1) // 2]
        xis = [x for x in xis if x % 3 and 0 < x < mod]
        got = sl.point_values(C_old, n, xis)
        ref = np.array([v.c_at(C, n, x) for x in xis], dtype=np.complex128)
        assert np.array_equal(got, ref), n


def test_bad_set_residues_and_escape_weights_agree(layers):
    """The downstream exact quantities are unchanged under streaming."""
    for n in (10, 12):
        C_old = layers[n - 1]
        C = layers[n]
        mod = 3 ** n
        M_ref, _ = v.half_mag_scan(C)
        got = sl.stream_layer(C_old, n, (0.2,), nthreads=3, chunk_pow=10)
        u_inv = [pow(2, -a, mod) for a in range(1, v.A_TRUNC + 1)]
        for src in (got["bad_idx"][0.2], v.bad_half_indices(C, M_ref, 0.2)):
            bad = v.bad_residues_from_indices(src, mod)
            cand = v.escape_weight_candidates(bad, mod)
            w = min(v.escape_weight_exact(bad, u_inv, mod, e) for e in cand)
            if src is got["bad_idx"][0.2]:
                w_stream, bad_stream = w, bad
            else:
                w_res, bad_res = w, bad
        assert bad_stream == bad_res, n
        assert w_stream == w_res, n
