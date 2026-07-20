# Formalizing the computational-encoding fence

## 1. The fixed map and three different decision questions

Use the accelerated map

\[
T(n)=\begin{cases}n/2,&n\text{ even},\\(3n+1)/2,&n\text{ odd}.
\end{cases}
\]

It is the two-branch map represented by the matrices in §3. For the target
`1`, reachability under `T` is equivalent to reachability under the usual
unaccelerated `3n+1` map: acceleration only skips the even intermediate
`3n+1`, which cannot itself be `1`. Binary reachability to arbitrary targets
is different, so all definitions below use `T` explicitly.

Define

\[
H_T=\{n>0:\exists t\geq0,\ T^t(n)=1\}
\]

and

\[
R_T=\{(n,m)>0:\exists t\geq0,\ T^t(n)=m\}.
\]

The global Collatz sentence is

\[
C_T:\quad \forall n>0\ \exists t\geq0\ [T^t(n)=1].
\]

These are not interchangeable:

1. `H_T` and `R_T` are computably enumerable: simulate the unique orbit and
   accept when the target is reached.
2. `H_T` many-one reduces to `R_T` by `n -> (n,1)`. Therefore decidability of
   `R_T` implies decidability of `H_T`; no converse is established here.
3. `C_T` is a syntactic `Pi^0_2` arithmetic sentence because its bracketed
   predicate is decidable. A single fixed sentence is not thereby
   `Pi^0_2`-complete, undecidable, or independent.
4. If `C_T` is true, then semantically `H_T` is all positive integers and is
   decidable. If `H_T` were proved undecidable, `C_T` would therefore be false.
   The converse fails: a false `C_T` can coexist with either a decidable or an
   undecidable `H_T`.
5. A decision procedure for `H_T` would not by itself settle `C_T`: one must
   still decide whether that procedure ever outputs “no” over all inputs.

Kurtz and Simon study a parameterized collection of generalized Collatz maps;
the input includes the map description. Their global problem is
`Pi^0_2`-complete. Their result does **not** classify this fixed `T`.
Conflating the index problem for a family of maps with the one fixed Collatz
sentence is the first fence error to avoid.

## 2. What “simulate a machine” must mean here

Let a deterministic machine be a computable transition system
`(C, delta, Halt)` on configurations. Three strengths should be kept separate.

### 2.1 Step-faithful orbit embedding

A strict step simulation by `T` consists of

- a computable injection `E:C -> N+`;
- a computable delay `s(c)>=1` for nonhalting `c`; and
- the identity

\[
T^{s(c)}(E(c))=E(\delta(c)).
\]

For unambiguous macro-step boundaries one may additionally require that no
intermediate iterate `T^j(E(c))`, `0<j<s(c)`, lies in `E(C)`. A simulation of
a class is uniform if one algorithm computes `E` and `s` from program and
configuration descriptions.

### 2.2 Halting-set reachability simulation

A weaker simulation consists of a computable encoding `E` and a decidable
target set `D` such that

\[
c\text{ eventually halts}\quad\Longleftrightarrow\quad
\exists t\ T^t(E(c))\in D.
\]

This transfers the machine halting problem to reachability of a **set** under
`T`, but not necessarily to `H_T` or to point-to-point reachability.

### 2.3 Fixed-target simulation

The strongest version uses `D={1}`. A uniform fixed-target simulation of a
universal deterministic machine would many-one reduce its halting problem to
`H_T`, proving `H_T` undecidable. By §1(4), it would also imply that `C_T` is
false. This is a conditional relationship, not a claim that such a simulation
exists.

### 2.4 The parity-forcing condition

Let `w(c)` be the parity block used during a proposed macro-step and let
`L=s(c)`. If `a(w)` is its number of odd symbols, the word calculus forces

\[
E(\delta c)=\frac{3^{a(w)}E(c)+c_w}{2^L},
\qquad
E(c)\equiv\rho_L(w)\pmod {2^L},
\]

