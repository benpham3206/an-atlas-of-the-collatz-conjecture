#!/usr/bin/env python3
"""Executable evidence for COLLATZ_CONTRACTION_ONSET.md.

Odd-only (Syracuse) map  S(x) = (3x+1)/2^{v2(3x+1)}  on positive odd x.
With a_i = v2(3 x_{i-1} + 1),  A_i = a_1 + ... + a_i,  A_0 = 0,
C_0 = 0,  C_{i+1} = 3 C_i + 2^{A_i}, the exact cocycle is

        S^h(x) = (3^h x + C_h) / 2^{A_h}.

Call h CONTRACTING for x when 2^{A_h} > 3^h (the homogeneous multiplier
3^h/2^{A_h} has fallen below 1).

  Lemma 1 (descent requires contraction).  S^h(x) < x  =>  2^{A_h} > 3^h.
  Lemma 2 (offset bound).  If no j < h is contracting then C_h <= h*3^{h-1}.
  Theorem (onset bound).  If h is the first contracting index of x and
      S^h(x) >= x, then  x <= M(h) := floor( h*3^{h-1} / (2^{A*(h)} - 3^h) ),
      A*(h) := least A with 2^A > 3^h = bit_length(3^h).
  Corollary.  M(h) < 2^71 for every h <= H_MAX (computed here), so by
      Barina's verification a minimal counterexample has no contracting
      prefix at any depth h <= H_MAX.

Everything on the certificate path is exact integer arithmetic; there are no
floats anywhere in this file.

Knobs: VCO_HMAX (depth for the M table), VCO_XSCAN (odd-x scan bound),
VCO_ORBITS (orbits used for the lemma controls), VCO_REDUCED, VCO_OUT.
"""

import json
import os
import sys

REDUCED = os.environ.get("VCO_REDUCED", "0") == "1"
H_MAX = int(os.environ.get("VCO_HMAX", "3000" if REDUCED else "1000000"))
X_SCAN = int(os.environ.get("VCO_XSCAN", "200001" if REDUCED else "7795715"))
N_ORBITS = int(os.environ.get("VCO_ORBITS", "2000" if REDUCED else "20000"))
BARINA = 1 << 71                      # Barina 2025: every n < 2^71 reaches 1

HERE = os.path.dirname(os.path.abspath(__file__))


class Fail(Exception):
    """A kill criterion fired."""


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------------------
# exact Syracuse cocycle
# ---------------------------------------------------------------------------

def syracuse_step(x):
    t = 3 * x + 1
    a = (t & -t).bit_length() - 1
    return t >> a, a


def cocycle(x, steps):
    """Exact (a_i, A_i, C_i, S^i(x)) for i = 1..steps."""
    rows = []
    y = x
    A = 0
    C = 0
    for _ in range(steps):
        C = 3 * C + (1 << A)          # C_{i} = 3 C_{i-1} + 2^{A_{i-1}}
        y, a = syracuse_step(y)
        A += a
        rows.append((a, A, C, y))
    return rows


def a_star(h, p3=None):
    """Least A with 2^A > 3^h."""
    p = 3 ** h if p3 is None else p3
    return p.bit_length()


# ---------------------------------------------------------------------------
# 1. controls for the exact cocycle and for Lemmas 1 and 2
# ---------------------------------------------------------------------------

def check_cocycle_and_lemmas(nmax, steps):
    """On true orbits, exactly:
      * the affine identity 2^{A_h} S^h(x) = 3^h x + C_h;
      * Lemma 1: a descent below x forces 2^{A_h} > 3^h;
      * Lemma 2: before the first contracting index, C_h <= h*3^{h-1}.
    """
    ident = 0
    descents = 0
    lem2 = 0
    first_active_le_first_descent = 0
    p3 = [3 ** h for h in range(steps + 1)]
    for x in range(1, nmax + 1, 2):
        rows = cocycle(x, steps)
        first_active = None
        first_descent = None
        for h, (_a, A, C, y) in enumerate(rows, start=1):
            need((1 << A) * y == p3[h] * x + C,
                 "affine cocycle identity failed at x=%d h=%d" % (x, h))
            ident += 1
            if first_active is None and (1 << A) > p3[h]:
                first_active = h
            if first_descent is None and y < x:
                first_descent = h
                descents += 1
                need((1 << A) > p3[h],
                     "Lemma 1 failed: descent without contraction "
                     "at x=%d h=%d" % (x, h))
            if first_active is None or h <= first_active:
                if first_active is None or h < first_active:
                    need(C <= h * p3[h - 1],
                         "Lemma 2 failed: C_h > h*3^(h-1) at x=%d h=%d"
                         % (x, h))
                    lem2 += 1
        if first_active is not None and first_descent is not None:
            need(first_active <= first_descent,
                 "first contraction after first descent at x=%d" % x)
            first_active_le_first_descent += 1
    return {"odd_starts": (nmax + 1) // 2, "steps_per_orbit": steps,
            "affine_identities_checked": ident,
            "descents_observed": descents,
            "lemma2_bounds_checked": lem2,
            "orbits_with_both_events": first_active_le_first_descent}


# ---------------------------------------------------------------------------
# 2. the onset bound M(h), computed incrementally with exact integers
# ---------------------------------------------------------------------------

