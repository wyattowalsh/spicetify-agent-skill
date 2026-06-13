# Confirmation flow

**Path:** `docs/planning/add-spicetify-skill/confirmation-flow.md`
**Purpose:** Defines how `/spicetify` obtains, validates, invalidates, and reports human confirmations.
**Status:** Proposed
**Load/use when:** Implementing `apply`, `repair`, `restore`, `rollback`, `uninstall`, `devtools`, third-party install, or any high-risk workflow.

## Core rule

A confirmation is not a vague yes/no. It is a scoped grant bound to a specific `planId`, `planHash`, risk class, snapshot requirement, and human-readable mutation summary. Any change to the plan, source hashes, local config, staged files, audit findings, command list, or rollback path invalidates the grant.

## Confirmation levels

| Grant | Required for | Extra constraints |
|---|---|---|
| `snapshot` | any mutation that changes config/assets | snapshot must be created and verified first |
| `medium-mutation` | `spicetify backup`, `spicetify apply`, profile/theme switch | plan hash must match execution input |
| `high-mutation` | `restore`, fallback repair, DevTools enablement | separate risk acknowledgement |
| `destructive` | delete, uninstall, reset, overwrite | exact file list and restore path shown |
| `third-party-code` | enabling extension, theme JS, custom app, Marketplace/GitHub code | audit report and provenance lock accepted |
| `network-fetch` | fetching source archives or metadata | pinned source/ref and destination staging root shown |
| `devtools-log` | reading console/log output | redaction level and collection duration shown |
| `screenshot` | capturing UI screenshots | capture scope and retention policy shown |
| `launch-flag` | editing `spotify_launch_flags` or remote debugging | rollback value and port/origin risk shown |
| `package-manager` / `permission-change` | installer or chmod-style advice | manual-only unless the user separately approves outside normal automation |

## Confirmation object

See `schemas/confirmation.schema.json`. The implementation should persist confirmation grants beside operation records and reference them from `OperationRun` reports.

## UX requirements

Before asking for confirmation, `/spicetify` must display:

1. purpose and mode;
2. exact commands and file mutations;
3. snapshot ID or snapshot plan;
4. audit/provenance result for third-party code;
5. rollback path;
6. risks that remain after safeguards;
7. what will *not* be automated.

## Invalidating events

- `config-xpui.ini` hash changes after planning.
- Any staged third-party file changes after audit.
- Command registry entry changes.
- Policy decision changes.
- User asks for a different mode or target.
- Snapshot creation fails or hashes mismatch.
- Verification plan changes.

## Reporting

Reports must include whether confirmation was absent, granted, invalidated, expired, or revoked. Reports must not include raw confirmation tokens, secrets, prefs contents, or unredacted DevTools logs.


## Consent grants vs confirmations

Confirmations approve mutations or high-risk plan effects. Consent grants approve bounded evidence collection such as logs, screenshots, launch flags, source archives, network staging, or build-script execution. A plan may need both. Consent grants are modeled separately in `schemas/consent-grant.schema.json` so evidence scope, duration, output limit, redaction policy, and shareability are explicit.

## Redaction dependency

Any confirmation involving logs, screenshots, launch flags, reports, or source archives must name the redaction policy that will be applied before evidence is persisted or displayed as shareable output.
