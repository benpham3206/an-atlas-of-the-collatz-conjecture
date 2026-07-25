# meta/ — strategy research, not proofwork

Everything here studies **how to attack the problem**, not the problem. No
result in this directory is evidence for a mathematical claim. Nothing here
may be cited by a `contribution/` packet as support for a theorem.

That separation is the point. The repository already learned once that a
framework can look like progress while proving nothing.

| File | What it holds |
|---|---|
| [`LEDGER.md`](LEDGER.md) | Per-session record: strategy used, what worked, what failed, mistakes, lessons. The flywheel's memory. |
| [`SIMPLE_QUESTIONS.md`](SIMPLE_QUESTIONS.md) | Small, exactly-answerable questions, starting with "why does it cycle back to 4-2-1". |
| [`AGENT_CONDUCT.md`](AGENT_CONDUCT.md) | How an agent should behave here. Read before working. |
| [`READING.md`](READING.md) | External reading, with honest verdicts on what transfers. |
| [`TRANSFER_AUDITS.md`](TRANSFER_AUDITS.md) | Assessments of outside methods proposed for Collatz. Mostly negative, deliberately kept. |

## Why a meta directory at all

Three of the four highest-cost mistakes in this project's history were
strategic, not mathematical:

1. spending a session extending a search already dominated by the literature
   by eleven orders of magnitude;
2. extrapolating through a quantity that was a sawtooth, producing a
   meaningless "falsified prediction";
3. building an elaborate framework whose own novelty gate it then failed.

None of those was caught by a verifier. All three would have been caught by a
five-minute strategy check. That check is what this directory is for.

## The standing rule

> A framework is not progress. A framework that has not deleted a route, or
> produced a number, has not earned its directory.

Anything here that goes three sessions without either killing a route or
feeding a `contribution/` packet gets moved to `exploratory/` or deleted.
