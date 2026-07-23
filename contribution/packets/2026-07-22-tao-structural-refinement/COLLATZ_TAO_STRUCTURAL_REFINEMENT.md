# A structural refinement of Tao's exceptional set, and the honest route map beyond it

**Date:** 22 July 2026
**Status:** assessment + one combination theorem + numerical evidence.
**Not** a proof of Collatz, **not** a counterexample, **not** a
re-proof of Tao's theorem, and **not** a stronger density statement than
Tao's. The strengthening offered here is in the *description* of the
exceptional set, not its size.
Source: T. Tao, *Almost all orbits of the Collatz map attain almost
bounded values*, arXiv:1909.03562 **v7 (16 Jul 2026)**, read in full.

**Companion executable evidence:** `verify_syracuse_mixing.py`,
`test_verify_syracuse_mixing.py`, `syracuse_mixing_certificate.json`.

---

## 1. What Tao proved, exactly

**Theorem 1.3 (Tao).** For any \(f:\mathbb N_{+1}\to\mathbb R\) with
\(f(N)\to+\infty\), \(\mathrm{Col}_{\min}(N)<f(N)\) for almost all
\(N\) — in the sense of **logarithmic density**.

Proof skeleton (his numbering):

- Syracuse reformulation (Theorem 1.6): odd iterates only,
  \(\mathrm{Syr}^n(N)=3^n2^{-|\vec a^{(n)}(N)|}N+F_n(\vec a^{(n)}(N))\).
