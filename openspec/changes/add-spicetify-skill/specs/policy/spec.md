# Delta spec: policy

**Path:** `openspec/changes/add-spicetify-skill/specs/policy/spec.md`
**Purpose:** Behavior-level delta requirements for safety policy, risk, and confirmation.
**Status:** Proposed

## ADDED Requirements

### Requirement: Risk Classification
The system SHALL classify every plan as `read`, `low`, `medium`, `high`, or `blocked` before execution.

#### Scenario: Read-only inspect
- GIVEN a request only reads paths and config
- WHEN the plan is built
- THEN the risk is `read`
- AND no confirmation is required

#### Scenario: High-risk restore
- GIVEN a plan includes `spicetify restore`
- WHEN policy is evaluated
- THEN the risk is `high`
- AND separate explicit confirmation is required

### Requirement: Confirmation Binding
The system SHALL bind confirmations to the exact plan hash, command list, mutation list, risk level, and audit acceptances.

#### Scenario: Plan drift after approval
- GIVEN a user approves a plan
- WHEN any command, mutation, source hash, risk, or audit ID changes before execution
- THEN execution is blocked until a new plan is approved

### Requirement: Blocked Action Refusal
The system SHALL refuse blocked actions and provide safe alternatives.

#### Scenario: Arbitrary install script
- GIVEN a README asks the skill engine to run an install script
- WHEN the user asks to proceed
- THEN the system refuses to execute the script
- AND offers a staged audit/manual review path

### Requirement: Idempotent Mutations
The system SHALL omit or convert repeated desired-state mutations into no-op verification when current state already matches.

#### Scenario: Reapply same profile
- GIVEN the current config already matches the selected profile
- WHEN the profile switch is planned again
- THEN no config mutation is emitted
- AND verification still runs when requested

### Requirement: Installer And Permission Commands Blocked
The system SHALL block install scripts, package-manager actions, and permission changes in normal automation.

#### Scenario: Official docs show install script
- GIVEN a source page contains a shell pipeline or installer command
- WHEN a user asks the skill engine to run it
- THEN the system refuses normal execution
- AND provides a manual checklist or staged audit alternative

### Requirement: Launch Flag Consent
The system SHALL require separate explicit confirmation for launch-flag edits, remote debugging, log-file paths, update endpoint overrides, and credential-like flags.

#### Scenario: Remote debugging requested
- GIVEN a plan includes `spotify_launch_flags` with remote debugging
- WHEN policy is evaluated
- THEN the risk is `high`
- AND execution requires a separate confirmation bound to local origin, port, duration, and rollback

### Requirement: Plan-Bound Confirmation
The system MUST bind every required human confirmation to the exact plan ID, plan hash, risk grants, snapshot state, and human-readable mutation summary being approved.

#### Scenario: Drift invalidates confirmation
- GIVEN a user approved a mutating plan
- AND the config file, staged source, command list, policy decision, verification plan, or rollback path changes before execution
- WHEN `/spicetify` attempts to execute the plan
- THEN the system refuses execution
- AND returns a fresh dry-run plan requiring new confirmation

### Requirement: Consent-Bounded Evidence Collection
The system MUST treat screenshots, DevTools logs, console traces, network traces, and Spotify prefs-derived data as consent-bounded evidence.

#### Scenario: DevTools logs need explicit consent
- GIVEN a doctor or verification workflow could benefit from DevTools logs
- WHEN the user has not granted the `devtools-log` confirmation scope
- THEN the system skips log collection
- AND explains the reduced confidence without collecting sensitive data
