"""
F2 — Collatz induced first-return maps + collapse search.

Imports Terras map from frozen F1; does not modify F1.

Exact integer arithmetic only (Fraction for mass accounting). Python 3 stdlib.

For residue class (k, r), 0 ≤ r < 2^k:
  r' = r if r > 0 else 2^k
  class = { n = r' + 2^k · m : m ≥ 0 }

Induced first-return of Terras T on the class is computed by iterative
explicit-stack symbolic DFS over 2-adic refinements of m, yielding exact
affine branches plus always-reported unresolved 2-adic mass.
"""

from __future__ import annotations

import heapq
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

try:
    from f1_word_calculus import terras
except ImportError:  # package-style import from repo root
    from fold.f1_word_calculus import terras

# ---------------------------------------------------------------------------
# Hard budgets (packet-exact, corrected spec)
# ---------------------------------------------------------------------------
K_MIN = 1
K_MAX = 5  # never attempt k > 5
S_EXTRA = 22  # s ≤ k + S_EXTRA per class
NODE_BUDGET = 3_000_000  # nodes per class
GLOBAL_TIME_BUDGET_SEC = 20 * 60
MASS_THRESHOLD = Fraction(1, 1 << 10)  # 2^{-10} for collapse witnesses

# Branch: domain m ≡ u (mod 2^s); induced free param m' ↦ α m' + β
# Full branch also stores (a, t): odd-step count and Terras steps to return.
BranchCanon = Tuple[int, int, int, int]  # (s, u, alpha, beta)
BranchFull = Tuple[int, int, int, int, int, int]  # (s, u, alpha, beta, a, t)
SignatureItem = Tuple[int, int, int]  # (s, a, t)


@dataclass(frozen=True)
class UnresolvedLeaf:
    """A DFS path that hit a cap before first return was decided."""

    s: int
    u: int
    t: int
    reason: str  # "max_s" | "node_budget"


@dataclass
class ClassResult:
    k: int
    r: int
    r_prime: int
    branches: Tuple[BranchFull, ...]
    unresolved: Tuple[UnresolvedLeaf, ...]
    unresolved_mass: Fraction  # exact dyadic rational
    nodes_visited: int
    max_s_cap: int
    truncated: bool  # True if node budget exhausted with work remaining

    def canonical(self) -> Tuple[BranchCanon, ...]:
        """Sorted resolved branches (s, u, alpha, beta) in lowest exact form."""
        canons = [
            normalize_branch(s, u, alpha, beta)
            for s, u, alpha, beta, _a, _t in self.branches
        ]
        return tuple(sorted(canons))

    def signature(self) -> Tuple[SignatureItem, ...]:
        """Multiset of (s, odd-steps, t) as a sorted tuple."""
        items = [(s, a, t) for s, u, alpha, beta, a, t in self.branches]
        return tuple(sorted(items))

    def resolved_mass(self) -> Fraction:
        m = Fraction(0)
        for s, _u, _a, _b, _od, _t in self.branches:
            m += Fraction(1, 1 << s)
        return m

    def total_mass(self) -> Fraction:
        """Resolved + unresolved; must equal 1."""
        return self.resolved_mass() + self.unresolved_mass


