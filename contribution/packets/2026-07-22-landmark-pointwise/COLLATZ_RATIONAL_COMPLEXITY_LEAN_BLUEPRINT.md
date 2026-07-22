# Lean blueprint: rational-lift complexity obstruction

This is a formalization plan, not compiled Lean code.

## Main mathematical statement

Let `q : Nat -> Fin 2` be the parity transcript of a rational 2-adic state
`a / d`, with `d` positive and odd. If `q` is not eventually periodic, then

```text
limsup_k factorComplexity(q,k) / k >= 1 / log_2(3/2).
```

Consequently, no Sturmian word is the parity transcript of a rational 2-adic
state under the Terras map.

## Recommended integer-scaled definitions

Avoid rational arithmetic in the orbit. Fix `a : Int` and positive odd
`d : Nat`, and define

```lean
def TerrasScaled (d : Nat) (y : Int) : Int :=
  if Even y then y / 2 else (3*y + d) / 2

def scaledOrbit (d : Nat) (a : Int) : Nat -> Int
| 0 => a
| n+1 => TerrasScaled d (scaledOrbit d a n)

def parity (d : Nat) (a : Int) (n : Nat) : Fin 2 :=
  Int.emod (scaledOrbit d a n) 2
```

Prove that oddness of `d` makes this parity equal to the 2-adic parity of
`scaledOrbit / d`.

## Core lemmas

1. `scaled_affine_block`

For a length-`k` parity block with `s` ones, prove an integer identity

```text
2^k * y_{i+k} = 3^s * y_i + d * c(block)
```

for an explicitly recursive natural/integer `c`.

2. `same_block_congruent`

If two length-`k` blocks agree, then

```text
y_i = y_j (mod 2^k).
```

3. `scaled_growth`

```text
abs(y_{n+1}) + d <= (3/2) * (abs(y_n) + d)
```

Use a denominator-cleared form:

```text
2 * (abs(y_{n+1}) + d) <= 3 * (abs(y_n) + d).
```

Induct to obtain

```text
2^n * (abs(y_n) + d) <= 3^n * (abs(a) + d).
```

4. `height_block_injective`

If all `|y_i| <= H` for `i <= N` and `2^k > 2*H`, then the first `N+1`
length-`k` blocks are pairwise distinct unless the orbit is eventually
periodic.

5. `complexity_lower_sequence`

Choose an integer `k_N` satisfying

```text
2^k_N > 2 * (abs(a)+d) * (3/2)^N.
```

Then `factorComplexity q k_N >= N+1` and `k_N / N -> log_2(3/2)`.

## Sturmian interface

Only two properties are needed:

```lean
structure SturmianData (q : Nat -> Fin 2) where
  not_eventually_periodic : Not (EventuallyPeriodic q)
  complexity : forall k, factorComplexity q k = k + 1
```

No balance or slope theorem is required for the rationality obstruction.

## Headline theorem

```lean
theorem sturmian_not_rational_terras_parity
  (q : Nat -> Fin 2)
  (hs : SturmianData q)
  (a : Int) (d : Nat)
  (hdpos : 0 < d) (hdodd : Odd d)
  (hq : q = parityTranscriptOfRational a d) : False := by
  -- obtain p(k_N) >= N+1
  -- rewrite p(k_N) = k_N+1
  -- use k_N/N -> log_2(3/2) < 1
  ...
```

## Audit points

- Work over `Int`; negative rational states are included.
- Use `2^k > 2H`, not merely `2^k > H`, because states may have opposite signs.
- Equality of two scaled states implies eventual periodicity by determinism.
- The theorem concerns rational 2-adic states, i.e. odd denominator.
- No probabilistic statement or unproved Collatz claim is needed.
