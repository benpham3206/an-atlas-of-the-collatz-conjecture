"""
F4 — Symbolic-feature regression vs mod-2^B baseline (Terras stopping label).

Exhaustive enumeration of a small arithmetic feature grammar. No neural nets.
Python 3 stdlib only. Imports Terras map from frozen F1.

Protocol
--------
- Domain: n in [2, N) with N = 2**EXP (default EXP=20).
- Label y(n) = 1 iff sigma(n) > 4, where sigma is the Terras stopping time
  (least j >= 1 with T^j(n) < n).
- Split: train = n < N//2, test = n in [N//2, N).
- Baseline (B in {8,10,12}): majority label per residue n mod 2^B on train.
- Features: singles + pairs with joint key space <= 2^12.
- Budget of a feature set = ceil(log2(product of value-space sizes)).
  Matched baseline uses the smallest B in {8,10,12} with B >= budget
  (if budget > 12, no baseline match / no win possible under the rule).
- Win: test accuracy exceeds matched baseline by >= 1.0 absolute percentage points.

Also: excursion / sustained odd-step density records (ground characterization).
"""

from __future__ import annotations

import math
import os
import sys
from collections import Counter, defaultdict
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from f1_word_calculus import terras  # noqa: E402

# ---------------------------------------------------------------------------
# Constants / domain
# ---------------------------------------------------------------------------

DEFAULT_EXP = 20
LABEL_THRESHOLD = 4  # y = [sigma > 4]
BASELINE_BUDGETS = (8, 10, 12)
MAX_JOINT_SPACE = 1 << 12  # 4096
WIN_MARGIN_PP = 1.0  # absolute percentage points on test accuracy
# log(2)/log(3) threshold for divergent-orbit density lower bound
DENSITY_NUM, DENSITY_DEN = 2, 3  # compare a/L >= log2/log3 via cross-log
# For integer-safe threshold checks we use float only in reporting; comparisons
# use a * math.log(3) >= L * math.log(2) when needed, or exact rational proxy.

FeatureFn = Callable[[int], int]
SpaceSize = int


# ---------------------------------------------------------------------------
# Stopping time & labels
# ---------------------------------------------------------------------------

def sigma(n: int) -> int:
    """Terras stopping time: least j >= 1 with T^j(n) < n."""
    if n <= 1:
        raise ValueError(f"sigma requires n >= 2, got {n}")
    x = n
    j = 0
    while True:
        x = terras(x)
        j += 1
        if x < n:
            return j


def sigma_direct_simulation(n: int) -> int:
    """Same definition, explicit loop (for test cross-check)."""
    if n <= 1:
        raise ValueError(f"sigma requires n >= 2, got {n}")
    x = n
    j = 0
    while True:
        if x % 2 == 0:
            x = x // 2
        else:
            x = (3 * x + 1) // 2
        j += 1
        if x < n:
            return j


def label_long_glide(n: int, threshold: int = LABEL_THRESHOLD) -> int:
    """Binary label [sigma(n) > threshold]."""
    return 1 if sigma(n) > threshold else 0


# ---------------------------------------------------------------------------
# Primitive integer features (no floats in values)
# ---------------------------------------------------------------------------

def popcount(n: int) -> int:
    return n.bit_count()


def bit_length_feat(n: int) -> int:
    return n.bit_length()


def nu2(m: int) -> int:
    """2-adic valuation of positive m; nu2(odd)=0. m must be > 0."""
    if m <= 0:
        raise ValueError(f"nu2 requires positive m, got {m}")
    return (m & -m).bit_length() - 1


def nu2_n_plus_1(n: int) -> int:
    return nu2(n + 1)


def nu2_3n_plus_1(n: int) -> int:
    return nu2(3 * n + 1)


def longest_run_ones(n: int) -> int:
    """Longest consecutive run of 1-bits in binary(n)."""
    best = 0
    cur = 0
    x = n
    while x:
        if x & 1:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
        x >>= 1
    return best


