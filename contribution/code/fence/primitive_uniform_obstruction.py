"""Bounded exact analyzer for primitive uniform binary substitutions.

A candidate Collatz parity transcript may be proposed as the fixed point of a
binary k-uniform morphism (substitution).  This module validates such
morphisms, decides primitivity of the 2x2 incidence matrix by a finite matrix
power, computes the exact stationary one-frequency as a rational, and reports
finite-prefix factor and density statistics.

Scope is finite evidence only.  It does not prove or refute Collatz, does not
classify arbitrary automatic sequences, and never uses floating-point logs for
acceptance decisions.  Because alpha = log_3(2) is irrational, supercritical
comparisons accept rational bounds alpha_lo < alpha < alpha_hi and return
interval-safe classifications.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


Bit = int
Symbol = int  # 0 or 1


class SubstitutionError(ValueError):
    """Invalid morphism, seed, or analysis request."""

    def __init__(
        self,
        message: str,
        *,
        component: str = "primitive_uniform_obstruction",
        root_cause: str | None = None,
        failure_type: str = "input_error",
    ) -> None:
        super().__init__(message)
        self.component = component
        self.root_cause = root_cause if root_cause is not None else message
        self.failure_type = failure_type

    def as_structured(self) -> dict[str, str]:
        return {
            "component": self.component,
            "rootCause": self.root_cause,
            "failureType": self.failure_type,
        }


# ---------------------------------------------------------------------------
# Validation and incidence
# ---------------------------------------------------------------------------


def _as_bit_tuple(image: Sequence[int], *, label: str) -> tuple[Bit, ...]:
    if not image:
        raise SubstitutionError(
            f"{label} image must be nonempty",
            root_cause=f"empty image for {label}",
            failure_type="validation_error",
        )
    out: list[Bit] = []
    for index, symbol in enumerate(image):
        if symbol not in (0, 1):
            raise SubstitutionError(
                f"{label} image bit at index {index} must be 0 or 1, got {symbol!r}",
                root_cause=f"nonbinary image for {label}",
                failure_type="validation_error",
            )
        out.append(int(symbol))
    return tuple(out)


def validate_uniform_binary_morphism(
    rules: Mapping[int, Sequence[int]],
    *,
    seed: Symbol = 0,
) -> tuple[dict[Symbol, tuple[Bit, ...]], int, Symbol]:
    """Validate a binary k-uniform morphism and a fixed-point seed.

    Requires:
      - rules for symbols 0 and 1 only (extra keys rejected);
      - nonempty binary images of equal length k >= 2;
      - seed in {0, 1} whose image begins with itself.
    """
    if set(rules.keys()) != {0, 1}:
        raise SubstitutionError(
            "rules must map exactly the symbols {0, 1}",
            root_cause=f"rule keys={sorted(rules.keys())!r}",
            failure_type="validation_error",
        )
    image0 = _as_bit_tuple(rules[0], label="0")
    image1 = _as_bit_tuple(rules[1], label="1")
    if len(image0) != len(image1):
        raise SubstitutionError(
            "images must have equal length (uniform morphism)",
            root_cause=f"len(0)={len(image0)} len(1)={len(image1)}",
            failure_type="validation_error",
        )
    k = len(image0)
    if k < 2:
        raise SubstitutionError(
            "uniform length k must be at least 2",
            root_cause=f"k={k}",
            failure_type="validation_error",
        )
    if seed not in (0, 1):
        raise SubstitutionError(
            f"seed must be 0 or 1, got {seed!r}",
            root_cause="invalid seed",
            failure_type="validation_error",
        )
    images = {0: image0, 1: image1}
    if images[seed][0] != seed:
        raise SubstitutionError(
            "seed image must begin with the seed (fixed-point generation)",
            root_cause=f"image({seed})={images[seed]!r} does not start with {seed}",
            failure_type="validation_error",
        )
    return images, k, seed


def incidence_matrix(rules: Mapping[int, Sequence[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the 2x2 incidence matrix with columns as source symbols.

    M[i][j] = number of times output symbol i appears in the image of j.
    Rows and columns are ordered (0, 1).  Seed is not required for incidence;
    only the two images are validated (nonempty, binary, equal length k >= 2).
    """
    if set(rules.keys()) != {0, 1}:
        raise SubstitutionError(
            "rules must map exactly the symbols {0, 1}",
            root_cause=f"rule keys={sorted(rules.keys())!r}",
            failure_type="validation_error",
        )
    image0 = _as_bit_tuple(rules[0], label="0")
    image1 = _as_bit_tuple(rules[1], label="1")
    if len(image0) != len(image1):
        raise SubstitutionError(
            "images must have equal length (uniform morphism)",
            root_cause=f"len(0)={len(image0)} len(1)={len(image1)}",
            failure_type="validation_error",
        )
    if len(image0) < 2:
        raise SubstitutionError(
            "uniform length k must be at least 2",
            root_cause=f"k={len(image0)}",
            failure_type="validation_error",
        )
    return (
        (image0.count(0), image1.count(0)),
        (image0.count(1), image1.count(1)),
    )


