"""
F1 — Collatz word-fold calculus (Terras-accelerated map).

Exact integer arithmetic only for certificates.
Python 3 stdlib; arbitrary-precision ints throughout the core.

Definitions (packet-exact)
-------------------------
Terras map on positive integers:
    T(n) = n/2           if n even
    T(n) = (3n+1)/2      if n odd

Parity word of n, length k: w = (w_0, ..., w_{k-1}) with
    w_i = parity bit of T^i(n)   (1 = odd step, 0 = even step).

Composite affine form: a fixed word w of length L with a ones computes
    n  ↦  (3^a · n + c_w) / 2^L
where c_w is the nonnegative integer derived below.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

# Word bits: 1 = odd Terras step, 0 = even Terras step
Word = Sequence[int]  # each entry in {0, 1}


# ---------------------------------------------------------------------------
# Core map
# ---------------------------------------------------------------------------

def terras(n: int) -> int:
    """One Terras-accelerated Collatz step. n must be a positive integer."""
    if n <= 0:
        raise ValueError(f"terras requires positive integer, got {n}")
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def terras_iter(n: int, k: int) -> int:
    """T^k(n) by direct iteration."""
    for _ in range(k):
        n = terras(n)
    return n


def parity_word(n: int, length: int) -> Tuple[int, ...]:
    """Parity word of n of length `length`: bits of T^0(n), ..., T^{length-1}(n)."""
    if length < 0:
        raise ValueError("length must be nonnegative")
    bits: List[int] = []
    x = n
    for _ in range(length):
        bits.append(x & 1)
        x = terras(x)
    return tuple(bits)


# ---------------------------------------------------------------------------
# Composite affine form
# ---------------------------------------------------------------------------
#
# Inductive derivation of c_w:
#   Represent the state after s steps as (A·n + C) / 2^s with A = 3^{#odds so far}.
#   Even step (w_s = 0):  next = m/2          →  A' = A,     C' = C
#   Odd  step (w_s = 1):  next = (3m+1)/2     →  A' = 3A,    C' = 3C + 2^s
#
# After L steps with a ones: T_w^L(n) = (3^a · n + c_w) / 2^L, where c_w = C.
#
# Closed form: if odd steps occur at 0-based indices i_1 < ... < i_a,
#   c_w = Σ_{j=1}^{a}  3^{a-j} · 2^{i_j}.
#

def word_composite(w: Word) -> Tuple[int, int, int]:
    """
    Map word w → (3^a, c_w, 2^L).

    Returns exact integers (pow3, c_w, pow2) such that applying w yields
        (pow3 * n + c_w) // pow2
    whenever n follows word w (so the division is exact and yields an integer).
    """
    a = 0
    c = 0
    L = len(w)
    for i, bit in enumerate(w):
        if bit not in (0, 1):
            raise ValueError(f"word bits must be 0 or 1, got {bit}")
        if bit == 1:
            c = 3 * c + (1 << i)  # 3C + 2^i
            a += 1
    return (3 ** a, c, 1 << L)


def apply_composite(n: int, w: Word) -> int:
    """Apply the composite affine form of w to n (exact integer division)."""
    pow3, c, pow2 = word_composite(w)
    num = pow3 * n + c
    if num % pow2 != 0:
        raise ValueError(
            f"composite not integral: ({pow3}*{n}+{c}) not divisible by {pow2}"
        )
    return num // pow2


def c_w_closed_form(w: Word) -> int:
    """Closed-form c_w for cross-check against the inductive accumulator."""
    odd_indices = [i for i, b in enumerate(w) if b == 1]
    a = len(odd_indices)
    c = 0
    for j, i_j in enumerate(odd_indices):
        # j is 0-based among odds; exponent of 3 is a - (j+1) = a - j - 1
        c += (3 ** (a - j - 1)) * (1 << i_j)
    return c


# ---------------------------------------------------------------------------
# Terras bijection (mod 2^k ↔ length-k parity words)
# ---------------------------------------------------------------------------

def terras_bijection_check(k: int) -> Tuple[bool, str]:
    """
    Verify: as n runs through 0..2^k-1 (or 1..2^k with n mod 2^k),
    the length-k parity words of the residue class are all distinct and
    therefore hit every word in {0,1}^k exactly once.

    Exact statement verified:
      For each k, the map
          φ_k : Z/2^k Z → {0,1}^k
          φ_k([n]) = parity word of length k of any positive lift of [n]
      is a bijection.  (Positive lift: n if n>0, else n+2^k.)

    Returns (ok, message).
    """
    if k < 0:
        raise ValueError("k must be nonnegative")
    if k == 0:
        return True, "k=0: trivial bijection on a singleton"
    mod = 1 << k
    seen = {}
    for r in range(mod):
        n = r if r > 0 else mod  # positive lift of residue 0 is 2^k
        w = parity_word(n, k)
        if w in seen:
            return False, f"collision at k={k}: n≡{seen[w]} and n≡{r} both give {w}"
        seen[w] = r
    if len(seen) != mod:
        return False, f"k={k}: only {len(seen)} distinct words, expected {mod}"
    return True, (
        f"k={k}: φ_k : Z/2^{k}Z → {{0,1}}^{k} is bijective "
        f"({mod} residues → {mod} distinct length-{k} parity words)"
    )


# ---------------------------------------------------------------------------
# Cycle-candidate sweep
# ---------------------------------------------------------------------------
#
# Fixed point of the composite for word w:
#   n = (3^a n + c_w) / 2^L
#   n (2^L - 3^a) = c_w
#   n = c_w / (2^L - 3^a)
# Require 2^L > 3^a (positive denominator), n positive integer, and
# parity_word(n, L) == w.
#

def cycle_n_for_word(w: Word) -> Tuple[int | None, int, int, int]:
    """
    Return (n_or_None, a, c_w, L).
    n is the unique rational fixed point of the affine form when 2^L != 3^a;
    returned only if it is a positive integer (division exact and n > 0).
    """
    L = len(w)
    a = sum(1 for b in w if b == 1)
    pow3, c, pow2 = word_composite(w)
    denom = pow2 - pow3
    if denom <= 0:
        return None, a, c, L
    if c % denom != 0:
        return None, a, c, L
    n = c // denom
    if n <= 0:
        return None, a, c, L
    return n, a, c, L


def is_canonical_necklace_mask(mask: int, L: int) -> bool:
    """
    True if the length-L bitstring (bit i = word step i) is the lexicographically
    minimal rotation among its cyclic shifts. Bit order: step 0 = LSB.
    Lex order compares step 0 first, then step 1, etc.
    """
    if L <= 1:
        return True
    # Extract bits once
    bits = [(mask >> i) & 1 for i in range(L)]
    for s in range(1, L):
        # Compare rotation starting at s with rotation starting at 0
        less = False
        for j in range(L):
            a = bits[(s + j) % L]
            b = bits[j]
            if a < b:
                less = True
                break
            if a > b:
                break
        else:
            continue  # equal rotation
        if less:
            return False
    return True


def cycle_candidate_sweep(
    max_L: int = 24,
    *,
    skip_cyclic_duplicates: bool = True,
) -> dict:
    """
    Exhaustive enumeration over words with 1 ≤ L ≤ max_L.
    Prune: require 2^L > 3^a before testing integrality of n.
    Optionally skip non-canonical necklaces (non-minimal cyclic rotations at fixed L).

    Returns a result dict with counts and the list of verified positive cycles.
    """
    words_examined = 0
    words_pruned_growth = 0
    words_skipped_necklace = 0
    candidates_integral = 0
    verified_cycles: List[dict] = []

    pow3_table = [3 ** a for a in range(max_L + 1)]

    for L in range(1, max_L + 1):
        pow2 = 1 << L
        n_words = 1 << L
        # max a with 3^a < 2^L
        max_a_ok = 0
        while max_a_ok < L and pow3_table[max_a_ok + 1] < pow2:
            max_a_ok += 1

        for mask in range(n_words):
            a = mask.bit_count()
            if a > max_a_ok:
                words_pruned_growth += 1
                continue

            if skip_cyclic_duplicates and not is_canonical_necklace_mask(mask, L):
                words_skipped_necklace += 1
                continue

            words_examined += 1

            # c_w inductive: odd at bit i → c = 3c + 2^i
            c = 0
            m = mask
            i = 0
            while m:
                if m & 1:
                    c = 3 * c + (1 << i)
                m >>= 1
                i += 1
                if i >= L:
                    break
            # also handle remaining zero high bits — no odds there

            denom = pow2 - pow3_table[a]
            if c % denom != 0:
                continue
            n = c // denom
            if n <= 0:
                continue
            candidates_integral += 1

            w = tuple((mask >> i) & 1 for i in range(L))
            if parity_word(n, L) != w:
                continue
            if apply_composite(n, w) != n:
                continue

            verified_cycles.append(
                {
                    "n": n,
                    "L": L,
                    "a": a,
                    "word": w,
                    "c_w": c,
                    "denom": denom,
                }
            )

    trivial_ns = {1, 2}
    orbit_trivial = set()
    for cyc in verified_cycles:
        n0 = cyc["n"]
        x = n0
        seen: set = set()
        while x not in seen and len(seen) < 100:
            seen.add(x)
            x = terras(x)
        if seen <= {1, 2} or ({1, 2} <= seen):
            orbit_trivial.add(n0)

    nontrivial_outside = [
        c
        for c in verified_cycles
        if c["n"] not in orbit_trivial and c["n"] not in trivial_ns
    ]

    return {
        "max_L": max_L,
        "words_examined": words_examined,
        "words_pruned_growth": words_pruned_growth,
        "words_skipped_necklace": words_skipped_necklace,
        "candidates_integral": candidates_integral,
        "verified_cycles": verified_cycles,
        "nontrivial_outside_orbit_1_2": nontrivial_outside,
        "only_trivial": len(nontrivial_outside) == 0,
    }


# ---------------------------------------------------------------------------
# Stopping-time spectrum
# ---------------------------------------------------------------------------

def stopping_time(n: int) -> int:
    """Least k ≥ 1 with T^k(n) < n. Raises if n ≤ 1 (never drops below 1)."""
    if n <= 1:
        raise ValueError("stopping_time defined for n ≥ 2")
    k = 0
    x = n
    while True:
        x = terras(x)
        k += 1
        if x < n:
            return k


def total_stopping_time(n: int, cache: dict | None = None) -> int:
    """
    Least k ≥ 0 with T^k(n) = 1.
    Uses optional memo cache mapping m → steps from m to 1.
    """
    if n < 1:
        raise ValueError("n must be positive")
    if cache is None:
        # no cache: plain walk
        k = 0
        x = n
        while x != 1:
            x = terras(x)
            k += 1
        return k

    # Path compression cache
    if n in cache:
        return cache[n]
    path: List[int] = []
    x = n
    while x not in cache and x != 1:
        path.append(x)
        x = terras(x)
    # base
    steps_from_x = 0 if x == 1 else cache[x]
    # fill backwards
    for i in range(len(path) - 1, -1, -1):
        steps_from_x += 1
        cache[path[i]] = steps_from_x
    cache.setdefault(1, 0)
    return cache[n]


def stopping_time_spectrum(limit: int = 1 << 20) -> dict:
    """
    For all n with 2 ≤ n < limit: stopping time.
    For all n with 1 ≤ n < limit: total stopping time.
    Returns distribution summary (percentiles, max, argmax).
    Floats only in summary stats.
    """
    import time

    t0 = time.perf_counter()
    stop_times: List[int] = []
    max_st = -1
    argmax_st = None
    for n in range(2, limit):
        st = stopping_time(n)
        stop_times.append(st)
        if st > max_st:
            max_st = st
            argmax_st = n
    t_stop = time.perf_counter() - t0

    t1 = time.perf_counter()
    cache: dict = {1: 0}
    total_times: List[int] = [0]  # n=1
    max_tst = 0
    argmax_tst = 1
    for n in range(2, limit):
        tst = total_stopping_time(n, cache)
        total_times.append(tst)
        if tst > max_tst:
            max_tst = tst
            argmax_tst = n
    t_total = time.perf_counter() - t1

    def percentiles(data: List[int], ps: Iterable[float]) -> dict:
        if not data:
            return {}
        s = sorted(data)
        m = len(s)
        out = {}
        for p in ps:
            # nearest-rank style
            if m == 1:
                out[p] = s[0]
                continue
            idx = min(m - 1, max(0, int(round((p / 100.0) * (m - 1)))))
            out[p] = s[idx]
        return out

    ps = (50, 90, 99, 99.9)
    return {
        "limit": limit,
        "n_range_stopping": f"[2, {limit})",
        "n_range_total": f"[1, {limit})",
        "stopping": {
            "count": len(stop_times),
            "max": max_st,
            "argmax": argmax_st,
            "min": min(stop_times) if stop_times else None,
            "mean": (sum(stop_times) / len(stop_times)) if stop_times else None,
            "percentiles": percentiles(stop_times, ps),
            "runtime_s": t_stop,
        },
        "total_stopping": {
            "count": len(total_times),
            "max": max_tst,
            "argmax": argmax_tst,
            "min": min(total_times) if total_times else None,
            "mean": (sum(total_times) / len(total_times)) if total_times else None,
            "percentiles": percentiles(total_times, ps),
            "runtime_s": t_total,
        },
    }


# ---------------------------------------------------------------------------
# Extremal-word atlas
# ---------------------------------------------------------------------------

def extremal_word_check(k: int) -> Tuple[bool, str]:
    """
    Assert for n = 2^k - 1:
      - parity word of length k is (1,1,...,1)  (k consecutive odd steps)
      - T^k(2^k - 1) = 3^k - 1
    """
    if k < 1:
        raise ValueError("k ≥ 1")
    n = (1 << k) - 1
    w = parity_word(n, k)
    expected_w = tuple(1 for _ in range(k))
    if w != expected_w:
        return False, f"k={k}: parity word of {n} is {w}, expected all-ones"
    got = terras_iter(n, k)
    expected = (3 ** k) - 1
    if got != expected:
        return False, f"k={k}: T^{k}({n})={got}, expected {expected}"
    # also via composite
    pow3, c, pow2 = word_composite(expected_w)
    via = (pow3 * n + c) // pow2
    if via != expected:
        return False, f"k={k}: composite gives {via}, expected {expected}"
    return True, f"k={k}: n=2^{k}-1={n} takes {k} odd steps; T^{k}(n)=3^{k}-1={expected}"


def extremal_word_atlas(max_k: int = 30) -> dict:
    results = []
    all_ok = True
    for k in range(1, max_k + 1):
        ok, msg = extremal_word_check(k)
        results.append({"k": k, "ok": ok, "msg": msg})
        if not ok:
            all_ok = False
    return {"max_k": max_k, "all_ok": all_ok, "results": results}


# ---------------------------------------------------------------------------
# Property tests helpers (used by test_f1 and CLI)
# ---------------------------------------------------------------------------

def random_composite_property_test(
    num_samples: int = 10_000,
    n_max: int = 10**6,
    L_max: int = 30,
    seed: int = 20260718,
) -> dict:
    """
    For ≥ num_samples random n < n_max, take L ≤ L_max, form n's own parity word
    of length L, and check apply_composite(n, w) == T^L(n).
    """
    import random
    import time

    rng = random.Random(seed)
    t0 = time.perf_counter()
    failures = []
    for i in range(num_samples):
        n = rng.randrange(1, n_max)
        L = rng.randrange(1, L_max + 1)
        w = parity_word(n, L)
        direct = terras_iter(n, L)
        try:
            via = apply_composite(n, w)
        except ValueError as e:
            failures.append((n, L, w, str(e)))
            continue
        if via != direct:
            failures.append((n, L, w, f"composite={via} direct={direct}"))
        # closed-form c_w check
        _, c_ind, _ = word_composite(w)
        c_cf = c_w_closed_form(w)
        if c_ind != c_cf:
            failures.append((n, L, w, f"c_w mismatch ind={c_ind} closed={c_cf}"))
    elapsed = time.perf_counter() - t0
    return {
        "num_samples": num_samples,
        "n_max": n_max,
        "L_max": L_max,
        "seed": seed,
        "failures": failures,
        "ok": len(failures) == 0,
        "runtime_s": elapsed,
    }


def run_all_calibrations(
    *,
    composite_samples: int = 10_000,
    bijection_max_k: int = 20,
    cycle_max_L: int = 24,
    spectrum_limit: int = 1 << 20,
    extremal_max_k: int = 30,
) -> dict:
    """Run all F1 calibration sections; return structured results with timings."""
    import time

    out: dict = {}

    # 1. Composite calculus property test
    out["composite"] = random_composite_property_test(num_samples=composite_samples)

    # 2. Terras bijection
    t0 = time.perf_counter()
    bij = []
    bij_ok = True
    for k in range(0, bijection_max_k + 1):
        ok, msg = terras_bijection_check(k)
        bij.append({"k": k, "ok": ok, "msg": msg})
        if not ok:
            bij_ok = False
    out["bijection"] = {
        "max_k": bijection_max_k,
        "ok": bij_ok,
        "details": bij,
        "statement": (
            "For each k ≤ {mk}, the map φ_k : Z/2^k Z → {{0,1}}^k sending a residue "
            "class [n] to the length-k parity word of a positive lift of [n] is a "
            "bijection (hits every word exactly once)."
        ).format(mk=bijection_max_k),
        "runtime_s": time.perf_counter() - t0,
    }

    # 3. Cycle sweep
    t0 = time.perf_counter()
    cycle = cycle_candidate_sweep(max_L=cycle_max_L, skip_cyclic_duplicates=True)
    cycle["runtime_s"] = time.perf_counter() - t0
    out["cycles"] = cycle

    # 4. Stopping-time spectrum
    out["spectrum"] = stopping_time_spectrum(limit=spectrum_limit)

    # 5. Extremal words
    t0 = time.perf_counter()
    ext = extremal_word_atlas(max_k=extremal_max_k)
    ext["runtime_s"] = time.perf_counter() - t0
    out["extremal"] = ext

    return out


if __name__ == "__main__":
    import json
    import time

    t_all = time.perf_counter()
    results = run_all_calibrations()
    results["total_runtime_s"] = time.perf_counter() - t_all
    # compact print for CLI
    print("=== F1 word-fold calibration ===")
    print(f"composite ok={results['composite']['ok']} "
          f"samples={results['composite']['num_samples']} "
          f"t={results['composite']['runtime_s']:.3f}s")
    print(f"bijection ok={results['bijection']['ok']} "
          f"k≤{results['bijection']['max_k']} "
          f"t={results['bijection']['runtime_s']:.3f}s")
    cyc = results["cycles"]
    print(
        f"cycles examined={cyc['words_examined']} "
        f"integral={cyc['candidates_integral']} "
        f"verified={len(cyc['verified_cycles'])} "
        f"only_trivial={cyc['only_trivial']} "
        f"t={cyc['runtime_s']:.3f}s"
    )
    for v in cyc["verified_cycles"]:
        print(f"  cycle n={v['n']} L={v['L']} a={v['a']} word={v['word']}")
    sp = results["spectrum"]
    print(
        f"spectrum limit={sp['limit']} "
        f"stop_max={sp['stopping']['max']}@{sp['stopping']['argmax']} "
        f"total_max={sp['total_stopping']['max']}@{sp['total_stopping']['argmax']} "
        f"t_stop={sp['stopping']['runtime_s']:.3f}s "
        f"t_tot={sp['total_stopping']['runtime_s']:.3f}s"
    )
    print(f"extremal ok={results['extremal']['all_ok']} "
          f"k≤{results['extremal']['max_k']} "
          f"t={results['extremal']['runtime_s']:.3f}s")
    print(f"TOTAL {results['total_runtime_s']:.3f}s")
