# Quarantine

Untrusted, disproven, or high-risk material that agents must **not** treat as
positive evidence for Collatz results.

## Policy

| Bucket | Use for | Do not use for |
|---|---|---|
| [`../contribution/`](../contribution/) | proofs, verifiers, and reports with explicit evidentiary status | speculative drafts |
| [`../exploratory/`](../exploratory/) | terminology and reformulation drafts not cited as results | claimed proofs or counterexamples |
| **this folder** | failed attacks, untrusted model write-ups, circular arguments, and material under adversarial hold | anything agents should cite as established |

Anything here may be wrong, incomplete, or actively misleading. Prefer
`contribution/` and `COLLATZ_ONE_PAGE.md` for handoffs.

## Contents

This directory starts empty except for this policy file. Drop quarantined
artifacts as siblings or in dated subfolders, and keep a one-line status at
the top of each file:

```
Status: quarantine — not evidence; reason: <one line>
```
