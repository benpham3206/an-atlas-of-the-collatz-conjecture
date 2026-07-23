# Structure–randomness transfer assessment, and an isolated test object for the remaining leap

**Date:** 22 July 2026
**Status:** assessment + one proved theorem + one explicit open test
question. **Not** a proof of Collatz, **not** a counterexample.
Sources read for this memo: Tao, *Structure and randomness in
combinatorics* (arXiv:0707.4269v2) and *Structure and randomness in the
prime numbers* (2009 expository). The repo's existing anchor, Tao's
almost-all-orbits paper (arXiv:1909.03562), is a different, quantitative
work; nothing here conflicts with it.

**Companion executable evidence:** `verify_structure_randomness.py`,
`test_verify_structure_randomness.py`, `structure_randomness_certificate.json`.

---

## 1. The question

What, if anything, does the structure–randomness method buy the Collatz
program beyond what the atlas already contains?

## 2. The crosswalk

| Tao, primes | Collatz atlas | status |
|---|---|---|
| Cramér random model | Bernoulli(1/2) parity model (Lagarias heuristic) | standard |
| Local obstructions (mod 2, mod 3, …) refine the model | Terras bijection: parity prefix of length `L` ⇔ one residue mod `2^L` | in repo, Theorem 1 |
| "Classify all conspiracies that could sink the conjecture; eliminate each" (Vinogradov program) | The wall program: periodic transcripts (decidable), complexity wall, drift wall, substitution obstruction | in repo; this is exactly the atlas's architecture |
| Collective statistics easier than single points ("weigh the box") | Tao 2019: almost-all orbits almost bounded; item 1 of the attack list asks to amplify one survivor to positive log-density | **open; no transfer found** |
| Pseudorandom residual after structure removal is computable-as-random | New content of this memo: the residual survives *every* symbolic wall, explicitly | §3 below |

The primes-paper playbook is already the atlas's architecture: the walls
**are** a conspiracy classification, and each exclusion theorem kills one
conspiracy class. So the honest question becomes: after all current
symbolic conspiracies are killed, what does the surviving region actually
contain? If it contained only pathological, unnamable words, one could
hope the next wall closes it. Theorem 1 below shows it contains an
absolutely explicit word.

## 3. Theorem 1 — the walls do not separate: an explicit survivor of every symbolic screen

Let \(C_3\in\{0,1,2\}^{\mathbb N}\) be the base-3 Champernowne word
(concatenation of the base-3 representations of \(1,2,3,\ldots\)), and
let \(\varphi:\{0,1,2\}\to\{0,1\}\) be \(\varphi(0)=\varphi(1)=1\),
\(\varphi(2)=0\). Define

\[
q^{*}=\varphi(C_3).
\]

**Statement.**

1. \(q^{*}\) is not eventually periodic.
2. \(\displaystyle s_L(q^{*})/L\to 2/3>\alpha=\log_3 2\).
3. \(\displaystyle p_{q^{*}}(k)=2^{k}\) for every \(k\ge1\) (full factor
   complexity, maximal entropy).

Hence \(q^{*}\) passes **every** screen currently in the atlas: the drift
wall (pointwise-drift-wall packet), the complexity wall (landmark memo,
Corollary 4), the bounded-discrepancy entropy requirement (its
Corollary 6, vacuously, since entropy is already full), the
primitive-uniform obstruction (not a substitution fixed point), and the
periodic cycle equation (not periodic).

**Proof.** \(C_3\) is normal in base 3: every word over \(\{0,1,2\}\)
occurs with frequency \(3^{-k}\) (Champernowne 1933). (2) is the case
\(k=1\): the digits \(0,1\) have combined frequency \(2/3\). (3): given a
binary word \(w\) of length \(k\), choose a ternary preimage \(t\) with
\(t_i=0\) where \(w_i=1\) and \(t_i=2\) where \(w_i=0\); \(t\) occurs in
\(C_3\), hence \(w\) occurs in \(q^{*}\). (1): an eventually periodic
word of period \(p\) has at most \(p\) factors of each length, while
\(q^{*}\) has \(2^k\); take \(2^k>p\). \(\square\)

The drift comparison is certified exactly:
\(2^3<3^2\Rightarrow\log_3 2<2/3\).

## 4. Corollary — symbolic closure is impossible; the residual is arithmetic

No exclusion criterion phrased purely in symbolic terms — factor
complexity, subword densities, critical discrepancy, topological entropy,
substitution/automatic/Toeplitz structure — can ever exclude \(q^{*}\),
because \(q^{*}\) extremalizes all of those statistics in the "guilty"
direction. The structure–randomness dichotomy, applied to the parity
word, therefore terminates with a pseudorandom-at-biased-level residual
that is *indistinguishable from guilty by symbolic means*.

The only remaining property that can separate \(q^{*}\) from a
counterexample is the ordinary-lift condition of the realizability wall:

\[
\Phi(q^{*})\in\mathbb Z_{>0}
\;\Longleftrightarrow\;
q^{*}\text{ is the parity transcript of a positive integer}
\;\Longleftrightarrow\;
\text{Collatz is false (divergent orbit).}
\]

**The entire residual difficulty of the conjecture is therefore witnessed
by one explicit, combinatorially trivial question:**

