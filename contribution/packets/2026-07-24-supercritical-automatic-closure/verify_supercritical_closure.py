#!/usr/bin/env python3
"""Executable evidence for COLLATZ_SUPERCRITICAL_AUTOMATIC_CLOSURE.md.

Shrinks the enumerated supercritical stratum of the 2-automatic class:
of the 109 supercritical primitive-uniform survivors of
`2026-07-22-automatic-transcript-rigidity`, 99 are proved to satisfy
Phi(q) not in Z_{>0}.  Ten survive and are named in the certificate.

The missing ingredient supplied here is a PROVED upper bound on the
factor-complexity constant

    C(q) = limsup_k p_q(k)/k,

computed from the EXACT factor language of the fixed point (not from a
prefix sample; Lemma D of the memo).  Feeding that bound into two
inequalities the atlas already proved --

  * Corollary 4 (landmark memo):  C >= kappa = 1/log_2(3/2)
  * Corollary 7 (landmark memo):  C >= alpha/(beta - alpha), for any beta
    such that every length-l factor has at most beta*l + const ones

-- contradicts Phi(q) in Q_odd, hence in Z_{>0}.  An admissible beta is
supplied by one exact computation: beta = f(ell)/ell, where f is the
maximal number of ones in a length-ell factor (subadditive, so Fekete
makes a single ell legitimate).  Neither inequality is new here; the
computable bound on C and the exact beta are.

Every certificate path is exact integer / Fraction arithmetic.  The only
float64 in this file is inside strings printed for human reading; each is
labelled "numeric".  No proved statement depends on a float.

Environment knobs (reduced mode used by the test suite):
  VSAC_REDUCED=1   -> M0=24, ELL_DENS=64, MAXLEN=3, no ternary sweep.
  Individual overrides: VSAC_M0, VSAC_ELL_DENS, VSAC_MAXLEN, VSAC_TERNARY,
  VSAC_NCHECK, VSAC_PREFIX.
"""

import json
import os
import sys
from fractions import Fraction
from itertools import product as iterproduct

# ---------------------------------------------------------------------------
# configuration
# ---------------------------------------------------------------------------

REDUCED = os.environ.get("VSAC_REDUCED", "0") == "1"

# m0: base of the complexity window [m0, k*m0] (Lemma D below).
M0 = int(os.environ.get("VSAC_M0", "24" if REDUCED else "192"))
# ell: length at which the exact maximal factor one-density is evaluated.
ELL_DENS = int(os.environ.get("VSAC_ELL_DENS", "64" if REDUCED else "512"))
MAXLEN = int(os.environ.get("VSAC_MAXLEN", "3" if REDUCED else "4"))
TERNARY = os.environ.get("VSAC_TERNARY", "0" if REDUCED else "1") == "1"
NCHECK = int(os.environ.get("VSAC_NCHECK", "200" if REDUCED else "2000"))
PREFIX = int(os.environ.get("VSAC_PREFIX", "2048" if REDUCED else "8192"))
DEDUP = 256                       # prefix length used to deduplicate words
# depth at which an exact factor count is recorded for words the kill misses
FRONTIER_N = int(os.environ.get("VSAC_FRONTIER_N", "128" if REDUCED
                                else "1537"))

HERE = os.path.dirname(os.path.abspath(__file__))


class Fail(Exception):
    """A kill criterion fired.  Raised, never swallowed."""


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------------------
# 1.  exact comparisons against alpha = log_3 2   (no floats)
# ---------------------------------------------------------------------------

def cmp_frac_alpha(fr):
    """Compare Fraction a/b (a,b > 0) with alpha = log_3 2.

    a/b < alpha  <=>  a*log 3 < b*log 2  <=>  3^a < 2^b.
    Equality never occurs (unique factorization); a 0 return is a kill.
    """
    a, b = fr.numerator, fr.denominator
    lhs, rhs = 3 ** a, 2 ** b
    return -1 if lhs < rhs else (1 if lhs > rhs else 0)


# Continued-fraction convergents of alpha (landmark memo, Part VII.2).  Each
# side of the bracket is certified by one exact integer comparison; keeping
# the denominators small keeps 3^a and 2^b cheap.  Every DECISION in this
# file uses cmp_frac_alpha directly; the bracket is for reporting and for
# the kappa identity check.
ALPHA_CONVERGENTS = [Fraction(306, 485), Fraction(665, 1054),
                     Fraction(15601, 24727)]


