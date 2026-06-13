# Architecture

**Path:** `docs/planning/add-spicetify-skill/architecture.md`
**Purpose:** Expanded architecture notes for implementation.
**Status:** Draft
**Load/use when:** Read after OpenSpec design for subsystem details.


## Architecture principles

1. Plan before execution.
2. Snapshot before mutation.
3. Execute only typed, allowlisted commands.
4. Verify after every meaningful step.
5. Roll back from known state, not vibes.
6. Treat third-party code as untrusted until audited.
7. Keep `/spicetify` concise; put depth in references.

## Runtime boundaries

| Boundary | Allowed | Blocked by default |
|---|---|---|
| Spicetify CLI | registered argv arrays | shell strings, pipes, unknown flags |
| Filesystem | Spicetify userdata roots, `/spicetify` state root, project workspace | symlink escapes, arbitrary deletes, Spotify prefs contents |
| Network | staged approved fetches | README scripts, implicit package installs, auto-updates |
| DevTools/logs | optional redacted capture | remote debugging flags without confirmation |
| Reports | redacted JSON/Markdown | secrets, tokens, unredacted prefs/logs |

## Data flow

```text
SpicetifyRequest
  -> ModePlanRequest
  -> OperationPlan
  -> SnapshotManifest
  -> OperationRun
  -> VerificationReport
  -> OperationReport
```

## Mode lifecycle

```text
classify -> inspect -> preconditions -> audit/policy -> dry-run plan
         -> confirmation gate -> snapshot -> execute -> verify -> report
                                      | failure
                                      v
                                  rollback plan
```

## State roots

Use discovered Spicetify paths at runtime. Proposed `/spicetify` state roots:

- Windows: `%APPDATA%/spicetify/state/`
- macOS: `~/Library/Application Support/spicetify/state/`
- Linux: `${XDG_STATE_HOME:-~/.local/state}/spicetify/state/`

## Implementation modules

| Module | Responsibility |
|---|---|
| `src/intent` | Prompt/mode routing |
| `src/core` | policies, plans, operation runner |
| `src/spicetify` | command registry, runner, output parsers, path/config discovery |
| `src/fs` | safe path, staging, transactions, hashing |
| `src/state` | snapshots, last-known-good, operation logs |
| `src/modes` | mode planners/executors/verifiers |
| `src/audit` | JS/CSS/manifest/repo auditors |
| `src/verify` | verification checks |
| `src/reports` | Markdown/JSON reports and redaction |
| `skills/spicetify` | compact Skill docs and references |

## Companion Fumadocs site architecture

The documentation surface is an accompanying Next/Fumadocs site with shadcn/ui components. It is planned as a separate application surface that reads authored/generated documentation, not live local Spotify state. It exists to explain `/spicetify` safety, modes, workflows, schemas, reports, and recovery paths.

Key constraints:

- no runtime access to local Spicetify roots, snapshots, logs, screenshots, or Spotify prefs;
- synthetic or redacted examples only;
- shadcn/ui code and third-party registry inputs are reviewed before install;
- Fumadocs content is sourced from local `content/docs` files and deterministic schema/mode reference generation;
- deployment remains a proposal until a trusted repo and host are approved.

See `DESIGN.md`, `fumadocs-site-plan.md`, `docs-content-architecture.md`, `docs-site-design-system.md`, and `docs-site-implementation-plan.md`.
