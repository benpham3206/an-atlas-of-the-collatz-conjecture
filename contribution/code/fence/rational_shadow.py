"""Exact periodic rational shadows for finite Collatz parity prefixes.

For a nonempty binary word w of length L, the Terras composite is

    T_w^L(x) = (3^s x + c_w) / 2^L.

Its unique fixed point is the odd-denominator rational

    x_w = c_w / (2^L - 3^s).

The program verifies, by independent rational iteration and modular evaluation
of the inverse Terras series, that x_w follows w and returns to itself.  Thus
periodic rational states can shadow every finite parity prefix.  This is a
finite exact verifier, not a Collatz proof or a positive-integer search result.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


Bit = int


class ShadowInputError(ValueError):
    """Raised when a requested shadow word is empty or nonbinary."""


def checked_word(bits: Iterable[Bit]) -> tuple[Bit, ...]:
    word = tuple(bits)
    if not word:
        raise ShadowInputError("word must contain at least one bit")
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise ShadowInputError(
                f"word bit at index {index} must be 0 or 1, got {bit!r}"
            )
    return word


def affine_composite(bits: Iterable[Bit]) -> tuple[int, int, int]:
    """Return ``(3^s, c_w, 2^L)`` for the supplied Terras word."""

    word = checked_word(bits)
    offset = 0
    ones = 0
    for index, bit in enumerate(word):
        if bit:
            offset = 3 * offset + (1 << index)
            ones += 1
    return 3**ones, offset, 1 << len(word)


def periodic_shadow(bits: Iterable[Bit]) -> Fraction:
    """Return the unique rational fixed point of the word composite."""

    pow3, offset, pow2 = affine_composite(bits)
    return Fraction(offset, pow2 - pow3)


def terras_step(value: Fraction) -> Fraction:
    """Apply the 2-adic Terras branch to an odd-denominator rational."""

    if value.denominator % 2 == 0:
        raise ShadowInputError(
            f"Terras rational must have odd denominator, got {value.denominator}"
        )
    if value.numerator % 2 == 0:
        return value / 2
    return (3 * value + 1) / 2


def rational_parity_prefix(value: Fraction, length: int) -> tuple[Bit, ...]:
    if length < 0:
        raise ShadowInputError(f"length must be nonnegative, got {length}")
    bits: list[Bit] = []
    state = value
    for _ in range(length):
        bits.append(state.numerator & 1)
        state = terras_step(state)
    return tuple(bits)


def iterate(value: Fraction, steps: int) -> Fraction:
    state = value
    for _ in range(steps):
        state = terras_step(state)
    return state


def phi_prefix_residue(bits: Iterable[Bit]) -> int:
    """Independently evaluate ``Phi(bits) mod 2^L`` from its defining series."""

    word = checked_word(bits)
    modulus = 1 << len(word)
    inv3 = pow(3, -1, modulus)
    inv3_power = inv3
    residue = 0
    for index, bit in enumerate(word):
        if bit:
            residue = (residue - (1 << index) * inv3_power) % modulus
            inv3_power = (inv3_power * inv3) % modulus
    return residue


def rational_residue(value: Fraction, length: int) -> int:
    modulus = 1 << length
    return (value.numerator * pow(value.denominator, -1, modulus)) % modulus


def two_adic_agreement(left: Fraction, right: Fraction) -> int | None:
    """Return v_2(left-right), or ``None`` when the values are equal."""

    difference = left - right
    if difference == 0:
        return None
    numerator = abs(difference.numerator)
    valuation = 0
    while numerator % 2 == 0:
        numerator //= 2
        valuation += 1
    return valuation


def fibonacci_prefix(length: int) -> tuple[Bit, ...]:
    """Return a prefix of the fixed point of the morphism 0->01, 1->0."""

    if length < 1:
        raise ShadowInputError(f"length must be positive, got {length}")
    word = "0"
    while len(word) < length:
        word = "".join("01" if symbol == "0" else "0" for symbol in word)
    return tuple(int(symbol) for symbol in word[:length])


def rational_height(value: Fraction) -> int:
    """Return the denominator-scaled height ``|numerator| + denominator``."""

    return abs(value.numerator) + value.denominator


def recurrent_height_certificates(
    bits: Iterable[Bit], *, max_block: int
) -> list[dict[str, object]]:
    """Check finite height lower bounds forced by recurrent blocks.

    For the periodic shadow of a finite prefix, equal length-K blocks at i<j
    followed by an observed mismatch imply distinct scaled states congruent
    modulo 2^K.  Hence the reduced shadow a/d satisfies

        |a| + d >= 2^(K-1) * (2/3)^j.

    The best (largest) witnessed lower bound is retained for each K.
    """

    word = checked_word(bits)
    if max_block < 1:
        raise ShadowInputError(f"max_block must be positive, got {max_block}")
    shadow = periodic_shadow(word)
    height = rational_height(shadow)
    rows: list[dict[str, object]] = []

    for block_length in range(1, min(max_block, len(word) - 1) + 1):
        positions: dict[tuple[Bit, ...], list[int]] = {}
        best: tuple[Fraction, int, int, int] | None = None
        for right in range(0, len(word) - block_length + 1):
            block = word[right : right + block_length]
            for left in positions.get(block, []):
                mismatch = next(
                    (
                        offset
                        for offset in range(block_length, len(word) - right)
                        if word[left + offset] != word[right + offset]
                    ),
                    None,
                )
                if mismatch is None:
                    continue
                lower_bound = Fraction(1 << (block_length - 1), 1) * Fraction(
                    2, 3
                ) ** right
                if best is None or lower_bound > best[0]:
                    best = (lower_bound, left, right, mismatch)
            positions.setdefault(block, []).append(right)

        if best is not None:
            lower_bound, left, right, mismatch = best
            rows.append(
                {
                    "block_length": block_length,
                    "left_position": left,
                    "right_position": right,
                    "mismatch_offset": mismatch,
                    "height": height,
                    "lower_bound": str(lower_bound),
                    "bound_holds": Fraction(height, 1) >= lower_bound,
                }
            )
    return rows


def verify_word(bits: Iterable[Bit]) -> dict[str, object]:
    word = checked_word(bits)
    pow3, offset, pow2 = affine_composite(word)
    shadow = periodic_shadow(word)
    direct_word = rational_parity_prefix(shadow, len(word))
    direct_return = iterate(shadow, len(word))
    series_residue = phi_prefix_residue(word)
    shadow_residue = rational_residue(shadow, len(word))
    denominator = pow2 - pow3
    return {
        "length": len(word),
        "word": "".join(str(bit) for bit in word),
        "ones": sum(word),
        "pow3": pow3,
        "pow2": pow2,
        "offset": offset,
        "fixed_point": str(shadow),
        "fixed_point_numerator": shadow.numerator,
        "fixed_point_denominator": shadow.denominator,
        "raw_cycle_denominator": denominator,
        "divisibility_remainder": offset % abs(denominator),
        "is_ordinary_integer": shadow.denominator == 1,
        "parity_matches": direct_word == word,
        "returns_after_period": direct_return == shadow,
        "series_residue": series_residue,
        "shadow_residue": shadow_residue,
        "residue_matches": series_residue == shadow_residue,
    }


def build_report(max_exhaustive_length: int = 10) -> dict[str, object]:
    if not 1 <= max_exhaustive_length <= 16:
        raise ShadowInputError(
            "max_exhaustive_length must lie in [1, 16], "
            f"got {max_exhaustive_length}"
        )

    failures: list[dict[str, object]] = []
    checked = 0
    for length in range(1, max_exhaustive_length + 1):
        for word in itertools.product((0, 1), repeat=length):
            row = verify_word(word)
            checked += 1
            if not all(
                row[key]
                for key in (
                    "parity_matches",
                    "returns_after_period",
                    "residue_matches",
                )
            ):
                failures.append(row)

    lengths = (2, 3, 5, 8, 13, 21, 34, 55)
    fibonacci_rows = [verify_word(fibonacci_prefix(length)) for length in lengths]
    coherence = []
    for left, right in zip(fibonacci_rows, fibonacci_rows[1:]):
        left_value = Fraction(str(left["fixed_point"]))
        right_value = Fraction(str(right["fixed_point"]))
        required = int(left["length"])
        valuation = two_adic_agreement(left_value, right_value)
        matches = valuation is None or valuation >= required
        coherence.append(
            {
                "left_length": required,
                "right_length": int(right["length"]),
                "difference_v2": valuation,
                "required_v2": required,
                "matches": matches,
            }
        )

    height_rows = recurrent_height_certificates(
        fibonacci_prefix(lengths[-1]), max_block=24
    )
    all_checks_passed = (
        not failures
        and all(row["matches"] for row in coherence)
        and bool(height_rows)
        and all(row["bound_holds"] for row in height_rows)
    )
    return {
        "schema_version": 1,
        "object": "periodic_rational_collatz_shadows",
        "claim_scope": {
            "proved_symbolically": "every finite parity word has an exact periodic rational shadow",
            "verified_finitely": (
                "three independent identities for every word through the configured bound"
            ),
            "not_claimed": (
                "a positive-integer counterexample, irrationality from finite data, "
                "or resolution of eventual lift stabilization"
            ),
        },
        "exhaustive": {
            "max_length": max_exhaustive_length,
            "words_checked": checked,
            "failures": failures,
        },
        "fibonacci_periodic_shadows": fibonacci_rows,
        "fibonacci_coherence": coherence,
        "fibonacci_recurrent_height_bounds": height_rows,
        "all_checks_passed": all_checks_passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-exhaustive-length", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = build_report(args.max_exhaustive_length)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output is not None:
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if report["all_checks_passed"] else 1
    except Exception as exc:
        failure = {
            "component": "rational_shadow",
            "rootCause": str(exc),
            "failureType": type(exc).__name__,
        }
        print(json.dumps({"error": failure}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
