# Extension and custom app workflow

**Path:** `docs/planning/add-spicetify-skill/workflows/extension-custom-app.md`
**Purpose:** Defines developer scaffolds and enable/debug flows.
**Status:** Draft
**Load/use when:** Read when implementing this cross-cutting workflow.


## Extension scaffold

Default: TypeScript + bundler template. Creator compatibility is explicit because the upstream repository reports deprecation.

## Custom app scaffold

Default: React/TypeScript with generated `manifest.json`, escaped SVG icons, `index.js`, and optional CSS.

## Enable flow

stage/build -> audit -> copy -> config append -> apply -> verify -> optional redacted DevTools logs.
