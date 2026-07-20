# F2 Report — Induced First-Return Maps + Collapse Search

## Budgets

- k = 1..5 (attempted up to 5)
- s ≤ k + 22 per class
- node budget = 3,000,000 per class
- global runtime cap = 20 minutes
- collapse mass threshold = 2^{-10} = 1/1024

**Note:** Completed full search for k=1..5.

**Total runtime:** 644.440 s

## Per-k statistics

| k | classes | mean branches | max branches | min branches | classes w/ unres | max unres mass | min resolved mass | time (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 23.00 | 23 | 23 | 2 | 1/2^23 | 8388607/2^23 | 0.000 |
| 2 | 4 | 23322.00 | 46368 | 276 | 4 | 75025/2^24 | 16702191/2^24 | 1.362 |
| 3 | 8 | 250384.50 | 367684 | 196392 | 8 | 1414547/2^24 | 15362669/2^24 | 55.349 |
| 4 | 16 | 200826.56 | 241062 | 108657 | 16 | 520947/2^21 | 1576205/2^21 | 186.597 |
| 5 | 32 | 97299.81 | 108652 | 51079 | 32 | 2255007/2^22 | 1939297/2^22 | 386.582 |

## Branch-count vs k (growth curve)

| k | mean | max | max/mean |
|---:|---:|---:|---:|
| 1 | 23.00 | 23 | 1.00 |
| 2 | 23322.00 | 46368 | 1.99 |
| 3 | 250384.50 | 367684 | 1.47 |
| 4 | 200826.56 | 241062 | 1.20 |
| 5 | 97299.81 | 108652 | 1.12 |

Per-class branch counts:

- k=1: [23, 23]
- k=2: [46368, 276, 276, 46368]
- k=3: [241070, 367684, 367684, 196392, 196392, 196392, 196392, 241070]
- k=4: [108658, 175195, 175195, 241060, 199859, 241061, 199859, 241061, 241062, 199859, 199859, 199859, 241060, 199860, 241061, 108657]
- k=5: [51079, 78162, 78162, 108649, 108650, 100222, 100223, 100222, 100222, 100223, 100222, 108652, 100223, 93554, 100223, 108650, 108650, 108650, 108651, 100222, 87429, 108651, 93557, 108651, 108651, 93558, 93555, 87428, 108651, 100223, 108650, 51079]

## Unresolved mass

- Global max class unresolved mass: 2255007/2^22
- Global min resolved mass: 1939297/2^22

Classes with positive unresolved mass:

- (1,0): mass=1/2^23, leaves=1, branches=23, nodes=47, truncated=False
- (1,1): mass=1/2^23, leaves=1, branches=23, nodes=47, truncated=False
- (2,0): mass=75025/2^24, leaves=75025, branches=46368, nodes=242785, truncated=False
- (2,1): mass=25/2^24, leaves=25, branches=276, nodes=601, truncated=False
- (2,2): mass=25/2^24, leaves=25, branches=276, nodes=601, truncated=False
- (2,3): mass=75025/2^24, leaves=75025, branches=46368, nodes=242785, truncated=False
- (3,0): mass=1414547/2^24, leaves=2517861, branches=241070, nodes=3000000, truncated=True
- (3,1): mass=312627/2^23, leaves=1250508, branches=367684, nodes=3000000, truncated=True
- (3,2): mass=312627/2^23, leaves=1250508, branches=367684, nodes=3000000, truncated=True
- (3,3): mass=158905/2^24, leaves=317810, branches=196392, nodes=1028403, truncated=False
- (3,4): mass=158905/2^24, leaves=317810, branches=196392, nodes=1028403, truncated=False
- (3,5): mass=158905/2^24, leaves=317810, branches=196392, nodes=1028403, truncated=False
- (3,6): mass=158905/2^24, leaves=317810, branches=196392, nodes=1028403, truncated=False
- (3,7): mass=1414547/2^24, leaves=2517861, branches=241070, nodes=3000000, truncated=True
- (4,0): mass=2083787/2^23, leaves=2782685, branches=108658, nodes=3000000, truncated=True
- (4,1): mass=1015863/2^22, leaves=2649611, branches=175195, nodes=3000000, truncated=True
- (4,2): mass=1015863/2^22, leaves=2649611, branches=175195, nodes=3000000, truncated=True
- (4,3): mass=1731575/2^23, leaves=2517881, branches=241060, nodes=3000000, truncated=True
- (4,4): mass=477431/2^21, leaves=2600283, branches=199859, nodes=3000000, truncated=True
- (4,5): mass=865787/2^22, leaves=2517879, branches=241061, nodes=3000000, truncated=True
- (4,6): mass=477431/2^21, leaves=2600283, branches=199859, nodes=3000000, truncated=True
- (4,7): mass=865787/2^22, leaves=2517879, branches=241061, nodes=3000000, truncated=True
- (4,8): mass=1731573/2^23, leaves=2517877, branches=241062, nodes=3000000, truncated=True
- (4,9): mass=477431/2^21, leaves=2600283, branches=199859, nodes=3000000, truncated=True
- (4,10): mass=477431/2^21, leaves=2600283, branches=199859, nodes=3000000, truncated=True
- (4,11): mass=477431/2^21, leaves=2600283, branches=199859, nodes=3000000, truncated=True
- (4,12): mass=1731575/2^23, leaves=2517881, branches=241060, nodes=3000000, truncated=True
- (4,13): mass=1909723/2^23, leaves=2600281, branches=199860, nodes=3000000, truncated=True
- (4,14): mass=865787/2^22, leaves=2517879, branches=241061, nodes=3000000, truncated=True
- (4,15): mass=520947/2^21, leaves=2782687, branches=108657, nodes=3000000, truncated=True
- (5,0): mass=774893/2^21, leaves=2897843, branches=51079, nodes=3000000, truncated=True
- (5,1): mass=245563/2^19, leaves=2843677, branches=78162, nodes=3000000, truncated=True
- (5,2): mass=245563/2^19, leaves=2843677, branches=78162, nodes=3000000, truncated=True
- (5,3): mass=2255007/2^22, leaves=2782703, branches=108649, nodes=3000000, truncated=True
- (5,4): mass=1127503/2^21, leaves=2782701, branches=108650, nodes=3000000, truncated=True
- (5,5): mass=1090067/2^21, leaves=2799557, branches=100222, nodes=3000000, truncated=True
- (5,6): mass=2180133/2^22, leaves=2799555, branches=100223, nodes=3000000, truncated=True
- (5,7): mass=1090067/2^21, leaves=2799557, branches=100222, nodes=3000000, truncated=True
- (5,8): mass=1090067/2^21, leaves=2799557, branches=100222, nodes=3000000, truncated=True
- (5,9): mass=2180133/2^22, leaves=2799555, branches=100223, nodes=3000000, truncated=True
- (5,10): mass=1090067/2^21, leaves=2799557, branches=100222, nodes=3000000, truncated=True
- (5,11): mass=563751/2^20, leaves=2782697, branches=108652, nodes=3000000, truncated=True
- (5,12): mass=2180133/2^22, leaves=2799555, branches=100223, nodes=3000000, truncated=True
- (5,13): mass=1062497/2^21, leaves=2812893, branches=93554, nodes=3000000, truncated=True
- (5,14): mass=2180133/2^22, leaves=2799555, branches=100223, nodes=3000000, truncated=True
- (5,15): mass=1127503/2^21, leaves=2782701, branches=108650, nodes=3000000, truncated=True
- (5,16): mass=1127503/2^21, leaves=2782701, branches=108650, nodes=3000000, truncated=True
- (5,17): mass=1127503/2^21, leaves=2782701, branches=108650, nodes=3000000, truncated=True
- (5,18): mass=2255005/2^22, leaves=2782699, branches=108651, nodes=3000000, truncated=True
- (5,19): mass=1090067/2^21, leaves=2799557, branches=100222, nodes=3000000, truncated=True
- (5,20): mass=8041/2^14, leaves=2825143, branches=87429, nodes=3000000, truncated=True
- (5,21): mass=2255005/2^22, leaves=2782699, branches=108651, nodes=3000000, truncated=True
- (5,22): mass=2124991/2^22, leaves=2812887, branches=93557, nodes=3000000, truncated=True
- (5,23): mass=2255005/2^22, leaves=2782699, branches=108651, nodes=3000000, truncated=True
- (5,24): mass=2255005/2^22, leaves=2782699, branches=108651, nodes=3000000, truncated=True
- (5,25): mass=1062495/2^21, leaves=2812885, branches=93558, nodes=3000000, truncated=True
- (5,26): mass=2124993/2^22, leaves=2812891, branches=93555, nodes=3000000, truncated=True
- (5,27): mass=2058497/2^22, leaves=2825145, branches=87428, nodes=3000000, truncated=True
- (5,28): mass=2255005/2^22, leaves=2782699, branches=108651, nodes=3000000, truncated=True
- (5,29): mass=2180133/2^22, leaves=2799555, branches=100223, nodes=3000000, truncated=True
- (5,30): mass=1127503/2^21, leaves=2782701, branches=108650, nodes=3000000, truncated=True
- (5,31): mass=774893/2^21, leaves=2897843, branches=51079, nodes=3000000, truncated=True

## Collapse witnesses

**NO COLLAPSE at k ≤ 5** (min resolved mass = 1939297/2^22 everywhere among fully covered classes; no different-k pair shares an identical resolved canonical form with both unresolved masses < 2^{-10}).

## Shortlist (equal signature, unequal form, different k)

No shortlist pairs (no equal-signature unequal-form cross-k pairs).

## Verdict

NO COLLAPSE at k ≤ 5, min resolved mass = 1939297/2^22
