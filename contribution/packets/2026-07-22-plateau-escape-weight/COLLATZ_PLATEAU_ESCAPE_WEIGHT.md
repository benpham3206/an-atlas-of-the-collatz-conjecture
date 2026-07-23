# Plateau self-similarity of the resonance chain: exact chain phases, the containment-to-rate theorem, and the proved impossibility of phase-blind propagation

**Date:** 22 July 2026
**Status:** five proved statements (P1–P5) + one proved arithmetic
dichotomy (P6) from measured constants + float64 measurements to
\(n=14\). **Not** a proof of a positive lower bound on the escape weight
\(w_n(\varepsilon)\); **not** a proof of uniform exponential decay;
**not** Collatz progress per se. What it does: (i) extracts the chain
phases in *exact integer arithmetic*; (ii) reduces uniform decay to a
single integer per layer — the length \(L(n)\) of the bad chain interval
— with an explicit rate (proved); (iii) *proves* that no "finite check
at one layer + phase-blind propagation" argument can ever establish
\(w_n(\varepsilon)\ge w>0\), locating the circularity exactly; (iv)
shows the two empirical laws in the program (stable escape weight vs
\(\exp(-1.06\sqrt n)\) decay) are asymptotically incompatible, with the
crossover computed: \(n^{*}=1776\). No counterexample candidate was
found; none was expected.

**Companion executable evidence:** `verify_plateau_escape_weight.py`,
`test_verify_plateau_escape_weight.py`,
`plateau_escape_weight_certificate.json`.

Notation follows the syracuse-fourier and scalar-phase packets:
\(\widehat c_n\), \(M_n=\max_{3\nmid\xi}|\widehat c_n(\xi)|\),
\(u_a=2^{-a}\bmod 3^{n+1}\), \(e(t)=e^{2\pi it}\), \(A_{\rm trunc}=40\).
The measured peak frequency is \(\xi^*_n\equiv s_n2^{K(n)}\bmod 3^n\),
\(s_n\in\{\pm1\}\), and the *chain profile* is
\(p_j(n)=|\widehat c_n(\xi^*_n 2^{-j})|/M_n\) (so \(p_0=1\)), with
intrinsic phases \(\psi_j(n)=\arg\widehat c_n(\xi^*_n2^{-j})\).

---

## Kill criteria (stated up front)

1. A bad frequency off the chain interval: some computed layer and
   \(\varepsilon\in\{0.05,0.1,0.2\}\) with \(B_n(\varepsilon)\not\subseteq
   \{\pm2^{K(n)-j}\}\). *Kills the containment route (P4) and redirects
   the attack.* The verifier asserts containment at every computed
   layer/\(\varepsilon\). **Survived** (\(n\le13\)).
2. The chain-exponent law breaks: \(K(n)>n+3\) or \(2^{K(n)}\ge3^n\)
   (the exact phase formula P1 loses its clean no-wrap form).
   **Survived**: \(K(n)-n\in\{0,1,2,3\}\) for \(6\le n\le14\), and
   \(2^{K(n)}<3^n\) is certified in exact integer arithmetic.
3. \(w_n(0.05)<\tfrac14-2^{-40}\) at a layer where containment holds
   (kills P4 numerically). **Survived**: measured \(w_n\) equals
   \(2^{-L}-2^{-40}\) *exactly* (the bound is tight).
4. The phase plateau breaks: circular concentration of \(\psi_j(n)\)
   drops below \(0.9\) in the window (kills the only remaining
   fixed-point route, §8).
   **Survived**: \(\psi_j\) concentrations \(0.967\)–\(0.996\)
   throughout. (The dominant-4 peak-term phases \(\theta_a\) are much
   less concentrated — \(0.876\) at \(n=9\), \(0.8995\) at \(n=10\),
   \(0.94\)–\(0.96\) later — so the criterion is scoped to \(\psi_j\);
   the \(\theta_a\) dip is recorded, not hidden.)
