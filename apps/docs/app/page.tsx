import { RiskBadge } from "../components/spicetify/risk-badge";

const modes = [
  "inspect",
  "doctor",
  "audit",
  "snapshot",
  "apply",
  "rollback",
  "repair",
  "theme",
  "extension",
  "custom-app",
  "snippet",
  "marketplace",
  "devtools",
  "watch",
  "update",
];

export default function HomePage() {
  return (
    <main className="page">
      <section className="intro">
        <p className="eyebrow">/spicetify</p>
        <h1>Dry-run-first Spicetify operations</h1>
        <p>
          A local operator and Skill for planning, auditing, snapshotting, applying, verifying,
          reporting, and rolling back Spicetify customizations without arbitrary shell access.
        </p>
      </section>
      <section className="grid" aria-label="Safety properties">
        <RiskBadge level="read" label="Read probes first" />
        <RiskBadge level="medium" label="Snapshot before mutation" />
        <RiskBadge level="high" label="High-risk actions need confirmation" />
        <RiskBadge level="blocked" label="Shell passthrough blocked" />
      </section>
      <section>
        <h2>Mode catalog</h2>
        <ul className="modes">
          {modes.map((mode) => (
            <li key={mode}>{mode}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
