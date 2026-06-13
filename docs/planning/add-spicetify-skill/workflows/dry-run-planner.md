# Dry-run planner

**Path:** `docs/planning/add-spicetify-skill/workflows/dry-run-planner.md`
**Purpose:** Explains every mutation before applying it.
**Status:** Draft
**Load/use when:** Read when implementing this cross-cutting workflow.


## Plan stages

1. Intent and mode classification.
2. Read-only probes.
3. Preconditions.
4. Diff calculation.
5. Risk classification.
6. Snapshot requirement.
7. Command/file mutation list.
8. Verification list.
9. Rollback plan.
10. Human confirmation token for medium/high risk.

## OperationPlan invariants

- Contains no raw shell.
- Contains all mutations.
- Contains plan hash.
- Contains explicit rollback.
- Contains verification checks.
- Is invalidated by source drift before execution.
