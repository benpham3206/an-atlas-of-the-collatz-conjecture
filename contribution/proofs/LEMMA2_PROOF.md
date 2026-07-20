# Lemma 2: exact first-return branch count

**Status: PROVEN.** The statement is true for every `k >= 1` and `t >= 1`
when “branch” has the meaning used by the fold implementation and by
`fold/note/NOTE.md`: a symbolic first-return cylinder in the index `m`.

## Statement with all conventions fixed

Let

\[
T(n)=\begin{cases}n/2,&n\equiv0\pmod2,\\(3n+1)/2,&n\equiv1\pmod2\end{cases}
\]

on the positive integers. Fix `k >= 1` and a class `r mod 2^k`. Put
`r* = r` for `r > 0` and `r* = 2^k` for `r = 0`, so the class is indexed by

\[
n_m=r^*+2^k m,\qquad m\geq0.
\]

Let `w=w_0...w_{k-1}` be the common length-`k` parity word of this class.
Use the KMP automaton for `w`, with nonterminal states `0,...,k-1`; state `i`
means that the longest suffix read so far which is a prefix of `w` has length
`i`. A transition which reaches state `k` completes `w`. Let

- `b` be the length of the longest proper border of `w`;
- `Q_{ij}` be the number of bits in `{0,1}` which take nonterminal state `i`
  to nonterminal state `j` without completing `w`;
- `h_i` be the number of bits which complete `w` from state `i`; and
- `e_b` be the row vector concentrated at state `b`.

Let `B_w(t)` be the number of canonical fold cylinders `m = u mod 2^t` on
which the first positive return of `n_m` to `r mod 2^k` occurs at time `t`.
Then

\[
\boxed{B_w(t)=e_bQ^{t-1}h.}
\]

## Proof

### 1. Refinements of `m` are exactly extensions of the initial word

The Terras bijection says that length-`L` parity words are in bijection with
residues modulo `2^L`. Apply it with `L=k+t`.

For `u mod 2^t`, the residue

\[
n_u=r^*+2^k u\pmod {2^{k+t}}
\]

is well defined. Distinct `u mod 2^t` give distinct residues modulo
`2^{k+t}`. Every resulting length-`k+t` parity word starts with `w`, because
reducing `n_u` modulo `2^k` returns the fixed class `r`.

Conversely, let `wx` be any binary word of length `k+t` whose first `k` bits
are `w`, where `x` has length `t`. The Terras bijection gives one residue
`n mod 2^{k+t}` realizing `wx`. Its reduction modulo `2^k` realizes `w`, so,
again by injectivity of the length-`k` Terras map, that reduction is `r`.
Thus `n` has a unique expression `r^*+2^k u mod 2^{k+t}` with
`u mod 2^t`.

Therefore

\[
u\pmod {2^t}\longleftrightarrow x\in\{0,1\}^t
\]

is a bijection between index cylinders and length-`t` extensions of the
already-fixed initial copy of `w`.

### 2. First return is exactly first completion in the extension

Write the parity word of `n_u` through time `k+t-1` as `wx`. For
`1 <= j <= t`, the length-`k` parity word of `T^j(n_u)` is the sliding window
at positions `j,...,j+k-1`; all these positions lie inside `wx`. By the
length-`k` Terras bijection,

\[
T^j(n_u)\equiv r\pmod {2^k}
\quad\Longleftrightarrow\quad
(wx)_{j}\cdots(wx)_{j+k-1}=w.
\]

The initial `w` has already completed at shift `0`. To search for the next
possibly overlapping occurrence, KMP resumes in state `b`, the longest
proper suffix of this occurrence which is also a prefix of `w`. Reading the
first `j` bits of `x` completes `w` exactly when the window beginning at
shift `j` equals `w`. Consequently the first positive return time is `t` if
and only if

- the first `t-1` bits of `x` make only noncompletion transitions, and
- the last bit of `x` completes `w`.

This includes overlapping returns. For example, after `00` the correct state
is `1`, so the next `0` records the return `00 -> 00` at shift one.

### 3. Each accepted extension is exactly one fold branch

By Step 1, an accepted `x` determines one and only one cylinder
`m = u mod 2^t`. Every positive `m` in that cylinder has the same parity
prefix `wx`, hence the same first return time `t`. On that cylinder the fixed
first `t` parity steps have the composite form

\[
T^t(n)=\frac{3^a n+c}{2^t}.
\]

Substituting `m=u+2^t q` makes the returned class index an affine integer
function of the free parameter `q`. This is precisely a resolved branch in
`fold/f2_fold_operator.py`.

No two accepted extensions give the same symbolic branch: they give distinct
residues `u mod 2^t`. Nor can a coarser index cylinder determine that extension,
because it contains more than one residue modulo `2^t`. Thus the branch
refinement depth is exactly `s=t`, matching the independent engine read-back.

### 4. Transfer-matrix count

Starting from `b`, matrix multiplication by `Q` counts one-symbol extensions
which remain in nonterminal states. Inductively, the `i`-th component of
`e_bQ^{t-1}` is the number of length-`t-1` prefixes which avoid completion and
end in state `i`. From state `i`, exactly `h_i` choices for the final bit
complete `w`. Summing over `i` gives

\[
B_w(t)=\sum_i(e_bQ^{t-1})_i h_i=e_bQ^{t-1}h.
\]

For `t=1`, this reads `e_bQ^0h=e_bh`, as required. This completes the proof.
`\square`

## Adversarial audit

- **No circular reasoning.** The proof assumes only the Terras finite-word
  bijection and the elementary affine composite formula; it does not assume
  recurrence, convergence, or the fold theorem.
- **No finite-bound inference.** The argument is for arbitrary `k,t`. The
  existing `196/196` comparison is corroboration, not a premise.
- **No smuggled nondeterminism.** The transfer matrix counts different starting
  cylinders `m mod 2^t`. For any fixed `m`, parity still selects one path.
- **Branch semantics.** The result counts the canonical return-word/cylinder
  partition used by the code. Any theorem phrased instead in terms of
  “maximal affine pieces” must separately prove that its chosen notion of
  maximality preserves this symbolic partition under conjugacy.

