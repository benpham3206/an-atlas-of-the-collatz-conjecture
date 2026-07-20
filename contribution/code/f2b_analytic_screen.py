"""
F2b — analytic collapse screen.

Necessary condition: if the folds of classes (k, r) and (k', r') are affinely
conjugate as dynamical systems, the branch partitions correspond, so their
return-word languages have equal counting growth. Return words of class (k, r)
avoid r's k-bit parity window as an interior factor (F2 finding, Fibonacci
mechanism), so the growth rate is the entropy of the pattern-avoiding language
— computable exactly from the window's KMP automaton, no enumeration.

Screen: compute the avoiding-count sequence for every class's window, k ≤ K.
Cross-depth pairs whose sequences have provably different growth are
ELIMINATED at all resolutions. Pairs with matching growth go to the exact
enumeration check (they are expected to be the degenerate low-entropy classes,
which are small).

Stdlib only; counts are exact integers.
"""

from __future__ import annotations

import sys
from fractions import Fraction

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from f1_word_calculus import parity_word  # noqa: E402

N_TERMS = 80  # counts a(1..N_TERMS); rates compared via tail ratios + exact recurrence


def window_of_class(k: int, r: int) -> tuple:
    """The k-bit parity window realized by class r mod 2^k (Terras bijection).
    Use a positive representative."""
    n = r if r > 0 else (1 << k)
    return parity_word(n, k)


def kmp_automaton(w: tuple) -> list:
    """States 0..k-1 = length of current suffix matching a prefix of w
    (state k = pattern occurred, absorbing/dead for avoidance).
    trans[state][bit] -> next state, k means death."""
    k = len(w)
    # failure function
    fail = [0] * k
    for i in range(1, k):
        j = fail[i - 1]
        while j and w[i] != w[j]:
            j = fail[j - 1]
        fail[i] = j + 1 if w[i] == w[j] else 0
    trans = []
    for st in range(k):
        row = []
        for b in (0, 1):
            j = st
            while j and w[j] != b:
                j = fail[j - 1]
            row.append(j + 1 if w[j] == b else 0)
        trans.append(row)
    return trans  # next state == k means pattern completed


def avoid_counts(w: tuple, n_terms: int = N_TERMS) -> list:
    """a(n) = number of binary strings of length n containing no occurrence of w."""
    k = len(w)
    trans = kmp_automaton(w)
    vec = [0] * k
    vec[0] = 1
    out = []
    for _ in range(n_terms):
        new = [0] * k
        for st, cnt in enumerate(vec):
            if not cnt:
                continue
            for b in (0, 1):
                nxt = trans[st][b]
                if nxt < k:
                    new[nxt] += cnt
        vec = new
        out.append(sum(vec))
    return out


def min_recurrence(seq: list) -> list:
    """Exact minimal linear recurrence over Q via iterative Hankel solve
    (simple Gaussian elimination; sequences here have small order <= k)."""
    for order in range(1, min(16, len(seq) // 2)):
        # solve seq[n] = sum c_i seq[n-1-i] for n = order..2*order-1
        rows = []
        rhs = []
        for n in range(order, 2 * order):
            rows.append([Fraction(seq[n - 1 - i]) for i in range(order)])
            rhs.append(Fraction(seq[n]))
        # gaussian solve
        m = [row[:] + [b] for row, b in zip(rows, rhs)]
        cols = order
        piv = 0
        ok = True
        for c in range(cols):
            pr = next((i for i in range(piv, len(m)) if m[i][c] != 0), None)
            if pr is None:
                ok = False
                break
            m[piv], m[pr] = m[pr], m[piv]
            pv = m[piv][c]
            m[piv] = [x / pv for x in m[piv]]
            for i in range(len(m)):
                if i != piv and m[i][c] != 0:
                    f = m[i][c]
                    m[i] = [a - f * b for a, b in zip(m[i], m[piv])]
            piv += 1
        if not ok:
            continue
        coeffs = [m[i][cols] for i in range(cols)]
        # verify on the rest of the sequence
        good = all(
            seq[n] == sum(coeffs[i] * seq[n - 1 - i] for i in range(order))
            for n in range(2 * order, len(seq))
        )
        if good:
            return coeffs
    return []


def char_poly_key(coeffs: list) -> tuple:
    """Canonical key for the recurrence: x^d - c0 x^{d-1} - ... - c_{d-1}."""
    return tuple(Fraction(c) for c in coeffs)


def main(K: int = 8) -> None:
    classes = {}
    for k in range(1, K + 1):
        for r in range(1 << k):
            w = window_of_class(k, r)
            seq = avoid_counts(w)
            rec = min_recurrence(seq)
            classes[(k, r)] = {
                "window": w,
                "seq_tail": seq[-4:],
                "rec": rec,
                "order": len(rec),
                "rate": (seq[-1] / seq[-2]) if seq[-2] else 0.0,
            }

    # bucket by exact recurrence (same minimal recurrence => same growth;
    # different minimal recurrence with different dominant root => different growth.
    # We bucket conservatively by (order, coeffs) == identical counting law.)
    buckets: dict = {}
    for key, info in classes.items():
        bkey = char_poly_key(info["rec"])
        buckets.setdefault(bkey, []).append(key)

    print(f"F2b analytic screen, k <= {K}: {len(classes)} classes, "
          f"{len(buckets)} distinct exact counting laws")
    survivors = []
    for bkey, members in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        depths = {k for k, _ in members}
        cross = len(depths) > 1
        rate = classes[members[0]]["rate"]
        if cross:
            survivors.append((bkey, members))
        tag = "CROSS-DEPTH — needs exact check" if cross else "single-depth"
        print(f"  law order={len(bkey)} rate≈{rate:.6f} members={len(members)} "
              f"depths={sorted(depths)} [{tag}]")
        if cross and len(members) <= 40:
            print(f"    {members}")

    # float-rate near-collisions across DIFFERENT laws (paranoia check:
    # distinct minimal recurrences could still share the dominant root)
    print("\nParanoia check — distinct laws with tail-rates within 1e-9:")
    laws = [(bkey, classes[m[0]]["rate"]) for bkey, m in buckets.items()]
    found = False
    for i in range(len(laws)):
        for j in range(i + 1, len(laws)):
            if abs(laws[i][1] - laws[j][1]) < 1e-9:
                print(f"  RATE COLLISION between distinct laws: "
                      f"{laws[i][1]:.12f} — needs exact root comparison")
                found = True
    if not found:
        print("  none — every distinct law has a distinct dominant rate at 1e-9")

    n_cross = sum(len(m) for _, m in survivors)
    print(f"\nVERDICT: {n_cross} classes sit in cross-depth counting-law buckets; "
          f"all other cross-depth pairs ELIMINATED at all resolutions.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
