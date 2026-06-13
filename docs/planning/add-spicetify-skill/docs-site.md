# Companion docs site plan

**Path:** `docs/planning/add-spicetify-skill/docs-site.md`
**Purpose:** Full plan for an accompanying configured and customized Fumadocs site using shadcn/ui.
**Status:** Proposed
**Load/use when:** Planning, implementing, auditing, or handing off the documentation site.

## Objective

Create a polished documentation site for `/spicetify` that teaches safe usage, documents every mode, exposes schemas and examples, and gives implementation agents a public-quality reference surface. The site uses Fumadocs for docs architecture and shadcn/ui for customized UI primitives and product-specific components.

## Product role

The docs site serves four audiences:

| Audience | Job |
|---|---|
| Novice user | Learn what `/spicetify` can do, how dry-run planning works, and how to avoid damaging local Spotify state. |
| Power user | Understand profiles, manifests, audit reports, repair flows, and automation boundaries. |
| Contributor | Read architecture, mode contracts, schemas, fake environment strategy, and test requirements. |
| Auditor | Review safety model, policy matrix, privacy/redaction model, provenance, and failure recovery behavior. |

## Recommended stack

| Layer | Recommendation | Notes |
|---|---|---|
| Framework | Next.js App Router | Use only after target repo conventions are checked. |
| Docs framework | Fumadocs MDX and Fumadocs UI | Use `source.config.ts`, `lib/source.ts`, and `content/docs`. |
| UI primitives | shadcn/ui | Copy components into repo, customize through tokens, and review third-party registry sources. |
| Package manager | Preserve detected package manager; use pnpm only for new repos | Commands remain proposals until approved. |
| Styling | Tailwind CSS plus CSS variables | Dark terminal-style theme should align with `/spicetify` examples. |
| Icons | lucide-react via shadcn defaults | Avoid custom icon packages unless approved. |
| Testing | typecheck, lint, build, MDX compile, link check, accessibility checks | Use synthetic fixtures only. |

## Proposed repo layout

```text
apps/docs/
  app/
    layout.tsx
    page.tsx
    docs/[[...slug]]/page.tsx
    api/search/route.ts                  # optional, if target deployment supports it
  content/docs/
    index.mdx
    getting-started/
    concepts/
    modes/
    workflows/
    safety/
    schemas/
    troubleshooting/
    contributing/
  components.json                         # shadcn/ui config for this workspace
  components/
    ui/                                   # shadcn/ui copied primitives
    docs/
      risk-badge.tsx
      mode-card.tsx
      operation-timeline.tsx
      command-plan.tsx
      schema-viewer.tsx
      recovery-callout.tsx
      provenance-panel.tsx
      platform-note.tsx
      report-preview.tsx
  lib/
    source.ts
    docs-map.ts
    examples.ts
  source.config.ts
  next.config.mjs
  package.json
```

If the target repo is not a monorepo, place equivalent paths at the repo root. Preserve existing conventions unless migration is explicitly approved.

## Fumadocs configuration plan

- Use `source.config.ts` to define docs collections under `content/docs`.
- Use `next.config.mjs` so Fumadocs MDX ESM behavior is handled cleanly.
- Use `lib/source.ts` to load the docs collection and set the docs base URL.
- Keep generated `.source` output out of hand-edited docs and cache commits unless the target repo intentionally tracks generated artifacts.
- Put human-authored docs in MDX files; generate reference pages from schemas only through explicit scripts that are deterministic and reviewable.

## shadcn/ui customization plan

### Component baseline

Add only the components the docs actually need:

- `button`
- `badge`
- `card`
- `tabs`
- `accordion`
- `alert`
- `table`
- `separator`
- `tooltip`
- `dialog`
- `scroll-area`
- `command`
- `textarea`
- `input`

Each added component is copied source and should be reviewed like repo code. Third-party registry components are not automatically trusted.

### Design tokens

Use a dark terminal-inspired palette that mirrors the sample Spicetify theme without implying the site is Spotify itself.

| Token role | Intent |
|---|---|
| background | near-black documentation canvas |
| foreground | high-contrast terminal text |
| muted | command output and secondary explanations |
| primary | safe action emphasis |
| warning | approval-gated or risky actions |
| destructive | blocked/destructive operation labels |
| border | subtle terminal panel outlines |
| code | monospace command/schema snippets |

### Custom docs components

| Component | Purpose |
|---|---|
| `RiskBadge` | Render `read`, `low`, `medium`, `high`, and `blocked` risk levels. |
| `ModeCard` | Link to mode docs with inputs, safety, and rollback summary. |
| `OperationTimeline` | Explain dry-run → snapshot → confirm → execute → verify → rollback. |
| `CommandPlan` | Show allowlisted argv arrays without encouraging raw shell. |
| `SchemaViewer` | Render schema summaries and validation examples. |
| `RecoveryCallout` | Map an error code to safe next actions. |
| `ProvenancePanel` | Explain source, hash, audit verdict, and accepted risk. |
| `PlatformNote` | Display Windows/Linux/macOS package caveats. |
| `ReportPreview` | Show redacted operation reports using synthetic data. |

## Information architecture

See `docs-site-content-map.md` for the full page tree. Required top-level groups:

1. Start
2. Core concepts
3. Modes
4. Workflows
5. Safety and privacy
6. Profiles and manifests
7. Developer workflows
8. Troubleshooting and repair
9. Schemas and reports
10. Contributor guide

## Content generation policy

- Source docs from OpenSpec and planning artifacts only through deterministic scripts.
- Generated pages must include a source-path footer or frontmatter field.
- Human-authored pages should prefer examples and explanations over duplicated spec text.
- Never publish real local paths, logs, screenshots, tokens, prefs contents, or user snapshots.
- All examples use synthetic names and synthetic reports.

## Search and navigation

- Provide search over documentation content.
- Sidebar groups mirror progressive disclosure: quick start before safety deep dives; mode catalog before individual mode details.
- Every mode page links to: relevant workflow, schema, safety rule, failure recovery entry, and example prompt.
- Every risky operation page includes a blocked/high-risk explanation and confirmation requirements.

## Implementation sequence

1. Confirm target repo layout and package manager.
2. Add docs-site OpenSpec domain and docs-site schema contracts.
3. Scaffold Fumadocs in the approved path.
4. Configure shadcn/ui in the docs workspace.
5. Add custom docs components.
6. Add content map and first pages.
7. Add schema/reference rendering pipeline.
8. Add docs validation commands.
9. Add accessibility and link checks.
10. Document deployment as a proposal only.

## Validation

Proposed target-repo checks:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs build
pnpm --filter docs test
```

Equivalent commands should be substituted when the target repo uses another package manager or workspace layout.

## Stop conditions

Stop before implementation if:

- target repo already has a docs framework and migration is not approved;
- package manager is unclear;
- installing dependencies is not approved;
- shadcn/ui registry access would require network and no approval was granted;
- Fumadocs build constraints conflict with target deployment;
- generated examples might leak real local paths, logs, screenshots, or tokens.

## Relationship to deeper docs

This file is the compact docs-site overview. Use these files for deeper implementation detail:

- `fumadocs-site-plan.md` — full site mission, route plan, content model, search, AI-readable routes, and cutline.
- `docs-content-architecture.md` — frontmatter, generated-reference pipeline, navigation, editorial workflow, and LLM-readable docs model.
- `docs-site-design-system.md` — shadcn/ui component inventory, risk variants, custom docs components, and accessibility.
- `docs-site-implementation-plan.md` — implementation waves, done criteria, and stop conditions.
- `workflows/fumadocs-site.md` — operational workflow for implementation and rollback.
