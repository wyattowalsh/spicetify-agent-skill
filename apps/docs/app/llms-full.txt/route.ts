import { docsSource } from "../../lib/source";
import { getContentMap, listDocsPages } from "../../lib/content";

export function GET() {
  const contentMap = getContentMap();
  const pages = listDocsPages();
  const body = [
    "# /spicetify full docs index",
    "",
    "This route is generated from stable docs metadata only. It excludes local reports, logs, screenshots, prefs, and live Spicetify state.",
    "",
    `Content root: ${docsSource.root}`,
    `Generated references: ${docsSource.generatedReferences.join(", ")}`,
    "",
    `Modes: ${contentMap.modePages.join(", ")}`,
    "",
    ...pages.flatMap((page) => [
      `## ${page.title}`,
      "",
      `Source: ${page.sourcePath}`,
      `Route: ${page.href}`,
      "",
      page.body,
      "",
    ]),
  ].join("\n");

  return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8" } });
}
