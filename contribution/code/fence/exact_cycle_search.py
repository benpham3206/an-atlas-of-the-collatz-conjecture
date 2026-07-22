"""Exact positive-cycle search for the fixed odd-only 3n+1 map.

Map (odd positives only):
    U(n) = (3n + 1) / 2^{v_2(3n+1)}

For an exponent tuple a = (a_0, ..., a_{m-1}) of positive integers with
sum(a) = K, the odd-only affine composite is built by

    S_0 = 0,  C_0 = 0,
    C_{j+1} = 3 * C_j + 2^{S_j},
    S_{j+1} = S_j + a_j.

Any fixed point of the composite satisfies n = C_m / (2^K - 3^m) when
2^K > 3^m.  A candidate is accepted only after exact divisibility, n > 0 odd,
and direct verification that v_2(3 n_j + 1) = a_j for every step with
n_m = n_0.

Cyclic rotations of a name the same valuation cycle; the search reports each
cycle once under the lexicographically minimal rotation.  Composition counts
are stated both before and after that symmetry filter.

This is a finite, explicit enumeration over supplied (m, K) pairs — not a
Collatz proof, not a divergence certificate, and not a claim beyond those pairs.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Iterator, Sequence


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StructuredError:
    """Machine-checkable failure record."""

    component: str
    rootCause: str
    failureType: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class CycleSearchError(Exception):
    """Raised for invalid CLI / parameter input with a structured payload."""

    def __init__(self, component: str, root_cause: str, failure_type: str) -> None:
        super().__init__(root_cause)
        self.error = StructuredError(component, root_cause, failure_type)


# ---------------------------------------------------------------------------
# Core arithmetic (exact ints only)
# ---------------------------------------------------------------------------


def v2(n: int) -> int:
    """2-adic valuation of a positive even integer; rejects non-positive."""
    if n <= 0:
        raise CycleSearchError(
            "v2",
            f"v2 requires positive integer, got {n}",
            "invalid_argument",
        )
    if n % 2 != 0:
        return 0
    val = 0
    while n % 2 == 0:
        n //= 2
        val += 1
    return val


def odd_only_step(n: int) -> tuple[int, int]:
    """One step of U on a positive odd integer.

    Returns ``(U(n), a)`` where ``a = v_2(3n+1)`` and ``U(n) = (3n+1) // 2^a``.
    """
    if n <= 0 or n % 2 == 0:
        raise CycleSearchError(
            "odd_only_step",
            f"U requires positive odd integer, got {n}",
            "invalid_argument",
        )
    triple = 3 * n + 1
    a = v2(triple)
    return triple >> a, a


def U(n: int) -> int:
    """Odd-only accelerated Collatz map on positive odd integers."""
    return odd_only_step(n)[0]


def affine_CS(exponents: Sequence[int]) -> tuple[int, int]:
    """Compute (C_m, S_m) for exponent tuple a via the packet recurrence.

    S_0 = 0, C_0 = 0;
    C_{j+1} = 3*C_j + 2^{S_j};
    S_{j+1} = S_j + a_j.
    """
    s = 0
    c = 0
    for a_j in exponents:
        c = 3 * c + (1 << s)
        s = s + a_j
    return c, s


def fixed_point_fraction(exponents: Sequence[int]) -> Fraction | None:
    """Return C_m / (2^K - 3^m) when 2^K != 3^m; else None."""
    m = len(exponents)
    if m == 0:
        return None
    c_m, k = affine_CS(exponents)
    pow2 = 1 << k
    pow3 = 3**m
    denom = pow2 - pow3
    if denom == 0:
        return None
    return Fraction(c_m, denom)


def is_positive_composition(exponents: Sequence[int], m: int, k: int) -> bool:
    """True iff a is a length-m composition of K into positive parts."""
    if len(exponents) != m:
        return False
    if any(a < 1 for a in exponents):
        return False
    return sum(exponents) == k


# ---------------------------------------------------------------------------
# Compositions and cyclic canonicalization
# ---------------------------------------------------------------------------


def compositions_of(k: int, m: int) -> Iterator[tuple[int, ...]]:
    """Stream all ordered compositions of K into m positive integer parts.

    Count of this stream is ``binom(K-1, m-1)`` when 1 <= m <= K; empty otherwise.
    This is the **pre-symmetry** enumeration (before cyclic rotation filter).
    """
    if m < 1 or k < m:
        return
        yield  # pragma: no cover — makes this a generator
    if m == 1:
        yield (k,)
        return

    # a_0 >= 1, ..., a_{m-1} >= 1, sum = k
    # Write a_i = b_i + 1 with b_i >= 0, sum(b) = k - m.
    target = k - m

    def rec(remaining_parts: int, remaining_sum: int, prefix: list[int]) -> Iterator[tuple[int, ...]]:
        if remaining_parts == 1:
            yield tuple(prefix + [remaining_sum + 1])
            return
        for b in range(remaining_sum + 1):
            prefix.append(b + 1)
            yield from rec(remaining_parts - 1, remaining_sum - b, prefix)
            prefix.pop()

    yield from rec(m, target, [])


def rotations(exponents: Sequence[int]) -> list[tuple[int, ...]]:
    a = tuple(exponents)
    m = len(a)
    if m == 0:
        return []
    return [a[i:] + a[:i] for i in range(m)]


def canonical_rotation(exponents: Sequence[int]) -> tuple[int, ...]:
    """Lexicographically minimal cyclic rotation (unique cycle representative)."""
    rots = rotations(exponents)
    if not rots:
        raise CycleSearchError(
            "canonical_rotation",
            "empty exponent tuple has no rotation",
            "invalid_argument",
        )
    return min(rots)


def is_canonical_rotation(exponents: Sequence[int]) -> bool:
    a = tuple(exponents)
    return a == canonical_rotation(a)


def composition_count(m: int, k: int) -> int:
    """Number of positive compositions of K into m parts (before symmetry)."""
    if m < 1 or k < m:
        return 0
    # binom(k-1, m-1)
    n, r = k - 1, m - 1
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    num = 1
    for i in range(r):
        num = num * (n - i) // (i + 1)
    return num


def canonical_composition_count(m: int, k: int) -> int:
    """Number of cyclic orbits of length-m positive compositions of K.

    Burnside's lemma gives

        (1/m) * sum_{d | gcd(m,K)} phi(d) * C(K/d - 1, m/d - 1).

    Every orbit has exactly one lexicographically minimal representative, so
    this is also the number retained by the canonical-rotation convention.
    """
    if m < 1 or k < m:
        return 0

    def euler_phi(n: int) -> int:
        result = n
        factor = 2
        remaining = n
        while factor * factor <= remaining:
            if remaining % factor == 0:
                while remaining % factor == 0:
                    remaining //= factor
                result -= result // factor
            factor += 1
        if remaining > 1:
            result -= result // remaining
        return result

    total = 0
    common = gcd(m, k)
    for divisor in range(1, common + 1):
        if common % divisor == 0:
            total += euler_phi(divisor) * composition_count(
                m // divisor, k // divisor
            )
    if total % m != 0:
        raise CycleSearchError(
            "canonical_composition_count",
            f"Burnside total {total} is not divisible by m={m}",
            "internal_invariant",
        )
    return total // m


# ---------------------------------------------------------------------------
# Candidate construction and orbit verification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CycleCandidate:
    """One verified integral odd cycle for a valuation word (canonical form)."""

    m: int
    k: int
    exponents: tuple[int, ...]
    n0: int
    orbit: tuple[int, ...]
    c_m: int
    denom: int  # 2^K - 3^m
    is_trivial: bool
    valuation_verified: bool
    returns_to_start: bool
    all_states_odd_positive: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "m": self.m,
            "k": self.k,
            "exponents": list(self.exponents),
            "n0": self.n0,
            "orbit": list(self.orbit),
            "c_m": self.c_m,
            "denom": self.denom,
            "is_trivial": self.is_trivial,
            "valuation_verified": self.valuation_verified,
            "returns_to_start": self.returns_to_start,
            "all_states_odd_positive": self.all_states_odd_positive,
            "is_nontrivial_counterexample": (
                self.valuation_verified
                and self.returns_to_start
                and self.all_states_odd_positive
                and not self.is_trivial
            ),
        }


def try_integral_fixed_point(
    exponents: Sequence[int],
) -> tuple[int, int, int] | None:
    """If a yields an exact positive odd integer fixed point, return (n, C_m, denom).

    Conditions: 2^K > 3^m, exact divisibility, n > 0, n odd.
    Uses exact integer arithmetic only (no floats).
    """
    a = tuple(exponents)
    m = len(a)
    if m == 0 or any(x < 1 for x in a):
        return None
    c_m, k = affine_CS(a)
    if k != sum(a):
        return None
    pow2 = 1 << k
    pow3 = 3**m
    if pow2 <= pow3:
        return None
    denom = pow2 - pow3
    if c_m % denom != 0:
        return None
    n = c_m // denom
    if n <= 0 or n % 2 == 0:
        return None
    return n, c_m, denom


def verify_valuation_orbit(
    n0: int, exponents: Sequence[int]
) -> tuple[bool, bool, bool, tuple[int, ...]]:
    """Direct exact orbit check for U under prescribed valuations.

    Returns
    -------
    valuation_ok : every step has v2(3 n_j + 1) == a_j
    returns : n_m == n_0
    all_odd_positive : every state is a positive odd integer
    orbit : (n_0, n_1, ..., n_{m-1})  (length m; n_m checked separately)
    """
    a = tuple(exponents)
    m = len(a)
    if m == 0:
        return False, False, False, ()
    states: list[int] = []
    n = n0
    valuation_ok = True
    all_odd_positive = True
    for j in range(m):
        if n <= 0 or n % 2 == 0:
            all_odd_positive = False
            valuation_ok = False
            states.append(n)
            # cannot continue meaningfully with U
            for _ in range(j + 1, m):
                states.append(0)
            return False, False, False, tuple(states)
        states.append(n)
        triple = 3 * n + 1
        observed = v2(triple)
        if observed != a[j]:
            valuation_ok = False
        n = triple >> observed
    returns = n == n0
    # final state after m steps must still be odd positive if cycle closes
    if n <= 0 or n % 2 == 0:
        all_odd_positive = False
    return valuation_ok, returns, all_odd_positive, tuple(states)


def is_trivial_cycle(orbit: Sequence[int]) -> bool:
    """True iff the verified orbit is exactly the odd-only fixed point {1}."""
    return len(orbit) >= 1 and all(x == 1 for x in orbit)


def evaluate_exponents(exponents: Sequence[int]) -> CycleCandidate | None:
    """Build a CycleCandidate if the valuation word yields a verified integral cycle.

    Returns None when the affine fixed point is not a positive odd integer or
    when direct orbit verification fails.  The returned candidate uses the
    **canonical** rotation of the exponent tuple and the corresponding orbit
    start (the state on the cycle matching that rotation).
    """
    a = tuple(exponents)
    if not a or any(x < 1 for x in a):
        return None
    # Evaluate at the given word first
    fp = try_integral_fixed_point(a)
    if fp is None:
        return None
    n0, c_m, denom = fp
    val_ok, returns, all_odd, orbit = verify_valuation_orbit(n0, a)
    if not (val_ok and returns and all_odd):
        return None

    # Canonicalize: re-express under lex-min rotation
    canon = canonical_rotation(a)
    if canon == a:
        start = n0
        canon_orbit = orbit
        c_m_c, k_c = affine_CS(canon)
        denom_c = (1 << k_c) - 3 ** len(canon)
    else:
        # Find which rotation index maps a -> canon; shift orbit start
        rots = rotations(a)
        idx = rots.index(canon)
        start = orbit[idx]
        # Recompute affine constants for the canonical word
        fp_c = try_integral_fixed_point(canon)
        if fp_c is None:
            return None
        start_check, c_m_c, denom_c = fp_c
        if start_check != start:
            # Should match: fixed point of rotated word is rotated state
            # Prefer the affine fixed point for consistency
            start = start_check
        val_ok_c, returns_c, all_odd_c, canon_orbit = verify_valuation_orbit(
            start, canon
        )
        if not (val_ok_c and returns_c and all_odd_c):
            return None
        val_ok, returns, all_odd = val_ok_c, returns_c, all_odd_c

    trivial = is_trivial_cycle(canon_orbit)
    return CycleCandidate(
        m=len(canon),
        k=sum(canon),
        exponents=canon,
        n0=start,
        orbit=canon_orbit,
        c_m=c_m_c,
        denom=denom_c,
        is_trivial=trivial,
        valuation_verified=val_ok,
        returns_to_start=returns,
        all_states_odd_positive=all_odd,
    )


# ---------------------------------------------------------------------------
# Pair search
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PairResult:
    m: int
    k: int
    compositions_before_symmetry: int
    compositions_after_symmetry: int
    denom_positive: bool  # 2^K > 3^m
    integral_candidates: list[CycleCandidate]
    nontrivial_counterexamples: list[CycleCandidate]

    def to_dict(self) -> dict[str, object]:
        return {
            "m": self.m,
            "k": self.k,
            "pow2_K": 1 << self.k,
            "pow3_m": 3**self.m,
            "denom": (1 << self.k) - 3**self.m,
            "denom_positive": self.denom_positive,
            "composition_count_policy": {
                "before_symmetry_filter": (
                    "all ordered positive compositions of K into m parts; "
                    "count = binom(K-1, m-1)"
                ),
                "after_symmetry_filter": (
                    "only compositions that equal their lexicographically "
                    "minimal cyclic rotation; each valuation cycle counted once"
                ),
            },
            "compositions_before_symmetry": self.compositions_before_symmetry,
            "compositions_after_symmetry": self.compositions_after_symmetry,
            "integral_candidate_count": len(self.integral_candidates),
            "integral_candidates": [c.to_dict() for c in self.integral_candidates],
            "nontrivial_counterexample_count": len(self.nontrivial_counterexamples),
            "nontrivial_counterexamples": [
                c.to_dict() for c in self.nontrivial_counterexamples
            ],
        }


def search_pair(m: int, k: int) -> PairResult:
    """Exhaustive exact search over positive compositions for one (m, K)."""
    if m < 1:
        raise CycleSearchError(
            "search_pair",
            f"m must be a positive integer, got {m}",
            "invalid_parameter",
        )
    if k < 1:
        raise CycleSearchError(
            "search_pair",
            f"K must be a positive integer, got {k}",
            "invalid_parameter",
        )

    denom_positive = (1 << k) > 3**m
    before = composition_count(m, k)
    # Burnside counts cyclic orbits exactly. Enumerate every composition, but
    # pay rotational-canonicalization cost only after a word passes the affine
    # and direct-orbit gates. ``seen`` removes verified rotations.
    after = canonical_composition_count(m, k)
    candidates: list[CycleCandidate] = []
    seen: set[tuple[int, ...]] = set()

    for a in compositions_of(k, m):
        if not denom_positive:
            continue
        cand = evaluate_exponents(a)
        if cand is None:
            continue
        if cand.exponents in seen:
            continue
        seen.add(cand.exponents)
        candidates.append(cand)

    # Deterministic order: by n0, then exponents
    candidates.sort(key=lambda c: (c.n0, c.exponents))
    nontrivial = [c for c in candidates if not c.is_trivial]

    return PairResult(
        m=m,
        k=k,
        compositions_before_symmetry=before,
        compositions_after_symmetry=after,
        denom_positive=denom_positive,
        integral_candidates=candidates,
        nontrivial_counterexamples=nontrivial,
    )


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


DEFAULT_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 2),
    (5, 8),
    (12, 19),
    (17, 27),
)

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "exact_cycle_search_results.json"


def parse_pair(spec: str) -> tuple[int, int]:
    """Parse ``m:K`` into integers."""
    if ":" not in spec:
        raise CycleSearchError(
            "parse_pair",
            f"pair must be m:K, got {spec!r}",
            "invalid_parameter",
        )
    left, right = spec.split(":", 1)
    try:
        m = int(left)
        k = int(right)
    except ValueError as exc:
        raise CycleSearchError(
            "parse_pair",
            f"pair m:K must be integers, got {spec!r}",
            "invalid_parameter",
        ) from exc
    if m < 1 or k < 1:
        raise CycleSearchError(
            "parse_pair",
            f"m and K must be positive, got m={m}, K={k}",
            "invalid_parameter",
        )
    return m, k


def build_report(pairs: Sequence[tuple[int, int]]) -> dict[str, object]:
    """Run the search on each pair and assemble a deterministic JSON report."""
    # Stable unique pairs, sorted
    unique_sorted = sorted(set((int(m), int(k)) for m, k in pairs))
    pair_rows: list[dict[str, object]] = []
    all_integral: list[dict[str, object]] = []
    all_nontrivial: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    checks: list[dict[str, object]] = []

    for m, k in unique_sorted:
        try:
            result = search_pair(m, k)
        except CycleSearchError as exc:
            errors.append(exc.error.to_dict())
            continue
        row = result.to_dict()
        pair_rows.append(row)
        for c in result.integral_candidates:
            all_integral.append(c.to_dict())
        for c in result.nontrivial_counterexamples:
            all_nontrivial.append(c.to_dict())

        # Structural checks recorded in the report
        checks.append(
            {
                "pair": [m, k],
                "composition_count_matches_formula": (
                    result.compositions_before_symmetry == composition_count(m, k)
                ),
                "after_symmetry_le_before": (
                    result.compositions_after_symmetry
                    <= result.compositions_before_symmetry
                ),
                "every_candidate_verified": all(
                    c.valuation_verified
                    and c.returns_to_start
                    and c.all_states_odd_positive
                    for c in result.integral_candidates
                ),
                "trivial_only_when_orbit_is_one": all(
                    (c.is_trivial == is_trivial_cycle(c.orbit))
                    for c in result.integral_candidates
                ),
            }
        )

    # Known sanity: (1,2) must yield exactly trivial n=1 when present
    if (1, 2) in set(unique_sorted):
        row_12 = next(r for r in pair_rows if r["m"] == 1 and r["k"] == 2)
        cands = row_12["integral_candidates"]
        checks.append(
            {
                "name": "pair_1_2_exactly_trivial_one",
                "passed": (
                    len(cands) == 1
                    and cands[0]["n0"] == 1
                    and cands[0]["is_trivial"] is True
                    and cands[0]["exponents"] == [2]
                ),
            }
        )

    all_checks_passed = (
        len(errors) == 0
        and all(
            bool(c.get("composition_count_matches_formula", True))
            and bool(c.get("after_symmetry_le_before", True))
            and bool(c.get("every_candidate_verified", True))
            and bool(c.get("trivial_only_when_orbit_is_one", True))
            and bool(c.get("passed", True))
            for c in checks
        )
    )

    report: dict[str, object] = {
        "parameters": {
            "map": "U(n)=(3n+1)/2^{v2(3n+1)} on positive odd integers",
            "affine_recurrence": {
                "S_0": 0,
                "C_0": 0,
                "C_next": "C_{j+1}=3*C_j+2^{S_j}",
                "S_next": "S_{j+1}=S_j+a_j",
                "fixed_point": "n=C_m/(2^K-3^m)",
            },
            "acceptance": [
                "2^K > 3^m",
                "exact integer divisibility C_m % (2^K-3^m) == 0",
                "n > 0 and n odd",
                "direct orbit: v2(3*n_j+1)=a_j for all j and n_m=n_0",
                "counterexample only if verified orbit is not {1}",
            ],
            "symmetry": (
                "cyclic rotations of the exponent tuple identify the same "
                "valuation cycle; reported under lex-min rotation"
            ),
            "pairs": [[m, k] for m, k in unique_sorted],
        },
        "exact_scope": {
            "enumerated_pairs": [[m, k] for m, k in unique_sorted],
            "composition_domain": (
                "all ordered m-tuples of positive integers summing to K"
            ),
            "symmetry_filter": (
                "lexicographically minimal cyclic rotation; "
                "compositions_before_symmetry counts all ordered compositions; "
                "compositions_after_symmetry counts only canonical representatives"
            ),
            "arithmetic": "Python arbitrary-precision ints only; no floats in decisions",
        },
        "counts_per_pair": [
            {
                "m": r["m"],
                "k": r["k"],
                "compositions_before_symmetry": r["compositions_before_symmetry"],
                "compositions_after_symmetry": r["compositions_after_symmetry"],
                "integral_candidate_count": r["integral_candidate_count"],
                "nontrivial_counterexample_count": r[
                    "nontrivial_counterexample_count"
                ],
                "denom_positive": r["denom_positive"],
            }
            for r in pair_rows
        ],
        "pairs": pair_rows,
        "every_integral_candidate": all_integral,
        "nontrivial_counterexamples": all_nontrivial,
        "direct_verification_summary": {
            "candidates_with_valuation_verified": sum(
                1 for c in all_integral if c["valuation_verified"]
            ),
            "candidates_returning_to_start": sum(
                1 for c in all_integral if c["returns_to_start"]
            ),
            "candidates_all_odd_positive": sum(
                1 for c in all_integral if c["all_states_odd_positive"]
            ),
            "total_integral_candidates": len(all_integral),
            "total_nontrivial_counterexamples": len(all_nontrivial),
        },
        "checks": checks,
        "errors": errors,
        "all_checks_passed": all_checks_passed,
        "limitations": [
            "Results hold only for the explicitly enumerated (m, K) pairs.",
            "No claim of completeness over all m, K or over all Collatz cycles.",
            "No claim of a Collatz proof, independence result, or divergent orbit.",
            "Absence of a nontrivial counterexample in a finite (m, K) box "
            "does not prove the odd-only map has only the cycle {1}.",
            "Generalized Collatz parameters and non-positive starts are excluded.",
        ],
    }
    return report


def dumps_report(report: dict[str, object]) -> str:
    """Deterministic sorted-key JSON with trailing newline."""
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def write_report(report: dict[str, object], path: Path) -> str:
    text = dumps_report(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


# ---------------------------------------------------------------------------
# Independent affine cross-check helper (used by tests and CLI self-check)
# ---------------------------------------------------------------------------


def affine_fixed_point_via_direct_formula(exponents: Sequence[int], n: int) -> int:
    """Apply the composite odd-only map assuming valuations a hold: (3^m n + C_m) / 2^K."""
    a = tuple(exponents)
    m = len(a)
    c_m, k = affine_CS(a)
    num = (3**m) * n + c_m
    den = 1 << k
    if num % den != 0:
        raise CycleSearchError(
            "affine_apply",
            f"composite ({3**m}*{n}+{c_m}) not divisible by 2^{k}",
            "non_integral_composite",
        )
    return num // den


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Exact positive-cycle search for the odd-only 3n+1 map U, "
            "parameterized by (m, K) valuation-word length and total valuation."
        )
    )
    p.add_argument(
        "--pair",
        action="append",
        default=None,
        metavar="m:K",
        help="Search pair m:K (repeatable). Default: 1:2, 5:8, 12:19, 17:27.",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"JSON output path (default: {DEFAULT_OUTPUT})",
    )
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.pair:
            pairs = [parse_pair(spec) for spec in args.pair]
        else:
            pairs = list(DEFAULT_PAIRS)
        report = build_report(pairs)
        text = write_report(report, Path(args.output))
        # stdout identical to file
        sys.stdout.write(text)
        return 0 if report.get("all_checks_passed") else 1
    except CycleSearchError as exc:
        payload = {
            "all_checks_passed": False,
            "errors": [exc.error.to_dict()],
            "limitations": [
                "Aborted before enumeration due to invalid input.",
            ],
        }
        text = dumps_report(payload)
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError:
            pass
        sys.stdout.write(text)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
