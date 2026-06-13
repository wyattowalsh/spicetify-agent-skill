# Mode router reference

**Path:** `skills/spicetify/references/mode-router.md`
**Purpose:** Compact routing table for the /spicetify skill.
**Status:** Draft
**Load/use when:** Use inside the skill when mapping prompts to modes.


| User intent | Mode |
|---|---|
| What is installed? What paths/config/assets exist? | `inspect` |
| What is broken? Why is Marketplace gone? | `doctor` |
| Save current state | `snapshot` |
| Restore named state | `restore` |
| Spotify update broke Spicetify | `repair` |
| Execute approved plan | `apply` |
| Change config key/list | `config` |
| Switch minimal/dev/visualizer setup | `profile` |
| Create/install/switch theme | `theme` |
| Scaffold/audit/enable extension | `extension` |
| Scaffold/audit/enable custom app | `custom-app` |
| Add/manage CSS tweak | `snippet` |
| Inspect/audit Marketplace assets | `marketplace` |
| Review third-party code | `audit` |
| Enable/collect debug logs | `devtools` |
| Hot reload local dev changes | `watch` |
| Export/migrate setup | `migrate` |
| Hot reload / CLI upgrade plan / post-update | `update` |
| Return to last-known-good | `rollback` |
| Remove assets/customizations | `uninstall` |
| Share diagnostics | `report` |
