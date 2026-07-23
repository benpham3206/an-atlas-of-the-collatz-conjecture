#!/usr/bin/env python3
"""Cycle-exclusion extension runner: exact search at m = 19, 20 odd members.

Extends contribution/code/fence/exact_cycle_search.py (which excluded
nontrivial positive Collatz cycles with <= 18 odd members) to the next
valuation-word layers.  All acceptance arithmetic is exact integer arithmetic
(Python arbitrary-precision ints); wall-clock timings are the only floats and
are labeled measurements, never part of any acceptance decision.

Search window (exact, per the fence proof doc):

    3^m < 2^K <= (22/7)^m

evaluated with integer comparisons 2^K <= 3^m and 2^K * 7^m <= 22^m only.

Layers covered here:

    (19, 31)                    86,493,225 ordered compositions
    (20, 32)                   141,120,525 ordered compositions
    (20, 33)                   347,373,600 ordered compositions

plus a regression re-scan of the twelve m <= 18 pairs from the fence doc.

Two phases per extension pair, cross-validated:

  * primary:      repo enumerator exact_cycle_search.compositions_of and the
                  repo gate exact_cycle_search.try_integral_fixed_point;
  * independent:  a separately written iterative composition enumerator
                  (reverse lexicographic order, different algorithm) with an
                  inline independently coded affine/divisibility gate.

Every divisibility hit from either phase is re-verified end-to-end by
exact_cycle_search.evaluate_exponents (exact divisibility, positive odd
quotient, direct orbit valuation check, closure, trivial-cycle exclusion).
A verified nontrivial cycle would be a Collatz counterexample: the runner
then sets counterexample_watch.fired = true and exits with status 3.

Parallelism partitions the composition space by value prefixes (each chunk is
the set of words with a fixed prefix); chunks are independent and merged
deterministically.  Chunking never skips or duplicates words: every pair's
enumerated-word total is checked against binom(K-1, m-1) exactly, in both
phases.

Usage:
    python3 run_cycle_exclusion_extension.py plan
    python3 run_cycle_exclusion_extension.py scan --pair 19:31 [--phase both]
    python3 run_cycle_exclusion_extension.py finalize
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from math import comb
from pathlib import Path
from typing import Iterator, Sequence

PACKET_DIR = Path(__file__).resolve().parent
FENCE_DIR = PACKET_DIR.parents[1] / "code" / "fence"
sys.path.insert(0, str(FENCE_DIR))

import exact_cycle_search as ecs  # noqa: E402

RESULTS_PATH = PACKET_DIR / "cycle_exclusion_extension_results.json"
OLD_RESULTS_PATH = FENCE_DIR / "exact_cycle_search_results.json"

# Surviving (m, K) pairs for m <= 18 per the fence proof doc (control first).
REGRESSION_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 2),
    (5, 8),
    (8, 13),
    (10, 16),
    (11, 18),
    (13, 21),
    (14, 23),
    (15, 24),
    (16, 26),
    (17, 27),
    (17, 28),
    (18, 29),
)
EXTENSION_PAIRS: tuple[tuple[int, int], ...] = (
    (19, 31),
    (20, 32),
    (20, 33),
)

# Stride for the closed-form mid-stream audit in the independent phase
# (prime, so it does not alias the enumerator's period structure).
AUDIT_STRIDE = 10_000_019

DEFAULT_WORKERS = 12
DEFAULT_MAX_CHUNK = 25_000_000  # words per chunk; bounds per-task latency


# ---------------------------------------------------------------------------
# Exact window
# ---------------------------------------------------------------------------


def exact_window(m: int) -> list[int]:
    """All K with 3^m < 2^K <= (22/7)^m, via integer comparisons only."""
    if m < 1:
        raise ValueError(f"m must be positive, got {m}")
    pow3 = 3**m
    pow7 = 7**m
    pow22 = 22**m
    ks: list[int] = []
    k = 1
    while (1 << k) <= pow3:
        k += 1
    while (1 << k) * pow7 <= pow22:
        ks.append(k)
        k += 1
    return ks


# ---------------------------------------------------------------------------
# Independent composition enumerator (NOT imported from the fence module).
# Iterative, reverse-lexicographic order: first part descending.
# ---------------------------------------------------------------------------


def iter_compositions_independent(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Stream all compositions of ``total`` into ``parts`` positive parts.

    Independent re-implementation used to cross-validate the repo oracle
    ``compositions_of`` (which is recursive and lex-ascending).  This one is
    iterative and lex-descending; a different algorithm in a different order.
    """
    if parts < 1 or total < parts:
        return
    if parts == 1:
        yield (total,)
        return
    a = [total - parts + 1] + [1] * (parts - 1)
    last = parts - 1
    while True:
        yield tuple(a)
        i = last - 1
        while i >= 0 and a[i] == 1:
            i -= 1
        if i < 0:
            return
        a[i] -= 1
        a[i + 1] = a[last] + 1
        for j in range(i + 2, parts):
            a[j] = 1