def longest_run_zeros(n: int) -> int:
    """
    Longest consecutive run of 0-bits in binary(n), ignoring leading zeros
    (i.e. only interior/trailing zeros within the bit_length window).
    """
    if n <= 0:
        return 0
    # Work within bit_length bits (no leading zeros by definition of bit_length).
    width = n.bit_length()
    best = 0
    cur = 0
    for i in range(width):
        if (n >> i) & 1:
            cur = 0
        else:
            cur += 1
            if cur > best:
                best = cur
    return best


def popcount_3n_plus_1(n: int) -> int:
    return popcount(3 * n + 1)


def popcount_parity(n: int) -> int:
    return popcount(n) & 1


def make_mod(m: int) -> FeatureFn:
    def _mod(n: int) -> int:
        return n % m

    _mod.__name__ = f"mod_{m}"
    return _mod


# ---------------------------------------------------------------------------
# Value-space sizes (for budget accounting)
# ---------------------------------------------------------------------------

def value_space_sizes(N: int) -> Dict[str, int]:
    """
    Cardinality of each feature's value space on domain n in [2, N).

    Sizes are exact upper bounds on image cardinality (hand-checkable).
    """
    # Max bit length of n < N is (N-1).bit_length()
    max_bits = (N - 1).bit_length()
    # popcount in {1, ..., max_bits} ⊆ {0, ..., max_bits} → max_bits+1
    # bit_length in {2, ..., max_bits} → max_bits - 1 values for N>=4
    # nu2(n+1): n+1 in [3, N], valuation in {0, ..., floor(log2(N))} if N power of 2
    #   when N=2^e, n+1 <= 2^e → nu2 <= e → values 0..e → e+1
    e = max_bits  # for N=2^e, max_bits = e
    # nu2(3n+1): 3n+1 < 3N; valuation <= floor(log2(3N-1))
    max_nu2_3n1 = (3 * N - 1).bit_length()  # generous: 0..that inclusive → +1
    sizes: Dict[str, int] = {
        "popcount": max_bits + 1,  # 0..max_bits
        "bit_length": max_bits,  # 1..max_bits (covers 2..max_bits)
        "nu2_np1": e + 1,  # 0..e for N=2^e
        "nu2_3n1": max_nu2_3n1 + 1,
        "longest_ones": max_bits + 1,  # 0..max_bits
        "longest_zeros": max_bits,  # 0..max_bits-1 typically; bound max_bits
        "popcount_3n1": (3 * N - 1).bit_length() + 1,  # popcount bound
        "popcount_mod2": 2,
    }
    for i in range(1, 7):
        sizes[f"mod_3^{i}"] = 3 ** i
    for m in (5, 7, 11, 13):
        sizes[f"mod_{m}"] = m
    return sizes


def budget_of_spaces(sizes: Sequence[int]) -> int:
    """ceil(log2(product of sizes)). product >= 1."""
    if not sizes:
        return 0
    prod = 1
    for s in sizes:
        if s < 1:
            raise ValueError(f"space size must be >= 1, got {s}")
        prod *= s
    # ceil(log2(prod)) for prod >= 1
    if prod <= 1:
        return 0
    return (prod - 1).bit_length()  # floor(log2(prod-1))+1 = ceil(log2(prod)) for prod>=2


def matched_baseline_B(budget: int, available: Sequence[int] = BASELINE_BUDGETS) -> Optional[int]:
    """Smallest B in available with B >= budget; None if none."""
    for B in sorted(available):
        if B >= budget:
            return B
    return None


# ---------------------------------------------------------------------------
# Feature registry
# ---------------------------------------------------------------------------

def build_feature_registry(N: int) -> List[Tuple[str, FeatureFn, int]]:
    """
    Return list of (name, fn, space_size) for all single features in the grammar.
    Order is deterministic.
    """
    sizes = value_space_sizes(N)
    specs: List[Tuple[str, FeatureFn]] = [
        ("popcount", popcount),
        ("bit_length", bit_length_feat),
        ("nu2_np1", nu2_n_plus_1),
        ("nu2_3n1", nu2_3n_plus_1),
        ("longest_ones", longest_run_ones),
        ("longest_zeros", longest_run_zeros),
    ]
    for i in range(1, 7):
        m = 3 ** i
        specs.append((f"mod_3^{i}", make_mod(m)))
    for m in (5, 7, 11, 13):
        specs.append((f"mod_{m}", make_mod(m)))
    specs.append(("popcount_3n1", popcount_3n_plus_1))
    specs.append(("popcount_mod2", popcount_parity))

    out: List[Tuple[str, FeatureFn, int]] = []
    for name, fn in specs:
        out.append((name, fn, sizes[name]))
    return out