5. "Phase-blind propagation works." **Closed by proof** (P2, P5): this
   kill criterion can no longer fire in either direction.

## P1 — exact chain phases (proved; exact-arithmetic certificate)

**Statement.** Let \(n\ge6\) and suppose the unit peak of
\(|\widehat c_n|\) is at \(\xi^*\equiv s\,2^{K}\bmod 3^n\) with
\(2^K<3^n\) (an integer inequality, certified exactly). Then for
\(1\le a\le K\) the residue in the recursion phase is the *integer*
\(s\,2^{K-a}\) (resp. \(3^n-2^{K-a}\)) with **no modular wrap**, so

\[
\boxed{
z_a=e\!\left(-\frac{s\,2^{K-a}}{3^n}\right),\qquad
\text{and the dominant-pair scalar misalignment is exactly }
\frac{2^{K-2}}{3^n}\ \pmod 1 .
}
\tag{P1}
\]

**Proof.** \(u_a=2^{-a}\bmod 3^n\) and \(\xi^*u_a\equiv s2^{K-a}\pmod
{3^n}\); since \(0<2^{K-a}\le2^{K-1}<3^n\), the canonical residue is
the integer \(2^{K-a}\) itself. The relative circle point is
\(\{\xi^*(u_1-u_2)/3^n\}=\{s2^{K-2}/3^n\}\). \(\square\)

**Corollary (scalar alignment is exponential).** Conditional on the
measured law \(K(n)\le n+3\) (asserted in the verifier for \(n\le14\)),
the misalignment is \(\le 2^{n+1}/3^{n}=2(2/3)^n\), so Theorem S2's
scalar contraction on the chain vanishes like \((2/3)^{2n}\): **the
scalar phase can never supply the escape weight; all contraction on the
chain is intrinsic-phase.** Measured (exact Fractions in the
certificate): at \(n=14\), \(K=17\), circle points
\(2^{17-a}/3^{14}=65536/4782969,\ 32768/4782969,\dots\), misalignment
exactly \(2^{15}/3^{14}\approx0.006851\) — the bound is attained
(\(K=n+3\)).

The exact-arithmetic content (residues, Fractions, no-wrap) is
certified; *which* frequency is the peak, and the value of \(K(n)\),
are float64 measurements.

## P2 — no phase-blind supersolution (proved barrier)

**Statement.** Fix \(n\) and let \(T\) be the same-layer magnitude
transport \((Tq)(\xi)=\sum_{a=1}^{A_{\rm trunc}}2^{-a}q(\xi
2^{-a}\bmod 3^n)\) on \((\mathbb Z/3^n\mathbb Z)^*\). If \(q\ge0\)
satisfies \(Tq\le\rho q\) pointwise, then \(\rho\ge1-2^{-A_{\rm trunc}}\).

**Proof.** Multiplication by \(2^{-a}\) permutes the units, so
\(\sum_\xi(Tq)(\xi)=(\sum_a2^{-a})\sum_\xi q(\xi)
=(1-2^{-A_{\rm trunc}})\sum_\xi q(\xi)\). If \(Tq\le\rho q\) pointwise,
summing gives \((1-2^{-A_{\rm trunc}})\sum q\le\rho\sum q\). \(\square\)

So a *layer-independent* magnitude profile that transports with strict
contraction does not exist: the frequency walk is (up to the tail)
doubly stochastic, its Perron eigenvalue is \(1\) (\(1-2^{-40}\) after
truncation), and any pointwise
phase-blind domination is contraction-free. Numeric control (seeded
random \(q\), \(n=6\)): mass preserved to factor \(1-2^{-40}\) within
\(10^{-9}\), and \(\min_\xi(Tq)(\xi)/q(\xi)=0.427\le1-2^{-40}\).
This is the pointwise sharpening of packet 4's spectral barrier for the
escape-weight question.

## P3 — S3 is the \(\varepsilon\)-quantization of the triangle bound (proved)

**Statement.** For every unit \(\xi\) at layer \(n+1\), writing
\(w(\xi)=\sum_{a:\,\xi u_a\notin B_n(\varepsilon)}2^{-a}\),

