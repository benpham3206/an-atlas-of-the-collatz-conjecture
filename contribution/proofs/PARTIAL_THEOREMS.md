# Partial fence theorems

These results locate exact weak regions and exact obligations on any encoding.
None decides the Collatz conjecture or the reachability relations of the fixed
`3n+1` map.

## Theorem 1 — finite-cylinder saturation

**Statement.** For every `L>=1` and every binary word `w` of length `L`, there
is exactly one residue `rho_L(w) mod 2^L` such that

\[
n\text{ begins with parity word }w
\quad\Longleftrightarrow\quad
n\equiv\rho_L(w)\pmod {2^L}.
\]

Consequently every finite parity transcript occurs, and a length-`L` transcript
contains exactly the same information as `L` low 2-adic bits of the starting
integer.

**Proof.** This is the Terras bijection, applied in both directions. The
forward implication follows because the parity prefix depends only on the
residue modulo `2^L`; injectivity says no second residue realizes `w`;
surjectivity says one does. `\square`

**Encoding consequence.** A proposed `L`-step control block does not select an
individual computation state. It selects one arithmetic progression
`rho_L(w)+2^L Z`. Conversely, there is no forbidden finite control block from
which to derive a local weakness theorem. Any fence must use compatibility
across unbounded lengths, positivity/integrality, or another global condition.

**Audit: VALID.** This does not claim that every infinite word is realized by
a positive integer, nor that all finite-state analyses are useless. It rules
out only arguments whose obstruction is a missing finite parity word or a
proper finite-window subshift.

## Theorem 2 — exact global realizability criterion

Let `q=q_0q_1...` be an infinite binary sequence, and let

\[
d_0<d_1<\cdots
\]

be the positions of its ones. Define, with a finite sum if there are finitely
many ones,

\[
\Phi(q)=-\sum_{j\geq0}\frac{2^{d_j}}{3^{j+1}}\in\mathbb Z_2.
\]

**Statement.** The series converges 2-adically and `Phi(q)` is the unique
2-adic integer whose parity vector under the extended Terras map is `q`.
Therefore `q` is realized by a positive integer orbit if and only if

\[
\Phi(q)\in\mathbb Z_{>0}\subset\mathbb Z_2.
\]

**Proof.** Since `d_j -> infinity` when the set of ones is infinite and `3` is
a 2-adic unit, the valuations of the summands tend to infinity; hence the
series converges in `Z_2`.

Let `sigma q` delete the first bit. If `q_0=0`, all `d_j>=1`, so `Phi(q)` is
even and direct division of the series gives

\[
\Phi(q)/2=\Phi(\sigma q).
\]

If `q_0=1`, then `d_0=0`, so

\[
\Phi(q)=-\frac13-\sum_{j\geq1}\frac{2^{d_j}}{3^{j+1}}
\]

is odd in `Z_2`, and

\[
\frac{3\Phi(q)+1}{2}
=-\sum_{j\geq1}\frac{2^{d_j-1}}{3^j}
=\Phi(\sigma q).
\]

Thus one Terras step shifts the prescribed sequence and its parity is the
prescribed first bit. Induction gives all bits of `q`.

For uniqueness, if two 2-adic integers have the same first `L` parity bits,
the finite Terras bijection makes them congruent modulo `2^L`. Agreement for
every `L` makes them equal in `Z_2`. The positive-integer criterion now follows
from uniqueness. `\square`

**Encoding consequence.** Suppose a simulator assigns control blocks along an
infinite machine run and concatenates them into `q`. Finite Terras congruences
guarantee a compatible 2-adic starting state, namely `Phi(q)`. They do **not**
guarantee a positive-integer starting state. Any exact positive-integer
simulation must prove `Phi(q)>0` and integral in the ordinary sense, for every
encoded initial configuration, and must prove that each block boundary lands
back in the code set. This is the realizability wall in a single formula.

**Audit: VALID.** The theorem is a conjugacy formula over `Z_2`, not a claim
about convergence in the ordinary real metric. It makes no assertion that the
positive-integer membership test is decidable for arbitrary computable `q`.

## Theorem 3 — eventually periodic transcripts are a decidable weak island

**Statement.** If `q` is eventually periodic, `Phi(q)` is an effectively
computable rational number. Whether it is a positive integer is decidable.
If it is a positive integer, its `T`-orbit is eventually periodic. Hence this
transcript class cannot support a step-faithful injective simulation of an
infinite machine run with infinitely many distinct configurations.

**Proof.** Split `q` into a finite prefix of length `h` and a period of length
`p`. If the period contains `m>0` ones, group the tail terms in Theorem 2 by
period. Each repetition multiplies the grouped contribution by

\[
2^p/3^m,
\]

whose 2-adic absolute value is less than one. The tail is therefore an exact
rational geometric sum. If the period has no ones, only the finite-prefix
terms remain. Thus `Phi(q)` is rational and can be reduced exactly; checking
denominator `1` and positive numerator decides positive-integral membership.

If `q` is realized by `n>0`, then the parity vector of `T^h(n)` is
`sigma^h q`. Periodicity gives

\[
Q(T^{h+p}n)=\sigma^{h+p}q=\sigma^h q=Q(T^h n),
\]

where `Q` denotes the parity-vector map. The uniqueness part of Theorem 2
implies `T^{h+p}n=T^h n`. Thus the integer orbit is eventually periodic and
contains only finitely many distinct states. An injective code cannot map an
infinite distinct machine run into it. `\square`

**Audit: VALID.** This excludes only eventually periodic control transcripts.
It does not quantify over all encodings or over automatic, morphic, or general
computable transcripts.

## Theorem 4 — the `a=1` two-branch family is nonuniversal under orbit embedding

For a fixed positive odd `b`, define

\[
S_b(n)=\begin{cases}n/2,&n\text{ even},\\(n+b)/2,&n\text{ odd}.
\end{cases}
\]

**Statement.** Every positive orbit of `S_b` enters the finite invariant set
`{1,...,b}` and is eventually periodic. Point-to-point reachability is
decidable. Consequently `S_b` cannot step-faithfully simulate any machine
class containing an infinite run with pairwise distinct configurations under
an injective encoding.

**Proof.** If `n>b`, then the even branch gives `n/2<n`; the odd branch gives
`(n+b)/2<n` because `b<n`. Hence the orbit strictly decreases until it enters
`{1,...,b}`. That set is invariant: for even `n<=b`, `n/2<=b`, and for odd
`n<=b`, `(n+b)/2<=b`. A deterministic orbit in a finite set repeats and is
eventually periodic.

To decide whether the orbit of `x` reaches `y`, iterate while recording visited
states; answer yes on `y` and no on the first repeat. Termination follows from
the preceding paragraph. Finally, an injective step simulation of an infinite
distinct machine run would require an integer orbit with infinitely many
distinct encoded states, which does not exist. `\square`

**Position of `3n+1`.** Within positive odd multipliers, `a=3` is the first
case outside this elementary descent proof. This is a threshold for the
particular well-founded ranking `n`, not a proved universality threshold.

**Audit: VALID.** The theorem fixes `b>0`, uses the explicit step-simulation
definition, and does not claim that every conceivable weaker coding into
finite orbit statistics is impossible. It says nothing about `a=3` beyond
locating it outside the proved subclass.

