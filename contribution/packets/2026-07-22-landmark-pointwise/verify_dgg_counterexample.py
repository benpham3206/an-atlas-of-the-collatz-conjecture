#!/usr/bin/env python3
"""Exact verifier for the publicly posted Dinitz-Garg-Goemans instance.

The instance has three commodities.  Each commodity has exactly two routes:
a zero-cost "long" route and a positive-cost "direct" route.  Arc capacities
are the loads of the displayed fractional flow.  The allowed additive capacity
violation is d_max = 15.

This script checks:
  1. feasibility and cost 58 of the displayed fractional flow;
  2. every one of the 2^3 unsplittable routings;
  3. the minimum feasible unsplittable cost is 60.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Tuple

Arc = str


@dataclass(frozen=True)
class Route:
    arcs: Tuple[Arc, ...]
    unit_cost: int


@dataclass(frozen=True)
class Commodity:
    name: str
    demand: int
    direct: Route
    long: Route


CAPACITY: Dict[Arc, int] = {
    "s_t1": 10,
    "s_t2": 6,
    "s_u": 24,
    "u_v": 14,
    "v_w": 9,
    "v_t1": 5,
    "w_t2": 4,
    "w_t3": 5,
    "u_t3": 10,
}

COMMODITIES = (
    Commodity(
        "t1",
        15,
        direct=Route(("s_t1",), 2),
        long=Route(("s_u", "u_v", "v_t1"), 0),
    ),
    Commodity(
        "t2",
        10,
        direct=Route(("s_t2",), 3),
        long=Route(("s_u", "u_v", "v_w", "w_t2"), 0),
    ),
    Commodity(
        "t3",
        15,
        direct=Route(("s_u", "u_t3"), 2),
        long=Route(("s_u", "u_v", "v_w", "w_t3"), 0),
    ),
)

# Amount sent on the direct route in the displayed fractional solution.
FRACTIONAL_DIRECT = {"t1": 10, "t2": 6, "t3": 10}
D_MAX = max(c.demand for c in COMMODITIES)


def add_load(load: Dict[Arc, int], arcs: Iterable[Arc], amount: int) -> None:
    for arc in arcs:
        load[arc] = load.get(arc, 0) + amount


def verify_fractional() -> tuple[Dict[Arc, int], int]:
    load: Dict[Arc, int] = {}
    cost = 0
    for c in COMMODITIES:
        direct_amount = FRACTIONAL_DIRECT[c.name]
        long_amount = c.demand - direct_amount
        assert 0 <= direct_amount <= c.demand
        add_load(load, c.direct.arcs, direct_amount)
        add_load(load, c.long.arcs, long_amount)
        cost += direct_amount * c.direct.unit_cost
        cost += long_amount * c.long.unit_cost
    assert load == CAPACITY, (load, CAPACITY)
    assert cost == 58, cost
    return load, cost


def verify_unsplittable() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for choices in product(("direct", "long"), repeat=len(COMMODITIES)):
        load: Dict[Arc, int] = {arc: 0 for arc in CAPACITY}
        cost = 0
        for c, choice in zip(COMMODITIES, choices):
            route = getattr(c, choice)
            add_load(load, route.arcs, c.demand)
            cost += c.demand * route.unit_cost
        excess = {arc: load[arc] - CAPACITY[arc] for arc in CAPACITY}
        feasible = all(value <= D_MAX for value in excess.values())
        rows.append(
            {
                "choices": dict(zip((c.name for c in COMMODITIES), choices)),
                "cost": cost,
                "feasible": feasible,
                "max_excess": max(excess.values()),
                "violating_arcs": tuple(
                    arc for arc, value in excess.items() if value > D_MAX
                ),
            }
        )
    feasible_costs = [int(row["cost"]) for row in rows if bool(row["feasible"])]
    assert feasible_costs
    assert min(feasible_costs) == 60, feasible_costs
    return rows


def main() -> None:
    load, fractional_cost = verify_fractional()
    rows = verify_unsplittable()
    print(f"d_max = {D_MAX}")
    print(f"fractional cost = {fractional_cost}")
    print(f"fractional loads = {load}")
    print("\nAll unsplittable choices:")
    for row in rows:
        print(row)
    print("\nminimum feasible unsplittable cost = 60")
    print("certificate verified")


if __name__ == "__main__":
    main()