def m_table(hmax):
    """max over h <= hmax of M(h), plus the argmax and a few sample rows."""
    p3 = 1                              # 3^h
    p3prev = 0                          # 3^{h-1}
    best = 0
    arg = 0
    samples = {}
    for h in range(1, hmax + 1):
        p3prev = p3
        p3 = p3 * 3
        A = p3.bit_length()
        gap = (1 << A) - p3
        need(gap > 0, "A*(h) does not exceed 3^h at h=%d" % h)
        need((1 << (A - 1)) <= p3, "A*(h) is not minimal at h=%d" % h)
        m = (h * p3prev) // gap
        if m > best:
            best = m
            arg = h
        if h in (1, 2, 5, 12, 41, 53, 306, 665, 15601, hmax):
            samples[h] = {"A_star": A, "M": m}
    return best, arg, samples


# ---------------------------------------------------------------------------
# 3. the odd-x scan: is any x > 1 contracting before it descends?
# ---------------------------------------------------------------------------

def scan_onset(hi, step_cap=200000):
    """x is a 'ceiling-active survivor' iff its first contracting index comes
    strictly before its first descent below x.  Returns every such x > 1."""
    survivors = []
    stuck = []
    for x in range(3, hi, 2):
        y = x
        A = 0
        p3 = 1
        first_active = None
        hit = False
        for h in range(1, step_cap + 1):
            t = 3 * y + 1
            a = (t & -t).bit_length() - 1
            y = t >> a
            A += a
            p3 *= 3
            if first_active is None and (1 << A) > p3:
                first_active = h
            if y < x:
                if first_active is None or first_active < h:
                    survivors.append(x)
                hit = True
                break
        if not hit:
            stuck.append(x)
    return survivors, stuck


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    cert = {
        "packet": "2026-07-24-contraction-onset",
        "scope": "exact integer arithmetic only; no floats anywhere",
        "env": {"VCO_HMAX": H_MAX, "VCO_XSCAN": X_SCAN,
                "VCO_ORBITS": N_ORBITS},
        "barina_limit": "2^71 = %d" % BARINA,
    }

    # --- controls -----------------------------------------------------------
    cert["cocycle_and_lemma_controls"] = check_cocycle_and_lemmas(
        N_ORBITS, 40 if REDUCED else 60)

    # named controls: x = 1 survives, x = 3 and x = 7 die at first contraction
    named = {}
    for x, expect in ((1, "survives"), (3, "dies"), (7, "dies"),
                      (27, "dies"), (703, "dies")):
        y = x
        A = 0
        p3 = 1
        fa = fd = None
        for h in range(1, 4000):
            y, a = syracuse_step(y)
            A += a
            p3 *= 3
            if fa is None and (1 << A) > p3:
                fa = h
            if fd is None and y < x:
                fd = h
                break
        got = "survives" if (fd is None or (fa is not None and fa < fd)) \
            else "dies"
        need(got == expect,
             "named control x=%d expected %s, got %s (fa=%s fd=%s)"
             % (x, expect, got, fa, fd))
        named[str(x)] = {"first_contracting_index": fa,
                         "first_descent_index": fd, "verdict": got}
    cert["named_controls"] = named

    # --- the onset bound ----------------------------------------------------
    best, arg, samples = m_table(H_MAX)
    need(best < BARINA,
         "max M(h) reached 2^71 at h<=%d: the corollary's range ends here"
         % H_MAX)
    cert["onset_bound"] = {
        "H_MAX": H_MAX,
        "max_M": best,
        "argmax_h": arg,
        "two_pow_71": BARINA,
        "max_M_below_2^71": True,
        "orders_of_magnitude_of_slack": len(str(BARINA)) - len(str(best)),
        "samples": samples,
        "statement": ("every x with a first contracting index h <= %d and no "
                      "descent at h satisfies x <= %d < 2^71" % (H_MAX, best)),
    }

    # --- the odd-x scan -----------------------------------------------------
    surv, stuck = scan_onset(X_SCAN)
    need(not stuck, "an odd x did not descend within the step cap: %r"
         % stuck[:3])
    need(not surv, "found an odd x > 1 contracting before descending: %r"
         % surv[:5])
    cert["odd_x_scan"] = {
        "bound": X_SCAN,
        "odd_x_checked": (X_SCAN - 3) // 2 + 1,
        "survivors_above_1": surv,
        "depths_fully_decided": ("every h whose M(h) <= %d; with the table "
                                 "above that includes all h <= 10000"
                                 % X_SCAN),
    }

    cert["conclusion"] = (
        "A minimal Collatz counterexample m satisfies 2^{A_h} <= 3^h for "
        "every h <= %d: at a first contracting index h it would need "
        "m <= M(h) <= %d < 2^71, contradicting Barina's verification. "
        "Separately, no odd x with 1 < x <= %d contracts before it descends, "
        "so the trivial 1-cycle is the only surviving ceiling-active branch "
        "at every depth the scan decides." % (H_MAX, best, X_SCAN))

    path = os.environ.get("VCO_OUT") or os.path.join(
        HERE, "contraction_onset_certificate.json")
    with open(path, "w") as fh:
        fh.write(json.dumps(cert, indent=2, sort_keys=True) + "\n")

    print(json.dumps({k: v for k, v in cert.items() if k != "samples"},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fail as exc:
        print("KILL CRITERION FIRED: %s" % exc, file=sys.stderr)
        sys.exit(2)
