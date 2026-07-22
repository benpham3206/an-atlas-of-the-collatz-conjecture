# Exact counterexample search: cycle branch

**Verdict:** no unconditional positive-integer Collatz counterexample was found.
The search below is exhaustive for every nontrivial odd-only cycle with at
most 18 odd members, and it found none. This is a verified bounded exclusion,
not a resolution of the Collatz conjecture.

The result file is `contribution/code/fence/exact_cycle_search_results.json`.

## Why the cycle branch

There are only two ways the positive-integer Collatz conjecture can fail:

1. a positive orbit enters a nontrivial cycle; or
2. a positive orbit is unbounded.

A cycle is the only branch with a finite unconditional certificate: list its
positive states and verify one exact return. A long trajectory that has not
yet descended is not a divergence certificate, regardless of its height,
entropy, or runtime cap.

This search therefore targeted a nontrivial cycle. It did not change the map,
admit zero or negative integers, or treat a rational 2-adic orbit as a Collatz
counterexample.

## Exact cycle certificate

Use the odd-only map

\[
U(n)=\frac{3n+1}{2^{v_2(3n+1)}}
\]

on positive odd integers. For a proposed cycle of \(m\) odd states, let

\[
a_i=v_2(3n_i+1),\qquad K=\sum_{i=0}^{m-1}a_i.
\]

Define

\[
S_0=0,\quad C_0=0,
\]

and

\[
C_{j+1}=3C_j+2^{S_j},
\qquad
S_{j+1}=S_j+a_j.
\]

Then

\[
U^m(n)=\frac{3^mn+C_m}{2^K}.
\]

A fixed point must therefore be

\[
\boxed{n=\frac{C_m}{2^K-3^m}}.
\]

The executable acceptance gate requires all of the following:

1. \(2^K>3^m\);
2. \((2^K-3^m)\mid C_m\);
3. the quotient \(n\) is a positive odd integer;
4. direct iteration observes exactly the proposed valuations \(a_i\);
5. the final state equals the initial state; and
6. the orbit is not the trivial odd-only fixed point \(\{1\}\).

These conditions are exact integer equalities. No floating-point comparison
or heuristic score participates in acceptance.

## A complete finite search window

Multiplying

\[
2^{a_i}=3+\frac1{n_i}
\]

around a cycle gives

\[
2^K=\prod_{i=0}^{m-1}\left(3+\frac1{n_i}\right)>3^m.
\]

A nontrivial positive cycle cannot contain `1`. It also cannot contain `3` or
`5`, because

\[
3\mapsto5\mapsto1,
\qquad
5\mapsto1
\]

under the odd-only map. Thus every state in a nontrivial cycle is at least
`7`, and

\[
2^K\le\left(3+\frac17\right)^m
=\left(\frac{22}{7}\right)^m.
\]

Consequently, for each fixed \(m\), every nontrivial cycle lies in the exact
finite window

\[
\boxed{3^m<2^K\le(22/7)^m.}
\]

For \(m\le18\), only the following pairs survive:

| odd members \(m\) | total valuation \(K\) | ordered compositions |
|---:|---:|---:|
| 5 | 8 | 35 |
| 8 | 13 | 792 |
| 10 | 16 | 5,005 |
| 11 | 18 | 19,448 |
| 13 | 21 | 125,970 |
| 14 | 23 | 497,420 |
| 15 | 24 | 817,190 |
| 16 | 26 | 3,268,760 |
| 17 | 27 | 5,311,735 |
| 17 | 28 | 13,037,895 |
| 18 | 29 | 21,474,180 |

All other \((m,K)\) pairs with \(m\le18\) violate one of the two exact power
inequalities. The number of ordered compositions is
\(\binom{K-1}{m-1}\).

## Result

The primary implementation exhaustively evaluated:

\[
44{,}558{,}430
\]

ordered positive valuation words, representing

\[
2{,}578{,}829
\]

cyclic classes after exact Burnside counting.

It found:

- zero integral candidates in the nontrivial search window;
- zero verified nontrivial positive cycles;
- the expected trivial control \(a=(2)\), \(n=1\).

An independent combinations-based oracle, which did not import the search
module, repeated all 23,084,250 words through \(m=17\) and the 21,474,180
words at \((18,29)\). It also found zero cycles.

Therefore:

\[
\boxed{\text{There is no nontrivial positive Collatz cycle with at most 18 odd members.}}
\]

This conclusion is unconditional inside the stated finite class.

## Why enumeration stops here

The next layer, \((m,K)=(19,31)\), contains 86,493,225 ordered compositions.
It is computationally feasible with more engineering, but it would add no
meaningful mathematical frontier.

Hercher proved that if convergence is verified through
\(1536\cdot2^{60}=3\cdot2^{69}\), then every nontrivial cycle has more than
\(1.375\cdot10^{11}\) odd members. Bařina's subsequent computation verified
convergence through \(2^{71}\), which exceeds that hypothesis. Thus published
work already dominates an extension from 18 to 19 by roughly ten orders of
magnitude.

The Musk-style deletion decision is therefore exact: delete further naive
valuation-word enumeration. It cannot catch up with the known lower bound and
cannot touch the divergent-orbit branch.

## What remains for a complete counterexample

No counterexample is currently present in the artifacts. A complete
unconditional counterexample would require one of:

1. **Cycle certificate:** a positive integer list closing under the fixed
   `3n+1` rule and not containing the trivial cycle. The verifier would accept
   this immediately.
2. **Divergence proof:** one positive starting integer together with an
   infinite invariant or monotone certificate proving its orbit never returns
   to a bounded set. No finite prefix, cap exit, or apparent positive drift is
   sufficient.

The exact obstruction is no longer search implementation. It is the absence
of either certificate. Producing one would disprove a famous open conjecture;
declaring one without the certificate would only rename an unverified finite
observation.

## Reproduction

The search engine and tests are:

- `contribution/code/fence/exact_cycle_search.py`
- `contribution/code/fence/test_exact_cycle_search.py`
- `contribution/code/fence/exact_cycle_search_results.json`

The persisted JSON lists every searched pair, pre- and post-symmetry counts,
all integral candidates, direct verification fields, structured errors, and
the empty `nontrivial_counterexamples` list.

## Sources

- Christian Hercher, *There are no Collatz m-Cycles with m <= 91*:
  https://arxiv.org/abs/2201.00406
- David Bařina, *Improved verification limit for the convergence of the
  Collatz conjecture*:
  https://doi.org/10.1007/s11227-025-07337-0
- Jeffrey Lagarias, *The 3x+1 problem and its generalizations*:
  https://www.cecm.sfu.ca/organics/papers/lagarias/

