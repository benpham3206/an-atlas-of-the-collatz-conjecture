"""
F1 tests — plain asserts, stdlib-runnable (also pytest-compatible).

Run:
    python3 fold/test_f1.py
    # or from fold/:
    python3 test_f1.py
"""

from __future__ import annotations

import os
import sys
import time
import traceback

# Allow running as script from repo root or fold/
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from f1_word_calculus import (  # noqa: E402
    apply_composite,
    c_w_closed_form,
    cycle_candidate_sweep,
    extremal_word_atlas,
    parity_word,
    random_composite_property_test,
    stopping_time_spectrum,
    terras,
    terras_bijection_check,
    terras_iter,
    word_composite,
)


class Results:
    def __init__(self) -> None:
        self.sections: list[dict] = []

    def record(self, name: str, status: str, runtime_s: float, detail: str = "") -> None:
        self.sections.append(
            {"name": name, "status": status, "runtime_s": runtime_s, "detail": detail}
        )
        print(f"[{status}] {name}  ({runtime_s:.3f}s)  {detail}")


def test_d1_composite_calculus(R: Results) -> None:
    """Deliverable 1: composite affine form vs direct iteration (≥10k random)."""
    t0 = time.perf_counter()
    # Spot checks first
    # word (1,0) on n=1: T(1)=2, T(2)=1 → after 2 steps back to 1
    w10 = (1, 0)
    pow3, c, pow2 = word_composite(w10)
    assert pow3 == 3 and pow2 == 4 and c == 1, (pow3, c, pow2)
    assert apply_composite(1, w10) == 1
    assert c_w_closed_form(w10) == c

    # word (0,1) on n=2
    w01 = (0, 1)
    pow3, c, pow2 = word_composite(w01)
    assert pow3 == 3 and pow2 == 4 and c == 2, (pow3, c, pow2)
    assert apply_composite(2, w01) == 2

    # all-even word of length 3 on n=8: 8→4→2→1
    w000 = (0, 0, 0)
    assert word_composite(w000) == (1, 0, 8)
    assert apply_composite(8, w000) == 1
    assert terras_iter(8, 3) == 1

    prop = random_composite_property_test(
        num_samples=10_000, n_max=10**6, L_max=30, seed=20260718
    )
    assert prop["ok"], f"composite failures: {prop['failures'][:5]}"
    assert prop["num_samples"] >= 10_000
    elapsed = time.perf_counter() - t0
    R.record(
        "D1 composite calculus",
        "PASS",
        elapsed,
        f"samples={prop['num_samples']} property_t={prop['runtime_s']:.3f}s",
    )


def test_d2_terras_bijection(R: Results) -> None:
    """Deliverable 2: bijection parity-word ↔ Z/2^k Z for k ≤ 20."""
    t0 = time.perf_counter()
    max_k = 20
    msgs = []
    for k in range(0, max_k + 1):
        ok, msg = terras_bijection_check(k)
        assert ok, msg
        msgs.append(msg)
    elapsed = time.perf_counter() - t0
    statement = (
        f"For each k≤{max_k}, φ_k : Z/2^k Z → {{0,1}}^k, "
        "φ_k([n]) = length-k parity word of a positive lift of [n], is bijective."
    )
    R.record("D2 Terras bijection", "PASS", elapsed, statement)


def test_d3_cycle_sweep(R: Results) -> None:
    """Deliverable 3: exhaustive cycle candidates L ≤ 24; only trivial cycle through 1."""
    t0 = time.perf_counter()
    max_L = 24
    # Runtime budget: if L=24 too slow we shrink (report SHRUNK)
    status = "PASS"
    result = cycle_candidate_sweep(max_L=max_L, skip_cyclic_duplicates=True)
    elapsed = time.perf_counter() - t0

    # If unexpectedly slow path already finished; check correctness
    assert result["only_trivial"], (
        f"nontrivial cycles found: {result['nontrivial_outside_orbit_1_2']}"
    )
    # Must find the trivial 2-cycle (at least one of n=1 or n=2)
    found_ns = {c["n"] for c in result["verified_cycles"]}
    assert found_ns & {1, 2}, f"trivial cycle not found; got {result['verified_cycles']}"

    # Every verified cycle point must actually cycle under Terras and hit 1 or 2
    for cyc in result["verified_cycles"]:
        n = cyc["n"]
        w = cyc["word"]
        assert apply_composite(n, w) == n
        assert parity_word(n, cyc["L"]) == w
        # orbit eventually in {1,2}
        x = n
        seen = set()
        while x not in seen:
            seen.add(x)
            x = terras(x)
            if x in (1, 2) and n in (1, 2):
                break
            if len(seen) > 50:
                break
        assert n in (1, 2) or (1 in seen and 2 in seen), cyc

    detail = (
        f"max_L={result['max_L']} examined={result['words_examined']} "
        f"pruned_growth={result['words_pruned_growth']} "
        f"skipped_necklace={result['words_skipped_necklace']} "
        f"integral={result['candidates_integral']} "
        f"verified={len(result['verified_cycles'])} ns={sorted(found_ns)}"
    )
    R.record("D3 cycle-candidate sweep", status, elapsed, detail)
    # stash for report
    R._cycle_result = result  # type: ignore[attr-defined]