def enumerate_feature_sets(
    registry: List[Tuple[str, FeatureFn, int]],
    max_joint: int = MAX_JOINT_SPACE,
) -> List[Tuple[str, Callable[[int], Tuple[int, ...]], int, int]]:
    """
    Singles + pairs with product of spaces <= max_joint.

    Returns list of (name, key_fn, space_product, budget).
    """
    sets: List[Tuple[str, Callable[[int], Tuple[int, ...]], int, int]] = []

    for name, fn, sp in registry:
        prod = sp
        if prod > max_joint:
            # Still include singles even if > 2^12 (packet: pairs filtered;
            # singles like mod 3^6 = 729 are fine; none exceed 4096 alone except none)
            pass
        bud = budget_of_spaces([sp])

        def _make_single(f: FeatureFn = fn) -> Callable[[int], Tuple[int, ...]]:
            return lambda n: (f(n),)

        sets.append((name, _make_single(), prod, bud))

    nreg = len(registry)
    for i in range(nreg):
        for j in range(i + 1, nreg):
            n1, f1, s1 = registry[i]
            n2, f2, s2 = registry[j]
            prod = s1 * s2
            if prod > max_joint:
                continue
            bud = budget_of_spaces([s1, s2])

            def _make_pair(
                a: FeatureFn = f1, b: FeatureFn = f2
            ) -> Callable[[int], Tuple[int, ...]]:
                return lambda n: (a(n), b(n))

            sets.append((f"{n1}+{n2}", _make_pair(), prod, bud))

    return sets


# ---------------------------------------------------------------------------
# Majority-lookup predictors
# ---------------------------------------------------------------------------

def fit_majority_table(
    keys: Iterable, labels: Iterable[int]
) -> Dict:
    """
    Majority label per key on training data.
    Ties: prefer label 0 (conservative — not long-glide).
    Missing keys at predict time → 0.
    """
    counts: Dict = defaultdict(lambda: [0, 0])
    for k, y in zip(keys, labels):
        counts[k][y] += 1
    table: Dict = {}
    for k, (c0, c1) in counts.items():
        table[k] = 1 if c1 > c0 else 0
    return table


def predict_table(table: Dict, keys: Iterable) -> List[int]:
    return [table.get(k, 0) for k in keys]


