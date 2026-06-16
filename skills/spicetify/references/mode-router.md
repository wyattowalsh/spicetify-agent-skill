# Mode Router

Use this table to map user intent to `/spicetify` modes.

| User intent | Mode |
|---|---|
| What is installed? What paths, config, assets, and snapshots exist? | `inspect` |
| What is broken? Why did Marketplace, CSS, extensions, or themes stop working? | `doctor` |
| Save current state before changes | `snapshot` |
| Restore a named snapshot or backup | `restore` |
| Spotify updated and Spicetify broke | `repair` |
| Execute a previously approved dry-run plan | `apply` |
| Change a config key or list | `config` |
| Switch minimal, visual, or development setup | `profile` |
| Create, install, switch, or remove a theme | `theme` |
| Scaffold, audit, enable, or disable an extension | `extension` |
| Scaffold, audit, enable, or disable a custom app | `custom-app` |
| Add or manage a CSS snippet | `snippet` |
| Inspect or audit Marketplace assets | `marketplace` |
| Review third-party JavaScript, CSS, manifest, or README content | `audit` |
| Collect debug logs, DevTools evidence, or screenshots | `devtools` |
| Hot reload local development changes | `watch` |
| Export or migrate a setup | `migrate` |
| Plan CLI upgrades or post-update repair | `update` |
| Return to last-known-good | `rollback` |
| Remove assets or customizations | `uninstall` |
| Share diagnostics or operation evidence | `report` |
| Review eval results or skill-use evidence to improve `/spicetify` safely | `evolve` |

Mode combinations are allowed, but mutation still requires one plan hash, one snapshot policy, and one explicit confirmation flow.