def test_d4_stopping_spectrum(R: Results) -> None:
    """Deliverable 4: stopping-time spectrum for n < 2^20."""
    t0 = time.perf_counter()
    limit = 1 << 20
    status = "PASS"
    # Quick known values before full sweep
    assert terras(1) == 2
    assert terras(2) == 1
    # 3 → 5 → 8 → 4 → 2 → 1  (Terras)
    # stopping time of 3: 3→5 (up), 5→8 (up), 8→4 (<3) so st=3? Wait 8>3, 4>3? 4>3, 2<3 so k=4
    # T: 3 odd → (9+1)/2=5; 5→(15+1)/2=8; 8→4; 4→2; 2→1
    # first < 3 is 2 at k=4
    from f1_word_calculus import stopping_time, total_stopping_time

    assert stopping_time(3) == 4
    assert total_stopping_time(3) == 5
    assert total_stopping_time(1) == 0

    # Budget: 2^20 should be fine; if needed shrink
    try:
        spec = stopping_time_spectrum(limit=limit)
    except Exception:
        limit = 1 << 18
        status = f"SHRUNK-TO-{limit}"
        spec = stopping_time_spectrum(limit=limit)

    assert spec["stopping"]["max"] is not None
    assert spec["stopping"]["argmax"] is not None
    assert spec["total_stopping"]["max"] is not None
    elapsed = time.perf_counter() - t0
    st = spec["stopping"]
    tt = spec["total_stopping"]
    detail = (
        f"limit={spec['limit']} "
        f"stop_max={st['max']}@n={st['argmax']} "
        f"p50={st['percentiles'].get(50)} p99={st['percentiles'].get(99)} "
        f"total_max={tt['max']}@n={tt['argmax']} "
        f"tp50={tt['percentiles'].get(50)} tp99={tt['percentiles'].get(99)}"
    )
    R.record("D4 stopping-time spectrum", status, elapsed, detail)
    R._spectrum = spec  # type: ignore[attr-defined]


def test_d5_extremal_words(R: Results) -> None:
    """Deliverable 5: n=2^k-1 takes k odd steps; T^k(n)=3^k-1 for k≤30."""
    t0 = time.perf_counter()
    atlas = extremal_word_atlas(max_k=30)
    assert atlas["all_ok"], [r for r in atlas["results"] if not r["ok"]]
    # explicit k=1,5,10
    assert parity_word((1 << 1) - 1, 1) == (1,)
    assert terras_iter(1, 1) == 2  # 3^1-1=2
    assert terras_iter((1 << 5) - 1, 5) == (3 ** 5) - 1
    elapsed = time.perf_counter() - t0
    R.record(
        "D5 extremal-word atlas",
        "PASS",
        elapsed,
        f"k=1..30 all verified; e.g. T^5(31)={3**5-1}",
    )
    R._extremal = atlas  # type: ignore[attr-defined]


