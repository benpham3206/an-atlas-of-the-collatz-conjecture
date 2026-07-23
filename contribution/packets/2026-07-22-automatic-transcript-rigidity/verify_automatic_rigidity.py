#!/usr/bin/env python3
"""Executable controls for COLLATZ_AUTOMATIC_TRANSCRIPT_RIGIDITY.md.

Track A of the atlas program: 2-automatic parity transcripts q and the
realizability map Phi(q) = -sum_{j>=0} 2^{d_j}/3^{j+1} in Z_2, where
d_0 < d_1 < ... are the positions of the ones of q (PARTIAL_THEOREMS.md,
Theorem 2). q is realized by a positive integer orbit iff Phi(q) in Z_{>0}.

Everything on the certificate path is exact integer/Fraction arithmetic:

  * Phi(q) mod 2^L = -sum_{j: d_j < L} 2^{d_j} * 3^{-(j+1)}  (mod 2^L),
    computed with pow(3, -(j+1), 2^L); only the first L symbols of q enter.
  * Density comparisons with alpha = log_3 2 use rho = a/b < alpha iff
    3^a < 2^b  (rho < alpha  <=>  rho*ln3 < ln2  <=>  3^rho < 2). No floats.
  * Primitive uniform morphism letter frequencies are exact Fractions:
    the Perron eigenvalue of a length-ell uniform incidence matrix is ell
    (integer), so the frequency vector lies in the rational null space of
    M - ell*I.

Float64 appears only in explicitly-labeled numeric controls (prefix
densities, numeric periodicity detection).

Environment knobs (reduced test mode):
  VATR_REDUCED=1  ->  L_MAX=96, binary morphism length <= 3, no ternary
                      sweep, 150 orbit cross-checks, shorter prefixes.
  Individual overrides: VATR_L_MAX, VATR_MAXLEN, VATR_TERNARY,
  VATR_NCHECK, VATR_DENSITY_PREFIX.
"""

import json
import math
import os
import sys
from fractions import Fraction
from itertools import product as iterproduct

# ---------------------------------------------------------------------------
# configuration
# ---------------------------------------------------------------------------

REDUCED = os.environ.get("VATR_REDUCED", "0") == "1"

L_MAX = int(os.environ.get("VATR_L_MAX", "96" if REDUCED else "512"))
MAXLEN = int(os.environ.get("VATR_MAXLEN", "3" if REDUCED else "4"))
TERNARY = os.environ.get("VATR_TERNARY", "0" if REDUCED else "1") == "1"
NCHECK = int(os.environ.get("VATR_NCHECK", "150" if REDUCED else "2000"))
DENSITY_PREFIX = int(os.environ.get("VATR_DENSITY_PREFIX",
                                    "2048" if REDUCED else "8192"))
PERIOD_PREFIX = DENSITY_PREFIX          # prefix used for periodicity controls

# ---------------------------------------------------------------------------
# exact Phi engine (Theorem 4 of the memo)
# ---------------------------------------------------------------------------

def phi_mod(word, L):
    """Exact Phi(q) mod 2^L from the first L symbols of q.

    word: iterable of 0/1 (at least L symbols). Returns an integer in
    [0, 2^L). Terms with one-position d_j >= L vanish mod 2^L.
    """
    mod = 1 << L
    acc = 0
    j = 0
    for d in range(min(L, len(word))):
        if word[d]:
            acc = (acc + pow(2, d, mod) * pow(3, -(j + 1), mod)) % mod
            j += 1
    return (-acc) % mod


def phi_periodic_fraction(period_word, preperiod_word=()):
    """Exact Phi(q) as a Fraction for an eventually periodic word
    q = preperiod_word ++ period_word**omega (purely periodic if the
    preperiod is empty)."""
    h = len(preperiod_word)
    m0 = sum(preperiod_word)
    # prefix contribution
    val = Fraction(0)
    j = 0
    for d, b in enumerate(preperiod_word):
        if b:
            val -= Fraction(2 ** d, 3 ** (j + 1))
            j += 1
    # periodic tail
    p = len(period_word)
    ones = [i for i, b in enumerate(period_word) if b]
    m = len(ones)
    if m > 0:
        base = Fraction(0)
        for i, r in enumerate(ones):
            # the one at position r + k*p has one-index k*m + i
            base += Fraction(2 ** r, 3 ** (i + 1))
        tail = -Fraction(3 ** m, 3 ** m - 2 ** p) * base
        val += Fraction(2 ** h, 3 ** m0) * tail
    return val


