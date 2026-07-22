"""Targeted tests for primitive uniform binary substitution analyzer."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from primitive_uniform_obstruction import (  # noqa: E402
    DEFAULT_ALPHA_HI,
    DEFAULT_ALPHA_LO,
    FINITE_EVIDENCE_SEMANTICS,
    PERIOD_DOUBLING_RULES,
    THUE_MORSE_RULES,
    SubstitutionError,
    analyze_morphism,
    build_report,
    classify_density_vs_alpha,
    default_alpha_bound_certificate,
    factor_count,
    factor_set,
    fixed_point_prefix,
    incidence_matrix,
    is_primitive,
    max_supercritical_discrepancy,
    one_frequency,
    validate_uniform_binary_morphism,
)


MODULE_PATH = Path(__file__).resolve().with_name("primitive_uniform_obstruction.py")


def test_incidence_matrices_named_controls() -> None:
    assert incidence_matrix(THUE_MORSE_RULES) == ((1, 1), (1, 1))
    assert incidence_matrix(PERIOD_DOUBLING_RULES) == ((1, 2), (1, 0))


def test_primitivity_named_controls_and_counterexample() -> None:
    assert is_primitive(incidence_matrix(THUE_MORSE_RULES)) is True
    assert is_primitive(incidence_matrix(PERIOD_DOUBLING_RULES)) is True
    # Period-2 permutation matrix: powers alternate, never entrywise positive.
    assert is_primitive(((0, 1), (1, 0))) is False
    # Positive matrix is primitive.
    assert is_primitive(((1, 1), (1, 1))) is True


def test_exact_one_frequencies() -> None:
    assert one_frequency(THUE_MORSE_RULES, seed=0) == Fraction(1, 2)
    assert one_frequency(PERIOD_DOUBLING_RULES, seed=0) == Fraction(1, 3)


def test_known_fixed_point_prefixes() -> None:
    tm = fixed_point_prefix(THUE_MORSE_RULES, 16, seed=0)
    assert tm == (0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0)
    assert "".join(map(str, tm[:8])) == "01101001"

    pd = fixed_point_prefix(PERIOD_DOUBLING_RULES, 16, seed=0)
    assert pd[:8] == (0, 1, 0, 0, 0, 1, 0, 1)
    assert "".join(map(str, pd[:8])) == "01000101"

    # Matches independent Thue-Morse definition: popcount mod 2.
    for index, bit in enumerate(tm):
        assert bit == (index.bit_count() & 1)


def test_factor_counting_matches_naive_set() -> None:
    word = fixed_point_prefix(THUE_MORSE_RULES, 64, seed=0)
    for n in (1, 2, 3, 4, 5, 8):
        naive = {
            tuple(word[i : i + n]) for i in range(len(word) - n + 1)
        }
        assert factor_set(word, n) == naive
        assert factor_count(word, n) == len(naive)


def test_invalid_input_errors_are_structured() -> None:
    with pytest.raises(SubstitutionError) as empty:
        validate_uniform_binary_morphism({0: (), 1: (0, 1)})
    assert empty.value.as_structured()["failureType"] == "validation_error"
    assert "component" in empty.value.as_structured()
    assert "rootCause" in empty.value.as_structured()

    with pytest.raises(SubstitutionError):
        validate_uniform_binary_morphism({0: (0,), 1: (1,)})  # k < 2

    with pytest.raises(SubstitutionError):
        validate_uniform_binary_morphism({0: (0, 1), 1: (0, 1, 1)})  # non-uniform

    with pytest.raises(SubstitutionError):
        validate_uniform_binary_morphism({0: (0, 2), 1: (1, 0)})  # nonbinary

    with pytest.raises(SubstitutionError):
        # seed 1 but image(1)=10 does not start with 1
        validate_uniform_binary_morphism({0: (0, 1), 1: (0, 0)}, seed=1)

    with pytest.raises(SubstitutionError) as nonprim:
        one_frequency({0: (0, 0), 1: (1, 1)}, seed=0)
    assert nonprim.value.failure_type == "non_primitive"


def test_interval_safe_discrepancy_classification() -> None:
    alpha_lo = Fraction(63, 100)  # 0.63
    alpha_hi = Fraction(631, 1000)  # 0.631

    # 10/16 = 0.625 < 0.63 → subcritical
    assert classify_density_vs_alpha(10, 16, alpha_lo, alpha_hi) == "subcritical"
    # 11/16 = 0.6875 > 0.631 → supercritical
    assert classify_density_vs_alpha(11, 16, alpha_lo, alpha_hi) == "supercritical"
    # density inside (alpha_lo, alpha_hi) → inconclusive
    # 631/1000 = 0.631; need ones/length in (0.63, 0.631)
    # 63/100 = 0.63 exactly is subcritical by <= alpha_lo
    assert classify_density_vs_alpha(63, 100, alpha_lo, alpha_hi) == "subcritical"
    # 630/1000 = 0.63 → subcritical; 631/1000 = alpha_hi → supercritical
    assert classify_density_vs_alpha(631, 1000, alpha_lo, alpha_hi) == "supercritical"

    # Construct a density strictly between bounds: 6301/10000 = 0.6301
    assert alpha_lo < Fraction(6301, 10000) < alpha_hi
    assert (
        classify_density_vs_alpha(6301, 10000, alpha_lo, alpha_hi) == "inconclusive"
    )

    # Window scan on an all-ones block is safely supercritical.
    ones_word = (1,) * 32
    stats = max_supercritical_discrepancy(ones_word, 16, alpha_lo, alpha_hi)
    assert stats["any_supercritical"] is True
    assert stats["max_ones"] == 16
    assert stats["max_safe_discrepancy_lo"] == Fraction(16) - alpha_hi * 16
    assert stats["max_safe_discrepancy_lo"] > 0

    # All zeros: subcritical only.
    zeros = (0,) * 32
    zstats = max_supercritical_discrepancy(zeros, 16, alpha_lo, alpha_hi)
    assert zstats["any_subcritical"] is True
    assert zstats["any_supercritical"] is False
    assert zstats["max_safe_discrepancy_lo"] is None

    with pytest.raises(SubstitutionError):
        classify_density_vs_alpha(1, 2, alpha_hi, alpha_lo)  # bad order


def test_default_alpha_bounds_have_exact_integer_certificates() -> None:
    certificate = default_alpha_bound_certificate()
    assert 3**63 < 2**100
    assert 2**1000 < 3**631
    assert certificate["verified"] is True
    assert certificate["arithmetic"] == "exact_integer"


def test_finite_evidence_semantics_explicit() -> None:
    report = build_report(prefix_length=64)
    assert report["evidence_scope"] == "finite_only"
    assert report["all_checks_passed"] is True
    assert "finite" in report["claim_scope"]["finite_evidence_only"].lower()
    assert "never prove" in report["claim_scope"]["finite_evidence_only"].lower()
    assert "Collatz" in report["claim_scope"]["not_claimed"]
    assert FINITE_EVIDENCE_SEMANTICS in report["claim_scope"]["finite_evidence_only"]
    for row in report["analyses"]:
        assert row["evidence_scope"] == "finite_only"
        assert row["primitive"] is True


def test_analyze_morphism_and_report_controls() -> None:
    tm = analyze_morphism("thue_morse", THUE_MORSE_RULES, prefix_length=32)
    assert tm["primitive"] is True
    assert tm["one_frequency"] == "1/2"
    assert tm["incidence_matrix"] == [[1, 1], [1, 1]]
    assert tm["prefix"].startswith("01101001")

    pd = analyze_morphism("period_doubling", PERIOD_DOUBLING_RULES, prefix_length=32)
    assert pd["primitive"] is True
    assert pd["one_frequency"] == "1/3"
    assert pd["incidence_matrix"] == [[1, 2], [1, 0]]
    assert pd["prefix"].startswith("01000101")

    report = build_report(prefix_length=128, window_length=16)
    assert report["all_checks_passed"] is True
    assert report["check_failures"] == []
    assert report["alpha_bound_certificate"]["verified"] is True
    assert report["alpha_bound_certificate"]["applies_to_params"] is True
    assert report["primitivity_algorithm"]["wielandt_bound"] == 2
    names = {row["name"] for row in report["analyses"]}
    assert names == {"thue_morse", "period_doubling"}


def test_cli_emits_deterministic_json_all_checks_passed() -> None:
    proc = subprocess.run(
        [sys.executable, str(MODULE_PATH), "--prefix-length", "64"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    report = json.loads(proc.stdout)
    assert report["all_checks_passed"] is True
    assert report["object"] == "primitive_uniform_binary_substitution_obstruction"
    # Determinism: second run matches exactly.
    proc2 = subprocess.run(
        [sys.executable, str(MODULE_PATH), "--prefix-length", "64"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc2.stdout == proc.stdout


def test_cli_structured_error_on_bad_alpha() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--alpha-lo",
            "not-a-fraction",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert "error" in payload
    err = payload["error"]
    assert set(err.keys()) == {"component", "rootCause", "failureType"}
    assert err["component"] == "primitive_uniform_obstruction"


def test_no_floats_in_acceptance_path() -> None:
    # Densities and frequencies are Fractions / ints only.
    freq = one_frequency(PERIOD_DOUBLING_RULES)
    assert isinstance(freq, Fraction)
    label = classify_density_vs_alpha(1, 2, DEFAULT_ALPHA_LO, DEFAULT_ALPHA_HI)
    assert label in {"subcritical", "supercritical", "inconclusive"}
    stats = max_supercritical_discrepancy(
        (1, 0, 1, 1, 0, 0, 1, 0) * 4,
        8,
        DEFAULT_ALPHA_LO,
        DEFAULT_ALPHA_HI,
    )
    disc = stats["max_safe_discrepancy_lo"]
    assert disc is None or isinstance(disc, Fraction)