def affine_cs_closed_form(word: Sequence[int]) -> tuple[int, int]:
    """C_m and K via the closed form C_m = sum_j 3^{m-1-j} 2^{S_j}.

    Independent of the recurrence in exact_cycle_search.affine_CS; used to
    audit the recurrence on every hit and on a strided mid-stream sample.
    """
    m = len(word)
    pow3 = [1] * m
    for j in range(m - 2, -1, -1):
        pow3[j] = pow3[j + 1] * 3
    c = 0
    s = 0
    for j, a_j in enumerate(word):
        c += pow3[j] << s
        s += a_j
    return c, s


# ---------------------------------------------------------------------------
# Chunked parallel scan
# ---------------------------------------------------------------------------


def build_chunks(m: int, k: int, max_chunk: int) -> list[tuple[tuple[int, ...], int, int, int]]:
    """Partition words by prefix.  Returns (prefix, remaining_sum, remaining_parts, size)."""
    chunks: list[tuple[tuple[int, ...], int, int, int]] = []

    def rec(prefix: tuple[int, ...]) -> None:
        rs = k - sum(prefix)
        rp = m - len(prefix)
        size = comb(rs - 1, rp - 1)
        if size <= max_chunk or rp == 1:
            chunks.append((prefix, rs, rp, size))
            return
        for t in range(1, rs - rp + 2):
            rec(prefix + (t,))

    rec(())
    return chunks


def _scan_chunk(args: tuple[int, int, tuple[int, ...], int, int, str, int]) -> dict:
    """Scan one prefix chunk.  Top-level for multiprocessing pickling."""
    m, k, prefix, rs, rp, phase, audit_stride = args
    count = 0
    hits: list[tuple[tuple[int, ...], int, int, int]] = []
    audits = 0
    audit_mismatches: list[tuple[int, ...]] = []
    if phase == "primary":
        for suffix in ecs.compositions_of(rs, rp):
            word = prefix + suffix
            count += 1
            fp = ecs.try_integral_fixed_point(word)
            if fp is not None:
                n0, c_m, denom = fp
                hits.append((word, n0, c_m, denom))
    elif phase == "independent":
        denom = (1 << k) - 3**m
        for suffix in iter_compositions_independent(rs, rp):
            word = prefix + suffix
            count += 1
            c = 0
            s = 0
            for a_j in word:
                c = 3 * c + (1 << s)
                s += a_j
            if audit_stride and count % audit_stride == 0:
                audits += 1
                c_cf, s_cf = affine_cs_closed_form(word)
                if c_cf != c or s_cf != s:
                    audit_mismatches.append(word)
            if c % denom == 0:
                n0 = c // denom
                if n0 > 0 and n0 % 2 == 1:
                    hits.append((word, n0, c, denom))
    else:  # pragma: no cover
        raise ValueError(f"unknown phase {phase!r}")
    return {
        "count": count,
        "hits": hits,
        "audits": audits,
        "audit_mismatches": audit_mismatches,
    }


