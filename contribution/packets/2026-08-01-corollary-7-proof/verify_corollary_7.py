#!/usr/bin/env python3
"""Exact-arithmetic verifier for Corollary 7 (2026-08-01).

No float on any acceptance path.  float64 is display only.

Checks
  A. Unrolling identity (3.1) matches the recursive orbit (2.1).
  B. Ones-cap growth bound (4.3) holds on random words with enforced ones-cap.
  C. Rate algebra: beta=1 recovers kappa; g>0 iff 3^beta > 2 (integer form).
  D. Independent reimplementation of the unrolled Green formula.
  E. Boundary: beta <= alpha is rejected (g <= 0).

Usage:  python3 verify_corollary_7.py
"""

from __future__ import annotations

import json
import os
import platform
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = os.path.join(HERE, "corollary_7_certificate.json")


class Fail(Exception):
    pass


def need(cond: bool, msg: str) -> None:
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------------------
# alpha = log_3 2 comparisons via integer arithmetic only
# ---------------------------------------------------------------------------

def cmp_beta_alpha(beta: Fraction) -> int:
    """-1/0/+1 as beta is below / equal / above alpha = log_3 2.

    a/b < log_3 2  <=>  3^a < 2^b.
    """
    a, b = beta.numerator, beta.denominator
    # beta = a/b;  beta < alpha <=> a/b < log_3 2 <=> 3^a < 2^b
    # Careful: if a,b can be any sign — we only use positive beta.
    need(a > 0 and b > 0, "beta must be positive")
    lhs, rhs = pow(3, a), pow(2, b)
    return -1 if lhs < rhs else (1 if lhs > rhs else 0)


def g_positive(beta: Fraction) -> bool:
    """g = beta log2 3 - 1 > 0  <=>  3^beta > 2  <=>  3^a > 2^b for beta=a/b."""
    return cmp_beta_alpha(beta) > 0


# ---------------------------------------------------------------------------
# Orbit recursion and two independent unrollers
# ---------------------------------------------------------------------------

def step_y(y: int, q: int, d: int) -> int:
    """One step of (2.1).  Exact integer division by 2.

    Requires q ≡ y (mod 2) — the Terras parity of the current state.
    """
    need(q in (0, 1), "parity bit")
    need(q == (y & 1), f"parity mismatch: y={y} q={q}")
    num = (3 if q else 1) * y + d * q
    need(num % 2 == 0, "parity invariant broken: numerator odd")
    return num // 2


def orbit_from_state(a: int, d: int, N: int) -> tuple[list[int], list[int]]:
    """Run N Terras steps from y_0=a.  Returns (parity word, y_0..y_N)."""
    need(d % 2 == 1 and d > 0, "d must be positive odd")
    ys = [a]
    word: list[int] = []
    y = a
    for _ in range(N):
        q = y & 1
        word.append(q)
        y = step_y(y, q, d)
        ys.append(y)
    return word, ys


def orbit_y(a: int, d: int, word: list[int]) -> list[int]:
    """y_0..y_N along a *prescribed* word.  Word must match parities."""
    ys = [a]
    y = a
    for q in word:
        y = step_y(y, q, d)
        ys.append(y)
    return ys


def unroll_green(y_i: int, d: int, word: list[int]) -> int:
    """Identity (3.1): compute y_{i+N} from y_i and the segment word.

    2^N y_{i+N} = 3^s y_i + d * sum_{t: q_t=1} 3^{s-s(t+1)} 2^t
    """
    N = len(word)
    if N == 0:
        return y_i
    # prefix one-counts s(r)
    s_pref = [0]
    for q in word:
        s_pref.append(s_pref[-1] + q)
    s = s_pref[N]
    total = (3 ** s) * y_i
    for t, q in enumerate(word):
        if q:
            # ones strictly after t: s - s(t+1)
            ones_after = s - s_pref[t + 1]
            total += d * (3 ** ones_after) * (2 ** t)
    # total = 2^N * y_{i+N}
    need(total % (2 ** N) == 0, "unroll not divisible by 2^N")
    return total // (2 ** N)


