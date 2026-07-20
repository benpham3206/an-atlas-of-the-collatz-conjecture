# Exact finite phase table for two-branch affine maps

For positive odd `a,b`, this scan applies `T(n)=n/2` on even `n` and `T(n)=(a*n+b)/2` on odd `n`. Every integer `1 <= n < 1,000,000` was classified with exact integer arithmetic.

The labels are observations at the recorded caps, not asymptotic theorems:

- `all-converge`: all tested seeds reached `1`.
- `cycles`: every seed resolved, but some entered a cycle not containing `1`.
- `apparent-divergence`: some seed exceeded the step or bit-length cap; this   does not prove divergence.

Caps: `10000` new steps per path; current value unresolved when bit length exceeds `64`. The memoization cap `1000000000` changes performance only, not classification.

| a | b | label | hit 1 | nontrivial-cycle basin | unresolved | cycles (lengths) |
|---:|---:|---|---:|---:|---:|---|
| 1 | 1 | all-converge | 999999 | 0 | 0 | none |
| 1 | 3 | cycles | 666666 | 333333 | 0 | 1 |
| 1 | 5 | cycles | 800000 | 199999 | 0 | 1 |
| 1 | 7 | cycles | 428571 | 571428 | 0 | 3, 1 |
| 1 | 9 | cycles | 666666 | 333333 | 0 | 2, 1 |
| 3 | 1 | all-converge | 999999 | 0 | 0 | none |
| 3 | 3 | cycles | 20 | 999979 | 0 | 2 |
| 3 | 5 | cycles | 140991 | 859008 | 0 | 2, 5, 5, 27, 27 |
| 3 | 7 | cycles | 689910 | 310089 | 0 | 4, 2 |
| 3 | 9 | cycles | 20 | 999979 | 0 | 2 |
| 5 | 1 | apparent-divergence | 4324 | 8998 | 986677 | 7, 7 |
| 5 | 3 | apparent-divergence | 1216 | 10389 | 988394 | 5, 7, 7, 7, 7, 7 |
| 5 | 5 | apparent-divergence | 20 | 23793 | 976186 | 5, 7, 7 |
| 5 | 7 | apparent-divergence | 30941 | 13785 | 955273 | 5, 5, 42, 7, 7 |
| 5 | 9 | apparent-divergence | 17411 | 38762 | 943826 | 3, 5, 63, 21, 7, 7, 7, 7, 7 |
| 7 | 1 | apparent-divergence | 291 | 0 | 999708 | none |
| 7 | 3 | apparent-divergence | 20 | 217 | 999762 | 3 |
| 7 | 5 | apparent-divergence | 20 | 2490 | 997489 | 6, 3, 31 |
| 7 | 7 | apparent-divergence | 20 | 1284 | 998695 | 3 |
| 7 | 9 | apparent-divergence | 121 | 166 | 999712 | 3 |
| 9 | 1 | apparent-divergence | 248 | 0 | 999751 | none |
| 9 | 3 | apparent-divergence | 20 | 0 | 999979 | none |
| 9 | 5 | apparent-divergence | 226 | 0 | 999773 | none |
| 9 | 7 | apparent-divergence | 93 | 0 | 999906 | none |
| 9 | 9 | apparent-divergence | 20 | 0 | 999979 | none |

## Exact cycle certificates

