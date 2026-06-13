# Research brief

**Path:** `docs/planning/add-spicetify-skill/research.md`
**Purpose:** Source-backed facts, assumptions, and recheck triggers.
**Status:** Draft
**Load/use when:** Read when reviewing volatile Spicetify/OpenSpec/tooling facts.


## Bottom line

The bundle is grounded in official Spicetify docs and the OpenSpec concepts documentation checked on 2026-06-06. The most important product implications are: wrap Spicetify as a semantic plan/execution engine, do not expose raw shell, treat Spotify updates as compatibility-risk events, treat third-party customization code as untrusted, and keep implementation details outside behavior specs.

## Source table

| Source | Date checked | What it supports | Confidence |
|---|---:|---|---|
| https://spicetify.app/docs/getting-started | 2026-06-06 | Spicetify is multiplatform and customizes the Spotify desktop client; install methods vary by platform. | High |
| https://spicetify.app/docs/cli/commands | 2026-06-06 | CLI commands: `backup`, `apply`, `restore`, `update`, `upgrade`, `config`, `path`, `enable-devtools`, `watch`, `auto`. | High |
| https://spicetify.app/docs/customization/config-file/ | 2026-06-06 | Config model, `config-xpui.ini`, default locations, CLI config editing, AdditionalOptions/Patch sections. | High |
| https://spicetify.app/docs/development/themes.html | 2026-06-06 | Theme locations, home priority, required `color.ini` and `user.css`. | High |
| https://spicetify.app/docs/customization/extensions.html | 2026-06-06 | Extension placement and enable/apply flow; list append behavior. | High |
| https://spicetify.app/docs/customization/custom-apps.html | 2026-06-06 | Custom app placement, `index.js` and `manifest.json`, enable/apply flow, troubleshooting. | High |
| https://spicetify.app/docs/customization/marketplace.html | 2026-06-06 | Marketplace provides in-Spotify browsing/installation/management for extensions/themes/snippets. | High |
| https://spicetify.app/docs/faq.html | 2026-06-06 | Post-Spotify-update repair guidance and platform-specific path/prefs issues. | High |
| https://github.com/spicetify/spicetify-creator | 2026-06-06 | GitHub README says Creator is deprecated for bundling; use modern bundlers instead. | High |
| https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md | 2026-06-06 | OpenSpec change folders, artifact flow, delta spec format, archive model. | High |

## Verified facts

- Spicetify is a multiplatform CLI for customizing the official Spotify client.
- `spicetify apply` injects theme, extension, custom app, and other modifications.
- `spicetify restore` removes Spicetify modifications while preserving config/customization files.
- `spicetify update` is a theme hot-reload command, not a CLI upgrade command.
- `spicetify upgrade` applies to script-based Spicetify installations.
- `spicetify config extensions <file.js>` and `custom_apps <folder>` append to existing lists.
- Removing extension/custom app entries uses a trailing `-`.
- Spicetify config is `config-xpui.ini`; default path differs by platform.
- Themes should include `color.ini` and `user.css`.
- Custom apps require at minimum `index.js` and `manifest.json`.
- After Spotify updates, official guidance recommends `spicetify backup apply`, with caveats that new Spotify client builds may not yet be supported.

## Assumptions

- ASSUMPTION-001: The skill runs locally with user-level permissions.
- ASSUMPTION-002: The implementation can invoke `spicetify` through `spawn` in a trusted local process.
- ASSUMPTION-003: CLI output formats may drift and should be parsed conservatively.
- ASSUMPTION-004: Source downloads are opt-in and staged; no network by default.

## Source conflict

Official Spicetify docs still describe Spicetify Creator as a modern TypeScript/React/esbuild workflow, while the GitHub README says the project is deprecated. The plan chooses modern bundler templates by default and leaves Creator as legacy compatibility only.

## Recheck triggers

- Spicetify CLI changelog/source metadata or command docs change.
- Spotify desktop client updates break Spicetify.
- Spicetify Marketplace installation/publishing behavior changes.
- Spicetify Creator status changes.
- OpenSpec command/profile syntax changes.
- Codex Skill packaging conventions change.