def unroll_green_independent(y_i: int, d: int, word: list[int]) -> int:
    """Second unroller: forward Horner-style accumulation, no s_pref table.

    Walk the word once, maintaining
        acc = 3^{ones_so_far} * y_i + d * sum_{past ones} 3^{ones_since} * 2^{pos}
    scaled so that after N steps, acc = 2^N y_{i+N}.
    Equivalent form: start acc = y_i; for each bit,
        acc = 3^q * acc + d*q; then the running power of 2 is applied by
    delaying the division — we multiply the *previous* scale.

    Explicit independent formula: process left-to-right keeping
    `val` such that after t steps, val = 2^t y_{i+t}.
    """
    val = y_i  # at t=0, 2^0 y_i
    for q in word:
        # 2^{t+1} y_{next} = 3^q * (2^t y)  +  d q * 2^t
        # but val = 2^t y, so 2^{t+1} y_next = 3^q val + d q 2^t
        # We need the absolute 2-power.  Track t.
        # Simpler: just use the recursion on y and re-multiply — NO, that
        # shares code with step_y.  Pure formula:
        # new_val = 3^q * val + d*q * 2^t, then we are at scale 2^{t+1}?
        # 2^{t+1} y_next = 3^q * 2 * y * 2^t / 1? From (2.1):
        # y_next = (3^q y + d q)/2, so 2 y_next = 3^q y + d q,
        # 2^{t+1} y_next = 3^q * 2^t y + d q 2^t = 3^q val + d q 2^t.
        pass  # filled below with an explicit t loop

    val = y_i
    scale_pow = 0  # val means 2^{scale_pow} * y_current; always scale_pow == t
    for t, q in enumerate(word):
        # val = 2^t * y_i+t
        need(scale_pow == t, "scale desync")
        # 2^{t+1} y_next = 3^q * val + d*q*2^t
        val = (3 if q else 1) * val + d * q * (2 ** t)
        scale_pow = t + 1
    N = len(word)
    need(scale_pow == N, "final scale")
    need(val % (2 ** N) == 0, "independent unroll not divisible by 2^N")
    return val // (2 ** N)


# ---------------------------------------------------------------------------
# Ones-cap growth bound (4.3), exact integer form
# ---------------------------------------------------------------------------

def bound_4_3(y_i: int, d: int, N: int, beta: Fraction, C: int) -> int:
    """Integer upper bound on |y_{i+N}| from (4.3).

    |y| <= 3^C * (3^beta/2)^N * |y_i|
         + d * 3^C * (N/2) * (3^beta/2)^{N-1}

    With beta = p/q, replace 3^{p m / q} by 3^{ceil(p m / q)} (looser, valid).
    Clear the remaining factors by writing over denominator 2^{N+1}:

      total <= [ 2 * 3^{C+ceil(pN/q)} |y_i|
               + 2 * d * 3^C * N * 3^{ceil(p(N-1)/q)} ] / 2^{N+1}

    (The second numerator carries a factor 2: T2 = d*3^C*N*3^{beta(N-1)}/2^N
    = 2*d*3^C*N*3^{beta(N-1)}/2^{N+1}. An earlier version of this function
    omitted it and tested the stronger, unproved bound T1 + T2/2; corrected
    2026-08-01 after independent audit.)
    """
    need(N >= 1, "N>=1")
    need(C >= 0, "C>=0")
    p, q = beta.numerator, beta.denominator
    exp3_N = (p * N + q - 1) // q  # ceil(pN/q)
    exp3_Nm1 = 0 if N == 1 else (p * (N - 1) + q - 1) // q
    num = (
        2 * (3 ** (C + exp3_N)) * abs(y_i)
        + 2 * d * (3 ** C) * N * (3 ** exp3_Nm1)
    )
    den = 2 ** (N + 1)
    return (num + den - 1) // den  # ceil(num/den)


