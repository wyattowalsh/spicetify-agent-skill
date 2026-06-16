# Schema notes

**Path:** `docs/planning/add-spicetify-skill/schemas/README.md`
**Purpose:** Human guide to structured schemas in the bundle.
**Status:** Proposed
**Load/use when:** Use when implementing request, plan, policy, provenance, verification, run, report, and fixture validation.

## Contract graph

```text
request
  -> policy-decision
  -> operation-plan
       -> confirmation
       -> command-invocation
       -> policy-decision
       -> provenance-lock refs
       -> verification steps
  -> operation-run
       -> verification-report
  -> operation-report
       -> operation-run
       -> verification-report
       -> audit-report findings

command-registry
  -> command-invocation allowlist

snapshot-manifest
  -> restore / rollback / last-known-good

profile
  -> provenance-lock refs
  -> operation-plan diff

fixture-manifest
  -> fake Spicetify integration tests

eval-suite
  -> eval-case
  -> eval-result
       -> eval-trace refs
       -> evolution-report refs
```

## Required schema files

| Schema | Purpose |
|---|---|
| `request.schema.json` | User/API request envelope; always dry-run-first. |
| `operation-plan.schema.json` | Typed dry-run plan with mutations, commands, verifications, rollback, policy decision, provenance refs, idempotency key, and plan hash. |
| `command-registry.schema.json` | Registry entry for all allowlisted Spicetify command shapes. |
| `command-invocation.schema.json` | Concrete argv invocation; `shell` is always `false`. |
| `policy.schema.json` | Declarative policy rule shape. |
| `policy-decision.schema.json` | Per-plan allow/confirm/manual/block decision evidence. |
| `provenance-lock.schema.json` | Locked source refs, hashes, audit verdicts, and accepted risks. |
| `audit-report.schema.json` | Static audit output for themes, extensions, custom apps, snippets, Marketplace repos, and prompt-injection text. |
| `snapshot-manifest.schema.json` | Immutable snapshot manifest with redaction/exclusion metadata. |
| `profile.schema.json` | Exact-state profile manifest. |
| `verification-report.schema.json` | Post-execution evidence and pass/fail state. |
| `operation-run.schema.json` | Actual execution log for an approved plan. |
| `operation-report.schema.json` | User-facing JSON/Markdown operation report source. |
| `error.schema.json` | Normalized error taxonomy. |
| `fixture-manifest.schema.json` | Fake Spicetify environment and expected findings. |
| `eval-case.schema.json` | Deterministic skill eval case with activation, fixture, oracle, trace, report, and artifact expectations. |
| `eval-suite.schema.json` | Versioned local eval suite with offline runner requirements and mode coverage. |
| `eval-result.schema.json` | Schema-shaped runner output with summary, case results, grader results, and artifacts. |
| `eval-trace.schema.json` | Redacted local trace contract for routing, policy, commands, fake observations, and report output. |
| `evolution-report.schema.json` | Ranked eval-driven improvement proposal contract for `evolve`. |

## Implementation requirements

- Validate every emitted JSON object in tests.
- Treat schema failures as implementation defects, not user errors.
- Keep schemas strict enough to reject accidental broad mutations, but extensible enough for mode-specific `inputs` and report evidence.
- Any schema extension that enables new mutation, command, network, DevTools, package-manager, or filesystem behavior must update `policy-matrix.md`, `traceability.md`, and regression prompts.


## Added schema contracts

| Schema | Purpose |
|---|---|
| `schemas/desired-state-manifest.schema.json` | Declarative manifest import/export and replay. |
| `schemas/asset-manifest.schema.json` | Asset trust, ownership, file hashes, and install state. |
| `schemas/redaction-policy.schema.json` | Report shareability and sensitive-value handling. |
| `schemas/consent-grant.schema.json` | Bounded approval for logs, screenshots, launch flags, source archives, network staging, and build scripts. |

## Docs-site schemas

| Schema | Purpose |
|---|---|
| `schemas/docs-site-manifest.schema.json` | Validates the planned Fumadocs app root, routes, content sources, UI policy, validation, and safety gates. |
| `schemas/docs-page.schema.json` | Validates docs frontmatter and generated-page metadata. |

## Docs-site schemas

- `schemas/docs-site-manifest.schema.json` — validates the docs-site package/source/content outputs planned for the Fumadocs site.
- `schemas/docs-page.schema.json` — validates page metadata, source traceability, and safety labels.
- `schemas/docs-site-config.schema.json` — validates planned Fumadocs + shadcn/ui site configuration, content sections, custom components, and validation gates.
- `schemas/docs-site-content.schema.json` — validates documentation information architecture, required mode pages, workflow pages, schema pages, and redaction policy for examples.

## Subagent schemas

- `schemas/subagent-task-graph.schema.json` validates the Codex swarm DAG, including agents, waves, merge protocol, and fallback.
- `schemas/subagent-result.schema.json` validates each subagent result envelope before orchestrator consolidation.
