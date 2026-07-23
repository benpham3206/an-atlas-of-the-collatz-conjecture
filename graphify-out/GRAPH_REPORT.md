# Graph Report - collatz-atlas  (2026-07-23)

## Corpus Check
- 106 files · ~178,014 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1353 nodes · 2085 edges · 75 communities (72 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6541c485`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_f2.py
- f4_feature_regression.py
- test_f1.py
- test_primitive_uniform_obstruction.py
- verify_automatic_rigidity.py
- COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md
- rational_shadow.py
- Landmark Proof Architectures and a Collatz Continuation
- verify_drift_wall.py
- Elements of Collatz — A Euclid-Style Research Spine
- test_transcript_lift_oracle.py
- verify_plateau_escape_weight.py
- verify_deep_fourier_scan.py
- test_fence_phase.py
- test_exact_cycle_search.py
- An Atlas of the Collatz Conjecture
- RATIONAL_IRRATIONAL_SHADOW.md
- LENSES.md
- verify_structure_randomness.py
- FENCE.md
- verify_scalar_phase.py
- verify_syracuse_mixing.py
- CycleSearchError
- exact_cycle_search.py
- test_verify_syracuse_fourier.py
- Collatz attack packet — one page for Kimi K3 (and peers)
- Book VIII — Collatz as Language
- LIFT_COCYCLE.md
- PRIMITIVE_UNIFORM_OBSTRUCTION.md
- Elements of Metadynamical Geometry
- affine_CS
- Automatic transcript rigidity: the subcritical and critical strata are closed, the supercritical stratum is provably the
- Plateau self-similarity of the resonance chain: exact chain phases, the containment-to-rate theorem, and the proved impo
- Pointwise drift wall — subcritical aperiodic words are not positive-integer Collatz states
- main
- F1 Report — Collatz word-fold calculus
- Complete research packet — 2026-07-22
- F1 Report — Collatz word-fold calculus
- Architecture — Collatz Atlas + MoO v0
- Structure–randomness transfer assessment, and an isolated test object for the remaining leap
- FORMALIZATION.md
- NOTE.md
- contribution/README.md
- VERIFICATION.md
- EXACT_COUNTEREXAMPLE_SEARCH.md
- F4 Report — Symbolic-feature regression vs mod-2^B baseline
- A structural refinement of Tao's exceptional set, and the honest route map beyond it
- F4 Report — Symbolic-feature regression vs mod-2^B baseline
- The scalar-phase second moment: three exact reductions and the resonance chain that carries the obstruction
- Syracuse Fourier analysis: an exact recursion, exponential L² mixing, and the precise spectral barrier to "all"
- LEMMA2_PROOF.md
- F3 — Fold literature map
- verify_dgg_counterexample.py
- verify_complexity_pressure.py
- verify_rational_complexity_finite.py
- Deep Fourier scan: the resonance-chain structure at depth n = 17, and one measured law that needed restating
- F2 Report — Induced First-Return Maps + Collapse Search
- Lean blueprint: rational-lift complexity obstruction
- PARTIAL_THEOREMS.md
- quarantine/README.md
- COLLATZ_PREFIX_RETURN_BARRIER.md
- Exact finite phase table for two-branch affine maps
- F2b independent screen through k = 10
- Grok packet result
- F2b — analytic collapse screen (2026-07-18)
- verify_plateau_drift_test.py
- collatz_shadow_barrier_verify.py
- Collatz rational shadows: an exact two-metric barrier
- Plateau drift test: the near-peak profile to depth n = 20, exact escape-weight sweeps at all depths, and the failure of the n ≈ 22 crossing on the current trend
- 2. Claim-by-claim alignment with the atlas
- Repository state
- plateau_drift_kernel.c
- Provenance — shadow-barrier packet

## God Nodes (most connected - your core abstractions)
1. `Landmark Proof Architectures and a Collatz Continuation` - 37 edges
2. `Elements of Collatz — A Euclid-Style Research Spine` - 36 edges
3. `An Atlas of the Collatz Conjecture` - 35 edges
4. `Collatz attack packet — one page for Kimi K3 (and peers)` - 29 edges
5. `Complete research packet — 2026-07-22` - 25 edges
6. `Book VIII — Collatz as Language` - 20 edges
7. `main()` - 18 edges
8. `SubstitutionError` - 17 edges
9. `get_class()` - 17 edges
10. `run_all()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Complete research packet — 2026-07-22` --references--> `Collatz attack packet — one page for Kimi K3 (and peers)`  [EXTRACTED]
  contribution/packets/2026-07-22-landmark-pointwise/README.md → COLLATZ_ONE_PAGE.md
- `An Atlas of the Collatz Conjecture` --references--> `Collatz attack packet — one page for Kimi K3 (and peers)`  [EXTRACTED]
  README.md → COLLATZ_ONE_PAGE.md
- `main()` --calls--> `step()`  [INFERRED]
  contribution/packets/2026-07-23-plateau-drift-test/verify_plateau_drift_test.py → contribution/code/fence/fence_phase.py
- `simulate_first_return()` --calls--> `terras()`  [EXTRACTED]
  contribution/code/f2_fold_operator.py → contribution/code/f1_word_calculus.py
- `odd_step_density_scan()` --calls--> `terras()`  [EXTRACTED]
  contribution/code/f4_feature_regression.py → contribution/code/f1_word_calculus.py

## Import Cycles
- None detected.

## Communities (75 total, 3 thin omitted)

### Community 0 - "test_f2.py"
Cohesion: 0.06
Nodes (71): BranchCanon, _apply_terras_step(), _assert_ints(), _branch_diff_count(), ClassResult, collapse_search(), compute_all_classes(), format_canonical() (+63 more)

### Community 1 - "f4_feature_regression.py"
Cohesion: 0.06
Nodes (65): accuracy(), bit_length_feat(), budget_of_spaces(), build_feature_registry(), compute_labels(), enumerate_feature_sets(), excursion_records(), fit_majority_table() (+57 more)

### Community 2 - "test_f1.py"
Cohesion: 0.07
Nodes (62): apply_composite(), c_w_closed_form(), cycle_candidate_sweep(), cycle_n_for_word(), extremal_word_atlas(), extremal_word_check(), is_canonical_necklace_mask(), parity_word() (+54 more)

### Community 3 - "test_primitive_uniform_obstruction.py"
Cohesion: 0.09
Nodes (48): analyze_morphism(), _as_bit_tuple(), build_report(), classify_density_vs_alpha(), default_alpha_bound_certificate(), factor_count(), factor_set(), fixed_point_prefix() (+40 more)

### Community 4 - "verify_automatic_rigidity.py"
Cohesion: 0.07
Nodes (40): all_sigmas(), all_words(), block_oscillator(), classify_word(), cmp_fraction_vs_alpha(), enumerate_uniform(), fibonacci_word(), fixed_point_prefix() (+32 more)

### Community 5 - "COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md"
Cohesion: 0.04
Nodes (47): 2. Near-neutral resonance tiles, Phase 4: globalize, 6. Smale 17: use the right condition metric and the right output notion, Part X. Parallel research programs, Lemma 2. Height-complexity collision principle, Part V. Consequences, 1. The true critical constants, Corollary 7. Balanced supercritical words require large complexity (+39 more)

### Community 6 - "rational_shadow.py"
Cohesion: 0.15
Nodes (36): affine_composite(), build_report(), checked_word(), fibonacci_prefix(), iterate(), main(), periodic_shadow(), phi_prefix_residue() (+28 more)

### Community 7 - "Landmark Proof Architectures and a Collatz Continuation"
Cohesion: 0.06
Nodes (35): Theorem 4.1 — Recurrence forces a `2^L` excursion, Interpretation, 7.1 Golden ratio and golden angle, 2. The recent Dinitz–Garg–Goemans certificate, Consequences, Positive-entropy / high-complexity branch, 7.2 Mersenne excursions, 6. New theorem III: a Perelman-style blow-up at infinity (+27 more)

### Community 8 - "verify_drift_wall.py"
Cohesion: 0.07
Nodes (15): certify_alpha_bounds(), check_lemma1_identity(), check_lemma3_envelope(), correction_cesaro_control(), density_control(), fibonacci_word(), main(), Exact prefix-density controls: final density and max tail density.      Uses int (+7 more)

### Community 9 - "Elements of Collatz — A Euclid-Style Research Spine"
Cohesion: 0.06
Nodes (32): Pattern B — Prove “almost all,” then fight exceptions, Book VI — Proposed Elements table of contents (living), Book 0 — Definitions, Lens 4 — Number theory (integers and divisibility), Proposition 1, Book I — Propositions already proved (firm ground), Lens 3 — Graph theory, Pattern E — Formalize small lemmas (Elements style) (+24 more)

### Community 10 - "test_transcript_lift_oracle.py"
Cohesion: 0.16
Nodes (29): _brute_residue(), _parity_word(), Independent checks for the transcript lift oracle., _terras(), test_all_words_through_length_ten_match_direct_iteration(), test_exact_periodic_controls(), test_positive_integer_lift_bits_are_binary_digits(), test_report_schema_and_controls() (+21 more)

### Community 11 - "verify_plateau_escape_weight.py"
Cohesion: 0.11
Nodes (24): small_stack(), test_bad_set_containment_guard(), test_chain_recursion_identity(), test_exact_chain_phases_small(), test_t3_quantization_gap_and_s3(), test_t5_phaseblind_propagation_gap_positive(), bad_mask(), chain_log() (+16 more)

### Community 12 - "verify_deep_fourier_scan.py"
Cohesion: 0.10
Nodes (16): bad_indices(), chain_exponent(), chain_log_bruteforce(), chain_log_bsgs(), decay_fit(), escape_weights(), main(), Smallest k with 2^k == +xi or 2^k == -xi (mod 3^n), or None. (+8 more)

### Community 13 - "test_fence_phase.py"
Cohesion: 0.18
Nodes (23): canonical_cycle(), classify_system(), contains_float(), main(), markdown_table(), Path, Exact finite phase scan for two-branch maps T_{a,b}.  This is an empirical class, Classify every seed in [1, seed_stop) under explicit finite caps. (+15 more)

### Community 14 - "test_exact_cycle_search.py"
Cohesion: 0.13
Nodes (23): canonical_composition_count(), composition_count(), compositions_of(), fixed_point_fraction(), Fraction, Return C_m / (2^K - 3^m) when 2^K != 3^m; else None., Stream all ordered compositions of K into m positive integer parts.      Count o, Number of positive compositions of K into m parts (before symmetry). (+15 more)

### Community 15 - "An Atlas of the Collatz Conjecture"
Cohesion: 0.09
Nodes (18): Repository layout, Literature references, Foundational structure, Status, Verification commands, Statistical results, Cycles, Surveys and bibliography (+10 more)

### Community 16 - "RATIONAL_IRRATIONAL_SHADOW.md"
Cohesion: 0.10
Nodes (20): The requested irrational limit, 2. Delete the part or process, Verdict, Kill criteria and next exact question, Proposition 3 — rational imitation has a height cost, Chaos and emergent-complexity interpretation, 3. Simplify and optimize what remains, Sources and provenance (+12 more)

### Community 17 - "LENSES.md"
Cohesion: 0.10
Nodes (20): Lens catalog (progress trees), 3. Physics — least energy / Lyapunov, 2. Engineering — control, stability, FMEA, 7. Binary residue descent certificates, 8. Material science — microstructure & annealing, 4. Physics — Dirac / Schrödinger / transfer operator, Strategic target (your Tao bridge), Suggested session order (mechanical engineer path) (+12 more)

### Community 18 - "verify_structure_randomness.py"
Cohesion: 0.15
Nodes (11): biased_champernowne(), certify_critical_line(), density_control(), fibonacci_word(), full_complexity_certificate(), lift_digit_report(), lift_stats(), main() (+3 more)

### Community 19 - "FENCE.md"
Cohesion: 0.10
Nodes (19): 1. Known landscape, with scope, 8. Adversarial audit and disagreements with repo framing, 9. Sources, 1. Structured-transcript integrality, 3. Minimal deterministic generalized-Collatz compiler, 7. Ranked attack routes, 4. Empirical phase map, Disagreements (+11 more)

### Community 20 - "verify_scalar_phase.py"
Cohesion: 0.14
Nodes (11): chain_log(), escape_weight_profile(), main(), Per-unit escape weight sum_{a: xi u_a not in B(eps)} 2^-a.      Returns (weights, Smallest k with 2^k == +/- xi (mod 3^n), or None., max ||c_{n+1}(xi)|^2 - (diagonal + cross-term sum from layer n)|., Return (eta, phi) with phi = arg(A conj(B)), eta = 1 - cos(phi)., s1_second_moment_check() (+3 more)

### Community 21 - "verify_syracuse_mixing.py"
Cohesion: 0.15
Nodes (11): char_function_max(), decay_table(), main(), oscillation(), One step of Lemma 1.12: P on Z/3^n -> Q on Z/3^{n+1}, exact., Yield (n, P) float64 distributions for n = 1..n_max., max |sum_x P(x) e^{-2πi ξ x / 3^n}| over ξ not divisible by 3., Osc_{m,n} of the distribution tuple (Tao's (1.27)).      Coset of Y is {Y' == Y (+3 more)

### Community 22 - "CycleSearchError"
Cohesion: 0.14
Nodes (15): CycleSearchError, odd_only_step(), parse_pair(), Direct exact orbit check for U under prescribed valuations.      Returns     ---, Machine-checkable failure record., Parse ``m:K`` into integers., Raised for invalid CLI / parameter input with a structured payload., 2-adic valuation of a positive even integer; rejects non-positive. (+7 more)

### Community 23 - "exact_cycle_search.py"
Cohesion: 0.18
Nodes (14): canonical_rotation(), CycleCandidate, evaluate_exponents(), is_canonical_rotation(), is_positive_composition(), is_trivial_cycle(), Exact positive-cycle search for the fixed odd-only 3n+1 map.  Map (odd positives, True iff a is a length-m composition of K into positive parts. (+6 more)

### Community 24 - "test_verify_syracuse_fourier.py"
Cohesion: 0.16
Nodes (8): char_recursion_check(), is_primitive_root_2(), main(), max |c_{n+1}(xi) - sum_a 2^-a e(-xi u_a/3^{n+1}) c_n(xi u_a mod 3^n)|., Check ord_{3^n}(2) == 2*3^{n-1}., Eigenvalues of the walk t -> t - a (Geom(2)) on Z/NZ, N = 2*3^{n-1}.      Compar, syracuse_float_layers(), walk_eigenvalue_check()

### Community 25 - "Collatz attack packet — one page for Kimi K3 (and peers)"
Cohesion: 0.13
Nodes (16): 3. Best computational assault this arc (Codex, 2026-07-22), 2.1 Finite parity = residue (Terras), 2.2 Realizability wall, 2.6 Rational complexity pressure (pointwise advance), 4. Complete research packet (strategy + diagrams), 2.4 Fold counting law (Lemma 2), 2.8 Primitive uniform subcritical obstruction, 2. Already-proved toolkit (use these; do not re-derive casually) (+8 more)

### Community 26 - "Book VIII — Collatz as Language"
Cohesion: 0.13
Nodes (16): Multi-Lens Collatz Research — Engineering & Physics Map, Is this “homomorphic” with your earlier program?, Pure language proof-search prompt, Book VIII — Definitions (vocabulary), Three language attacks (concrete, no W-focus), Attack B — Parser density (Tao bridge in language), Why “language” might be the right primary lens, Attack A — Finite grammar cover (+8 more)

### Community 27 - "LIFT_COCYCLE.md"
Cohesion: 0.12
Nodes (15): Positive-integer criterion, Grok 4.5/high registry, Proof, Cycle Double Cover prompt and proof, Metadynamical Geometry audit, Oracle, One-read resume, Exact lift recurrence (+7 more)

### Community 28 - "PRIMITIVE_UNIFORM_OBSTRUCTION.md"
Cohesion: 0.13
Nodes (14): Exact boundary of the advance, Rational states with irrational-like Collatz behavior, 3. Rational realization would force full factor entropy, What was deleted from the search, Primitive subcritical substitutions cannot be rational Collatz transcripts, Result, Two exact corollaries, Proof (+6 more)

### Community 29 - "Elements of Metadynamical Geometry"
Cohesion: 0.14
Nodes (15): Elements of Metadynamical Geometry, Book 0 — Postulates, Book 0 — Common notions, Book III — Founding problems, Book 0 — Definitions, Proposition 2 — Finite observational collision is an equivalence relation, How to read this, Exploratory drafts (+7 more)

### Community 30 - "affine_CS"
Cohesion: 0.18
Nodes (14): affine_CS(), affine_fixed_point_via_direct_formula(), Odd-only accelerated Collatz map on positive odd integers., Compute (C_m, S_m) for exponent tuple a via the packet recurrence.      S_0 = 0,, If a yields an exact positive odd integer fixed point, return (n, C_m, denom)., Apply the composite odd-only map assuming valuations a hold: (3^m n + C_m) / 2^K, try_integral_fixed_point(), U() (+6 more)

### Community 31 - "Automatic transcript rigidity: the subcritical and critical strata are closed, the supercritical stratum is provably the"
Cohesion: 0.15
Nodes (14): 5. Theorem 1 — the automatic rigidity trichotomy (PROVED), 13. Reproduce, 6. Theorem 2 — the critical density is forbidden to automatic words (PROVED), 3. Lemma A — \(\log_3 2\) is transcendental (PROVED), 7. Theorem 3 — the supercritical stratum is nonempty and density-proof (PROVED), 1. Setup, Automatic transcript rigidity: the subcritical and critical strata are closed, the supercritical stratum is provably the, 10. Route 4 assessment: the lift is not a finite transduction (+6 more)

### Community 32 - "Plateau self-similarity of the resonance chain: exact chain phases, the containment-to-rate theorem, and the proved impo"
Cohesion: 0.17
Nodes (13): P1 — exact chain phases (proved; exact-arithmetic certificate), P3 — S3 is the \(\varepsilon\)-quantization of the triangle bound (proved), Plateau self-similarity of the resonance chain: exact chain phases, the containment-to-rate theorem, and the proved impo, What is proved vs what remains, Kill criteria (stated up front), P2 — no phase-blind supersolution (proved barrier), Reproduce, Related work (+5 more)

### Community 33 - "Pointwise drift wall — subcritical aperiodic words are not positive-integer Collatz states"
Cohesion: 0.17
Nodes (13): Pointwise drift wall — subcritical aperiodic words are not positive-integer Collatz states, 5. Corollary — the two-wall screen for any counterexample transcript, Lemma 3 — unconditional upper envelope, 6. Named-class eliminations, 3. Theorem 1 — pointwise drift wall, 9. Reproduce, 8. Related work, 4. Theorem 2 — subcritical realizability obstruction (+5 more)

### Community 34 - "main"
Cohesion: 0.21
Nodes (11): ArgumentParser, build_arg_parser(), build_report(), dumps_report(), main(), PairResult, Path, Run the search on each pair and assemble a deterministic JSON report. (+3 more)

### Community 35 - "F1 Report — Collatz word-fold calculus"
Cohesion: 0.18
Nodes (12): Per-section results and wall-clock runtimes, Stopping time (first drop below n), F1 Report — Collatz word-fold calculus, Total stopping time (to 1), Environment, Stopping-time spectrum summary, Exact statements verified, Files (+4 more)

### Community 36 - "Complete research packet — 2026-07-22"
Cohesion: 0.18
Nodes (3): Complete research packet — 2026-07-22, Related Codex best attempt (same research arc), Artifact map

### Community 37 - "F1 Report — Collatz word-fold calculus"
Cohesion: 0.18
Nodes (12): Total stopping time (to 1), Environment, F1 Report — Collatz word-fold calculus, Per-section results and wall-clock runtimes, Cycle-candidate certificate detail, Stopping time (first drop below n), Exact statements verified, Definitions (+4 more)

### Community 38 - "Architecture — Collatz Atlas + MoO v0"
Cohesion: 0.20
Nodes (10): Extension points, Tool Plane (`tools/`), MoO Control Plane (`moo/`), Architecture — Collatz Atlas + MoO v0, Planes, Hypothesis synthesis flow, Quarantine, Purpose (+2 more)

### Community 39 - "Structure–randomness transfer assessment, and an isolated test object for the remaining leap"
Cohesion: 0.20
Nodes (11): 7. What *does* transfer, 2. The crosswalk, Structure–randomness transfer assessment, and an isolated test object for the remaining leap, 8. Kill criteria and exact boundary, 1. The question, 9. Related work, 5. Lift-digit excursion statistics (numerical, non-rigorous), 4. Corollary — symbolic closure is impossible; the residual is arithmetic (+3 more)

### Community 40 - "FORMALIZATION.md"
Cohesion: 0.18
Nodes (10): 3. Guarded matrix-semigroup framing, Formalizing the computational-encoding fence, 1. The fixed map and three different decision questions, 2. What “simulate a machine” must mean here, 2.3 Fixed-target simulation, Lemma 2: exact first-return branch count, 2.4 The parity-forcing condition, 2.1 Step-faithful orbit embedding (+2 more)

### Community 41 - "NOTE.md"
Cohesion: 0.20
Nodes (9): 3. The slope invariant, 4. The counting law, 7. Computational appendix, Abstract, No Small Self-Similar Collapse in the Collatz Fold, 1. Setup, 6. What this result is, and is not, 5. The screen and the theorem (+1 more)

### Community 42 - "contribution/README.md"
Cohesion: 0.20
Nodes (6): Code, Fold program, Fold program, Results, Files, DEFINITIONS — the fold program's ledger of primitives

### Community 43 - "VERIFICATION.md"
Cohesion: 0.20
Nodes (9): All 14 empirical comparisons, Confidence, Exact first-return correction, Discrepancy with existing framing, Independent recurrence comparison, F2b verification, What ran, Extension result (+1 more)

### Community 44 - "EXACT_COUNTEREXAMPLE_SEARCH.md"
Cohesion: 0.20
Nodes (9): Result, THE FENCE: computational encoding for the fixed `3n+1` map, Exact cycle certificate, A complete finite search window, What remains for a complete counterexample, Reproduction, Why enumeration stops here, Why the cycle branch (+1 more)

### Community 45 - "F4 Report — Symbolic-feature regression vs mod-2^B baseline"
Cohesion: 0.22
Nodes (10): F4 Report — Symbolic-feature regression vs mod-2^B baseline, Runtime note, Baselines, Files, Verdict, Null hypothesis, Protocol, Observation (why the baseline is perfect) (+2 more)

### Community 46 - "A structural refinement of Tao's exceptional set, and the honest route map beyond it"
Cohesion: 0.25
Nodes (9): 4. Observation B — Tao's deepest proposition is a Bernoulli-convolution problem, 1. What Tao proved, exactly, 6. Kill criteria and exact boundary, 7. Related work, Exact counterexample search: cycle branch, A structural refinement of Tao's exceptional set, and the honest route map beyond it, 3. Theorem A — the exceptional set is density-zero AND symbolically rigid, 5. The route map beyond Tao, ranked by honesty (+1 more)

### Community 47 - "F4 Report — Symbolic-feature regression vs mod-2^B baseline"
Cohesion: 0.25
Nodes (9): F4 Report — Symbolic-feature regression vs mod-2^B baseline, Runtime note, Files, Baselines, Leaderboard (top 20 features + baselines inline), Verdict, Protocol, Excursion records (sustained odd-step density) (+1 more)

### Community 48 - "The scalar-phase second moment: three exact reductions and the resonance chain that carries the obstruction"
Cohesion: 0.25
Nodes (9): 5. What is now proved vs what remains, 8. Reproduce, The scalar-phase second moment: three exact reductions and the resonance chain that carries the obstruction, 6. Kill criteria, 1. Theorem S1 — exact second-moment recursion (proved), 3. Theorem S3 — the bad-set escape criterion (proved), 2. Theorem S2 — conditional contraction / coherence dichotomy (proved), 7. Related work (+1 more)

### Community 49 - "Syracuse Fourier analysis: an exact recursion, exponential L² mixing, and the precise spectral barrier to "all""
Cohesion: 0.25
Nodes (9): Syracuse Fourier analysis: an exact recursion, exponential L² mixing, and the precise spectral barrier to "all", 5. What this buys the "almost all → all" program, 7. Related work, 3. Corollary 3 — exponential L² Fourier mixing (proved), 4. Theorem 4 — the spectral barrier, as a number, 6. Kill criteria and exact boundary, 8. Reproduce, 1. Theorem 1 — exact characteristic-function recursion (+1 more)

### Community 50 - "LEMMA2_PROOF.md"
Cohesion: 0.22
Nodes (8): Transcript lift cocycle — first realizability probe, 3. Each accepted extension is exactly one fold branch, Statement with all conventions fixed, 2. First return is exactly first completion in the extension, 1. Refinements of `m` are exactly extensions of the initial word, Lemma 2: exact first-return branch count, 4. Transfer-matrix count, Proof

### Community 51 - "F3 — Fold literature map"
Cohesion: 0.25
Nodes (9): 2. 2-adic structure, 6. First-return / induced maps  ⟵ F2's territory, 5. Undecidability fence, F3 — Fold literature map, 7. Heights / arithmetic dynamics, 1. Parity words, 3. The 3x+1 semigroup, Three-line summary (+1 more)

### Community 52 - "verify_dgg_counterexample.py"
Cohesion: 0.43
Nodes (7): Arc, add_load(), Commodity, main(), Route, verify_fractional(), verify_unsplittable()

### Community 53 - "verify_complexity_pressure.py"
Cohesion: 0.43
Nodes (6): check_seed(), green_exact(), main(), orbit_and_parity(), Fraction, terras()

### Community 54 - "verify_rational_complexity_finite.py"
Cohesion: 0.36
Nodes (7): affine_constant(), check_case(), main(), Orbit, One Terras step for x=y/d with d positive odd; return (next_y, parity)., Return (number of ones, c) in 2^k y_k = 3^s y_0 + d*c., scaled_step()

### Community 55 - "Deep Fourier scan: the resonance-chain structure at depth n = 17, and one measured law that needed restating"
Cohesion: 0.29
Nodes (8): Deep Fourier scan: the resonance-chain structure at depth n = 17, and one measured law that needed restating, 1. Kill criteria, stated before build criteria, 6. Related work, 3. What held (all float64 measurements, n = 6..17), 4. What broke: the window law \(k(n)\in[n,n+3]\), 5. Verdict, Landmark Resolution Strategies and a Pointwise Collatz Advance, 2. What was extended

### Community 56 - "F2 Report — Induced First-Return Maps + Collapse Search"
Cohesion: 0.29
Nodes (8): Unresolved mass, F2 Report — Induced First-Return Maps + Collapse Search, Shortlist (equal signature, unequal form, different k), Per-k statistics, Collapse witnesses, Branch-count vs k (growth curve), Verdict, Budgets

### Community 57 - "Lean blueprint: rational-lift complexity obstruction"
Cohesion: 0.33
Nodes (7): Sturmian interface, Lean blueprint: rational-lift complexity obstruction, Headline theorem, Core lemmas, Main mathematical statement, Recommended integer-scaled definitions, Audit points

### Community 58 - "PARTIAL_THEOREMS.md"
Cohesion: 0.33
Nodes (5): Theorem 1 — finite-cylinder saturation, Partial fence theorems, Theorem 3 — eventually periodic transcripts are a decidable weak island, Primitive subcritical substitutions cannot be rational Collatz transcripts, Theorem 2 — exact global realizability criterion

### Community 59 - "quarantine/README.md"
Cohesion: 0.33
Nodes (3): Contents, Policy, Quarantine

### Community 60 - "COLLATZ_PREFIX_RETURN_BARRIER.md"
Cohesion: 0.40
Nodes (4): Interpretation, Theorem, Prefix-return barrier for positive Collatz parity transcripts, Proof

### Community 61 - "Exact finite phase table for two-branch affine maps"
Cohesion: 0.67
Nodes (4): Unresolved witnesses, Exact finite phase table for two-branch affine maps, Exact cycle certificates, F2b verification

### Community 62 - "F2b independent screen through k = 10"
Cohesion: 0.67
Nodes (4): Rate collisions are not law collisions, F2b independent screen through k = 10, Exact law table, Verdict

### Community 67 - "verify_plateau_drift_test.py"
Cohesion: 0.06
Nodes (46): dense_stack(), The candidate-set minimum (new, used at all depths) equals the     brute-force m, Synthetic bad block of length L on the chain: w = 2^-L - 2^-40     exactly, atta, The recursion identity, numpy path, against dense FFT ground truth     at every, The C transport kernel agrees with the numpy reference to 1e-13 at     every lay, Exact discrete-log certificate against a brute-force reference     (provenance:, test_c_kernel_matches_numpy(), test_chain_exponent_bsgs_vs_bruteforce() (+38 more)

### Community 68 - "collatz_shadow_barrier_verify.py"
Cohesion: 0.21
Nodes (21): affine_data(), build_report(), canonical_positive_residue(), checked_word(), floor_fraction(), iterate_integer(), iterate_rational(), main() (+13 more)

### Community 69 - "Collatz rational shadows: an exact two-metric barrier"
Cohesion: 0.12
Nodes (16): 1. Definitions, 2. The shadow-barrier theorem, 3. Exact strict-rise pruning, 4. The two-metric theorem, 5. What this changes, 6. Engineering strategy after the deletion, 7. Verification, 8. Source boundary (+8 more)

### Community 70 - "Plateau drift test: the near-peak profile to depth n = 20, exact escape-weight sweeps at all depths, and the failure of the n ≈ 22 crossing on the current trend"
Cohesion: 0.17
Nodes (11): 10. Reproduce, 1. The prediction under test (stated up front), 2. Why the old engine died at n = 18 (diagnosis) and the new engine, 3. What was extended (all float64 measurements unless labelled exact), 4. The parity alternation (new structural observation), 5. The p₂-extrapolation verdict, 6. L-creep and \(w_n(0.05)\) vs the \(1/4\) threshold, 7. Counterexample watch (mandatory section) (+3 more)

### Community 71 - "2. Claim-by-claim alignment with the atlas"
Cohesion: 0.17
Nodes (11): 1. The "Terence Method" as described in the thread, 2.1 Transcript-lift framework, 2.2 Structured low-complexity exclusions, 2.3 Shadow barrier, 2.4 Ghost words, 2.5 Lift digits as the residual wall, 2.6 Other concrete claims in the thread, 2. Claim-by-claim alignment with the atlas (+3 more)

### Community 72 - "Repository state"
Cohesion: 0.40
Nodes (4): BLOCKED, ESTABLISHED, NEXT, Repository state

### Community 74 - "Provenance — shadow-barrier packet"
Cohesion: 0.50
Nodes (3): Adversarial read-back: gaps between this theorem and Collatz progress, Independent rerun verdict, Provenance — shadow-barrier packet

## Knowledge Gaps
- **517 isolated node(s):** `Route`, `Commodity`, `ESTABLISHED`, `BLOCKED`, `NEXT` (+512 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Complete research packet — 2026-07-22` connect `Complete research packet — 2026-07-22` to `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`, `Landmark Proof Architectures and a Collatz Continuation`, `EXACT_COUNTEREXAMPLE_SEARCH.md`, `COLLATZ_PREFIX_RETURN_BARRIER.md`, `RATIONAL_IRRATIONAL_SHADOW.md`, `verify_dgg_counterexample.py`, `verify_complexity_pressure.py`, `verify_rational_complexity_finite.py`, `exact_cycle_search.py`, `Lean blueprint: rational-lift complexity obstruction`, `PRIMITIVE_UNIFORM_OBSTRUCTION.md`, `Collatz attack packet — one page for Kimi K3 (and peers)`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `Collatz attack packet — one page for Kimi K3 (and peers)` connect `Collatz attack packet — one page for Kimi K3 (and peers)` to `Complete research packet — 2026-07-22`, `COLLATZ_LANDMARK_STRATEGY_AND_POINTWISE_THEOREM.md`, `NOTE.md`, `contribution/README.md`, `EXACT_COUNTEREXAMPLE_SEARCH.md`, `COLLATZ_PREFIX_RETURN_BARRIER.md`, `An Atlas of the Collatz Conjecture`, `RATIONAL_IRRATIONAL_SHADOW.md`, `LEMMA2_PROOF.md`, `PARTIAL_THEOREMS.md`, `PRIMITIVE_UNIFORM_OBSTRUCTION.md`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `An Atlas of the Collatz Conjecture` connect `An Atlas of the Collatz Conjecture` to `Architecture — Collatz Atlas + MoO v0`, `NOTE.md`, `contribution/README.md`, `VERIFICATION.md`, `FENCE.md`, `Collatz attack packet — one page for Kimi K3 (and peers)`, `quarantine/README.md`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `Route`, `Commodity`, `ESTABLISHED` to the rest of the system?**
  _517 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_f2.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05980861244019139 - nodes in this community are weakly interconnected._
- **Should `f4_feature_regression.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060528559249786874 - nodes in this community are weakly interconnected._
- **Should `test_f1.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06603346901854365 - nodes in this community are weakly interconnected._