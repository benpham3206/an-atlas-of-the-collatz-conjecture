#!/usr/bin/env python3
"""Exact rational bracket for the Hausdorff dimension of the surviving set.

After the 2026-07-25 priority search the remaining symbolic gap is

    G = { q in {0,1}^N : liminf_L s_L(q)/L = alpha },   alpha = log_3 2,

where s_L is the number of ones in the first L symbols.  Besicovitch (1934)
and Eggleston (1949) give the Hausdorff dimension of the level set on which
the frequency EXISTS and equals p:

    dim_H { q : lim s_L/L = p }  =  H(p) = -p log_2 p - (1-p) log_2 (1-p).

That level set is contained in G, so dim_H(G) >= H(alpha).  This file
brackets H(alpha) by exact rational bounds.

Method -- every decision is an integer comparison, no floats on the
certificate path:

  * alpha:      a/b < alpha  <=>  3^a < 2^b.
  * -log_2(x):  for x = p/q in (0,1) and a candidate bound c/d > 0,
                    -log_2(x) >= c/d  <=>  x <= 2^(-c/d)
                                      <=>  x^d * 2^c <= 1
                                      <=>  p^d * 2^c <= q^d.
    The candidate c/d is GUESSED with floating point and then VERIFIED by
    that integer comparison, so the guess never has to be trusted.
  * H is assembled by interval arithmetic on Fractions, using that
    L(x) = -log_2 x is decreasing and that alpha > 1/2.

Run:  python3 contribution/code/dimension_bracket.py
"""

import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PREC = int(os.environ.get("DIM_PREC", "200000"))  # denominator scale of guesses


class Fail(Exception):
    """A check that must hold and did not."""


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------------------
# alpha = log_3 2, bracketed by continued-fraction convergents
# ---------------------------------------------------------------------------

def cmp_frac_alpha(fr):
    """-1, 0, +1 as a/b is below, equal to, or above alpha = log_3 2.

    a/b < log_3 2  <=>  (a/b) log 3 < log 2  <=>  3^a < 2^b.
    """
    a, b = fr.numerator, fr.denominator
    lhs, rhs = 3 ** a, 2 ** b
    return -1 if lhs < rhs else (1 if lhs > rhs else 0)


# convergents of log_3 2 (landmark memo, Part VII.2)
ALPHA_CONVERGENTS = [Fraction(2, 3), Fraction(5, 8), Fraction(12, 19),
                     Fraction(41, 65), Fraction(53, 84), Fraction(306, 485),
                     Fraction(665, 1054), Fraction(15601, 24727)]


def alpha_bracket():
    """Tightest certified (lo, hi) with lo < alpha < hi."""
    lo = hi = None
    for fr in ALPHA_CONVERGENTS:
        c = cmp_frac_alpha(fr)
        need(c != 0, "a convergent equals alpha: unique factorization broken")
        if c < 0:
            lo = fr if lo is None or fr > lo else lo
        else:
            hi = fr if hi is None or fr < hi else hi
    need(lo is not None and hi is not None, "alpha bracket incomplete")
    need(lo < hi, "alpha bracket is inverted")
    return lo, hi


# ---------------------------------------------------------------------------
# exact bracket for L(x) = -log_2(x),  0 < x < 1
# ---------------------------------------------------------------------------

def _certified_lower(x, c, d):
    """True iff -log_2(x) >= c/d, by the integer test p^d * 2^c <= q^d."""
    p, q = x.numerator, x.denominator
    return p ** d * 2 ** c <= q ** d


def _certified_upper(x, c, d):
    """True iff -log_2(x) <= c/d, by the integer test p^d * 2^c >= q^d."""
    p, q = x.numerator, x.denominator
    return p ** d * 2 ** c >= q ** d


def neg_log2_bracket(x, prec=PREC):
    """(lo, hi) Fractions with lo <= -log_2(x) <= hi, both certified by an
    exact integer comparison.  The starting guess uses float64 and is then
    verified; a wrong guess is corrected, never trusted."""
    need(0 < x < 1, "neg_log2_bracket needs 0 < x < 1")
    guess = -math.log2(float(x))
    d = prec
    c = int(guess * d)
    # walk down until the lower bound certifies
    lo_c = c
    while not _certified_lower(x, lo_c, d):
        lo_c -= 1
        need(lo_c > 0, "lower bound search fell through zero")
    # walk up until the upper bound certifies
    hi_c = lo_c + 1
    while not _certified_upper(x, hi_c, d):
        hi_c += 1
        need(hi_c < 100 * d, "upper bound search diverged")
    lo, hi = Fraction(lo_c, d), Fraction(hi_c, d)
    need(lo <= hi, "neg_log2 bracket inverted")
    return lo, hi


