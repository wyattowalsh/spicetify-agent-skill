# Fumadocs site plan

**Path:** `docs/planning/add-spicetify-skill/fumadocs-site-plan.md`
**Purpose:** Complete plan for the accompanying Fumadocs documentation site with shadcn/ui customization.
**Status:** Proposed
**Load/use when:** Planning, implementing, or auditing the public/local documentation site for `/spicetify`.

## Mission

Create a full documentation site that makes `/spicetify` understandable, auditable, and implementable without pasting the whole planning bundle into an agent prompt. The site should serve four audiences:

| Audience | Needs |
|---|---|
| Novice power user | Safe quickstarts, mode explanations, confirmation language, rollback confidence. |
| Spicetify power user | Profile/manifest automation, audit output, dry-run diffs, repair recipes. |
| Implementer | OpenSpec map, schemas, task graph, fake fixtures, runtime contracts. |
| Security reviewer | Threat model, policy matrix, provenance, privacy/redaction, blocked actions. |

## Site deliverable

Recommended package path:

```text
apps/docs/
  app/
    layout.tsx
    page.tsx
    docs/[[...slug]]/page.tsx
    docs/layout.tsx
    llms.txt/route.ts
    llms-full.txt/route.ts
    api/search/route.ts
  content/docs/
    index.mdx
    quickstart.mdx
    concepts/
    modes/
    workflows/
    schemas/
    security/
    development/
    docs-site/
  components/
    mdx.tsx
    search.tsx
    docs/
    spicetify/
    ui/
  lib/
    source.ts
    get-llm-text.ts
    site-map.ts
  scripts/
    sync-openspec-content.ts
    validate-docs-content.ts
  source.config.ts
  next.config.mjs
  components.json
  package.json
```

The package is planned, not created by this bundle. Any package-manager command remains approval-gated in the target repo.

## Framework and content decisions

| Decision | Rationale | Revisit trigger |
|---|---|---|
| Fumadocs + Next app router | Fumadocs is a React docs framework with first-class Next support, MDX content, docs layouts, search, and customization hooks. | Existing repo is not Next-based or requires a different app shell. |
| Fumadocs MDX content source | It turns docs collections into type-safe data and preserves local content review. | The repo wants runtime-only Markdown loading instead of build-time processing. |
| shadcn/ui components | Components are local code, customizable, and aligned with the user's preference for shadcn-style design systems. | The repo already has a conflicting design system. |
| Fumadocs shadcn preset | It lets Fumadocs UI adopt shadcn theme colors and tokens. | Fumadocs theme mechanics change or the site uses a different CSS architecture. |
| Local search by default | Avoids external credentials while keeping docs searchable. | Hosted docs require a managed search provider and the user approves credentials. |
| LLM-readable routes | Improves agent consumption of docs without context dumps. | The site is private and AI-readable exports are not desired. |

## Information architecture

```text
/
  Landing page: value proposition, safety invariants, primary calls to action.
/docs
  Overview
  Quickstart
  Installation and trust model
  Concepts
    Dry-run planning
    Snapshots and rollback
    Policy and confirmations
    Provenance and audits
    Desired-state manifests
  Modes
    inspect, doctor, snapshot, restore, repair, apply, config, profile, theme,
    extension, custom-app, snippet, marketplace, audit, devtools, watch,
    migrate, update, rollback, uninstall, report
  Workflows
    Spotify updated repair
    Create a terminal theme
    Install a GitHub theme safely
    Audit an extension
    Switch profiles
    Scaffold extension/custom app
    Roll back last-known-good
  Security
    Threat model
    Blocked actions
    DevTools and logs
    Privacy and redaction
    Third-party code audit
  Reference
    CLI command registry
    Schemas
    Error taxonomy
    Operation states
    OpenSpec traceability
  Development
    Runtime architecture
    Fake Spicetify fixtures
    Testing strategy
    Codex handoff
  Docs site
    Content model
    Design system
    Component inventory
    Validation
```

