# THE FENCE: computational encoding for the fixed `3n+1` map

## Verdict

No proof places the fixed `3n+1` map on a decidable or universal side. The
useful boundary located here is more precise:

\[
\text{finite control words}
\xrightarrow[\text{Terras}]{\text{always}}
\text{one compatible }2\text{-adic state}
\xrightarrow[\text{open in structured families}]{\Phi(q)\in\mathbb Z_{>0}}
\text{one positive-integer orbit}.
\]

Finite blocks are free in the exact sense that every block occurs. Infinite
block concatenation is not free: it must pass the positive-integer
realizability test

\[
\Phi(q)=-\sum_{j\ge0}2^{d_j}/3^{j+1}\in\mathbb Z_{>0},
\]

and every proposed macro-step boundary must land back in the encoding set.
That is the current constructive fence. It is a proved obligation, not a proof
that the obligation is decidable or impossible.

## 1. Known landscape, with scope

| Result | Exact use here | What it does not imply |
|---|---|---|
| Terras, 1976: residues modulo `2^L` correspond bijectively to length-`L` parity vectors | Every finite branch transcript is realized by one residue cylinder | An arbitrary infinite transcript comes from a positive integer |
| Conway, 1972: sufficiently general residue-class affine iterations have algorithmically unsolvable behavior | There is a genuine universality/undecidability region in the larger map space | The fixed two-branch coefficients `(1/2,0)` and `(3/2,1/2)` are universal |
| Kurtz–Simon, 2007: a natural generalized Collatz global problem is `Pi^0_2`-complete | The parameterized family problem is maximally hard at its arithmetical level | Their proof applies to the fixed `3n+1` map; the paper explicitly separates that case |
| Kannan–Lipton, 1986: point reachability under powers of one rational matrix is polynomial-time decidable | Single-matrix linear dynamics are on a decidable side | State-guarded switching of the two Collatz matrices reduces to one matrix |
| Fremont, 2013: free reachability for finitely many 1D integer affine maps is decidable | Low-dimensional affine reachability can remain decidable despite free word choice | The rational, parity-guarded Collatz pair is covered by that algorithm |
| Ghahremani–Kelmendi–Ouaknine, 2023: reachability for injective 1D piecewise-affine maps is decidable; the general two-interval case remains a frontier | Injectivity is a meaningful positive island | It covers `T`, which is noninjective because `T(1)=T(4)=2` |
| Matrix mortality results | Useful warning about dimension/generator sensitivity | Anything here: both Collatz matrices are invertible, so their semigroup cannot contain zero |

The formal distinctions and one-way reductions are proved in
[`FORMALIZATION.md`](FORMALIZATION.md). In particular:

- `H_T={n: orbit reaches 1}` and binary reachability `R_T` are computably
  enumerable;
- `H_T <=_m R_T` via `n -> (n,1)`;
- the global Collatz sentence is syntactically `Pi^0_2`, but this gives no
  completeness or undecidability result for the fixed map; and
- a uniform universal-machine simulation with fixed target `1` would prove
  `H_T` undecidable and therefore would imply that the Collatz conjecture is
  false. No such simulation is constructed here.

The Busy Beaver connection is retained only at supported resolution: current
BB(6) work contains Antihydra, whose halting is governed by a Collatz-like
orbit and a parity-count inequality. The precise coefficient in the repo's
literature map is disputed in §8 below.

## 2. Lemma 2 warm-up

**Status: PROVEN.** [`LEMMA2_PROOF.md`](LEMMA2_PROOF.md) proves for arbitrary
`k>=1,t>=1` that

\[
B_w(t)=e_bQ^{t-1}h.
\]

The proof establishes a bijection

\[
\{\text{accepted length-}t\text{ KMP extensions after }w\}
\longleftrightarrow
\{m\bmod2^t:\tau_{k,r}(m)=t\}.
\]

It handles self-overlap by starting at the longest proper border `b`, proves
that deleting completion transitions enforces first return, and proves the
refinement depth is exactly `s=t`. The `196/196` machine comparison is not a
premise.

