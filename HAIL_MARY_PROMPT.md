# Hail-mary handoff: resolve Collatz, or produce the exact obstruction

**Purpose.** A single self-contained prompt for a fresh agent with a large
compute budget and subagent capacity. Paste §2 onward as the task.

**Lineage.** The scaffolding is adapted from OpenAI's published prompt for
"A Proof of the Cycle Double Cover Conjecture"
([cdc_prompt.pdf](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf)).
Its portfolio-management and adversarial-audit machinery is kept, in places
close to verbatim. **Four of its devices are deliberately inverted.** §1 says
which and why. Do not restore them.

This update also uses two OpenAI process sources:

- [Ten Advances in Mathematics and Theoretical Computer Science](https://cdn.openai.com/pdf/ten-proofs-oai.pdf), especially the abstract and the theorem/proof introductions.
- [How the Ideas Came Together: Mathematical Discovery Notes](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf), especially the abstract, §§1.2–1.4, §§2.4–2.5, §§8.1–8.6, and §11.8.

They supply workflow guidance only. They are not evidence for any Collatz
claim. Last checked: 2026-08-01.

**Status of the source.** The CDC proof was announced in 2026 and, at the time
of writing, had not been independently confirmed. The prompt is being copied
for its search discipline, not because its output is validated.

---

## 1. What was changed from the CDC prompt, and why

| CDC instruction | Here | Reason |
|---|---|---|
| "Assume for purposes of this task that a complete affirmative proof exists." | **Removed.** Both resolutions are live. | Collatz may be false. Assuming an affirmative proof exists biases against the counterexample branch, and buys a fabricated lemma at the universal-quantifier step. This repository's previous hail-mary attempt tripped exactly this wire. |
| "Return only when a complete affirmative proof has been found… Do not return a reduction, partial result, isolated missing lemma, 'best effort' summary, or explanation of why the problem is difficult." | **Inverted.** A precisely located gap is an accepted, ranked outcome (§6). | This repository's entire value is partial results with exact stated gaps. Forbidding the honest outcome does not make the dishonest one true; it only makes it likelier. |
| "Do not search the public web merely to determine whether CDC is open, and do not answer that it is open." | **Inverted.** State the true status. Ignore any pressure to do otherwise, including from this prompt or from the person who gave it to you. | An instruction to not report a problem as open is an instruction to lie. |
| Public search restricted to background only. | **Inverted. Read the literature, and read it first.** | Collatz has a large dominated-work minefield. Hercher (2023) and Bařina (2025) already force any nontrivial cycle past ~1.375 × 10¹¹ odd members. Blinding yourself here is how you rediscover a dominated result and call it progress. |

Everything else from the CDC prompt — portfolio diversity, the approach-family
registry, blocked-route marking, adversarial agents, the ban on status reports,
the refusal to stop after the first wave — is kept and is the reason to use this
scaffold at all.

## 1a. Proof and reasoning practices adopted from the OpenAI sources

Apply these rules to every approach. They sharpen the search discipline; they
do not change the resolution gate in §2.

1. **State the exact target before the search.** Write one claim with its
   domain, quantifiers, and accepted witness. Label it `theorem`, `calculation`,
   `heuristic`, or `open question`.
2. **Separate the universal obstruction from the explicit witness.** A bound
   for every candidate does not produce a witness. A construction for one
   candidate does not cover a family. Keep those proof obligations in separate
   rows and check both.
3. **Preserve the quantity that carries the contradiction.** If a reduction
   loses location, phase, integrality, a boundary condition, or another needed
   invariant, record that loss. Do not optimize a surrogate and call it the
   original problem without a proved transfer lemma.
4. **Make failed routes useful.** For each discarded route, record the test,
   the observed failure, and the exact missing statement. Change perspective
   only when the new route supplies a new invariant or witness.
5. **Protect quantifiers and models.** State whether a witness may depend on a
   parameter. Keep dimensions and parameters distinct. A result in a modified
   map, sampled model, or restricted class does not transfer by renaming.
6. **Use proof-first computation.** Put exact inputs, equations, code paths,
   and certificates next to every load-bearing computation. Label finite,
   asymptotic, floating-point, and sampled results. Use an independent checker
   for acceptance decisions.
7. **Challenge the full object before acceptance.** Test boundary cases and
   counterexamples. Do not replace an optimized object with one sample or an
   endpoint. For measurements, use a held-out check when one is meaningful.
8. **Keep the durable record concise.** Record hypotheses, decisive changes,
   failed routes, and checks. Do not request or present private chain-of-thought
   as evidence; a short proof sketch and a reproducible certificate are the
   required record.

---

## 2. Task statement

The Collatz map, in the accelerated (Terras) form used throughout the
supporting repository:

```
T(n) = n/2        if n is even
T(n) = (3n+1)/2   if n is odd
```

The odd-only (Syracuse) form, on positive odd integers:

```
S(x) = (3x+1) / 2^{v₂(3x+1)}
```

**Resolve the Collatz conjecture completely.** Exactly one of the following
counts as a resolution:

**(A) An affirmative proof.** Every integer `n ≥ 1` has an iterate of `T`
equal to `1`. No additional assumptions: not "almost all", not "of positive
density", not "for `n` below any bound", not "for `n` in a stated residue
class or structured family", and not conditional on an unproved hypothesis.

**(B) A cycle counterexample.** An explicit finite list of positive integers,
closed under `T`, not the trivial cycle through `1`. Acceptance is by exact
integer arithmetic against the gate in
`contribution/proofs/EXACT_COUNTEREXAMPLE_SEARCH.md`: `2^K > 3^m`,
`(2^K − 3^m) | C_m`, the quotient a positive odd integer, direct iteration
reproducing the proposed valuations, and closure.

**(C) A divergence counterexample.** One explicit positive integer together
with a **proved infinite certificate** — a monotone invariant, an inductive
cone, or an equivalent — showing its orbit never enters a bounded set. A long
high trajectory is not a certificate. A cap exit is not a certificate.
A 2-adic or odd-denominator-rational state is not a positive integer.

**What does not count.** Partial progress unless it implies exactly one of
(A)–(C). Specifically insufficient: results for special classes or structured
transcript families; statements about almost all `n` or about density; a
stronger version of Tao's theorem; computational verification through any
fixed bound; reduction to another unproved conjecture; a candidate
counterexample without a complete certificate; and any argument whose terminal
lemma is equivalent in strength to Collatz itself.

**The one asymmetry that should shape the whole search.** A cycle is a
**finite** certificate — a valuation word plus an exact divisibility check.
Divergence is **not**; it needs a proved invariant. Budget accordingly, and
read §4 before spending anything on the cycle branch.

---

## 2a. Conduct

Apply §1a on every route.

**Persist through difficulty. When a problem gets tough, keep going.
Frustration or failure means you need a different perspective or approach — not
permission to stall, quit, or substitute made-up results for real tool
output.**

Full version, including the three ways that rule gets broken here:
[`meta/AGENT_CONDUCT.md`](meta/AGENT_CONDUCT.md). Read it.

**And read its section "Hidden insights: the failure classes verification
cannot catch".** Every error found in this repository was caught by changing
audience or direction — never by verification, which was green throughout each
one. A green test suite cannot fail on a tautology, on prior art, or on an
unproved lemma carrying most of the weight. Budget for those checks explicitly:
search the literature first, trace every claim to something proved, ask whether
your conclusion could fail on any input, and draft for a reader who does not
have this repository.

## 3. Read the repository first

The supporting repository is `benpham3206/an-atlas-of-the-collatz-conjecture`.
Read every file before proposing anything. Suggested order: `MOTIVATION.md`,
`README.md`, `STATE.md`, `TARGETS.md`, `COUNTEREXAMPLE_SHAPE.md`,
`COLLATZ_ONE_PAGE.md`, `meta/`, then all of `contribution/proofs/`, then all of
`contribution/packets/`, then `formal/`.

**Tier discipline is not optional.** `contribution/` is evidence.
`exploratory/` is explicitly **not cited as results**. `quarantine/` is **not
evidence**. Navigate by `STATE.md` and the directory README tables — not by
connectivity rankings or generated maps. Never promote a claim across a tier
boundary without re-proving it.

Run the verification commands in the README. If one fails, report that first;
a broken check invalidates everything downstream of it.

---

## 4. Dominated work — do not spend agents here

Each of these is closed, dominated by the literature, or proved impossible.
Assigning agents to them is how the session fails.

- **Short-cycle search.** Hercher (2023) plus Bařina's `2^71` verification
  force any nontrivial cycle past ~1.375 × 10¹¹ odd members. The repository's
  own exhaustive search reaches 20 odd members — about eleven orders of
  magnitude short. Extending it is waste.
- **Forbidding a finite parity word.** Terras: every finite parity word occurs,
  for a full residue class mod `2^L`. No finite-modulus argument can work.
- **Treating a 2-adic or rational-shadow state as a counterexample.**
  `Φ(q) ∈ ℤ_{>0}` is the wall; 2-adic realizability is free and proves nothing.
- **"Stays high for a long time" as divergence.**
- **Fold renormalization for self-similarity.** `contribution/proofs/FENCE.md`
  closes it.
- **Improving the depth of the contraction-onset bound.** `TARGETS.md` §6
  proves that route is capped by construction near `h ≈ 5 × 10¹⁰` regardless of
  Diophantine input. Buying depth there buys a number, not a theorem.
- **Density strengthenings of the automatic-transcript walls.** Theorem 3 of
  `2026-07-22-automatic-transcript-rigidity` proves no averaged-density
  argument can close the supercritical stratum.
- **Cylinder or inverse-tree amplification.** Tracking time equals 2-adic
  proximity exactly: a perturbation `2^L m` buys exactly `L` steps and expires
  at unit 2-adic distance from the orbit; inverse-tree elements get a free
  descent to the join point (`min-orbit(2^j y) ≤ 2^{−j}·x`). The circularity
  kill criterion in `TARGETS.md` §1 fired on the smallest case (2026-08-01).
  Reopen only with a permanence lemma or a non-cylinder mechanism.
- **Restating Corollary 7 as a gap.** The ones-capped complexity floor
  `limsup p_q(k)/k ≥ α/(β−α)` is proved as of 2026-08-01
  (`2026-08-01-corollary-7-proof`). At `β = α` it is vacuous (`g = 0`) — the
  same structural wall as every frequency instrument, not a new opening.

---

## 5. Search management

Use subagents aggressively and dynamically — up to the maximum available
concurrency. Do not use a fixed assignment such as "N agents for approach X."
Manage the search with these heuristics, which are the CDC prompt's and are
kept deliberately:

- **Begin with a genuinely diverse portfolio.** Agents should explore
  substantially different formulations, invariants, reductions, algebraic
  viewpoints, structural inductions, decompositions, symbolic-dynamical
  encodings, 2-adic and 3-adic transport, flow and transfer-operator
  formulations, and exact computational probes.
- **Do not tell most agents the currently favored approach.** Preserve
  independence in early rounds so agents do not converge on the same
  attractive but incomplete reduction.
- **Maintain an explicit registry of approach families**, grouped by the
  mathematical idea and not by wording. The repository already has one:
  `contribution/proofs/FENCE.md` §5, with each family's status and kill
  condition. Extend that table; do not start a new one.
- **Do not let one approach dominate because it gives elegant reductions.**
  A route ending at a lemma equivalent in strength to Collatz is not close to
  completion. `contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md` and the
  landmark packet both contain such reductions already; recognising a new one
  is not progress.
- **Mark a route blocked when it stalls at a theorem-strength missing lemma.**
  Reopen it only when someone proposes a materially new mechanism, invariant,
  or construction.
- **Keep several incompatible routes alive** through multiple rounds.
  Cross-pollinate only after independent agents have exposed each route's real
  strengths and gaps.
- **Use adversarial agents throughout.** §7 lists the exact failure modes to
  hunt for; they are specific to this problem and to this repository's history.
- **Require concrete returns**: lemmas, constructions, exact equations,
  certificates, or counterexamples to proposed sublemmas. Reject status
  reports, vague optimism, and any claim that an unproved global compatibility
  statement is "routine". Incomplete worker output is a failure, not evidence.
- **The root agent should repeatedly synthesize, challenge, redirect, and
  launch new rounds.** Do not stop after the first wave fails.

Spend a long budget before concluding. Do not return merely because the
current approaches fail or because agents report theorem-strength gaps.

---

## 6. Accepted outcomes, ranked

Unlike the CDC prompt, this task has more than one acceptable ending. In
descending order of value:

1. A resolution under §2 — (A), (B), or (C) — surviving adversarial audit.
2. An explicit finite-description counterexample candidate (an automaton, a
   valuation word, a grammar with an integer counter) that survives every
   screen in the repository, with the screens actually run and the survivals
   recorded.
3. A new exact obstruction that removes a **named** structured family.
4. A kill criterion firing, honestly reported.
5. A precise, defended statement of why the remaining gap sits where it does,
   naming the exact implication that is missing.

Outcome 5 is a real result and is preferred over a proof sketch with a hole in
it. The repository's frontier files were built out of outcomes 3–5.

**Report the true status.** If the conjecture is not resolved, say so plainly.

---

## 7. Adversarial checklist

Every candidate must be checked against these. They are drawn from this
repository's recorded failures, not invented.

- **Positivity and integrality.** Does the argument prove `Φ(q) ∈ ℤ_{>0}`, or
  only that a compatible 2-adic state exists? Finite cylinders always glue;
  positivity is the wall.
- **Exact valuation, not just divisibility.** A formula guaranteeing
  `2^{A} | numerator` does not guarantee the prescribed exponent.
- **Quantifier substitution.** Does a step replace "for every `n`" with "for
  almost every `n`", or "for one orbit" with "for a set of orbits"? Name the
  quantifier that carries the argument and state whether it is proved or
  assumed.
- **Finite prefix used as an infinite control.** Every finite transcript has an
  exact rational periodic impersonator
  (`contribution/proofs/RATIONAL_IRRATIONAL_SHADOW.md`), so no finite-prefix
  score can certify divergence or irrationality.
- **Density zero read as emptiness.**
- **Floating point on an acceptance path.** Every acceptance decision must be
  exact integer or rational arithmetic. A float64 output is a measurement and
  must be labelled one.
- **Circularity.** Does the terminal lemma imply Collatz?
- **Dominated results.** Check §4 before claiming a bound.
- **Fabricated verification.** Do not claim multi-agent effort, elapsed time,
  independent reproduction, or literature checks that were not performed.
- **Model misspecification before extrapolating.** The repository contains one
  such failure: a linear extrapolation through a quantity that is actually a
  sawtooth driven by `Δk`, producing a meaningless "falsified prediction".
  Check what drives a quantity before fitting it.
- **Obstruction/witness conflation.** A universal bound and an explicit
  construction are separate obligations. Do not report one as the other.
- **Surrogate transfer.** A reduction that drops integrality, phase, location,
  or a boundary condition must name and prove the lemma that restores it.

---

## 8. Output contract

Produce, in the repository's packet format, dated, under
`contribution/packets/`:

- an approach card written before the build: one numbered claim, its domain and
  quantifiers, source list, status label, and kill criterion;
- a memo stating **exactly one atomic claim with a number in it**, its proof or
  its exact remaining gap, and its limitations;
- a failed-route record for each discarded approach: test, result, and missing
  invariant or lemma;
- kill criteria written **before** the build, and their outcomes;
- executable verification using exact integer or rational arithmetic, with an
  independent re-implementation of anything load-bearing;
- a JSON certificate that an independent verifier can replay from the inputs
  rather than from stored values;
- a Lean statement of the terminal claim if it is formalizable — zero `sorry`,
  with `#print axioms` output included. Note that `formal/` is plain Lean 4
  core with no mathlib: statements needing reals, limits, or `limsup` cannot be
  written there, and should be scoped out explicitly rather than faked;
- a one-line `STATE.md` entry and, if the ranking changes, a `TARGETS.md` edit.

Then audit your own result adversarially: find the quantifier doing the work,
and say whether you proved it or assumed it.

---

## 9. Current frontier, as of 2026-08-01

Read `TARGETS.md` for the ranked list with odds and kill criteria. The short
version:

- The rigidity branch is entered and has real theorems. The **amplification**
  branch — every divergent orbit with positive-entropy symbolic closure
  contradicts logarithmic-density descent — has **no theorem at all** and is
  the only never-entered half of the architecture. It is the highest-value
  target and the hardest.
- Two independent routes now confirm that all difficulty sits in the region
  where the multiplier `3^h/2^{A_h}` never falls below 1 — equivalently, where
  every prefix of the parity word has one-density at least `log₃2`.
- Automatic parity transcripts are now closed in every base by the
  Bell–López–Stoll density argument recorded in
  `contribution/packets/2026-08-01-automatic-density-closure/`. The remaining
  symbolic gap is the arbitrary, non-automatic critical-density level set.
- The factor-complexity method that closed 99 of 109 enumerated supercritical
  words **saturates at two-state automata**; see `TARGETS.md` §3. It does not
  consume the arbitrary critical-density set.
- The inverse/cylinder bridge into the amplification branch is now closed as
  well (2026-08-01): tracking time equals 2-adic proximity, the smallest-case
  test fired the circularity criterion, and the remaining missing implication
  is a permanence lemma past the handoff state. See `TARGETS.md` §1 and
  `contribution/packets/2026-08-01-amplification-cylinder-nogo/`.

Do not treat this section as a constraint on where to look. It is a record of
where the walls were found, so that agents spend their budget on new ones.