def accuracy(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    if not y_true:
        return 0.0
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return 100.0 * correct / len(y_true)


# ---------------------------------------------------------------------------
# Data prep
# ---------------------------------------------------------------------------

def compute_labels(N: int) -> List[int]:
    """
    labels[n] for n in 0..N-1; labels[0]=labels[1]=0 unused.
    y = [sigma(n) > 4].
    """
    labels = [0] * N
    for n in range(2, N):
        labels[n] = 1 if sigma(n) > LABEL_THRESHOLD else 0
    return labels


def train_test_ranges(N: int) -> Tuple[range, range]:
    half = N // 2
    return range(2, half), range(half, N)


# ---------------------------------------------------------------------------
# Regression experiment
# ---------------------------------------------------------------------------

LeaderRow = Dict  # name, budget, train_acc, test_acc, kind, ...


def run_baselines(
    labels: Sequence[int], train: range, test: range, budgets: Sequence[int] = BASELINE_BUDGETS
) -> Dict[int, LeaderRow]:
    y_train = [labels[n] for n in train]
    y_test = [labels[n] for n in test]
    out: Dict[int, LeaderRow] = {}
    for B in budgets:
        mod = 1 << B
        keys_tr = [n % mod for n in train]
        keys_te = [n % mod for n in test]
        table = fit_majority_table(keys_tr, y_train)
        pred_tr = predict_table(table, keys_tr)
        pred_te = predict_table(table, keys_te)
        out[B] = {
            "name": f"baseline_mod_2^{B}",
            "budget": B,
            "space": mod,
            "train_acc": accuracy(y_train, pred_tr),
            "test_acc": accuracy(y_test, pred_te),
            "kind": "baseline",
            "matched_B": B,
            "margin_pp": 0.0,
            "win": False,
        }
    return out


def run_feature_sets(
    labels: Sequence[int],
    train: range,
    test: range,
    feature_sets: List[Tuple[str, Callable[[int], Tuple[int, ...]], int, int]],
    baselines: Dict[int, LeaderRow],
) -> List[LeaderRow]:
    y_train = [labels[n] for n in train]
    y_test = [labels[n] for n in test]
    rows: List[LeaderRow] = []

    for name, key_fn, prod, bud in feature_sets:
        keys_tr = [key_fn(n) for n in train]
        keys_te = [key_fn(n) for n in test]
        table = fit_majority_table(keys_tr, y_train)
        pred_tr = predict_table(table, keys_tr)
        pred_te = predict_table(table, keys_te)
        tr_acc = accuracy(y_train, pred_tr)
        te_acc = accuracy(y_test, pred_te)
        mB = matched_baseline_B(bud)
        margin = 0.0
        win = False
        base_acc = None
        if mB is not None and mB in baselines:
            base_acc = baselines[mB]["test_acc"]
            margin = te_acc - base_acc
            win = margin >= WIN_MARGIN_PP
        rows.append(
            {
                "name": name,
                "budget": bud,
                "space": prod,
                "train_acc": tr_acc,
                "test_acc": te_acc,
                "kind": "feature",
                "matched_B": mB,
                "baseline_test_acc": base_acc,
                "margin_pp": margin,
                "win": win,
            }
        )
    return rows


def leaderboard(
    feature_rows: List[LeaderRow],
    baselines: Dict[int, LeaderRow],
    top_k: int = 20,
) -> List[LeaderRow]:
    """
    Full leaderboard: feature rows sorted by test_acc desc, with baseline rows
    spliced inline (baselines always present for reference, not counting against top_k
    of features — packet: top 20 with baseline row inline).

    Implementation: sort features by test_acc; take top_k; append all baselines;
    re-sort by test_acc so baselines sit inline by score.
    """
    feats = sorted(feature_rows, key=lambda r: (-r["test_acc"], r["name"]))
    top = feats[:top_k]
    board = top + list(baselines.values())
    board.sort(key=lambda r: (-r["test_acc"], 0 if r["kind"] == "baseline" else 1, r["name"]))
    return board


# ---------------------------------------------------------------------------
# Excursion / sustained density records
# ---------------------------------------------------------------------------

def odd_step_density_scan(
    n: int, min_L: int = 20
) -> Tuple[float, int, int, Optional[int]]:
    """
    Walk Terras orbit of n until reaching the {1,2} cycle (x becomes 1).

    Returns (max_density, L_at_max, a_at_max, max_L_above_threshold)
    where density = a/L for L >= min_L, a = # odd Terras steps in first L steps.
    max_L_above_threshold = max L >= min_L with a/L >= log2/log3, or None.
    """
    # Compare a/L >= ln2/ln3  iff  a * ln3 >= L * ln2
    ln2 = math.log(2.0)
    ln3 = math.log(3.0)

    x = n
    a = 0
    L = 0
    best_d = -1.0
    best_L = 0
    best_a = 0
    max_L_thr: Optional[int] = None
    # Safety cap: total stopping times for n < 2^20 are < 400 Terras steps
    # to 1 (F1 report: total_max=329). Use generous cap.
    cap = 10_000
    seen_one = False
    while L < cap:
        odd = x & 1
        x = terras(x)
        L += 1
        a += odd
        if L >= min_L:
            d = a / L
            if d > best_d:
                best_d = d
                best_L = L
                best_a = a
            if a * ln3 >= L * ln2:
                max_L_thr = L
        if x == 1:
            seen_one = True
            # continue a few more steps through the cycle? Prefixes of the
            # transient+cycle; once on cycle density → 1/2. Stop at first hit of 1.
            break
    if not seen_one and best_L == 0:
        # never reached min_L
        return 0.0, 0, 0, None
    return best_d, best_L, best_a, max_L_thr


def excursion_records(
    N: int, min_L: int = 20, top_k: int = 10
) -> Tuple[List[Tuple[int, int, int, float]], int]:
    """
    For n in [2, N): per-n max prefix density a/L (L >= min_L).

    Returns (top_k list of (n, L, a, a/L) by density desc, global_max_L_at_threshold).
    global_max_L_at_threshold = max over n of max L with a/L >= log2/log3.
    """
    records: List[Tuple[int, int, int, float]] = []
    global_max_L = 0

    for n in range(2, N):
        best_d, best_L, best_a, max_L_thr = odd_step_density_scan(n, min_L=min_L)
        if best_L >= min_L:
            records.append((n, best_L, best_a, best_d))
        if max_L_thr is not None and max_L_thr > global_max_L:
            global_max_L = max_L_thr

    records.sort(key=lambda t: (-t[3], t[0]))
    return records[:top_k], global_max_L


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

def run_experiment(N: int = 1 << DEFAULT_EXP) -> Dict:
    """
    Run full F4 experiment. Returns a results dict (JSON-serializable primitives).
    """
    train, test = train_test_ranges(N)
    labels = compute_labels(N)
    baselines = run_baselines(labels, train, test)
    registry = build_feature_registry(N)
    fsets = enumerate_feature_sets(registry)
    feat_rows = run_feature_sets(labels, train, test, fsets, baselines)
    board = leaderboard(feat_rows, baselines, top_k=20)

    wins = [r for r in feat_rows if r["win"]]
    if wins:
        wins.sort(key=lambda r: (-r["margin_pp"], r["name"]))
        best = wins[0]
        verdict = (
            f"WIN: {best['name']} +{best['margin_pp']:.1f} pts over budget-"
            f"{best['matched_B']} baseline"
        )
    else:
        verdict = "NO WIN vs mod-2^B baseline"

    top_exc, max_L_thr = excursion_records(N)

    n_train = len(train)
    n_test = len(test)
    base_rate_train = 100.0 * sum(labels[n] for n in train) / n_train
    base_rate_test = 100.0 * sum(labels[n] for n in test) / n_test

    return {
        "N": N,
        "exp": (N).bit_length() - 1 if (N & (N - 1)) == 0 else None,
        "n_train": n_train,
        "n_test": n_test,
        "base_rate_train": base_rate_train,
        "base_rate_test": base_rate_test,
        "n_feature_sets": len(fsets),
        "n_singles": len(registry),
        "baselines": {str(B): baselines[B] for B in baselines},
        "leaderboard": board,
        "all_features": sorted(feat_rows, key=lambda r: (-r["test_acc"], r["name"])),
        "wins": wins,
        "verdict": verdict,
        "excursion_top": [
            {"n": n, "L": L, "a": a, "density": d} for n, L, a, d in top_exc
        ],
        "max_L_density_ge_log2_log3": max_L_thr,
        "density_threshold": math.log(2) / math.log(3),
    }


def format_leaderboard(board: List[LeaderRow], baselines: Optional[Dict] = None) -> str:
    lines = [
        f"{'rank':>4}  {'name':<40}  {'bud':>3}  {'train%':>8}  {'test%':>8}  "
        f"{'mB':>3}  {'base%':>8}  {'Δpp':>7}  {'win':>3}"
    ]
    lines.append("-" * len(lines[0]))
    for i, r in enumerate(board, 1):
        mB = r.get("matched_B")
        base = r.get("baseline_test_acc")
        if r["kind"] == "baseline":
            base_s = "—"
            mB_s = str(r["budget"])
            d_s = "—"
            w_s = "—"
            tag = " [BASE]"
        else:
            base_s = f"{base:.4f}" if base is not None else "n/a"
            mB_s = str(mB) if mB is not None else "—"
            d_s = f"{r['margin_pp']:+.4f}" if base is not None else "—"
            w_s = "YES" if r["win"] else "no"
            tag = ""
        lines.append(
            f"{i:4d}  {r['name'] + tag:<40}  {r['budget']:3d}  "
            f"{r['train_acc']:8.4f}  {r['test_acc']:8.4f}  "
            f"{mB_s:>3}  {base_s:>8}  {d_s:>7}  {w_s:>3}"
        )
    return "\n".join(lines)


def format_excursion(top: List[Dict], max_L: int, thr: float) -> str:
    lines = [
        f"Density threshold log2/log3 ≈ {thr:.6f}",
        f"Max L with a/L >= threshold for some n < N: {max_L}",
        "",
        f"{'rank':>4}  {'n':>12}  {'L':>6}  {'a':>6}  {'a/L':>10}",
        "-" * 48,
    ]
    for i, rec in enumerate(top, 1):
        lines.append(
            f"{i:4d}  {rec['n']:12d}  {rec['L']:6d}  {rec['a']:6d}  {rec['density']:10.6f}"
        )
    return "\n".join(lines)


def write_report(results: Dict, path: str) -> None:
    N = results["N"]
    lines: List[str] = []
    lines.append("# F4 Report — Symbolic-feature regression vs mod-2^B baseline")
    lines.append("")
    lines.append("## Protocol")
    lines.append("")
    lines.append(f"- Domain: `n ∈ [2, {N})` (N = {N}).")
    lines.append(
        f"- Label: `y(n) = [σ(n) > {LABEL_THRESHOLD}]` where `σ` is Terras stopping time "
        "(least `j ≥ 1` with `T^j(n) < n`)."
    )
    lines.append(
        f"- Split: train = `n < {N // 2}` ({results['n_train']} points), "
        f"test = `n ∈ [{N // 2}, {N})` ({results['n_test']} points)."
    )
    lines.append(
        f"- Base rate P(y=1): train {results['base_rate_train']:.4f}%, "
        f"test {results['base_rate_test']:.4f}%."
    )
    lines.append(
        f"- Feature sets enumerated: {results['n_feature_sets']} "
        f"({results['n_singles']} singles + pairs with joint space ≤ 2^12)."
    )
    lines.append(
        "- Predictor: majority label per feature key on train; default 0 on unseen keys; "
        "ties → 0."
    )
    lines.append(
        f"- Win rule: test accuracy ≥ matched baseline + {WIN_MARGIN_PP:.1f} absolute pp, "
        "where matched baseline is the smallest B ∈ {8,10,12} with B ≥ feature budget "
        "`⌈log2(∏ space sizes)⌉`."
    )
    lines.append("")
    lines.append("## Null hypothesis")
    lines.append("")
    lines.append(
        "By Terras (1976), the first `k` Terras steps of `n` are exactly determined by "
        "`n mod 2^k` (verified in F1). Any feature that only repackages mod-2^k "
        "information cannot beat a residue lookup at matched information budget. "
        "Expected outcome: **no win**."
    )
    lines.append("")
    lines.append("## Baselines")
    lines.append("")
    lines.append("| B | space | train acc % | test acc % |")
    lines.append("|---|-------|-------------|------------|")
    for B in BASELINE_BUDGETS:
        b = results["baselines"][str(B)]
        lines.append(
            f"| {B} | 2^{B}={b['space']} | {b['train_acc']:.4f} | {b['test_acc']:.4f} |"
        )
    lines.append("")
    lines.append("## Leaderboard (top 20 features + baselines inline)")
    lines.append("")
    lines.append("```")
    # Rebuild board display
    base_dict = {int(k): v for k, v in results["baselines"].items()}
    lines.append(format_leaderboard(results["leaderboard"], base_dict))
    lines.append("```")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(f"**{results['verdict']}**")
    lines.append("")
    if results["wins"]:
        lines.append("Winning feature sets (anomaly — report loudly):")
        for w in results["wins"]:
            lines.append(
                f"- `{w['name']}`: test {w['test_acc']:.4f}% vs baseline-B={w['matched_B']} "
                f"{w['baseline_test_acc']:.4f}% (Δ = {w['margin_pp']:+.4f} pp)"
            )
        lines.append("")
    else:
        # Note when baseline is perfect (common for low stopping-time thresholds)
        b8 = results["baselines"]["8"]
        if b8["test_acc"] >= 100.0 - 1e-12:
            lines.append("### Observation (why the baseline is perfect)")
            lines.append("")
            lines.append(
                "On this domain, the long-glide label `y = [σ > 4]` is **constant on each "
                "residue class mod 2^8** (hence also mod 2^10 and 2^12): baseline test "
                "accuracy is exactly 100% at every budget B ∈ {8,10,12}. The empirical "
                f"base rate is ~{results['base_rate_test']:.4f}% on test. No non-2-adic "
                "feature in the grammar can exceed a perfect 2-adic lookup."
            )
            lines.append("")
            lines.append(
                "This is the doctrine outcome: the difficulty is 2-adic; the grammar found "
                "no anomaly."
            )
            lines.append("")
    lines.append("## Excursion records (sustained odd-step density)")
    lines.append("")
    lines.append(
        "For each `n < N`, walk the Terras orbit to 1 and track running odd-step density "
        "`a/L` (a = # of odd Terras steps in the first L steps) for all prefixes `L ≥ 20`. "
        "Per-n record = max density; table = top-10 n by that record."
    )
    lines.append("")
    lines.append(
        f"A divergent orbit would need density `≥ log 2 / log 3 ≈ "
        f"{results['density_threshold']:.6f}` forever."
    )
    lines.append("")
    lines.append(
        f"**Max L at which any n < {N} still has a/L ≥ log2/log3:** "
        f"{results['max_L_density_ge_log2_log3']}"
    )
    lines.append("")
    lines.append("| rank | n | L | a | a/L |")
    lines.append("|------|---|---|---|-----|")
    for i, rec in enumerate(results["excursion_top"], 1):
        lines.append(
            f"| {i} | {rec['n']} | {rec['L']} | {rec['a']} | {rec['density']:.6f} |"
        )
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- `fold/f4_feature_regression.py` — experiment")
    lines.append("- `fold/test_f4.py` — verification")
    lines.append("- `fold/F4_REPORT.md` — this report")
    lines.append("")
    lines.append("## Runtime note")
    lines.append("")
    if N < (1 << DEFAULT_EXP):
        lines.append(
            f"Domain shrunk to N={N} (from 2^{DEFAULT_EXP}) to meet the 15-minute runtime "
            "cap; protocol unchanged."
        )
    else:
        lines.append(f"Full domain N=2^{DEFAULT_EXP}={N}; protocol as specified.")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="F4 symbolic-feature regression")
    p.add_argument(
        "--exp",
        type=int,
        default=DEFAULT_EXP,
        help=f"domain N=2^exp (default {DEFAULT_EXP})",
    )
    p.add_argument(
        "--report",
        type=str,
        default=os.path.join(_HERE, "F4_REPORT.md"),
        help="path for markdown report",
    )
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)

    N = 1 << args.exp
    results = run_experiment(N)
    write_report(results, args.report)

    if not args.quiet:
        print(f"N={N}  train={results['n_train']}  test={results['n_test']}")
        print(
            f"base rates: train={results['base_rate_train']:.4f}%  "
            f"test={results['base_rate_test']:.4f}%"
        )
        print(f"feature sets: {results['n_feature_sets']}")
        print()
        print("Baselines:")
        for B in BASELINE_BUDGETS:
            b = results["baselines"][str(B)]
            print(f"  B={B}: train={b['train_acc']:.4f}%  test={b['test_acc']:.4f}%")
        print()
        print("Leaderboard (top 20 + baselines):")
        print(format_leaderboard(results["leaderboard"]))
        print()
        print("Excursion records:")
        print(
            format_excursion(
                results["excursion_top"],
                results["max_L_density_ge_log2_log3"],
                results["density_threshold"],
            )
        )
        print()
        print(f"VERDICT: {results['verdict']}")
        print(f"Report written: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
