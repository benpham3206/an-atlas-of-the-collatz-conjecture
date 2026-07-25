# Descent requires contraction: a minimal counterexample cannot contract in its first 1,000,000 Syracuse steps

**Date:** 24 July 2026
**Status:** two elementary lemmas, one theorem, one corollary that consumes
Bařina's verification limit, plus an exhaustive exact scan. **Not** a proof of
the Collatz conjecture and **not** a counterexample.

> ## ⚠ PRIORITY CORRECTION (25 July 2026)
>
> A literature search run after this packet was written found that **its
> mathematical content is known, and has been since 1976.** The packet is
> retained as a quantitative refresh, not as a new theorem. Specifically:
>
> - **Lemma 1 is Terras's inequality `κ(n) ≤ σ(n)`.** Terras (1976) defines the
>   **coefficient stopping time** `κ(n)` — the least `k` with the multiplier
>   `α = 3^{a}/2^{k} < 1`, which is exactly "the first contracting index" here.
>   That descent forces contraction, because the additive term `β` is positive,
>   is his observation and is stated in Lagarias's annotated bibliography as
>   "it is clear that `κ(n) ≤ σ(n)`".
> - **The `M(h)` bound is Terras's own proof method** — upper-bound `β`,
>   lower-bound `1 − α`, conclude `n ≤ β/(1−α)`. Terras proved
>   `κ(n) = σ(n)` for `κ(n) ≤ 2593`; **Garner (1981)** extended it to
>   `κ(n) < 105,000` using the same bound plus continued-fraction convergents
>   of `log₂3` and machine verification to `2 × 10⁹`.
> - **Therefore §7's corollary is a quantitative refresh of Garner 1981**: the
>   same argument with Bařina's `2^71` in place of `2 × 10⁹`, reaching
>   `h ≤ 10⁶` rather than `κ < 105,000`. About 9.5× further in `h`, from a
>   verification bound roughly 10¹² times larger — which is itself a useful
>   datum about how slowly `M(h)` grows.
>
> **Not checked:** whether anyone has already published a post-2020 numerical
> extension of the coefficient-stopping-time verification using a Bařina-class
> bound. Until that is checked, **no novelty is claimed for the `10⁶` figure
> either.**
>
> What survives as this packet's own contribution: the exact `M(h)` table and
> its record structure at the convergents *and semiconvergents* of `log₂3`,
> the odd-`x` scan to 1.45 × 10⁹, and the verifier. See
> [`PRIORITY.md`](../../../PRIORITY.md).

**Companion executable evidence:** `verify_contraction_onset.py`,
`test_verify_contraction_onset.py`, `verify_contraction_onset.out`,
`contraction_onset_certificate.json`.

**Provenance.** The question was raised by an externally supplied research
note, `DANGEROUS_EXPONENT_CYLINDERS_NEXT_STEPS_V2.md` (user-supplied, not in
this repository), whose §13 "finite-ceiling collapse" lemma asks what lives in
the region where the homogeneous multiplier has contracted. The answer below
is that, quantitatively, almost nothing does. The note's algebra was re-derived
independently before this packet was written; the framing, the lemmas and the
bound here are stated in the atlas's own coordinates.

---

## 1. The claim

> **Claim.** Let `m` be a minimal Collatz counterexample — the least positive
> integer whose orbit does not reach 1. Then for every `h ≤ 1 000 000`,
> ```
> 2^{A_h(m)}  ≤  3^h ,
> ```
> where `A_h(m)` is the total 2-adic valuation consumed by the first `h`
> Syracuse steps of `m`. Equivalently: over its first `A_1000000 ≈ 1 585 000`
> Terras steps, **every** prefix of `m`'s parity word has one-density at least
> `log₃2`.

Not a liminf, not almost-all: every prefix, unconditionally, with an explicit
depth.

A second, independent statement from the same machinery:

> For every odd `x > 1` up to `1 447 674 322` (723 837 160 starts), the
> Syracuse orbit of `x` first contracts and first drops below `x` **at the
> same step**. The only odd `x` that contracts strictly before it descends is
> `x = 1` — the trivial cycle.

## 2. Kill criteria, written before the build

1. An orbit where `2^{A_h} S^h(x) ≠ 3^h x + C_h` — the cocycle is wrong.
   *600 000 identities checked exactly.*
2. An orbit that descends below its start at a step that is **not**
   contracting — Lemma 1 is false. *9 998 first descents observed; none.*
3. `C_h > h·3^{h-1}` at a step before the first contracting index — Lemma 2
   is false. *24 611 bounds checked.*
