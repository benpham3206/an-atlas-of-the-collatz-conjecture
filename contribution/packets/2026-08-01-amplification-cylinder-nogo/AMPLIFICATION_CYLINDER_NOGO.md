# Amplification: the inverse/cylinder route is killed at the handoff

**Date.** 2026-08-01.
**Branch served.** Amplification — the never-entered half of the architecture
(`TARGETS.md` §1).
**Status.** Kill criterion fired, honestly reported; the exact missing
implication is named. This packet proves no Collatz result in either
direction.
**Outcome class (per `HAIL_MARY_PROMPT.md` §6).** 4 (kill criterion firing) + 5
(precise, defended statement of where the gap sits).

---

## Approach card (written before the build)

**Claim 1 (numbered).** The only two arithmetic families attached to a single
divergent orbit — its inverse tree and its forward 2-adic cylinder family —
both provably fail to supply the positive-log-density exceptional family that
the amplification branch requires.

**Domain and quantifiers.** Terras map `T` on positive integers. Universal
quantifiers: every `y ≥ 1`, every `L ≥ 1`, every `m ≥ 1`, every `i ≤ L`
(Theorem A); every `j ≥ 0`, every `y` (Theorem B). No asymptotic, no density,
no float anywhere in the proved part.

**Sources.** Terras 1976 (residue bijection); Bernstein–Lagarias 1996 (2-adic
conjugacy); Tao 2019/2022 ([arXiv:1909.03562](https://arxiv.org/abs/1909.03562))
for the logarithmic-density descent the no-go is measured against; repo:
`TARGETS.md` §1, `2026-07-24-contraction-onset` (supercritical prefixes).
Last checked: 2026-08-01.

**Status label.** Theorem A and B: proved here (elementary; Theorem A is a
corollary of the Terras affine form — folklore strength, no priority claim).
The no-go conclusion: a synthesis, claimed as a route-kill, not as a theorem
about Collatz.

**Kill criterion (written before the build).** From `TARGETS.md` §1, verbatim:
*if the density transfer needs control of the orbit of one fixed integer
rather than of a set, the argument is circular — test on the smallest
non-trivial case first and stop if it fires.* Test case: `y = 27`, `L = 20`,
`m = 1`.

---

## The atomic claim

> **Theorem A (tracking time = 2-adic proximity).** Let `x ≠ y` be positive
> integers, `v = v₂(x − y)`, and `u = (x − y)/2^v` (odd). Then `x` and `y`
> share exactly their first `v` parity symbols; writing `s_i` for the number
> of ones in the shared length-`i` prefix,
>
> ```
> T^i(x) − T^i(y)  =  3^{s_i} · 2^{v−i} · u        (0 ≤ i ≤ v),
> ```
>
> and at `i = v` the difference is `3^{s_v}·u`, an **odd** multiple of a power
> of 3, so `v₂(T^v(x) − T^v(y)) = 0`: the `(v+1)`-th parity symbols differ and
> no further tracking is forced.

**Proof.** `x ≡ y (mod 2^v)` and the Terras bijection give the shared prefix
of length exactly `v` (agreement mod `2^v` forces `v` symbols; the difference
being exactly divisible by `2^v` and no more makes the `(v+1)`-th symbols
differ — this is the isometry form of the Bernstein–Lagarias conjugacy). The
affine form of a length-`i` prefix, `T^i(n) = (3^{s_i} n + c_i)/2^i` with
`c_i` depending only on the word, is immediate by induction; subtracting the
two instances eliminates `c_i` and gives the displayed identity. At `i = v`
the difference is `3^{s_v} u` with `u` odd, hence has valuation `0`. ∎

**Corollary A1 (supercritical floor).** If `x > y` (so `u ≥ 1`) and every
prefix of the shared word is supercritical (`3^{s_i} ≥ 2^i`, equivalently
`s_i/i ≥ log₃2`), then

```
T^i(x) ≥ 2^v·u = x − y        for every 0 ≤ i ≤ v.
```

A cylinder start `x = y + 2^L m` is therefore **proved** to stay above
`x − y` for exactly `v₂(x − y)` steps — and, at the handoff state
`z = T^v(x)`, is at 2-adic **unit distance** from every state it could track.
The control bought by a perturbation is exactly its own 2-adic valuation, and
it expires with the orbit still uncontrolled and still high
(`z ≥ x − y`, since `3^{s_v} ≥ 2^v`).

> **Theorem B (inverse family has vanishing relative minima).** If `T^j(x) = y`
> then `min-orbit(x) ≤ y`. In particular the pure-doubling preimage
> `x = 2^j y` has `min-orbit(x) ≤ y = 2^{−j}·x`.

**Proof.** `x`'s orbit passes through `y`, so its minimum is at most
`min(y, min-orbit(y)) ≤ y`. For `x = 2^j y` the orbit begins
`2^j y, 2^{j−1} y, …, y`, so `min-orbit(x) ≤ y = 2^{−j} x`. ∎

---

## Why this kills the route

The amplification target (`TARGETS.md` §1) asks: convert one divergent orbit
into a **positive logarithmic-density set of orbits whose minima exceed a
growing function**, contradicting Tao. Note first that a divergent (non-cyclic,
unbounded) orbit has `liminf = ∞`: if its `liminf` were finite, some value
would recur (finite set, deterministic map), forcing a cycle. So the orbit's
tail minima `μ(t) = min_{s≥t} T^s(N)` tend to infinity — the *tail* is not the
obstruction. The two candidate families:

**Inverse tree.** Every `x` with `T^j(x)` on the orbit gets a free descent to
the join point: `min-orbit(x) ≤ y_join`, while `x` itself can exceed the join
point by `2^j` (Theorem B). Tao's exceptional set needs minima **growing with
the start**; the inverse tree's large elements have relative minima
`≤ 2^{−j}` — they are Tao's *good* set, with arbitrarily small relative
minima. **No exceptional family here.**

**Forward cylinders.** The class `C_{y,L} = {y + 2^L m : m ≥ 1}` has natural
density `2^{−L}` and, when `y`'s prefixes are supercritical, every member
stays `≥ x − y` for `L` steps (Corollary A1). But `L = v₂(x − y)` is finite
by construction, and Theorem A's handoff shows the control expires at unit
2-adic distance from the orbit: the handoff state `z = T^L(y) + 3^{s_L} m`
(`m` odd) shares **not one further forced parity symbol** with any orbit
point. What happens after step `L` is information the divergent orbit does
not contain. "Stays high for `L ≈ log₂ x` steps" is explicitly dominated work
(`HAIL_MARY_PROMPT.md` §4), and on the smallest test case it is also false as
a certificate: `x = 27 + 2²⁰` tracks above `2²⁰` for exactly 20 steps, then
drops below the floor at step **34** and later reaches 1.

**The kill criterion fires.** Supplying the missing step — a lower bound on
the **full** orbit minimum of the handoff states `z = T^L(y) + 3^{s_L}·u`,
`u` odd, ranging over a positive-density family of `(y, L, u)` — requires
control of the orbit of one fixed integer at a time (`z`), with zero symbolic
input from the original divergent orbit. That is the pointwise statement the
transfer was meant to supply. `TARGETS.md` §1's kill criterion is therefore
met, and the inverse/cylinder route to amplification is **BLOCKED** — reopened
only by a materially new mechanism, per `HAIL_MARY_PROMPT.md` §5.

### The exact missing implication, named

> **Permanence at the handoff.** From "the orbit of `N` is unbounded with all
> prefixes supercritical", deduce that for a positive-log-density family of
> starts `x`, the orbit minimum of `T^{v₂(x−y)}(x)` — a state at 2-adic unit
> distance from the tracked orbit — stays above a growing function of `x`.
>
> Equivalently: any lemma that converts **finite** tracking
> (`T^i(x) ≥ x − y` for `i ≤ v₂(x − y)`) into a bound on the **infinite**
> orbit minimum. Theorem A shows finite tracking is free and maximal at
> exactly `v₂(x − y)` steps; the permanence lemma is precisely the content
> that remains.

This is a sharper location than "no theorem exists": the gap is not in
generating provably-high excursions (Corollary A1 generates them at positive
density, for free) but in their **persistence past the 2-adic proximity
scale**. Any future entrant to the amplification branch must either prove a
permanence lemma or build its exceptional family by a mechanism that is not a
2-adic cylinder and not an inverse tree.

---

## Failed-route records

| Route | Test | Result | Missing invariant/lemma |
|---|---|---|---|
| Inverse tree of the divergent orbit | Theorem B + exact instance `x = 2⁴⁰·27` | Killed: `min-orbit(x) = 1 ≤ 27 = 2⁻⁴⁰·x`; large elements are maximally Tao-non-exceptional | A height-transfer principle bounding preimages' minima **below by a growing function of their size** — none exists; doubling chains forbid it |
| Forward cylinders `y + 2^L m` | Theorem A + named case `y=27, L=20, m=1` | Killed as a certificate route: tracking is exact but expires at `L = v₂(x−y)`; handoff at unit 2-adic distance; test case drops below the floor at step 34 and reaches 1 | The permanence lemma above |
| Negative perturbations `y − 2^L m` | Theorem A applies with `u < 0` | Not pursued: tracked values are **below** the orbit, sign uncontrolled; cannot lower-bound minima | — |
| Word-property families (e.g. "all prefixes supercritical") | Entropy of the constraint `s_i ≥ αi ∀i ≤ L` | Density decays exponentially in `L` (level-set dimension `H(α) < 1`, repo `dimension_bracket.py`); no positive-density family of this shape exists | — |

## Kill criteria and outcomes (all written before the build)

1. **K1.** If the tracking identity fails on any exact instance → no-go
   collapses. **Outcome: did not fire.** 49,195 identities over 3,000 random
   `(y, L, m)`, two independent implementations (direct iteration vs. affine
   form from the word), zero mismatches.
2. **K2.** If the handoff state retains *structural* 2-adic proximity to the
   tracked orbit (`v₂ > 0` for odd `m`) → re-entry possible, second leg fails.
   **Outcome: did not fire.** 2,000 handoffs: `v₂(T^L(x) − T^L(y)) = v₂(m)`
   every time; `0` for odd `m`.
3. **K3.** If the inverse tree's large elements have minima comparable to
   their size on the smallest case → inverse route survives. **Outcome: fired
   against the route.** `x = 2⁴⁰·27` has `min-orbit(x) = 1`.
4. **K4 (the TARGETS.md §1 criterion).** If the density transfer needs control
   of one fixed integer's orbit → circular; stop. **Outcome: FIRED.** The
   permanence lemma quantifies over individual handoff-state orbits; the
   smallest test case confirms the transfer cannot certify exceptionality past
   the handoff.

## Verification

```
python3 verify_amplification_nogo.py      # writes amplification_nogo_certificate.json
python3 test_verify_amplification_nogo.py # 8 tests incl. 2 RED mutants; also runs under pytest
```

Exact integer arithmetic only; the two implementations of the tracking
identity share only the input integers; the certificate is replayable from
the inputs. No proved statement depends on numpy or floats.

## Prior art and honesty notes

- Theorem A is a corollary of the Terras affine form and the isometry of the
  Bernstein–Lagarias conjugacy — **folklore strength, no priority claim**.
  The supercritical floor (Corollary A1) is the contraction-onset packet's
  own inequality read in the perturbation direction. The packet's content is
  the **synthesis**: the kill of both natural families and the naming of the
  permanence gap. A targeted search on 2026-08-01 found no source stating
  this route-kill; that is not a novelty claim.
- The no-go is independent of the entropy hypothesis in the amplification
  statement: it kills the cylinder/inverse *mechanism*, whichever symbolic
  closure the divergent orbit has. A mechanism consuming positive entropy
  directly (not via cylinders) is untouched by this packet.
- **Lean.** Scoped out per `HAIL_MARY_PROMPT.md` §8: the permanence statement
  needs limits and a liminf and cannot be written in `formal/`'s plain Lean 4
  core; Theorem A is formalizable but folklore, and formalizing it adds no
  assurance beyond the exact two-path verifier. Not faked.
- The quantifier doing the work in the no-go is the **universal over handoff
  states** in the permanence lemma. It is **assumed by no step here** — the
  packet's point is that nothing in the repository or the tracked orbit
  supplies it.

## Related literature finding (Target 4 side-note)

Bell 2020 ([arXiv:2002.07256](https://arxiv.org/pdf/2002.07256), §6)
explicitly raises as an **open question** whether lower/upper densities of
morphic sets are algebraic, and suspects they are. The residual morphic case
of `TARGETS.md` §4 is therefore blocked on a named open problem in the source
paper itself, not merely on an unattempted extension. Recorded here so the
next session does not re-search it. Last checked: 2026-08-01.
