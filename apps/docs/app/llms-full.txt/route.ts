import { docsSource } from "../../lib/source";

export function GET() {
  const body = [
    "# /spicetify full docs index",
    "",
    "This route is generated from stable docs metadata only. It excludes local reports, logs, screenshots, prefs, and live Spicetify state.",
    "",
    `Content root: ${docsSource.root}`,
    `Generated references: ${docsSource.generatedReferences.join(", ")}`,
    "",
    "Modes: inspect, doctor, audit, snapshot, restore, repair, apply, config, profile, theme, extension, custom-app, snippet, marketplace, devtools, watch, migrate, update, rollback, uninstall, report.",
  ].join("\n");

  return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8" } });
}
