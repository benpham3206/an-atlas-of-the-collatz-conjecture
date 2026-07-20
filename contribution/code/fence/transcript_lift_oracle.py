"""Exact finite oracle for Collatz transcript lift bits.

For a binary parity transcript q, let r_L be the unique representative in
[0, 2^L) whose first L accelerated-Collatz parity bits equal q[:L].  Coherence
forces

    r_(L+1) = r_L + epsilon_L * 2^L,  epsilon_L in {0, 1}.

The epsilon_L are the ordinary binary digits of the 2-adic state Phi(q).
Consequently q is realized by a positive ordinary integer exactly when the
lift sequence is eventually zero and the stabilized residue is positive.

This program is a finite probe, not a decision procedure for eventual zero.
It constructs residues by a lift recurrence and independently checks selected
prefixes using the defining 2-adic series for Phi.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Iterable, Sequence


Bit = int


class OracleInputError(ValueError):
    """Raised when a transcript generator produces a non-bit."""


def _checked_bit(value: int, *, index: int) -> Bit:
    if value not in (0, 1):
        raise OracleInputError(
            f"transcript bit at index {index} must be 0 or 1, got {value!r}"
        )
    return value


def lift_trace(bits: Iterable[Bit]) -> list[dict[str, int]]:
    """Return the exact coherent residue and lift bit after every input bit.

    State after L bits:
      r = r_L,
      pow3 = 3^(number of ones),
      z = (pow3*r + c_w)/2^L,
    where c_w is the affine composite offset of the length-L word.

    If b is the next word bit, divisibility by 2^(L+1) gives
      epsilon = (z + b) mod 2.
    The formulas below then update z without modular inverses.
    """

    residue = 0
    quotient = 0
    pow3 = 1
    rows: list[dict[str, int]] = []

    for index, raw_bit in enumerate(bits):
        bit = _checked_bit(raw_bit, index=index)
        epsilon = (quotient + bit) & 1
        residue += epsilon << index

        if bit:
            pow3 *= 3
            numerator = 3 * quotient + 1 + epsilon * pow3
        else:
            numerator = quotient + epsilon * pow3

        if numerator & 1:
            raise ArithmeticError(
                "{component: transcript lift recurrence, "
                f"root cause: odd update numerator at index {index}, "
                "failure type: invariant violation}"
            )
        quotient = numerator // 2
        rows.append(
            {
                "length": index + 1,
                "transcript_bit": bit,
                "lift_bit": epsilon,
                "residue": residue,
                "quotient": quotient,
                "pow3": pow3,
            }
        )

    return rows


def phi_prefix_residue(bits: Sequence[Bit]) -> int:
    """Compute Phi(q) modulo 2^L directly from a length-L prefix.

    This is deliberately independent of ``lift_trace``.  If the ones occur at
    d_0 < ... < d_(a-1), it evaluates

        -sum_j 2^d_j / 3^(j+1)  (mod 2^L).
    """

    length = len(bits)
    if length == 0:
        return 0

    modulus = 1 << length
    inv3 = pow(3, -1, modulus)
    inv3_power = inv3
    residue = 0

    for index, raw_bit in enumerate(bits):
        bit = _checked_bit(raw_bit, index=index)
        if bit:
            residue = (residue - (1 << index) * inv3_power) % modulus
            inv3_power = (inv3_power * inv3) % modulus

    return residue


def thue_morse(length: int) -> list[Bit]:
    return [index.bit_count() & 1 for index in range(length)]


def morphic_prefix(seed: str, rules: dict[str, str], length: int) -> list[Bit]:
    word = seed
    while len(word) < length:
        word = "".join(rules[symbol] for symbol in word)
    return [_checked_bit(int(symbol), index=i) for i, symbol in enumerate(word[:length])]


def period_doubling(length: int) -> list[Bit]:
    return morphic_prefix("0", {"0": "01", "1": "00"}, length)


def _grid(max_length: int) -> list[int]:
    values: list[int] = []
    length = 8
    while length < max_length:
        values.append(length)
        length *= 2
    values.append(max_length)
    return sorted(set(value for value in values if 1 <= value <= max_length))


def _max_zero_run(bits: Sequence[Bit]) -> int:
    best = current = 0
    for bit in bits:
        if bit == 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def _trailing(bits: Sequence[Bit], value: Bit) -> int:
    count = 0
    for bit in reversed(bits):
        if bit != value:
            break
        count += 1
    return count


def analyze_transcript(
    name: str,
    bits: Sequence[Bit],
    *,
    exact_value: int | None = None,
    exact_classification: str | None = None,
) -> dict:
    trace = lift_trace(bits)
    lift_bits = [row["lift_bit"] for row in trace]
    checkpoints = []
    mismatches = []

    for length in _grid(len(bits)):
        recurrence_residue = trace[length - 1]["residue"]
        series_residue = phi_prefix_residue(bits[:length])
        matches = recurrence_residue == series_residue
        row = {
            "length": length,
            "recurrence_residue": recurrence_residue,
            "series_residue": series_residue,
            "matches": matches,
            "lift_ones": sum(lift_bits[:length]),
            "trailing_zero_lifts": _trailing(lift_bits[:length], 0),
        }
        checkpoints.append(row)
        if not matches:
            mismatches.append(row)

    if mismatches:
        verdict = "FINDING_PATH_MISMATCH"
    elif exact_classification is not None:
        verdict = exact_classification
    else:
        verdict = "NONSTABILIZED_THROUGH_BOUND"

    result = {
        "name": name,
        "length": len(bits),
        "transcript_ones": sum(bits),
        "lift_ones": sum(lift_bits),
        "last_lift_one": max((i for i, bit in enumerate(lift_bits) if bit), default=None),
        "max_zero_run": _max_zero_run(lift_bits),
        "trailing_zero_lifts": _trailing(lift_bits, 0),
        "residue_bit_length": trace[-1]["residue"].bit_length() if trace else 0,
        "exact_value": exact_value,
        "checkpoints": checkpoints,
        "mismatches": mismatches,
        "verdict": verdict,
    }

    if exact_value is not None and trace:
        modulus = 1 << len(bits)
        expected_residue = exact_value % modulus
        result["exact_value_matches"] = trace[-1]["residue"] == expected_residue

    return result


def build_report(max_length: int = 4096) -> dict:
    if max_length < 16:
        raise OracleInputError(f"max_length must be at least 16, got {max_length}")

    controls = {
        "zero": ([0] * max_length, 0, "EXACT_ZERO_NOT_POSITIVE"),
        "one_cycle": ([1 - (i & 1) for i in range(max_length)], 1, "EXACT_POSITIVE_INTEGER"),
        "two_cycle": ([i & 1 for i in range(max_length)], 2, "EXACT_POSITIVE_INTEGER"),
        "all_ones": ([1] * max_length, -1, "EXACT_NEGATIVE_INTEGER"),
        "single_one": ([1] + [0] * (max_length - 1), None, "EXACT_NONINTEGER_MINUS_ONE_THIRD"),
    }
    live = {
        "thue_morse": thue_morse(max_length),
        "period_doubling": period_doubling(max_length),
    }

    analyses = []
    for name, (bits, value, classification) in controls.items():
        analyses.append(
            analyze_transcript(
                name,
                bits,
                exact_value=value,
                exact_classification=classification,
            )
        )
    for name, bits in live.items():
        analyses.append(analyze_transcript(name, bits))

    mismatches = [
        {"name": analysis["name"], "rows": analysis["mismatches"]}
        for analysis in analyses
        if analysis["mismatches"]
    ]
    exact_failures = [
        analysis["name"]
        for analysis in analyses
        if analysis.get("exact_value_matches") is False
    ]

    return {
        "schema_version": 1,
        "object": "collatz_transcript_lift_cocycle",
        "semantics": {
            "finite": "nonstabilization is evidence only, never nonintegrality proof",
            "positive_integer": "lift bits eventually zero and stabilized residue positive",
            "negative_integer": "lift bits eventually one",
        },
        "params": {"max_length": max_length, "checkpoint_grid": _grid(max_length)},
        "path_independence": {
            "path_a": "exact quotient lift recurrence",
            "path_b": "direct modular Phi prefix series",
        },
        "analyses": analyses,
        "mismatches": mismatches,
        "exact_control_failures": exact_failures,
        "all_checks_passed": not mismatches and not exact_failures,
    }


def _description_hash(report: dict) -> str:
    payload = json.dumps(report["params"], sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    started = time.perf_counter()
    try:
        report = build_report(args.max_length)
        report["description_hash"] = _description_hash(report)
        report["runtime_ms"] = round((time.perf_counter() - started) * 1000, 3)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output is not None:
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if report["all_checks_passed"] else 1
    except Exception as exc:
        failure = {
            "component": "transcript_lift_oracle",
            "rootCause": str(exc),
            "failureType": type(exc).__name__,
        }
        print(json.dumps({"error": failure}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
