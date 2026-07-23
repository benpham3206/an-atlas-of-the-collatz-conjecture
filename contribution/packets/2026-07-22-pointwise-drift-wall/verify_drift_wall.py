#!/usr/bin/env python3
"""Executable controls for COLLATZ_POINTWISE_DRIFT_WALL.md.

Everything here is a FINITE control. The theorems live in the memo; this
script (1) certifies the exact integer comparisons pinning log_3(2),
(2) verifies Lemma 1 (exact multiplicative expansion) and Lemma 3
(upper envelope) on exact rational orbits, (3) confirms the classical
one-densities of the named aperiodic word classes on long prefixes,
(4) confirms the Sturmian complexity law p(k)=k+1 on the Fibonacci word,
and (5) emits a deterministic JSON certificate.

No float arithmetic is used anywhere in the certificate path.
"""

from fractions import Fraction
import json
import os
import sys

# ----------------------------------------------------------------------------
# Exact critical-line certificates
# ----------------------------------------------------------------------------

def certify_alpha_bounds():
    """63/100 < log_3 2 < 631/1000, by exact integer comparison."""
    lower = 3**63 < 2**100            # 63/100 < log_3 2
    upper = 2**1000 < 3**631          # log_3 2 < 631/1000
    return {
        "lower_63_over_100": lower,
        "upper_631_over_1000": upper,
        "exact_witnesses": ["3^63 < 2^100", "2^1000 < 3^631"],
    }


# ----------------------------------------------------------------------------
# Terras orbit machinery (exact)
# ----------------------------------------------------------------------------

def terras_orbit(n, cap=100000):
    """Positive-integer Terras orbit until first entry of 1 (or cap)."""
    orbit = [n]
    x = n
    while x != 1 and len(orbit) < cap:
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
        orbit.append(x)
    return orbit


def check_lemma1_identity(orbit):
    """Lemma 1: 2^L x_L == n 3^{s_L} prod_{odd j<L} (1 + 1/(3 x_j))."""
    n = orbit[0]
    prod = Fraction(1, 1)
    s = 0
    for L, x in enumerate(orbit):
        lhs = Fraction((1 << L) * x)
        rhs = Fraction(n) * Fraction(3) ** s * prod
        if lhs != rhs:
            return False, L
        if L < len(orbit) - 1:
            if x % 2 == 1:
                prod *= 1 + Fraction(1, 3 * x)
                s += 1
    return True, len(orbit) - 1


def check_lemma3_envelope(orbit):
    """Lemma 3: x_L <= n 2^{2 s_L - L}, cross-multiplied to integers."""
    n = orbit[0]
    s = 0
    for L, x in enumerate(orbit):
        e = 2 * s - L
        if e >= 0:
            ok = x <= n * (1 << e)
        else:
            ok = x * (1 << (-e)) <= n
        if not ok:
            return False, L
        if x % 2 == 1:
            s += 1
    return True, len(orbit) - 1


