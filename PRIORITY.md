# Priority search

## 0. CLOSED — every automatic parity transcript

Bell (2020), Corollary 1.2, proves that the lower density of every
`k`-automatic set is rational. López–Stoll (2021) prove that a rational
2-adic integer with a non-cyclic `3x+1` trajectory must have lower parity
density exactly `log₃2`. That number is irrational. Therefore no rational
non-cyclic trajectory has an automatic parity word in any base.

This strictly strengthens §7 below. The absence of a natural density is not a
surviving case because Bell controls `liminf` directly. See
[`contribution/packets/2026-08-01-automatic-density-closure/`](contribution/packets/2026-08-01-automatic-density-closure/).

**Priority status.** The two inputs are prior work. A targeted search found no
source stating this direct Collatz corollary. That is not a novelty claim.

Eleven packets carried the line "no literature-priority claim is made" or "no
priority search was made". This is the first search actually run, on
2026-07-25. It should have been run first.

**Headline: two of the repository's three most-cited results are subsumed by
prior work.** One genuinely new mechanism survives, and it happens to be the
only instrument pointed at what is now known to be the only remaining case.

Verdicts use: **SUBSUMED** (prior work proves it, or more) · **PARTLY NEW**
(new only on a stated remainder) · **APPARENTLY NEW** (nothing found;
provisional) · **REFRESH** (known method, updated number).

---

## 1. SUBSUMED — the supercritical exclusion

**What the repository claims.** `2026-07-24-supercritical-automatic-closure`:
99 of 109 enumerated supercritical words have `Φ(q) ∉ ℤ_{>0}`, via a proved
factor-complexity bound fed into Corollaries 4 and 7. And
`2026-07-22-automatic-transcript-rigidity` frames the supercritical stratum as
"exactly the whole remaining gap".

**Prior art.** J. López and P. Stoll, *The 3x+1 Periodicity Conjecture in ℝ*,
[arXiv:2101.12747](https://arxiv.org/abs/2101.12747) (2021). From the abstract,
read directly:

> "We prove that the `3x+1` conjugacy `Φ` maps aperiodic `v ∈ ℤ₂` onto aperiodic
> 2-adic integers provided that `liminf (h/ℓ) > ln(2)/ln(3)` where `h` is the
> number of 1's in the first `ℓ` digits of `v`, with the following constraint:
> if there is a rational 2-adic integer with a non-cyclic trajectory, then
> necessarily `liminf (h/ℓ) = ln(2)/ln(3)`."

"Aperiodic 2-adic integer" means irrational, i.e. `∉ ℚ_odd ⊇ ℤ_{>0}`. So:

> **aperiodic `q` with `liminf s_L/L > α` ⟹ `Φ(q) ∉ ℤ_{>0}`.**

Every one of the 109 survivors has an exact rational Perron density `ρ > α`,
certified in the packet by an integer witness `3^a > 2^b`. Their liminf is `ρ`.
**All 109 are excluded directly by this theorem — no complexity bound, no
Lemma D, no computation.** The packet's 99 is a strict subset of a 2021 result.

**Consequences beyond that packet.** Combining López–Stoll with the
repository's own drift wall (`liminf < α ⟹ Φ ∉ ℤ_{>0}`, itself prior art — see
§3):

| `liminf s_L/L` | status |
|---|---|
| `< α` | closed — drift wall, and prior art |
| `> α` | closed — **López–Stoll 2021** |
| `= α` **exactly** | **the entire remaining gap** |

The rigidity packet's "supercritical stratum is exactly the whole remaining
gap" is therefore **wrong as stated**. The gap is far narrower: it is the
single critical density `liminf s_L/L = log₃ 2`. That is a much sharper — and
much more encouraging — statement of where the problem lives, and the
repository did not know it.

## 2. APPARENTLY NEW — the factor-complexity lower bound

**The claim.** Landmark memo Corollary 4: if `q` is not eventually periodic and
`Φ(q) ∈ ℚ_odd`, then

```
limsup_k  p_q(k)/k  ≥  κ = 1/log₂(3/2) = 1.7095112913…
```

**Nothing found.** Searched López–Stoll (2009 and 2021), Bernstein–Lagarias
(1996), Monks–Yazinski, Lagarias's overview and both annotated bibliographies,
and the base-3/2 representation literature.

