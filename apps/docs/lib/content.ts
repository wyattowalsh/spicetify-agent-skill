import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative, sep } from "node:path";

export type DocsSection = {
  slug: string;
  title: string;
  pages: string[];
};

export type DocsContentMap = {
  sections: DocsSection[];
  modePages: string[];
  workflowPages: string[];
  schemaPages: string[];
  redaction: {
    syntheticExamplesOnly: true;
    noPrefsContent: true;
  };
};

export type DocsPage = {
  slug: string;
  href: string;
  title: string;
  description: string;
  sourcePath: string;
  body: string;
};

const docsRoot = process.cwd();
const contentRoot = join(docsRoot, "content", "docs");

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function stripFrontmatter(text: string): { metadata: Record<string, string>; body: string } {
  if (!text.startsWith("---\n")) {
    return { metadata: {}, body: text };
  }
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) {
    return { metadata: {}, body: text };
  }
  const metadata = Object.fromEntries(
    text
      .slice(4, end)
      .trim()
      .split("\n")
      .filter(Boolean)
      .map((line) => {
        const index = line.indexOf(":");
        return [line.slice(0, index).trim(), line.slice(index + 1).trim().replace(/^"|"$/g, "")];
      }),
  );
  return { metadata, body: text.slice(end + "\n---\n".length).trim() };
}

function slugToFile(slug: string): string {
  const normalized = slug === "" ? "index" : slug.replace(/^\/+|\/+$/g, "");
  if (normalized.includes("..") || normalized.split("/").some((part) => part === "")) {
    throw new Error(`invalid docs slug: ${slug}`);
  }
  return join(contentRoot, `${normalized}.mdx`);
}

function walkMdx(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walkMdx(path) : [path];
  });
}

export function getContentMap(): DocsContentMap {
  return readJson<DocsContentMap>(join(docsRoot, "content-map.json"));
}

export function listDocsPages(): DocsPage[] {
  return walkMdx(contentRoot)
    .filter((file) => file.endsWith(".mdx"))
    .map((file) => {
      const slug = relative(contentRoot, file).replaceAll(sep, "/").replace(/\.mdx$/, "");
      return readDocsPage(slug === "index" ? "" : slug);
    })
    .sort((a, b) => a.href.localeCompare(b.href));
}

export function readDocsPage(slug: string): DocsPage {
  const file = slugToFile(slug);
  if (!existsSync(file)) {
    throw new Error(`docs page not found: ${slug || "index"}`);
  }
  const { metadata, body } = stripFrontmatter(readFileSync(file, "utf8"));
  const normalizedSlug = slug === "index" ? "" : slug;
  return {
    slug: normalizedSlug,
    href: normalizedSlug ? `/docs/${normalizedSlug}` : "/docs",
    title: metadata.title ?? normalizedSlug,
    description: metadata.description ?? "",
    sourcePath: metadata.sourcePath ?? relative(docsRoot, file).replaceAll(sep, "/"),
    body,
  };
}

