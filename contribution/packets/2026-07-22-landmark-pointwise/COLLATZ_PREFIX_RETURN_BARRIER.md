# Prefix-return barrier for positive Collatz parity transcripts

Let

\[
T(n)=\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd},
\end{cases}
\]

let \(x_j=T^j(n)\), and let \(q_j=x_j\bmod 2\). For \(L\ge1\), define the
first return time of the length-\(L\) prefix, when it exists, by

\[
\tau_q(L)=\min\{j\ge1:q_jq_{j+1}\cdots q_{j+L-1}=q_0q_1\cdots q_{L-1}\}.
\]

## Theorem

Assume that the parity word \(q\) is not eventually periodic. If \(2^L>n\)
and \(\tau_q(L)\) exists, then

\[
\boxed{
\tau_q(L)>
\frac{L\log 2-\log(n+1)}{\log(3/2)}.
}
\]

Consequently, along every unbounded sequence of prefix lengths for which the
prefix recurs,

\[
\boxed{
\liminf\frac{\tau_q(L)}L
\ge
\frac{\log2}{\log(3/2)}
=1.70951129135\ldots .
}
\]

## Proof

The universal one-step estimate is

\[
T(x)+1\le\frac32(x+1),
\]

and hence

\[
x_j+1\le(n+1)(3/2)^j.
\]

If the length-\(L\) prefix recurs at shift \(j\), the Terras parity-vector
bijection gives

\[
x_j\equiv n\pmod {2^L}.
\]

Suppose instead that

\[
j\le\frac{L\log2-\log(n+1)}{\log(3/2)}.
\]

Then \(x_j+1\le2^L\), so \(0\le x_j<2^L\). The hypothesis \(n<2^L\)
and the congruence imply \(x_j=n\). Determinism makes the orbit, and therefore
its parity word, eventually periodic, contrary to the hypothesis. This proves
the strict inequality. Dividing by \(L\) gives the asymptotic statement.
\(\square\)

## Interpretation

A positive Collatz transcript cannot combine aperiodicity with very rapid exact
recurrence. The obstruction constant \(1.7095\ldots\) is larger than the golden
ratio \(1.6180\ldots\). Golden/Fibonacci recurrence is therefore a useful
adversarial model: its repetitions are too efficient to coexist with the
power-of-two congruence separation required by a nonperiodic positive orbit.
The stronger factor-complexity theorem in the main research memo excludes all
Sturmian transcripts directly.