# ---------------------------------------------------------------------------
# H(p) = p*L(p) + (1-p)*L(1-p),  L = -log_2,  assembled by interval arithmetic
# ---------------------------------------------------------------------------

def entropy_bracket(plo, phi, prec=PREC):
    """(H_lo, H_hi) for H(p) valid for every p in [plo, phi] subset (1/2, 1).

    L is decreasing, so on [plo, phi]:
        L(p)   in [L(phi),     L(plo)]
        L(1-p) in [L(1-plo),   L(1-phi)]
    and p in [plo, phi], 1-p in [1-phi, 1-plo], all factors positive.
    """
    need(Fraction(1, 2) < plo <= phi < 1, "entropy_bracket needs 1/2 < p < 1")
    L_plo_lo, L_plo_hi = neg_log2_bracket(plo, prec)
    L_phi_lo, L_phi_hi = neg_log2_bracket(phi, prec)
    L_qlo_lo, L_qlo_hi = neg_log2_bracket(1 - plo, prec)
    L_qhi_lo, L_qhi_hi = neg_log2_bracket(1 - phi, prec)
    H_lo = plo * L_phi_lo + (1 - phi) * L_qlo_lo
    H_hi = phi * L_plo_hi + (1 - plo) * L_qhi_hi
    need(H_lo <= H_hi, "entropy bracket inverted")
    return H_lo, H_hi


def main():
    a_lo, a_hi = alpha_bracket()
    need(cmp_frac_alpha(a_lo) == -1, "alpha lower bound is not below alpha")
    need(cmp_frac_alpha(a_hi) == 1, "alpha upper bound is not above alpha")
    need(a_lo > Fraction(1, 2), "alpha bracket must sit above 1/2")

    H_lo, H_hi = entropy_bracket(a_lo, a_hi)

    # independent control: float64 evaluation must land inside the bracket.
    # This is a CONTROL, not the certificate.
    af = math.log(2) / math.log(3)
    Hf = -af * math.log2(af) - (1 - af) * math.log2(1 - af)
    need(float(H_lo) <= Hf <= float(H_hi),
         "float64 control fell outside the exact bracket")

    # the bracket must be tight enough to be worth quoting
    need(H_hi - H_lo < Fraction(1, 100000), "bracket too loose to report")

    cert = {
        "packet": "dimension of the surviving set",
        "statement": (
            "G = {q : liminf s_L/L = alpha} contains the Besicovitch-Eggleston "
            "level set {q : lim s_L/L = alpha}, whose Hausdorff dimension is "
            "H(alpha); hence dim_H(G) >= H(alpha)."),
        "alpha_bracket": {"lo": str(a_lo), "hi": str(a_hi),
                          "lo_witness": "3^%d < 2^%d" % (a_lo.numerator,
                                                         a_lo.denominator),
                          "hi_witness": "3^%d > 2^%d" % (a_hi.numerator,
                                                         a_hi.denominator)},
        "H_alpha_bracket": {"lo": str(H_lo), "hi": str(H_hi),
                            "lo_decimal": "%.9f" % float(H_lo),
                            "hi_decimal": "%.9f" % float(H_hi),
                            "note": ("decimals are renderings of the exact "
                                     "rational bounds, not the certificate")},
        "guess_denominator": PREC,
        "float64_control": "%.12f" % Hf,
        "method": ("every bound certified by an integer comparison: "
                   "a/b < log_3 2 iff 3^a < 2^b; -log_2(p/q) >= c/d iff "
                   "p^d * 2^c <= q^d"),
    }
    path = os.path.join(HERE, "dimension_bracket_certificate.json")
    with open(path, "w") as fh:
        fh.write(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: cert[k] for k in
                      ("alpha_bracket", "H_alpha_bracket", "float64_control")},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fail as exc:
        print("CHECK FAILED: %s" % exc, file=sys.stderr)
        sys.exit(2)
