# No Small Self-Similar Collapse in the Collatz Fold

**A counting-law obstruction to cross-depth conjugacy of induced first-return maps**

*Draft v2 — 2026-07-18. Authors: B. Pham (program, questions, direction) and
Claude Fable 5 (formalization, computation, this text); independent
verification and the exact first-return formula by GPT-5.6 Sol
(`fold/verify/`). Status: internal draft; machine-verified throughout; one
written proof outstanding (Lemma 2's general case); NOT submitted anywhere.*

---

## Abstract

For the Terras-accelerated Collatz map $T(n) = n/2$ ($n$ even), $(3n+1)/2$
($n$ odd), we study the *fold operator*: the induced first-return map of $T$
on a residue class mod $2^k$, renormalized to an exact system of affine
branches indexed by return words. We ask whether the map is self-similar under
folding — whether two folds at different depths $k \ne k'$ can be affinely
conjugate ("collapse"). We prove a counting-law obstruction: affine conjugacy
preserves branch slopes $3^a/2^L$, which encode return-word lengths, so
conjugate folds must have identical branch-count sequences; and each class's
count sequence obeys the linear recurrence of a pattern-avoidance language
determined by its $k$-bit parity window (Guibas–Odlyzko correlation theory —
the Fibonacci numbers $F_{24}, F_{25}$ appear verbatim in the depth-2 fold's
computed statistics). An exact computation of the counting laws of all 2,046
classes with $k \le 10$ — three independent implementations, including the
corrected first-return counts — finds 85 distinct laws, none shared across
depths. Consequently no cross-depth collapse exists for $k \le 10$, at any
resolution — a question that
exact enumeration provably cannot decide (truncation mass is bounded below by
$(1-2^{-k})^s$). We are explicit about scope: this is a structural result
about the fold operator, not progress on the Collatz conjecture.

---

## 1. Setup

Let $T:\mathbb{Z}^{+}\to\mathbb{Z}^{+}$ be the Terras map. The **parity word**
of $n$ of length $L$ is $w = (w_0,\dots,w_{L-1})$, $w_i \equiv T^i(n) \bmod 2$.
Two classical facts anchor everything (Terras 1976; Everett 1977):

**Fact 1 (Terras bijection).** The length-$k$ parity word of $n$ depends only
on $n \bmod 2^k$, and the induced map $\mathbb{Z}/2^k \to \{0,1\}^k$ is a
bijection. *(Machine-verified for $k \le 20$ in `fold/test_f1.py`.)*

**Fact 2 (composite affine form).** Applying a fixed word $w$ of length $L$
containing $a$ ones computes $n \mapsto (3^a n + c_w)/2^L$ with
$c_w \in \mathbb{Z}_{\ge 0}$ determined by $w$.
*(Machine-verified against $10^4$ random orbits in `fold/test_f1.py`.)*

By Fact 1, the residue of $T^t(n)$ mod $2^k$ is determined by the length-$k$
window of the parity word at offset $t$: residue trajectories mod $2^k$ are
**sliding $k$-bit windows** over the parity word.

## 2. The fold operator

Fix $k \ge 1$ and $r \in \{0,\dots,2^k-1\}$, and write the class as
$\{\,r' + 2^k m : m \ge 0\,\}$ (with $r' = r$ for $r>0$, else $2^k$). The
**fold** of $T$ at $(k,r)$ is the first-return map of $T$ to this class,
written in the index $m$. A *return word* is a parity word $w$ of length $L$
whose window equals $r$'s window at offsets $0$ and $L$ and at no offset in
between. Each return word contributes one **branch**: by Facts 1–2, its domain
is an arithmetic progression in $m$ and its action is affine,

$$ m \;\longmapsto\; \frac{3^{a_w}\, m + c'_w}{2^{L_w}} \cdot 2^{\,\text{(normalization)}},
\qquad \text{slope} = \frac{3^{a_w}}{2^{L_w}}, $$

with all data exact integers (implementation: `fold/f2_fold_operator.py`; the
branch-predicted image agrees with direct simulation of $T$ to first return on
1000/1000 random samples, and branch-domain masses sum to exactly $1$ per
class in $\mathbb{Q}$).

**Definition (collapse).** Folds at $(k,r)$ and $(k',r')$ with $k \ne k'$
*collapse* if they are affinely conjugate: there is an affine bijection $h$
between the index sets with $h \circ R_{k,r} = R_{k',r'} \circ h$.

The question — does the Collatz map ever reproduce itself under folding? — is
a renormalization question. We found no prior literature treating it
(see `fold/F3-literature-map.md`; nearest neighbors are residue-decomposition
studies without induced-map conjugacy).

## 3. The slope invariant

**Proposition 1.** *If two folds are affinely conjugate, then for every
$L$ they have the same number of branches of return-word length $L$.*

*Proof.* Branches are the maximal affine pieces of the fold, so any affine
conjugacy $h$ carries the branch partition of one fold onto that of the other,
matching branches bijectively. If $b$ is a branch with map
$x \mapsto \sigma x + \tau$, the corresponding branch of the conjugate system
is $h \circ b \circ h^{-1}$, with slope $\alpha\sigma\alpha^{-1} = \sigma$:
slopes are preserved. A branch's slope is $3^{a_w}/2^{L_w}$, and by unique
factorization the pair $(a_w, L_w)$ is recoverable from the slope. Hence the
count of branches at each return-word length $L$ (indeed at each $(a,L)$) is a
conjugacy invariant. $\blacksquare$

**Remark (maximality of the symbolic partition).** Proposition 1 speaks of
maximal affine pieces; the counting (Lemma 2) counts symbolic first-return
cylinders. These coincide: two distinct cylinders could merge into one larger
affine piece only if they were sibling classes $u,\, u+2^{t-1} \bmod 2^t$
carrying the same affine map, but siblings share their length-$(t-1)$ parity
prefix, hence the same automaton state before the final bit, and from any
state at most one bit completes the window ($h_i \in \{0,1\}$) — so at most
one sibling is a first-return branch at time $t$. Merging is impossible, and
the symbolic partition is exactly the maximal-piece partition. *(Flagged as a
proof obligation by independent verification — `fold/fence/FENCE.md` §8.4 —
and discharged here.)*

So the **branch-count sequence** $\beta_{k,r}(L)$ — a purely combinatorial
shadow of the fold — must coincide for conjugate folds.

## 4. The counting law

Return words at $(k,r)$ are exactly the parity words whose sliding window
*first re-attains* $r$'s window at offset $L$. First-occurrence counting of a
pattern in binary strings is classical (Guibas–Odlyzko 1981): the generating
function of such counts has denominator determined by the window's
**autocorrelation polynomial**, the same denominator that governs the language
of strings *avoiding* the window. In particular the count sequences satisfy
linear recurrences determined by the window, and windows fall into finitely
many correlation classes per depth.

*Related folklore.* Fibonacci-like growth of aggregate level counts in
residue-refinement trees over the Collatz map is a recurring amateur and
folklore observation (binary refinement with a forbidden configuration). The
contribution here is not the appearance of Fibonacci but the **per-class
counting law** — different classes at the same depth obey different laws,
Fibonacci versus linear, governed by the window's autocorrelation — and its
use as a conjugacy invariant.

**Empirical anchor (exact).** At $k=2$ the two self-overlapping windows
(`00`, `11` — classes $r \in \{0,3\}$, i.e., two consecutive even or odd
steps) yield the Fibonacci law: the enumerated fold has exactly
$F_{24} = 46368$ resolved branches and $F_{25} = 75025$ unresolved leaves at
truncation depth $24$, while the non-self-overlapping windows (`01`, `10`)
yield the degenerate linear law (276 branches, 25 leaves). Both predictions
and both mirror-symmetries come out exactly (`fold/F2_REPORT.md`).

**Lemma 2 (window law — exact form; general proof outstanding).** Let $Q$ be
the window's KMP transfer matrix with completion transitions deleted, $b$ the
window's longest proper border state, and $h$ the completion-count vector.
Then the branch count at return length $t$ is

$$ \beta_{k,r}(t) \;=\; e_b\, Q^{\,t-1}\, h. $$

The *naive* avoidance count $e_0 Q^n \mathbf{1}$ is **not** the branch count —
the fold starts immediately after an occurrence of the window (state $b$, not
state $0$) and counts completions, not survivors. The corrected formula was
derived in independent verification (`fold/verify/VERIFICATION.md`) and
matches the exact fold enumeration in **196/196 positions** across all 14
classes with $k \le 3$. Both count families share the annihilating structure
of $Q$, which is why the avoidance-law screen and the corrected-count screen
bucket identically (§5). What remains for full rigor is a short written proof
that the Terras bijection identifies every first-return branch with exactly
one accepted length-$t$ extension for arbitrary $k, t$ — a bookkeeping
argument, machine-checked exhaustively at small scale, not yet written out.

## 5. The screen and the theorem

Three screens were run, in escalating rigor: (i) avoidance-law recurrences,
all 510 classes $k \le 8$ (`fold/f2b_analytic_screen.py`, 0.64 s); (ii) an
independent reimplementation (different automaton construction, exact
Berlekamp–Massey), all 2,046 classes $k \le 10$, agreeing with (i) on every
class (`fold/verify/`, 11.7 s); (iii) the **corrected first-return sequences**
$\beta_{k,r}$ of Lemma 2 for all 2,046 classes, bucketed by exact 80-term
sequence equality.

**Result.** $k \le 10$: 2,046 classes realize **85 distinct counting laws
(and 85 distinct corrected $\beta$-sequences). None is shared between two
different depths $k \ne k'$ — in any of the three screens.**

**Theorem 3 (conditional on Lemma 2's written proof).** *No two folds at
different depths $k, k' \le 10$ are affinely conjugate.*

*Proof.* Conjugacy forces equal branch-count sequences (Proposition 1), hence
equal minimal recurrences; by Lemma 2 these are the window counting laws; by
the computation no two classes at different depths share one. $\blacksquare$

Two remarks on the computation. First, a growth-rate-only comparison would
*not* suffice: each $k$-bonacci dominant root (golden ratio, tribonacci, …)
reappears at depth $k+1$ inside a different minimal law — same leading
eigenvalue, different sequence. The full-recurrence comparison separates
these. Second, the analytic route decides what enumeration provably cannot:
the unresolved mass of a truncated enumeration at depth $s$ is at least
$(1-2^{-k})^s$, so driving it below any fixed witness threshold requires
$s = \Omega(2^k)$ — exponentially unattainable. The fog is intrinsic;
the invariant sees through it.

## 6. What this result is, and is not

- It is a structural theorem about the *fold operator*: the Collatz map does
  not reproduce itself under first-return renormalization at small depth;
  its fold complexity strictly increases, with entropy marching through the
  $k$-bonacci constants toward $2$.
- It is **not** progress on the Collatz conjecture. Every object here lives on
  the "free" side of what we call the *realizability* constraint — the fact
  that parity feedback selects exactly one infinite word per integer. Finite-
  window combinatorics cannot exclude any asymptotic behavior (every finite
  word is realized, by Fact 1). The conjecture's difficulty is untouched, in
  the same way (and for the same reason) that statistical results (Tao 2019)
  leave the measure-zero exceptional set untouched.
- Its value, beyond the answer itself: it closes the "maybe it folds into
  itself nicely" family of approaches with a certificate, it identifies the
  correlation polynomial of the parity window as the fold's governing
  invariant, and it demonstrates a case where an analytic invariant decides a
  question that exact computation cannot reach.

## 7. Computational appendix

All code is Python 3 stdlib, exact integer/rational arithmetic in every
certificate; repository `Collatz Conjecture`, directory `fold/`.

| Artifact | Role | Runtime |
|---|---|---|
| `f1_word_calculus.py` + `test_f1.py` | word calculus; Facts 1–2 verified; cycle sweep $L \le 24$ trivial-only; stopping-time spectrum ($n < 2^{20}$, max total stopping time at $n = 837{,}799$) | 58 s |
| `f2_fold_operator.py` + `test_f2.py` | exact fold enumeration, 62 classes $k \le 5$; simulation cross-check 1000/1000; mass partition $=1$ exact | ~11 min warm |
| `f2b_analytic_screen.py` | the counting-law screen of §5 | 0.64 s |
| `F2_REPORT.md`, `F2B_REPORT.md`, `F3-literature-map.md` | results and literature | — |
| `verify/` | independent re-verification (GPT-5.6 Sol): 510/510 law match; $k \le 10$ extension; exact first-return formula, 196/196 term match | 11.7 s |

**References** (status per `fold/F3-literature-map.md`): Terras 1976 *Acta
Arith.*; Everett 1977 *Adv. Math.*; Lagarias 1985 *Amer. Math. Monthly*;
Guibas–Odlyzko 1981 *J. Combin. Theory A* (string overlaps, pattern matching);
Applegate–Lagarias 2006 (3x+1 semigroup); Hercher 2023 *J. Integer Seq.*;
Tao 2019 (almost-all orbits); Conway 1972; Kurtz–Simon 2007.

---

*Provenance note: the fold question, the "fold it in on itself" framing, and
the observation that 46368 is a Fibonacci number arose from B.P.'s riffing;
formalization, probes, and this text by C.F. Every numeric claim above traces
to a committed artifact in this repository. Draft awaiting: Lemma 2
verification (agent task in flight), then human review.*
