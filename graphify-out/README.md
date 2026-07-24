# Agent map — accuracy notes

Audited 2026-07-24. The graph is a **navigation aid, not an evidence
tier**. Read this before handing `graph.html` or `GRAPH_REPORT.md` to
another agent.

## The graph does not separate evidence tiers — this is the important one

The repository's whole claim discipline is the split between
`contribution/` (evidence), `exploratory/` (drafts, explicitly *not* cited
as results), and `quarantine/` (**not evidence** — untrusted, disproven, or
high-risk). **The graph flattens all three.** Indexed file counts:

| Tier | Files in graph | Repo status |
|---|---|---|
| `contribution/` | 103 | evidence |
| `exploratory/` | 11 | *not cited as results* |
| `quarantine/` | 1 | **not evidence** |
| `formal/` | 2 | evidence (but see below) |

The consequence is concrete and not hypothetical: the report's **"God Nodes
(most connected — your core abstractions)"** list ranks
`Elements of Collatz — A Euclid-Style Research Spine` at **#2, above the
repository README**, and `Book VIII — Collatz as Language` at #6. Both are
`exploratory/` drafts that the repo explicitly does not cite. An agent
navigating by connectivity will land on non-evidence first.

Until the map is tier-aware, treat every node as unranked and check which
directory a file lives in before using it.

## The freshness line is wrong

`GRAPH_REPORT.md` says:

> Built from commit: `04efaa25` … Run `git rev-parse HEAD` and compare to
> check if the graph is stale.

That protocol does not work here. The manifest **contains files added in
`eb81928`**, which is a *later* commit than `04efaa25` — the
cycle-exclusion-extension packet (4 files), `formal/README.md`, and
`formal/lake-manifest.json`. So the graph was rebuilt after `04efaa25`
without the freshness line being updated, and comparing that hash to HEAD
tells you nothing reliable.

## Three file counts disagree

| Source | Count |
|---|---|
| `cost.json` → `runs[0].files` | 103 |
| `GRAPH_REPORT.md` → Corpus Check | 112 |
| `manifest.json` keys | 120 |

`cost.json` was not rewritten on the rebuild: both it and
`2026-07-23/cost.json` carry the identical timestamp
`2026-07-23T08:09:38`, while their sibling manifests differ (120 vs 114
entries). Only `manifest.json` reflects what was actually indexed.

## The Lean certificates are absent

`formal/` contributes exactly two files to the graph — `README.md` and
`lake-manifest.json`. **Zero `.lean` files are indexed**, so none of
`Formal.lean`, `TerrasBijection.lean`, `TwoBranchFamily.lean`, or
`Pigeonhole.lean` appear. The repository's only externally rejectable
artifact — the zero-sorry certificates targeted at
`google-deepmind/formal-conjectures` — is invisible in the map that is
meant to be shared.

`MOTIVATION.md` is also missing (added in `d89960a`, after the last build).

## What the graph does get right

- It does **not** assert mathematical claims of its own. Community labels
  and hub names are document titles echoed verbatim, so the map carries no
  independent stale results — the audit exposure is structural, not
  factual.
- It records a build commit at all, and tells the reader to compare it.
  The mechanism is sound; only this instance's value is wrong.
- Extraction is deterministic (`0 input · 0 output` tokens, AST plus
  markdown structure), so the map is reproducible and costs nothing to
  rebuild.

## Rebuild

```bash
graphify update .
```

After rebuilding, re-check the four items above; none of them are fixed by
the rebuild alone except the file counts and the missing `MOTIVATION.md`.