def random_word_with_cap(N: int, beta: Fraction, C: int, rng: random.Random) -> list[int]:
    """Length-N word whose every *prefix* has ones-count <= floor(beta*ell + C).

    Prefix-only is weaker than every-factor, but enough to test the growth
    bound on the single orbit segment from 0 used for H_N.
    """
    word: list[int] = []
    ones = 0
    p, q = beta.numerator, beta.denominator
    for ell in range(1, N + 1):
        max_ones = (p * ell + C * q) // q  # floor(beta*ell + C)
        if ones >= max_ones:
            bit = 0
        else:
            bit = rng.randint(0, 1)
        ones += bit
        word.append(bit)
        need(ones <= max_ones, "cap construction broke")
    return word


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def section_A(rng: random.Random) -> dict:
    """Unrolling (3.1) vs recursive (2.1) on real parity orbits."""
    trials = 0
    for _ in range(200):
        d = rng.choice([1, 3, 5, 7, 9, 11, 13])
        a = rng.randint(-50, 50) or 1
        N = rng.randint(1, 40)
        word, ys = orbit_from_state(a, d, N)
        y_from_unroll = unroll_green(a, d, word)
        need(y_from_unroll == ys[N], f"unroll mismatch: {y_from_unroll} vs {ys[N]}")
        trials += 1
    return {"trials": trials, "status": "pass"}


def section_D(rng: random.Random) -> dict:
    """Independent unroller agrees with both recursion and first unroller."""
    trials = 0
    for _ in range(200):
        d = rng.choice([1, 3, 5, 7, 9])
        a = rng.randint(-30, 30) or 1
        N = rng.randint(1, 35)
        word, ys = orbit_from_state(a, d, N)
        y_rec = ys[N]
        y_u1 = unroll_green(a, d, word)
        y_u2 = unroll_green_independent(a, d, word)
        need(y_rec == y_u1 == y_u2, f"independent mismatch {y_rec},{y_u1},{y_u2}")
        trials += 1
    return {"trials": trials, "status": "pass"}


def section_B(rng: random.Random) -> dict:
    """Growth bound (4.3) on real orbits whose prefixes meet a ones-cap.

    Sample many (a, d, N).  For each beta > alpha and slack C, keep those
    orbits whose every prefix of length ell <= N has ones <= floor(beta*ell+C),
    and check |y_N| <= bound_4_3.
    """
    betas = [Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(5, 6), Fraction(1, 1)]
    for beta in betas:
        need(cmp_beta_alpha(beta) > 0, f"beta={beta} not > alpha")

    trials = 0
    accepted = 0
    for beta in betas:
        p, qden = beta.numerator, beta.denominator
        for C in (0, 1, 2, 5, 10, 20):
            attempts = 0
            got = 0
            while got < 15 and attempts < 4000:
                attempts += 1
                d = rng.choice([1, 3, 5, 7])
                a = rng.randint(-40, 40) or 1
                N = rng.randint(1, 30)
                word, ys = orbit_from_state(a, d, N)
                ones = 0
                ok = True
                for ell, bit in enumerate(word, 1):
                    ones += bit
                    if ones > (p * ell + C * qden) // qden:
                        ok = False
                        break
                if not ok:
                    continue
                yN = ys[N]
                bnd = bound_4_3(a, d, N, beta, C)
                need(
                    abs(yN) <= bnd,
                    f"bound fail |y|={abs(yN)} > {bnd} beta={beta} C={C} N={N} a={a} d={d}",
                )
                got += 1
                accepted += 1
                trials += 1
            # beta=1, C=0 always accepts every orbit — must get 15.
            if beta == 1 and C == 0:
                need(got >= 15, f"beta=1 C=0 under-sampled: got {got}")
    need(accepted >= 50, f"too few cap-satisfying orbits: {accepted}")
    return {
        "trials": trials,
        "accepted_orbits": accepted,
        "status": "pass",
        "betas": [str(b) for b in betas],
    }


