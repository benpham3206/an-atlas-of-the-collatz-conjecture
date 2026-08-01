"""Pytest wrapper for the Corollary 7 verifier."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "verify_corollary_7.py")


def test_verifier_exits_zero():
    proc = subprocess.run(
        [sys.executable, SCRIPT],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    assert '"verdict": "PASS"' in proc.stdout or '"verdict": "PASS"' in proc.stdout.replace(
        " ", ""
    )


def test_unroll_small_hand():
    """Hand check of identity (3.1) for N=1,2."""
    sys.path.insert(0, HERE)
    import verify_corollary_7 as v

    # N=1, q=0: y' = y/2; 2 y' = y
    assert v.unroll_green(10, d=1, word=[0]) == 5
    assert v.step_y(10, 0, 1) == 5
    # N=1, q=1: y' = (3y+d)/2
    assert v.unroll_green(7, d=1, word=[1]) == (3 * 7 + 1) // 2
    assert v.unroll_green_independent(7, d=1, word=[1]) == (3 * 7 + 1) // 2
    # N=2, word 10: y1=(3*7+1)/2=11; y2=11/2 — wait 11 odd, d=1, y1 must be odd when q0=1
    # 7 odd, q=1 -> (21+1)/2=11 odd; q=0 -> 11/2 not int. Use even after.
    # a=1,d=1, word=[1,0]: y0=1; y1=(3+1)/2=2; y2=1
    assert v.orbit_y(1, 1, [1, 0]) == [1, 2, 1]
    assert v.unroll_green(1, 1, [1, 0]) == 1
    assert v.unroll_green_independent(1, 1, [1, 0]) == 1
