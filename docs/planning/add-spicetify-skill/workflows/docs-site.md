# Workflow: companion docs site

**Path:** `docs/planning/add-spicetify-skill/workflows/docs-site.md`
**Purpose:** Compact router for companion docs-site implementation guidance.
**Status:** Proposed
**Load/use when:** A task references docs-site workflow but the implementation should use the canonical Fumadocs workflow.

## Canonical workflow

Use `workflows/fumadocs-site.md` for the full workflow. This file exists as a semantic alias for readers who search for “docs-site”.

## Guardrails

- Confirm target repo package manager and docs root before implementation.
- Do not install packages or access shadcn registries without approval.
- Do not embed real local paths, logs, screenshots, prefs contents, snapshots, or tokens.
- Keep generated reference pages deterministic and source-linked.
- Roll back only under the approved docs-site root and reviewed package metadata changes.
