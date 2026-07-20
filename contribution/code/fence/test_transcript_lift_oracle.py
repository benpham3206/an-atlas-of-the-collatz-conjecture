"""Independent checks for the transcript lift oracle."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from transcript_lift_oracle import (  # noqa: E402
    analyze_transcript,
    build_report,
    lift_trace,
    period_doubling,
    phi_prefix_residue,
    thue_morse,
)


def _terras(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def _parity_word(n: int, length: int) -> tuple[int, ...]:
    bits = []
    for _ in range(length):
        bits.append(n & 1)
        n = _terras(n)
    return tuple(bits)


def _brute_residue(word: tuple[int, ...]) -> int:
    modulus = 1 << len(word)
    matches = []
    for residue in range(modulus):
        positive_lift = residue if residue > 0 else modulus
        if _parity_word(positive_lift, len(word)) == word:
            matches.append(residue)
    assert len(matches) == 1
    return matches[0]


def test_all_words_through_length_ten_match_direct_iteration() -> None:
    for length in range(1, 11):
        for word in itertools.product((0, 1), repeat=length):
            trace = lift_trace(word)
            assert trace[-1]["residue"] == _brute_residue(word)
            assert trace[-1]["residue"] == phi_prefix_residue(word)


def test_positive_integer_lift_bits_are_binary_digits() -> None:
    for n in range(1, 1001):
        length = max(16, n.bit_length() + 8)
        word = _parity_word(n, length)
        trace = lift_trace(word)
        for index, row in enumerate(trace):
            assert row["lift_bit"] == ((n >> index) & 1)
            assert row["residue"] == n % (1 << (index + 1))


def test_exact_periodic_controls() -> None:
    length = 64
    one = lift_trace([1, 0] * (length // 2))
    two = lift_trace([0, 1] * (length // 2))
    negative_one = lift_trace([1] * length)

    assert one[-1]["residue"] == 1
    assert sum(row["lift_bit"] for row in one) == 1
    assert two[-1]["residue"] == 2
    assert sum(row["lift_bit"] for row in two) == 1
    assert negative_one[-1]["residue"] == (1 << length) - 1
    assert all(row["lift_bit"] == 1 for row in negative_one)


def test_structured_prefix_paths_match() -> None:
    for bits in (thue_morse(512), period_doubling(512)):
        analysis = analyze_transcript("probe", bits)
        assert analysis["mismatches"] == []
        assert analysis["verdict"] == "NONSTABILIZED_THROUGH_BOUND"


def test_report_schema_and_controls() -> None:
    report = build_report(128)
    assert report["schema_version"] == 1
    assert report["all_checks_passed"] is True
    assert report["mismatches"] == []
    by_name = {analysis["name"]: analysis for analysis in report["analyses"]}
    assert by_name["one_cycle"]["exact_value_matches"] is True
    assert by_name["two_cycle"]["exact_value_matches"] is True
    assert by_name["all_ones"]["exact_value_matches"] is True
    assert by_name["single_one"]["verdict"] == "EXACT_NONINTEGER_MINUS_ONE_THIRD"