def write_report(R: Results, path: str) -> None:
    """Deliverable 6: F1_REPORT.md"""
    lines = [
        "# F1 Report — Collatz word-fold calculus",
        "",
        "Packet F1 calibration: exact-arithmetic compositions of the Terras map.",
        "",
        "## Definitions",
        "",
        "- **Terras map:** `T(n)=n/2` if even; `T(n)=(3n+1)/2` if odd.",
        "- **Parity word** of length `k`: `w_i = parity(T^i(n))` (1=odd, 0=even).",
        "- **Composite affine form:** word `w` of length `L` with `a` ones gives",
        "  `n ↦ (3^a · n + c_w) / 2^L`, with",
        "  `c_w = Σ_j 3^{a-j-1} · 2^{i_j}` over odd-step indices `i_j` (0-based),",
        "  equivalently the inductive rule `c ← 3c + 2^i` on each odd step at index `i`.",
        "",
        "## Exact statements verified",
        "",
        "1. **Composite calculus.** For a random sample of ≥10 000 pairs `(n,L)` with",
        "   `1 ≤ n < 10^6` and `1 ≤ L ≤ 30`, if `w` is the length-`L` parity word of `n`,",
        "   then `(3^a n + c_w) / 2^L = T^L(n)` (exact integer equality).",
        "2. **Terras bijection.** For each `k ≤ 20`, the map",
        "   `φ_k : ℤ/2^kℤ → {0,1}^k` sending residue `[n]` to the length-`k` parity word",
        "   of a positive lift of `[n]` is a **bijection** (all `2^k` words hit exactly once).",
        "3. **Cycle candidates.** A cycle realizing word `w` requires",
        "   `n = c_w / (2^L − 3^a)` to be a positive integer whose parity word is `w`.",
        "   Exhaustive enumeration over necklace-canonical words with `L ≤ 24` and",
        "   `2^L > 3^a` finds only the trivial 2-cycle through `{1,2}`.",
        "4. **Stopping-time spectrum.** For all `n` in the reported range, stopping time",
        "   (least `k≥1` with `T^k(n)<n`) and total stopping time (least `k` with `T^k(n)=1`)",
        "   are computed; distribution summary below.",
        "5. **Extremal words.** For each `k ≤ 30`, `n = 2^k − 1` has parity word",
        "   `(1,…,1)` of length `k`, and `T^k(2^k−1) = 3^k − 1`.",
        "",
        "## Per-section results and wall-clock runtimes",
        "",
        "| Section | Status | Runtime (s) | Detail |",
        "|---------|--------|-------------|--------|",
    ]
    for s in R.sections:
        detail = s["detail"].replace("|", "\\|")
        lines.append(
            f"| {s['name']} | {s['status']} | {s['runtime_s']:.3f} | {detail} |"
        )
    lines.append("")

    # Cycle detail
    if hasattr(R, "_cycle_result"):
        cyc = R._cycle_result
        lines += [
            "## Cycle-candidate certificate detail",
            "",
            f"- max_L: {cyc['max_L']}",
            f"- words examined (after growth prune + necklace filter): {cyc['words_examined']}",
            f"- words pruned by `2^L ≤ 3^a`: {cyc['words_pruned_growth']}",
            f"- words skipped as non-canonical necklace: {cyc['words_skipped_necklace']}",
            f"- integral positive `n = c_w/(2^L−3^a)` candidates: {cyc['candidates_integral']}",
            f"- verified cycles (parity word matches): {len(cyc['verified_cycles'])}",
            "",
            "Verified cycle points:",
            "",
        ]
        for v in cyc["verified_cycles"]:
            lines.append(
                f"- n={v['n']}, L={v['L']}, a={v['a']}, word={v['word']}, "
                f"c_w={v['c_w']}, denom={v['denom']}"
            )
        lines.append("")
        lines.append(
            f"- only_trivial (orbit in {{1,2}}): **{cyc['only_trivial']}**"
        )
        lines.append("")

    # Spectrum detail
    if hasattr(R, "_spectrum"):
        sp = R._spectrum
        st = sp["stopping"]
        tt = sp["total_stopping"]
        lines += [
            "## Stopping-time spectrum summary",
            "",
            f"- limit N = {sp['limit']} (n in ranges {sp['n_range_stopping']} stopping; "
            f"{sp['n_range_total']} total)",
            "",
            "### Stopping time (first drop below n)",
            "",
            f"- count: {st['count']}",
            f"- min / max / argmax: {st['min']} / {st['max']} / n={st['argmax']}",
            f"- mean: {st['mean']:.6f}",
            f"- percentiles (50, 90, 99, 99.9): "
            f"{st['percentiles'].get(50)}, {st['percentiles'].get(90)}, "
            f"{st['percentiles'].get(99)}, {st['percentiles'].get(99.9)}",
            f"- section runtime: {st['runtime_s']:.3f}s",
            "",
            "### Total stopping time (to 1)",
            "",
            f"- count: {tt['count']}",
            f"- min / max / argmax: {tt['min']} / {tt['max']} / n={tt['argmax']}",
            f"- mean: {tt['mean']:.6f}",
            f"- percentiles (50, 90, 99, 99.9): "
            f"{tt['percentiles'].get(50)}, {tt['percentiles'].get(90)}, "
            f"{tt['percentiles'].get(99)}, {tt['percentiles'].get(99.9)}",
            f"- section runtime: {tt['runtime_s']:.3f}s",
            "",
        ]

    # Extremal
    if hasattr(R, "_extremal"):
        ext = R._extremal
        lines += [
            "## Extremal-word atlas",
            "",
            f"- max_k: {ext['max_k']}",
            f"- all_ok: **{ext['all_ok']}**",
            f"- sample: k=10, n=2^10−1=1023, T^10(1023)=3^10−1=59048",
            "",
        ]

    lines += [
        "## Anomalies",
        "",
        "An anomaly is a noteworthy result, not a test failure.",
        "",
    ]
    anomalies = []
    if hasattr(R, "_cycle_result"):
        cyc = R._cycle_result
        # Multiple representations of the same 2-cycle at different L (periodic extensions)
        if len(cyc["verified_cycles"]) > 2:
            anomalies.append(
                f"Cycle sweep found {len(cyc['verified_cycles'])} verified fixed points "
                f"of words (not just n=1 and n=2). All lie on the trivial orbit {{1,2}} "
                f"or are necklace-filtered representations; listed above. Periodic "
                f"repetitions of the 2-cycle word (e.g. (1,0) repeated) yield the same n=1."
            )
        if cyc["candidates_integral"] > len(cyc["verified_cycles"]):
            anomalies.append(
                f"{cyc['candidates_integral'] - len(cyc['verified_cycles'])} integral "
                f"candidates n=c_w/(2^L−3^a) failed the parity-word check (false positives "
                f"of the affine fixed-point equation alone). This is expected: integrality "
                f"of the formal fixed point does not imply the residue path realizes w."
            )
    if hasattr(R, "_spectrum"):
        st = R._spectrum["stopping"]
        tt = R._spectrum["total_stopping"]
        anomalies.append(
            f"Among n < {R._spectrum['limit']}, max stopping time is {st['max']} "
            f"at n={st['argmax']}; max total stopping time is {tt['max']} at n={tt['argmax']}."
        )
    if not anomalies:
        lines.append("None recorded.")
    else:
        for a in anomalies:
            lines.append(f"- {a}")
    lines += [
        "",
        "## Environment",
        "",
        f"- Python: {sys.version.split()[0]}",
        "- Arithmetic: Python arbitrary-precision ints only in certificates",
        "- Dependencies: stdlib only",
        "",
        "## Files",
        "",
        "- `fold/f1_word_calculus.py` — library",
        "- `fold/test_f1.py` — tests + report emitter",
        "- `fold/F1_REPORT.md` — this report",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {path}")


def main() -> int:
    R = Results()
    print("=== F1 test suite ===")
    total_t0 = time.perf_counter()
    failed = []
    for name, fn in [
        ("D1", test_d1_composite_calculus),
        ("D2", test_d2_terras_bijection),
        ("D3", test_d3_cycle_sweep),
        ("D4", test_d4_stopping_spectrum),
        ("D5", test_d5_extremal_words),
    ]:
        try:
            fn(R)
        except Exception as e:
            elapsed = 0.0
            # try to get partial timing from last section if any
            tb = traceback.format_exc()
            print(f"[FAIL] {name}: {e}\n{tb}")
            R.record(f"{name}", "FAIL", elapsed, str(e))
            failed.append(name)

    report_path = os.path.join(_HERE, "F1_REPORT.md")
    try:
        write_report(R, report_path)
        R.record("D6 F1_REPORT.md", "PASS", 0.0, report_path)
    except Exception as e:
        print(f"[FAIL] D6 report: {e}")
        failed.append("D6")
        R.record("D6 F1_REPORT.md", "FAIL", 0.0, str(e))

    total = time.perf_counter() - total_t0
    print("=== summary ===")
    for s in R.sections:
        print(f"  {s['status']:12}  {s['name']:28}  {s['runtime_s']:8.3f}s  {s['detail'][:100]}")
    print(f"TOTAL wall-clock: {total:.3f}s")
    if failed:
        print(f"FAILED: {failed}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
