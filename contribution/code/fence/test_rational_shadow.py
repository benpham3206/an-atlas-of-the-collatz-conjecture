"""Independent checks for exact periodic rational Collatz shadows."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from rational_shadow import (  # noqa: E402
    build_report,
    fibonacci_prefix,
    periodic_shadow,
    rational_height,
    rational_parity_prefix,
    rational_residue,
    recurrent_height_certificates,
    terras_step,
    two_adic_agreement,
    verify_word,
)


def test_every_word_through_length_nine_has_an_exact_periodic_shadow() -> None:
    for length in range(1, 10):
        for word in itertools.product((0, 1), repeat=length):
            row = verify_word(word)
            assert row["parity_matches"] is True
            assert row["returns_after_period"] is True
            assert row["residue_matches"] is True


def test_known_integer_and_noninteger_periodic_states() -> None:
    assert periodic_shadow((1, 0)) == 1
    assert periodic_shadow((0, 1)) == 2
    assert periodic_shadow((1,)) == -1
    assert periodic_shadow((1, 0, 0)) == Fraction(1, 5)


def test_rational_branch_iteration_preserves_odd_denominators() -> None:
    value = Fraction(22, 23)
    expected = fibonacci_prefix(5)
    assert rational_parity_prefix(value, 5) == expected
    for _ in range(50):
        assert value.denominator % 2 == 1
        value = terras_step(value)


def test_fibonacci_shadows_form_a_coherent_two_adic_sequence() -> None:
    lengths = (3, 5, 8, 13, 21, 34)
    shadows = [periodic_shadow(fibonacci_prefix(length)) for length in lengths]
    for index, left_length in enumerate(lengths):
        for right in shadows[index + 1 :]:
            valuation = two_adic_agreement(shadows[index], right)
            assert valuation is None or valuation >= left_length
            assert rational_residue(shadows[index], left_length) == rational_residue(
                right, left_length
            )


def test_report_keeps_finite_evidence_scope_explicit() -> None:
    report = build_report(8)
    assert report["all_checks_passed"] is True
    assert report["exhaustive"]["words_checked"] == 510
    assert report["exhaustive"]["failures"] == []
    assert "not_claimed" in report["claim_scope"]


def test_recurrent_fibonacci_blocks_force_exact_height_bounds() -> None:
    word = fibonacci_prefix(55)
    shadow = periodic_shadow(word)
    rows = recurrent_height_certificates(word, max_block=24)
    assert rows
    assert all(row["bound_holds"] is True for row in rows)
    assert all(row["height"] == rational_height(shadow) for row in rows)
    assert max(int(row["block_length"]) for row in rows) >= 13
