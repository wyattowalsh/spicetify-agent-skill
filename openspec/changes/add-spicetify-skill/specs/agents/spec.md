# Delta for Agents

**Path:** `openspec/changes/add-spicetify-skill/specs/agents/spec.md`
**Purpose:** OpenSpec delta requirements for subagent/swarm execution behavior.
**Status:** Proposed

## ADDED Requirements

### Requirement: Bounded Subagent Task Graph
The planning bundle MUST define a subagent task graph with explicit agent roles, dependencies, read scopes, write scopes, expected outputs, validation requirements, and stop conditions.

#### Scenario: Swarm kickoff references bounded graph
- GIVEN a user asks Codex to implement `/spicetify` with subagents
- WHEN Codex starts the task
- THEN Codex reads the subagent task graph before spawning agents
- AND each spawned agent is assigned a bounded role and write scope

### Requirement: Parallel Work Scope Isolation
The subagent graph MUST mark work as parallel-safe only when dependencies are satisfied and write scopes do not overlap.

#### Scenario: Overlapping write scopes block parallel execution
- GIVEN two candidate subagents would edit the same file family
- WHEN the orchestrator evaluates the swarm plan
- THEN the system MUST NOT mark those agents as parallel-safe
- AND the orchestrator MUST sequence the work or request a narrower assignment

### Requirement: Subagent Result Envelope
Each subagent SHALL return a structured result envelope containing status, tasks attempted, read scope, write scope used, changed files, validation results, findings, handoff notes, and stop conditions hit.

#### Scenario: Orchestrator rejects incomplete result
- GIVEN a subagent returns without validation status or changed-file scope
- WHEN the orchestrator consolidates results
- THEN the orchestrator MUST flag the result as incomplete
- AND MUST NOT claim the swarm completed successfully

### Requirement: Orchestrator Consolidation
The orchestrator MUST consolidate subagent results, detect conflicts, update living planning state, and run validation before declaring success.

#### Scenario: Conflicting subagent findings
- GIVEN two subagents recommend incompatible schema or API changes
- WHEN the orchestrator reviews their result envelopes
- THEN the orchestrator MUST pause implementation
- AND record the conflict and decision path in planning docs

### Requirement: Approval and Sandbox Inheritance
Subagents MUST inherit the active sandbox and approval policy and MUST NOT request authority expansion except as a stop-and-report item for the human operator.

#### Scenario: Subagent needs network access
- GIVEN a subagent believes network access or package installation is needed
- WHEN the active policy has not approved it
- THEN the subagent MUST stop and report the need
- AND MUST NOT perform the network or package-manager action

### Requirement: Codex Kickoff Prompt
The bundle SHALL include a copyable Codex kickoff prompt that names the read-first files, task graph, subagent sequence, write scopes, validation commands, stop conditions, and final response contract.

#### Scenario: Kickoff prompt avoids context dump
- GIVEN a user wants to start Codex on `/spicetify`
- WHEN they open the kickoff prompt
- THEN the prompt MUST reference bundle paths rather than embedding the full planning bundle
- AND MUST include validation and stop conditions

### Requirement: Sequential Fallback
The subagent task graph SHALL define a sequential fallback that preserves the same write scopes, validation rules, and stop conditions when subagents are unavailable.

#### Scenario: Subagents unavailable
- GIVEN Codex cannot spawn subagents in the current environment
- WHEN the kickoff prompt is used
- THEN Codex MUST proceed through the graph sequentially
- AND return a result envelope after each phase
