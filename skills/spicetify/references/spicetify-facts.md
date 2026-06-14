# Spicetify Facts

Use these facts to separate upstream Spicetify behavior from `/spicetify` safety behavior.

## Upstream Spicetify

- Spicetify is the official external CLI used to customize the Spotify desktop client.
- The executable is named `spicetify`; this skill must not create a competing command with that name.
- The config file is typically `config-xpui.ini`.
- Default config paths documented by Spicetify are `%appdata%\spicetify\config-xpui.ini` on Windows and `~/.config/spicetify/config-xpui.ini` on Linux/macOS.
- Use Spicetify path/config commands to discover actual local paths instead of guessing.
- Common customization surfaces include config keys, themes, extensions, custom apps, snippets, and Marketplace assets.
- Combined upstream commands such as backup/apply flows should be decomposed into separate checkpointed operations by `/spicetify`.

## /spicetify Contracts

- `spicetify-agent` is the safe helper CLI for planning, audit, snapshot, verification, reporting, and guarded execution.
- Desired-state manifests, provenance locks, redaction policies, consent grants, and asset manifests are `/spicetify` contracts, not upstream Spicetify features.
- Marketplace metadata does not establish trust.
- Installer scripts, package-manager actions, permission changes, DevTools evidence, screenshots, and publishing require separate gates.

## Recheck Triggers

Recheck upstream docs before changing behavior that depends on Spicetify command semantics, install paths, Spotify package behavior, Creator/Marketplace rules, DevTools flags, or config-file format.
