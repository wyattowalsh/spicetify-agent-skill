# Design: Build the `/spicetify` Skill

**Path:** `openspec/changes/add-spicetify-skill/design.md`
**Purpose:** Architecture, alternatives, data flows, and implementation boundaries.
**Status:** Proposed
**Load/use when:** Read before implementation tasks or detailed workflow docs.

## Summary

`/spicetify` is a skill-facing orchestration layer over a local Python package named `spicetify-agent`. It never becomes an arbitrary terminal. It classifies intent into modes, performs read-only discovery, builds a typed dry-run plan, checks policy, snapshots if needed, executes allowlisted commands/file transactions only after approval, verifies, and produces a report. Failed mutating operations have a recorded rollback path.

## Goals

- Make Spicetify workflows safe enough for novices and powerful enough for power users.
- Preserve user files, config, and last-known-good customization state.
- Treat Spicetify, Spotify, Marketplace, extensions, snippets, themes, custom apps, GitHub repos, docs, and CLI output as unstable/untrusted unless proven otherwise.
- Use structured outputs over prose-only action.
- Keep the visible skill simple: `/spicetify`.
- Make safety invariants testable in fake environments before any real mutation can be attempted.

## Non-goals

- Replace Spicetify.
- Install Spotify or Spicetify by default.
- Make Marketplace publishing autonomous.
- Guarantee compatibility with future Spotify client builds.
- Execute shell snippets from users or third-party docs.
- Automate package-manager installs, permission changes, shortcuts, launch agents, or remote repo changes.

## Architecture

```text
/spicetify prompt
  -> SkillRouter
  -> IntentRouter / ModeController
  -> EnvironmentProbe              # read-only
  -> PlanBuilder                   # dry-run only
  -> PolicyEngine                  # risk, approvals, stop rules
  -> SnapshotStore                 # immutable hash manifests
  -> TransactionRunner             # exact approved plan hash
       -> SpicetifyCommandAdapter  # allowlisted argv + shell:false
       -> FileTransactionAdapter   # staged writes + path guard
       -> NetworkStagingAdapter    # disabled unless explicitly approved
  -> Verifier                      # CLI/config/files/logs/screenshots optional
  -> RollbackManager
  -> ConsentManager                # evidence/log/screenshot approval bounds
  -> ReportWriter                  # redacted JSON/Markdown
```


## Companion documentation-site architecture

```text
OpenSpec + planning docs + schemas
  -> curated MDX content and deterministic reference generation
  -> Fumadocs source collection
  -> Next.js App Router docs pages
  -> shadcn/ui primitives + custom /spicetify docs components
  -> validated docs build with synthetic/redacted examples only
```

The companion site is designed as an operations manual, not a separate product. It should explain safe usage, mode behavior, schema contracts, recovery paths, and implementation boundaries. It must not connect to the local operator runtime, read local Spotify state, collect logs, or present mutating commands as casual copy-paste actions.

## Core invariants

- Commands are arrays, never shell strings.
- Combined Spicetify commands are split into checkpointed steps.
- Medium/high mutations require snapshots.
- Third-party executable code requires audit and provenance lock before enablement.
- Plan hash and audited file hashes are checked immediately before execution.
- Last-known-good updates only after required verification passes.
- CI uses fake Spicetify and fake roots only.
- Desired-state manifests are data inputs and cannot disable core policy invariants.
- Debug evidence and shareable reports are governed by consent and redaction contracts.
- Documentation examples are synthetic or redacted and are validated before publishing.
- Scaffolded build output is audited before installation or enablement.

## Data flow

1. Normalize request into `SpicetifyRequest`.
2. Run read-only environment probes.
3. Build `OperationPlan` with typed mutations, commands, verification, rollback, and policy hints.
4. Evaluate plan through `PolicyEngine`.
5. If mutation is possible, present dry-run and require confirmation token bound to plan hash.
6. Create snapshot and verify snapshot manifest.
7. Execute exactly the approved command/file steps.
8. Verify required checks.
9. Update last-known-good only on success.
10. Emit `OperationReport`.

## Command design

The engine uses `subprocess.run([executable, *argv], shell=False)` behind a command registry. No mode can pass a raw command string. Config edits prefer `spicetify config`; direct INI transactions are reserved for exact list replacement or comment-preserving edits that the CLI cannot express.

## State model

Spicetify vanilla backups and `/spicetify` snapshots are separate concepts.

- Spicetify `backup` protects vanilla Spotify files.
- `/spicetify` snapshots protect user config/customization assets.
- A mutating operation has pre-snapshot, operation log, verification report, and rollback pointer.
- `last-known-good` updates only after verification.

See `apps/docs/content/docs/archive/add-spicetify-skill/operation-state-machine.mdx`.

## Desired-state and automation model

Profiles describe exact named customization states. Desired-state manifests describe a broader repeatable setup: profiles, config, assets, provenance locks, safety policy, and verification expectations. The implementation treats manifests as declarative data, computes an explicit dry-run diff, and refuses unsafe overrides. Headless automation may generate plans and reports, but it cannot auto-approve blocked or high-risk operations.

## Privacy and evidence model

The runtime uses a `ConsentGrant` before collecting screenshots, DevTools logs, launch flags, source archives, or other high-context evidence. `ReportWriter` applies a `RedactionPolicy`, assigns a shareability label, and blocks issue-ready output when secret scanning fails. Snapshot defaults exclude sensitive or non-restorable data.

## Scaffold model

## Docs-site model

