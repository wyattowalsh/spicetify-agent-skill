# /spicetify safety policy

**Path:** `skills/spicetify/references/safety-policy.md`
**Purpose:** Compact safety policy for the skill router.
**Status:** Proposed
**Load/use when:** Any request might mutate local state, execute commands, inspect logs, install third-party code, or repair Spotify/Spicetify.

## Default stance

- Dry-run first for any possible mutation.
- No arbitrary shell or user-provided command passthrough.
- Snapshot before mutation.
- Verify after mutation.
- Rollback path required before execution.
- Third-party code is untrusted until staged, audited, and provenance-locked.

## Approval gates

| Gate | Examples |
|---|---|
| No approval | read-only inspect, doctor without logs, static local audit. |
| Snapshot + confirmation | config/theme/profile apply, generated local extension enable. |
| Separate confirmation | `spicetify restore`, fallback repair, DevTools launch flags, third-party JS enable, uninstall/delete. |
| Manual-only | package-manager commands, permission changes, install scripts, shortcut edits, publishing. |
| Block | arbitrary shell, secret exfiltration, DRM/account/ad bypass. |

## Redaction

Never include secrets, tokens, cookies, auth headers, real credentials, or Spotify prefs contents in reports. DevTools logs and screenshots are opt-in and redacted.


## Manifest, privacy, and automation guardrails

- Desired-state manifests are declarative data, not scripts.
- Manifests and policy presets cannot disable no-shell, snapshot, provenance, audit, redaction, or confirmation invariants.
- Logs, screenshots, launch flags, and shareable reports require consent and redaction policy.
- Headless automation may dry-run and report but cannot auto-approve blocked or high-risk actions.