\[
\boxed{
\bigl(1-\varepsilon w(\xi)\bigr)M_n
\;\ge\;
\sum_a2^{-a}\,|\widehat c_n(\xi u_a)|
\;\ge\;
|\widehat c_{n+1}(\xi)| .
}
\tag{P3}
\]

**Proof.** \(1-\varepsilon w(\xi)=\sum_{a\in B}2^{-a}
+(1-\varepsilon)\sum_{a\notin B}2^{-a}\), and \(|\widehat c_n|\le M_n\)
on \(B_n(\varepsilon)\), \(\le(1-\varepsilon)M_n\) off it. \(\square\)

Hence the escape-weight bound can **never beat the phase-blind triangle
bound at the same frequency**; the gap is the quantization loss
\(\sum_{a\notin B}2^{-a}\bigl((1-\varepsilon)-p(\xi u_a)\bigr)\).
Measured at the peak, \(n=13\), \(\varepsilon=0.05\): S3 bound
\(0.9875\), triangle bound \(0.9115\), true ratio \(0.8674\) — the
\(0.076\) quantization gap and the \(0.044\) phase gap are comparable,
and proving \(w_n\ge w\) is *exactly* controlling the quantization gap
of data the triangle bound already has. Circularity, first form.

## P4 — containment \(\Rightarrow\) explicit rate (proved reduction)

**Statement.** Let \(n\ge5\), \(1\le L\le A_{\rm trunc}\), and suppose

\[
B_n(\varepsilon)\subseteq
\{\pm2^{m-j}\bmod3^n:\ 0\le j<L\}
\qquad\text{for some } m .
\tag{containment}
\]

Then every unit \(\xi\) at layer \(n+1\) has bad-image weight
\(\beta(\xi)=\sum_{a:\,\xi u_a\in B_n(\varepsilon)}2^{-a}
\le1-2^{-L}\), hence

\[
\boxed{
w_n(\varepsilon)\ge2^{-L}-2^{-40},
\qquad
M_{n+1}\le\bigl(1-\varepsilon(2^{-L}-2^{-40})\bigr)M_n .
}
\tag{P4}
\]

**Proof.** Since \(2\) is a primitive root mod \(3^n\) with order
\(2\cdot3^{n-1}>2A_{\rm trunc}\) (\(n\ge5\)), each bad residue has at
most one preimage \(a\in[1,A_{\rm trunc}]\) under \(a\mapsto\xi2^{-a}\).
Same-sign bad \(a\)'s satisfy \(a-a'=j-j'\) as integers
(\(2\cdot3^{n-1}>2A_{\rm trunc}\)), so they form \(t+S\) for some
\(t\ge1\) and \(S\subseteq\{0,\dots,L-1\}\), of weight
\(\sum_{j\in S}2^{-(t+j)}\le\sum_{i=1}^{L}2^{-i}=1-2^{-L}\) (maximized
at \(t=1\), \(S\) full). Mixed signs would need
\(a-a'\equiv3^{n-1}+(j-j')\pmod{2\cdot3^{n-1}}\) with
\(|a-a'|\le39\) and \(|j-j'|\le L-1\), impossible since
\(3^{n-1}>39+L-1\) for \(n\ge5\). So \(\beta(\xi)\le1-2^{-L}\), and S3
concludes. \(\square\)

**Integrated form.** If containment holds at every layer with interval
length \(L(n)\), then
\(M_N\le M_{n_0}\exp\bigl(-\varepsilon\sum_{n<N}2^{-L(n)}\bigr)\).
Consequences (all proved as implications):

- \(L\) **bounded** \(\Rightarrow\) uniform exponential decay (strictly
  stronger than Tao's \(n^{-A}\) and than the measured
  \(\exp(-1.06\sqrt n)\));
- \(L(n)\le\tfrac12\log_2n+O(1)\) \(\Rightarrow\)
  \(\exp(-c\sqrt n)\)-type decay;
