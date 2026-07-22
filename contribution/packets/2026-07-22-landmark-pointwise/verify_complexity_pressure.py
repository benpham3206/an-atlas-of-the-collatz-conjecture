#!/usr/bin/env python3
"""Finite exact checks for the height-complexity and pressure identities.

This is not a proof of the asymptotic theorems. It independently checks the
finite identities and implications used in the proof on a configurable range.
"""
from __future__ import annotations

from fractions import Fraction
from math import ceil, log2


def terras(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def orbit_and_parity(n: int, steps: int) -> tuple[list[int], list[int]]:
    xs = [n]
    qs: list[int] = []
    for _ in range(steps):
        qs.append(xs[-1] & 1)
        xs.append(terras(xs[-1]))
    return xs, qs


def green_exact(n: int, q: list[int], L: int) -> Fraction:
    # x_L = M(0,L)n + 1/2 sum q_j M(j+1,L)
    suffix_ones = [0] * (L + 1)
    for j in range(L - 1, -1, -1):
        suffix_ones[j] = suffix_ones[j + 1] + q[j]
    value = Fraction(3 ** suffix_ones[0] * n, 2**L)
    for j in range(L):
        if q[j]:
            value += Fraction(3 ** suffix_ones[j + 1], 2 ** (L - j))
    return value


def factor_complexity(q: list[int], k: int) -> int:
    return len({tuple(q[i : i + k]) for i in range(len(q) - k + 1)})


def check_seed(n: int, N: int, k_max: int) -> None:
    # Need N+k_max symbols to form all N+1 future blocks.
    xs, q = orbit_and_parity(n, N + k_max)

    # Exact Green expansion.
    for L in range(1, N + 1):
        got = green_exact(n, q, L)
        assert got.denominator == 1 and got.numerator == xs[L], (n, L, got, xs[L])

    # Universal affine growth bound x_j+1 <= (3/2)^j (n+1).
    for j in range(N + 1):
        assert Fraction(xs[j] + 1, 1) <= Fraction(3**j * (n + 1), 2**j)

    H = max(xs[: N + 1])
    for k in range(1, k_max + 1):
        blocks = [tuple(q[i : i + k]) for i in range(N + 1)]
        if 2**k > H and len(set(blocks)) < N + 1:
            # A collision below 2^k must be an actual state collision.
            seen: dict[tuple[int, ...], int] = {}
            for i, b in enumerate(blocks):
                if b in seen:
                    j = seen[b]
                    assert xs[i] == xs[j], (n, N, k, i, j, xs[i], xs[j])
                else:
                    seen[b] = i


def main() -> None:
    seeds = 2000
    N = 80
    k_max = 24
    for n in range(1, seeds + 1):
        check_seed(n, N, k_max)
    print({"status": "ok", "seeds": seeds, "N": N, "k_max": k_max})


if __name__ == "__main__":
    main()
