# Examples

**Path:** `skills/spicetify/references/examples.md`
**Purpose:** Prompt and response examples for the /spicetify skill.
**Status:** Draft
**Load/use when:** Use for regression and UX design.


## Repair

`/spicetify Spotify updated and Spicetify broke, fix it.`

Return a dry-run repair plan with inspect, doctor, snapshot, backup, apply, verify, and confirmation-gated fallback.

## Theme

`/spicetify create a dark terminal-style theme.`

Return a theme creation plan with generated files, config diff, snapshot requirement, verification, and rollback.

## Audit

`/spicetify audit this extension before enabling it.`

Return an audit report and do not enable unless verdict and confirmation allow it.

## Profile

`/spicetify switch from minimal to dev profile.`

Return exact add/remove config diff and snapshot requirement.

## Docs site examples

The accompanying Fumadocs site should show examples as documentation only. It may render fake operation plans, fake audit reports, and fake rollback reports. It must not embed real local user reports, private paths, screenshots, DevTools logs, or Spotify prefs content unless a human explicitly provided redacted examples for documentation.