- \(L(n)\le\log_2n-(1+\delta)\log_2\log n\) \(\Rightarrow\)
  superpolynomial decay (Tao strength).

**The uniform-decay problem is now exactly one integer per layer.**
The weakest sufficient profile statement is *bounded bad-interval
length*; it is independent of the measured data in the strong sense
that Tao's proved \(n^{-A}\) permits \(L(n)\) as large as
\(\log_2n-\log_2\log n\), and the \(n\le14\) window determines nothing
about \(L\)'s asymptotics.

**Measured tightness.** At every computed layer the bound is *exact*:
\(\max_\xi\beta(\xi)=1-2^{-L}\) and \(w_n(\varepsilon)=2^{-L}-2^{-40}\),
attained at the chain successor \(\xi=\pm2^{m+1}\), whose first \(L\)
images are precisely the bad block. P4 cannot be improved without finer
geometry. Measured intervals (certificate, full next-layer sweeps):
\(\varepsilon=0.05\): \(L\in\{1,2\}\), \(w\in\{\tfrac12,\tfrac14\}\);
\(\varepsilon=0.1\): \(L\in\{1,2\}\); \(\varepsilon=0.2\):
\(L=2,2,3,3,3,3,3,4\) for \(n=6..13\), \(w\) falling \(\tfrac14\to
\tfrac1{16}\). **Interval creep is visible** at \(\varepsilon=0.2\);
\(L\sim\tfrac12\log_2n\) is the creep rate the measured
\(\exp(-1.06\sqrt n)\) law requires.

## P5 — phase-blind propagation of containment is impossible (proved; the exact circularity)

**Statement.** Suppose all that is known at layer \(n\) is
\(|\widehat c_n|\le M_n\) globally and
\(|\widehat c_n|\le(1-\varepsilon)M_n\) off \(B_n(\varepsilon)\). Then
for any next-layer unit \(\xi\) with bad-image weight \(\beta(\xi)\),
the best phase-blind certificate is
\(|\widehat c_{n+1}(\xi)|\le(1-\varepsilon(1-\beta(\xi)))M_n\).
Certifying \(\xi\) as non-bad at layer \(n+1\) requires
\((1-\varepsilon(1-\beta))M_n\le(1-\varepsilon)M_{n+1}\), i.e.

\[
\frac{M_{n+1}}{M_n}\ge
\frac{1-\varepsilon(1-\beta)}{1-\varepsilon}
=1+\frac{\varepsilon\beta}{1-\varepsilon}>1 ,
\tag{P5}
\]

which is impossible, since \(M_{n+1}\le M_n\) (triangle +
\(\sum_a2^{-a}=1\), proved). \(\square\)

So **no unit is ever certifiably non-bad at the next layer without phase
information**, at any layer where \(M\) strictly decreases — the
induction behind "finite check at \(n_0\) + propagation lemma" has no
phase-blind closure, and by P2 no phase-blind plateau supersolution
exists either. The measured margin by which the phase-blind certificate
misses the next-layer threshold is \(0.16\)–\(0.34\,M_n\) at the worst
unit (the chain successor; certificate `t5_propagation_gap_over_M`) —
and the only thing that closes it is phase cancellation on the bad
images, *the same cancellation that determines \(M_{n+1}/M_n\) itself*.
This is the circularity, precisely: a lower bound on \(w_n(\varepsilon)\)
is not a weaker statement than the decay it would prove; it is the same
statement one layer earlier, \(\varepsilon\)-quantized (P3), and any
propagation of it must input the intrinsic phases at every layer.

## P6 — the two empirical laws are asymptotically incompatible (proved arithmetic from measured constants)