\[
\boxed{\;\text{Is }\Phi\bigl(\varphi(C_3)\bigr)\text{ a positive integer? (Expected: no.)}\;}
\]

- If **yes**: \(q^{*}\) is aperiodic with a positive-integer realization,
  hence a divergent Collatz orbit exists — the conjecture falls.
- If **no**: the proof cannot use any symbolic statistic (Theorem 1) and
  must attack the lift digits \(\varepsilon_L\) directly — i.e. it must
  invent precisely the machinery the landmark memo's target theorem (9.1)
  asks for. A technique that settles this one word very likely settles
  the class.

This is the structure–randomness method's real gift to the program: not a
new wall, but a **minimal explicit carrier** of everything that is still
hard, in the spirit of isolating a conjecture in one finite gadget —
except that here the gadget is one infinite word with a two-line
definition.

## 5. Lift-digit excursion statistics (numerical, non-rigorous)

The verifier computes the exact lift digits
\(\varepsilon_0,\ldots,\varepsilon_{N-1}\) of \(\Phi(q^{*})\bmod 2^{N}\)
for \(N=2^{16}\) via
\(\Phi(q)\equiv-\sum_{d_j<N}2^{d_j}\,3^{-(j+1)}\pmod{2^{N}}\),
with two controls:

- periodic transcript \((10)^\infty\): \(\Phi=1\), digits
  \(1,0,0,0,\ldots\) — eventually zero, as realizability requires;
- Fibonacci word: aperiodic, \(\Phi\) irrational by the complexity wall.

Observed (see certificate JSON): the digits of \(\Phi(q^{*})\) are
statistically indistinguishable from fair coin flips — one-density near
\(1/2\), longest zero-run of order \(\log_2 N\) — exactly like the
Fibonacci control and exactly unlike the realizable periodic control.
This is the numerical shape of the wall: nothing in the first \(2^{16}\)
lift digits of \(q^{*}\) is tending toward permanent zero. **These
statistics are a hypothesis generator, not evidence in the logical
sense; no finite computation can certify an eventually-zero tail.**

## 6. What does *not* transfer (stated plainly)

1. **Energy increment / regularity decompositions** are worst-case,
   tower-type quantitative tools for *collective* statistics. They do
   not produce a mechanism to amplify one divergent orbit into a
   positive-log-density set of them. Attack item 1 (parser-density
   amplification against Tao 2019) needs a different idea; we found none
   in these two texts.
2. **Inverse theorems for uniformity norms** (Gowers, Green–Tao–Ziegler)
   require the ambient object to carry group or nilspace structure. The
   parity-shift system is a 2-adic odometer conjugacy, not a group
   rotation on \(\mathbb Z/N\); no direct application was found.
3. **The primes' "weigh the box" move** works because primes form a
   large set. A hypothetical Collatz survivor is (conjecturally empty,
   at best) density zero; collective statistics cannot see it, which is
   exactly why almost-all results do not decide the conjecture.

## 7. What *does* transfer

1. The **conspiracy-classification architecture** (already the atlas's
   design) — now with a proved endpoint: the classification is complete
   on the symbolic side, and the last conspiracy is arithmetic.
2. The **isolation move**: reduce the residual difficulty to one
   explicit test object before building machinery. All future lift-digit
   work has a concrete benchmark: prove
   \(\Phi(\varphi(C_3))\notin\mathbb Z_{>0}\).
3. The **honesty norm** of both Tao texts: heuristic models are labeled
   heuristic; finite computations are controls, not proofs. Applied
   throughout.

## 8. Kill criteria and exact boundary

- Theorem 1 dies if an error is found in the normality argument or in
  the verifier's complexity/density certificates.
- The isolation claim (§4) dies if some symbolic statistic not yet
  considered separates \(q^{*}\) from realizability — by (3) of
  Theorem 1 it must be a statistic in which \(q^{*}\) is *not*
  extremal; we know of none.
- This memo proves nothing about \(\Phi(q^{*})\) itself; §5 is openly
  heuristic; no Collatz progress on the all-integers statement is
  claimed.

## 9. Related work

The structure/randomness framing follows Tao's program (*Structure and
randomness in combinatorics*, arXiv:0707.4269) and its Collatz instance
(arXiv:1909.03562). The word \(q^*\) is a Champernowne-type normal word;
its complexity and density properties are standard facts of symbolic
dynamics (Allouche–Shallit, 2003). What appears to be new is the use of
such a word as a *delimiting witness*: \(q^*\) passes every symbolic
wall the atlas can compute while \(\Phi(q^*)\notin\mathbb Z_{>0}\), so
no purely symbolic screen of this type can separate genuine integers
from non-integers. This is the symbolic analogue of the fence question
in the computability literature: Conway's generalized Collatz maps
encode universal computation (1972) and Kurtz–Simon (2007) prove a
\(\Pi^0_2\)-completeness result that explicitly does not apply to the
\(3n+1\) map itself — which side of the encoding fence \(3n+1\) sits on
is open, and is the subject of the atlas's fence program.

## 10. Reproduce

```bash
python3 contribution/packets/2026-07-22-structure-randomness-transfer/verify_structure_randomness.py
python3 -m pytest contribution/packets/2026-07-22-structure-randomness-transfer/ -q
```

Certificate: `structure_randomness_certificate.json`.
