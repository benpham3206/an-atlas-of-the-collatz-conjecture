#!/usr/bin/env python3
"""Finite exact audit for the rational Terras complexity lemmas.

This program does not prove the asymptotic theorem. It exhaustively checks the
integer-scaled recurrence, block-affine identity, congruence collision lemma,
and denominator-cleared growth bound over a finite deterministic grid of odd
rational denominators and signed numerators.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Orbit:
    y: tuple[int, ...]
    q: tuple[int, ...]


def scaled_step(y: int, d: int) -> tuple[int, int]:
    """One Terras step for x=y/d with d positive odd; return (next_y, parity)."""
    if d <= 0 or d % 2 == 0:
        raise ValueError("d must be positive and odd")
    q = y & 1
    numerator = (3 if q else 1) * y + d * q
    assert numerator % 2 == 0
    return numerator // 2, q


def orbit(a: int, d: int, steps: int) -> Orbit:
    ys = [a]
    qs: list[int] = []
    y = a
    for _ in range(steps):
        y, q = scaled_step(y, d)
        qs.append(q)
        ys.append(y)
    return Orbit(tuple(ys), tuple(qs))


def affine_constant(word: tuple[int, ...]) -> tuple[int, int]:
    """Return (number of ones, c) in 2^k y_k = 3^s y_0 + d*c."""
    s = 0
    c = 0
    for j, q in enumerate(word):
        if q:
            c = 3 * c + (1 << j)
            s += 1
    return s, c


def check_case(a: int, d: int, steps: int, max_block: int) -> int:
    data = orbit(a, d, steps + max_block)
    ys, qs = data.y, data.q
    checks = 0

    # Exact recurrence and denominator-cleared absolute growth.
    for j in range(steps + max_block):
        q = qs[j]
        expected = ((3 if q else 1) * ys[j] + d * q) // 2
        assert ys[j + 1] == expected
        assert 2 * (abs(ys[j + 1]) + d) <= 3 * (abs(ys[j]) + d)
        checks += 2

    # Exact affine block law at every start and block length in range.
    for i in range(steps + 1):
        for k in range(1, max_block + 1):
            word = tuple(qs[i : i + k])
            s, c = affine_constant(word)
            assert (1 << k) * ys[i + k] == (3**s) * ys[i] + d * c
            checks += 1

    # Equal blocks imply congruence modulo 2^k. If their scaled states are
    # closer than 2^k, the states must actually coincide.
    for k in range(1, max_block + 1):
        seen: dict[tuple[int, ...], int] = {}
        modulus = 1 << k
        for i in range(steps + 1):
            word = tuple(qs[i : i + k])
            if word in seen:
                j = seen[word]
                assert (ys[i] - ys[j]) % modulus == 0
                if abs(ys[i] - ys[j]) < modulus:
                    assert ys[i] == ys[j]
                checks += 2
            else:
                seen[word] = i
    return checks


def main() -> None:
    denominators = tuple(range(1, 32, 2))
    numerators = tuple(range(-128, 129))
    steps = 48
    max_block = 12
    total = 0
    for d in denominators:
        for a in numerators:
            total += check_case(a, d, steps, max_block)
    print(
        {
            "status": "ok",
            "odd_denominators": len(denominators),
            "signed_numerators": len(numerators),
            "steps": steps,
            "max_block": max_block,
            "assertion_groups_checked": total,
        }
    )


if __name__ == "__main__":
    main()
