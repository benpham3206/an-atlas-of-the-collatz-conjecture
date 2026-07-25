---
name: thermo-nuclear-code-quality-review
description: "Strict structure + exactness review for the Collatz atlas (code judo, 1k-line files, spaghetti — plus no floats on a certificate path, independent re-implementation, stated kill criteria, deterministic certificates). Use for thermo-nuclear review, deep quality audit, pre-ship bar, or review of any verifier, certificate generator, or packet in this repo."
version: 1.0.0
author: Hermes Agent
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [code-review, quality, maintainability, architecture, exact-arithmetic, mathematics]
    related_skills: [requesting-code-review, simplify-code]
---

# Thermo-Nuclear Review — Collatz Atlas

Repo-local adaptation of the fleet skill. Canonical portable bar:
`~/FABLE/AGENTS.md` § thermo-nuclear. Full generic prompt:
`~/.hermes/skills/software-development/thermo-nuclear-code-quality-review/`.

**When:** non-trivial code mutate, new or changed verifier, new packet,
pre-commit, pre-ship, any diff that touches a stated result. Not pure
chat, not docs-only typos.

The code here is not application code. It is exact-arithmetic verifiers
and certificate generators that stand behind mathematical claims. A bug
here does not degrade a feature — it invents a theorem. Both bars below
are mandatory. **Exactness outranks structure when they conflict.**

## A. Exactness bar (repo-specific — presumptive blockers)

1. **No floats on a certificate path.** Integers, `fractions.Fraction`,
   exact rationals only. `float`, `math.log`, `numpy` dtypes, `**` with a
   non-integer exponent, and division `/` on the proof path are blockers.
   Use `//`, `<<`, `bit_length()`. Floats are allowed **only** in
   measurements that no proved statement depends on, and the file must
   say so (see the header of `contribution/packets/2026-07-24-contraction-onset/verify_contraction_onset.py`).
2. **Kill criteria before build criteria.** Every load-bearing computation
   asserts a condition that would fire if the claim were false — a `need()`
   / raise, not a printed warning. A verifier that can only pass is not
   evidence. Check exit code is non-zero when a kill criterion fires.
3. **Independent re-implementation for load-bearing numbers.** The claimed
   value must be reproduced by a second, structurally different path
   (direct enumeration vs. closed form, dual enumerator, oracle) or by an
   independent agent recorded in `contribution/reports/VERIFICATION.md`.
   One implementation agreeing with itself is not verification.
4. **Determinism.** Same inputs and env knobs → byte-identical certificate.
   No wall-clock, no unseeded RNG, no set/dict iteration order in output,
   no host-dependent parallelism reordering results. JSON is written
   `sort_keys=True`.
5. **Named controls.** Known-answer cases (x = 1 survives; x = 3, 7, 27,
   703 die) are asserted, including at least one case that must **fail**.
   A screen with no negative control is untested.
6. **Scope honesty — never promote a measurement to a theorem.** A finite
   scan is a bounded exclusion, not a proof. Language must match evidence:
   "verified for h ≤ H_MAX", not "always". Check that any diff touching a
   claim also updates the evidentiary-status column in `README.md` /
   `contribution/README.md` / `STATE.md`, and that nothing moves out of
   `exploratory/` or `quarantine/` without a proof.
7. **Reduced mode must not weaken the claim.** Env knobs (`VCO_REDUCED`,
   `VCO_HMAX`, …) may shrink runtime; the certificate must record the
   actual bound used, and no claim may be stated at a bound the run did
   not reach.
8. **Literature boundary.** A new bound must be compared to the known one
   (Hercher ≤ 91 local minima; Bařina 2^71). Do not present a dominated
   local result as a frontier.

## B. Structure bar (generic — presumptive blockers)

Ambition first: hunt **code judo** — reframes that delete branches,
helpers, modes, or layers while preserving behavior. "It works" is not
approval.

1. File crosses **1000 lines** because of this change → decompose first.
2. Spaghetti growth: ad-hoc `if`s bolted onto unrelated flows.
3. Special-case flags/modes tangled into an already busy path.
4. Packet-specific logic leaking into shared modules (`contribution/code/`,
   `code/fence/`) — and the reverse: a packet re-deriving a canonical
   helper instead of importing it.
5. Thin wrappers, identity abstractions, magic generic mush.
6. Casts / optional soup hiding the real invariant.
7. Bespoke helper where a canonical one exists (cocycle, Terras bijection,
   Φ evaluation, exact cycle search).
8. Logic in the wrong layer: proof prose in code, or a mathematical claim
   living only in a docstring with no `.md` home.
9. Needless sequential orchestration; non-atomic half-written certificates.
10. Refactors that **move** complexity instead of deleting it.

## Review order

Exactness violation → scope overclaim → missing/weak kill criterion →
missing independent check → structural regression → missed code judo →
spaghetti → boundaries → file size → legibility.

Fewer high-conviction comments beat a nit flood.

## Checklist to run before approving

- [ ] `grep -nE '\bfloat\(|math\.(log|sqrt|exp)|numpy|[^/]/[^/=]' ` the diff;
      every hit is either off the certificate path or justified in the header.
- [ ] Every new claim has a kill criterion that can fire, and a control
      that does fire.
- [ ] Load-bearing numbers reproduced by a second path or an independent
      verifier; the record exists in `contribution/reports/`.
- [ ] Verifier run twice → identical certificate bytes.
- [ ] Runtime and env knobs documented in the README verification-commands
      block.
- [ ] Claim wording, evidentiary-status tables, and `STATE.md` all match
      the strength of the evidence.
- [ ] No structural blocker from section B unjustified.

## Tone

Direct, serious, demanding. Not rude. If the diff makes the repo messier,
say so. If a claim outruns its evidence, say so first and loudest. Fix in
the same turn when you own the diff.