where `rho_L(w)` is the unique Terras residue realizing `w`. The second
condition is not optional. Choosing a convenient word and applying its affine
formula without the congruence condition smuggles free control into a
deterministic orbit.

Moreover, satisfying every finite macro-step separately is insufficient. The
concatenated infinite control transcript must be the parity vector of one
positive integer. `PARTIAL_THEOREMS.md`, Theorem 2, gives the exact 2-adic
test for that global condition.

Determinism itself is not an anti-universality theorem: deterministic universal
Turing machines exist. What is missing here is a programmable branch table.
The two coefficients and the parity guard are fixed, and the entire infinite
control transcript must be globally realized by one positive integer.

## 3. Guarded matrix-semigroup framing

In homogeneous coordinates put

\[
M_0=\begin{pmatrix}1/2&0\\0&1\end{pmatrix},\qquad
M_1=\begin{pmatrix}3/2&1/2\\0&1\end{pmatrix}.
\]

Then `M_0(n,1)^T=(T(n),1)^T` when `n` is even, and similarly for `M_1`
when `n` is odd. For a word `w=w_0...w_{L-1}`,

\[
M_{w_{L-1}}\cdots M_{w_0}
=\begin{pmatrix}3^{a(w)}/2^L&c_w/2^L\\0&1\end{pmatrix}.
\]

There are two distinct reachability relations:

- **Free semigroup reachability:** does *some* word `w` satisfy
  `M_w(n,1)^T=(m,1)^T`?
- **Parity-guarded reachability:** does such a word exist **and** satisfy, at
  every prefix, that `w_i` is the parity of the current integer state?

For fixed `n` and `L`, exactly one length-`L` word is guard-admissible. Thus

\[
(n,m)\in R_T
\quad\Longleftrightarrow\quad
\exists L\ [M_{w(n,L)}(n,1)^T=(m,1)^T],
\]

where `w(n,L)` is forced, not guessed. Free semigroup reachability is an
over-approximation and cannot transfer undecidability without a proof that its
witness words satisfy the guard.

### 3.1 What neighboring matrix results do and do not say

- Kannan–Lipton point reachability for powers of **one** rational matrix is
  decidable in polynomial time. It does not cover guarded switching between
  two matrices.
- Free reachability under a finite set of one-dimensional **integer** affine
  functions is decidable (Fremont gives a `2-EXPTIME` algorithm). The Collatz
  pair uses rational affine maps whose integer-valid applications are selected
  by a state guard, so this is a neighbor, not a reduction.
- General reachability for one-dimensional two-interval piecewise-affine maps
  remains a frontier; the injective subclass is decidable. The Collatz map is
  noninjective (`T(1)=T(4)=2`), so that positive result does not apply.
- Generic matrix mortality asks whether a free product is the zero matrix.
  Here `det(M_0)=1/2` and `det(M_1)=3/2`; every product is invertible. Mortality
  is therefore impossible for this pair. Paterson's undecidability for finite
  sets of `3x3` integer matrices, and low-dimensional mortality complexity
  results, provide no answer to guarded reachability for this fixed pair.

The exact matrix fence question is therefore: **is point reachability for this
one fixed pair under this one arithmetic guard decidable?** None of the cited
free-semigroup or single-matrix theorems answers it.

## 4. Formal fence questions

The phrase “which side of the fence?” resolves into at least these questions:

1. Is `H_T` decidable? Is the stronger binary relation `R_T` decidable?
2. Does `T` admit a uniform step-faithful embedding of a universal deterministic
   transition system into positive-integer orbits?
3. Does it admit only a weaker halting-set simulation, or the much stronger
   fixed-target simulation to `1`?
4. Is guarded reachability for `(M_0,M_1)` decidable even though nearby free
   semigroup problems can be hard and single-matrix orbit reachability is easy?
5. For what restricted transcript generators can the positive-integer
   realizability test be decided?

No equivalence among all five is asserted. The proved implications above are
one-way unless explicitly marked otherwise.