Measured (packet 3 / packet 5, float64): \(M_n\sim e^{-1.06\sqrt n}\).
Measured here (full sweeps, \(n\le13\)):
\(w_n(0.05)\in\{\tfrac14-2^{-40},\tfrac12-2^{-40}\}\), never below
\(\tfrac14-2^{-40}\). If \(w_n(0.05)\ge\tfrac14\) for all \(n\ge n_0\),
then P4+S3 give \(M_n\le M_{n_0}(79/80)^{n-n_0}\), which eventually
lies strictly below any constant multiple of \(e^{-1.06\sqrt n}\). The
per-layer decay rate of the measured law, \(e^{-1.06/(2\sqrt n)}\),
first falls below \(79/80\) at

\[
n^{*}=\left\lceil\Bigl(\frac{1.06}{-2\ln(79/80)}\Bigr)^{2}\right\rceil
=\lceil 1775.31\ldots\rceil=1776 .
\tag{P6}
\]

(This is where the ratio of the two laws is minimized; the level
crossing itself is constant-dependent — with unit constants it occurs
near \(n\approx7102\). The asymptotic incompatibility is unaffected.)

So exactly one of the following holds (both resolutions visible in the
data): **(i)** the plateau is exactly stable (\(L\) bounded) and the
\(\sqrt n\)-law breaks to true exponential decay; **(ii)** the bad
interval creeps, \(L(n)\to\infty\) like \(\tfrac12\log_2n\), and
\(w_n(0.05)\to0\) like \(c/\sqrt n\). The window data favors (ii):
\(L\) creep at \(\varepsilon=0.2\) (\(2\to4\) over \(n=6..13\)) and an
upward drift of the near-peak profile (\(p_1,p_2,p_3\) slopes
\(+0.011,+0.024,+0.019\) per layer) — drift *toward* flatness. Under
(ii), \(w_n(0.05)\) has a *windowed* positive liminf (\(\tfrac14\)) but
a vanishing asymptotic one; a \(c/\sqrt n\) law for \(w_n(0.05)\) is
quantization-invisible in the window (the first drop below \(1/4\)
requires \(L\ge3\) at \(\varepsilon=0.05\), i.e. \(p_2>0.95\); linear
extrapolation of the drift puts that near \(n\approx22\) — a falsifiable
float64 prediction, not a theorem).

## Measurements supporting the above (float64, \(n\le14\))

**(a) Profile table and plateau.** \(p_j(n)\), \(j=0..8\), \(n=8..14\)
(certificate `profile_table`):

| \(j\) | range | mean | slope/layer |
|---|---|---|---|
| 1 | 0.846–0.987 | 0.921 | +0.0114 |
| 2 | 0.619–0.838 | 0.728 | +0.0238 |
| 3 | 0.446–0.632 | 0.531 | +0.0186 |
| 4 | 0.308–0.437 | 0.367 | +0.0102 |
| 5 | 0.194–0.288 | 0.240 | +0.0069 |
| 6–8 | 0.073–0.192 | — | \(0\) to \(+0.006\) |

Approximate plateau (max deviation \(\le0.11\)) with slow upward drift
at small \(j\). \(\Delta K(n)=K(n{+}1)-K(n)\in\{1,2\}\); no sign flips.

**(b) Phase plateau.** \(\psi_j(n)\) circular concentration
\(0.967\)–\(0.996\) per \(j\); the means
\((-0.49,-0.10,0.20,0.41,0.52,0.46,0.12,-0.39,-0.61)\) rad form a
stable rotating pattern. Total peak term phases
\(\theta_a=\arg(z_a\widehat c_{n-1}(\cdot))\): spread \(54^\circ\)–\(77^\circ\)
over \(a=1..4\), dominant-pair gap \(23^\circ\)–\(31^\circ\), stable in
\(n\); dominant-\(4\) concentration \(0.876\)–\(0.938\). The intrinsic
phase pattern — not the scalar phase (P1) — is what contracts the peak
(phase factor \(0.90\)–\(0.95\) per layer, measured).