def scan_pair(
    m: int,
    k: int,
    phase: str,
    workers: int = DEFAULT_WORKERS,
    max_chunk: int = DEFAULT_MAX_CHUNK,
    audit_stride: int = AUDIT_STRIDE,
    chunk_start: int | None = None,
    chunk_stop: int | None = None,
) -> dict:
    """Scan compositions for one (m, K) pair in one phase.

    With chunk_start/chunk_stop, scans only that slice of the deterministic
    chunk partition (for wall-clock-bounded invocations of large pairs);
    coverage merging and completeness happen in cmd_scan.
    """
    chunks = build_chunks(m, k, max_chunk)
    n_chunks = len(chunks)
    start = 0 if chunk_start is None else chunk_start
    stop = n_chunks if chunk_stop is None else chunk_stop
    if not (0 <= start < stop <= n_chunks):
        raise ValueError(f"bad chunk slice [{start},{stop}) of {n_chunks}")
    selected = chunks[start:stop]
    args = [(m, k, p, rs, rp, phase, audit_stride) for (p, rs, rp, _size) in selected]
    t0 = time.perf_counter()
    total = 0
    hits: list[tuple[tuple[int, ...], int, int, int]] = []
    audits = 0
    audit_mismatches: list[tuple[int, ...]] = []
    if workers > 1 and len(args) > 1:
        ctx = mp.get_context("fork")
        with ctx.Pool(min(workers, len(args))) as pool:
            for res in pool.imap_unordered(_scan_chunk, args):
                total += res["count"]
                hits.extend(res["hits"])
                audits += res["audits"]
                audit_mismatches.extend(res["audit_mismatches"])
    else:
        for a in args:
            res = _scan_chunk(a)
            total += res["count"]
            hits.extend(res["hits"])
            audits += res["audits"]
            audit_mismatches.extend(res["audit_mismatches"])
    dt = time.perf_counter() - t0

    formula = comb(k - 1, m - 1)
    partial = not (start == 0 and stop == n_chunks)
    hits.sort(key=lambda h: h[0])
    return {
        "phase": phase,
        "m": m,
        "k": k,
        "chunks": len(selected),
        "total_chunks": n_chunks,
        "coverage": [[start, stop]],
        "partial": partial,
        "workers": workers if len(args) > 1 else 1,
        "words_enumerated": total,
        "composition_count_formula": formula,
        "count_matches_formula": (total == formula) if not partial else None,
        "wall_seconds_measured_float": dt,
        "throughput_words_per_second_measured_float": (total / dt) if dt > 0 else None,
        "divisibility_hit_count": len(hits),
        "hits": [
            {"word": list(w), "n0": n0, "c_m": c_m, "denom": denom}
            for (w, n0, c_m, denom) in hits
        ],
        "closed_form_audits": audits,
        "closed_form_audit_mismatches": [list(w) for w in audit_mismatches],
    }


def merge_phase_results(prev: dict, new: dict) -> dict:
    """Additively merge two partial (or partial+full) phase scans.

    Rejects overlapping chunk coverage, which would double-count words.
    """
    if (prev["m"], prev["k"], prev["phase"]) != (new["m"], new["k"], new["phase"]):
        raise RuntimeError("phase merge mismatch")
    if prev["total_chunks"] != new["total_chunks"]:
        raise RuntimeError("chunk partition changed between invocations")
    intervals = sorted(prev["coverage"] + new["coverage"])
    norm: list[list[int]] = []
    for s, e in intervals:
        if norm and s < norm[-1][1]:
            raise RuntimeError(f"overlapping chunk coverage: {intervals}")
        if norm and s == norm[-1][1]:
            norm[-1][1] = e
        else:
            norm.append([s, e])
    complete = norm == [[0, new["total_chunks"]]]
    hits = sorted(prev["hits"] + new["hits"], key=lambda h: h["word"])
    total = prev["words_enumerated"] + new["words_enumerated"]
    wall = (
        prev["wall_seconds_measured_float"] + new["wall_seconds_measured_float"]
    )
    return {
        "phase": new["phase"],
        "m": new["m"],
        "k": new["k"],
        "chunks": prev["chunks"] + new["chunks"],
        "total_chunks": new["total_chunks"],
        "coverage": norm,
        "partial": not complete,
        "workers": new["workers"],
        "words_enumerated": total,
        "composition_count_formula": new["composition_count_formula"],
        "count_matches_formula": (
            (total == new["composition_count_formula"]) if complete else None
        ),
        "wall_seconds_measured_float": wall,
        "throughput_words_per_second_measured_float": (total / wall) if wall > 0 else None,
        "divisibility_hit_count": len(hits),
        "hits": hits,
        "closed_form_audits": prev["closed_form_audits"] + new["closed_form_audits"],
        "closed_form_audit_mismatches": (
            prev["closed_form_audit_mismatches"] + new["closed_form_audit_mismatches"]
        ),
    }


