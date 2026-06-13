import { readFileSync, readdirSync } from "node:fs";
import { extname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../../..", import.meta.url));
const lintRoots = ["app", "components", "content", "lib", "scripts"].map((dir) => join(appRoot, dir));
const sourceExtensions = new Set([".md", ".mdx", ".mjs", ".ts", ".tsx"]);
const forbidden = [
  [/\/Users\/(?!ww\/dev\/projects\/spicetify-agent-skill\b)[^\s"'`)]+/g, "private local path"],
  [/token[=:]+[A-Za-z0-9._~+/=-]{8,}/gi, "token-like literal"],
  [/from\s+["']node:child_process["']|require\(["']node:child_process["']\)/g, "child process import"],
];
const contentPlaceholders = [/\bTODO\b|\bTBD\b/g, "placeholder marker"];

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.name === ".next" || entry.name === "node_modules") return [];
    return entry.isDirectory() ? walk(path) : [path];
  });
}

const failures = [];
for (const root of lintRoots) {
  for (const file of walk(root)) {
    if (!sourceExtensions.has(extname(file))) continue;
    const text = readFileSync(file, "utf8");
    const display = relative(repoRoot, file);
    for (const [pattern, label] of forbidden) {
      pattern.lastIndex = 0;
      if (pattern.test(text)) failures.push(`${display}: ${label}`);
    }
    if (display.startsWith("apps/docs/content/")) {
      const [pattern, label] = contentPlaceholders;
      pattern.lastIndex = 0;
      if (pattern.test(text)) failures.push(`${display}: ${label}`);
    }
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log("docs lint ok");
