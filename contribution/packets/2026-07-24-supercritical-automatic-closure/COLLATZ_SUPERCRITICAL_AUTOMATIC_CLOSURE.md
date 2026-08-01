# Closing 99 of the 109: the supercritical automatic stratum was never density-bound, it was complexity-bound

**Date:** 24 July 2026
**Status:** one atomic claim, proved, with an exact finite certificate per
word. **Not** a proof of the Collatz conjecture, **not** a counterexample,
and **not** a closure of the supercritical automatic stratum — 10 explicit
words survive and are named in §8. No literature-priority claim is made.

> ## ⚠ PRIORITY CORRECTION (25 July 2026) — this result is subsumed
>
> A literature search run after this packet was written found that **all 109
> words were already excluded in 2021**, by a theorem this repository had not
> cited.
>
> López & Stoll, *The 3x+1 Periodicity Conjecture in ℝ*,
> [arXiv:2101.12747](https://arxiv.org/abs/2101.12747), prove: `Φ` maps an
> aperiodic `v` to an **aperiodic** (i.e. irrational, i.e. `∉ ℚ_odd`) 2-adic
> integer whenever `liminf s_L/L > log₃2`.
>
> Every survivor here has an exact rational density `ρ > α`, certified in §8 by
> an integer witness `3^a > 2^b`. Their liminf is `ρ`. So all 109 fall to that
> theorem directly — **no complexity bound, no Lemma D, no computation.**
>
> The conclusion of this packet is therefore not new, and "99 of 109
> supercritical survivors closed" is retired as a headline claim. What remains
> of value: Lemma D and the exact factor-language machinery (still needed at
> the critical density, where every density argument is vacuous), the measured
> saturation of the method, and the verifier.
>
> **The more important consequence** is in `PRIORITY.md` §1: combined with the
> drift wall, López–Stoll narrows the entire remaining gap from "the
> supercritical stratum" to the single critical density
> `liminf s_L/L = log₃2` **exactly**.

**Companion executable evidence:** `verify_supercritical_closure.py`,
`test_verify_supercritical_closure.py`, `verify_supercritical_closure.out`,
`supercritical_closure_certificate.json`, and the zero-`sorry` Lean module
[`formal/Formal/CollisionPrinciple.lean`](../../../formal/Formal/CollisionPrinciple.lean).

---

## 1. The claim

> **Claim.** Of the **109** supercritical primitive-uniform survivors
> enumerated by
> [`2026-07-22-automatic-transcript-rigidity`](../2026-07-22-automatic-transcript-rigidity/),
> **99** satisfy `Φ(q) ∉ ℤ_{>0}` — proved, not screened. **97** of those need
> no input beyond exact integer arithmetic on the word's own factor language.
> All **56** binary-morphism survivors are closed. **10** ternary-coded words
> remain open, and §8 shows their survival is not an artefact of a loose
> bound.

The named example of that packet — Witness 1 of its Theorem 3, the fixed
point of `σ(0)=11, σ(1)=10` from seed `1`, one-density `ρ = 2/3` — was
previously excluded only on a finite window (`Φ(u) ∉ {1,…,2^507−1}`). Its
kill certificate here is one integer comparison:

```
3^27 < 2^43          (7 625 597 484 987  <  8 796 093 022 208)
```

## 2. Kill criteria, written before the build

1. An exact factor set that disagrees with the factors actually observed in
   a long prefix (either direction) — the language machinery is wrong.
   *Verifier: five lengths on eight enumerated words. Test suite: ten
   lengths on the named witness. Equality in every case.*
2. A word whose proved complexity bound `c` falls **below** an exactly
   computed `p_u(n)/n` — Lemma D is wrong. *Checked at five depths on the
   named witness, up to n = 1024.*
3. `f(a+b) > f(a) + f(b)`, or the derived `ℓ·f(m) > f(ℓ)·(m+ℓ)`, for the
   maximal-ones function — the Fekete step that makes `f(ℓ)/ℓ` an
   admissible `β` is wrong. *Both checked on grids.*
4. The two `Φ` engines (lift cocycle vs modular series) disagreeing, or
   either disagreeing with a true Terras orbit. *2 000 orbits, mod 2^64.*
5. Two orbit positions with equal length-`k` parity blocks, both states
   below `2^k`, and **unequal** states — the collision principle is wrong.
   *17 565 block pairs over 600 orbits.*
6. Any rational one-density comparing **equal** to `α` — Gelfond–Schneider
   would be false.
7. A word in the rigidity packet's survivor list that this sweep fails to
   reproduce. *All 109 reproduced.*
8. `sorryAx` in `#print axioms`. *Absent.*

None fired. Every check is in the certificate.

## 3. What was actually open

The rigidity packet proved the trichotomy and closed the subcritical and
critical strata. Its supercritical stratum was left as **109 words excluded
only on a finite lift window** — "if `Φ(q) ∈ ℤ_{>0}` then `Φ(q) ≥ 2^505`".
That is a screen, not a theorem.

Meanwhile the landmark packet had already proved two pointwise inequalities
that bite exactly here. For `q` not eventually periodic with
`Φ(q) ∈ ℚ_odd`, and `C := limsup_k p_q(k)/k`:

| | statement | source |
|---|---|---|
| **Corollary 4** | `C ≥ κ = 1/log₂(3/2) = 1.7095112913…` | `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md` §V |
| **Corollary 7** | if every length-`ℓ` factor has `≤ βℓ + C₀` ones with `β > α`, then `C ≥ 1/(β log₂3 − 1) = α/(β − α)` | ibid. |

Neither had ever been applied to the stratum, for one reason: **nobody had a
bound on `C`.** The rigidity packet computes densities, periods and lift
bits; it never computes factor complexity. Corollary 7 in particular was
stated without a written proof at the time of this packet (proved later in
`../2026-08-01-corollary-7-proof/`; this packet's kill arithmetic is
unchanged).

So the gap was not a missing theorem. It was a missing *number* — and the
number is finitely computable.

Note also that `α/(β−α)` at `β = 1` is `α/(1−α) = κ`: Corollary 7 contains
Corollary 4 as its endpoint. The verifier checks that identity against the
certified bracket for `α`.

## 4. Lemma D — a proved, finitely computable bound on `C` (new here)

Let `u` be the fixed point of a `k`-uniform morphism `σ` on `d` letters
(`σ(seed)[0] = seed`), and let `q = τ(u)` for a letter-to-letter coding `τ`,
so `p_q ≤ p_u`.

> **Lemma D.** For every `m₀ ≥ 2`,
> ```
> limsup_n p_u(n)/n  ≤  max_{ m₀ ≤ m ≤ k·m₀ }  p_u(m+1)/(m−1).
> ```

**Proof.** Write `a_r = ⌊(n−2)/k^r⌋`, so `a_{r+1} = ⌊a_r/k⌋`, and put
`m_r = a_r + 1`. A length-`n` factor of `u` starting at `t = i·k^r + o` with
`0 ≤ o < k^r` lies inside `σ^r(u_i ⋯ u_{i+M})` where
`M = ⌊(o+n−1)/k^r⌋ ≤ m_r`, so it is determined by a factor of length
`≤ m_r + 1` together with the offset `o`. Hence

```
p_u(n)  ≤  p_u(m_r + 1) · k^r .
```

Since `a_r ≤ (n−2)/k^r`, we get `k^r ≤ (n−2)/(m_r − 1)` whenever `m_r ≥ 2`.
Finally, write `M = m₀ − 1 ≥ 1` and take the least `r` with
`a_r ≤ kM + k − 1 = k·m₀ − 1`; for `n` large enough that `r ≥ 1`, the
previous term satisfies `a_{r−1} ≥ k(M+1)`, hence
`a_r = ⌊a_{r−1}/k⌋ ≥ M + 1 = m₀`. So `m₀ ≤ a_r ≤ k·m₀ − 1`, i.e.
`m_r ∈ [m₀, k·m₀]`. Combining, `p_u(n)/n ≤ p_u(m_r+1)/(m_r−1)` for all
large `n`, which is what a `limsup` needs. ∎

The right-hand side is a **finite exact computation**, because the language
of `u` is finitely presented: `L₂(u)` is the least fixed point of

```
F(P) = { internal pairs of σ(a) : a reachable from seed }
     ∪ { (last σ(a), first σ(b)) : (a,b) ∈ P } ,
```

and for `k^R ≥ n` every length-`n` factor is a window of `σ^R(a)σ^R(b)` at
an offset in `[0, k^R)` for some `ab ∈ L₂(u)`. The verifier computes `L₂`
by that closure and enumerates the windows; the result is the **complete**
factor set, not a prefix sample, and it is checked against brute-force
prefix enumeration (five lengths on eight enumerated words in the verifier,
ten on the named witness in the test suite).

Because `p_u` is nondecreasing, the window maximum is evaluated on a
geometric partition `m₀ = A₀ < ⋯ < A_s = k·m₀` (ratio `201/200`), using
`p_u(m+1)/(m−1) ≤ p_u(A_{i+1}+1)/(A_i−1)` on `[A_i, A_{i+1}]`. The run uses
`m₀ = 192`, so the bound sits within about 1.5 % of the true constant.

## 5. The admissible `β` — also a finite exact computation

Let `f(ℓ)` be the maximal number of coded ones in a length-`ℓ` factor of `q`.
`f` is subadditive (split a long factor), so by Fekete `f(ℓ)/ℓ` decreases to
the asymptotic maximal factor density, and **for every single `ℓ`**

```
f(m) ≤ ⌈m/ℓ⌉ f(ℓ) ≤ (f(ℓ)/ℓ)·m + f(ℓ)   for all m.
```

That is exactly Corollary 7's hypothesis with `β = f(ℓ)/ℓ` and `C₀ = f(ℓ)`.
So one exact factor-language computation at one length `ℓ` (the run uses
`ℓ = 512`) supplies a legitimate `β`. No asymptotics, no cited dynamics.

**Variant with one cited classical input.** A primitive substitution
subshift is uniquely ergodic, so factor one-densities converge to `ρ`
*uniformly* — the same standard fact `PRIMITIVE_UNIFORM_OBSTRUCTION.md` uses
in its step 1 (Queffélec; Allouche–Shallit §8.4). Then the asymptotic
maximal factor density **is** `ρ`, and `β = ρ` is admissible. This is
strictly better since `ρ ≤ f(ℓ)/ℓ`, and it closes 2 words the self-contained
route misses.

## 6. The kill, as one integer comparison

With `β = a/b` and a proved bound `c = u/v ≥ C` (lowest terms), Corollary 7
says `c ≥ α/(β − α)`, i.e. `β·c/(1+c) ≥ α`. So the contradiction fires iff

```
   β · c/(1+c) < α        ⟺        3^(a·u)  <  2^(b·(u+v)).
```

Corollary 4 is the `β = 1` case: `3^u < 2^(u+v)`.

Both are exact integer comparisons — a few thousand bits with `β = ρ`, a few
tens of thousands with `β = f(512)/512`. For Witness 1, `c = 27/16` and the
`κ` certificate is `3^27 < 2^43`; its `β = ρ = 2/3` certificate is
`3^54 < 2^129`, and its self-contained one is `3^4617 < 2^11008`.

## 7. Why the conclusion needs no periodicity hypothesis

The rigidity packet labels its survivors aperiodic by a **numeric** KMP
control. Corollaries 4 and 7 require genuine aperiodicity, so that label
would be load-bearing. It is not needed here, because both branches close:

* **`q` eventually periodic.** If `Φ(q) = n ∈ ℤ_{>0}` then the `T`-orbit of
  `n` is eventually periodic (`PARTIAL_THEOREMS.md` Theorem 3), so it enters
  a cycle whose parity period has `a` ones in length `L`. The natural
  density of an eventually periodic word is its period's density, so
  `a/L = ρ` (the Perron frequency, which exists for a primitive substitution
  fixed point). The cycle equation `2^L x = 3^a x + C` with `C > 0` forces
  `2^L > 3^a`, i.e. `a/L < α`. Every word in the sweep carries an exact
  witness `3^a > 2^b` for `ρ > α`. Contradiction.
* **`q` aperiodic.** Corollary 4 / Corollary 7 with the computed `c` and
  `β`. Contradiction.

So for every word the second branch closes — that is, for all 116 of the
126 — `Φ(q) ∉ ℤ_{>0}` holds **unconditionally**, with no reliance on the
rigidity packet's numeric aperiodicity label. In particular none of them is
the parity transcript of a divergent positive orbit.

## 8. Results

Sweep: every primitive uniform binary morphism of length `≤ 4` and every
primitive uniform ternary morphism of length `2` under all six nonconstant
codings, all prolongable seeds — **126** distinct words with exact rational
`ρ > α` (a superset of the rigidity packet's 109 survivors, which this sweep
reproduces exactly; the extra 17 are words that packet had classified as
numerically periodic or deduplicated away).

| route | words closed |
|---|---:|
| Corollary 4 (`C < κ = 1.7095112913…`) | 30 |
| Corollary 7 with `β = f(512)/512` (self-contained) | 114 |
| Corollary 7 with `β = ρ` (unique ergodicity) | 116 |
| **union** | **116 of 126** |

Against the rigidity packet's survivor list: **97 of 109** closed
self-contained, **99 of 109** with the unique-ergodicity variant, **10**
open. All 10 are ternary-coded; **no binary survivor remains**.

Thresholds and outcomes by density, over the full 126-word sweep
(`α/(ρ−α)` is the complexity constant a survivor would have to exceed):

| `ρ` | `α/(ρ−α)` | words | closed |
|---|---:|---:|---:|
| 2/3 | 17.6548 | 73 | 73 |
| 5/7 | 7.5691 | 2 | 2 |
| 3/4 | 5.2988 | 36 | 32 |
| 4/5 | 3.7318 | 9 | 6 |
| 5/6 | 3.1172 | 4 | 2 |
| 6/7 | 2.7891 | 2 | 1 |

**The 10 that survive, and why it is not slack.** For each, the verifier
records the *exact* factor count `p_u(1537)`. In all ten cases the exact
ratio `p_u(1537)/1537` **already exceeds** `α/(ρ−α)`:

| σ | seed | coding | ρ | proved `C ≤` | exact `p_u(1537)/1537` | threshold |
|---|---:|---|---|---|---|---|
| `01,02,10` | 0 | 110 | 5/6 | 261/64 = 4.078 | 6146/1537 = 3.999 | 3.117 |
| `01,02,20` | 0 | 110 | 3/4 | 95/16 = 5.938 | 8960/1537 = 5.829 | 5.299 |
| `01,02,20` | 0 | 101 | 3/4 | 95/16 | 5.829 | 5.299 |
| `01,02,20` | 2 | 110 | 3/4 | 95/16 | 5.829 | 5.299 |
| `01,02,20` | 2 | 101 | 3/4 | 95/16 | 5.829 | 5.299 |
| `01,12,00` | 0 | 110 | 4/5 | 95/16 | 5.829 | 3.732 |
| `01,12,00` | 1 | 110 | 4/5 | 95/16 | 5.829 | 3.732 |
| `01,20,00` | 0 | 110 | 6/7 | 101/32 = 3.156 | 4610/1537 = 2.999 | 2.789 |
| `01,20,10` | 0 | 110 | 5/6 | 27/8 = 3.375 | 5121/1537 = 3.332 | 3.117 |
| `01,20,11` | 0 | 110 | 4/5 | 97/16 = 6.063 | 9216/1537 = 5.996 | 3.732 |

So tightening Lemma D cannot close any of them. These ten words are simply
complex enough to satisfy the complexity–density inequality. **The frontier
of the enumerated supercritical stratum is now these ten automata, not one
hundred and nine.**

## 9. What this does not do

- It does **not** close the supercritical automatic stratum. Theorem 1 of
  the rigidity packet's Gap statement — *no divergent Collatz orbit has a
  2-automatic parity word* — remains open, and the ten words above are inside
  it.
- It does **not** extend to 2-automatic words in general. Every conclusion
  here needs a computed `C`, and `C` is only computable this way for words
  presented as a coding of a uniform-morphism fixed point. A DFAO with many
  states can have `C` far above every threshold in the table.
- It does **not** touch **Witness 2** of the rigidity packet's Theorem 3
  (`q(n)=1` iff `n` even or `bitlength(n)` odd). That word is outside this
  sweep, and worse: it contains arbitrarily long all-ones runs (an entire
  even dyadic shell), so `f(ℓ) = ℓ` and its admissible `β` is `1`. The
  density route then degenerates to `C ≥ α/(1−α) = κ`, i.e. to Corollary 4,
  and gains nothing. The word that was built to be density-proof is also
  the word this packet's mechanism cannot reach — which is the right
  outcome, and worth stating plainly.
- It does **not** prove or disprove the Collatz conjecture, and it produces
  no counterexample candidate. Every closed word is *removed* from the
  candidate pool.
- It adds no new inequality. Corollaries 4 and 7 are the landmark packet's;
  Lemma D and the exact-language computation are what this packet supplies.
- `p_u(1537)/1537` in the table is an **exact rational**, not a proof about
  `limsup`. It shows the ten survivals are not bound slack; it is not itself
  a lower bound on `C`.

## 10. Adversarial audit: which quantifier does the work?

The chain is
`Φ(q) ∈ ℚ_odd` **⇒** (Theorem 3, landmark memo) `p_q(K_N) ≥ N+1` for every
`N` **⇒** `C ≥ α/(β−α)` **⇒** contradiction with `C ≤ c`.

The universal quantifier that carries it is **"for every `N`"** in Theorem 3,
and Theorem 3 is *proved* there (Lemmas 1–2 plus the exact Green expansion),
not assumed. Its finite core — a repeated length-`k` parity block in an orbit
that is not eventually periodic forces a state `≥ 2^k` — is now machine-checked
in `formal/Formal/CollisionPrinciple.lean`, zero `sorry`.

The quantifier this packet had to *supply* is **"for every `n`"** in
`p_u(n) ≤ c·n`. That is Lemma D, and it is proved, with the exact factor
counts feeding it computed completely rather than sampled. This is the one
place where a bug would be invisible to the rest of the pipeline, so it
carries two independent checks: the exact factor sets are compared against
brute-force prefix enumeration, and the resulting bound is compared against
exact `p_u(n)/n` at five larger depths.

The quantifier that is **assumed, not proved**, in the 2-word improvement of
§5 is the uniform Birkhoff property of primitive substitutions. It is
classical and cited, and the 97-word self-contained count is reported
separately precisely so that the reader can discount it.

One thing that could still be wrong and would not be caught: if `L₂(u)`
computed by the least fixed point were a *proper subset* of the true pair
set, every downstream factor set would be too small and `c` too small,
producing spurious kills. That is why kill criterion 1 checks containment in
**both** directions against observed prefixes, and why `pairs_exact` is
separately tested for σ-closure and for equality with the observed pairs.

## 11. Reproduce

```bash
python3 contribution/packets/2026-07-24-supercritical-automatic-closure/verify_supercritical_closure.py
python3 contribution/packets/2026-07-24-supercritical-automatic-closure/test_verify_supercritical_closure.py
```

Verifier runtime ~16 s; tests ~0.5 s. The test file also runs under
`python3 -m pytest … -q`. Certificate:
`supercritical_closure_certificate.json` (deterministic; the suite runs the
verifier twice in reduced mode and byte-compares). Knobs: `VSAC_M0`,
`VSAC_ELL_DENS`, `VSAC_MAXLEN`, `VSAC_TERNARY`, `VSAC_FRONTIER_N`,
`VSAC_REDUCED`, `VSAC_OUT`.

Lean:

```bash
cd formal && lake build      # expect no `sorryAx` in the #print axioms lines
```

## 12. Related work

The inequalities are the atlas's own (landmark packet, Corollaries 4 and 7,
resting on the Bernstein–Lagarias conjugacy). The substitution-language
machinery is standard automatic-sequence theory (Cobham 1972;
Allouche–Shallit, *Automatic Sequences*, 2003, Ch. 6 and §8.4), as is
subadditivity of the maximal-ones function (Fekete). Unique ergodicity of
primitive substitution subshifts is Queffélec, *Substitution Dynamical
Systems*, §5. The stratum being closed is defined by
[`2026-07-22-automatic-transcript-rigidity`](../2026-07-22-automatic-transcript-rigidity/);
the density wall it sits above is
[`2026-07-22-pointwise-drift-wall`](../2026-07-22-pointwise-drift-wall/).
No priority search was run for Lemma D, which is an elementary
desubstitution count and is almost certainly folklore.
