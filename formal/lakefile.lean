import Lake
open Lake DSL

/--
Collatz atlas — formal certificates.

Plain Lean 4 core only: NO mathlib dependency, so `lake build` finishes in
seconds and any Lean 4 v4.31.0 toolchain can check the proofs.
-/
package «collatz-atlas-formal» where

@[default_target]
lean_lib «Formal» where
  -- Library root: `Formal.lean`; modules under `Formal/`.
  globs := #[.andSubmodules `Formal]