4. `A*(h) ≠ bit_length(3^h)`, i.e. the minimal exponent is misidentified —
   checked on both sides at every `h ≤ 1 000 000`.
5. `max_h M(h)` reaching `2^71` inside the computed range — that would end
   the corollary's reach, and is reported rather than hidden.
6. An odd `x > 1` that contracts strictly before it descends — the second
   claim is false. *723 837 160 odd starts; none.*
7. An odd `x` in the scan that never descends within the step cap — would be
   a counterexample. *None.*

None fired.

## 3. Setup

Syracuse map on positive odd integers, as in
[`EXACT_COUNTEREXAMPLE_SEARCH.md`](../../proofs/EXACT_COUNTEREXAMPLE_SEARCH.md):

```
S(x) = (3x+1) / 2^{v₂(3x+1)},   a_i = v₂(3x_{i-1}+1),   A_i = a_1+⋯+a_i,
C_0 = 0,   C_{i+1} = 3C_i + 2^{A_i},   so   S^h(x) = (3^h x + C_h) / 2^{A_h}.
```

That offset recurrence is the atlas's own — it is the same `C` used by the
exact cycle search. Call `h` **contracting** for `x` when `2^{A_h} > 3^h`,
i.e. when the homogeneous multiplier `3^h/2^{A_h}` has fallen below 1.

## 4. Lemma 1 — descent requires contraction

> **Lemma 1.** For every positive odd `x` and every `h ≥ 1`,
> `S^h(x) < x  ⟹  2^{A_h} > 3^h`.

**Proof.** `C_h ≥ C_1 = 2^{A_0} = 1 > 0` for `h ≥ 1`. From
`S^h(x) = (3^h x + C_h)/2^{A_h} < x` we get `3^h x + C_h < 2^{A_h} x`, hence
`(2^{A_h} − 3^h)x > C_h > 0`, and `x > 0` gives `2^{A_h} > 3^h`. ∎

So the first contracting index never comes *after* the first descent. The
non-contracting region is exactly the region where non-descent is automatic —
no pruning is possible there, ever. This is the precise reason a
non-descent-based search can only bite once the multiplier has turned over.

## 5. Lemma 2 — the offset bound before onset

> **Lemma 2.** If no `j < h` is contracting for `x`, then `C_h ≤ h·3^{h-1}`.

**Proof.** `C_h = Σ_{j=0}^{h-1} 3^{h-1-j} 2^{A_j}`. For each `j < h` the
hypothesis gives `2^{A_j} ≤ 3^j` (and `2^{A_0} = 1 = 3^0`), so every summand
is at most `3^{h-1-j}·3^j = 3^{h-1}`. There are `h` of them. ∎

## 6. Theorem — the onset bound

Write `A*(h)` for the least exponent with `2^{A*(h)} > 3^h`; exactly,
`A*(h) = bit_length(3^h)`. Define

```
M(h) := ⌊ h · 3^{h-1} / ( 2^{A*(h)} − 3^h ) ⌋ .
```

> **Theorem.** Let `h` be the **first** contracting index of `x` and suppose
> `S^h(x) ≥ x`. Then `x ≤ M(h)`.

**Proof.** `S^h(x) ≥ x` gives `3^h x + C_h ≥ 2^{A_h}x`, i.e.
`x(2^{A_h} − 3^h) ≤ C_h`. The left factor is positive since `h` is
contracting. Lemma 2 applies because `h` is the *first* contracting index, so
`C_h ≤ h·3^{h-1}`. Finally `A_h ≥ A*(h)` by minimality of `A*`, so
`2^{A_h} − 3^h ≥ 2^{A*(h)} − 3^h > 0`. Combining,
`x ≤ C_h/(2^{A_h} − 3^h) ≤ h·3^{h-1}/(2^{A*(h)} − 3^h)`, and `x` is an
integer. ∎

`M(h)` is one exact integer computation per depth. Computed values:

| `h` | `A*(h)` | `M(h)` |
|---:|---:|---:|
| 5 | 8 | 31 |
| 41 | 65 | 1 185 |
| 53 | 85 | 17 |
| 306 | 485 | 99 729 |
| 665 | 1 055 | 221 |
| 9 616 | 15 241 | 7 795 714 |
| 15 601 | 24 727 | 285 814 986 |
| 190 537 | 302 141 | **984 572 779 224** (max over `h ≤ 1 000 000`) |

`M(h)` is large precisely when `2^{A*(h)}/3^h` is close to 1, i.e. at a
near-resonance — so the record-setting depths are the good rational
approximations to `log₂3` **from above**. Through `h ≤ 3000` they are