- `(a,b)=(1,3)`: (3)
- `(a,b)=(1,5)`: (5)
- `(a,b)=(1,7)`: (3, 5, 6); (7)
- `(a,b)=(1,9)`: (3, 6); (9)
- `(a,b)=(3,3)`: (3, 6)
- `(a,b)=(3,5)`: (5, 10); (19, 31, 49, 76, 38); (23, 37, 58, 29, 46); (187, 283, 427, 643, 967, 1453, 2182, 1091, 1639, 2461, 3694, 1847, 2773, 4162, 2081, 3124, 1562, 781, 1174, 587, 883, 1327, 1993, 2992, 1496, 748, 374); (347, 523, 787, 1183, 1777, 2668, 1334, 667, 1003, 1507, 2263, 3397, 5098, 2549, 3826, 1913, 2872, 1436, 718, 359, 541, 814, 407, 613, 922, 461, 694)
- `(a,b)=(3,7)`: (5, 11, 20, 10); (7, 14)
- `(a,b)=(3,9)`: (9, 18)
- `(a,b)=(5,1)`: (13, 33, 83, 208, 104, 52, 26); (17, 43, 108, 54, 27, 68, 34)
- `(a,b)=(5,3)`: (3, 9, 24, 12, 6); (39, 99, 249, 624, 312, 156, 78); (43, 109, 274, 137, 344, 172, 86); (51, 129, 324, 162, 81, 204, 102); (53, 134, 67, 169, 424, 212, 106); (61, 154, 77, 194, 97, 244, 122)
- `(a,b)=(5,5)`: (5, 15, 40, 20, 10); (65, 165, 415, 1040, 520, 260, 130); (85, 215, 540, 270, 135, 340, 170)
- `(a,b)=(5,7)`: (7, 21, 56, 28, 14); (9, 26, 13, 36, 18); (57, 146, 73, 186, 93, 236, 118, 59, 151, 381, 956, 478, 239, 601, 1506, 753, 1886, 943, 2361, 5906, 2953, 7386, 3693, 9236, 4618, 2309, 5776, 2888, 1444, 722, 361, 906, 453, 1136, 568, 284, 142, 71, 181, 456, 228, 114); (91, 231, 581, 1456, 728, 364, 182); (119, 301, 756, 378, 189, 476, 238)
- `(a,b)=(5,9)`: (3, 12, 6); (9, 27, 72, 36, 18); (29, 77, 197, 497, 1247, 3122, 1561, 3907, 9772, 4886, 2443, 6112, 3056, 1528, 764, 382, 191, 482, 241, 607, 1522, 761, 1907, 4772, 2386, 1193, 2987, 7472, 3736, 1868, 934, 467, 1172, 586, 293, 737, 1847, 4622, 2311, 5782, 2891, 7232, 3616, 1808, 904, 452, 226, 113, 287, 722, 361, 907, 2272, 1136, 568, 284, 142, 71, 182, 91, 232, 116, 58); (89, 227, 572, 286, 143, 362, 181, 457, 1147, 2872, 1436, 718, 359, 902, 451, 1132, 566, 283, 712, 356, 178); (117, 297, 747, 1872, 936, 468, 234); (129, 327, 822, 411, 1032, 516, 258); (153, 387, 972, 486, 243, 612, 306); (159, 402, 201, 507, 1272, 636, 318); (183, 462, 231, 582, 291, 732, 366)
- `(a,b)=(7,3)`: (3, 12, 6)
- `(a,b)=(7,5)`: (3, 13, 48, 24, 12, 6); (5, 20, 10); (27, 97, 342, 171, 601, 2106, 1053, 3688, 1844, 922, 461, 1616, 808, 404, 202, 101, 356, 178, 89, 314, 157, 552, 276, 138, 69, 244, 122, 61, 216, 108, 54)
- `(a,b)=(7,7)`: (7, 28, 14)
- `(a,b)=(7,9)`: (9, 36, 18)

## Unresolved witnesses