**Why it is plausibly new, stated precisely.** Every prior partial result
toward the Bernstein–Lagarias periodicity conjecture constrains **letter
frequency** — an abelian, one-dimensional statistic. Lagarias's Relation 2.31,
Monks–Yazinski Thm 2.7(b), and López–Stoll Thm 1 are all of that type. Corollary
4 constrains **factor complexity** — a *logically independent* statistic, not a
stronger one (Sturmian words realise every irrational density at `p(k)=k+1`, so
neither determines the other; corrected 2026-07-25) — and its
mechanism is different: pigeonhole on distinct length-`k` factors under
`(3/2)`-affine state growth, rather than `2^ℓ/3^h → 0`.

**And it is the right tool for what remains.** The complexity bound is
*insensitive to density* — which is exactly why it still bites at
`liminf = α`, the one case López–Stoll leaves open and where every
frequency-based argument is vacuous.

**Status: provisional.** A negative search result is not a priority claim. This
needs a real literature review, ideally by someone who knows the symbolic
dynamics literature, before it appears in a paper.

## 3. SUBSUMED — the drift wall

`2026-07-22-pointwise-drift-wall` Theorem 1: a divergent positive orbit has
`liminf s_L/L ≥ log₃ 2`.

Prior art: Lagarias's Relation 2.31; **Monks & Yazinski**, *The Autoconjugacy of
the 3x+1 Function*, Thm 2.7(b)
([PDF](https://monks.scranton.edu/files/pubs/AutoConjV13.pdf)), which gives
`liminf h/ℓ ≥ ln2/ln3` for divergent **rationals** — a strictly more general
statement than the positive-integer case. The named-family eliminations
(Thue–Morse, period-doubling, Rudin–Shapiro, paperfolding, Champernowne, normal
words) follow from it immediately and are therefore also not new.

## 4. PARTLY NEW — the Sturmian exclusion

Landmark memo Corollary 5: `q` Sturmian ⟹ `Φ(q) ∉ ℚ_odd`.

A Sturmian word of slope `θ` has letter density exactly `θ`. So López–Stoll 2021
kills every slope `θ > α` and Monks–Yazinski every slope `θ < α`. **New only at
the single slope `θ = α = log₃2`** — which is irrational, hence a legitimate
Sturmian slope, and which López–Stoll explicitly flag as needing special
attention.

The Fibonacci and golden-angle codings have slope `1/φ² ≈ 0.382 < α`, so those
specific exclusions were already known.

Sell Corollary 5 as a corollary of Corollary 4 at one exceptional slope. Never
as a headline.

**Note.** J. López and P. Stoll, *The 3x+1 Conjugacy Map Over a Sturmian Word*,
INTEGERS 9 (2009) A13 — the paper cited in the repository's own reference list
— does **not** prove this. It gives a 2-adic continued-fraction expansion, and
its abstract says outright: "It is unknown if there exists any aperiodic `v`
with an eventually periodic `Φ(v)`." The relevant paper is their 2021 one,
which the repository never cited.

## 5. REFRESH — contraction onset

`2026-07-24-contraction-onset` re-derives **Terras (1976)**. Its "first
contracting index" is the **coefficient stopping time** `κ(n)`; its Lemma 1 is
`κ(n) ≤ σ(n)`; its `M(h)` bound is Terras's own proof method. **Garner (1981)**,
[DOI](https://doi.org/10.1090/S0002-9939-1981-0603593-2), pushed it to
`κ(n) < 105,000` using continued-fraction convergents of `log₂3` and
verification to `2 × 10⁹`.

The packet reaches `h ≤ 10⁶` with Bařina's `2^71` — about 9.5× further from a
verification bound roughly 10¹² times larger. **A quantitative refresh, not a
theorem.** Not checked: whether a post-2020 extension already exists.

Full correction is in the packet.

## 6. FOLKLORE — Lemma D

The desubstitution complexity bound is the textbook argument. Allouche &
Shallit, *Automatic Sequences*, **Theorem 10.3.1** already gives the effective
bound `ρ_x(n) ≤ k·n·ρ(2) ≤ k·n·m²` for a `k`-automatic sequence from an
`m`-state DFAO. See also Klouda,
[TCS](https://doi.org/10.1016/j.tcs.2012.11.024), for computable upper bounds
on primitive substitution fixed points, and Cassaigne (1997) for exact
computation via bispecial factors. The `m₀`-parametrized limsup form appears
unstated, but a referee would call it folklore.

---

## 7. A new consequence, not just a correction

> **Superseded 2026-08-01.** Bell's 2020 theorem makes the lower density of
> every automatic set rational. The residual no-natural-density case below is
> therefore impossible at the irrational value `log₃2`. Section 0 gives the
> complete closure.

Combining López–Stoll 2021 with the repository's own Theorem 2 gives a sharper
statement than either alone. It is worth stating as a result.

> **Corollary (25 July 2026).** A divergent Collatz orbit whose parity word is
> 2-automatic has **no natural one-density**.

**Proof.** Let `q` be the parity word of a divergent positive orbit, so `q` is
aperiodic and `Φ(q) = n ∈ ℤ_{>0} ⊂ ℚ_odd`.

1. The drift wall gives `liminf s_L/L ≥ α`.
2. López–Stoll 2021 gives: aperiodic and `liminf s_L/L > α` implies
   `Φ(q) ∉ ℚ_odd`. So `liminf s_L/L ≤ α`.
3. Hence `liminf s_L/L = α` exactly.
4. Suppose `q` is 2-automatic and its natural density `ρ` exists. Then
   `ρ = liminf s_L/L = α`.
5. But Theorem 2 of `2026-07-22-automatic-transcript-rigidity` says no
   2-automatic word has natural density exactly `α` — automatic densities are
   rational (Cobham) and `α = log₃2` is transcendental (Gelfond–Schneider).

Contradiction, so `ρ` does not exist. ∎

**Why this matters.** It removes the *entire* natural-density case from the
2-automatic Gap. What survives is exactly the regime of that packet's own
**Witness 2** — `q(n) = 1` iff `n` is even or `bitlength(n)` is odd, whose
`s_L/L` oscillates between `2/3` and `5/6` and has no limit. The target is no
longer "the supercritical stratum" or even "the critical density"; for
2-automatic words it is:

> words with no natural one-density, whose `liminf s_L/L` is exactly `log₃2`.

That is a very small and very specific object. Witness 2 itself has
`liminf = 2/3 > α`, so **López–Stoll kills Witness 2 too** — the packet's
flagship density-proof witness is no longer a survivor. Whether any 2-automatic
word achieves `liminf = α` exactly while having no natural density is now the
open question, and Theorem 2's proof suggests it is tightly constrained.

**Status.** This is a deduction from three published/proved inputs, all cited.
No new mechanism. But it is the sharpest available statement of the 2-automatic
gap and it did not exist before today.

---

## What this changes

**The claim ledger.** The headline "99 of 109 supercritical survivors closed"
must be retired. The correct statement is that they were already closed in
2021, and the packet's contribution is the machinery, not the conclusion.

**The frontier.** The remaining gap is not "the supercritical stratum". It is
`liminf s_L/L = log₃ 2` **exactly** — a measure-zero, critically-tuned class.
Everything above and below it is closed. This is genuinely useful and should
propagate into `STATE.md`, `TARGETS.md` and `COUNTEREXAMPLE_SHAPE.md`.

**The direction.** The one apparently-new instrument, the complexity bound, is
also the only one that survives at the critical density. That is a coincidence
worth taking seriously: it is the sole reason the repository has anything to
contribute at the exact point where the problem now demonstrably sits.

**The lesson.** Eleven packets were written before a single priority search.
The search took one session and retired two headline results. Run it first, on
every future packet, before the memo is written — not after.

## Confidence and what is not checked

- López–Stoll 2021: abstract read directly from arXiv by the author of this
  file; full text read by an agent. The abstract alone is sufficient for the
  subsumption finding. **Ben should read it himself before any external
  submission** — it is now load-bearing for a major downgrade.
- Monks–Yazinski Thm 2.7(b): relied on López–Stoll's verbatim citation; full
  text not obtained.
- MathSciNet was not accessible. No review-database search was performed.
- Nothing here has been checked against the post-2021 literature systematically.