def _incidence_from_images(
    images: Mapping[Symbol, tuple[Bit, ...]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    image0, image1 = images[0], images[1]
    return (
        (image0.count(0), image1.count(0)),
        (image0.count(1), image1.count(1)),
    )


def _mat_mul(
    a: tuple[tuple[int, int], tuple[int, int]],
    b: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def _mat_positive(m: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    return m[0][0] > 0 and m[0][1] > 0 and m[1][0] > 0 and m[1][1] > 0


def is_primitive(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> bool:
    """Decide primitivity of a 2x2 nonnegative integer matrix exactly.

    A nonnegative matrix is primitive iff some power is entrywise positive.
    For n=2 the Wielandt bound is n^2 - 2n + 2 = 2, so M is primitive iff
    M^2 is entrywise positive (which also covers the case M > 0, since then
    M^2 > 0 for nonnegative M with positive diagonal block structure; more
    directly we check M and M^2).

    Algorithm (exact, 2x2 only):
      1. Reject if any entry is negative.
      2. Compute M^1 and M^2 by integer arithmetic.
      3. Return True iff at least one of M, M^2 is entrywise strictly positive.

    This is necessary and sufficient: if some power is positive then a power
    at most the Wielandt index is positive; if neither M nor M^2 is positive
    then no higher power becomes positive for 2x2 nonnegative matrices under
    the Wielandt bound.
    """
    for row in matrix:
        for entry in row:
            if not isinstance(entry, int) or entry < 0:
                raise SubstitutionError(
                    "incidence matrix entries must be nonnegative integers",
                    root_cause=f"bad entry {entry!r}",
                    failure_type="validation_error",
                )
    if _mat_positive(matrix):
        return True
    return _mat_positive(_mat_mul(matrix, matrix))


# ---------------------------------------------------------------------------
# Frequencies and fixed points
# ---------------------------------------------------------------------------


def one_frequency(
    rules: Mapping[int, Sequence[int]],
    *,
    seed: Symbol = 0,
) -> Fraction:
    """Exact stationary frequency of symbol 1 as a Fraction.

    Solves M v = k v with v0 + v1 = 1 for the right Perron eigenvector of a
    primitive uniform incidence matrix (Perron eigenvalue equals the uniform
    length k).  Rejects non-primitive and degenerate inputs explicitly.
    """
    images, k, _seed = validate_uniform_binary_morphism(rules, seed=seed)
    matrix = _incidence_from_images(images)
    if not is_primitive(matrix):
        raise SubstitutionError(
            "morphism incidence matrix is not primitive",
            root_cause=f"matrix={matrix}",
            failure_type="non_primitive",
        )
    # m10 * v0 + m11 * v1 = k * v1  and  v0 + v1 = 1
    # => m10 * (1 - v1) = (k - m11) * v1 = m01 * v1
    # => v1 = m10 / (m10 + m01) when denominator > 0
    m01 = matrix[0][1]
    m10 = matrix[1][0]
    denom = m10 + m01
    if denom == 0:
        # Both off-diagonal blocks for the 0↔1 exchange vanish.
        # Then either all-zero or all-one images; not a useful mixed frequency.
        raise SubstitutionError(
            "degenerate incidence matrix: cannot form a unique mixed one-frequency",
            root_cause=f"m01={m01} m10={m10} matrix={matrix}",
            failure_type="degenerate_frequency",
        )
    freq = Fraction(m10, denom)
    # Sanity: also check first row / column-sum consistency with eigenvalue k.
    v0 = 1 - freq
    left = matrix[0][0] * v0 + matrix[0][1] * freq
    if left != k * v0:
        raise SubstitutionError(
            "eigenvector equation M v = k v failed (internal consistency)",
            root_cause=f"left={left} expected={k * v0}",
            failure_type="degenerate_frequency",
        )
    return freq


def fixed_point_prefix(
    rules: Mapping[int, Sequence[int]],
    length: int,
    *,
    seed: Symbol = 0,
) -> tuple[Bit, ...]:
    """Generate a length-bounded prefix of the pure morphic fixed point.

    Expands symbol-by-symbol and stops as soon as ``length`` symbols are
    available, so the last expansion overshoots by at most k-1 symbols rather
    than materializing a full k^t block when only a short prefix is needed.
    """
    if length < 0:
        raise SubstitutionError(
            f"length must be nonnegative, got {length}",
            failure_type="validation_error",
        )
    if length == 0:
        return ()
    images, _k, seed = validate_uniform_binary_morphism(rules, seed=seed)
    word: list[Bit] = [seed]
    while len(word) < length:
        expanded: list[Bit] = []
        for symbol in word:
            expanded.extend(images[symbol])
            if len(expanded) >= length:
                return tuple(expanded[:length])
        word = expanded
    return tuple(word[:length])


# ---------------------------------------------------------------------------
# Factors and interval-safe density
# ---------------------------------------------------------------------------


def factor_set(word: Sequence[Bit], factor_length: int) -> set[tuple[Bit, ...]]:
    """Return the set of distinct factors of the given length in ``word``."""
    if factor_length < 0:
        raise SubstitutionError(
            f"factor_length must be nonnegative, got {factor_length}",
            failure_type="validation_error",
        )
    if factor_length == 0:
        return {()}
    if factor_length > len(word):
        return set()
    return {
        tuple(word[i : i + factor_length])
        for i in range(len(word) - factor_length + 1)
    }


def factor_count(word: Sequence[Bit], factor_length: int) -> int:
    """Exact number of distinct factors of ``factor_length`` in ``word``."""
    return len(factor_set(word, factor_length))


def classify_density_vs_alpha(
    ones: int,
    length: int,
    alpha_lo: Fraction,
    alpha_hi: Fraction,
) -> str:
    """Interval-safe classification of ones/length against alpha = log_3(2).

    Requires alpha_lo < alpha_hi as exact rationals with
    alpha_lo < log_3(2) < alpha_hi supplied by the caller (not verified here
    against the transcendental; the caller owns the bound certificate).

    Returns:
      - "supercritical" if ones/length >= alpha_hi  (hence > alpha)
      - "subcritical"   if ones/length <= alpha_lo  (hence < alpha)
      - "inconclusive"  otherwise
    """
    if length <= 0:
        raise SubstitutionError(
            f"length must be positive for density, got {length}",
            failure_type="validation_error",
        )
    if ones < 0 or ones > length:
        raise SubstitutionError(
            f"ones must satisfy 0 <= ones <= length, got ones={ones} length={length}",
            failure_type="validation_error",
        )
    if not isinstance(alpha_lo, Fraction) or not isinstance(alpha_hi, Fraction):
        raise SubstitutionError(
            "alpha_lo and alpha_hi must be fractions.Fraction",
            failure_type="validation_error",
        )
    if alpha_lo >= alpha_hi:
        raise SubstitutionError(
            "require alpha_lo < alpha_hi",
            root_cause=f"alpha_lo={alpha_lo} alpha_hi={alpha_hi}",
            failure_type="validation_error",
        )
    density = Fraction(ones, length)
    if density >= alpha_hi:
        return "supercritical"
    if density <= alpha_lo:
        return "subcritical"
    return "inconclusive"


def max_supercritical_discrepancy(
    word: Sequence[Bit],
    window_length: int,
    alpha_lo: Fraction,
    alpha_hi: Fraction,
) -> dict[str, object]:
    """Scan windows of fixed length; report interval-safe supercritical stats.

    Discrepancy lower bound for a window with s ones is
        s - alpha_hi * window_length
    (a positive value certifies supercritical excess over alpha).  The maximum
    of these lower bounds among windows classified supercritical is returned
    as an exact Fraction.  No float logs are used.
    """
    if window_length < 1:
        raise SubstitutionError(
            f"window_length must be positive, got {window_length}",
            failure_type="validation_error",
        )
    if len(word) < window_length:
        return {
            "window_length": window_length,
            "windows_scanned": 0,
            "max_ones": None,
            "max_safe_discrepancy_lo": None,
            "any_supercritical": False,
            "any_subcritical": False,
            "any_inconclusive": False,
            "classifications_seen": [],
        }

    max_ones = 0
    max_disc_lo: Fraction | None = None
    seen: set[str] = set()
    n = window_length
    # rolling ones count
    ones = sum(1 for b in word[:n] if b)
    for start in range(0, len(word) - n + 1):
        if start > 0:
            ones += int(word[start + n - 1]) - int(word[start - 1])
        if ones > max_ones:
            max_ones = ones
        label = classify_density_vs_alpha(ones, n, alpha_lo, alpha_hi)
        seen.add(label)
        if label == "supercritical":
            disc_lo = Fraction(ones, 1) - alpha_hi * n
            if max_disc_lo is None or disc_lo > max_disc_lo:
                max_disc_lo = disc_lo

    return {
        "window_length": n,
        "windows_scanned": len(word) - n + 1,
        "max_ones": max_ones,
        "max_safe_discrepancy_lo": max_disc_lo,
        "any_supercritical": "supercritical" in seen,
        "any_subcritical": "subcritical" in seen,
        "any_inconclusive": "inconclusive" in seen,
        "classifications_seen": sorted(seen),
    }


# ---------------------------------------------------------------------------
# Named controls and report
# ---------------------------------------------------------------------------

# Classical binary uniform morphisms used as non-periodic transcript probes.
THUE_MORSE_RULES: dict[int, tuple[Bit, ...]] = {0: (0, 1), 1: (1, 0)}
PERIOD_DOUBLING_RULES: dict[int, tuple[Bit, ...]] = {0: (0, 1), 1: (0, 0)}

# Rational bounds with alpha_lo < log_3(2) < alpha_hi.
# The inequalities are certified below using exact integer exponentiation.
DEFAULT_ALPHA_LO = Fraction(63, 100)
DEFAULT_ALPHA_HI = Fraction(631, 1000)


def default_alpha_bound_certificate() -> dict[str, object]:
    """Return exact certificates for the bundled bounds on log_3(2).

    Since exponentiation by positive integers and log base 3 are increasing,
    ``3^63 < 2^100`` is equivalent to ``63/100 < log_3(2)``, while
    ``2^1000 < 3^631`` is equivalent to ``log_3(2) < 631/1000``.
    """
    lower_verified = 3**63 < 2**100
    upper_verified = 2**1000 < 3**631
    return {
        "alpha_lo": str(DEFAULT_ALPHA_LO),
        "alpha_hi": str(DEFAULT_ALPHA_HI),
        "lower_inequality": "3^63 < 2^100",
        "upper_inequality": "2^1000 < 3^631",
        "lower_verified": lower_verified,
        "upper_verified": upper_verified,
        "verified": lower_verified and upper_verified,
        "arithmetic": "exact_integer",
    }

FINITE_EVIDENCE_SEMANTICS = (
    "All statistics are computed from finite validated prefixes and exact "
    "2x2 matrix algebra.  Primitivity and one-frequency are exact for the "
    "morphism.  Factor counts and density classifications are finite-prefix "
    "evidence only and never prove non-integrality, divergence, or a Collatz "
    "resolution.  Supercritical labels use rational bounds alpha_lo < alpha "
    "< alpha_hi; the bundled defaults have exact integer certificates and "
    "custom bounds remain caller-owned.  No float log_3(2) is evaluated."
)


def analyze_morphism(
    name: str,
    rules: Mapping[int, Sequence[int]],
    *,
    seed: Symbol = 0,
    prefix_length: int = 256,
    factor_lengths: Sequence[int] = (1, 2, 3, 4, 8),
    window_length: int = 16,
    alpha_lo: Fraction = DEFAULT_ALPHA_LO,
    alpha_hi: Fraction = DEFAULT_ALPHA_HI,
) -> dict[str, object]:
    """Full finite analysis of one uniform binary morphism."""
    images, k, seed = validate_uniform_binary_morphism(rules, seed=seed)
    matrix = _incidence_from_images(images)
    primitive = is_primitive(matrix)
    result: dict[str, object] = {
        "name": name,
        "rules": {str(sym): list(images[sym]) for sym in (0, 1)},
        "seed": seed,
        "uniform_length": k,
        "incidence_matrix": [list(matrix[0]), list(matrix[1])],
        "primitive": primitive,
        "evidence_scope": "finite_only",
    }
    if not primitive:
        result["one_frequency"] = None
        result["error"] = {
            "component": "primitive_uniform_obstruction",
            "rootCause": "non-primitive incidence matrix",
            "failureType": "non_primitive",
        }
        return result

    freq = one_frequency(rules, seed=seed)
    prefix = fixed_point_prefix(rules, prefix_length, seed=seed)
    factors = {
        str(n): factor_count(prefix, n)
        for n in factor_lengths
        if n >= 0
    }
    discrepancy = max_supercritical_discrepancy(
        prefix, window_length, alpha_lo, alpha_hi
    )
    # JSON-friendly discrepancy
    disc_payload = dict(discrepancy)
    if disc_payload["max_safe_discrepancy_lo"] is not None:
        disc_payload["max_safe_discrepancy_lo"] = str(
            disc_payload["max_safe_discrepancy_lo"]
        )

    result.update(
        {
            "one_frequency": str(freq),
            "one_frequency_numerator": freq.numerator,
            "one_frequency_denominator": freq.denominator,
            "prefix_length": len(prefix),
            "prefix": "".join(str(b) for b in prefix),
            "prefix_ones": sum(prefix),
            "factor_counts": factors,
            "discrepancy": disc_payload,
            "alpha_lo": str(alpha_lo),
            "alpha_hi": str(alpha_hi),
        }
    )
    return result


def build_report(
    *,
    prefix_length: int = 256,
    factor_lengths: Sequence[int] = (1, 2, 3, 4, 8),
    window_length: int = 16,
    alpha_lo: Fraction = DEFAULT_ALPHA_LO,
    alpha_hi: Fraction = DEFAULT_ALPHA_HI,
) -> dict[str, object]:
    """Deterministic report for the named controls (Thue-Morse, period-doubling)."""
    controls = [
        ("thue_morse", THUE_MORSE_RULES, 0),
        ("period_doubling", PERIOD_DOUBLING_RULES, 0),
    ]
    analyses = [
        analyze_morphism(
            name,
            rules,
            seed=seed,
            prefix_length=prefix_length,
            factor_lengths=factor_lengths,
            window_length=window_length,
            alpha_lo=alpha_lo,
            alpha_hi=alpha_hi,
        )
        for name, rules, seed in controls
    ]

    expected_freq = {
        "thue_morse": Fraction(1, 2),
        "period_doubling": Fraction(1, 3),
    }
    check_failures: list[str] = []
    alpha_certificate = default_alpha_bound_certificate()
    using_default_alpha_bounds = (
        alpha_lo == DEFAULT_ALPHA_LO and alpha_hi == DEFAULT_ALPHA_HI
    )
    if using_default_alpha_bounds and not alpha_certificate["verified"]:
        check_failures.append("default_alpha_bound_certificate")
    for row in analyses:
        name = str(row["name"])
        if not row.get("primitive"):
            check_failures.append(f"{name}:not_primitive")
            continue
        freq = Fraction(str(row["one_frequency"]))
        if freq != expected_freq[name]:
            check_failures.append(f"{name}:frequency")
        # known short prefixes
        got = str(row["prefix"])
        if name == "thue_morse" and not got.startswith("01101001"):
            check_failures.append(f"{name}:prefix")
        if name == "period_doubling" and not got.startswith("01000101"):
            check_failures.append(f"{name}:prefix")

    return {
        "schema_version": 1,
        "object": "primitive_uniform_binary_substitution_obstruction",
        "claim_scope": {
            "exact": (
                "2x2 incidence primitivity by Wielandt index 2; "
                "stationary one-frequency as Fraction for primitive morphisms"
            ),
            "finite_evidence_only": FINITE_EVIDENCE_SEMANTICS,
            "not_claimed": (
                "Collatz proof or refutation; classification of arbitrary "
                "automatic sequences; infinite-word factor complexity; "
                "float-based log_3(2) decisions"
            ),
        },
        "primitivity_algorithm": {
            "matrix_size": 2,
            "wielandt_bound": 2,
            "rule": "primitive iff M or M^2 is entrywise strictly positive",
            "arithmetic": "exact nonnegative integer matrix powers",
        },
        "params": {
            "prefix_length": prefix_length,
            "factor_lengths": list(factor_lengths),
            "window_length": window_length,
            "alpha_lo": str(alpha_lo),
            "alpha_hi": str(alpha_hi),
        },
        "alpha_bound_certificate": {
            **alpha_certificate,
            "applies_to_params": using_default_alpha_bounds,
        },
        "analyses": analyses,
        "check_failures": check_failures,
        "all_checks_passed": not check_failures,
        "evidence_scope": "finite_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix-length", type=int, default=256)
    parser.add_argument("--window-length", type=int, default=16)
    parser.add_argument(
        "--alpha-lo",
        type=str,
        default=str(DEFAULT_ALPHA_LO),
        help="rational lower bound for log_3(2), e.g. 63/100",
    )
    parser.add_argument(
        "--alpha-hi",
        type=str,
        default=str(DEFAULT_ALPHA_HI),
        help="rational upper bound for log_3(2), e.g. 631/1000",
    )
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()
    try:
        alpha_lo = Fraction(args.alpha_lo)
        alpha_hi = Fraction(args.alpha_hi)
        report = build_report(
            prefix_length=args.prefix_length,
            window_length=args.window_length,
            alpha_lo=alpha_lo,
            alpha_hi=alpha_hi,
        )
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(rendered)
        print(rendered, end="")
        return 0 if report["all_checks_passed"] else 1
    except SubstitutionError as exc:
        print(json.dumps({"error": exc.as_structured()}, sort_keys=True))
        return 2
    except Exception as exc:  # noqa: BLE001 — CLI boundary
        failure = {
            "component": "primitive_uniform_obstruction",
            "rootCause": str(exc),
            "failureType": type(exc).__name__,
        }
        print(json.dumps({"error": failure}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
