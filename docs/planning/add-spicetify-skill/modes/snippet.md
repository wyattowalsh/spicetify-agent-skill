# Mode: snippet

**Path:** `docs/planning/add-spicetify-skill/modes/snippet.md`
**Purpose:** Detailed contract for `/spicetify snippet` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `snippet` behavior.

## Purpose

Create, audit, install, group, enable, disable, or migrate CSS snippets.

## Inputs

CSS text/source, snippet name, target profile/theme, source provenance.

## Preconditions

CSS parses; install strategy selected.

## Commands/files touched

Skill-managed CSS overlay or theme/snippet file; optional profile manifest; apply/update.

## Safety checks

Block remote imports/URLs by default; no Marketplace internal writes unless discovered and approved.

## Plan output

`SnippetPlan` with CSS hash, target overlay, profile association, rollback block ID.

## Execution flow

Parse/audit CSS → stage overlay block → snapshot → write → apply/update.

## Verification flow

Overlay contains snippet hash; target profile/theme references it; UI checks optional.

## Rollback flow

Remove snippet block by ID or restore overlay snapshot.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Remote import or unsafe overlay -> block or require explicit risk acceptance.
- Snippet removal mismatch -> restore overlay snapshot.


## Data contracts

Primary contracts: `asset-manifest, audit-report, operation-plan`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify add a snippet to compact the sidebar`

## Example structured response

```json
{
  "mode": "snippet",
  "snippet": "compact-sidebar",
  "risk": "medium",
  "installStrategy": "skill-overlay"
}
```
