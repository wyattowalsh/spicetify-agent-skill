# Theme workflow

**Path:** `docs/planning/add-spicetify-skill/workflows/theme.md`
**Purpose:** Defines theme creation, validation, installation, switching, and rollback.
**Status:** Draft
**Load/use when:** Read when implementing this cross-cutting workflow.


## Required theme files

- `color.ini`
- `user.css`

## Safe install flow

stage -> audit CSS/optional JS -> validate files -> snapshot -> copy -> config -> apply -> verify -> report

## Generated terminal theme

The default example theme is `TerminalDark` with dark terminal colors, local CSS only, and no remote imports.
