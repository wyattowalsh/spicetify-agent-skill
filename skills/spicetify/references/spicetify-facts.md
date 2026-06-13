# Spicetify facts

**Path:** `skills/spicetify/references/spicetify-facts.md`
**Purpose:** Source-backed Spicetify facts used by the skill.
**Status:** Proposed / source-refreshed
**Load/use when:** Grounding command/config/path/theme/extension/custom-app/Marketplace behavior.

Checked on 2026-06-07.

## Verified facts

- Spicetify is a multiplatform CLI for customizing the official Spotify desktop client.
- Config file is `config-xpui.ini`.
- Default config paths documented by Spicetify:
  - Windows: `%appdata%\spicetify\config-xpui.ini`
  - Linux/macOS: `~/.config/spicetify/config-xpui.ini`
- Use `spicetify -c` and `spicetify config-dir`/path commands to discover actual local paths.
- Prefer `spicetify config <key> <value>` followed by `spicetify apply` for config edits.
- `spicetify config extensions <file.js>` appends; remove with `<file.js>-`.
- `spicetify config custom_apps <folder>` appends; remove with `<folder>-`.
- Themes should include `color.ini` and `user.css`; `theme.js` is optional and security-sensitive.
- Extensions are JavaScript files enabled via config and applied to Spotify.
- Custom apps need `index.js` and `manifest.json`; manifest includes icon/subfile fields.
- Marketplace handles extensions, themes, snippets, and partial custom-app/manual flows; Marketplace metadata is not a trust boundary.
- After Spotify updates, official guidance includes `spicetify backup apply`, but support may lag new Spotify client builds.
- Creator documentation and Creator GitHub README conflict; default to maintained bundlers and treat Creator as compatibility-only.

## Recheck triggers

Recheck sources before implementation if Spicetify CLI identity, Spotify package behavior, Creator status, Marketplace publishing rules, DevTools flags, or CLI command semantics matter.


## /spicetify-specific facts

- Desired-state manifests, provenance locks, redaction policies, consent grants, and asset manifests are `/spicetify` contracts, not upstream Spicetify features.
- When reporting facts, separate upstream Spicetify behavior from `/spicetify` safety behavior.
