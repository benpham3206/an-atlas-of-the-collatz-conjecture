# Simple questions with exact answers

Small questions, asked deliberately below the frontier. Each one has a
complete answer in a few lines, and each connects to a machine that is
load-bearing elsewhere. The point is not that they are hard. The point is that
answering them exposes which structure is actually doing the work.

Every answer here is exact integer arithmetic and independently checkable.

---

## Q1. Why does it cycle back to 4 → 2 → 1?

Because `4 − 3 = 1`. That is the whole reason, and it is the tightest
possible near-miss between a power of 2 and a power of 3.

**Exactly.** Work in the odd-only map. A cycle with `m` odd members, total
2-adic valuation `K`, has its state fixed by

```
n = C_m / (2^K − 3^m),     C_0 = 0,  C_{j+1} = 3C_j + 2^{S_j}
```

Take `m = 1`. Then `C_1 = 3·0 + 2^0 = 1`, so

```
n = 1 / (2^K − 3).
```

For `n` to be a positive integer, `2^K − 3` must be a positive divisor of 1 —
so `2^K − 3 = 1`, giving `K = 2` and `n = 1`. Nothing else is possible.

And `K = 2` is exactly the observed orbit: `3·1 + 1 = 4 = 2²`, two halvings
back to 1. **The 4-2-1 cycle exists because `3 + 1` happens to be a power of
two, and it is the only one-odd-member cycle for that reason alone.**

**Why this is not a curiosity.** The same equation with `m` large is the
entire cycle branch. A nontrivial cycle needs `2^K − 3^m` to be *small
relative to `C_m`* — i.e. `2^K ≈ 3^m`, a near-resonance. The trivial cycle is
the `m = 1` instance of the resonance condition that governs Hercher's bound,
the contraction-onset bound, and the whole 2–3 resonance lattice. The
smallest question in the subject and the largest one are the same equation.

## Q2. Why is there no cycle with exactly two odd members?

Because the window is empty — no power of two lives in it.

Every cycle state is at least 7 (Q3), which forces
`3^m < 2^K ≤ (22/7)^m`. At `m = 2` that reads

```
9 < 2^K ≤ 9.8775…
```

and there is no power of 2 in that interval. Done — no arithmetic on `C_m`
required. Most small `m` die this way, which is why the exhaustive search only
has to examine a handful of `(m, K)` pairs.

## Q3. Why must every cycle state be at least 7?

Because 1, 3 and 5 all reach 1, so none of them can sit on a nontrivial cycle:

```
odd-only orbit of 1:  1 → 1
odd-only orbit of 3:  3 → 5 → 1
odd-only orbit of 5:  5 → 1
```

A nontrivial cycle contains no state that reaches 1, so its least member is
≥ 7. That single fact supplies the `(22/7)^m` upper bound in Q2, since each
step multiplies by `3 + 1/n_i ≤ 3 + 1/7`.

## Q4. What is special about 3? Would 5 do?

No — and the failure is sharp and computable.

For the family `T_A(x) = (Ax+1)/2` on odd `x`, the factor-complexity threshold
that excludes low-complexity transcripts is `κ_A = 1/log₂(A/2)`:

| `A` | `κ_A` | consequence |
|---:|---|---|
| 3 | **1.7095…** | exceeds 1, so it excludes every Sturmian word (`p(k) = k+1`) |
| 5 | 0.7565… | below 1 — **vacuous**, weaker than the Morse–Hedlund bound every aperiodic word already satisfies |
| 7 | 0.5533… | vacuous |

So `A = 3` is the unique odd multiplier greater than 1 on the useful side of
the threshold, and it is useful because `3 < 4`. The moment `A > 4` the whole
complexity machinery says nothing. That is a genuine structural feature of the
coefficient, not numerology — and it is why "generalize to `An+B`" is a
stress test, never a shortcut.

## Q5. Why can't a simple energy function work?

Because Mersenne numbers rise too fast for any bounded correction to absorb.

Suppose `V(n) = log(n+1) + h(n)` with `h` bounded, and suppose `V` never
increases. Take `n = 2^p − 1`. Then `T^j(n) = 3^j·2^{p−j} − 1` for
`0 ≤ j ≤ p`, so over the first `p` steps `log(n+1)` increases by exactly
`p·log(3/2)` — unbounded in `p` — while `h` moves by at most a constant.

So no such `V` exists. Any Lyapunov-style potential must either be unbounded
near the 2-adic point `−1` (whose parity word is `111…`, which Mersenne
numbers approximate) or use variable-length returns instead of single steps.

---

## Asked but not yet answered

- Why is the *first* contraction always the *first* descent, for every odd
  `x > 1`? Verified to 1.45 × 10⁹; no proof, and probably not provable by the
  elementary route (see `TARGETS.md` §6).
- Is there a smallest `m` for which the cycle window `3^m < 2^K ≤ (22/7)^m`
  contains **two** powers of 2? What happens there?
- What is the smallest starting value whose orbit exceeds every earlier
  record? (The record-setter sequence — is it in OEIS, and does its structure
  say anything about near-resonance?)

Add to this list freely. The bar is that the answer must be exact and short.
If a question needs a packet, it is not a simple question — put it in
`TARGETS.md`.