def alpha_bracket():
    """Tightest certified (lower, upper) rational bracket for alpha, chosen
    from the convergents by exact 3^a vs 2^b comparisons."""
    lo = hi = None
    for fr in ALPHA_CONVERGENTS:
        c = cmp_frac_alpha(fr)
        need(c != 0, "a convergent equals alpha: unique factorization broken")
        if c < 0:
            lo = fr if lo is None or fr > lo else lo
        else:
            hi = fr if hi is None or fr < hi else hi
    need(lo is not None and hi is not None, "alpha bracket incomplete")
    return lo, hi


def kappa_bounds():
    """kappa = 1/log_2(3/2) = alpha/(1-alpha).  Exact rational bounds
    obtained by pushing the alpha bracket through t -> t/(1-t), which is
    increasing on (0,1)."""
    lo, hi = alpha_bracket()
    return lo / (1 - lo), hi / (1 - hi)


# ---------------------------------------------------------------------------
# 2.  Phi engine -- independent lift-cocycle path (LIFT_COCYCLE.md)
# ---------------------------------------------------------------------------

def phi_mod_lift(word, L):
    """Phi(q) mod 2^L via the exact lift/quotient recurrence.

    r_0 = 0, z_0 = 0, a_0 = 0; for each transcript bit b = q_j:
        eps = (z + b) mod 2,   r <- r + eps*2^j,
        z  <- (z + eps*3^a)/2                 if b = 0
        z  <- (3z + 1 + eps*3^(a+1))/2        if b = 1
        a  <- a + b
    Returns r_L in [0, 2^L).  This path shares no code with the modular
    series below; agreement of the two is an independent check.
    """
    r = 0
    z = 0
    a = 0
    p3 = 1                                     # 3^a
    for j in range(L):
        b = word[j]
        eps = (z + b) & 1
        if eps:
            r += 1 << j
        if b:
            num = 3 * z + 1 + (eps * p3 * 3)
            p3 *= 3
            a += 1
        else:
            num = z + eps * p3
        need(num % 2 == 0, "lift recurrence produced an odd numerator")
        z = num // 2
    return r


def phi_mod_series(word, L):
    """Phi(q) mod 2^L = -sum_{j: d_j < L} 2^{d_j} 3^{-(j+1)} (mod 2^L)."""
    mod = 1 << L
    acc = 0
    j = 0
    for d in range(min(L, len(word))):
        if word[d]:
            acc = (acc + pow(2, d, mod) * pow(3, -(j + 1), mod)) % mod
            j += 1
    return (-acc) % mod


def terras_orbit(n, steps):
    """Exact Terras orbit and its parity transcript."""
    xs = []
    q = []
    x = n
    for _ in range(steps):
        xs.append(x)
        q.append(x & 1)
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
    return xs, q


# ---------------------------------------------------------------------------
# 3.  exact language of a uniform-morphism fixed point
# ---------------------------------------------------------------------------

def reachable_letters(sigma, seed):
    A = {seed}
    while True:
        new = set(A)
        for a in A:
            new |= set(sigma[a])
        if new == A:
            return A
        A = new


def pairs_exact(sigma, seed):
    """Exact set L_2(u) of adjacent letter pairs of u = lim sigma^t(seed).

    L_2(u) is the least fixed point of
        F(P) = {internal pairs of sigma(a) : a reachable}
               u {(last sigma(a), first sigma(b)) : (a,b) in P}.
    Soundness: every pair of u is internal to some block sigma(a) or is a
    block boundary coming from a pair one level up; boundary descent
    strictly decreases the position index, so it terminates at an internal
    pair (morphism length >= 2).
    """
    A = reachable_letters(sigma, seed)
    P = set()
    while True:
        new = set(P)
        for a in A:
            w = sigma[a]
            for i in range(len(w) - 1):
                new.add((w[i], w[i + 1]))
        for (a, b) in P:
            new.add((sigma[a][-1], sigma[b][0]))
        if new == P:
            return P
        P = new


def sigma_pow(sigma, a, r):
    w = [a]
    for _ in range(r):
        w = [x for c in w for x in sigma[c]]
    return w


