#!/usr/bin/env python3
"""Executable controls for COLLATZ_STRUCTURE_RANDOMNESS_TRANSFER.md.

Finite controls only:
  (1) exact integer certificates for log_3(2) < 2/3 and 63/100 < log_3(2);
  (2) exact density of the biased base-3 Champernowne word q* on a long
      prefix, certified above the drift wall;
  (3) exact certificate p_{q*}(k) = 2^k for k <= 12 (full complexity);
  (4) exact lift digits of Phi(q*) mod 2^N, N = 2^17, with a realizable
      periodic control (Phi = 1) and the aperiodic Fibonacci control.

Items (1)-(3) back Theorem 1 of the memo. Item (4) is openly a
hypothesis generator: no finite computation can certify an
eventually-zero lift tail.
"""

from fractions import Fraction
import json
import os
import sys

import numpy as np

# ----------------------------------------------------------------------------
# Critical-line certificates
# ----------------------------------------------------------------------------

def certify_critical_line():
    return {
        "log3_2_lt_2_over_3": 2**3 < 3**2,        # 8 < 9
        "63_over_100_lt_log3_2": 3**63 < 2**100,
        "log3_2_lt_631_over_1000": 2**1000 < 3**631,
    }


# ----------------------------------------------------------------------------
# The isolated test object q* = phi(C_3),  phi: 0,1 -> 1,  2 -> 0
# ----------------------------------------------------------------------------

MAP3 = (1, 1, 0)


def biased_champernowne(N):
    """First N symbols of q* = phi(base-3 Champernowne)."""
    out = []
    m = 1
    while len(out) < N:
        x = m
        digits = []
        while x:
            x, r = divmod(x, 3)
            digits.append(MAP3[r])
        out.extend(reversed(digits))
        m += 1
    return out[:N], m - 1


def fibonacci_word(N):
    w = [0]
    while len(w) < N:
        w = [b for a in w for b in ((0, 1) if a == 0 else (0,))]
    return w[:N]


# ----------------------------------------------------------------------------
# Density control (exact)
# ----------------------------------------------------------------------------

def density_control(word):
    s = sum(word)
    d = Fraction(s, len(word))
    bound = Fraction(631, 1000)  # certified > log_3 2
    return {
        "N": len(word),
        "ones": s,
        "density": str(d),
        "above_631_over_1000": d > bound,
        "two_thirds_gap": str(Fraction(2, 3) - d),
    }


# ----------------------------------------------------------------------------
# Full complexity certificate  p_{q*}(k) = 2^k  for k <= k_max
# ----------------------------------------------------------------------------

def full_complexity_certificate(k_max=12):
    # Numbers 1..3^k_max guarantee every ternary word of length k_max,
    # hence every binary word of each length k <= k_max in the image.
    need_numbers = 3**k_max
    approx_digits = (k_max + 1) * need_numbers
    word, used = biased_champernowne(approx_digits)
    n = len(word)
    Xp = np.concatenate([np.asarray(word, dtype=np.uint64),
                         np.zeros(k_max - 1, dtype=np.uint64)])
    # masks[i] packs word[i..i+k_max-1] into a uint64 (padding zeros at end)
    masks = Xp[:n].copy()
    for i in range(1, k_max):
        masks |= Xp[i:i + n] << i
    results = {}
    for k in range(1, k_max + 1):
        lowk = masks[:n - k + 1] & ((1 << k) - 1)
        count = int(np.unique(lowk).size)
        results[str(k)] = {"distinct_factors": count, "expected": 1 << k}
        assert count == (1 << k), k
    return {"k_max": k_max, "symbols_examined": n,
            "source_numbers": used, "per_k": results,
            "full_complexity_certified": True}


# ----------------------------------------------------------------------------
# Exact lift digits of Phi(q) mod 2^N
# ----------------------------------------------------------------------------

def phi_mod(word, N):
    """Phi(q) mod 2^N as an ordinary integer in [0, 2^N).

    Phi(q) = -sum_j 2^{d_j} 3^{-(j+1)}  (2-adically); only terms with
    d_j < N contribute mod 2^N. Shifts and masks instead of big
    multiply/divide: per-one cost is one N x N-bit Karatsuba multiply.
    """
    M = 1 << N
    MASK = M - 1
    inv3 = pow(3, -1, M)
    inv = inv3            # 3^{-(j+1)} for j = 0
    S = 0
    ones = 0
    for pos, bit in enumerate(word[:N]):
        if bit:
            S = (S + ((inv << pos) & MASK)) & MASK
            inv = (inv * inv3) & MASK
            ones += 1
    return (-S) & MASK, ones


def lift_stats(phi, N):
    ones = phi.bit_count()
    # longest runs over the N-bit window
    longest_zero = longest_one = run = 0
    prev = None
    for L in range(N):
        b = (phi >> L) & 1
        if b == prev:
            run += 1
        else:
            run = 1
            prev = b
        if b:
            longest_one = max(longest_one, run)
        else:
            longest_zero = max(longest_zero, run)
    top = phi.bit_length() - 1 if phi else -1
    return {
        "N": N,
        "one_digits": ones,
        "zero_digits": N - ones,
        "one_fraction": str(Fraction(ones, N)),
        "longest_zero_run": longest_zero,
        "longest_one_run": longest_one,
        "highest_set_digit": top,
        "has_set_digit_above_N_over_2": top > N // 2,
    }


def lift_digit_report(N):
    qstar, used = biased_champernowne(N)
    phi_star, ones_star = phi_mod(qstar, N)
    star = lift_stats(phi_star, N)
    star["word"] = "q* = phi(base-3 Champernowne)"
    star["prefix_ones"] = ones_star

    periodic = [1, 0] * (N // 2)
    phi_per, _ = phi_mod(periodic, N)
    per = {"word": "(10)^inf (parity transcript of n=1)",
           "phi_equals_1": phi_per == 1,
           "highest_set_digit": phi_per.bit_length() - 1}
    assert phi_per == 1

    fib = fibonacci_word(N)
    phi_fib, ones_fib = phi_mod(fib, N)
    fibs = lift_stats(phi_fib, N)
    fibs["word"] = "Fibonacci word (aperiodic control)"
    fibs["prefix_ones"] = ones_fib

    return {"test_object": star, "periodic_control": per,
            "fibonacci_control": fibs,
            "interpretation": "hypothesis generator only; finite lift "
                              "windows cannot certify eventually-zero tails"}


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    cert = {"packet": "2026-07-22-structure-randomness-transfer",
            "scope": "finite controls; Theorem 1 proved in memo; lift "
                     "statistics heuristic"}
    cert["critical_line"] = certify_critical_line()
    assert all(cert["critical_line"].values())

    N_density = int(os.environ.get("VSR_DENSITY_N", 1 << 20))
    word, _ = biased_champernowne(N_density)
    cert["density"] = density_control(word)
    assert cert["density"]["above_631_over_1000"]

    k_max = int(os.environ.get("VSR_KMAX", 12))
    cert["full_complexity"] = full_complexity_certificate(k_max)

    N_lift = int(os.environ.get("VSR_LIFT_N", 1 << 16))
    cert["lift_digits"] = lift_digit_report(N_lift)

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("structure_randomness_certificate.json", "w") as f:
        f.write(out + "\n")
    print(json.dumps({
        "status": "ok",
        "density": cert["density"]["density"],
        "full_complexity_through_k": k_max,
        "periodic_control_phi_equals_1": True,
        "qstar_highest_set_digit": cert["lift_digits"]["test_object"]["highest_set_digit"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