- **Proposition 1.9** (valuation heuristic justified):
  \(\vec a^{(n)}(N)\approx\mathrm{Geom}(2)^n\) in total variation,
  error \(\ll 2^{-c_1 n}\), for \(N\) uniform enough mod \(2^{n'}\).
- **Proposition 1.11** (stabilisation of first passage): the hard
  engine; (1.19) easy, (1.20) the difficult estimate
  \(d_{TV}(\mathrm{Pass}_x(\mathcal N_{x^\alpha}),
  \mathrm{Pass}_x(\mathcal N_{x^{\alpha^2}}))\ll\log^{-c}x\).
- **Proposition 1.14** (fine-scale mixing of offsets):
  \(\mathrm{Osc}_{m,n}\) of \(\mathrm{Syrac}(\mathbb Z/3^n\mathbb Z)\)
  is \(\ll_A m^{-A}\) for all \(A\).
- **Proposition 1.17** (the deepest step, §7): superpolynomial decay
  of the characteristic function
  \(\mathbb E\,e^{-2\pi i\xi\,\mathrm{Syrac}(\mathbb Z/3^n\mathbb Z)/3^n}
  \ll_A n^{-A}\) for \(3\nmid\xi\), via a two-dimensional renewal
  process avoiding triangles.

## 2. Where "all" degrades to "almost all" (his own markers)

1. **Remark 1.4 — the constant barrier.** Getting
   \(\mathrm{Col}_{\min}(N)\le C_0\) for almost all \(N\) is "likely to
   be almost as hard as the full Collatz conjecture": one orbit that
   never drops below \(C_0\) should, by his heuristics, *infect* a
   positive-density set of starting values. This is precisely the
   atlas's attack item 1 (parser-density amplification), and it remains
   a heuristic — proving infection is the missing bridge.
2. **Logarithmic vs natural density.** Forced by the
   \(\exp(O(\sqrt n))\) random-walk fluctuations (his (1.17)). He notes
   the upgrade to natural density is plausible but needs fine-scale
   mixing of the whole affine map \(\mathrm{Aff}_{\mathrm{Geom}(2)^n}\),
   not just the offset (Remark 1.16).
3. **Superpolynomial, not exponential, mixing.** The random-map
   heuristic predicts \(\exp(-cm)\) decay in Proposition 1.14/1.17; the
   paper proves only \(m^{-A}\) (Remark 1.15). He remarks (1.20) may be
   improvable to \(x^{-c}\).
4. **Effectivity.** \(C_\delta\ll\exp(\delta^{-O(1)})\); Ben Green's
   footnote observes an explicit version + numerics could give Collatz
   on a positive-log-density set.

## 3. Theorem A — the exceptional set is density-zero AND symbolically rigid

Fix \(f(N)\to\infty\) and let
\(E_f=\{N\in\mathbb N_{+1}:\mathrm{Col}_{\min}(N)\ge f(N)\}\) be Tao's
exceptional set. Then:

**(i) (Tao)** \(E_f\) has logarithmic density \(0\).

**(ii) (this packet, pointwise)** every \(N\in E_f\) has a Terras
parity word \(q\) of exactly one of two rigid types:

- **Type P (eventually periodic).** The orbit is eventually periodic;
  its cycle has \(a\) odd members in period length \(L\) with
  \(a/L<\log_3 2\) (strictly, from positivity of the cycle equation),
  \(a>18\) (atlas exact-search box), and indeed
  \(a>1.375\times10^{11}\) (Hercher–Bařina).
- **Type D (aperiodic).** The orbit diverges and \(q\) satisfies, with
  \(\alpha=\log_3 2\), \(\kappa=1/\log_2(3/2)\):
  \[
  \liminf_L\frac{s_L}L\ge\alpha,
  \qquad
  \limsup_k\frac{p_q(k)}k\ge\kappa,
  \]
  and, if its critical block discrepancy is bounded, full binary factor
  entropy. In particular Type D words pass **every** symbolic screen in
  the atlas; \(q^{*}=\varphi(C_3)\) of the structure-randomness packet
  is an explicit member of this class.

**Proof.** If \(N\in E_f\), its orbit never reaches \(1\), hence is
eventually periodic (Type P) or divergent. Type P: the cycle-analysis of
`COLLATZ_POINTWISE_DRIFT_WALL.md` §5. Type D: the drift wall (same
packet, Theorem 1) and the complexity wall (landmark memo, Corollaries 4
and 6). \(\square\)

This is the structure–randomness *inverse theorem* form of Tao's
result: **defiance of the almost-bounded behaviour forces rigid symbolic
structure**, and each type has its own kill program — finite certified
cycle search for Type P, lift-digit arithmetic for Type D. Tao bounds
the *size* of \(E_f\); this bounds its *shape*. The two are
complementary, and the combination is strictly sharper than either.

**Honest weighting:** (ii) is a restating of already-proved walls into
Tao's language. Its value is the combination and the explicitness of
the two types, not new hard analysis.

## 4. Observation B — Tao's deepest proposition is a Bernoulli-convolution problem

The Syracuse random variable is (his Remark 1.13)
\[
\mathrm{Syrac}(\mathbb Z_3)\equiv\sum_{j\ge0}3^j\,2^{-a[1,j+1]},
\qquad a_i\ \text{iid}\ \mathrm{Geom}(2),
\]
the stationary measure of the Markov chain \(x\mapsto(3x+1)/2^a\)
with transition probability \(2^{-a}\) on \(\mathbb Z_3\). This is a
**3-adic self-affine random series — a Bernoulli-convolution-type
object**. Proposition 1.17 is a Fourier-decay statement about it, and
the conjectured \(\exp(-cm)\) strengthening (his Remark 1.15) is exactly
the kind of question that is famously hard for classical Bernoulli
convolutions (Erdős–Kahane–Solomyak–Hochman–Varjú). Reframing:
**the analytic heart of Tao's paper is the Fourier decay of one
explicit self-affine 3-adic measure**, and upgrading Tao likely equals
upgrading that decay.

**Numerical window (hypothesis generator only).** The verifier computes
the exact distributions of \(\mathrm{Syrac}(\mathbb Z/3^n\mathbb Z)\) via
his Lemma 1.12 (cross-checked against the paper's own tabulated \(n=1,2\)
vectors, and float-vs-exact to \(10^{-9}\) at \(n\le5\)), then measures,
in float64 up to \(n=14\):

- **Maximal characteristic magnitude**
  \(M_n=\max_{3\nmid\xi}|\mathbb E\,e^{-2\pi i\xi\mathrm{Syrac}/3^n}|\):
  \((0.577, 0.378, 0.252, \ldots, 0.0191)\) at \(n=1,\ldots,14\), with
  \(-\ln M_n/\sqrt n\) stabilising at \(\approx 1.06\) for \(n\ge9\)
  while \(-\ln M_n/n\) steadily decreases and \(-\ln M_n/\ln n\) steadily
  grows. The data is therefore consistent with **stretched-exponential
  decay \(M_n\approx e^{-c\sqrt n}\)** (\(c\approx1.06\)) — faster than
  the proved superpolynomial bound for large \(n\), slower than the
  conjectured \(\exp(-cm)\). The worst frequencies are near powers of
  \(2\) (e.g. \(\xi=2^{17}\) at \(n=14\)) — the \(2\)-adic/\(3\)-adic
  resonance surfacing as the obstruction to mixing.
- **Oscillations** \(\mathrm{Osc}_{m,n}\): at fixed \(m\) they grow
  toward limits below \(1\) as \(n\to\infty\); at fixed \(n\) they decay
  in \(m\) (e.g. \(n=14\): \(0.72, 0.56, 0.44, 0.35, 0.26\) at
  \(m=2,4,6,8,10\), \(\sim m^{-0.6}\) in this range), consistent with
  Proposition 1.14's uniform-in-\(n\) bound \(\ll_A m^{-A}\).

See the certificate JSON for the full tables. These measurements are a
hypothesis generator, not a proof; the exact-verified content stops at
the recursion, the paper vectors, and the \(n\le5\) cross-check.

## 5. The route map beyond Tao, ranked by honesty

| route | statement | status | blocker |
|---|---|---|---|
| R1 | natural density instead of log density | plausible per Remark 1.16 | mixing of full affine map, not just offset |
| R2 | \(\exp(-cm)\) Fourier decay (Prop 1.17) | heuristic-supported; Bernoulli-convolution-hard | 70 years of BC literature |
| R3 | one bad orbit ⇒ positive-density infection (kills Collatz via Theorem 1.3) | **the real prize** | proving infection = the same wall as attack item 1; currently heuristic |
| R4 | effective \(C_\delta\) (currently \(\exp(\delta^{-O(1)})\)) | incremental | effective Proposition 1.17 |
| R5 | Theorem A above: rigidity of exceptions | **done here** | — |

R3 is the strategically important one: Theorem 1.3's density-zero
conclusion is *incompatible* with a positive-density infection set, so a
rigorous infection theorem would end the conjecture. Tao's machinery
(Proposition 1.11 stabilisation) is precisely the kind of tool that
could prove infection — the first passage map \(\mathrm{Pass}_x\) is
approximately transport-invariant — but applying it to the *wake* of a
hypothetical bad orbit requires controlling \(\mathrm{Pass}_x\) at
\(x\) comparable to orbit elements, where the current estimates lose
pointwise control (total-variation errors, again).

## 6. Kill criteria and exact boundary

- Theorem A dies if an exception is exhibited outside Types P/D (that
  would refute the drift or complexity walls — i.e., would itself be
  major).
- Observation B is a reframing, not a theorem; the numerical decay
  table is openly heuristic (float64 beyond \(n=5\), exact Fraction
  cross-check at \(n\le5\) against the paper's tabulated vectors).
- Nothing here re-proves Tao's theorem, strengthens his density
  statement, or touches the all-\(N\) question.

## 7. Reproduce

```bash
python3 contribution/packets/2026-07-22-tao-structural-refinement/verify_syracuse_mixing.py
python3 -m pytest contribution/packets/2026-07-22-tao-structural-refinement/ -q
```

Certificate: `syracuse_mixing_certificate.json`.
