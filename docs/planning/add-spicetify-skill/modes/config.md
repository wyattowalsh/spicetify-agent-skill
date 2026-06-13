# Mode: config

**Path:** `docs/planning/add-spicetify-skill/modes/config.md`
**Purpose:** Detailed contract for `/spicetify config` mode.
**Status:** Proposed
**Load/use when:** Implementing, testing, or reviewing `config` behavior.

## Purpose

Inspect, diff, and safely edit `config-xpui.ini`.

## Inputs

config key/value changes, exact list changes, `applyAfter?`.

## Preconditions

Config path found and config parses.

## Commands/files touched

`spicetify config`; transactional INI edit only when CLI cannot express exact state.

## Safety checks

Allowlisted keys; `[Patch]` protected; snapshot before writes.

## Plan output

`ConfigPlan` with before/after, CLI-vs-INI strategy, required apply, rollback.

## Execution flow

Prefer CLI config commands; direct edit via staged atomic write if justified.

## Verification flow

Parse after config; compare desired model; optional apply verification.

## Rollback flow

Restore prior config snapshot and reapply if needed.

## Idempotency notes

The planner MUST diff current state before emitting mutations. Re-running an already satisfied desired state SHOULD become a no-op plus verification unless the user explicitly requests refresh/reapply.

## Failure modes and recovery

- Malformed config -> stop and snapshot for manual repair.
- Exact list replacement not expressible by CLI -> require transactional INI fallback.


## Data contracts

Primary contracts: `operation-plan, profile, verification-report`. Any implementation-specific schema expansion MUST update `docs/planning/add-spicetify-skill/schemas/README.md`, `api-contracts.md`, and regression prompts.

## Cross-cutting controls

- Policy decision is required before execution, even for no-op verification plans.
- Secrets, prefs content, logs, screenshots, and private paths follow `privacy-redaction.md`.
- Third-party, Marketplace, imported, or unknown assets require provenance and audit before enablement.
- Desired-state or automation inputs cannot waive non-negotiable safety invariants.

## Example user prompts

- `/spicetify config set current_theme TerminalDark`

## Example structured response

```json
{
  "mode": "config",
  "risk": "medium",
  "changes": [
    {
      "key": "current_theme",
      "from": "Default",
      "to": "TerminalDark"
    }
  ],
  "requiresApply": true
}
```
