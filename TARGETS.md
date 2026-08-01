# Attack targets, ranked

> **2026-08-01 closure notice.** Targets 3 and 5, and the automatic sub-target
> inside Target 2, are closed. Bell (2020) proves that every automatic set has
> rational lower density. López–Stoll (2021) force every rational non-cyclic
> trajectory to have lower parity density `log₃2`, which is irrational.
> Therefore no rational non-cyclic trajectory has an automatic parity word in
> any base. The arbitrary-word critical-density target remains open. See
> `contribution/packets/2026-08-01-automatic-density-closure/`.

Ranked by **importance if it lands** — what the result would mean for the
repository's own proof architecture
([landmark packet §8](contribution/packets/2026-07-22-landmark-pointwise/LANDMARK_STRATEGIES_AND_COLLATZ_CONTINUATION.md)),
not by how likely it is. Odds and fallbacks are stated separately so the
ranking stays usable: the highest-importance target is not the one to start
with, and §"What I would actually run next" says which is.

Every entry carries a kill criterion. Written 2026-07-24, after the
supercritical-automatic-closure and contraction-onset packets.

Targets 1–3 and 5 were offered as session options; 4, 6 and 7 were added to
make the frontier complete.

---

## 1. Amplification

> **Statement.** Every divergent orbit with positive-entropy symbolic closure
> contradicts logarithmic-density descent.

**Why first.** The repository's architecture says that after cycles are
excluded, **rigidity ∧ amplification ⟹ Collatz**. Rigidity is entered and has
real theorems — several strata are closed, and two more closed today.
Amplification has **no theorem at all**; `STATE.md` records it as "not
entered — a located barrier only." Every other target on this list lives
inside the rigidity branch. This is the only never-entered half of the
problem, so nothing else can be more important.

**What it needs.** Convert one divergent orbit into a positive
logarithmic-density set of orbits whose minima exceed a growing function,
contradicting Tao. The bridge is the inverse/cylinder family of a single
survivor.

**Odds in one session: very low.** This is Tao-strength. The honest expected
output is a precise statement of the missing implication.

**Kill criterion, check before building.** If the density transfer needs
control of the orbit of one fixed integer rather than of a set, the argument
is circular — it assumes the pointwise statement it is meant to supply. Test
that on the smallest non-trivial case first and stop if it fires.

**RUN 2026-08-01. The kill criterion fired — for the two families this entry
proposed.** The bridge named above was "the inverse/cylinder family of a
single survivor". Tested on the smallest case (`y = 27`, `L = 20`, `m = 1`)
and in general:

- inverse tree: preimages get a free descent to the join point
  (`min-orbit(2^j y) ≤ 2^{−j}·x`) — they are Tao's *good* set, not an
  exceptional family;
- forward cylinders `y + 2^L m`: tracking is exact and free but lasts exactly
  `v₂(x − y)` steps and expires at 2-adic unit distance from the orbit
  (tracking time = 2-adic proximity). The missing step is a **permanence
  lemma** over individual handoff states — pointwise control of one fixed
  integer's orbit. Circular, per the criterion.

The route is **blocked**, not the branch: a mechanism that consumes positive
entropy directly, not via cylinders or inverse trees, is untouched.
[`contribution/packets/2026-08-01-amplification-cylinder-nogo/`](contribution/packets/2026-08-01-amplification-cylinder-nogo/)

---

## 2. The critical density — the whole remaining symbolic gap

> **Statement.** No divergent Collatz orbit has a parity word with
> `liminf s_L/L = log₃2` exactly.

