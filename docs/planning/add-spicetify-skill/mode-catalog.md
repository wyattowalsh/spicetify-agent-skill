# Mode catalog

**Path:** `docs/planning/add-spicetify-skill/mode-catalog.md`
**Purpose:** One-page index of all semantic modes.
**Status:** Proposed
**Load/use when:** Routing prompts or selecting mode docs.

| Mode | Purpose | Typical risk | Snapshot |
|---|---|---|---|
| `inspect` | Read-only environment discovery and state inventory. | read | yes for mutation |
| `doctor` | Diagnose broken, risky, or platform-incompatible Spicetify state. | read | yes for mutation |
| `snapshot` | Capture restorable user Spicetify config/assets state before mutation. | medium | yes for mutation |
| `restore` | Restore a named snapshot with pre-restore guard snapshot. | medium/high | yes for mutation |
| `repair` | Run staged repair playbooks, especially after Spotify updates. | medium/high | yes for mutation |
| `apply` | Execute an approved dry-run plan exactly as reviewed. | medium/high | yes for mutation |
| `config` | Inspect, diff, and safely edit `config-xpui.ini`. | medium | yes for mutation |
| `profile` | Export and switch exact desired customization profiles. | medium | yes for mutation |
| `theme` | Create, validate, install, switch, watch, audit, or uninstall themes. | medium | yes for mutation |
| `extension` | Scaffold, build, audit, install, enable, debug, disable, or remove extensions. | medium | yes for mutation |
| `custom-app` | Scaffold, build, install, enable, debug, disable, or remove custom apps. | medium | yes for mutation |
| `snippet` | Create, audit, install, group, enable, disable, or migrate CSS snippets. | medium | yes for mutation |
| `marketplace` | Inspect Marketplace presence and audit Marketplace-style repos safely. | medium | yes for mutation |
| `audit` | Static security/provenance/compatibility review of local or staged assets. | read | yes for mutation |
| `devtools` | Enable and use debugging safely with consent and redaction. | medium/high | yes for mutation |
| `watch` | Run bounded development watch loops for trusted local projects/themes. | medium/high | yes for mutation |
| `migrate` | Convert ad hoc state into manifests/profiles or migrate /spicetify schema compatibility states. | medium | yes for mutation |
| `update` | Disambiguate hot reload, CLI upgrade planning, and post-Spotify-update repair. | medium/high | yes for mutation |
| `rollback` | Return to last-known-good or a selected snapshot. | medium/high | yes for mutation |
| `uninstall` | Safely remove skill-managed assets or produce manual full-uninstall plans. | medium/high | yes for mutation |
| `report` | Produce shareable redacted operation, audit, doctor, or profile reports. | read | yes for mutation |
| `evolve` | Review redacted eval results and skill-use evidence to propose eval-first improvements. | read/medium | no direct mutation |

Each mode has a dedicated file under `docs/planning/add-spicetify-skill/modes/` with inputs, preconditions, files touched, safety, plan, execution, verification, rollback, prompts, and structured response.
