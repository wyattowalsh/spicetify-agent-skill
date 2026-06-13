# Workflow: command abstraction

**Path:** `docs/planning/add-spicetify-skill/workflows/command-abstraction.md`
**Purpose:** Define how `/spicetify` compiles semantic intents into safe Spicetify CLI invocations.
**Status:** Proposed
**Load/use when:** Implementing `CommandRegistry`, `SpicetifyRunner`, command validation, or command-related tests.

## Principle

`/spicetify` is not a shell wrapper. It accepts user intent, builds a typed `OperationPlan`, and emits only command invocations that match a registry entry and pass argument validators.

## Allowed execution shape

```ts
spawn("spicetify", args, {
  shell: false,
  cwd: approvedCwd,
  env: sanitizedEnv,
  timeout: registryEntry.timeoutMs
});
```

The runner MUST NOT call `exec`, `spawn(..., { shell: true })`, concatenate command strings, run user-provided argv, or execute command text from READMEs, docs, Marketplace metadata, package scripts, or audit targets.

## Registry contract

Each registry entry defines:

- semantic verb;
- exact `spicetify` argv template;
- risk level;
- snapshot requirement;
- confirmation requirement;
- argument validators;
- output parser;
- timeout;
- platform applicability;
- documentation/source note for volatile command semantics.

Schemas: `schemas/command-registry.schema.json` and `schemas/command-invocation.schema.json`.

## Required command groups

| Group | Shape | Policy |
|---|---|---|
| Discovery | `--version`, `-c`, `config`, `path`, `path userdata`, `path spotify` | read-only; allowed in inspect/doctor. |
| Backup/apply | `backup`, `apply`, `apply --no-restart` | snapshot + confirmation for mutating runs. |
| Config edit | `config <key> <value>`, `config extensions <file.js>`, `config extensions <file.js->`, `config custom_apps <name>`, `config custom_apps <name->` | validated keys/values only. |
| Theme hot reload | `update` | only for explicit theme hot-reload intent; do not use as generic updater. |
| Maintenance/high-risk | `restore`, `upgrade`, `enable-devtools`, `watch`, `auto` | high-risk or approval-gated; never hidden. |

Combined official commands such as `backup apply` and `restore backup apply` are represented as separate steps so `/spicetify` can snapshot, verify, and stop between them.

## Update ambiguity rule

Official docs use update-related wording in multiple ways. The skill engine must disambiguate before action:

| User intent | `/spicetify` route | Allowed CLI behavior |
|---|---|---|
| “Hot reload my theme” | `update` mode with `theme-hot-reload` target | may plan `spicetify update`. |
| “Spotify updated and Spicetify broke” | `repair` mode | plan doctor → snapshot → `backup` → `apply`; fallback separate. |
| “Update Spicetify itself” | `update` mode with `maintenance-plan` target | inspect install method and produce manual/approval-gated plan; do not assume `update` vs `upgrade`. |
| “Run the update command from docs” | blocked until intent is clarified | no command emitted. |

## Argument validators

- `safeConfigKey`: allow only known config keys; protect `[Patch]` by default.
- `safeConfigValue`: validate booleans, slugs, leaf filenames, and discovered absolute paths by key.
- `safeExtensionFile`: basename only, `.js` suffix, no separators, no traversal.
- `safeCustomAppName`: basename/folder slug only.
- `safeThemeName`: slug/folder-safe name.
- `safePathFromDiscovery`: path must be discovered by Spicetify or explicitly approved.
- `noShellMetacharacters`: reject shell-only syntax even though shell is disabled.

## Output parsing

Output parsers are small and conservative:

- `cliIdentity`: semantic discovery verb that compiles to `spicetify --version`; never used as a hardcoded compatibility guarantee.
- `path`: exact path line(s), normalized but not trusted until existence checked.
- `config`: INI/list value capture.
- `text`: redacted raw evidence.
- `none`: for commands where exit code is enough.

## Failure handling

- Unknown verb: block with `COMMAND_NOT_ALLOWLISTED`.
- Validator failure: block with `COMMAND_ARGUMENT_REJECTED`.
- Registry drift: fail tests before runtime.
- Command failure: stop current plan, run verification snapshot check, recommend rollback if needed.
- Ambiguous update/upgrade/repair wording: stop with `COMMAND_INTENT_AMBIGUOUS` and ask for an explicit target or produce safe alternatives.

## Regression tests

- Every registry verb has at least one allowed fixture and one rejected fixture.
- Shell metacharacter input is rejected.
- `shell` is always `false`.
- Combined commands are decomposed.
- `restore`, `upgrade`, `enable-devtools`, `watch`, and `auto` require explicit policy gates.
- “Update Spicetify” and “Spotify updated” prompts route to different plans.
