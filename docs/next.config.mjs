import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const docsRoot = dirname(fileURLToPath(import.meta.url));
const workspaceRoot = resolve(docsRoot, "..");

const nextConfig = {
  turbopack: {
    root: workspaceRoot
  }
};

export default nextConfig;
