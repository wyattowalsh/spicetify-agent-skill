# DESIGN.md — `/spicetify` implementation design

**Path:** `DESIGN.md`
**Purpose:** Root-level design narrative tying the `/spicetify` skill, local Python runtime, OpenSpec artifacts, and accompanying Fumadocs + shadcn/ui site into one coherent implementation.
**Status:** Implemented baseline for v0.1.0
**Load/use when:** A reviewer or coding agent needs the shortest design-first orientation before reading deeper OpenSpec and planning docs.

## Design thesis

`/spicetify` is a local, transactional, plan-first Spicetify operator. It wraps Spicetify as a semantic workflow engine, not as a generic terminal. The system MUST keep planning, policy, execution, verification, reporting, and rollback separate so every mutation can be explained, approved, verified, and reversed.

The accompanying Fumadocs site is the operator's durable knowledge surface. It turns the OpenSpec artifacts into browsable docs for users, implementers, auditors, and future coding agents. The site is a first-class deliverable, but it remains documentation and local tooling: it MUST NOT become a bypass around `/spicetify` runtime safety gates.

## System boundaries

| Boundary | Inside | Outside unless explicitly approved |
|---|---|---|
| Runtime skill | `/spicetify` router, modes, schemas, policy, snapshots, command registry, fake fixtures | real Spotify mutation in CI, arbitrary shell, package installs, permission changes |
| Local state | Spicetify config/assets, skill-owned snapshots/reports/provenance locks | secrets, Spotify credentials, prefs contents by default, unrelated user files |
| Third-party code | staged, hashed, audited themes/extensions/snippets/custom apps | executing installer scripts, trusting Marketplace/GitHub by default |
| Docs site | Fumadocs content, MDX guides, shadcn/ui components, search, LLM text routes, examples | deployment, analytics, external search credentials, remote registry installs without approval |

## Primary architecture

```text
/spicetify prompt
  -> mode router
  -> read-only probes
  -> typed dry-run plan
  -> policy + invariant checks
  -> snapshot manager
  -> allowlisted command/file transaction runner
  -> verifier
  -> rollback manager
  -> redacted report

OpenSpec artifacts
  -> Fumadocs content source
  -> generated/curated MDX guides
  -> shadcn-themed docs UI
  -> search and LLM-readable routes
```

## Runtime design decisions

- Use a typed, packageable Python runtime under `skills/spicetify/scripts/` for schemas, filesystem transactions, process spawning, static JS/CSS auditing, and local CLI UX.
- Expose the installable console command as `spicetify-agent`; keep `/spicetify` as the user-facing skill name so the real `spicetify` CLI is never shadowed.
- Support `pip install .`, `uv run spicetify-agent`, `uvx --from . spicetify-agent`, and the tagged `v0.1.0` helper install path as release execution shapes.
- Use `shell: false` process execution and an allowlisted Spicetify command registry.
- Prefer Spicetify CLI config edits; use direct INI edits only when a precise state cannot be represented through CLI commands.
- Treat Spicetify backup and `/spicetify` snapshots as separate state systems.
- Treat Creator as compatibility-only; default scaffolds use maintained local templates.
- Keep every operation report machine-readable and human-readable.

## Docs-site design decisions

- Use Fumadocs-compatible content with a Next app-router app as the documentation shell.
- Use shadcn/ui-compatible local components and design tokens while keeping registry installs approval-gated.
- Keep docs chrome aligned with the same local theme tokens as shadcn-compatible components.
- Keep the docs site in an `docs` workspace package so it can be built, tested, and deployed independently from the local operator.
- Store user-facing content under `docs/content/docs` and reusable UI under `docs/components`.
- Generate or synchronize reference pages from schemas, OpenSpec specs, and planning mode docs, but keep generated files marked and reviewable.
- Provide local search, `llms.txt`, and `llms-full.txt` plans without requiring hosted credentials.
- Defer hosted analytics, cloud search, feedback backends, and deployment until explicitly approved.

## Read next

1. `openspec/changes/add-spicetify-skill/design.md`
2. `docs/content/docs/archive/add-spicetify-skill/fumadocs-site-plan.mdx`
3. `docs/content/docs/archive/add-spicetify-skill/docs-content-architecture.mdx`
4. `docs/content/docs/archive/add-spicetify-skill/docs-site-implementation-plan.mdx`
5. `openspec/changes/add-spicetify-skill/specs/docs-site/spec.md`
6. `openspec/changes/add-spicetify-skill/specs/docs-content/spec.md`
7. `openspec/changes/add-spicetify-skill/specs/docs-ui/spec.md`

## Subagent execution design

The implementation plan includes a bounded Codex swarm path, but the swarm is a coordination optimization rather than a safety boundary. `subagent-task-graph.md` defines the agent roster, write scopes, dependencies, result envelope, merge protocol, and sequential fallback. `codex-kickoff-prompt.md` is the copyable entry point for Codex.

Subagents are appropriate for independent contracts, command/policy/state, audit/provenance/privacy, platform/repair fixtures, docs-site work, validation, and red-team review. They are not appropriate for overlapping writes, authority expansion, package installation, deployment, real Spotify/Spicetify mutation, or hidden network access. The orchestrator remains responsible for consolidating results and updating `PLANS.md` before claiming completion.
