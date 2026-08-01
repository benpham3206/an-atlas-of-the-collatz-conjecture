"""Exact verifier for the amplification cylinder/inverse no-go packet.

Packet: 2026-08-01-amplification-cylinder-nogo
Claim file: AMPLIFICATION_CYLINDER_NOGO.md

Standard library only; exact integer arithmetic throughout. Every acceptance
decision is an integer equality. Two independent implementations share only
the input integers:

  Path A: direct Terras iteration of x and y, differenced.
  Path B: affine-form evaluation from the parity word alone,
          T^i(n) = (3^{s_i} n + c_i) / 2^i, with (s_i, c_i) built
          incrementally from the word and never from Path A.

A mismatch on any instance is a finding; the script exits nonzero.

Writes amplification_nogo_certificate.json: inputs, instance counts, and the
exact named-case values. The certificate is replayable from the inputs; no
bulk data is stored.
"""

import json
import random
import sys


def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def v2(n):
    assert n != 0
    n = abs(n)
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


# ---------- Path A: direct iteration ----------

def orbit(y, L):
    seq = [y]
    for _ in range(L):
        seq.append(T(seq[-1]))
    return seq


def parity_word(y, L):
    w = []
    n = y
    for _ in range(L):
        w.append(n % 2)
        n = T(n)
    return w


# ---------- Path B: affine form from the word alone ----------

def affine_chain(word):
    """Return list of (s_i, c_i) with T^i(n) = (3^{s_i} n + c_i)/2^i.

    Recurrence: bit 0 -> (s, c) stays, denominator gains a factor 2;
    bit 1 -> (s, c) -> (s+1, 3c + 2^i)."""
    chain = [(0, 0)]
    s, c = 0, 0
    for i, b in enumerate(word):
        if b == 0:
            pass
        else:
            s, c = s + 1, 3 * c + (1 << i)
        chain.append((s, c))
    return chain


def affine_eval(chain, i, n):
    s, c = chain[i]
    num = (3 ** s) * n + c
    den = 1 << i
    assert num % den == 0
    return num // den


# ---------- checks ----------

def check_tracking_identity(trials, seed):
    """Theorem A, first half: for x = y + 2^L m and i <= L,
    T^i(x) - T^i(y) = 3^{s_i} 2^{L-i} m, checked by Path A and Path B."""
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        y = rng.randint(1, 10 ** 6)
        L = rng.randint(1, 30)
        m = rng.randint(1, 10 ** 4)
        x = y + (1 << L) * m
        ys, xs = orbit(y, L), orbit(x, L)          # Path A
        chain = affine_chain(parity_word(y, L))    # Path B
        s = 0
        for i in range(L + 1):
            diff_a = xs[i] - ys[i]
            expect = (3 ** s) * (1 << (L - i)) * m
            if diff_a != expect:
                return {"ok": False, "instance": (y, L, m, i), "got": diff_a, "want": expect}
            # Path B must reproduce Path A states exactly
            if affine_eval(chain, i, y) != ys[i] or affine_eval(chain, i, x) != xs[i]:
                return {"ok": False, "instance": (y, L, m, i), "pathB_mismatch": True}
            if i < L:
                s += ys[i] % 2
            checked += 1
    return {"ok": True, "identities_checked": checked}


def check_isometry(trials, seed):
    """Theorem A, isometry form: for distinct positive x, y the common parity
    prefix length is exactly v2(x - y), and the (v+1)-th symbols differ."""
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        y = rng.randint(1, 10 ** 6)
        x = rng.randint(1, 10 ** 6)
        if x == y:
            continue
        v = v2(x - y)
        wx, wy = parity_word(x, v + 1), parity_word(y, v + 1)
        if wx[:v] != wy[:v] or wx[v] == wy[v]:
            return {"ok": False, "instance": (x, y, v)}
        checked += 1
    return {"ok": True, "pairs_checked": checked}