This closes the stated written-proof gap in Lemma 2. It does not automatically
accept every downstream conjugacy assertion in `fold/note/NOTE.md`; preservation
of the chosen symbolic branch partition under the draft's notion of affine
conjugacy remains a separate proof obligation.

## 3. Partial theorems proved in this run

Full statements and proofs are in
[`PARTIAL_THEOREMS.md`](PARTIAL_THEOREMS.md).

1. **Finite-cylinder saturation — VALID.** Every length-`L` parity word is
   realized by exactly one residue modulo `2^L`; finite local forbidden-word
   obstructions do not exist.
2. **Exact global realizability — VALID.** An infinite parity transcript `q`
   is realized by the unique 2-adic state `Phi(q)` above, and is realized by a
   positive integer exactly when `Phi(q)` is a positive ordinary integer.
3. **Eventually periodic transcript island — VALID.** `Phi(q)` is an
   effectively computable rational for eventually periodic `q`; positive
   realizations have eventually periodic `T`-orbits and cannot carry an
   infinite injective configuration run.
4. **The `a=1` family — VALID.** For positive odd `b`, the map
   `n/2` (even), `(n+b)/2` (odd) enters the finite invariant set `[1,b]`;
   reachability is decidable and strict orbit-embedding universality is
   impossible. The fixed `3n+1` map is the first positive odd multiplier
   outside this elementary descent island.

The last sentence is only a threshold for the ranking function `n`. It is not
a minimal universality theorem.

## 4. Empirical phase map

The failed Grok packet and the inline exact scan are recorded under
[`verify/`](verify/):

- [`GROK_PACKET_RESULT.md`](verify/GROK_PACKET_RESULT.md): verbatim delegate
  failure;
- [`fence_phase.py`](verify/fence_phase.py): exact scanner;
- [`test_fence_phase.py`](verify/test_fence_phase.py): property and read-back
  checks;
- [`phase_results.json`](verify/phase_results.json): machine-readable
  certificate; and
- [`PHASE_TABLE.md`](verify/PHASE_TABLE.md): all 25 rows, cycles, and witnesses.

Grid: `a,b in {1,3,5,7,9}`; every `1 <= n < 1,000,000`; exact integers;
unresolved at 10,000 new steps or current bit length greater than 64.

| bounded label | systems | interpretation |
|---|---:|---|
| `all-converge` | 2 | `(1,1)` and `(3,1)`; every tested seed reached `1` |
| `cycles` | 8 | every tested seed resolved; a non-`1` cycle has an exact edge certificate |
| `apparent-divergence` | 15 | at least one exact orbit prefix reached a cap |

The phase change is texture, not a theorem: all five `a=1` systems are
provably eventually periodic (Theorem 4), the `a=3` grid happens to resolve
at this bound, and every tested `a>=5` system has cap witnesses. Nothing in
this table proves convergence, divergence, decidability, or universality.

## 5. Registry of approach families

| family | concrete object | status | kill condition / next obligation |
|---|---|---|---|
| Finite windows and automata | allowed parity words, KMP states, fold counts | **CLOSED AS A FENCE PROOF** | Theorem 1: every finite word occurs. Retain only for exact bookkeeping such as Lemma 2. |
| Positive-integer realization | `Phi(q)` for machine-generated infinite transcripts | **LIVE — rank 1** | Prove decidability or a strict obstruction for a named transcript class; do not infer from finite prefixes. |
| Transcript hierarchy | eventually periodic -> automatic -> morphic -> computable | **LIVE** | Theorem 3 settles only the first rung. Next rung must include an exact ordinary-integrality test. |
| Descent/ranking subclasses | `T_{a,b}`, multistep residue rankings | **LIVE OUTSIDE `(3,1)`** | Extending a ranking all the way to `(3,1)` and target `1` is Collatz-strength and is **BLOCKED** unless a genuinely weaker intermediate theorem is named. |
| Direct universal simulator | configuration codes and macro-step parity blocks | **BLOCKED after two gaps** | Gap 1: finite blocks give only residue cylinders. Gap 2: their concatenation has not been proved positive-integral or closed on codes. |
| Free matrix-semigroup transfer | unrestricted products of `M_0,M_1`; generic mortality | **BLOCKED after two gaps** | Gap 1: witness words ignore the parity guard. Gap 2: generic hardness changes generators/dimension, while this fixed pair is invertible. |
| Minimal generalized-map threshold | restrict modulus, branch count, coefficients, and guards in Conway/Kurtz–Simon compilers | **LIVE — rank 3** | Produce an explicit deterministic compiler at a stated parameter point or a decidability theorem below it. “Generalized maps are universal” is too coarse. |
| Fold/renormalization complexity | first-return branch languages and cross-depth laws | **CLOSED FOR THIS QUESTION** | It measures the free finite-word side. No link to positive-integer computational encoding has been proved. |
| Finite parameter sweep | phase table in `verify/` | **COMPLETE AS TEXTURE** | No larger bound without a new invariant; finite-bound extrapolation is forbidden. |

