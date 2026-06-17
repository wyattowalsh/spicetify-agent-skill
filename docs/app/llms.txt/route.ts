import { getContentMap } from "../../lib/content";

export function GET() {
  const contentMap = getContentMap();
  const body = [
    "# /spicetify",
    "",
    "Current release: v0.1.0.",
    "",
    "Safe local Spicetify operations through the spicetify-agent tool.",
    "",
    "- Dry-run-first plans",
    "- Snapshot before mutation",
    "- Allowlisted argv-only Spicetify commands",
    "- Third-party code audit and provenance",
    "- Redacted reports",
    "",
    `Modes: ${contentMap.modePages.join(", ")}`,
    `Docs: ${contentMap.sections.flatMap((section) => section.pages).map((page) => (page === "index" ? "/docs" : `/docs/${page}`)).join(", ")}`,
  ].join("\n");

  return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8" } });
}
