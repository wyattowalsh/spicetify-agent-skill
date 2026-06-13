export function GET() {
  const body = [
    "# /spicetify",
    "",
    "Safe local Spicetify operations through the spicetify-agent tool.",
    "",
    "- Dry-run-first plans",
    "- Snapshot before mutation",
    "- Allowlisted argv-only Spicetify commands",
    "- Third-party code audit and provenance",
    "- Redacted reports",
  ].join("\n");

  return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8" } });
}
