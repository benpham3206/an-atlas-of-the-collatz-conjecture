# Can Bayesian theory be applied here?

**Yes, in exactly one place: deciding what to compute next. Never in
deciding what is true.**

Audited 2026-07-25. One live defect found in the claim ledger and fixed.

---

## 1. The defect this audit found

`STATE.md` reported the P6 branch comparison as **ΔAIC = +30.0** favouring the
Tao-strength branch. Reading `decay_model_test.py`:

```python
d_aic = N * math.log(exp_fit["ssr"] / sqrt_fit["ssr"])
```

`ΔAIC` is **identically** `N·ln(SSR ratio)`. With `N = 16` and a ratio of
6.516, that is 29.99. The number carries no information the residual ratio did
not — it only *looks* like strong evidence because AIC units are read as
log-likelihood.

The likelihood is fictional. `M_n` is an exact deterministic max-reduction over
a bit-identity-gated layer. The residuals are **model misspecification, not
noise**: deterministic, serially correlated, drifting monotonically. Multiplying
by `N` inflates a fit over 16 highly dependent points whose effective sample
size is far smaller.

`STATE.md` now reports the SSR ratio (6.52× full window, 4.22× on `n ≥ 13`)
with the caveat inline. **This is precisely the failure mode the repository
exists to prevent, and it survived several sessions.** The individual packet's
"Honest scope" section was correct throughout; the defect was in the frontier
summary, one citation away from becoming a premise.

## 2. Where Bayesian reasoning is a category error

A posterior over "Collatz is true" is not a proof object. `P(true) = 0.9999`
and a counterexample at `2^80` are perfectly consistent; the truth value is not
a random variable that computation samples.

There is a theorem-grade version of this already in the repository.
`RATIONAL_IRRATIONAL_SHADOW.md` Corollary 4: **any score depending on a finite
prefix is shadowed by a rational periodic impostor with the identical score.**
`M_n` over `n ≤ 21` is a finite-prefix score. A posterior computed from
finite-prefix scores inherits the same non-discrimination — it cannot separate
the true asymptotic from its shadow. That is why Bayesian evidence can never
enter the proof, and it is not a philosophical objection but a proved one.

## 3. Why the classical probabilistic heuristic is not a proof

Per odd step, `x → 3x/2^v` with `v` geometric of mean 2, so
`E[log ratio] = log 3 − 2 log 2 < 0` — the familiar 3/4 factor. Then `log x` is
a random walk with negative drift and returns below its start almost surely.

It fails at the **quantifier**. It proves a statement of the form *for almost
every `n`* under an invented measure on starting values; the conjecture asserts
*for every `n`*. Drift arguments give measure-zero exceptional sets, and a
single integer always lives in one. Second failure: the valuations `v_i` are
not independent random variables — they are determined by `n`.

Tao's theorem is the rigorous ceiling of this method, and every analytic packet
here correctly disclaims beating it. No sharpening converts "almost all" into
"all". That quantifier gap **is** the problem.

## 4. Where it is legitimate: allocation and ordering

Two uses that survive the repository's discipline, because in both the
Bayesian layer touches only *what to spend compute on*, never what is accepted.

### 4.1 Experimental design for the next depth

`n = 22` does not fit in memory by the current method. The decision — double
streaming, out-of-core, or more points on the `Δk = 2` subsequence — is a
resource-allocation problem. Put a prior over `β` in `−ln M_n = a·n^β + b`
(rather than the binary exponential-vs-`√n` choice, which hides the real
result) and compute expected information gain about `β` per unit compute.

- **Success:** the design picks a target whose realised posterior-variance
  reduction on `β` matches prediction within a factor of 2.
- **Kill:** predicted and realised differ by more than 5×, or the ranking
  inverts under any reasonable prior change. Then the design model is
  misspecified — delete it and go back to "compute the next feasible layer".

### 4.2 Search ordering for the surviving automata

For the 10 remaining ternary-coded words and the 26 three-state DFAO words, a
posterior over which resonance template each falls into, used **only** to order
which candidate gets handed to the exact lift-digit gate first.

- **Success:** the top-ranked template yields the deciding exact argument for
  at least one of them — and the exact certificate is what closes it, not the
  ranking.
- **Kill:** after all are probed, the ranking correlates no better than random
  with which ones the exact gate resolves. Then it is overhead.

## 5. The rule

> Bayesian methods may order the queue. They may never sign the certificate.

Acceptance stays exactly where the repository already puts it: exact integer or
rational arithmetic plus an independent verifier. Nothing float64 ever becomes a
premise.

## 6. A better default than AIC, if a fit is reported at all

Report the **SSR ratio** and a **held-out prediction**: fit through `n ≤ 20`,
predict `n = 21`, state the error. Predictive error on a genuinely unseen layer
is the one number here that does not require inventing a noise model. Fitting
`β` as a free continuous parameter and reporting its spread is more honest than
any binary model comparison, because the real finding is likely "β concentrates
near 0.5 with wide mass", which the two-branch framing hides.