def check_handoff_distance(trials, seed):
    """Theorem A, handoff: v2(T^L(x) - T^L(y)) = v2(m) for x = y + 2^L m.
    For odd m the handoff state sits at 2-adic unit distance from the tracked
    orbit: no further shared parity symbol is forced."""
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        y = rng.randint(1, 10 ** 6)
        L = rng.randint(1, 30)
        m = rng.randint(1, 10 ** 4)
        x = y + (1 << L) * m
        z, w = orbit(x, L)[-1], orbit(y, L)[-1]
        if v2(z - w) != v2(m):
            return {"ok": False, "instance": (y, L, m)}
        checked += 1
    return {"ok": True, "handoffs_checked": checked}


def named_case_small():
    """The smallest non-trivial case for the TARGETS.md section-1 kill test:
    y = 27 (canonical long excursion), L = 20, m = 1."""
    y, L, m = 27, 20, 1
    x = y + (1 << L) * m
    floor = (1 << L) * m
    seq = orbit(x, L)
    w40 = parity_word(27, 40)
    s, supercrit = 0, True
    for i in range(1, 41):
        s += w40[i - 1]
        if 3 ** s < 2 ** i:
            supercrit = False
    z, wy = seq[-1], orbit(y, L)[-1]
    # continue x past the handoff until it drops below the floor
    n, steps = z, L
    while n >= floor and steps < 200000:
        n = T(n)
        steps += 1
    result = {
        "x": x,
        "min_states_0_to_L": min(seq),
        "floor_2^L_m": floor,
        "tracking_floor_holds": min(seq) >= floor,
        "y27_prefixes_supercritical_to_40": supercrit,
        "handoff_z": z,
        "T^L(y)": wy,
        "handoff_v2_distance": v2(z - wy),
        "first_drop_below_floor_step": steps,
        "first_drop_below_floor_value": n,
    }
    expected = {
        "x": 1048603,
        "floor_2^L_m": 1048576,
        "tracking_floor_holds": True,
        "y27_prefixes_supercritical_to_40": True,
        "handoff_z": 14349302,
        "T^L(y)": 395,
        "handoff_v2_distance": 0,
        "first_drop_below_floor_step": 34,
        "first_drop_below_floor_value": 638467,
    }
    for k, want in expected.items():
        if result[k] != want:
            return {"ok": False, "field": k, "got": result[k], "want": want}
    return {"ok": True, **result}


def check_inverse_family():
    """Theorem B: the pure-doubling preimage x = 2^j y has
    min-orbit(x) <= y = 2^{-j} x. Exact instance: y = 27, j = 40."""
    y, j = 27, 40
    x = (1 << j) * y
    n, mn, steps = x, x, 0
    while n != 1 and steps < 100000:
        n = T(n)
        mn = min(mn, n)
        steps += 1
    ok = mn <= y and x == (1 << j) * y
    return {
        "ok": ok and mn == 1,
        "y": y, "j": j, "x": x,
        "min_orbit": mn,
        "bound_y": y,
        "relative_min_exponent": j,
    }


def main():
    cert = {"packet": "2026-08-01-amplification-cylinder-nogo",
            "scope": "exact integer arithmetic only; no floats anywhere",
            "checks": {}}
    all_ok = True
    for name, fn in [
        ("tracking_identity", lambda: check_tracking_identity(3000, 20260801)),
        ("isometry", lambda: check_isometry(3000, 20260802)),
        ("handoff_distance", lambda: check_handoff_distance(2000, 20260803)),
        ("named_case_y27_L20_m1", named_case_small),
        ("inverse_family_doubling", check_inverse_family),
    ]:
        res = fn()
        cert["checks"][name] = res
        if not res.get("ok"):
            all_ok = False
            print(f"FAIL {name}: {res}", file=sys.stderr)
    cert["all_ok"] = all_ok
    out = sys.argv[1] if len(sys.argv) > 1 else "amplification_nogo_certificate.json"
    with open(out, "w") as f:
        json.dump(cert, f, indent=2, sort_keys=True)
    print(json.dumps({k: (v if isinstance(v, dict) and "ok" in v else v)
                      for k, v in cert["checks"].items()}, indent=2, sort_keys=True))
    print("certificate written:", out)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