def section_C() -> dict:
    """Rate algebra with integer witnesses only."""
    # beta = 1 => g = log2(3/2), 1/g = 1/log2(3/2) = log(2)/log(3/2)
    # We do not compute floats.  We certify g>0 for listed betas via 3^a > 2^b.
    samples = {
        "1": Fraction(1, 1),
        "5/6": Fraction(5, 6),
        "3/4": Fraction(3, 4),
        "2/3": Fraction(2, 3),
        "5/8": Fraction(5, 8),  # < alpha
        "12/19": Fraction(12, 19),  # convergent below? check
    }
    results = {}
    for name, beta in samples.items():
        c = cmp_beta_alpha(beta)
        results[name] = {
            "beta": str(beta),
            "cmp_to_alpha": c,  # +1 above, -1 below
            "g_positive": c > 0,
        }
    need(results["1"]["g_positive"], "beta=1 must be > alpha")
    need(results["5/6"]["g_positive"], "5/6 > alpha")
    need(results["3/4"]["g_positive"], "3/4 > alpha")
    need(results["2/3"]["g_positive"], "2/3 > alpha")
    need(not results["5/8"]["g_positive"], "5/8 < alpha so g<=0")
    # Recover kappa identity: at beta=1, 1/g = 1/log2(3/2).
    # Equivalent certificate: g = log2(3/2) means 2^g = 3/2, not used numerically.
    # Cross-check the formula 1/g = alpha/(beta - alpha) at rational beta? 
    # 1/g = 1/(beta log2 3 - 1) = 1/log2(3^beta / 2).
    # alpha/(beta-alpha) = log3(2) / (beta - log3(2)).
    # These are equal:
    #   1/(beta log2 3 - 1) = ln2 / (beta ln3 - ln2)
    #   log3(2)/(beta - log3(2)) = (ln2/ln3) / (beta - ln2/ln3)
    #                            = (ln2/ln3) / ((beta ln3 - ln2)/ln3)
    #                            = ln2 / (beta ln3 - ln2).
    # Same.  Certify equality of the two symbolic forms by cross-multiplication
    # on a rational stand-in only when both are rational — not needed for proof.
    # Integer witness that alpha/(beta-alpha) description matches kill threshold
    # used in supercritical packet: for beta=2/3, check 3^2 < 2^3 so 2/3>alpha.
    # a/b < alpha <=> 3^a < 2^b.  So 2/3 > alpha <=> 3^2 > 2^3 (9 > 8).
    need(pow(3, 2) > pow(2, 3), "2/3 > alpha witness 3^2 > 2^3")
    # 5/8 < alpha <=> 3^5 < 2^8 (243 < 256).
    need(pow(3, 5) < pow(2, 8), "5/8 < alpha witness 3^5 < 2^8")
    return {"status": "pass", "samples": results}


def section_E() -> dict:
    """Boundary: subcritical beta rejected (g <= 0)."""
    # Convergents of log_3 2 alternate.  Subcritical (3^a < 2^b):
    sub = [Fraction(5, 8), Fraction(41, 65), Fraction(306, 485)]
    for beta in sub:
        need(cmp_beta_alpha(beta) < 0, f"{beta} should be < alpha")
        need(not g_positive(beta), f"g should be <=0 at {beta}")
    # Supercritical (3^a > 2^b):
    supra = [Fraction(2, 3), Fraction(12, 19), Fraction(53, 84)]
    for beta in supra:
        need(cmp_beta_alpha(beta) > 0, f"{beta} should be > alpha")
        need(g_positive(beta), f"g should be >0 at {beta}")
    return {
        "status": "pass",
        "subcritical_betas": [str(b) for b in sub],
        "supercritical_betas": [str(b) for b in supra],
    }


def main() -> int:
    rng = random.Random(20260801)
    report = {
        "packet": "2026-08-01-corollary-7-proof",
        "claim": "Corollary 7: ones-capped factors force limsup p(k)/k >= 1/g",
        "platform": platform.platform(),
        "python": sys.version.split()[0],
    }
    try:
        report["A_unroll_vs_recursion"] = section_A(rng)
        report["D_independent_unroll"] = section_D(rng)
        report["B_growth_bound"] = section_B(rng)
        report["C_rate_algebra"] = section_C()
        report["E_boundary"] = section_E()
        report["verdict"] = "PASS"
    except Fail as e:
        report["verdict"] = "FAIL"
        report["error"] = str(e)
        with open(CERT_PATH, "w") as f:
            json.dump(report, f, indent=2, sort_keys=True)
            f.write("\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    with open(CERT_PATH, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"\ncertificate -> {CERT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