def fraction_to_mod(frac, L):
    """Exact image of a Fraction with odd denominator in Z/2^L."""
    mod = 1 << L
    assert frac.denominator % 2 == 1
    return (frac.numerator % mod) * pow(frac.denominator % mod, -1, mod) % mod


# ---------------------------------------------------------------------------
# exact comparator with alpha = log_3 2 (Lemma A support)
# ---------------------------------------------------------------------------

def cmp_fraction_vs_alpha(rho):
    """Compare a nonnegative Fraction rho with alpha = log_3 2.

    rho < alpha  <=>  3^a < 2^b  for rho = a/b in lowest terms.
    Returns -1, 0, +1. Equality is impossible (alpha is transcendental,
    Lemma A); a 0 would be a Gelfond--Schneider-violating sensation.
    """
    a, b = rho.numerator, rho.denominator
    lhs, rhs = 3 ** a, 2 ** b
    return -1 if lhs < rhs else (1 if lhs > rhs else 0)


# ---------------------------------------------------------------------------
# uniform morphisms: incidence matrices, exact frequencies, fixed points
# ---------------------------------------------------------------------------

def incidence(sigma, r):
    M = [[0] * r for _ in range(r)]
    for j, w in enumerate(sigma):
        for letter in w:
            M[letter][j] += 1
    return M


def mat_mul(A, B, r):
    return [[sum(A[i][k] * B[k][j] for k in range(r)) for j in range(r)]
            for i in range(r)]


def is_primitive(M, r, max_pow=8):
    P = [row[:] for row in M]
    for _ in range(max_pow):
        if all(P[i][j] > 0 for i in range(r) for j in range(r)):
            return True
        P = mat_mul(P, M, r)
    return False


def freq_vector_exact(M, r, ell):
    """Normalized right eigenvector of M at the Perron eigenvalue ell
    (uniform morphism), as Fractions, or None if the rational null space
    of M - ell*I is not a positive line. Verifies (M - ell I) v == 0."""
    A = [[Fraction(M[i][j]) - (ell if i == j else 0) for j in range(r)]
         for i in range(r)]
    if r == 2:
        v = [A[0][1], -A[0][0]]   # null vector of the first row
        if v[0] == 0 and v[1] == 0:
            return None
    else:
        def cross(u, w):
            return [u[1] * w[2] - u[2] * w[1],
                    u[2] * w[0] - u[0] * w[2],
                    u[0] * w[1] - u[1] * w[0]]
        v = None
        for (i, j) in ((0, 1), (0, 2), (1, 2)):
            cand = cross(A[i], A[j])
            if any(x != 0 for x in cand):
                v = cand
                break
        if v is None:
            return None
    # exact eigenvector check
    for i in range(r):
        if sum(A[i][j] * v[j] for j in range(r)) != 0:
            return None
    s = sum(v)
    if s == 0:
        return None
    v = [x / s for x in v]
    if any(x < 0 for x in v):
        v = [-x for x in v]
    if any(x <= 0 for x in v):
        return None  # primitive Perron vector is strictly positive
    return v


def fixed_point_prefix(sigma, seed, n):
    """Iterate a uniform morphism; requires sigma[seed][0] == seed so the
    iterates form a prefix chain."""
    word = [seed]
    while len(word) < n:
        word = [x for a in word for x in sigma[a]]
    return word[:n]


# ---------------------------------------------------------------------------
# periodicity: numeric detection (KMP, control) + exact morphism witness
# ---------------------------------------------------------------------------

def minimal_period_of_suffix(word, start):
    """Minimal period p of word[start:] via the KMP failure function,
    or None if the suffix is not p-periodic with at least 3 repetitions."""
    s = word[start:]
    n = len(s)
    if n < 6:
        return None
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    p = n - pi[-1]
    if p <= n // 3 and all(s[i] == s[i + p] for i in range(n - p)):
        return p
    return None