def window_blocks(sigma, seed, R):
    """Blocks sigma^R(a) ++ sigma^R(b) over every adjacent pair ab of u.

    Every factor of u of length n <= k^R occurs as B[o:o+n] for one of
    these blocks B and some offset o in [0, k^R): a factor starting at
    position t = i*k^R + o spans at most two consecutive sigma^R blocks,
    and the pair of letters carrying them is adjacent in u.
    """
    P = pairs_exact(sigma, seed)
    cache = {}
    out = []
    for (a, b) in sorted(P):
        for c in (a, b):
            if c not in cache:
                cache[c] = bytes(sigma_pow(sigma, c, R))
        out.append(cache[a] + cache[b])
    return out


def factors_exact(blocks, kR, n):
    """Exact set of length-n factors (requires n <= kR)."""
    S = set()
    for B in blocks:
        for o in range(kR):
            S.add(B[o:o + n])
    return S


def fixed_point_prefix(sigma, seed, n):
    w = [seed]
    while len(w) < n:
        w = [x for a in w for x in sigma[a]]
    return w[:n]


# ---------------------------------------------------------------------------
# 4.  proved bounds:  complexity constant C  and  maximal factor density B
# ---------------------------------------------------------------------------

def complexity_nodes(m0, k, ratio_num=201, ratio_den=200):
    """Geometric partition m0 = A_0 < A_1 < ... < A_s = k*m0."""
    nodes = [m0]
    while nodes[-1] < k * m0:
        nxt = -((-nodes[-1] * ratio_num) // ratio_den)     # ceil
        nodes.append(min(nxt if nxt > nodes[-1] else nodes[-1] + 1, k * m0))
    return nodes


def complexity_bound(blocks, kR, k, m0):
    """Proved upper bound for C = limsup_n p_u(n)/n  (Lemma D of the memo).

        C <= max_{m0 <= m <= k*m0} p_u(m+1)/(m-1),

    evaluated on a geometric partition A_0 < ... < A_s of the window: p is
    nondecreasing, so for m in [A_i, A_{i+1}]

        p(m+1)/(m-1) <= p(A_{i+1}+1)/(A_i - 1),

    which needs only s+1 exact factor counts instead of the whole window.
    Returns (bound as Fraction, dict of the p values used).
    """
    need(k * m0 + 1 <= kR, "complexity window exceeds the exact-factor range")
    nodes = complexity_nodes(m0, k)
    pv = {}
    for a in nodes:
        pv[a] = len(factors_exact(blocks, kR, a + 1))
    best = Fraction(0)
    for i in range(len(nodes) - 1):
        cand = Fraction(pv[nodes[i + 1]], nodes[i] - 1)
        if cand > best:
            best = cand
    if len(nodes) == 1:                       # degenerate window (k = 1)
        best = Fraction(pv[nodes[0]], nodes[0] - 1)
    return best, pv


def max_factor_ones(blocks, kR, coding, ell):
    """f(ell) = max number of coded ones over all length-ell factors."""
    need(ell <= kR, "density length exceeds the exact-factor range")
    best = 0
    for w in factors_exact(blocks, kR, ell):
        c = sum(coding[x] for x in w)
        if c > best:
            best = c
    return best


def round_up_frac(fr, den):
    """Smallest multiple of 1/den that is >= fr (weakening is safe)."""
    return Fraction(-((-fr.numerator * den) // fr.denominator), den)


def kill_kappa(c_bound):
    """Corollary 4 kill: aperiodic + Phi in Q_odd forces C >= kappa.
    Fires when c_bound < kappa, i.e. c_bound*(1 - c_bound_free) ... exactly:
    c < alpha/(1-alpha)  <=>  c/(1+c) < alpha  <=>  3^u < 2^(u+v)
    for c = u/v in lowest terms."""
    u, v = c_bound.numerator, c_bound.denominator
    return 3 ** u < 2 ** (u + v), (u, u + v)


def kill_density(c_bound, beta):
    """Corollary 7' kill.  With an upper bound `beta` (Fraction) for the
    asymptotic maximal factor one-density, C >= alpha/(beta - alpha).
    Fires when c*(beta - alpha) < alpha
        <=>  beta * c/(1+c) < alpha
        <=>  a*u / (b*(u+v)) < alpha
        <=>  3^(a*u) < 2^(b*(u+v))
    for beta = a/b and c = u/v in lowest terms."""
    a, b = beta.numerator, beta.denominator
    u, v = c_bound.numerator, c_bound.denominator
    return 3 ** (a * u) < 2 ** (b * (u + v)), (a * u, b * (u + v))


# ---------------------------------------------------------------------------
# 5.  uniform morphisms: incidence, primitivity, exact Perron frequencies
# ---------------------------------------------------------------------------

def incidence(sigma, r):
    M = [[0] * r for _ in range(r)]
    for j, w in enumerate(sigma):
        for letter in w:
            M[letter][j] += 1
    return M


def mat_mul(A, B, r):
    return [[sum(A[i][t] * B[t][j] for t in range(r)) for j in range(r)]
            for i in range(r)]


def is_primitive(M, r, max_pow=8):
    P = [row[:] for row in M]
    for _ in range(max_pow):
        if all(P[i][j] > 0 for i in range(r) for j in range(r)):
            return True
        P = mat_mul(P, M, r)
    return False


def perron_freq(M, r, ell):
    """Exact normalized letter-frequency vector of a primitive uniform
    morphism: the Perron eigenvalue of a length-ell uniform incidence
    matrix is ell (all column sums equal ell), so the frequency vector
    spans the rational null space of M - ell*I.

    Computed here by exact Gaussian elimination over Fraction -- a
    different implementation from the hand-rolled cross-product route of
    the rigidity packet -- and then VERIFIED to satisfy M v = ell v.
    Returns None unless the null space is exactly one positive line.
    """
    A = [[Fraction(M[i][j]) - (ell if i == j else 0) for j in range(r)]
         for i in range(r)]
    # forward elimination with partial pivoting on exact rationals
    pivots = []
    row = 0
    for col in range(r):
        piv = next((i for i in range(row, r) if A[i][col] != 0), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        inv = A[row][col]
        A[row] = [x / inv for x in A[row]]
        for i in range(r):
            if i != row and A[i][col] != 0:
                fac = A[i][col]
                A[i] = [A[i][j] - fac * A[row][j] for j in range(r)]
        pivots.append(col)
        row += 1
    free = [c for c in range(r) if c not in pivots]
    if len(free) != 1:
        return None                     # null space must be a single line
    fc = free[0]
    v = [Fraction(0)] * r
    v[fc] = Fraction(1)
    for i, pc in enumerate(pivots):
        v[pc] = -A[i][fc]
    for i in range(r):
        if sum(Fraction(M[i][j]) * v[j] for j in range(r)) != ell * v[i]:
            return None
    s = sum(v)
    if s == 0:
        return None
    v = [x / s for x in v]
    if any(x <= 0 for x in v):
        return None                     # Perron vector is strictly positive
    return v


def minimal_period_of_suffix(word, start):
    """KMP minimal period of word[start:], or None.  NUMERIC CONTROL only:
    no conclusion in this packet depends on the periodicity label."""
    s = word[start:]
    n = len(s)
    if n < 6:
        return None
    pi = [0] * n
    for i in range(1, n):
        t = pi[i - 1]
        while t > 0 and s[i] != s[t]:
            t = pi[t - 1]
        if s[i] == s[t]:
            t += 1
        pi[i] = t
    p = n - pi[-1]
    if p <= n // 3 and all(s[i] == s[i + p] for i in range(n - p)):
        return p
    return None


# ---------------------------------------------------------------------------
# 6.  finite exact controls for the two atlas inequalities
# ---------------------------------------------------------------------------

def check_collision_principle(nmax, k):
    """Lemma 1 + Lemma 2 (landmark memo), exact, on true Terras orbits.

    (a) equal length-k parity blocks at positions i<j  =>  2^k | x_i - x_j;
    (b) if in addition both states are < 2^k, the states are EQUAL and the
        orbit repeats -- the collision principle Theorem 4.1 rests on.
    """
    checked = 0
    collisions = 0
    for n in range(1, nmax + 1):
        xs, q = terras_orbit(n, 3 * k + 40)
        blocks = {}
        for i in range(len(q) - k):
            w = tuple(q[i:i + k])
            if w in blocks:
                j = blocks[w]
                need((xs[j] - xs[i]) % (1 << k) == 0,
                     "Lemma 1 failed: equal parity blocks, unequal residues")
                checked += 1
                if xs[i] < (1 << k) and xs[j] < (1 << k):
                    need(xs[i] == xs[j],
                         "Lemma 2 failed: small distinct states share a block")
                    collisions += 1
            else:
                blocks[w] = i
    return {"orbits": nmax, "block_length": k,
            "equal_block_pairs_checked": checked,
            "small_state_collisions_forced_equal": collisions}


def check_balance_bound(word, ell, f, nmax):
    """Exact integer control for step 1 of the memo's proof:

        ell * s(i,j) <= f * (j-i) + f * ell     for every 0 <= i < j <= nmax,

    where f = f(ell) is the maximal number of ones in a length-ell factor.
    This is the integer content of  D_N <= (B - alpha) N + f.
    """
    pre = [0] * (len(word) + 1)
    for i, b in enumerate(word):
        pre[i + 1] = pre[i] + b
    hi = min(nmax, len(word))
    worst = None
    for i in range(hi):
        for j in range(i + 1, hi + 1):
            s = pre[j] - pre[i]
            need(ell * s <= f * (j - i) + f * ell,
                 "balance bound violated: ell*s(i,j) > f*(j-i) + f*ell")
            slack = f * (j - i) + f * ell - ell * s
            if worst is None or slack < worst[0]:
                worst = (slack, i, j)
    return {"pairs_checked": hi * (hi + 1) // 2,
            "min_slack": worst[0], "argmin_i": worst[1], "argmin_j": worst[2]}


# ---------------------------------------------------------------------------
# 7.  enumeration of the supercritical primitive stratum
# ---------------------------------------------------------------------------

def enumerate_supercritical(r, ell, use_codings):
    """Records for every primitive uniform length-ell morphism on r letters
    (all prolongable seeds, optionally all nonconstant codings) whose coded
    fixed point has exact one-density rho > alpha.

    Deduplication is per (r, ell) sweep on the first DEDUP symbols, exactly
    as in `verify_automatic_rigidity.py`, so that the resulting stratum is
    directly comparable with that packet's survivor list.
    """
    seen = {}
    out = []
    codings = [None]
    if use_codings:
        codings = [tuple((mask >> a) & 1 for a in range(r))
                   for mask in range(1, 2 ** r - 1)]
    for sigma in iterproduct(iterproduct(range(r), repeat=ell), repeat=r):
        M = incidence(sigma, r)
        if not is_primitive(M, r):
            continue
        freq = perron_freq(M, r, ell)
        if freq is None:
            continue
        for seed in range(r):
            if sigma[seed][0] != seed:
                continue
            base = None
            for coding in codings:
                if base is None:
                    base = fixed_point_prefix(sigma, seed, PREFIX)
                cod = coding if coding is not None else tuple(
                    1 if a == 1 else 0 for a in range(r))
                word = [cod[a] for a in base]
                key = tuple(word[:DEDUP])
                if key in seen:
                    continue
                seen[key] = True
                rho = sum((freq[a] for a in range(r) if cod[a] == 1),
                          Fraction(0))
                c = cmp_frac_alpha(rho)
                need(c != 0, "rho == alpha exactly: Gelfond-Schneider violated")
                if c != 1:
                    continue                      # subcritical: packet 1 kills
                p = minimal_period_of_suffix(word, len(word) // 4)
                if p is None:
                    p = minimal_period_of_suffix(word, 0)
                out.append({
                    "alphabet": r, "length": ell,
                    "sigma": ",".join("".join(map(str, w)) for w in sigma),
                    "seed": seed,
                    "coding": ("".join(map(str, coding))
                               if coding is not None else None),
                    "rho": str(rho),
                    "rho_gt_alpha_witness": "3^%d > 2^%d" % (
                        rho.numerator, rho.denominator),
                    "period_numeric_control": p,
                    "_sigma": sigma, "_seed": seed, "_coding": cod,
                })
    return out


# ---------------------------------------------------------------------------
# 8.  per-word kill
# ---------------------------------------------------------------------------

_BLOCK_CACHE = {}
SURV_SRC = {}


def analyse(rec):
    sigma, seed, cod = rec["_sigma"], rec["_seed"], rec["_coding"]
    SURV_SRC[(rec["sigma"], rec["seed"], rec.get("coding"))] = (sigma, seed,
                                                                cod)
    k = rec["length"]
    R = 0
    while k ** R < max(k * M0 + 1, ELL_DENS):
        R += 1
    kR = k ** R
    ck = (sigma, seed, R)
    if ck not in _BLOCK_CACHE:
        _BLOCK_CACHE[ck] = window_blocks(sigma, seed, R)
    blocks = _BLOCK_CACHE[ck]

    c_exact, pv = complexity_bound(blocks, kR, k, M0)
    c = round_up_frac(c_exact, 64)                # weaken to a small rational
    f = max_factor_ones(blocks, kR, cod, ELL_DENS)
    B = Fraction(f, ELL_DENS)
    rho = Fraction(rec["rho"])
    # Corollary 7 needs beta > alpha; and the maximal factor density can
    # never fall below the mean density.  Both are exact checks.
    need(B >= rho, "max factor density fell below the Perron density")
    need(cmp_frac_alpha(B) == 1, "beta = f(ell)/ell is not above alpha")

    kap_ok, kap_wit = kill_kappa(c)
    # (a) self-contained: B = f(ell)/ell is an exact finite upper bound for
    #     the asymptotic maximal factor density (Fekete subadditivity).
    den_ok, den_wit = kill_density(c, B)
    # (b) one cited classical input: a primitive substitution subshift is
    #     uniquely ergodic, so long factors have one-density -> rho
    #     uniformly, and the asymptotic maximal factor density IS rho.
    rho_ok, rho_wit = kill_density(c, rho)

    rec.update({
        "complexity_window": "[%d, %d]" % (M0, k * M0),
        "complexity_nodes": len(pv),
        "p_u_at_m0_plus_1": pv[M0],
        "p_u_at_k_m0_plus_1": pv[k * M0],
        "C_upper_bound_exact": str(c_exact),
        "C_upper_bound_used": str(c),
        "max_factor_ones_f(ell)": f,
        "ell": ELL_DENS,
        "B_ell": str(B),
        "killed_by_kappa_corollary4": kap_ok,
        "kappa_witness": "3^%d < 2^%d" % kap_wit,
        "killed_by_density_selfcontained": den_ok,
        "density_witness_selfcontained": "3^%d < 2^%d" % den_wit,
        "killed_by_density_unique_ergodicity": rho_ok,
        "density_witness_rho": "3^%d < 2^%d" % rho_wit,
    })
    for key in ("_sigma", "_seed", "_coding"):
        rec.pop(key)
    return rec


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    cert = {
        "packet": "2026-07-24-supercritical-automatic-closure",
        "scope": ("exact integer/Fraction arithmetic on every certificate "
                  "path; no proved statement depends on a float"),
        "env": {"VSAC_M0": M0, "VSAC_ELL_DENS": ELL_DENS,
                "VSAC_MAXLEN": MAXLEN, "VSAC_TERNARY": TERNARY,
                "VSAC_NCHECK": NCHECK, "VSAC_PREFIX": PREFIX},
    }

    # --- A. alpha arithmetic ------------------------------------------------
    alo, ahi = alpha_bracket()
    need(alo < ahi, "alpha bracket is inverted")
    klo, khi = kappa_bounds()
    cert["constants"] = {
        "alpha_definition": "alpha = log_3 2",
        "alpha_bracket": "%s < alpha < %s" % (alo, ahi),
        "alpha_bracket_witnesses": [
            "3^%d < 2^%d" % (alo.numerator, alo.denominator),
            "3^%d > 2^%d" % (ahi.numerator, ahi.denominator)],
        "kappa_identity": "kappa = 1/log_2(3/2) = alpha/(1-alpha)",
        "kappa_bracket": "%s .. %s" % (klo, khi),
        "kappa_numeric": "%.10f (numeric, read off the exact bracket)"
                         % float(klo),
    }
    # The endpoint identity that makes Corollary 7' contain Corollary 4:
    # beta = 1 in  C >= alpha/(beta-alpha)  gives exactly alpha/(1-alpha),
    # which must be the landmark memo's kappa = 1.7095112913...
    need(klo < Fraction(17095112913, 10 ** 10) < khi,
         "alpha/(1-alpha) bracket does not contain kappa = 1.7095112913")

    # --- B. Phi engine: two independent paths agree -------------------------
    L = 64
    for n in range(1, NCHECK + 1):
        _, q = terras_orbit(n, L)
        a = phi_mod_lift(q, L)
        b = phi_mod_series(q, L)
        need(a == b, "lift-cocycle and modular-series Phi disagree at n=%d" % n)
        need(a == n % (1 << L), "Phi(transcript of n) != n mod 2^64 at n=%d" % n)
    cert["phi_engine"] = {
        "paths": ["lift/quotient cocycle (LIFT_COCYCLE.md)",
                  "modular series (PARTIAL_THEOREMS.md Thm 2)"],
        "orbits_cross_checked": NCHECK, "modulus": "2^64",
        "all_agree": True}

    # --- C. collision principle on true orbits ------------------------------
    cert["collision_principle"] = check_collision_principle(
        200 if REDUCED else 600, 12)

    # --- D. enumeration of the supercritical primitive stratum --------------
    recs = []
    for ell_i in range(2, MAXLEN + 1):
        recs += enumerate_supercritical(2, ell_i, False)
    n_binary = len(recs)
    if TERNARY:
        recs += enumerate_supercritical(3, 2, True)
    n_ternary = len(recs) - n_binary
    cert["stratum"] = {
        "binary_ell<=%d" % MAXLEN: n_binary,
        "ternary_ell2_coded": n_ternary,
        "total_supercritical_primitive": len(recs),
    }

    # --- E. balance bound control on one enumerated word --------------------
    if recs:
        r0 = recs[0]
        w0 = [r0["_coding"][a] for a in
              fixed_point_prefix(r0["_sigma"], r0["_seed"], 4 * ELL_DENS)]
        R0 = 0
        while r0["length"] ** R0 < ELL_DENS:
            R0 += 1
        b0 = window_blocks(r0["_sigma"], r0["_seed"], R0)
        f0 = max_factor_ones(b0, r0["length"] ** R0, r0["_coding"], ELL_DENS)
        cert["balance_bound_control"] = check_balance_bound(
            w0, ELL_DENS, f0, 200 if REDUCED else 700)
        cert["balance_bound_control"]["word"] = r0["sigma"]

    # --- F. exact-language control vs brute force ---------------------------
    lang_checks = []
    for rec in recs[: (3 if REDUCED else 8)]:
        k = rec["length"]
        R = 0
        while k ** R < 128:
            R += 1
        blocks = window_blocks(rec["_sigma"], rec["_seed"], R)
        pref = bytes(fixed_point_prefix(rec["_sigma"], rec["_seed"], 1 << 15))
        for n in (2, 3, 8, 32, 96):
            ex = factors_exact(blocks, k ** R, n)
            br = {pref[i:i + n] for i in range(len(pref) - n + 1)}
            need(br <= ex, "brute-force factor not in the exact factor set")
            need(ex == br,
                 "exact factor set exceeds the observed language at n=%d" % n)
        lang_checks.append({"sigma": rec["sigma"], "seed": rec["seed"],
                            "lengths": [2, 3, 8, 32, 96],
                            "exact_equals_brute_force": True})
    cert["exact_language_controls"] = lang_checks

    # --- G. the kill ---------------------------------------------------------
    out = [analyse(rec) for rec in recs]

    def sc(r):      # self-contained: kappa route or f(ell) density route
        return (r["killed_by_kappa_corollary4"]
                or r["killed_by_density_selfcontained"])

    def full(r):    # additionally allowing the unique-ergodicity input
        return sc(r) or r["killed_by_density_unique_ergodicity"]

    killed_sc = [r for r in out if sc(r)]
    killed_full = [r for r in out if full(r)]
    survivors = [r for r in out if not full(r)]

    cert["records"] = out
    cert["result"] = {
        "supercritical_primitive_words": len(out),
        "killed_by_corollary4_kappa": sum(
            1 for r in out if r["killed_by_kappa_corollary4"]),
        "killed_by_density_selfcontained": sum(
            1 for r in out if r["killed_by_density_selfcontained"]),
        "killed_by_density_unique_ergodicity": sum(
            1 for r in out if r["killed_by_density_unique_ergodicity"]),
        "killed_self_contained_total": len(killed_sc),
        "killed_with_unique_ergodicity_total": len(killed_full),
        "not_killed": len(survivors),
        "conclusion": ("for every killed word Phi(q) is not in Z_{>0}: the "
                       "aperiodic branch by the complexity contradiction, "
                       "the eventually-periodic branch by the cycle "
                       "equation rho < alpha (each rho > alpha is certified "
                       "by an exact 3^a > 2^b witness)"),
    }
    # For each survivor, record an exact factor count deep in the language.
    # It shows whether the failure is real or an artifact of the bound's
    # slack: if p(n)/n already exceeds alpha/(rho - alpha), no tightening of
    # Lemma D can close that word.
    surv_out = []
    for r in survivors:
        sig = SURV_SRC[(r["sigma"], r["seed"], r["coding"])]
        k = r["length"]
        R = 0
        while k ** R < FRONTIER_N:
            R += 1
        blocks = window_blocks(sig[0], sig[1], R)
        pn = len(factors_exact(blocks, k ** R, FRONTIER_N))
        rho = Fraction(r["rho"])
        # threshold fires iff  ratio*(rho - alpha) < alpha
        #                 iff  rho*ratio/(1+ratio) < alpha
        ratio = Fraction(pn, FRONTIER_N)
        below, _ = kill_density(ratio, rho)
        surv_out.append({
            "sigma": r["sigma"], "seed": r["seed"], "coding": r["coding"],
            "rho": r["rho"], "C_upper_bound_used": r["C_upper_bound_used"],
            "B_ell": r["B_ell"],
            "exact_p_u_at_n": {"n": FRONTIER_N, "p": pn,
                               "p_over_n": str(ratio)},
            "even_this_exact_ratio_would_not_fire": not below,
            "verdict": ("genuinely above the density threshold: even the "
                        "exact factor count at n=%d exceeds "
                        "alpha/(rho-alpha)" % FRONTIER_N) if not below else
                       ("bound slack only: the exact ratio at n=%d is below "
                        "the threshold, so a tighter Lemma D window would "
                        "close this word" % FRONTIER_N),
        })
    cert["result"]["survivor_sigmas"] = surv_out

    # --- H. cross-reference against the rigidity packet's survivor list -----
    rig = os.path.join(HERE, os.pardir,
                       "2026-07-22-automatic-transcript-rigidity",
                       "automatic_rigidity_certificate.json")
    full_sweep = MAXLEN >= 4 and TERNARY
    if not full_sweep:
        cert["cross_reference_rigidity_packet"] = {
            "status": "skipped: reduced sweep does not cover the rigidity "
                      "packet's enumeration (needs MAXLEN>=4 and ternary)"}
    elif os.path.exists(rig):
        with open(rig) as fh:
            rc = json.load(fh)
        theirs = {(s["sigma"], s["seed"], s.get("coding"))
                  for s in rc["survivors_supercritical_primitive"]}
        mine = {(r["sigma"], r["seed"], r["coding"]) for r in out}
        need(not (theirs - mine),
             "the rigidity packet lists a survivor this sweep did not "
             "reproduce: %r" % sorted(theirs - mine)[:3])
        k_sc = {(r["sigma"], r["seed"], r["coding"]) for r in killed_sc}
        k_fl = {(r["sigma"], r["seed"], r["coding"]) for r in killed_full}
        cert["cross_reference_rigidity_packet"] = {
            "their_supercritical_survivors": len(theirs),
            "reproduced_by_this_sweep": len(theirs & mine),
            "closed_here_self_contained": len(theirs & k_sc),
            "closed_here_with_unique_ergodicity": len(theirs & k_fl),
            "still_open": sorted(map(list, theirs - k_fl)),
            "still_open_count": len(theirs - k_fl),
            "binary_still_open": sorted(
                list(x) for x in (theirs - k_fl) if x[2] is None),
        }
        cert["result"]["headline"] = (
            "%d of the %d supercritical survivors of "
            "2026-07-22-automatic-transcript-rigidity are proved to have "
            "Phi(q) not in Z_{>0}; %d remain open."
            % (len(theirs & k_fl), len(theirs), len(theirs - k_fl)))
    else:
        cert["cross_reference_rigidity_packet"] = {
            "status": "rigidity certificate not found; cross-check skipped"}

    path = os.environ.get("VSAC_OUT") or os.path.join(
        HERE, "supercritical_closure_certificate.json")
    with open(path, "w") as fh:
        fh.write(json.dumps(cert, indent=2, sort_keys=True) + "\n")

    summary = {
        "status": "ok",
        "env": cert["env"],
        "phi_orbits_cross_checked": NCHECK,
        "stratum": cert["stratum"],
        "cross_reference_rigidity_packet": {
            k: v for k, v in cert["cross_reference_rigidity_packet"].items()
            if k != "still_open"},
        "result": {k: v for k, v in cert["result"].items()
                   if k not in ("conclusion", "survivor_sigmas")},
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fail as exc:
        print("KILL CRITERION FIRED: %s" % exc, file=sys.stderr)
        sys.exit(2)