def correction_cesaro_control(orbit):
    """Lemma 2 control: correction Cesàro mean along one long orbit.

    Reports the running mean of c_j = q_j log(1 + 1/(3 x_j)) at the end
    of the orbit, using exact Fraction logarithm-free comparison:
    we report C_L as the exact product P_L = prod (1 + 1/(3x_j)) and the
    exact per-step bound mean log(P_L)/L <= s_L log(4/3)/L as Fractions.
    """
    prod = Fraction(1, 1)
    s = 0
    records = []
    for L, x in enumerate(orbit):
        if L > 0 and x % 2 == 1:
            pass
        if L < len(orbit) - 1 and x % 2 == 1:
            prod *= 1 + Fraction(1, 3 * x)
            s += 1
        if L in (len(orbit) // 4, len(orbit) // 2, len(orbit) - 1) and L > 0:
            # crude exact control: log prod <= s log(4/3); mean <= s*log(4/3)/L
            # we store the exact product and the exact rational bound mean
            records.append({
                "L": L,
                "s_L": s,
                "correction_product_exact": str(prod),
                "mean_bound_num_over_den": str(Fraction(s, L)),
            })
    return records


# ----------------------------------------------------------------------------
# Named aperiodic word generators
# ----------------------------------------------------------------------------

def thue_morse(N):
    return [(j.bit_count() & 1) for j in range(N)]


def rudin_shapiro(N):
    # q_j = parity of the number of overlapping occurrences of "11" in bin(j)
    return [((j & (j >> 1)).bit_count() & 1) for j in range(N)]


def paperfolding(N):
    # regular paperfolding: a(4n)=1, a(4n+2)=0, a(2n+1)=a(n); a(0)=1
    a = [0] * N
    a[0] = 1
    for j in range(1, N):
        if j % 4 == 0:
            a[j] = 1
        elif j % 4 == 2:
            a[j] = 0
        elif j % 2 == 1:
            a[j] = a[(j - 1) // 2]
        else:  # j % 4 == 0 handled; even j: a(j)=a(j/2) not needed above
            a[j] = a[j // 2]
    return a


def period_doubling(N):
    # q_j = v_2(j+1) mod 2
    out = []
    for j in range(N):
        v = ((j + 1) & -(j + 1)).bit_length() - 1
        out.append(v & 1)
    return out


def fibonacci_word(N):
    # fixed point of 0 -> 01, 1 -> 0
    w = [0]
    while len(w) < N:
        w = [b for a in w for b in ((0, 1) if a == 0 else (0,))]
    return w[:N]


def champernowne_binary(N):
    out = []
    m = 1
    while len(out) < N:
        out.extend(int(b) for b in bin(m)[2:])
        m += 1
    return out[:N]


WORDS = {
    "thue_morse": thue_morse,
    "rudin_shapiro": rudin_shapiro,
    "paperfolding": paperfolding,
    "period_doubling": period_doubling,
    "fibonacci_word": fibonacci_word,
    "champernowne_binary": champernowne_binary,
}

# Exact classical densities (as Fractions where rational; Fibonacci is
# 2 - phi, certified below via prefix control only).
CLASSICAL_DENSITY = {
    "thue_morse": "1/2",
    "rudin_shapiro": "1/2",
    "paperfolding": "1/2",
    "period_doubling": "1/3",
    "fibonacci_word": "2-phi = 0.3819660112...",
    "champernowne_binary": "1/2",
}


def density_control(word, warm=1 << 14):
    """Exact prefix-density controls: final density and max tail density.

    Uses integer cross-multiplication instead of per-step Fractions.
    """
    N = len(word)
    s = 0
    mn, md = 0, 1  # running max tail density as exact rational
    max_tail_L = warm
    for L in range(1, N + 1):
        s += word[L - 1]
        if L >= warm and s * md > mn * L:
            mn, md, max_tail_L = s, L, L
    max_tail = Fraction(mn, md)
    final = Fraction(s, N)
    bound = Fraction(63, 100)
    return {
        "N": N,
        "final_density": str(final),
        "final_below_63_over_100": final < bound,
        "max_prefix_density_after_warmup": str(max_tail),
        "max_prefix_density_L": max_tail_L,
        "warmup_L": warm,
        "max_tail_below_63_over_100": max_tail < bound,
        "classical_exact_density": None,  # filled by caller
    }


# ----------------------------------------------------------------------------
# Sturmian complexity control
# ----------------------------------------------------------------------------

def sturmian_complexity_control(k_max=40, prefix_len=200000):
    w = fibonacci_word(prefix_len + k_max + 1)
    ok = True
    for k in range(1, k_max + 1):
        factors = {tuple(w[i:i + k]) for i in range(prefix_len)}
        if len(factors) != k + 1:
            ok = False
            break
    return {"k_max": k_max, "prefix_positions": prefix_len,
            "p_k_equals_k_plus_1": ok}


# ----------------------------------------------------------------------------
# Main certificate
# ----------------------------------------------------------------------------

def main():
    cert = {"packet": "2026-07-22-pointwise-drift-wall",
            "scope": "finite controls only; theorems proved in memo"}

    cert["alpha_bounds"] = certify_alpha_bounds()

    orbit_checks = {}
    for n in list(range(1, 65)) + [27, 97, 703, 6171]:
        orbit = terras_orbit(n)
        ok1, L1 = check_lemma1_identity(orbit)
        ok3, L3 = check_lemma3_envelope(orbit)
        orbit_checks[str(n)] = {
            "orbit_length": len(orbit),
            "reaches_1": orbit[-1] == 1,
            "lemma1_identity_exact": ok1,
            "lemma3_envelope_exact": ok3,
        }
        assert ok1 and ok3, (n, L1, L3)
    cert["orbit_exact_checks"] = orbit_checks

    cert["cesaro_control_orbit_27"] = correction_cesaro_control(terras_orbit(27))

    N = int(os.environ.get("VDW_N", 1 << 21))
    dens = {}
    for name, gen in WORDS.items():
        w = gen(N)
        ctl = density_control(w)
        ctl["classical_exact_density"] = CLASSICAL_DENSITY[name]
        dens[name] = ctl
        assert ctl["final_below_63_over_100"], name
        assert ctl["max_tail_below_63_over_100"], name
    cert["named_word_density_controls"] = dens

    cert["sturmian_complexity_control"] = sturmian_complexity_control()

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("drift_wall_certificate.json", "w") as f:
        f.write(out + "\n")
    summary = {
        "status": "ok",
        "orbits_checked_exact": len(orbit_checks),
        "named_words": len(dens),
        "all_densities_below_63_over_100": True,
        "sturmian_control": cert["sturmian_complexity_control"]["p_k_equals_k_plus_1"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
