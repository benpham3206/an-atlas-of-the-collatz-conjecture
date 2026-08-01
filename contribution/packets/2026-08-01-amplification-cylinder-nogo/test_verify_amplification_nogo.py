"""Standalone tests for the amplification no-go verifier.

Runs under pytest or directly:  python3 test_verify_amplification_nogo.py
Exact integer arithmetic only. Includes two RED-mutant checks: perturbing a
load-bearing relation must be caught.
"""

import verify_amplification_nogo as V


def test_tracking_identity_small():
    res = V.check_tracking_identity(200, 7)
    assert res["ok"], res


def test_isometry_small():
    res = V.check_isometry(200, 11)
    assert res["ok"], res


def test_handoff_distance_small():
    res = V.check_handoff_distance(200, 13)
    assert res["ok"], res


def test_named_case():
    res = V.named_case_small()
    assert res["ok"], res


def test_inverse_family():
    res = V.check_inverse_family()
    assert res["ok"], res


def test_affine_path_independent_of_direct_path():
    # Path B (affine form from the word) must reproduce Path A (direct
    # iteration) on a fixed structured instance with no shared machinery.
    y, L = 27, 20
    chain = V.affine_chain(V.parity_word(y, L))
    ys = V.orbit(y, L)
    for i in range(L + 1):
        assert V.affine_eval(chain, i, y) == ys[i]


def test_red_mutant_identity():
    # Perturb the expected identity by one step of L: it MUST fail.
    y, L, m = 27, 20, 1
    x = y + (1 << L) * m
    ys, xs = V.orbit(y, L), V.orbit(x, L)
    s = 0
    mutant_caught = False
    for i in range(L + 1):
        wrong = (3 ** s) * (1 << (L - i + 1)) * m  # mutant: L+1
        if xs[i] - ys[i] != wrong:
            mutant_caught = True
        if i < L:
            s += ys[i] % 2
    assert mutant_caught


def test_red_mutant_v2():
    # v2 must detect an off-by-one in the handoff valuation.
    assert V.v2(3 * 5 * 7) == 0
    assert V.v2(2 ** 9 * 27) == 9
    try:
        V.v2(0)
    except AssertionError:
        pass
    else:
        raise AssertionError("v2(0) must raise")


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} passed")