The docs site uses Fumadocs for MDX collections, navigation, search-oriented docs structure, and page rendering, and shadcn/ui for copied/customized UI primitives. The site is planned under `docs-site.md`, `docs-site-content-map.md`, `docs-site-design-system.md`, and `workflows/docs-site.md`. Install/build commands are proposals until a trusted target repo approves package-manager actions.

Local generated templates are first-party generated assets, but their build outputs are still audited before install/enable. Third-party or imported project package scripts are never run before package/source audit and explicit approval. Creator compatibility remains opt-in because the documentation and source repository currently conflict.

## Safety model

Risk levels: `read`, `low`, `medium`, `high`, `blocked`.

Blocked by default:

- arbitrary shell
- `curl | sh`, PowerShell install scripts, or package scripts from third-party repos
- direct secret/prefs reads
- permission changes
- launch flag mutation without explicit DevTools plan
- high-risk third-party JavaScript enablement without accepted audit
- package-manager, publishing, shortcut, desktop-file, or cloud/network actions outside explicit approval

See `policy-matrix.md` and `threat-model.md`.

## Platform design

The engine must discover rather than assume paths. Platform/package facts are captured in `platform-matrix.md`. Doctor/repair can explain package-specific remedies but must stop before running `sudo`, package managers, `snap remove`, shortcut rewrites, or broad permission changes.

## Alternatives considered

| Option | Pros | Cons | Decision |
|---|---|---|---|
| Thin shell wrapper | Fast to build | Unsafe, non-transactional, poor UX | Rejected |
| Pure prompt-only Skill | Easy to install | Cannot validate/snapshot/rollback robustly | Rejected for production implementation |
| Local CLI plus Skill | Safe execution boundary, testable, repeatable | More engineering work | Accepted |
| Always use Spicetify Creator | Familiar docs path | Upstream repo currently reports deprecation | Creator compatibility only; default to maintained bundler templates |
| Monolithic `SKILL.md` | Easy to paste | Bloated, poor context economy | Rejected; use progressive references |
| Auto-run Marketplace/install scripts | Convenient | Supply-chain risk and command injection | Rejected; stage/audit/manual approval only |
| Use generic Markdown docs only | Simple | Loses searchable, structured, component-rich safety guidance | Rejected; use Fumadocs with shadcn/ui for the companion site |
| Directly edit config for every change | Exact control | Corruption risk and drift from CLI semantics | Prefer CLI; transactional direct edit only when needed |

## Implementation boundary

Behavior belongs in `spec.md`. Concrete packages, parser choices, file layout, fake binaries, and AST audit implementation belong here, `tasks.md`, or planning docs.

Recommended implementation stack:

- Python 3.11+ package with `pyproject.toml`, `setuptools`, and the `spicetify-agent` console command
- standard-library-first runtime modules for CLI, schema loading, filesystem guards, snapshots, command planning, subprocess execution, reports, and tests
- JSON Schema files under `schemas/` as the root contract surface
- fake Spicetify binary for integration tests
- Python `pytest`, `ruff`, and `ty` as external development validation tools
- pnpm workspace metadata only for the isolated companion docs app
- Fumadocs MDX and Fumadocs UI for the companion documentation site
- shadcn/ui-compatible local components for the docs-site design system
- TypeScript only inside `apps/docs`, not as the runtime authority layer

## Rollout / rollback

Roll out by phases:

1. contracts, policy, command registry, fixtures
2. read-only inspect/doctor/audit/report
3. snapshot/config/profile/theme create
4. apply/rollback/repair
5. extension/custom-app scaffolds and local builds
6. Marketplace/network staging, watch, devtools, migration, uninstall

Rollback at runtime is file/config restore plus optional `spicetify apply`. Rollback in planning is restore from source control or delete generated implementation artifacts that have not been accepted.


## Invariant and recovery layer

The executor should treat invariants and the recovery catalog as runtime contracts, not documentation-only guidance. Policy decisions decide whether a plan may proceed; invariant assertions verify that non-waivable rules still hold immediately before execution; recovery catalog entries define what happens when a step fails. This keeps repair behavior deterministic and reviewable.

Implementation detail belongs in code and tests, but the observable contract is that failed operations produce structured recovery reports and never silently broaden authority.

## Accompanying Fumadocs documentation site

The implementation plan includes an accompanying documentation app. This is not part of the local mutation boundary, but it is part of the product surface because it makes safety behavior, modes, schemas, and implementation contracts reviewable.

Recommended app path: `apps/docs`.

Primary design:

```text
apps/docs
  -> Next app router
  -> Fumadocs MDX content source
  -> Fumadocs UI docs layout
  -> shadcn/ui local components and theme tokens
  -> generated reference pages from OpenSpec, schemas, mode docs, and traceability
  -> local search endpoint
  -> AI-readable routes after redaction
```

Docs-site safety constraints:

- package-manager commands are proposed until approved;
- deployment, analytics, hosted search, feedback storage, and external registries are deferred unless explicitly approved;
- generated docs must include source paths and be diff-reviewable;
- docs cannot weaken `/spicetify` safety invariants;
- docs cannot include real secrets, unredacted logs, private local paths, Spotify prefs contents, or sensitive screenshots.

See `DESIGN.md`, `fumadocs-site-plan.md`, `docs-site.md`, `docs-content-architecture.md`, `docs-site-content-map.md`, `docs-site-design-system.md`, `docs-site-implementation-plan.md`, and `workflows/fumadocs-site.md`.

## Docs-site source and validation boundary

The docs site may render pages generated from local OpenSpec, schema, mode, and traceability sources, but generation must be deterministic, diff-reviewable, and redaction-checked. The docs app must not connect to a running `/spicetify` engine or local Spotify state. Its search and AI-readable routes may expose stable documentation content only.
