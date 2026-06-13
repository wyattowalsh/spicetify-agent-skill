# Config and profile workflow

**Path:** `docs/planning/add-spicetify-skill/workflows/config-profile.md`
**Purpose:** Defines config parsing and declarative profile switching.
**Status:** Draft
**Load/use when:** Read when implementing this cross-cutting workflow.


## Config strategy

- Discover path with `spicetify -c`.
- Prefer `spicetify config <key> <value>`.
- Parse before and after.
- Protect `[Patch]` by default.
- Use direct INI transaction only for exact-list replacement or comment-preserving edits.

## Profile strategy

Profiles are exact desired state. A switch computes add/remove diffs for themes, color schemes, extensions, custom apps, snippets, and selected AdditionalOptions.
