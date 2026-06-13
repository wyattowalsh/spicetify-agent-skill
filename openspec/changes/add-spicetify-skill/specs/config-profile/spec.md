# Delta spec: config-profile

**Path:** `openspec/changes/add-spicetify-skill/specs/config-profile/spec.md`
**Purpose:** Behavior-level delta requirements for `config-profile`.
**Status:** Proposed

## ADDED Requirements

### Requirement: Config Modeling
The system SHALL parse and model `config-xpui.ini` without treating unknown low-level patches as editable by default.

#### Scenario: Read config
- GIVEN the config path is known
- WHEN the skill inspects state
- THEN the parsed model includes setting, preprocess, additional option, and protected patch sections

#### Scenario: Patch protected
- GIVEN a request tries to edit a patch key
- WHEN the plan is built
- THEN the operation is blocked unless explicitly elevated

### Requirement: CLI-Preferred Config Edits
The system SHALL prefer Spicetify CLI config operations over direct INI edits when the desired mutation can be represented by CLI arguments.

#### Scenario: Set current theme
- GIVEN a request sets `current_theme`
- WHEN the plan is built
- THEN the mutation is represented by `spicetify config current_theme <value>`

### Requirement: Profile Switching
The system SHALL treat profiles as exact desired customization state.

#### Scenario: Switch profile
- GIVEN current config has extra extensions
- WHEN the user switches to a profile
- THEN the plan removes unlisted extensions and adds missing listed extensions

#### Scenario: Profile audit
- GIVEN a profile references third-party JavaScript
- WHEN the plan is built
- THEN audit approval is required before enabling