# ---------------------------------------------------------------------------
# Hit verification and pair-level assembly
# ---------------------------------------------------------------------------


def verify_hits(m: int, k: int, hit_entries: list[dict]) -> tuple[list[dict], list[dict]]:
    """Full end-to-end verification of every divisibility hit via the fence
    module's evaluate_exponents, plus a closed-form C_m cross-check.

    Returns (verified_candidates, rejected_hits).  A hit is *rejected* when
    the affine fixed point does not lift to a real orbit following the word;
    a rejected hit is not a cycle and not a counterexample.
    """
    verified: list[dict] = []
    rejected: list[dict] = []
    seen: set[tuple[int, ...]] = set()
    for entry in hit_entries:
        word = tuple(entry["word"])
        # closed-form cross-check of the affine constant
        c_cf, s_cf = affine_cs_closed_form(word)
        if c_cf != entry["c_m"] or s_cf != sum(word):
            raise RuntimeError(f"closed-form mismatch on hit word {word}")
        cand = ecs.evaluate_exponents(word)
        if cand is None:
            rejected.append(
                {
                    "word": list(word),
                    "n0_affine_fixed_point": entry["n0"],
                    "reason": (
                        "integral affine fixed point does not lift to an orbit "
                        "following the prescribed valuations (direct iteration "
                        "rejects it); not a cycle"
                    ),
                }
            )
            continue
        if cand.exponents in seen:
            continue
        seen.add(cand.exponents)
        verified.append(cand.to_dict())
    verified.sort(key=lambda c: (c["n0"], c["exponents"]))
    return verified, rejected


def new_pair_record(m: int, k: int) -> dict:
    return {
        "m": m,
        "k": k,
        "pow2_K": 1 << k,
        "pow3_m": 3**m,
        "denom": (1 << k) - 3**m,
        "phases": {},
    }


def assemble_pair_record(record: dict) -> dict:
    """Recompute all derived fields of a pair record from its raw phases.

    Idempotent: safe to call after each single-phase scan invocation so that
    long pairs can be scanned one phase per process invocation.
    """
    m, k = record["m"], record["k"]
    primary = record["phases"].get("primary")
    if primary is None or primary.get("partial"):
        return record
    if not primary["count_matches_formula"]:
        raise RuntimeError(
            f"primary enumeration count mismatch at ({m},{k}): "
            f"{primary['words_enumerated']} != {primary['composition_count_formula']}"
        )

    # Cross-validation between phases
    if "independent" in record["phases"]:
        indep = record["phases"]["independent"]
        if indep.get("partial"):
            return record
        if not indep["count_matches_formula"]:
            raise RuntimeError(
                f"independent enumeration count mismatch at ({m},{k}): "
                f"{indep['words_enumerated']} != {indep['composition_count_formula']}"
            )
        record["cross_validation"] = {
            "counts_equal_both_phases": (
                indep["words_enumerated"] == primary["words_enumerated"]
            ),
            "independent_count_matches_formula": indep["count_matches_formula"],
            "hit_word_sets_equal": (
                sorted(tuple(h["word"]) for h in indep["hits"])
                == sorted(tuple(h["word"]) for h in primary["hits"])
            ),
            "closed_form_audit_mismatches": indep["closed_form_audit_mismatches"],
        }

    verified, rejected = verify_hits(m, k, primary["hits"])
    record["verified_candidates"] = verified
    record["rejected_hits"] = rejected
    record["nontrivial_counterexamples"] = [
        c for c in verified if c["is_nontrivial_counterexample"]
    ]
    return record


