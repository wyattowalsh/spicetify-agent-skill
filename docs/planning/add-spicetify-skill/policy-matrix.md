# Policy matrix

**Path:** `docs/planning/add-spicetify-skill/policy-matrix.md`
**Purpose:** Canonical risk and confirmation policy for `/spicetify`.
**Status:** Proposed
**Load/use when:** Implementing the `PolicyEngine`, reviewing unsafe workflows, or writing tests.

## Risk levels

| Level | Examples | Snapshot | Confirmation | Execution |
|---|---|---:|---:|---|
| `read` | inspect paths/config, static audit, report render | No | No | Allowed if command registered. |
| `low` | create new skill-owned file in empty folder, render dry-run plan | Optional | No unless overwrite | Allowed after policy pass. |
| `medium` | `spicetify backup`, `spicetify apply`, profile switch, theme switch | Required | Yes by default | Execute only approved plan hash. |
| `high` | `spicetify restore`, CLI maintenance/upgrade plan, DevTools enable, remote debugging, third-party JS enable, uninstall/delete | Required | Separate explicit confirmation | Execute only after high-risk acknowledgement. |
| `blocked` | arbitrary shell, third-party package script, `sudo chmod`, install script, secret exfiltration, shortcut rewrite, package install/remove | N/A | Cannot override in normal flow | Refuse and offer manual/safe alternative. |

## Confirmation token model

A confirmation MUST bind to:

- `planId`
- `planHash`
- `risk`
- list of mutation IDs
- list of command IDs
- snapshot policy
- accepted audit IDs, if any
- accepted launch/log/screenshot permissions, if any
- expiry timestamp

Execution MUST stop when any of these drift.

## Idempotency rules

- If desired config already matches, mutating config commands are omitted.
- Append-only Spicetify list commands are used only after diffing current list.
- Exact profiles remove extras and add missing entries; repeated profile switch should become a no-op plus verification.
- Generated files are content-hashed; identical writes are no-ops.
- Deletions are allowed only for skill-owned files or explicitly selected paths.
- Repair does not repeat fallback steps after a failed unsupported-compatibility diagnostic without a new plan.

## Approval-gated operations

- Package manager install/remove/upgrade, including `brew`, `winget`, `scoop`, `choco`, `apt`, `yay`, `nix`, `pnpm`, `npm`, `yarn`, and `bun`.
- Install scripts, script pipelines, README commands, Marketplace installer scripts, and package lifecycle scripts.
- `sudo`, `chmod`, ownership changes, shortcut edits, desktop file edits, shell profile edits, launch agents, and login items.
- Network fetches of repos/archives unless pinned, staged, and approved.
- Enabling third-party JavaScript, `theme.js`, `subfiles_extension`, or custom apps after any non-allow audit.
- DevTools enablement, remote debugging, log capture, screenshot capture, and `spotify_launch_flags` edits.
- `spicetify restore`, `upgrade`, `auto`, full uninstall, cache deletion, prefs edits, or update-disabling flags.
- Marketplace publishing, GitHub topic edits, commits, pushes, PRs, or external messages.

## Blocked by default

The engine MUST refuse normal automation for:

- arbitrary shell or user-provided argv;
- commands outside the registry;
- package-manager or install-script execution;
- permission changes;
- reading or printing Spotify prefs contents, cookies, tokens, or credentials;
- sending local data to external endpoints;
- remote debugging exposed beyond explicitly approved local origins;
- destructive delete outside skill-owned files.

## Stop conditions

The engine MUST stop before mutation if:

- snapshot fails or hashes mismatch;
- config cannot be parsed;
- source path is outside allowed roots;
- symlink escapes staging or target root;
- command is not in registry;
- mode planner emits an untyped mutation;
- audit verdict is `block` and no acceptable manual path exists;
- validation requires real Spotify in CI;
- a task needs secrets, credentials, private tokens, or unapproved network/tool expansion.