```
1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306, 971, 1636, 2301, 2966, …
```

The convergent denominators approaching from above (`5, 41, 306, 15601`) are
all records, and between `306` and `15601` the records are the interpolating
**semiconvergents** `306 + 665k` — `665` being the previous convergent
denominator. So this is the repository's own resonance lattice (landmark memo
§VII.2) reappearing as the only place `M` can be large. It is not only the
convergents: an early draft of this memo said so and the test suite caught it.

## 7. Corollary — consuming Bařina

> **Corollary.** `max_{h ≤ 1 000 000} M(h) = 984 572 779 224 < 2^71`. Therefore
> a minimal Collatz counterexample `m` has **no** contracting index
> `h ≤ 1 000 000`: `2^{A_h(m)} ≤ 3^h` for all such `h`.

**Proof.** A minimal counterexample never descends below itself, so
`S^h(m) ≥ m` for every `h`. If some `h ≤ 1 000 000` were contracting, take the
first; the Theorem gives `m ≤ M(h) ≤ 984 572 779 224 < 2^71`. But Bařina
(2025) verified that every `n < 2^71` reaches 1, so `m` is not a
counterexample. Contradiction. ∎

The slack is ten orders of magnitude, so the depth `1 000 000` is a compute
budget, not a mathematical boundary.

**Diophantine reading.** Writing `θ_h = A*(h) − h·log₂3 ∈ (0,1)`, the
Theorem's hypothesis `m ≤ M(h)` becomes `θ_h ≲ h/(3m·ln2)`. So the *first*
contracting prefix of a minimal counterexample must sit at a rational
approximation `A*(h)/h` to `log₂3` of quality about `1/2^71` — the same
near-resonance condition that governs the cycle bounds
(Simons–de Weger; the convergents of `log₂3` in the landmark memo §VII.2).
An effective irrationality measure for `log₂3` would turn `1 000 000` into an
unconditional infinite statement; the known effective exponents are too weak
to beat the direct computation, which is why the number above is computed
rather than derived.

## 8. The scan — the trivial cycle is the only survivor

Lemma 1 says the first contracting index is at most the first descent index.
When is it **strictly** less? That is exactly the case where a non-descending
orbit survives past the onset of contraction.

> **Computation.** For every odd `x > 1` in the ranges below, the first
> contracting index equals the first descent index. Only `x = 1` contracts
> (at `h = 1`, the word `(2,2,2,…)`) and never descends.

| scan bound | odd starts | survivors `> 1` | depths thereby decided |
|---|---:|---:|---|
| `7 795 715` (verifier default) | 3 897 856 | 0 | all `h ≤ 10 000` |
| `1 447 674 322` (extended run) | 723 837 160 | 0 | all `h ≤ 60 000` |

Named controls: `x = 3` both at `h = 2`; `x = 7` both at `h = 4`;
`x = 27` both at `h = 37`; `x = 703` both at `h = 51`.

Since a survivor at first-contracting-index `h` obeys `x ≤ M(h)` (the
Theorem), a scan to `B` decides **every** depth `h` with `M(h) ≤ B` — over all
exponent words at once, with no exponent cap and no tree enumeration. The
`max M` column of the table in §6 supplies the depth reached: `M(h) ≤ 7 795 714`
for `h ≤ 10 000` and `M(h) ≤ 1 447 674 321` for `h ≤ 60 000`.

The extended run is reproducible with

```bash
VCO_XSCAN=1447674322 python3 contribution/packets/2026-07-24-contraction-onset/verify_contraction_onset.py
```

and takes about 8 minutes; the default bound keeps the verifier at a few
seconds for that stage.

## 9. What this does not do

- It does **not** prove Collatz, and produces no counterexample.
- It does **not** show the contracting region is empty at *every* depth. The
  bound is `M(h) < 2^71` for `h ≤ 1 000 000`; beyond that `M` keeps growing and
  the argument runs out. Making it unconditional needs an effective
  irrationality measure for `log₂3` sharper than what is available.
- It says **nothing** about the non-contracting region, which is where the
  whole difficulty lives — and which is exactly the atlas's supercritical
  region: `2^{A_h} ≤ 3^h` for every prefix is the same condition as
  `S_ρ = {q : Σ_{j<L} q_j ≥ ⌈ρL⌉ for every L}` in
  [`LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md`](../2026-07-22-landmark-pointwise/LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md)
  §6, the boundary object of Theorem 6.1.
- The `1 000 000` and `7 795 715` are compute budgets. Neither is sharp.