- `(a,b)=(5,1)`: seed 7: bit_length_cap after 496 steps at 20792241994709032708 (65 bits), peak 20792241994709032708; seed 9: bit_length_cap after 494 steps at 20792241994709032708 (65 bits), peak 20792241994709032708; seed 11: bit_length_cap after 499 steps at 20792241994709032708 (65 bits), peak 20792241994709032708
- `(a,b)=(5,3)`: seed 5: bit_length_cap after 170 steps at 34778599078970729999 (65 bits), peak 34778599078970729999; seed 7: bit_length_cap after 168 steps at 34778599078970729999 (65 bits), peak 34778599078970729999; seed 10: bit_length_cap after 171 steps at 34778599078970729999 (65 bits), peak 34778599078970729999
- `(a,b)=(5,5)`: seed 13: bit_length_cap after 496 steps at 41584483989418065415 (66 bits), peak 41584483989418065415; seed 17: bit_length_cap after 494 steps at 41584483989418065415 (66 bits), peak 41584483989418065415; seed 21: bit_length_cap after 499 steps at 41584483989418065415 (66 bits), peak 41584483989418065415
- `(a,b)=(5,7)`: seed 19: bit_length_cap after 320 steps at 42737299218590718831 (66 bits), peak 42737299218590718831; seed 25: bit_length_cap after 525 steps at 37419054157896891281 (66 bits), peak 37419054157896891281; seed 29: bit_length_cap after 323 steps at 42737299218590718831 (66 bits), peak 42737299218590718831
- `(a,b)=(5,9)`: seed 15: bit_length_cap after 169 steps at 41734318894764875997 (66 bits), peak 41734318894764875997; seed 21: bit_length_cap after 167 steps at 41734318894764875997 (66 bits), peak 41734318894764875997; seed 30: bit_length_cap after 170 steps at 41734318894764875997 (66 bits), peak 41734318894764875997
- `(a,b)=(7,1)`: seed 3: bit_length_cap after 136 steps at 37440588738881858072 (66 bits), peak 37440588738881858072; seed 6: bit_length_cap after 137 steps at 37440588738881858072 (66 bits), peak 37440588738881858072; seed 7: bit_length_cap after 140 steps at 37440588738881858072 (66 bits), peak 37440588738881858072
- `(a,b)=(7,3)`: seed 5: bit_length_cap after 118 steps at 21111487734825885815 (65 bits), peak 21111487734825885815; seed 7: bit_length_cap after 138 steps at 22626927237820307029 (65 bits), peak 22626927237820307029; seed 9: bit_length_cap after 135 steps at 32091933204755878347 (65 bits), peak 32091933204755878347
- `(a,b)=(7,5)`: seed 9: bit_length_cap after 99 steps at 24419659589325802136 (65 bits), peak 24419659589325802136; seed 11: bit_length_cap after 121 steps at 40114707932475432416 (66 bits), peak 40114707932475432416; seed 15: bit_length_cap after 111 steps at 22237305628125617840 (65 bits), peak 22237305628125617840
- `(a,b)=(7,7)`: seed 5: bit_length_cap after 112 steps at 31132227879375864976 (65 bits), peak 31132227879375864976; seed 10: bit_length_cap after 113 steps at 31132227879375864976 (65 bits), peak 31132227879375864976; seed 11: bit_length_cap after 113 steps at 31132227879375864976 (65 bits), peak 31132227879375864976
- `(a,b)=(7,9)`: seed 3: bit_length_cap after 119 steps at 63334463204477657445 (66 bits), peak 63334463204477657445; seed 5: bit_length_cap after 110 steps at 20059124720517800345 (65 bits), peak 20059124720517800345; seed 6: bit_length_cap after 120 steps at 63334463204477657445 (66 bits), peak 63334463204477657445
- `(a,b)=(9,1)`: seed 5: bit_length_cap after 90 steps at 26711117999993500025 (65 bits), peak 26711117999993500025; seed 9: bit_length_cap after 121 steps at 76301006555797032470 (67 bits), peak 76301006555797032470; seed 10: bit_length_cap after 91 steps at 26711117999993500025 (65 bits), peak 26711117999993500025
- `(a,b)=(9,3)`: seed 3: bit_length_cap after 91 steps at 80133353999980500075 (67 bits), peak 80133353999980500075; seed 5: bit_length_cap after 95 steps at 80133353999980500075 (67 bits), peak 80133353999980500075; seed 6: bit_length_cap after 92 steps at 80133353999980500075 (67 bits), peak 80133353999980500075
- `(a,b)=(9,5)`: seed 5: bit_length_cap after 90 steps at 29679019999992777805 (65 bits), peak 29679019999992777805; seed 7: bit_length_cap after 137 steps at 59696803380277063159 (66 bits), peak 59696803380277063159; seed 9: bit_length_cap after 69 steps at 22153085483223568903 (65 bits), peak 22153085483223568903
- `(a,b)=(9,7)`: seed 3: bit_length_cap after 93 steps at 28885418476648797797 (65 bits), peak 28885418476648797797; seed 5: bit_length_cap after 87 steps at 28885418476648797797 (65 bits), peak 28885418476648797797; seed 6: bit_length_cap after 94 steps at 28885418476648797797 (65 bits), peak 28885418476648797797
- `(a,b)=(9,9)`: seed 3: bit_length_cap after 92 steps at 53422235999987000049 (66 bits), peak 53422235999987000049; seed 5: bit_length_cap after 99 steps at 53422235999987000049 (66 bits), peak 53422235999987000049; seed 6: bit_length_cap after 93 steps at 53422235999987000049 (66 bits), peak 53422235999987000049

## Audit boundary

The `(3,1)` row is only a bounded empirical `all-converge` row. Finite enumeration cannot establish the Collatz conjecture. Likewise, an unresolved orbit is only a cap witness, never a divergence certificate.
