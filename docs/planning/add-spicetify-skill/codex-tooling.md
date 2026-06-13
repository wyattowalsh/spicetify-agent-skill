# Codex tooling notes

**Path:** `docs/planning/add-spicetify-skill/codex-tooling.md`
**Purpose:** Safe proposal surface for Codex config, hooks, MCP, Skills, plugins, and subagents.
**Status:** Proposed
**Load/use when:** Deciding whether to add tooling beyond docs/Skill.

## Recommendation

Keep tooling minimal for MVP:

- Use the `/spicetify` Skill plus local CLI implementation.
- Do not add MCP, hooks, or project-local Codex config until a real trusted repo exists.
- Add deterministic validation scripts first; consider hooks only after they are reviewed and non-mutating.
- Package as a plugin only if the skill must be distributed across projects.

## Decision table

| Surface | Use when | Do not use when | Approval needed |
|---|---|---|---|
| `AGENTS.md` | Durable repo rules | Task details only | No for docs-only. |
| Skill | Recurring `/spicetify` workflow | One-off prompt | Yes before installing into a shared environment. |
| Hooks | Deterministic local validation | Hidden mutation, telemetry, network | Yes. |
| MCP | Repeated live context loop not representable as docs | Nice-to-have context | Yes. |
| Plugin | Distribution of Skill + tooling | Local planning only | Yes. |
| Subagents | Independent review/test slices | Overlapping write scope | Yes for write work. |

## Proposed subagents for implementation review

| Agent | Objective | Read scope | Write scope | Expected output | Stop condition |
|---|---|---|---|---|---|
| Safety reviewer | Review policy/command/snapshot invariants | specs, design, policy docs, tests | none | findings + patches | hidden shell or mutation path |
| Platform reviewer | Review Windows/Linux/macOS packaging cases | platform docs, doctor tests | none | platform matrix gaps | package commands needed |
| Audit reviewer | Review JS/CSS/manifest audit rules | audit docs, fixtures | none | false negative/positive report | third-party execution needed |
| UX reviewer | Review novice/power-user flows | UX docs, examples | none | wording/confirmation fixes | confirmation ambiguity |

## Approval checklist

- [ ] Repo is trusted.
- [ ] No secrets are embedded.
- [ ] Tooling removes a real repeated loop or improves safety.
- [ ] Permissions are least-privilege.
- [ ] Network behavior is explicit.
- [ ] Disable/rollback path is documented.
- [ ] Human approval obtained before adding config, hooks, MCP, plugin package, or write-capable subagents.

## Docs-site tooling proposal

For the docs app, proposed tooling remains minimal:

| Tooling | Use | Approval |
|---|---|---|
| package scripts | docs lint/typecheck/test/build/content validation | package install approval needed first |
| content sync script | deterministic local generation from OpenSpec/schemas/mode docs | allowed after review; writes only generated docs directory |
| link/a11y checks | quality gate for docs | allowed if dependency is already available or install is approved |
| deployment config | only when publishing is in scope | explicit approval required |
| external registries | shadcn registry or remote templates | explicit approval and provenance review required |

## Docs-site tooling note

Fumadocs and shadcn/ui setup commands are proposals only. A target repo may use pnpm, npm, yarn, or bun; preserve detected conventions. shadcn/ui registry access is network/tool expansion and requires approval. Any docs-site hook must be deterministic, local, and limited to build/lint/link/redaction checks.

## Subagent swarm recommendation

Use Codex subagents only when the target repo has been grounded and the assigned slices have non-overlapping write scopes. The canonical graph is `subagent-task-graph.md`; the copyable launch text is `codex-kickoff-prompt.md`.

| Agent | Objective | Read scope | Write scope | Expected output | Stop condition |
|---|---|---|---|---|---|
| A0 repository-preflight | Detect repo conventions and write scopes. | repo tree, package files, OpenSpec config, AGENTS | `context-map.md`, `PLANS.md` | evidence map and commands | assumptions contradicted |
| A1 contracts-and-schemas | Implement typed contracts. | schemas and specs | schema/test paths | schema patch and fixtures | incompatible contract change |
| A2 command-policy-state | Implement command registry, policy, state. | command/policy/state docs | core command/policy/state paths | guarded runtime core | raw shell or real Spicetify needed |
| A3 audit-provenance-security | Implement audit/provenance/privacy. | threat/audit/provenance/privacy docs | audit/provenance/privacy paths | audit and redaction tests | third-party execution needed |
| A4 platform-repair-fixtures | Implement platform/recovery fixtures. | platform and recovery docs | platform/recovery/fixture paths | fake env and recovery tests | package/permission automation needed |
| A5 modes-and-runtime-flows | Implement modes. | mode/workflow docs | mode/router paths | mode tests | missing contracts |
| A6 companion-docs-site | Implement docs site. | docs-site plans | docs-site paths | docs app/content/UI | install/deploy/registry approval needed |
| A7 tests-validation-evals | Harden validation. | validation/eval docs | tests/evals/validator | validation report | real Spotify/Spicetify path appears |
| A8 final-review-red-team | Review final diff. | all changed files | report only | severity-ranked findings | critical/high unresolved risk |

Approval is required before using worktrees, cloud tasks, package installation, network access, hooks, MCP, deployment, or write-capable subagents in an untrusted repo.
