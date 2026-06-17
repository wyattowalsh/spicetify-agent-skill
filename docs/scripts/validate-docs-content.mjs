import { existsSync, readFileSync, readdirSync } from "node:fs";
import { extname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));
const contentRoot = join(root, "content", "docs");
const modeRoot = join(
  repoRoot,
  "docs",
  "content",
  "docs",
  "archive",
  "add-spicetify-skill",
  "modes"
);
const schemaRoot = join(repoRoot, "skills", "spicetify", "assets", "schemas");

const requiredPages = [
  "index.mdx",
  "quickstart.mdx",
  "concepts/safety-model.mdx",
  "modes/index.mdx",
  "reference/schemas.mdx",
  "reference/openspec.mdx",
  "reference/modes.mdx",
  "workflows/post-spotify-update-repair.mdx",
  "workflows/audit-extension.mdx",
  "security/blocked-actions.mdx",
  "reference/index.mdx",
  "reference/schemas.mdx",
  "reference/openspec.mdx",
  "reference/modes.mdx",
  "docs-site/implementation-boundary.mdx"
];

const forbiddenPatterns = [
  [/sk-[A-Za-z0-9_-]{20,}/, "OpenAI-style API token"],
  [/xox[baprs]-[A-Za-z0-9-]+/, "Slack-style token"],
  [/gh[pousr]_[A-Za-z0-9_]+/, "GitHub-style token"],
  [/spotify\.com\/prefs/i, "Spotify prefs content"],
  [/\/Users\/(?!ww\/dev\/projects\/spicetify-agent-skill\b)[^\s)]+/, "private local user path"],
  [/%appdata%\\spotify/i, "real Spotify appdata path"]
];

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function slugFromSchema(fileName) {
  return fileName.replace(/\.schema\.json$/, "").replace(/\.json$/, "");
}

function assertUnique(items, label) {
  const seen = new Set();
  for (const item of items) {
    if (seen.has(item)) {
      throw new Error(`${label} contains duplicate entry ${item}`);
    }
    seen.add(item);
  }
}

function assertSameSet(actual, expected, label) {
  const actualSorted = [...actual].sort();
  const expectedSorted = [...expected].sort();
  if (actualSorted.join("\n") !== expectedSorted.join("\n")) {
    const missing = expectedSorted.filter((entry) => !actualSorted.includes(entry));
    const extra = actualSorted.filter((entry) => !expectedSorted.includes(entry));
    throw new Error(
      `${label} drift: missing [${missing.join(", ")}], extra [${extra.join(", ")}]`
    );
  }
}

function parseFrontmatter(text, file) {
  if (!text.startsWith("---\n")) {
    throw new Error(`${file}: missing YAML frontmatter`);
  }
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) {
    throw new Error(`${file}: unterminated YAML frontmatter`);
  }
  const raw = text.slice(4, end).trim();
  const values = Object.fromEntries(
    raw.split("\n").filter(Boolean).map((line) => {
      const index = line.indexOf(":");
      if (index === -1) {
        throw new Error(`${file}: invalid frontmatter line "${line}"`);
      }
      return [line.slice(0, index).trim(), line.slice(index + 1).trim().replace(/^"|"$/g, "")];
    })
  );
  const required = ["title", "description", "section", "source", "sourcePath", "owner", "status", "safetyLevel"];
  for (const key of required) {
    if (!values[key]) {
      throw new Error(`${file}: missing frontmatter key ${key}`);
    }
  }
  return values;
}

for (const page of requiredPages) {
  readFileSync(join(contentRoot, page), "utf8");
}

const manifest = readJson(join(root, "docs-site-manifest.json"));
if (manifest.site !== "/spicetify-docs" || manifest.appRoot !== "docs") {
  throw new Error("docs-site-manifest.json does not describe the approved docs app root");
}
if (manifest.safety?.noSecrets !== true || manifest.safety?.noDeploymentWithoutApproval !== true) {
  throw new Error("docs-site-manifest.json is missing required safety gates");
}
for (const route of ["/", "/docs", "/docs/[[...slug]]", "/llms.txt", "/llms-full.txt"]) {
  if (!manifest.routes?.includes(route)) {
    throw new Error(`docs-site-manifest.json missing route ${route}`);
  }
}

const contentMap = readJson(join(root, "content-map.json"));
if (!Array.isArray(contentMap.modePages) || contentMap.modePages.length < 23) {
  throw new Error("content-map.json must list all 23 /spicetify mode pages");
}
if (contentMap.redaction?.syntheticExamplesOnly !== true || contentMap.redaction?.noPrefsContent !== true) {
  throw new Error("content-map.json must require synthetic examples and omit prefs content");
}
assertUnique(contentMap.sections.map((section) => section.slug), "content-map sections");
assertUnique(contentMap.modePages, "content-map modePages");
assertUnique(contentMap.schemaPages, "content-map schemaPages");
for (const section of contentMap.sections) {
  for (const page of section.pages) {
    if (!existsSync(join(contentRoot, `${page}.mdx`))) {
      throw new Error(`content-map section ${section.slug} references missing page ${page}`);
    }
  }
}
const expectedModes = readdirSync(modeRoot)
  .filter((fileName) => fileName.endsWith(".mdx"))
  .map((fileName) => fileName.replace(/\.mdx$/, ""));
const expectedSchemas = readdirSync(schemaRoot)
  .filter((fileName) => fileName.endsWith(".json"))
  .map(slugFromSchema);
assertSameSet(contentMap.modePages, expectedModes, "content-map modePages");
assertSameSet(contentMap.schemaPages, expectedSchemas, "content-map schemaPages");

const files = walk(contentRoot).filter((file) => extname(file) === ".mdx");
for (const file of files) {
  const text = readFileSync(file, "utf8");
  const display = relative(repoRoot, file);
  const frontmatter = parseFrontmatter(text, display);
  if (frontmatter.sourcePath.includes("..")) {
    throw new Error(`${display}: sourcePath must be repo-relative without parent traversal`);
  }
  if (/\bTBD\b|\{\{[^}]+\}\}/.test(text)) {
    throw new Error(`${display}: unresolved placeholder text`);
  }
  for (const [pattern, label] of forbiddenPatterns) {
    if (pattern.test(text)) {
      throw new Error(`${display}: contains ${label}`);
    }
  }
}

console.log(`docs content ok: ${files.length} mdx pages`);
