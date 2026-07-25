#!/usr/bin/env python3
"""Tests for verify_contraction_onset.py.  Runs standalone or under pytest.

Attacks the three places this packet could be wrong: the cocycle, Lemma 2's
hypothesis (which is only valid before the FIRST contracting index), and the
minimality of A*(h).
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MODPATH = os.path.join(HERE, "verify_contraction_onset.py")
_spec = importlib.util.spec_from_file_location("vco", MODPATH)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)


def test_cocycle_matches_direct_iteration():
    for x in range(1, 4001, 2):
        rows = V.cocycle(x, 30)
        y = x
        for h, (a, A, C, sh) in enumerate(rows, start=1):
            y, aa = V.syracuse_step(y)
            assert aa == a and y == sh, (x, h)
            assert (1 << A) * sh == 3 ** h * x + C, (x, h)


def test_lemma1_descent_requires_contraction():
    """The load-bearing elementary step: no descent without 2^A > 3^h."""
    for x in range(1, 20001, 2):
        y = x
        A = 0
        p3 = 1
        for h in range(1, 80):
            y, a = V.syracuse_step(y)
            A += a
            p3 *= 3
            if y < x:
                assert (1 << A) > p3, f"x={x} descended at h={h} without contracting"
                break


def test_a_star_is_minimal():
    for h in range(1, 400):
        p3 = 3 ** h
        A = V.a_star(h, p3)
        assert (1 << A) > p3
        assert (1 << (A - 1)) <= p3
        assert A == p3.bit_length()


def test_lemma2_holds_before_onset_and_can_fail_after():
    """C_h <= h*3^(h-1) is claimed ONLY before the first contracting index.
    Confirm it holds there, and record that it is not claimed afterwards --
    if it were unconditionally true the Theorem would not need the
    'first' qualifier, so a failure after onset is expected, not a bug."""
    before = after_ok = after_bad = 0
    for x in range(1, 6001, 2):
        rows = V.cocycle(x, 45)
        first_active = None
        for h, (_a, A, C, _y) in enumerate(rows, start=1):
            if first_active is None and (1 << A) > 3 ** h:
                first_active = h
            bound = C <= h * 3 ** (h - 1)
            if first_active is None or h < first_active:
                assert bound, f"Lemma 2 failed before onset at x={x} h={h}"
                before += 1
            else:
                after_ok += bound
                after_bad += (not bound)
    assert before > 0
    # The point of the qualifier: the bound is not universally true.
    assert after_bad > 0, ("Lemma 2 never failed after onset in this sample; "
                           "the 'first contracting index' qualifier is then "
                           "untested here")


def test_theorem_bound_holds_on_real_orbits():
    """If h is the first contracting index and the orbit has not descended,
    then x <= M(h).  Only x = 1 reaches that branch, so also assert that."""
    hit = []
    for x in range(1, 200001, 2):
        y = x
        A = 0
        p3 = 1
        for h in range(1, 400):
            y, a = V.syracuse_step(y)
            A += a
            p3 *= 3
            if (1 << A) > p3:            # first contracting index
                if y >= x:
                    m = (h * 3 ** (h - 1)) // ((1 << V.a_star(h, p3)) - p3)
                    assert x <= m, f"Theorem violated: x={x} h={h} M={m}"
                    hit.append(x)
                break
    assert hit == [1], hit


def test_m_table_max_is_below_barina():
    best, arg, samples = V.m_table(3000)
    # argmax over h <= 3000 is the semiconvergent 2966 = 306 + 4*665, not a
    # convergent denominator -- the records interleave both.
    assert best == 1165905 and arg == 2966, (best, arg)
    assert best < V.BARINA
    assert samples[5]["M"] == 31 and samples[41]["M"] == 1185
    assert samples[306]["A_star"] == 485 and samples[306]["M"] == 99729


def test_record_depths_are_convergents_and_semiconvergents():
    """M(h) sets records only at good rational approximations to log_2 3 from
    above: the convergent denominators 5, 41, 306, 15601 and the
    semiconvergents 306 + k*665 interpolating the last gap."""
    p3 = 1
    best = 0
    recs = []
    for h in range(1, 3001):
        prev = p3
        p3 *= 3
        A = p3.bit_length()
        m = (h * prev) // ((1 << A) - p3)
        if m > best:
            best = m
            recs.append(h)
    for q in (5, 41, 306):
        assert q in recs, q
    tail = [h for h in recs if h > 306]
    assert tail == [306 + 665 * k for k in range(1, len(tail) + 1)], tail


def test_scan_finds_no_survivor_and_would_find_one():
    surv, stuck = V.scan_onset(50001)
    assert surv == [] and stuck == []
    # positive control: x = 1 is a survivor by the same criterion
    y, A, p3 = 1, 0, 1
    fa = None
    for h in range(1, 20):
        y, a = V.syracuse_step(y)
        A += a
        p3 *= 3
        if fa is None and (1 << A) > p3:
            fa = h
        assert y >= 1
    assert fa == 1


def test_verifier_is_deterministic():
    tmp = tempfile.mkdtemp()
    outs = []
    for i in range(2):
        dest = os.path.join(tmp, "c%d.json" % i)
        env = dict(os.environ, VCO_REDUCED="1", VCO_OUT=dest)
        subprocess.run([sys.executable, MODPATH], cwd=HERE, env=env,
                       check=True, capture_output=True)
        with open(dest, "rb") as fh:
            outs.append(fh.read())
    shutil.rmtree(tmp, ignore_errors=True)
    assert outs[0] == outs[1]
    cert = json.loads(outs[0])
    assert cert["onset_bound"]["max_M_below_2^71"] is True
    assert cert["odd_x_scan"]["survivors_above_1"] == []


def _main():
    fns = [(k, v) for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    bad = 0
    for name, fn in fns:
        try:
            fn()
            print("PASS %s" % name)
        except AssertionError as exc:
            bad += 1
            print("FAIL %s: %s" % (name, exc))
    print("%d/%d passed" % (len(fns) - bad, len(fns)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(_main())