# ---------------------------------------------------------------------------
# Report assembly / persistence
# ---------------------------------------------------------------------------


def load_results() -> dict:
    if RESULTS_PATH.exists():
        return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    return {
        "packet": "2026-07-23-cycle-exclusion-extension",
        "generated_by": "run_cycle_exclusion_extension.py",
        "statement": (
            "no nontrivial positive Collatz cycle with at most 20 odd members"
        ),
        "map": "U(n)=(3n+1)/2^{v2(3n+1)} on positive odd integers",
        "search_window": "3^m < 2^K <= (22/7)^m, evaluated with exact integer comparisons",
        "arithmetic": (
            "Python arbitrary-precision integers only; the only floats in this "
            "file are wall-clock measurements labeled *_measured_float"
        ),
        "machine": {
            "note": "36 GB Mac, 14 logical CPUs; chunk-parallel exact scan",
            "workers_default": DEFAULT_WORKERS,
        },
        "pairs": {},
        "counterexample_watch": {
            "fired": False,
            "detail": (
                "any verified nontrivial positive cycle at any scanned depth "
                "would set fired=true; a cycle certificate would be reported "
                "immediately"
            ),
        },
    }


def save_results(results: dict) -> None:
    RESULTS_PATH.write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def cmd_scan(args: argparse.Namespace) -> int:
    m, k = ecs.parse_pair(args.pair)
    phases = ("primary", "independent") if args.phase == "both" else (args.phase,)
    results = load_results()
    key = f"{m}:{k}"
    record = results["pairs"].get(key) or new_pair_record(m, k)
    for phase in phases:
        res = scan_pair(
            m, k, phase, workers=args.workers, max_chunk=args.max_chunk,
            chunk_start=args.chunk_start, chunk_stop=args.chunk_stop,
        )
        prev = record["phases"].get(phase)
        if prev is not None and (prev.get("partial") or res.get("partial")):
            if not res.get("partial") and not prev.get("partial"):
                record["phases"][phase] = res
            elif res.get("partial"):
                record["phases"][phase] = merge_phase_results(prev, res)
            else:
                # a full re-scan replaces a partial one
                record["phases"][phase] = res
        else:
            record["phases"][phase] = res
        # persist the raw phase immediately so a later invocation (or crash)
        # never loses a completed phase
        results["pairs"][key] = record
        save_results(results)
    record = assemble_pair_record(record)
    results["pairs"][key] = record
    if record.get("nontrivial_counterexamples"):
        results["counterexample_watch"]["fired"] = True
        save_results(results)
        sys.stderr.write(
            "COUNTEREXAMPLE WATCH FIRED: verified nontrivial positive cycle at "
            f"({m},{k}): {json.dumps(record['nontrivial_counterexamples'])}\n"
        )
        return 3
    save_results(results)
    primary = record["phases"].get("primary")
    summary = {
        "pair": [m, k],
        "phases_run": list(phases),
        "words": primary["words_enumerated"] if primary else None,
        "wall_seconds": {
            ph: record["phases"][ph]["wall_seconds_measured_float"] for ph in record["phases"]
        },
        "divisibility_hits": primary["divisibility_hit_count"] if primary else None,
        "verified_candidates": len(record.get("verified_candidates", [])),
        "nontrivial_counterexamples": len(record.get("nontrivial_counterexamples", [])),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:  # noqa: ARG001
    """Regression-compare against the fence m<=18 results and stamp the verdict."""
    results = load_results()
    old = json.loads(OLD_RESULTS_PATH.read_text(encoding="utf-8"))
    old_by_pair = {(r["m"], r["k"]): r for r in old["pairs"]}

    regression = {"pairs_checked": [], "all_match": True}
    for m, k in REGRESSION_PAIRS:
        key = f"{m}:{k}"
        fresh = results["pairs"].get(key)
        if fresh is None:
            regression["all_match"] = False
            regression["pairs_checked"].append({"pair": [m, k], "error": "missing fresh scan"})
            continue
        old_row = old_by_pair[(m, k)]
        old_cands = sorted(
            (tuple(c["exponents"]), c["n0"]) for c in old_row["integral_candidates"]
        )
        fresh_cands = sorted(
            (tuple(c["exponents"]), c["n0"]) for c in fresh.get("verified_candidates", [])
        )
        match = old_cands == fresh_cands
        regression["all_match"] = regression["all_match"] and match
        regression["pairs_checked"].append(
            {
                "pair": [m, k],
                "old_verified_candidates": [
                    {"exponents": list(ex), "n0": n0} for (ex, n0) in old_cands
                ],
                "fresh_verified_candidates": [
                    {"exponents": list(ex), "n0": n0} for (ex, n0) in fresh_cands
                ],
                "matches_fence_results": match,
            }
        )
    results["regression_vs_fence_m18"] = regression

    # window completeness for m <= 20
    window_rows = []
    incomplete: list[list[int]] = []
    for m in range(1, 21):
        ks = exact_window(m)
        window_rows.append({"m": m, "k_window": ks})
        for k in ks:
            rec = results["pairs"].get(f"{m}:{k}")
            if rec is None or any(
                ph.get("partial") for ph in rec.get("phases", {}).values()
            ):
                incomplete.append([m, k])
    results["exact_windows_m1_to_m20"] = window_rows
    if incomplete:
        results["incomplete_pairs"] = incomplete
        results["window_coverage_complete_through_m20"] = False
    else:
        results.pop("incomplete_pairs", None)
        results["window_coverage_complete_through_m20"] = True

    all_nontrivial = [
        {"pair": key, "candidate": c}
        for key, rec in sorted(results["pairs"].items())
        for c in rec.get("nontrivial_counterexamples", [])
    ]
    results["counterexample_watch"]["fired"] = bool(all_nontrivial)
    results["counterexample_watch"]["verified_nontrivial_cycles"] = all_nontrivial
    results["verdict"] = (
        "COUNTEREXAMPLE FOUND" if all_nontrivial
        else (
            "no nontrivial positive Collatz cycle with at most 20 odd members "
            "(exact exhaustive search over all valuation words in the window "
            "3^m < 2^K <= (22/7)^m for m <= 20)"
            if results["window_coverage_complete_through_m20"]
            else "INCOMPLETE: not all window pairs scanned"
        )
    )
    save_results(results)
    print(json.dumps({
        "regression_all_match": regression["all_match"],
        "window_coverage_complete_through_m20": results["window_coverage_complete_through_m20"],
        "counterexample_watch_fired": results["counterexample_watch"]["fired"],
        "verdict": results["verdict"],
    }, indent=2, sort_keys=True))
    return 3 if all_nontrivial else 0


def cmd_plan(args: argparse.Namespace) -> int:  # noqa: ARG001
    for m in (19, 20):
        for k in exact_window(m):
            chunks = build_chunks(m, k, DEFAULT_MAX_CHUNK)
            sizes = sorted((s for (_p, _rs, _rp, s) in chunks), reverse=True)
            print(
                f"({m},{k}): {comb(k-1, m-1):,} words, {len(chunks)} chunks, "
                f"largest {sizes[0]:,}"
            )
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("scan")
    sp.add_argument("--pair", required=True, metavar="m:K")
    sp.add_argument("--phase", choices=("primary", "independent", "both"), default="both")
    sp.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    sp.add_argument("--max-chunk", type=int, default=DEFAULT_MAX_CHUNK)
    sp.add_argument("--chunk-start", type=int, default=None,
                    help="first chunk index of a partial slice (default: full pair)")
    sp.add_argument("--chunk-stop", type=int, default=None,
                    help="one past the last chunk index of a partial slice")
    sp.set_defaults(func=cmd_scan)
    fp = sub.add_parser("finalize")
    fp.set_defaults(func=cmd_finalize)
    pp = sub.add_parser("plan")
    pp.set_defaults(func=cmd_plan)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