## 10. Adversarial audit: which quantifier does the work?

The corollary's universal quantifier is **"for every `h ≤ 1 000 000`"**, and it
is discharged by an exact finite computation of `M(h)` — not by an
extrapolation. The step that could silently be wrong is Lemma 2's hypothesis:
`C_h ≤ h·3^{h-1}` needs *every* earlier index to be non-contracting, and the
Theorem is stated only for the **first** contracting index for that reason. If
one applied the bound at a later contracting index the proof would be invalid,
because `C` can then contain terms with `2^{A_j} > 3^j`. The verifier checks
Lemma 2 only on indices strictly before the first contracting one, matching
the proof exactly.

The quantifier that is **assumed, not proved**, is Bařina's `n < 2^71`
verification. It is an external computational result; this packet consumes it
and cannot be stronger than it.

What this packet does *not* establish, and must not be read as establishing:
that a minimal counterexample exists, or that the non-contracting region is
non-empty for large depth. It constrains a hypothetical object.

## 11. Reproduce

```bash
python3 contribution/packets/2026-07-24-contraction-onset/verify_contraction_onset.py
python3 contribution/packets/2026-07-24-contraction-onset/test_verify_contraction_onset.py
```

Verifier runtime ~5.5 min (the `M(h)` table to 10^6 dominates; use `VCO_HMAX=300000` for a ~23 s run). Certificate:
`contraction_onset_certificate.json`. Knobs: `VCO_HMAX`, `VCO_XSCAN`,
`VCO_ORBITS`, `VCO_REDUCED`, `VCO_OUT`.

## 12. Related work — corrected 25 July 2026

**This packet re-derives Terras (1976) and refreshes Garner (1981).** The
original text of this section guessed that "Lemma 1 is elementary and is very
likely folklore; no priority search was made." The search was then made, and
the guess understated it: the concept is named, published, and central.

| This packet | Prior art |
|---|---|
| "first contracting index" — least `h` with `2^{A_h} > 3^h` | **coefficient stopping time** `κ(n)`, Terras (1976) |
| Lemma 1, descent requires contraction | `κ(n) ≤ σ(n)`, Terras (1976) |
| Theorem, `x ≤ M(h)` at the first contracting index | Terras's proof method: bound `β`, lower-bound `1−α`, get `n ≤ β/(1−α)` |
| §7 corollary at `h ≤ 10⁶` via Bařina `2^71` | same argument; Garner (1981) reached `κ(n) < 105,000` via verification to `2 × 10⁹` |

- R. Terras, *A stopping time problem on the positive integers*, **Acta Arith.
  30** (1976), 241–252 — introduces `κ(n)`, proves `κ(n) ≤ σ(n)`, and proves
  `κ = σ` for `κ(n) ≤ 2593`.
- L. E. Garner, *On the Collatz 3n+1 algorithm*, **Proc. AMS 82** (1981),
  19–22, [DOI](https://doi.org/10.1090/S0002-9939-1981-0603593-2) — extends to
  `κ(n) < 105,000` using continued-fraction convergents of `log₂3`.
- J. C. Lagarias, [annotated bibliography](https://arxiv.org/abs/math/0309224)
  entry 143, and [*The 3x+1 Problem: An Overview*](https://arxiv.org/abs/2111.02635)
  — the survey statements of the cocycle and of the coefficient stopping time.
  Theorems C and E there bound the same object more sharply than a naive
  `M(h)`, and should be read before any further work on this line.
- D. Bařina (2025), [DOI](https://doi.org/10.1007/s11227-025-07337-0) — the
  `2^71` input.
- Simons–de Weger (*Acta Arith.* 117, 2005) — the continued-fraction structure
  behind the near-resonance reading.

The offset recurrence and the window `3^m < 2^K ≤ (22/7)^m` remain the atlas's
own presentation of standard material
([`EXACT_COUNTEREXAMPLE_SEARCH.md`](../../proofs/EXACT_COUNTEREXAMPLE_SEARCH.md)).

**What is genuinely this packet's own, pending its own check:** the exact
`M(h)` table to `h ≤ 10⁶` with its record structure at convergents *and*
semiconvergents; the observation that `M(h)` grows slowly enough that a
10¹²-fold better verification bound buys only ~9.5× in `h`; and the exhaustive
odd-`x` scan to 1.45 × 10⁹ showing first-contraction and first-descent coincide
for every `x > 1`. That last statement is the coefficient-stopping-time
conjecture `κ = σ` restricted to first indices — **so it, too, is a known
conjecture and the scan is a verification of it, not a discovery.**