def r_prime(k: int, r: int) -> int:
    """Positive lift of residue r mod 2^k used as the class base."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    mod = 1 << k
    if not (0 <= r < mod):
        raise ValueError(f"r must satisfy 0 ≤ r < 2^{k}, got r={r}")
    return r if r > 0 else mod


def normalize_branch(s: int, u: int, alpha: int, beta: int) -> BranchCanon:
    """
    Lowest exact form of a branch.

    Domain: m ≡ u (mod 2^s) with 0 ≤ u < 2^s.
    Induced on free parameter m' = (m − u)/2^s: m' ↦ α m' + β.
    α, β are exact integers (no float, no free denominator).
    """
    if s < 0:
        raise ValueError("s must be nonnegative")
    if type(s) is not int or type(u) is not int:
        raise TypeError("s, u must be int")
    if type(alpha) is not int or type(beta) is not int:
        raise TypeError("alpha, beta must be int")
    mod = 1 << s
    return (s, u % mod, alpha, beta)


def _assert_ints(*vals: object) -> None:
    for v in vals:
        if type(v) is not int:
            raise TypeError(f"exact integer required, got {type(v).__name__}: {v!r}")


def _v_as_affine(A: int, B: int, t: int, s: int, u: int) -> Tuple[int, int]:
    """
    On m = u + 2^s m', write v = (A m + B)/2^t = P m' + Q with P, Q integers.
    Asserts exact integrality.
    """
    AuB = A * u + B
    A_shift = A << s  # A * 2^s
    den = 1 << t
    if AuB % den != 0:
        raise AssertionError(
            f"integrality fail Q: (A u + B)={AuB} not divisible by 2^{t}"
        )
    if A_shift % den != 0:
        raise AssertionError(
            f"integrality fail P: A*2^s={A_shift} not divisible by 2^{t}"
        )
    P = A_shift // den
    Q = AuB // den
    _assert_ints(P, Q)
    return P, Q


def _apply_terras_step(
    s: int, u: int, A: int, B: int, t: int, a: int, parity: int
) -> Tuple[int, int, int, int, int, int]:
    """
    Apply one Terras step given known parity of v.
    even: v' = v/2 = (A m + B)/2^{t+1}
    odd:  v' = (3v+1)/2 = (3A m + 3B + 2^t)/2^{t+1}
    """
    if parity == 0:
        return (s, u, A, B, t + 1, a)
    if parity == 1:
        return (s, u, 3 * A, 3 * B + (1 << t), t + 1, a + 1)
    raise ValueError(f"parity must be 0 or 1, got {parity}")


def _u_norm(s: int, u: int) -> int:
    return u % (1 << s) if s > 0 else 0


def induced_first_return(
    k: int,
    r: int,
    *,
    max_s: Optional[int] = None,
    node_budget: int = NODE_BUDGET,
) -> ClassResult:
    """
    Induced first-return map of T on class (k, r) via iterative explicit-stack DFS.

    Node state: (s, u, A, B, t, a)
      m ≡ u (mod 2^s)
      v(m) = (A m + B) / 2^t   (exact on the constrained class)
      t = Terras step count, a = odd-step count

    Caps: s ≤ k + 22 (default), node_budget nodes. Paths that hit caps become
    UNRESOLVED leaves; their 2-adic mass is always accounted.
    """
    if not (K_MIN <= k <= K_MAX):
        raise ValueError(f"k must be in {K_MIN}..{K_MAX}, got {k}")
    rp = r_prime(k, r)
    mod_k = 1 << k
    s_cap = k + S_EXTRA if max_s is None else max_s

    # Iterative explicit-stack search (no recursion). Mass-first: always expand
    # smallest s first so high-mass short returns resolve before the node budget
    # is spent on deep low-mass cones. Heap entries:
    #   (s, seq, u, A, B, t, a)
    heap: List[Tuple[int, int, int, int, int, int, int]] = []
    seq = 0

    def push(s: int, u: int, A: int, B: int, t: int, a: int) -> None:
        nonlocal seq
        seq += 1
        heapq.heappush(heap, (s, seq, u, A, B, t, a))

    # Initial: n = r' + 2^k m  ⇒  A=2^k, B=r', t=0, s=0, u=0
    push(0, 0, 1 << k, rp, 0, 0)

    branches: List[BranchFull] = []
    unresolved: List[UnresolvedLeaf] = []
    nodes = 0
    truncated = False

    while heap:
        if nodes >= node_budget:
            truncated = True
            for s, _seq, u, _A, _B, t, _a in heap:
                unresolved.append(
                    UnresolvedLeaf(
                        s=s, u=_u_norm(s, u), t=t, reason="node_budget"
                    )
                )
            heap.clear()
            break

        s, _seq, u, A, B, t, a = heapq.heappop(heap)
        nodes += 1
        _assert_ints(s, u, A, B, t, a)

        if s > s_cap:
            unresolved.append(
                UnresolvedLeaf(s=s, u=_u_norm(s, u), t=t, reason="max_s")
            )
            continue

        # Process this cone: chain decided steps in-place (no re-heap) until
        # we emit a branch, need a split, or hit a cap.
        while True:
            # --- Return decision (only for t ≥ 1) ---
            # P = 3^a · 2^{k+s−t}; return decidable iff s ≥ t
            if t >= 1:
                P, Q = _v_as_affine(A, B, t, s, u)
                if P % mod_k == 0:
                    if Q % mod_k == rp % mod_k:
                        if (Q - rp) % mod_k != 0:
                            raise AssertionError(
                                "return yes but Q − r' not 0 mod 2^k"
                            )
                        alpha = P // mod_k
                        beta = (Q - rp) // mod_k
                        _assert_ints(alpha, beta)
                        branches.append(
                            (s, _u_norm(s, u), alpha, beta, a, t)
                        )
                        break
                    # decided-no → take another Terras step below
                else:
                    # undecided return: need s ≥ t
                    if t > s_cap or s >= s_cap:
                        unresolved.append(
                            UnresolvedLeaf(
                                s=s, u=_u_norm(s, u), t=t, reason="max_s"
                            )
                        )
                        break
                    width = t - s
                    n_children = 1 << width
                    if n_children > max(2, node_budget - nodes):
                        unresolved.append(
                            UnresolvedLeaf(
                                s=s,
                                u=_u_norm(s, u),
                                t=t,
                                reason="node_budget",
                            )
                        )
                        break
                    base = _u_norm(s, u)
                    for j in range(n_children):
                        push(t, base + j * (1 << s), A, B, t, a)
                    break

            # --- Parity + apply one Terras step ---
            P, Q = _v_as_affine(A, B, t, s, u)
            if P % 2 == 0:
                parity = Q % 2
                s, u, A, B, t, a = _apply_terras_step(
                    s, u, A, B, t, a, parity
                )
                # chain continues in-place (same cone)
                continue
            # parity undecided → split one bit
            if s >= s_cap:
                unresolved.append(
                    UnresolvedLeaf(
                        s=s, u=_u_norm(s, u), t=t, reason="max_s"
                    )
                )
                break
            push(s + 1, u, A, B, t, a)
            push(s + 1, u + (1 << s), A, B, t, a)
            break

    # Unresolved 2-adic mass = Σ 2^{−s} over unresolved leaves (always)
    mass = Fraction(0)
    for leaf in unresolved:
        mass += Fraction(1, 1 << leaf.s)

    return ClassResult(
        k=k,
        r=r,
        r_prime=rp,
        branches=tuple(branches),
        unresolved=tuple(unresolved),
        unresolved_mass=mass,
        nodes_visited=nodes,
        max_s_cap=s_cap,
        truncated=truncated,
    )


# Back-compat aliases used by older test snippets
MAX_S = S_EXTRA  # note: actual per-class cap is k + S_EXTRA
MAX_STEPS = 10**9  # no separate step cap; s-cap + node budget govern


def mass_as_string(mass: Fraction) -> str:
    """Exact dyadic rational string for a mass Fraction."""
    if not isinstance(mass, Fraction):
        # legacy (num, exp) pair
        if isinstance(mass, tuple) and len(mass) == 2:
            num, exp = mass
            mass = Fraction(num, 1 << exp) if exp >= 0 else Fraction(num)
        else:
            raise TypeError(f"mass must be Fraction, got {type(mass)}")
    if mass == 0:
        return "0"
    # Prefer dyadic form n/2^e
    n, d = mass.numerator, mass.denominator
    # d should be a power of 2
    exp = 0
    dd = d
    while dd > 1 and dd % 2 == 0:
        dd //= 2
        exp += 1
    if dd != 1:
        return str(mass)  # non-dyadic fallback
    # fold factors of 2 out of numerator
    while n % 2 == 0 and exp > 0:
        n //= 2
        exp -= 1
    if exp == 0:
        return str(n)
    return f"{n}/2^{exp}"


def mass_to_float_proxy(mass: Fraction) -> float:
    """Reporting only; certificates stay exact."""
    return float(mass)


def simulate_first_return(
    n: int, k: int, r: int, max_steps: int = 10_000
) -> Tuple[int, int]:
    """
    Direct simulation: iterate T from n until first return to class (k, r).
    Returns (m_image, t) where return value = r' + 2^k * m_image, t = steps.
    """
    rp = r_prime(k, r)
    mod = 1 << k
    if n % mod != rp % mod:
        raise ValueError(f"n={n} not in class (k={k}, r={r})")
    x = n
    for t in range(1, max_steps + 1):
        x = terras(x)
        if x % mod == rp % mod:
            if (x - rp) % mod != 0:
                raise AssertionError("congruence but not divisible")
            return (x - rp) // mod, t
    raise RuntimeError(f"no return within {max_steps} steps for n={n}")


def predict_induced(result: ClassResult, m: int) -> Tuple[int, int]:
    """
    Using branch data, predict (m_image, t) for parameter m.
    Finds the unique branch whose domain contains m.
    """
    matches: List[Tuple[int, int, int, int]] = []
    for s, u, alpha, beta, a, t in result.branches:
        mod = 1 << s
        if m % mod == u % mod:
            m_prime = (m - u) // mod if s > 0 else m
            m_image = alpha * m_prime + beta
            matches.append((m_image, t, s, u))
    if not matches:
        for leaf in result.unresolved:
            mod = 1 << leaf.s
            if m % mod == leaf.u % mod:
                raise RuntimeError(
                    f"m={m} lands in unresolved leaf s={leaf.s} u={leaf.u} "
                    f"({leaf.reason})"
                )
        raise RuntimeError(
            f"m={m} matches no branch for class (k={result.k}, r={result.r})"
        )
    matches.sort(key=lambda x: -x[2])  # prefer larger s
    best = matches[0]
    for other in matches[1:]:
        if other[0] != best[0] or other[1] != best[1]:
            if other[2] == best[2]:
                raise AssertionError(
                    f"conflicting branches at same s for m={m}: {best} vs {other}"
                )
    return best[0], best[1]


def compute_all_classes(
    k_max: int,
    *,
    max_s: Optional[int] = None,
    node_budget: int = NODE_BUDGET,
    progress_every: int = 0,
    time_budget_sec: Optional[float] = None,
    deadline: Optional[float] = None,
) -> Tuple[Dict[Tuple[int, int], ClassResult], Dict[int, float], int]:
    """
    Compute induced maps for all classes k=1..k_max (k_max ≤ 5).

    Returns (results, per_k_times, achieved_k_max).
    If time would be exceeded before starting a new k, stops after the last
    fully completed k (never partial k).
    """
    if k_max > K_MAX:
        raise ValueError(f"k_max must be ≤ {K_MAX}, got {k_max}")
    out: Dict[Tuple[int, int], ClassResult] = {}
    per_k_times: Dict[int, float] = {}
    t0 = time.perf_counter()
    if deadline is None and time_budget_sec is not None:
        deadline = t0 + time_budget_sec
    achieved = 0

    for k in range(1, k_max + 1):
        if deadline is not None and time.perf_counter() >= deadline:
            break
        # Estimate: only skip starting k if already past deadline
        tk = time.perf_counter()
        for r in range(1 << k):
            out[(k, r)] = induced_first_return(
                k, r, max_s=max_s, node_budget=node_budget
            )
            if progress_every and (r + 1) % progress_every == 0:
                print(f"  k={k} r={r + 1}/{1 << k}", flush=True)
        per_k_times[k] = time.perf_counter() - tk
        achieved = k
        # After finishing k, if next would clearly bust and we're at k>=4, stop
        if deadline is not None and k < k_max:
            elapsed = time.perf_counter() - t0
            remaining = deadline - time.perf_counter()
            # crude estimate: next k costs ~ 3x this k (class count doubles+)
            if remaining < per_k_times[k] * 2.5 and k >= 4:
                break

    return out, per_k_times, achieved


def per_k_stats(
    results: Dict[Tuple[int, int], ClassResult], k: int
) -> dict:
    """Aggregate stats for a single k."""
    classes = [results[(k, r)] for r in range(1 << k) if (k, r) in results]
    if not classes:
        return {"k": k, "class_count": 0}
    branch_counts = [len(c.branches) for c in classes]
    total_mass = sum((c.unresolved_mass for c in classes), Fraction(0))
    max_mass = max((c.unresolved_mass for c in classes), default=Fraction(0))
    min_resolved = min((c.resolved_mass() for c in classes), default=Fraction(0))
    return {
        "k": k,
        "class_count": len(classes),
        "mean_branch_count": sum(branch_counts) / len(branch_counts),
        "max_branch_count": max(branch_counts),
        "min_branch_count": min(branch_counts),
        "total_unresolved_mass": total_mass,
        "max_class_unresolved_mass": max_mass,
        "min_resolved_mass": min_resolved,
        "classes_with_unresolved": sum(1 for c in classes if c.unresolved),
        "branch_counts": branch_counts,
        "mean_nodes": sum(c.nodes_visited for c in classes) / len(classes),
        "max_nodes": max(c.nodes_visited for c in classes),
    }


def _branch_diff_count(
    can_a: Tuple[BranchCanon, ...], can_b: Tuple[BranchCanon, ...]
) -> int:
    """Multiset symmetric-difference size of two canonical branch tuples."""
    ca = Counter(can_a)
    cb = Counter(can_b)
    diff = 0
    for key in set(ca) | set(cb):
        diff += abs(ca[key] - cb[key])
    return diff


def collapse_search(
    results: Dict[Tuple[int, int], ClassResult],
    k_max: int,
    *,
    mass_threshold: Fraction = MASS_THRESHOLD,
) -> dict:
    """
    Truncation-aware collapse search.

    Canonical form of a class = sorted resolved branches + unresolved mass
    (mass stored separately; forms compared on resolved branches only).

    COLLAPSE WITNESS: different k, identical resolved canonical forms,
    both unresolved masses < 2^{-10}.

    SHORTLIST: different k, equal signature (multiset of (s,a,t)), unequal
    forms; top 20 by fewest differing branches. No affine-conjugacy solving.
    """
    # Eligible for collapse: mass < threshold
    by_can: Dict[Tuple[BranchCanon, ...], List[Tuple[int, int, Fraction]]] = (
        defaultdict(list)
    )
    by_sig: Dict[
        Tuple[SignatureItem, ...],
        List[Tuple[int, int, Tuple[BranchCanon, ...]]],
    ] = defaultdict(list)

    for k in range(1, k_max + 1):
        for r in range(1 << k):
            key = (k, r)
            if key not in results:
                continue
            cr = results[key]
            can = cr.canonical()
            sig = cr.signature()
            by_sig[sig].append((k, r, can))
            if cr.unresolved_mass < mass_threshold:
                by_can[can].append((k, r, cr.unresolved_mass))

    collapses: List[dict] = []
    for can, members in by_can.items():
        # cross-k pairs only
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                k1, r1, m1 = members[i]
                k2, r2, m2 = members[j]
                if k1 != k2:
                    collapses.append(
                        {
                            "class1": (k1, r1),
                            "class2": (k2, r2),
                            "canonical": can,
                            "mass1": m1,
                            "mass2": m2,
                            "signature": results[(k1, r1)].signature(),
                        }
                    )

    seen_c = set()
    unique_collapses = []
    for c in collapses:
        key = tuple(sorted([c["class1"], c["class2"]]))
        if key not in seen_c:
            seen_c.add(key)
            unique_collapses.append(c)

    shortlist_candidates: List[dict] = []
    for sig, members in by_sig.items():
        if len(members) < 2:
            continue
        # group by canonical
        groups: Dict[Tuple[BranchCanon, ...], List[Tuple[int, int]]] = (
            defaultdict(list)
        )
        for k, r, can in members:
            groups[can].append((k, r))
        can_items = list(groups.items())
        for i in range(len(can_items)):
            can_a, pairs_a = can_items[i]
            for j in range(i + 1, len(can_items)):
                can_b, pairs_b = can_items[j]
                diff = _branch_diff_count(can_a, can_b)
                for k1, r1 in pairs_a:
                    for k2, r2 in pairs_b:
                        if k1 != k2:
                            shortlist_candidates.append(
                                {
                                    "class1": (k1, r1),
                                    "class2": (k2, r2),
                                    "signature": sig,
                                    "diff_branches": diff,
                                    "n_branches_1": len(can_a),
                                    "n_branches_2": len(can_b),
                                }
                            )

    shortlist_candidates.sort(
        key=lambda d: (
            d["diff_branches"],
            d["n_branches_1"] + d["n_branches_2"],
        )
    )
    seen_s = set()
    shortlist = []
    for s in shortlist_candidates:
        key = tuple(sorted([s["class1"], s["class2"]]))
        if key in seen_s or key in seen_c:
            continue
        seen_s.add(key)
        shortlist.append(s)
        if len(shortlist) >= 20:
            break

    n_complete = sum(
        1
        for k in range(1, k_max + 1)
        for r in range(1 << k)
        if (k, r) in results and results[(k, r)].unresolved_mass == 0
    )

    return {
        "collapses": unique_collapses,
        "shortlist": shortlist,
        "n_signatures": len(by_sig),
        "n_classes_complete": n_complete,
        "mass_threshold": mass_threshold,
    }


def run_fold_search(
    k_max: int = K_MAX,
    *,
    time_budget_sec: float = GLOBAL_TIME_BUDGET_SEC,
) -> dict:
    """
    Full search for k=1..k_max (≤5) with global time budget.
    Prefers finishing k≤4 fully if k=5 would bust the budget.
    """
    if k_max > K_MAX:
        k_max = K_MAX
    t0 = time.perf_counter()
    deadline = t0 + time_budget_sec
    results, per_k_times, achieved = compute_all_classes(
        k_max, deadline=deadline
    )
    stats = {k: per_k_stats(results, k) for k in range(1, achieved + 1)}
    search = collapse_search(results, achieved)
    total_time = time.perf_counter() - t0

    max_unres = Fraction(0)
    min_resolved = Fraction(1)
    for k in range(1, achieved + 1):
        for r in range(1 << k):
            if (k, r) not in results:
                continue
            cr = results[(k, r)]
            if cr.unresolved_mass > max_unres:
                max_unres = cr.unresolved_mass
            rm = cr.resolved_mass()
            if rm < min_resolved:
                min_resolved = rm

    note = ""
    if achieved < k_max:
        note = (
            f"Finished k≤{achieved} fully; stopped before k={achieved + 1}..{k_max} "
            f"to respect the {time_budget_sec / 60:.0f}-minute global budget."
        )
    else:
        note = f"Completed full search for k=1..{achieved}."

    return {
        "k_max": achieved,
        "results": results,
        "stats": stats,
        "search": search,
        "per_k_times": per_k_times,
        "total_time": total_time,
        "max_unresolved_mass": max_unres,
        "min_resolved_mass": min_resolved,
        "note": note,
    }


def format_canonical(can: Tuple[BranchCanon, ...]) -> str:
    lines = []
    for s, u, alpha, beta in can:
        lines.append(f"  m≡{u} (mod 2^{s}):  m' ↦ {alpha}*m' + {beta}")
    return "\n".join(lines) if lines else "  (empty)"


def write_report(out: dict, path: str) -> None:
    """Write F2_REPORT.md from a run_fold_search result."""
    k_max = out["k_max"]
    lines: List[str] = []
    lines.append("# F2 Report — Induced First-Return Maps + Collapse Search")
    lines.append("")
    lines.append("## Budgets")
    lines.append("")
    lines.append(f"- k = 1..{K_MAX} (attempted up to {k_max})")
    lines.append(f"- s ≤ k + {S_EXTRA} per class")
    lines.append(f"- node budget = {NODE_BUDGET:,} per class")
    lines.append(f"- global runtime cap = {GLOBAL_TIME_BUDGET_SEC // 60} minutes")
    lines.append(f"- collapse mass threshold = 2^{{-10}} = {MASS_THRESHOLD}")
    lines.append("")
    lines.append(f"**Note:** {out.get('note', '')}")
    lines.append("")
    lines.append(f"**Total runtime:** {out['total_time']:.3f} s")
    lines.append("")
    lines.append("## Per-k statistics")
    lines.append("")
    lines.append(
        "| k | classes | mean branches | max branches | min branches | "
        "classes w/ unres | max unres mass | min resolved mass | time (s) |"
    )
    lines.append(
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    )
    for k in range(1, k_max + 1):
        st = out["stats"][k]
        tk = out["per_k_times"].get(k, 0.0)
        lines.append(
            f"| {k} | {st['class_count']} | {st['mean_branch_count']:.2f} | "
            f"{st['max_branch_count']} | {st['min_branch_count']} | "
            f"{st['classes_with_unresolved']} | "
            f"{mass_as_string(st['max_class_unresolved_mass'])} | "
            f"{mass_as_string(st['min_resolved_mass'])} | {tk:.3f} |"
        )
    lines.append("")
    lines.append("## Branch-count vs k (growth curve)")
    lines.append("")
    lines.append("| k | mean | max | max/mean |")
    lines.append("|---:|---:|---:|---:|")
    for k in range(1, k_max + 1):
        st = out["stats"][k]
        mean = st["mean_branch_count"]
        mx = st["max_branch_count"]
        ratio = mx / mean if mean else 0.0
        lines.append(f"| {k} | {mean:.2f} | {mx} | {ratio:.2f} |")
    lines.append("")
    lines.append("Per-class branch counts:")
    lines.append("")
    for k in range(1, k_max + 1):
        bc = out["stats"][k]["branch_counts"]
        lines.append(f"- k={k}: {bc}")
    lines.append("")
    lines.append("## Unresolved mass")
    lines.append("")
    lines.append(
        f"- Global max class unresolved mass: "
        f"{mass_as_string(out['max_unresolved_mass'])}"
    )
    lines.append(
        f"- Global min resolved mass: "
        f"{mass_as_string(out['min_resolved_mass'])}"
    )
    lines.append("")
    # detail classes with unresolved
    any_unres = False
    for k in range(1, k_max + 1):
        for r in range(1 << k):
            cr = out["results"][(k, r)]
            if cr.unresolved_mass > 0:
                if not any_unres:
                    lines.append("Classes with positive unresolved mass:")
                    lines.append("")
                    any_unres = True
                lines.append(
                    f"- ({k},{r}): mass={mass_as_string(cr.unresolved_mass)}, "
                    f"leaves={len(cr.unresolved)}, branches={len(cr.branches)}, "
                    f"nodes={cr.nodes_visited}, truncated={cr.truncated}"
                )
    if not any_unres:
        lines.append("No class has positive unresolved mass at these caps.")
    lines.append("")
    lines.append("## Collapse witnesses")
    lines.append("")
    sc = out["search"]
    if sc["collapses"]:
        lines.append(
            f"Found **{len(sc['collapses'])}** collapse pair(s) "
            f"(identical resolved form, both masses < 2^{{-10}}):"
        )
        lines.append("")
        for c in sc["collapses"]:
            lines.append(
                f"- {c['class1']} ↔ {c['class2']} "
                f"(masses {mass_as_string(c['mass1'])}, "
                f"{mass_as_string(c['mass2'])})"
            )
            lines.append("  Shared form:")
            lines.append(format_canonical(c["canonical"]))
            lines.append("")
    else:
        thr = mass_as_string(out["min_resolved_mass"])
        lines.append(
            f"**NO COLLAPSE at k ≤ {k_max}** "
            f"(min resolved mass = {thr} everywhere among fully covered classes; "
            f"no different-k pair shares an identical resolved canonical form "
            f"with both unresolved masses < 2^{{-10}})."
        )
        lines.append("")
    lines.append("## Shortlist (equal signature, unequal form, different k)")
    lines.append("")
    if sc["shortlist"]:
        lines.append(
            f"Top {len(sc['shortlist'])} pairs by fewest differing branches "
            "(no affine-conjugacy solving — FABLE review):"
        )
        lines.append("")
        for i, s in enumerate(sc["shortlist"], 1):
            lines.append(
                f"{i}. {s['class1']} ↔ {s['class2']}: "
                f"diff_branches={s['diff_branches']}, "
                f"n_branches=({s['n_branches_1']},{s['n_branches_2']})"
            )
    else:
        lines.append("No shortlist pairs (no equal-signature unequal-form cross-k pairs).")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    if sc["collapses"]:
        pairs = ", ".join(
            f"{c['class1']}↔{c['class2']}" for c in sc["collapses"]
        )
        lines.append(f"COLLAPSE FOUND: {pairs}")
    else:
        lines.append(
            f"NO COLLAPSE at k ≤ {k_max}, min resolved mass = "
            f"{mass_as_string(out['min_resolved_mass'])}"
        )
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    print("F2 fold operator — run k=1..5 (20 min budget)")
    out = run_fold_search(K_MAX, time_budget_sec=GLOBAL_TIME_BUDGET_SEC)
    print(f"k_max={out['k_max']} total_time={out['total_time']:.3f}s")
    print(out.get("note", ""))
    for k, t in sorted(out["per_k_times"].items()):
        st = out["stats"][k]
        print(
            f"k={k}: time={t:.3f}s classes={st['class_count']} "
            f"mean_branches={st['mean_branch_count']:.2f} "
            f"max_branches={st['max_branch_count']} "
            f"unres_mass_max={mass_as_string(st['max_class_unresolved_mass'])}"
        )
    sc = out["search"]
    print(f"collapses={len(sc['collapses'])} shortlist={len(sc['shortlist'])}")
    if sc["collapses"]:
        for c in sc["collapses"][:10]:
            print(" COLLAPSE", c["class1"], c["class2"])
        print(
            "COLLAPSE FOUND:",
            ", ".join(f"{c['class1']}↔{c['class2']}" for c in sc["collapses"]),
        )
    else:
        print(
            f"NO COLLAPSE at k ≤ {out['k_max']}, min resolved mass = "
            f"{mass_as_string(out['min_resolved_mass'])}"
        )
    import os

    report_path = os.path.join(os.path.dirname(__file__), "F2_REPORT.md")
    write_report(out, report_path)
    print(f"Wrote {report_path}")
