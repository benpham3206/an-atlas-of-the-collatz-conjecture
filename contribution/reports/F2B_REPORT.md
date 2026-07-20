# F2b — analytic collapse screen (2026-07-18)

**Verdict: NO CROSS-DEPTH COLLAPSE for k ≤ 8 — analytically, at all resolutions.**

Method: if folds (k,r) and (k',r') are affinely conjugate, the conjugacy maps
branch partitions to branch partitions and preserves branch slopes 3^a/2^(L−k),
which uniquely encode (a, L). Hence conjugate folds have identical
branch-count-by-length sequences. Each class's sequence obeys the counting law
of its k-bit parity window's avoiding language (KMP transfer matrix, exact
integer counts, minimal recurrence over Q recovered and verified against 80 terms).

Result: 510 classes (k = 1..8) → 47 distinct exact counting laws, **none shared
across depths**. Every cross-depth pair eliminated. Runtime 0.64 s
(`f2b_analytic_screen.py`), vs ~1 h of enumeration for the fog-limited k ≤ 5
verdict in F2 — which this result subsumes and explains.

Observed structure: each k-bonacci dominant rate (φ, tribonacci, …) reappears
at depth k+1 inside a *different* minimal law (same dominant root, different
sequence) — a systematic near-collision that a growth-rate-only screen would
have missed; the full-law comparison separates them.

Caveat for the write-up (the one lemma needing care): avoiding-language counts
are used as the invariant proxy for first-return-word counts. F2's enumeration
supports it exactly at k = 2 (F₂₄/F₂₅ hits); the clean derivation is
Guibas–Odlyzko first-occurrence machinery. Until that lemma is written, the
verdict's status is: machine-verified necessary condition + exact enumeration
agreement at k ≤ 5.

Supersedes: the planned F2b enumeration engine (no longer needed for the
collapse question; enumeration remains useful only for fold data mining).
