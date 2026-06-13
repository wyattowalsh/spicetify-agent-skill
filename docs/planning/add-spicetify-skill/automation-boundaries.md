# Automation boundaries

**Path:** `docs/planning/add-spicetify-skill/automation-boundaries.md`
**Purpose:** Defines how `/spicetify` supports power-user automation without expanding authority.
**Status:** Proposed
**Load/use when:** Implementing batch plans, headless dry-runs, CI checks, policy presets, or manifest replay.

## Principle

Automation is a way to repeat approved desired-state workflows, not a way to bypass safety. The same policy engine decides interactive and headless operations.

## Supported automation shapes

| Shape | Allowed by default | Notes |
|---|---|---|
| Headless inspect/doctor/audit/report | Yes | Read-only, redacted output. |
| Headless dry-run manifest diff | Yes | No mutation, no downloads. |
| Generated-file-only local writes | Maybe | Must pass path guard and policy. |
| Batch profile/theme apply | Approval-gated | Snapshot and verification per mutation group. |
| Third-party download/install/enable | Approval-gated | Requires provenance and audit. |
| Package manager/build scripts | Manual or explicit approval | Never hidden in automation. |
| Permission/shortcut/launch-flag changes | Separate explicit approval | Not part of ordinary automation. |

## Batch execution model

A batch is a sequence of operation groups:

1. preflight and lock acquisition;
2. plan hash and policy decision;
3. snapshot group;
4. mutation group;
5. verification group;
6. report and last-known-good update;
7. rollback if required.

Execution stops when a required verification fails. Later groups do not run unless the user explicitly creates a new plan from the reported state.

## Policy presets

Policy presets may lower friction for trusted local generated assets, but cannot suppress blocked actions. A preset can say “local generated theme writes are usually low risk”; it cannot say “run arbitrary shell” or “skip snapshots for high-risk restore”.

## CI guardrails

CI must:

- use fake Spicetify binaries and fixture roots;
- fail if a real user Spicetify or Spotify path is detected;
- run schemas, lint, unit tests, and fake integration tests;
- never run install scripts, package manager mutations, remote downloads, DevTools, screenshots, or real Spotify apply/restore;
- produce operation reports only from fixtures.