## 6. Precise obstruction that remains

A proposed strict simulator must provide, uniformly over configurations:

1. an injective positive-integer code `E(c)`;
2. a forced parity block `w(c)` satisfying
   `E(c)=rho(w(c)) mod 2^{|w(c)|}`;
3. the exact affine transition
   `T^{|w(c)|}E(c)=E(delta c)`;
4. global compatibility: along every infinite run, the concatenated transcript
   `q_c` has `Phi(q_c) in Z_{>0}`; and
5. a reachability target whose relationship to machine halting is exact and
   does not assume the Collatz conclusion.

Known finite-word tools solve item 2 and the local algebra in item 3. They do
not solve items 1, 4, or 5. Conversely, a weakness theorem must quantify over
**all** encodings satisfying these obligations; ruling out one natural code,
one block grammar, or one finite-state parser is insufficient.

## 7. Ranked attack routes

### 1. Structured-transcript integrality

Extend Theorem 3 from eventually periodic transcripts to one precisely defined
larger class, preferably `2`-automatic or morphic parity sequences, and decide
whether `Phi(q)` is a positive integer. This attacks the actual realizability
wall without assuming a universal encoding.

**What would change my mind:** a known theorem already decides these series in
the required ordinary-integrality sense, making the route routine; or a clean
reduction shows the next rung is equivalent to an open Diophantine problem of
Collatz strength.

### 2. Guarded predecessor-set structure

Study target predecessor sets under the exact inverse rules `2m` and, when it
is a positive odd integer, `(2m-1)/3`. Seek semilinear, automatic, or other
decidable descriptions for restricted targets or restricted depth profiles.
This keeps the parity guard inside the object instead of filtering a free
semigroup afterward.

**What would change my mind:** a proof that even a sharply restricted target
class already uniformly represents an undecidable reachability problem, or a
counterexample family proving the proposed representation class is not closed
under one inverse step.

### 3. Minimal deterministic generalized-Collatz compiler

Reconstruct the Conway/Kurtz–Simon encoding with every resource explicit:
modulus, residue classes, coefficient signs, target type, and whether the map
varies with the program. Then minimize one resource at a time. This can place
rigorous upper points on the universality side without pretending they transfer
to modulus `2`.

**What would change my mind:** literature already contains a sharper minimal
compiler, or the compiler intrinsically requires the program to vary the map,
making comparison with one fixed `T` less informative than route 1.

### 4. Certified ranking islands in `(a,b)` space

Generalize Theorem 4 using multistep residue-dependent ranking functions, but
stop before `(3,1)` unless the intermediate theorem excludes a nontrivial
parameter region. Use the empirical table only to choose examples.

**What would change my mind:** every plausible ranking condition collapses to
global termination for `(3,1)`, or the certified region does not extend beyond
the elementary `a=1` case.

### 5. More empirical scanning

Lowest rank. It is useful only when attached to a proposed invariant or a
counterexample to a finite conjecture.

**What would change my mind:** a new exact statistic predicts the certified
cycles/cap exits and creates a theorem-sized classification question.

## 8. Adversarial audit and disagreements with repo framing

### Claims rejected