def period_witness_check(sigma, seed, p, word):
    """EXACT periodicity certificate for a uniform-morphism fixed point.

    Let v = w**omega with w = u[:p], ell the morphism length. If for every
    residue j mod p the block sigma(w[j]) equals the length-ell window of v
    starting at position (j*ell) mod p, then sigma(v) = v (each block of
    sigma(v) coincides with v's window at the same position). Since
    v[0] = seed and u = lim sigma^t(seed) is the unique fixed point from the
    seed, u = v. Proved in the memo (Lemma C)."""
    ell = len(sigma[seed])
    if len(word) < p:
        return False
    w = word[:p]
    rep = (w * (ell // p + 3))
    for j in range(p):
        start = (j * ell) % p
        if list(sigma[w[j]]) != rep[start:start + ell]:
            return False
    return True


# ---------------------------------------------------------------------------
# named families (generators over one indexed block [0, N) )
# ---------------------------------------------------------------------------

def thue_morse(N):
    return [bin(n).count("1") & 1 for n in range(N)]


def period_doubling(N):
    out = []
    for n in range(N):
        v = 0
        m = n + 1
        while m % 2 == 0:
            v += 1
            m //= 2
        out.append(v & 1)
    return out


def rudin_shapiro(N):
    out = []
    for n in range(N):
        b = bin(n)[2:]
        out.append(sum(1 for i in range(len(b) - 1)
                       if b[i] == "1" and b[i + 1] == "1") & 1)
    return out


def paperfolding(N):
    out = [1]  # conventional value at 0
    for n in range(1, N):
        m = n
        while m % 2 == 0:
            m //= 2
        out.append(1 if m % 4 == 1 else 0)
    return out


def fibonacci_word(N):
    word = [0]
    while len(word) < N:
        word = [x for a in word for x in ((0, 1) if a == 0 else (0,))]
    return word[:N]


def block_oscillator(N):
    """a(n) = 1 iff bitlength(n) is odd (n >= 1), a(0) = 0.

    2-automatic (two-state DFAO on the MSB-first expansion). Natural
    density does not exist; it oscillates between 1/3 and 2/3."""
    return [0] + [n.bit_length() & 1 for n in range(1, N)]


def supercritical_oscillator(N):
    """q(n) = 1 iff n is even or bitlength(n) is odd.

    2-automatic (four-state DFAO: bitlength parity x last bit).
    s_L/L >= 2/3 - o(1) for ALL L (memo, Theorem 3); liminf = 2/3 > alpha,
    natural density does not exist (oscillates 2/3 .. 5/6)."""
    out = []
    for n in range(N):
        out.append(1 if (n % 2 == 0 or (n > 0 and n.bit_length() & 1)) else 0)
    return out


def gap_example_word(N):
    """Fixed point of sigma(0)=11, sigma(1)=10 from seed 1: the proved
    supercritical aperiodic primitive-uniform example of the memo."""
    sigma = ((1, 1), (1, 0))
    return fixed_point_prefix(sigma, 1, N)


# ---------------------------------------------------------------------------
# lift-bit analysis
# ---------------------------------------------------------------------------

def lift_stats(word, L_max):
    """Compute A = Phi(q) mod 2^L_max once, then read off:
      bits[L]         = bit L of A (= change indicator N_{L+1} != N_L),
      last_change     = max L with bit L = 1 (-1 if A == 0),
      zero_run_max    = longest run of zero bits in [0, L_max),
      phi_mod_value   = A.
    A change at level L certifies Phi(q) not in {1, ..., 2^L - 1}
    (memo, Theorem 4)."""
    A = phi_mod(word, L_max)
    last_change = -1
    zero_run = 0
    zero_run_max = 0
    for L in range(L_max):
        bit = (A >> L) & 1
        if bit:
            last_change = L
            zero_run = 0
        else:
            zero_run += 1
            zero_run_max = max(zero_run_max, zero_run)
    return {"last_change": last_change, "zero_run_max": zero_run_max,
            "phi_mod_value": str(A)}


# ---------------------------------------------------------------------------
# Terras orbit cross-check of the Phi engine
# ---------------------------------------------------------------------------

def terras_transcript(n, steps):
    q = []
    x = n
    for _ in range(steps):
        q.append(x & 1)
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
    return q


# ---------------------------------------------------------------------------
# enumeration drivers
# ---------------------------------------------------------------------------

def all_words(ell, r):
    return iterproduct(range(r), repeat=ell)


def all_sigmas(ell, r):
    return iterproduct(all_words(ell, r), repeat=r)


def classify_word(word, rho_exact, kind_label):
    """Common per-word analysis. Returns a compact record."""
    rec = {"kind": kind_label}
    if rho_exact is not None:
        rec["rho"] = str(rho_exact)
        c = cmp_fraction_vs_alpha(rho_exact)
        rec["cmp_alpha"] = {(-1): "below", 0: "EQUAL", 1: "above"}[c]
    dens = sum(word) / len(word)
    rec["density_numeric_prefix"] = round(dens, 6)
    stats = lift_stats(word, L_MAX)
    rec["last_change_level"] = stats["last_change"]
    rec["zero_run_max"] = stats["zero_run_max"]
    return rec, stats


def enumerate_uniform(r, ell, use_codings):
    """Enumerate uniform length-ell morphisms on r letters, all valid
    seeds, optionally all nonconstant binary codings. Returns
    (distinct_records, survivor_records, periodic_records, anomalies)."""
    records = []
    survivors = []
    periodics = []
    anomalies = []
    seen = {}
    codings = [None]
    if use_codings:
        codings = [tuple((mask >> a) & 1 for a in range(r))
                   for mask in range(1, 2 ** r - 1)]
    for sigma in all_sigmas(ell, r):
        M = incidence(sigma, r)
        prim = is_primitive(M, r)
        freq = freq_vector_exact(M, r, ell) if prim else None
        for seed in range(r):
            if sigma[seed][0] != seed:
                continue
            base = None  # generated lazily
            for coding in codings:
                if base is None:
                    base = fixed_point_prefix(
                        sigma, seed, max(DENSITY_PREFIX, L_MAX))
                if coding is None:
                    word = base
                    cid = None
                else:
                    word = [coding[a] for a in base]
                    cid = "".join(map(str, coding))
                key = tuple(word[:min(L_MAX, 256)])
                if key in seen:
                    continue
                seen[key] = True
                rho = None
                if freq is not None:
                    if coding is None:
                        rho = freq[1] if r >= 2 else None
                    else:
                        rho = sum((freq[a] for a in range(r)
                                   if coding[a] == 1), Fraction(0))
                rec, stats = classify_word(word, rho,
                                           "binary" if r == 2 else "ternary")
                rec["sigma"] = ",".join("".join(map(str, w)) for w in sigma)
                rec["seed"] = seed
                if cid is not None:
                    rec["coding"] = cid
                rec["primitive"] = prim
                # periodicity: numeric detection + exact witness when possible
                p = minimal_period_of_suffix(word, len(word) // 4)
                if p is None:
                    p = minimal_period_of_suffix(word, 0)
                rec["period_numeric"] = p
                exact_period = False
                if p is not None and coding is None:
                    exact_period = period_witness_check(sigma, seed, p, word)
                rec["period_exact_witness"] = exact_period
                if exact_period:
                    # purely periodic by Lemma C: exact Fraction Phi
                    frac = phi_periodic_fraction(word[:p])
                    chk = fraction_to_mod(frac, min(64, L_MAX))
                    if chk != phi_mod(word, min(64, L_MAX)):
                        anomalies.append({"reason": "fraction_mod_mismatch",
                                          "rec_sigma": rec["sigma"]})
                    rec["phi_fraction"] = str(frac)
                    rec["phi_fraction_integral_positive"] = (
                        frac.denominator == 1 and frac.numerator > 0)
                    rec["phi"] = str(frac)
                    periodics.append(rec)
                    rec["class"] = "periodic_exact"
                elif p is not None:
                    # eventually periodic by numeric control only; Phi is
                    # rational (PARTIAL_THEOREMS Thm 3) but not computed here
                    rec["class"] = "periodic_numeric"
                    periodics.append(rec)
                elif prim and rho is not None:
                    if rec["cmp_alpha"] == "below":
                        rec["class"] = "killed_subcritical_primitive"
                    elif rec["cmp_alpha"] == "above":
                        rec["class"] = "survivor_supercritical_primitive"
                        rec["phi_mod_2^Lmax"] = stats["phi_mod_value"]
                        survivors.append(rec)
                    else:
                        anomalies.append({"reason": "EQUAL_alpha",
                                          "rec_sigma": rec["sigma"]})
                        rec["class"] = "CRITICAL_IMPOSSIBLE"
                else:
                    rec["class"] = "nonprimitive_numeric"
                records.append(rec)
    records.sort(key=lambda x: (x["kind"], x["sigma"],
                                x.get("coding", ""), x["seed"]))
    return records, survivors, periodics, anomalies


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    cert = {
        "packet": "2026-07-22-automatic-transcript-rigidity",
        "scope": ("exact integer/Fraction arithmetic in all certificate "
                  "paths; float64 entries are numeric controls only"),
        "env": {"VATR_L_MAX": L_MAX, "VATR_MAXLEN": MAXLEN,
                "VATR_TERNARY": TERNARY, "VATR_NCHECK": NCHECK,
                "VATR_DENSITY_PREFIX": DENSITY_PREFIX},
    }

    # --- Lemma A support -------------------------------------------------
    bound = 500
    for a in range(1, bound + 1):
        pa = 3 ** a
        for b in range(1, bound + 1):
            assert pa != 2 ** b
    cert["lemma_A_support"] = {
        "checked_2^b_neq_3^a_for_1<=a,b<=": bound,
        "comparator": "rho=a/b < log_3 2  iff  3^a < 2^b (exact integers)",
    }

    # --- Phi engine validation: trivial cycles ---------------------------
    w10 = ([1, 0] * 64)
    w01 = ([0, 1] * 64)
    w110 = ([1, 1, 0] * 64)
    f10 = phi_periodic_fraction([1, 0])
    f01 = phi_periodic_fraction([0, 1])
    f110 = phi_periodic_fraction([1, 1, 0])
    assert f10 == 1 and f01 == 2 and f110 == -5
    for word, frac in ((w10, f10), (w01, f01), (w110, f110)):
        assert phi_mod(word, 64) == fraction_to_mod(frac, 64)
    assert phi_mod(w10, 64) == 1 and phi_mod(w01, 64) == 2
    cert["engine_validation_trivial_cycles"] = {
        "(10)^omega": str(f10), "(01)^omega": str(f01),
        "(110)^omega": str(f110),
        "note": "(110)^omega is supercritical periodic: Phi = -5, "
                "correctly outside Z_{>0} (cycle equation 2^3 < 3^2)"}

    # --- Phi engine validation: true orbits ------------------------------
    for n in range(1, NCHECK + 1):
        q = terras_transcript(n, 64)
        assert phi_mod(q, 64) == n % (1 << 64), n
    cert["engine_validation_orbits"] = {
        "count": NCHECK, "modulus": "2^64",
        "statement": "Phi(transcript of n) mod 2^64 == n mod 2^64",
        "all_passed": True}

    # --- named families ----------------------------------------------------
    assert 3 ** 63 < 2 ** 100            # 63/100 < log_3 2
    assert 12500 > 7569                  # sqrt5 > 87/50  =>  2-phi < 63/100
    alpha_cmp = lambda a, b: cmp_fraction_vs_alpha(Fraction(a, b))
    named = []
    named_specs = [
        ("thue_morse", thue_morse, True, Fraction(1, 2), "3^1 < 2^2"),
        ("period_doubling", period_doubling, True, Fraction(1, 3), "3^1 < 2^3"),
        ("rudin_shapiro", rudin_shapiro, True, Fraction(1, 2), "3^1 < 2^2"),
        ("paperfolding", paperfolding, True, Fraction(1, 2), "3^1 < 2^2"),
        ("fibonacci_word", fibonacci_word, False, None,
         "2-phi < 63/100 (sqrt5 > 87/50) and 3^63 < 2^100"),
    ]
    for name, gen, is_auto, rho, witness in named_specs:
        word = gen(max(DENSITY_PREFIX, L_MAX))
        rec = {"name": name, "two_automatic": is_auto,
               "rho_exact": str(rho) if rho else "2-golden_ratio",
               "kill": "drift wall (packet 1 Thm 2): aperiodic, "
                       "subcritical => Phi not in Z_{>0}",
               "witness": witness,
               "density_numeric_prefix": round(sum(word) / len(word), 6)}
        if rho is not None:
            assert alpha_cmp(rho.numerator, rho.denominator) == -1
        stats = lift_stats(word, L_MAX)
        rec["last_change_level"] = stats["last_change"]
        rec["zero_run_max"] = stats["zero_run_max"]
        named.append(rec)
    cert["named_families"] = named

    # --- the two oscillator witnesses (Theorem 3 controls) ---------------
    osc = block_oscillator(1 << 15)
    d_lo = sum(osc[:4 ** 7]) / 4 ** 7
    d_hi = sum(osc[:2 * 4 ** 7]) / (2 * 4 ** 7)
    sup = supercritical_oscillator(1 << 14)
    running = 0
    min_ratio = 1.0
    for L in range(64, len(sup)):
        running += sup[L - 1]
        # s_L/L with s_L = sum of first L symbols
        pass
    s = 0
    ratios = []
    for L in range(1, len(sup) + 1):
        s += sup[L - 1]
        if L >= 64:
            ratios.append(s / L)
    min_ratio = min(ratios)
    max_ratio = max(ratios)
    sup_stats = lift_stats(sup, L_MAX)
    osc_stats = lift_stats(osc, L_MAX)
    cert["oscillators"] = {
        "block_oscillator": {
            "definition": "a(n)=1 iff bitlength(n) odd; 2-automatic, "
                          "natural density does not exist",
            "density_at_2^14_numeric": d_lo,
            "density_at_2^15_numeric": d_hi,
            "liminf_exact": "1/3", "limsup_exact": "2/3",
            "kill": "drift wall: liminf 1/3 < alpha, aperiodic "
                    "(density DNE) => Phi not in Z_{>0}  [PROVED]",
            "witness": "3^1 < 2^3",
            "last_change_level": osc_stats["last_change"],
        },
        "supercritical_oscillator": {
            "definition": "q(n)=1 iff n even or bitlength(n) odd; "
                          "2-automatic, natural density does not exist",
            "s_L_over_L_min_numeric_L>=64": min_ratio,
            "s_L_over_L_max_numeric": max_ratio,
            "liminf_exact": "2/3", "limsup_exact": "5/6",
            "status": "SURVIVES every density wall: s_L/L >= 2/3 - o(1) "
                      "uniformly, 2/3 > alpha (witness 3^2 > 2^3)",
            "last_change_level": sup_stats["last_change"],
            "zero_run_max": sup_stats["zero_run_max"],
            "phi_mod_2^Lmax": sup_stats["phi_mod_value"],
        },
    }
    assert d_lo < 0.34 < d_hi           # numeric control of the oscillation
    assert min_ratio > 0.66             # numeric control of liminf = 2/3

    # --- the proved gap example u: sigma(0)=11, sigma(1)=10, seed 1 ------
    u = gap_example_word(1 << 12)
    # self-similarity controls used by the aperiodicity proof:
    for i in range(len(u) // 4 - 1):
        assert u[2 * i] == 1
        assert u[4 * i + 1] == 0
        assert u[4 * i + 3] == u[i]
    freq_u = freq_vector_exact(incidence(((1, 1), (1, 0)), 2), 2, 2)
    assert freq_u == [Fraction(1, 3), Fraction(2, 3)]
    assert cmp_fraction_vs_alpha(freq_u[1]) == 1     # 2/3 > alpha
    u_stats = lift_stats(u, L_MAX)
    cert["gap_example_sigma_11_10"] = {
        "rho_exact": "2/3", "witness": "3^2 > 2^3",
        "self_similarity_controls_on_prefix": "u_{2i}=1, u_{4i+1}=0, "
                                              "u_{4i+3}=u_i  (checked)",
        "aperiodicity": "PROVED in memo by period divisibility descent",
        "density_numeric_prefix": round(sum(u) / len(u), 6),
        "last_change_level": u_stats["last_change"],
        "zero_run_max": u_stats["zero_run_max"],
        "phi_mod_2^Lmax": u_stats["phi_mod_value"],
        "certified": "if Phi(u) in Z_{>0} then Phi(u) >= 2^%d"
                     % u_stats["last_change"],
    }

    # --- enumeration -------------------------------------------------------
    enumeration = {}
    all_survivors = []
    all_anomalies = []
    all_records = []
    for (label, r, ell, codings) in (
            [("binary_ell<=MAXLEN", 2, None, False)] +
            ([("ternary_ell2_coded", 3, 2, True)] if TERNARY else [])):
        if r == 2:
            recs, survs, pers, anoms = [], [], [], []
            for ell_i in range(2, MAXLEN + 1):
                out = enumerate_uniform(2, ell_i, False)
                recs += out[0]
                survs += out[1]
                pers += out[2]
                anoms += out[3]
        else:
            recs, survs, pers, anoms = enumerate_uniform(r, ell, codings)
        counts = {}
        for rec in recs:
            counts[rec["class"]] = counts.get(rec["class"], 0) + 1
        enumeration[label] = {
            "distinct_words": len(recs),
            "counts_by_class": counts,
            "anomalies": anoms,
            "records": recs,
        }
        all_survivors += survs
        all_anomalies += anoms
        all_records += recs
    cert["enumeration"] = enumeration
    assert not all_anomalies, all_anomalies[:3]
    assert not any(r["class"] == "CRITICAL_IMPOSSIBLE" for r in all_records)

    # --- candidate scan: window-stabilized aperiodic words ---------------
    # A genuine integrality candidate has Phi(q) mod 2^L_MAX = n0 with all
    # bits from some level L0 to L_MAX equal to zero, i.e. a long TOP zero
    # run. Under the heuristic that lift bits are fair bits, a top run of
    # length >= 32 over ~10^4 words has probability ~10^4 * 2^-32 of
    # occurring by chance; none is expected. Short top runs are noise.
    STAB = 32
    for rec in all_records:
        rec["top_zero_run"] = L_MAX - 1 - rec["last_change_level"]
    candidates = [rec for rec in all_records
                  if not rec["class"].startswith("periodic")
                  and rec["top_zero_run"] >= STAB]
    max_top_run_aperiodic = max(
        (rec["top_zero_run"] for rec in all_records
         if not rec["class"].startswith("periodic")), default=0)
    # periodic words with positive integral Phi: only the trivial cycle
    trivial_hits = [r for r in all_records
                    if r["class"] == "periodic_exact"
                    and r.get("phi_fraction_integral_positive")]
    trivial_values = sorted({r["phi_fraction"] for r in trivial_hits})
    assert trivial_values == ["1", "2"], trivial_values
    cert["candidate_scan"] = {
        "stabilization_threshold_bits": STAB,
        "aperiodic_window_stabilized_candidates": len(candidates),
        "candidates": candidates,
        "max_top_zero_run_aperiodic_words": max_top_run_aperiodic,
        "periodic_words_with_positive_integral_Phi": trivial_values,
        "conclusion": ("no aperiodic automatic candidate; the only "
                       "positive-integral periodic Phi values in the sweep "
                       "are the trivial cycle transcripts 1 and 2"),
    }
    assert not candidates

    cert["survivors_supercritical_primitive"] = [
        {"sigma": r["sigma"], "seed": r["seed"],
         "coding": r.get("coding"), "rho": r["rho"],
         "witness_3^a_vs_2^b": "3^%s > 2^%s" % (
             Fraction(r["rho"]).numerator, Fraction(r["rho"]).denominator),
         "last_change_level": r["last_change_level"],
         "zero_run_max": r["zero_run_max"],
         "certified": "if Phi in Z_{>0} then Phi >= 2^%d"
                      % r["last_change_level"],
         "aperiodic_label": "numeric control (no period <= prefix/4 found "
                            "on %d symbols)" % DENSITY_PREFIX}
        for r in all_survivors]
    cert["max_zero_run_over_all_words"] = max(
        r["zero_run_max"] for r in all_records)

    out = json.dumps(cert, indent=2, sort_keys=True)
    with open("automatic_rigidity_certificate.json", "w") as f:
        f.write(out + "\n")

    summary = {
        "status": "ok",
        "L_MAX": L_MAX,
        "orbit_cross_checks": NCHECK,
        "named_families_killed": len(cert["named_families"]),
        "enumeration": {k: v["counts_by_class"]
                        for k, v in enumeration.items()},
        "supercritical_primitive_survivors": len(all_survivors),
        "aperiodic_candidates": len(candidates),
        "periodic_integral_phi_values": trivial_values,
        "max_zero_run": cert["max_zero_run_over_all_words"],
        "supercritical_oscillator_last_change":
            sup_stats["last_change"],
        "gap_example_last_change": u_stats["last_change"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