**⚠ Rewritten 2026-07-25 after the priority search.** This target used to read
"the 2-automatic Gap in full". That framing was too broad: López–Stoll 2021
([arXiv:2101.12747](https://arxiv.org/abs/2101.12747)) close every word with
`liminf > α`, and the drift wall closes every word with `liminf < α`. **Only
the exact critical density remains**, for any word — automatic or not.

That is a much smaller and better-defined target than "the supercritical
stratum", and it explains why every frequency-based instrument is now
exhausted: at `liminf = α` they are all vacuous by construction. The
factor-complexity bound is the only surviving tool, and it is also the only
result the priority search did not find in prior art.

**Automatic words are closed.** Bell 2020 proves that the lower density of
every automatic set is rational. It therefore cannot equal the irrational
number `α`. This applies even when the natural density does not exist, and it
closes the former automatic sub-target in every base.

**Why second.** This is the whole remaining frequency gap for arbitrary words.
The automatic subclass is now closed, but the full critical level set has
Hausdorff dimension at least `H(α) > 0.94995`, so the arbitrary-word target is
still large.

**Why not first.** 2-automatic words are a measure-zero class. Closing them
removes a family, not the branch.

**What it needs.** An arithmetic-realizability mechanism for non-automatic
critical-density words. Frequency and finite-state arguments are exhausted.

**Odds: very low.** No current packet controls this full level set.

---

## 3. The Gap for bounded automaton size — **closed 2026-08-01**

Bell's lower-density theorem closes this target for every finite `N`. The
census below remains as a record of where the older complexity method
saturated.

> **Statement.** No divergent Collatz orbit has a 2-automatic parity
> transcript generated by a DFAO with at most `N` states.

**Why third.** Target 2 with a number, and a *stated family* rather than an
enumerated list — a strictly better object than the 109 words closed today.
The machinery already exists and is proved: by Cobham's theorem every
2-automatic word is a letter-coding of a fixed point of a 2-uniform morphism
on the automaton's own state alphabet, which is exactly the class Lemma D of
[`2026-07-24-supercritical-automatic-closure`](contribution/packets/2026-07-24-supercritical-automatic-closure/)
covers. That packet pointed the machinery at 109 enumerated words; it was
never pointed at the general family.

**What it needs.** DFAO enumeration with canonical-form/minimisation
reduction, the drift wall and periodicity as cheap pre-filters, then the
exact complexity bound on whatever survives.

**RUN 2026-07-24. The kill criterion fired. `N = 2`.**

I estimated `N = 4–5`. Measured, over genuine 2-DFAOs (2-uniform morphisms on
`d` states with `σ(0)[0] = 0`, all non-constant codings, deduplicated):

| states `d` | distinct words | killed by drift wall | killed by Cor 7 | **survivors** | survival rate |
|---:|---:|---:|---:|---:|---:|
| 2 | 10 | 7 | 3 | **0** | 0% |
| 3 | 228 | 137 | 65 | **26** | 11% |
| 4 | 9,148 | 6,049 | 1,146 | **1,953** | **21%** |

So the theorem is:

> No divergent Collatz orbit has a 2-automatic parity transcript generated by
> a DFAO with at most **two** states.

True, and small. At three states 11% of the class already survives, and the
surviving complexity constants sit above the threshold — several survivors
have maximal factor density exactly `1` (arbitrarily long all-ones runs), where
`α/(β−α)` degenerates to `κ = 1.7095…` and the density refinement buys nothing
over Corollary 4.

The `d = 4` census makes it worse rather than neutral: survival roughly
doubles per state, the max proved complexity bound climbs `1.72 → 8.2 → 15.0`
while the threshold it must beat stays fixed, and the *cheap* screen (the
drift wall) does most of the killing at every size — 70%, 60%, 66% — while
Corollary 7's share falls from 30% to 13%. The expensive machinery contributes
less as the class grows, not more.

**The method saturates immediately. It does not scale with automaton size,
and no compute budget rescues it.** That retires target 2 as reachable by this
route — measured, not guessed.

**Why the estimate was wrong.** The 99-of-109 result came from uniform
morphisms of length `ℓ ≤ 4` on two letters, which is a different family. Worse
for the comparison: for `ℓ = 3` those fixed points are **3-automatic, not
2-automatic** — by Cobham's 1969 theorem a sequence that is both 2- and
3-automatic is eventually periodic, so the aperiodic `ℓ = 3` words are not in
the 2-automatic class at all. The `2026-07-22-automatic-transcript-rigidity`
packet labels its whole `ℓ ≤ 4` sweep "2-automatic"; that label is loose.
No conclusion in `2026-07-24-supercritical-automatic-closure` depends on it —
Corollaries 4 and 7 need aperiodicity, `Φ(q) ∈ ℚ_odd` and a complexity bound,
and never use automaticity — but the labelling should be corrected in the
older packet.

**Current verdict.** Do not push `N`. The 26 three-state survivors are closed
by the automatic-density corollary, although the complexity inequality alone
does not reach them.

**Reproduce.**

```bash
python3 contribution/packets/2026-07-24-supercritical-automatic-closure/probe_dfao_saturation.py 3
```

Output recorded in `probe_dfao_saturation.out`, which includes the `d = 4`
census (~7 min). The probe reuses that packet's exact factor-language
machinery.

---

## 4. Morphic transcripts with linear complexity *(added)*

> **2026-08-01 reduction.** Every morphic parity word with an existing natural
> one-frequency is closed: that frequency is algebraic, but López–Stoll require
> the transcendental value `log₃2`. Only non-uniform morphic words without a
> natural one-frequency remain in this target. Bell 2008 guarantees a
> logarithmic frequency, but that does not determine the lower natural
> frequency required here.

> **Statement.** Extend the realizability exclusion from automatic to the next
> rung of the transcript hierarchy.

**Why fourth.** `FENCE.md` route 1 names this explicitly as rank 1 among its
live routes: "extend Theorem 3 to one precisely defined larger class,
preferably 2-automatic or morphic." Automatic is now substantially done;
morphic is the adjacent rung and the machinery is closest to hand.

**The honest limit, and it is severe.** The inequality used throughout is a
**lower** bound on factor complexity, `C ≥ α/(β−α)`. It has force only when
`C` is small. By Pansiot's classification the fixed point of a
non-uniform morphism can have complexity `Θ(n log log n)`, `Θ(n log n)` or
`Θ(n²)` — in all of which `C = ∞` and the inequality is **vacuous**. So this
target is only reachable for the linear-complexity sub-case, and that must be
stated in the title of any packet, not discovered later.

**Odds: moderate, on the restricted class.**

**Kill criterion.** If the morphism's complexity is superlinear, stop
immediately: the method contributes nothing and reporting otherwise would be
an error of the kind §10's audit is designed to catch.

---

## 5. The ten remaining survivors — **closed 2026-08-01**

> **Statement.** Close the ten ternary-coded automata left open by
> [`2026-07-24-supercritical-automatic-closure`](contribution/packets/2026-07-24-supercritical-automatic-closure/) §8.

**Verdict.** Closed. Each is a coding of a uniform-morphism fixed point and is
therefore automatic in the morphism length. Bell makes its lower density
rational, while López–Stoll require `log₃2` for any rational non-cyclic
trajectory.

**Why fifth.** Narrow — ten specific words. But they are a sharp, named test
object, and any mechanism that closes them probably generalises.

**What it needs.** A mechanism that **consumes** high factor complexity rather
than requiring it. That packet establishes, with exact factor counts at
`n = 1537`, that their complexity constants genuinely exceed `α/(ρ−α)`, so
sharpening the existing bound **provably cannot** reach them. A new inequality
is required, not a better constant.

**Odds: low, and a miss yields nothing** — unlike targets 1 and 2, there is no
informative failure mode here beyond restating the obstruction.

---

## 6. Contraction onset to infinity — **closed door** *(added)*

> **Statement.** Remove the depth cap from
> [`2026-07-24-contraction-onset`](contribution/packets/2026-07-24-contraction-onset/):
> a minimal counterexample never contracts at *any* depth.

**This cannot work, and the reason is structural rather than technical.** It
is recorded here so it is not attempted.

The bound is `M(h) = ⌊h·3^{h-1}/(2^{A*(h)} − 3^h)⌋`, and the argument runs
while `M(h) < 2^71`. Better Diophantine input improves the denominator, but
`M(h)` still **grows without bound**: even with the best conceivable
irrationality measure for `log₂3` (measure 2, which is what almost all
numbers have and is far beyond what is proved), the gap is `≳ 1/h`, giving
`M(h) ≲ h²/3`. That exceeds `2^71` at roughly `h ≈ 5 × 10¹⁰`.

So the route is **capped by construction at around 10¹⁰ steps**, not by the
strength of available theorems. It is finite for the same reason the cycle
searches are finite: it consumes a fixed verification limit. Two separate
consequences:

- pushing the current `10⁶` further is a pure compute purchase with a known
  ceiling, and is worth doing only if the number itself is wanted;
- the general principle — rational approximation to `log₂3` controls the
  *multiplier* and is blind to both the additive offset and to which integers
  realise a word — means this family of techniques can reach cycles, where the
  certificate is finite, and can never reach divergence.

---

## 7. Lean: port to `formal-conjectures` *(added)*

> **Statement.** Contribute the zero-`sorry` certificates to the Collatz
> section of `google-deepmind/formal-conjectures`.

**Why last on importance, but not on value.** It proves no new mathematics.
It is, however, the repository's **only externally rejectable artifact** —
the one thing here that a stranger with a deadline can reject — which is the
commitment mechanism the project is built around. `STATE.md` already lists it
under NEXT.

**Ready to port.** `Formal/TerrasBijection.lean`, `Formal/TwoBranchFamily.lean`,
`Formal/CollisionPrinciple.lean`. Lemma 1 of the contraction-onset packet
(descent requires contraction) is two lines of `Nat` arithmetic and should go
with them.

**Kill criterion.** If the port needs mathlib machinery that does not exist
(2-adic integers for `Φ(q)`, KMP automata for the fold screen), scope those
out explicitly rather than opening a PR that cannot close.

---

## Do not touch

Restated from [`COLLATZ_ONE_PAGE.md`](COLLATZ_ONE_PAGE.md) §6 because these
are where sessions go to die:

- extending the exact cycle search past 20 odd members — dominated by
  Hercher/Bařina by ~11 orders of magnitude;
- forbidding finite parity words — Terras makes every finite word occur;
- treating a 2-adic or odd-denominator-rational state as a counterexample;
- "stays high for a long time" as a divergence certificate;
- fold renormalization for self-similarity — `FENCE.md` closes it.

---

## The complexity-consuming instrument: searched for, does not exist

**Run 2026-07-25.** Every saturation in this file has one cause: Corollary 4 is
a *lower* bound on complexity, so it can only kill **simple** objects. A
literature hunt for the missing converse — any theorem giving an **upper** bound
on factor complexity from an arithmetic hypothesis, or deriving a contradiction
*from* high complexity — returned nothing that transfers.

The structural reason is worth stating, because it retires a whole direction:

> Factor complexity is an invariant of the **orbit closure** of `q` under the
> shift. `Φ(q) ∈ ℚ_odd` is a condition on a **single point** of a null, meagre
> set. Low complexity makes the orbit closure small, so it can be intersected
> with an arithmetic condition. High complexity constrains nothing — the closure
> is merely large, and the arithmetic hypothesis is invisible at that
> resolution.

Every known implication in this area runs *low complexity ⇒ Diophantine
conclusion* (Adamczewski–Bugeaud via Ridout's p-adic Roth). The converse is not
unproved-but-plausible; it is the standing open problem. Nobody can show even
that algebraic irrationals satisfy `p(k) ≥ 2k`.

Checked and rejected: ×2×3 rigidity in both forms — Furstenberg 1967 needs the
full `{2^i 3^j}` semigroup orbit and a Collatz orbit supplies one exponent
*path*; Rudolph/Johnson and Einsiedler–Katok–Lindenstrauss need a jointly
invariant **measure** of positive entropy, which is what one would be trying to
prove. Host 1995's "pointwise" normality is μ-a.e., not for a designated point.
Cyr–Kra's low-complexity threshold `C < 4/3` sits below `κ`, wrong direction.

**One cheap probe, tested and dead.** Heinis's gap theorem says that if
`p(k)/k` converges the limit is `1` or `≥ 2`, and `κ = 1.7095…` sits inside
`(1,2)` — so any survivor with a *convergent* complexity ratio and limit below 2
would die for free. Measured: the ten survivors have proved complexity bounds
`101/32 ≈ 3.16` to `97/16 ≈ 6.06`, all far above 2. No kill.

### The redirect that follows

**Change the hypothesis, not the bound.** The survivors are DFAO and
uniform-morphism words — that is a *structural* hypothesis, and there is a tool
that consumes structure while being **completely indifferent to complexity
level**: Mahler's method. Adamczewski–Faverjon
([1508.07158](https://arxiv.org/abs/1508.07158),
[1809.04826](https://arxiv.org/abs/1809.04826)) give a decidable dichotomy — the
value of a Mahler function at an algebraic point is rational or transcendental —
with the corollary that an automatic number is rational or transcendental, *with
no complexity threshold anywhere*. A 3-state DFAO of complexity `2.4k` is as
tractable as one of complexity `1.2k`.

Two things would have to be established, and both are bounded questions rather
than research programmes:

1. That `Φ(q) = −Σ_j 2^{d_j}/3^{j+1}`, for `q` generated by a `k`-uniform
   morphism, is the value at a specific point of a solution of a Mahler-type
   functional equation `f(z^k) = R(z) f(z) + S(z)`. **The mixed bases 2 and 3
   are the obstruction** and this exact case was not found in the literature.
2. A **2-adic** version of the dichotomy, since the rationality test lives in
   `ℤ₂`. p-adic Mahler-method analogues exist in the Nishioka lineage; whether
   one covers this case is the **first thing to check**, and it is cheap.

**RUN 2026-07-25. Check 1 is answered, and the guess above was wrong.**
See [`2026-07-25-mahler-tower`](contribution/packets/2026-07-25-mahler-tower/).

The functional system **exists, for every uniform morphism**. Writing
`c_a(n) = #{i<n : u_i = a}` and `f_b(z,y) = Σ_{u_n=b} z^n Π_a y_a^{c_a(n)}`,

```
f_b(z, y) = Σ_a Q_{a,b}(z, y) · f_a(z^k, y^M),        Φ(q) = −(1/3) Σ_{τ(b)=1} f_b(2, 3^{−τ})
```

with `M` the incidence matrix. The mixed bases are **absorbed by the monomial
substitution `y ↦ y^M`** — they never obstruct the equation. Verified exactly
mod `2^160` on 240 random instances, against an independent re-implementation
of `Φ`.

**The obstruction moved, and it is sharper than the guess.** Iterating sends
`z_e = 2^{k^e} → 0` but `y_e(b) = 3^{−|τσ^e(b)|_1}`, which is a **2-adic unit
for every `e`**. Every form of Mahler's method — real or `p`-adic — requires the
point strictly inside the unit disc. Our point sits exactly on the excluded
boundary in the `y`-directions, and that is inherent: base 3 is a unit in the
base-2 metric.

Consequence for check 2: **a 2-adic dichotomy is not sufficient.** What is
needed is a Mahler-type theorem tolerating boundary points in the non-driving
variables. Nothing searched provides one.

**A new split of the ten survivors, for free.** The induced one-variable tower
converges iff `τ M^e → 0` in `ℤ₂^d`. Proved (F₂ pigeonhole, not measured):
**6 of the 10 fail this and 4 satisfy it.** The four are convergent
deformations of the classical automatic Mahler system; the six have no limiting
Mahler system at all. The stalled fraction *grows* with alphabet size — 50%,
64%, 73% at `d = 2,3,4` — the same direction as every other saturation in this
file. No survivor satisfies the two-variable collapse condition (0/10).

Also flagged as genuinely pointwise, unlike the entire ×2×3 shelf:
Flatto–Lagarias–Pollington, *On the range of fractional parts `{ξ(p/q)ⁿ}`*,
Acta Arith. 70 (1995)
([PDF](http://matwbn.icm.edu.pl/ksiazki/aa/aa70/aa7023.pdf)). Their exponent
`θ = log₂(3/2)` is exactly `1/κ` — they are studying the same shift. Their
theorem forbids the orbit from being confined to a short interval, which
consumes low richness in a *metric* rather than combinatorial sense, and is
therefore not obviously blocked by the ceiling above.

## What I would actually run next

**Superseded 2026-07-24 by running it.** Target 3 was the recommendation
because its failure mode was informative. It failed, informatively: the
complexity method saturates at two states, which retires target 2 as
reachable by that route and caps target 3 at a small theorem.

The 2026-08-01 density corollary changes the shortlist again. **Target 1
(amplification) remains the most important.** Target 2 remains open only for
arbitrary non-automatic words. Targets 3 and 5 are closed. Target 6 is a
proved closed door. Target 4 remains only for non-uniform morphic words.

The general lesson is worth keeping: the factor-complexity inequality is a
**lower** bound on complexity, so it can only ever kill *simple* objects. Every
attempt to extend it — to bigger automata, to morphic words, to the ten
survivors — runs into the same wall from a different side. A route that
consumes complexity rather than requiring it is the missing instrument, and it
would serve targets 2, 4 and 5 at once.