- “The 2-adic full shift is universal, therefore `3n+1` is universal.” The
  shift lives on all of `Z_2`; Theorem 2 isolates the missing positive-integer
  condition.
- “A free word product reaches the target, therefore the Collatz orbit does.”
  The witness must pass the parity guard at every prefix.
- “All tested `(3,1)` seeds converge, therefore Collatz is true.” Finite-bound
  fallacy; explicitly excluded by the phase certificate.
- “A cap witness diverges.” It is only an exact finite prefix.
- “One failed encoding proves weakness.” The quantifier is over all encodings.
- “The global question is `Pi^0_2`, therefore it is `Pi^0_2`-complete.” This
  confuses a fixed sentence with the parameterized generalized-map problem.

### Disagreements

1. **“Nondeterministic-flavored generality” is misleading.** Conway-style
   residue-class maps are deterministic once the integer state is fixed, and
   deterministic universal machines exist. The relevant added freedom is a
   programmable residue/affine branch table, not nondeterminism itself.
2. **There is not one binary notion of “simulates computation.”** Step-faithful
   orbit embedding, decidable-target reachability, and fixed-target-to-`1`
   simulation have different consequences. The last would already imply a
   counterexample to Collatz.
3. **Antihydra coefficient mismatch.** `fold/F3-literature-map.md` says the
   odd-step count merely exceeds the even-step count. The current Busy Beaver
   Cryptids page states the termination condition as `O > 2E`. Until the
   variable conventions are reconciled, only the qualitative parity-count
   reduction is load-bearing here.
4. **Lemma 2 does not by itself certify the whole fold theorem.** It proves the
   symbolic cylinder count. The draft's claim that affine conjugacy preserves
   that branch partition requires its own precise partition/maximality proof.
5. **“First wildness at `a=3`” would overstate Theorem 4.** `a=3` is only the
   first positive odd multiplier for which the simple ranking `n` stops being
   globally decreasing. The empirical grid does not locate universality.

## 9. Sources

- Riho Terras, [“A stopping time problem on the positive integers”](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers), *Acta Arithmetica* 30 (1976), 241–252.
- J. H. Conway, [“Unpredictable Iterations”](https://gwern.net/doc/cs/computable/1972-conway.pdf), *Proceedings of the Number Theory Conference*, Boulder (1972), 49–52.
- Stuart A. Kurtz and Janos Simon, [“The Undecidability of the Generalized Collatz Problem”](https://people.cs.uchicago.edu/~simon/RES/collatz.pdf), TAMC 2007, LNCS 4484, 542–553, [DOI](https://doi.org/10.1007/978-3-540-72504-6_49).
- Ravindran Kannan and Richard J. Lipton, [“Polynomial-Time Algorithm for the Orbit Problem”](https://doi.org/10.1145/6490.6496), *JACM* 33(4) (1986), 808–821.
- Michael S. Paterson, [“Unsolvability in 3 x 3 Matrices”](https://doi.org/10.1002/sapm1970491105), *Studies in Applied Mathematics* 49 (1970), 105–107.
- Daniel Fremont, [“The Reachability Problem for Affine Functions on the Integers”](https://arxiv.org/abs/1304.2639) (2013).
- Stefan Jaax and Stefan Kiefer, [“On Affine Reachability Problems”](https://arxiv.org/abs/1905.05114) (2019).
- Faraz Ghahremani, Edon Kelmendi, and Joël Ouaknine, [“Reachability in Injective Piecewise Affine Maps”](https://arxiv.org/abs/2301.09752) (2023).
- Busy Beaver Challenge, [BB(6)](https://wiki.bbchallenge.org/wiki/BB%286%29) and [Cryptids](https://wiki.bbchallenge.org/wiki/Cryptids), current pages checked 2026-07-18.
- Repo-local citation status and neighboring Collatz results:
  [`../F3-literature-map.md`](../F3-literature-map.md).

## 10. Reproduction

```bash
python3 fold/fence/verify/fence_phase.py
python3 fold/fence/verify/test_fence_phase.py
```

The first command regenerates only the two derived artifacts under
`fold/fence/verify/`. No existing repo file is edited.