## Content generation model

Use a hybrid model:

- Curated pages for overview, quickstart, UX, safety, and tutorials.
- Generated-reference pages from JSON schemas, mode docs, and OpenSpec requirements.
- Generated pages MUST include a source pointer and regeneration note.
- Generated pages MUST be reviewable in diffs and should never be silently published.
- `sync-openspec-content.ts` reads local files only and writes only under `apps/docs/content/docs/generated/` unless explicitly approved.

## shadcn/ui component plan

| Component group | Planned local components | Purpose |
|---|---|---|
| Core UI | button, badge, card, alert, table, tabs, accordion, dialog, sheet, tooltip, command, separator, scroll-area | Build docs surfaces with consistent styling. |
| `/spicetify` domain UI | `ModeCard`, `RiskBadge`, `PolicyDecision`, `PlanDiff`, `CommandInvocation`, `SnapshotTimeline`, `AuditFinding`, `RecoveryRecipe`, `SchemaViewer` | Explain structured plans and runtime outputs. |
| Docs chrome | `Hero`, `FeatureGrid`, `SafetyCallout`, `WorkflowStepper`, `ExamplePrompt`, `ReportPreview` | Make docs useful without overwhelming novices. |
| Generated references | `SchemaFieldTable`, `RequirementTrace`, `TaskWave`, `ErrorCodeTable` | Render machine-readable bundle content as navigable docs. |

Use local shadcn components only. External shadcn registries are third-party code and remain approval-gated like any other source registry.

## Visual system

- Default theme: dark-capable terminal-adjacent design, calm contrast, high readability.
- Color tokens: rely on shadcn theme variables and Fumadocs shadcn preset.
- Layout: Fumadocs docs layout for documentation pages, custom landing page for the root.
- Accessibility: keyboard navigation, visible focus, sufficient contrast, semantic headings, reduced-motion-friendly diagrams.
- Diagrams: prefer text/MDX diagrams and simple cards over heavy client-side visualization.

## Routes and integrations

| Route | Purpose | Notes |
|---|---|---|
| `/` | Landing page | Static marketing/product overview; no analytics by default. |
| `/docs/[[...slug]]` | Main docs pages | Fumadocs source-backed route. |
| `/api/search` | Local search endpoint | Uses Fumadocs/Orama plan by default. |
| `/llms.txt` | Index for AI readers | Generated from the page tree. |
| `/llms-full.txt` | Full AI-readable docs | Redaction-reviewed; no secrets or private local paths. |
| `/openapi` or `/docs/reference/api` | Optional API reference | Deferred until runtime API is stable. |

## Documentation safety rules

- Docs can show proposed commands but MUST mark package-manager, install, deployment, and external registry commands as approval-gated.
- Docs MUST NOT include real user paths, tokens, Spotify prefs contents, screenshots with private data, or unredacted DevTools logs.
- Generated examples MUST use fake paths and fake outputs unless explicitly labeled as local user output.
- Docs MUST NOT imply `/spicetify` can bypass Spicetify/Spotify limitations or unsupported update windows.
- Docs MUST preserve the exact user-facing skill name `/spicetify`.

## MVP docs site cutline

Build first:

1. docs shell and content source,
2. Fumadocs layout and shadcn theme integration,
3. overview, quickstart, safety model, and mode catalog,
4. schema and command reference generated from local bundle files,
5. local search,
6. LLM-readable routes,
7. docs validation script,
8. accessibility and link checks.

Defer:

- hosted deployment,
- analytics,
- feedback backend,
- external search credentials,
- OpenAPI auto-generation,
- live screenshots,
- remote registry packaging,
- public documentation publishing.

## Validation

Proposed target-repo checks:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs test
pnpm --filter docs build
pnpm --filter docs validate:content
python tools/validate_bundle.py --root .
openspec validate add-spicetify-skill --strict
```

If the target repo uses a different package manager, preserve it unless the user approves migration.
