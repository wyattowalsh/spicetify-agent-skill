# Delta spec: command

**Path:** `openspec/changes/add-spicetify-skill/specs/command/spec.md`
**Purpose:** Behavior-level delta requirements for `command`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Allowlisted Command Execution
The system SHALL execute only registered Spicetify command shapes with validated arguments and `shell: false`.

#### Scenario: Reject raw shell
- GIVEN the user provides a shell pipeline
- WHEN the skill builds a plan
- THEN the plan is blocked
- AND no shell command is emitted for execution

#### Scenario: Run allowed read probe
- GIVEN the engine needs the config path
- WHEN it constructs a command
- THEN the command matches the registry entry for `spicetify -c`

### Requirement: Dry-run Command Plans
The system SHALL explain every command and mutation before execution.

#### Scenario: Plan apply
- GIVEN a theme switch requires `spicetify apply`
- WHEN the skill plans the change
- THEN the plan lists the command, risk, preconditions, verification, and rollback

### Requirement: Combined Command Decomposition
The system SHALL decompose combined Spicetify commands into checkpointed atomic steps.

#### Scenario: Post-update repair command
- GIVEN official guidance would be expressible as `spicetify backup apply`
- WHEN `/spicetify repair` builds a plan
- THEN it emits separate `backup` and `apply` command invocations
- AND verifies each step before proceeding

### Requirement: Command Argument Validation
The system SHALL validate command arguments by semantic type before execution.

#### Scenario: Invalid extension filename
- GIVEN an extension argument contains a path separator
- WHEN a command invocation is built
- THEN the command is rejected before execution

### Requirement: Ambiguous Update Disambiguation
The system SHALL disambiguate update-related user intent before emitting any update, upgrade, backup, apply, or restore command.

#### Scenario: User asks to update Spicetify
- GIVEN the user says “update Spicetify” without specifying theme hot-reload, post-Spotify repair, or CLI maintenance
- WHEN the command plan is built
- THEN no mutating command is emitted
- AND the plan presents explicit safe targets to choose from

#### Scenario: Theme hot reload selected
- GIVEN the user explicitly requests theme hot-reload
- WHEN the command plan is built
- THEN `spicetify update` may be planned with theme-specific verification
