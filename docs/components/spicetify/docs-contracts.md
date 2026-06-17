# /spicetify Docs Components Contract

**Path:** `docs/components/spicetify/docs-contracts.md`
**Purpose:** Local component behavior contract for the future Fumadocs + shadcn/ui implementation.
**Status:** Proposed

These component contracts are local design notes. They are not copied from an
external registry and do not require package installation.

| Component | Purpose | Safety rule |
|---|---|---|
| `RiskBadge` | Render read, low, medium, high, and blocked risk states. | Include text labels, not color alone. |
| `ModeCard` | Summarize a mode purpose, risk, preconditions, plan shape, and rollback support. | Link to source mode docs. |
| `OperationTimeline` | Show dry-run, policy, snapshot, confirmation, execution, verification, and rollback. | Never imply mutation happens during docs preview. |
| `CommandPlan` | Display allowlisted argv arrays as structured data. | Do not render arbitrary shell as recommended commands. |
| `SchemaViewer` | Summarize required fields, enums, examples, and source paths. | Mark generated data with source and validation status. |
| `RecoveryCallout` | Map failure modes to safe next actions. | Manual-only actions stay manual-only. |
| `ProvenancePanel` | Show source type, ref, hash, and audit verdict. | Third-party sources remain untrusted until audited. |
