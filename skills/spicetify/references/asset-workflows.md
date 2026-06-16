# Asset Workflows

Use this reference when `/spicetify` needs to create, inspect, audit, stage, or plan changes for Spicetify assets.

## Asset State Machine

```text
discovered -> pinned -> staged -> inspected -> audited -> planned -> confirmed -> executed -> verified -> rollbackable
```

Stop at the earliest safe artifact. Do not execute mutation from the initial prompt.

For local audit or inspection, use only staged asset roots. The helper CLI can receive an explicit `--asset-root` for a staged directory; do not point it at real Spotify or Spicetify state. Symlinks, `..` escapes, secret-like names, and real app-state paths must be refused.

## Asset Kinds

- Theme: require `color.ini` and `user.css`; audit optional `theme.js` and remote assets.
- Extension: inspect JavaScript or MJS, Spicetify API wait patterns, Platform API usage, storage, network, and cleanup behavior.
- Custom app: distinguish raw `manifest.json` apps from Creator-compatible `src/settings.json` projects; audit `subfiles_extension` as startup JavaScript.
- Snippet: distinguish CSS-only snippets from executable JavaScript; flag deceptive UI CSS and external assets.
- Marketplace item: validate metadata and publishing shape, but never treat metadata as trust.

## Generated Local Assets

Generated templates should default to:

- feature detection for Spicetify APIs;
- no external network by default;
- unique storage prefixes;
- listener cleanup;
- auditable output metadata.

Build tools, package managers, Creator generators, watch commands, and lifecycle scripts remain manual or explicit approval-gated.
