"""Exact checks for the Collatz periodic-shadow barrier.

This program checks finite instances of a symbolic theorem. It does not prove
the Collatz conjecture. The proof is in the companion research note.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable


Bit = int


class VerificationInputError(ValueError):
    """Report an invalid verifier input."""


def checked_word(bits: Iterable[Bit]) -> tuple[Bit, ...]:
    word = tuple(bits)
    if not word:
        raise VerificationInputError("word must contain at least one bit")
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise VerificationInputError(
                f"word bit at index {index} must be 0 or 1, got {bit!r}"
            )
    return word


def terras_step_integer(value: int) -> int:
    return value // 2 if value % 2 == 0 else (3 * value + 1) // 2


def terras_step_rational(value: Fraction) -> Fraction:
    if value.denominator % 2 == 0:
        raise VerificationInputError(
            f"rational state must have odd denominator, got {value.denominator}"
        )
    return value / 2 if value.numerator % 2 == 0 else (3 * value + 1) / 2


def parity_prefix_integer(value: int, length: int) -> tuple[Bit, ...]:
    bits: list[Bit] = []
    state = value
    for _ in range(length):
        bits.append(state % 2)
        state = terras_step_integer(state)
    return tuple(bits)


def parity_prefix_rational(value: Fraction, length: int) -> tuple[Bit, ...]:
    bits: list[Bit] = []
    state = value
    for _ in range(length):
        bits.append(state.numerator % 2)
        state = terras_step_rational(state)
    return tuple(bits)


def iterate_integer(value: int, steps: int) -> int:
    state = value
    for _ in range(steps):
        state = terras_step_integer(state)
    return state


def iterate_rational(value: Fraction, steps: int) -> Fraction:
    state = value
    for _ in range(steps):
        state = terras_step_rational(state)
    return state


def affine_data(bits: Iterable[Bit]) -> tuple[int, int, int]:
    """Return ``(3^s, c_w, 2^L)`` for a Terras parity word."""

    word = checked_word(bits)
    offset = 0
    ones = 0
    for index, bit in enumerate(word):
        if bit:
            offset = 3 * offset + (1 << index)
            ones += 1
    return 3**ones, offset, 1 << len(word)


def canonical_positive_residue(bits: Iterable[Bit]) -> int:
    """Find the least positive integer in the word's residue cylinder.

    This is an independent direct-iteration path. It does not use the affine
    offset or the inverse 2-adic series.
    """

    word = checked_word(bits)
    modulus = 1 << len(word)
    for candidate in range(1, modulus + 1):
        if parity_prefix_integer(candidate, len(word)) == word:
            return candidate
    raise AssertionError("Terras cylinder residue was not found")


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def verify_word(bits: Iterable[Bit]) -> dict[str, object]:
    word = checked_word(bits)
    pow3, offset, pow2 = affine_data(word)
    denominator = pow2 - pow3
    shadow = Fraction(offset, denominator)
    canonical = canonical_positive_residue(word)

    parity_matches = parity_prefix_rational(shadow, len(word)) == word
    shadow_returns = iterate_rational(shadow, len(word)) == shadow
    identity_failures: list[dict[str, object]] = []

    if denominator > 0:
        strict_threshold = Fraction(offset - pow2, denominator)
        threshold_floor = floor_fraction(strict_threshold)
        formula_count = (
            0
            if threshold_floor < canonical
            else (threshold_floor - canonical) // pow2 + 1
        )
        predicted_count = 0
        observed_count = 0
        last_to_check = max(canonical, threshold_floor + pow2)
        for start in range(canonical, last_to_check + 1, pow2):
            endpoint = iterate_integer(start, len(word))
            predicted_strict_rise = start <= strict_threshold
            observed_strict_rise = endpoint >= start + 1
            if predicted_strict_rise:
                predicted_count += 1
            if observed_strict_rise:
                observed_count += 1
            if predicted_strict_rise != observed_strict_rise:
                identity_failures.append(
                    {
                        "start": start,
                        "endpoint": endpoint,
                        "predicted_strict_rise": predicted_strict_rise,
                    }
                )
        count_matches = (
            predicted_count == formula_count and observed_count == formula_count
        )
    else:
        strict_threshold = None
        formula_count = None
        count_matches = True
        for lift in range(5):
            start = canonical + lift * pow2
            endpoint = iterate_integer(start, len(word))
            if endpoint <= start:
                identity_failures.append(
                    {"start": start, "endpoint": endpoint, "expected": "strict rise"}
                )

    return {
        "word": "".join(str(bit) for bit in word),
        "length": len(word),
        "ones": sum(word),
        "pow2": pow2,
        "pow3": pow3,
        "offset": offset,
        "contractive": denominator > 0,
        "raw_denominator": denominator,
        "periodic_shadow": str(shadow),
        "canonical_positive_residue": canonical,
        "strict_threshold": (
            str(strict_threshold) if strict_threshold is not None else None
        ),
        "strict_candidate_count": formula_count,
        "parity_matches": parity_matches,
        "shadow_returns": shadow_returns,
        "count_matches": count_matches,
        "identity_failures": identity_failures,
    }


def build_report(max_length: int) -> dict[str, object]:
    if not 1 <= max_length <= 12:
        raise VerificationInputError(
            f"max_length must lie in [1, 12], got {max_length}"
        )

    words_checked = 0
    contractive_words = 0
    expansive_words = 0
    failures: list[dict[str, object]] = []
    survivors_by_length: dict[str, int] = {}

    for length in range(1, max_length + 1):
        survivors = 0
        for word in itertools.product((0, 1), repeat=length):
            row = verify_word(word)
            words_checked += 1
            if row["contractive"]:
                contractive_words += 1
                if int(row["strict_candidate_count"]) > 0:
                    survivors += 1
            else:
                expansive_words += 1
            if (
                not row["parity_matches"]
                or not row["shadow_returns"]
                or not row["count_matches"]
                or row["identity_failures"]
            ):
                failures.append(row)
        survivors_by_length[str(length)] = survivors

    return {
        "schema_version": 1,
        "object": "collatz_periodic_shadow_barrier",
        "claim_scope": {
            "proved_symbolically": (
                "the periodic rational shadow is the exact real descent barrier"
            ),
            "verified_finitely": (
                "direct integer and rational iteration for every word through "
                f"length {max_length}"
            ),
            "not_claimed": (
                "a Collatz proof, a counterexample, or an infinite-path exclusion"
            ),
        },
        "max_length": max_length,
        "words_checked": words_checked,
        "contractive_words": contractive_words,
        "expansive_words": expansive_words,
        "contractive_words_with_strict_candidates": survivors_by_length,
        "failures": failures,
        "all_checks_passed": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        report = build_report(args.max_length)
    except VerificationInputError as error:
        parser.error(
            json.dumps(
                {
                    "component": "shadow_barrier_verifier",
                    "rootCause": str(error),
                    "failureType": "invalid_input",
                },
                sort_keys=True,
            )
        )

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