**(c) Escape weights.** \(w_n(\varepsilon)=2^{-L(n,\varepsilon)}-2^{-40}\)
exactly at every computed layer (S3-faithful: min over *next-layer*
units, full sweeps \(n\le13\)); \(w_n(0.05)\) for \(n=6..13\):
\((\tfrac12,\tfrac12,\tfrac12,\tfrac12,\tfrac14,\tfrac12,\tfrac12,
\tfrac14)\); correlation of the windowed \(w_n(0.05)\) with \(1/\sqrt n\)
is \(0.48\) (meaningless: the values are dyadic-quantized). Typical
(off-chain) units escape with weight \(\ge0.99\) (packet 5); the entire
uniform problem is the chain and its immediate successor.

## Flatness, honestly (sharpening packet 5's kill criterion 3)

Flatness \(p_j(n)\to1\) for every fixed \(j\) is equivalent to
\(L(n)\to\infty\), hence to \(w_n(\varepsilon)\to0\) for every
\(\varepsilon\) — S3 becomes vacuous and **nothing** follows about the
decay rate in either direction (S3 is one-sided). Packet 5's assertion
that flatness would contradict Tao's \(n^{-A}\) therefore needs an extra
hypothesis: flatness *plus* phase alignment at rate \(o(1/n)\) on the
mass-\((1-o(1))\) support would give \(M_{n+1}/M_n=1-o(1/n)\), i.e.
\(M_n\ge n^{-o(1)}\), contradicting the uniform \(n^{-A}\) decay cited
there. Flatness alone is consistent with every rate from \(n^{-A}\) to
no decay. The measured drift is *toward* slow flatness (upward \(p_j\)
slopes, \(L\)-creep) but the phase pattern shows no alignment trend —
the window sits in resolution (ii) of P6.

## What is proved vs what remains

- **Proved:** P1 (exact phases, given peak location), P2 (no
  phase-blind supersolution), P3 (quantization gap), P4
  (containment\(\Rightarrow\)rate, tight), P5 (no phase-blind
  propagation), P6 (dichotomy arithmetic). \(M_n\) non-increasing.
- **Not proved:** any lower bound on \(w_n(\varepsilon)\) uniform in
  \(n\); any bound on \(L(n)\) beyond \(n\le13\); the propagation of
  containment. By P5+P2 the missing input is exactly the intrinsic
  phase pattern on the chain at every layer — i.e. Tao's §7 renewal
  geometry in profile form. The only route left visible is a
  phase-sensitive fixed-point induction on the pair \((p,\psi)\) (both
  measured to plateau, with summable memory \(2^{-a}\) making a
  finite-dimensional truncation legitimate for the peak equation); even
  if closed, it yields "only" uniform exponential decay of \(M_n\).
  Confidence that this route closes: low — the off-chain containment
  part is infinite-dimensional and the peak margin is the P3 gap
  itself. Confidence in the proved reductions: high.
- **Counterexample candidates:** none found; none expected.

## Related work

The chain profile and its self-consistency are the profile form of
Tao's Proposition 1.17 (arXiv:1909.03562, §7 two-dimensional renewal);
P2 is the pointwise shadow of packet 4's spectral barrier
(\(|\mu_1|=1-\Theta(9^{-n})\)); P4–P5 continue packet 5's S3
escape-weight criterion. The reduction of uniform decay to a bounded
bad-interval length, and the impossibility of phase-blind propagation,
do not appear in Tao or in Siegel's non-Archimedean spectral treatment
(arXiv:2412.02902). The same \(2\)–\(3\) resonance lattice drives the
cycle-equation literature (Eliahou 1993; Simons–de Weger 2005) and the
drift wall of packet 1; here it reappears as the exact rational phases
\(2^{K-a}/3^n\) of P1.

## Reproduce

```bash
python3 contribution/packets/2026-07-22-plateau-escape-weight/verify_plateau_escape_weight.py
python3 -m pytest contribution/packets/2026-07-22-plateau-escape-weight/ -q
```

Env knobs: `VEW_N_MAX` (default 14; tests use 8), `VEW_SAMPLE`
(default 200000; only used if \(3^{n+1}>5\times10^6\)). Certificate:
`plateau_escape_weight_certificate.json`; saved stdout:
`verify_plateau_escape_weight.out`.
