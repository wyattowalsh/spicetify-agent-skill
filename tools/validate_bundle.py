#!/usr/bin/env python3
"""Validate the /spicetify planning bundle.

Standard-library only. Does not read secrets or execute Spicetify.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import tomllib

CHANGE = "add-spicetify-skill"
RELEASE_VERSION = "0.1.0"
RELEASE_TAG = f"v{RELEASE_VERSION}"
SKIP_PARTS = {
    ".git",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp-clean-venv",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
ROOT_REQUIRED = [
    "README.md",
    "manifest.md",
    "agent-bundle.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    "AGENTS.md",
    "DESIGN.md",
    "openspec/config.yaml",
    f"openspec/changes/{CHANGE}/proposal.md",
    f"openspec/changes/{CHANGE}/design.md",
    f"openspec/changes/{CHANGE}/tasks.md",
    "skills/spicetify/SKILL.md",
    "evals/regression-prompts.json",
    "evals/spicetify-eval-suite.json",
]
APP_DOCS_REQUIRED = [
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
    "docs-site/implementation-boundary.mdx",
    "archive/add-spicetify-skill/index.mdx",
    "archive/add-spicetify-skill/plans.mdx",
    "archive/add-spicetify-skill/context-map.mdx",
    "archive/add-spicetify-skill/policy-matrix.mdx",
    "archive/add-spicetify-skill/validation.mdx",
    "archive/add-spicetify-skill/subagent-task-graph.mdx",
    "archive/add-spicetify-skill/codex-kickoff-prompt.mdx",
]
REQUIRED_SCRIPT_MODULES = {
    "spicetify_agent.py",
    "_asset_inspectors.py",
    "_asset_path_guard.py",
    "_asset_plans.py",
    "_asset_research.py",
    "_asset_sources.py",
    "_asset_templates.py",
    "_audit.py",
    "_commands.py",
    "_errors.py",
    "_intent_router.py",
    "_modes.py",
    "_platform.py",
    "_policy.py",
    "_privacy.py",
    "_provenance.py",
    "_reports.py",
    "_runner.py",
    "_safe_paths.py",
    "_schema_data.py",
    "_schemas.py",
    "_state.py",
    "_util.py",
    "_verify.py",
}
REQUIRED_SPEC_DOMAINS = {
    "skill",
    "agents",
    "command",
    "policy",
    "state",
    "platform",
    "config-profile",
    "customization",
    "audit",
    "provenance",
    "repair",
    "recovery",
    "devtools",
    "verification",
    "privacy",
    "manifest",
    "scaffold",
    "automation",
    "testing",
    "ux",
    "docs-site",
    "docs-content",
    "docs-ui",
}
REQUIRED_SCHEMAS = {
    "request.schema.json",
    "operation-plan.schema.json",
    "command-registry.schema.json",
    "command-invocation.schema.json",
    "policy.schema.json",
    "policy-decision.schema.json",
    "provenance-lock.schema.json",
    "audit-report.schema.json",
    "snapshot-manifest.schema.json",
    "profile.schema.json",
    "verification-report.schema.json",
    "operation-run.schema.json",
    "operation-report.schema.json",
    "confirmation.schema.json",
    "error.schema.json",
    "fixture-manifest.schema.json",
    "desired-state-manifest.schema.json",
    "asset-manifest.schema.json",
    "asset-analysis.schema.json",
    "asset-source.schema.json",
    "asset-workflow-plan.schema.json",
    "redaction-policy.schema.json",
    "consent-grant.schema.json",
    "intent-route.schema.json",
    "invariant.schema.json",
    "failure-recovery.schema.json",
    "docs-site-config.schema.json",
    "docs-site-content.schema.json",
    "docs-site-manifest.schema.json",
    "docs-page.schema.json",
    "subagent-task-graph.schema.json",
    "subagent-result.schema.json",
    "eval-case.schema.json",
    "eval-suite.schema.json",
    "eval-result.schema.json",
    "eval-trace.schema.json",
    "evolution-report.schema.json",
}
REQUIRED_MODES = {
    "inspect",
    "doctor",
    "snapshot",
    "restore",
    "repair",
    "apply",
    "config",
    "profile",
    "manifest",
    "theme",
    "extension",
    "custom-app",
    "snippet",
    "marketplace",
    "audit",
    "devtools",
    "watch",
    "migrate",
    "update",
    "rollback",
    "uninstall",
    "report",
}
REQUIRED_EVAL_MODES = REQUIRED_MODES | {"evolve"}
REQUIRED_WORKFLOWS = {
    "command-abstraction",
    "dry-run-planner",
    "state-snapshots-rollback",
    "config-profile",
    "theme",
    "extension-custom-app",
    "audit",
    "doctor-repair",
    "safety-boundaries",
    "verification",
    "manifest-automation",
    "fumadocs-site",
    "docs-site",
    "subagent-swarm",
}
REQUIRED_SKILL_REFERENCES = {
    "references/runtime.md",
    "references/mode-router.md",
    "references/research.md",
    "references/asset-workflows.md",
    "references/safety-policy.md",
    "references/troubleshooting.md",
    "references/spicetify-facts.md",
    "references/examples.md",
    "references/evals.md",
}
TASK_RE = re.compile(r"TASK-[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*")


def is_generated_path(path: pathlib.Path) -> bool:
    return (
        path.name.endswith(".tsbuildinfo")
        or any(part in SKIP_PARTS for part in path.parts)
        or any(part.endswith(".egg-info") for part in path.parts)
    )


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: pathlib.Path) -> dict[str, object]:
    return json.loads(read(path))


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_source_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and not is_generated_path(p))


def generated_manifest(root: pathlib.Path, files: list[pathlib.Path]) -> dict[str, object]:
    entries = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel == "manifest.generated.json":
            continue
        entries.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)})
    return {
        "root": ".",
        "file_count": len(entries),
        "flat": False,
        "self_hash_note": "manifest.generated.json omits its own hash to avoid self-reference",
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--json", action="store_true", help="accepted for compatibility; output is always JSON"
    )
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="rewrite manifest.generated.json from the current source tree before validating",
    )
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    files = iter_source_files(root)
    expected_manifest = generated_manifest(root, files)
    manifest_path = root / "manifest.generated.json"
    if args.write_manifest:
        manifest_path.write_text(json.dumps(expected_manifest, indent=2) + "\n", encoding="utf-8")

    for rel in ROOT_REQUIRED:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")

    if (root / "docs").exists():
        errors.append("root docs/ must be migrated into apps/docs and removed")

    docs_content_root = root / "apps" / "docs" / "content" / "docs"
    planning = docs_content_root / "archive" / CHANGE
    for rel in APP_DOCS_REQUIRED:
        if not (docs_content_root / rel).exists():
            errors.append(f"missing apps/docs/content/docs/{rel}")

    scripts_dir = root / "skills" / "spicetify" / "scripts"
    found_script_modules = (
        {p.name for p in scripts_dir.glob("*.py")} if scripts_dir.exists() else set()
    )
    missing_script_modules = sorted(REQUIRED_SCRIPT_MODULES - found_script_modules)
    extra_script_modules = sorted(found_script_modules - REQUIRED_SCRIPT_MODULES)
    if missing_script_modules:
        errors.append("missing skill script modules: " + ", ".join(missing_script_modules))
    if extra_script_modules:
        warnings.append("extra skill script modules: " + ", ".join(extra_script_modules))

    specs_dir = root / "openspec/changes" / CHANGE / "specs"
    specs = sorted(specs_dir.glob("*/spec.md")) if specs_dir.exists() else []
    domains = {p.parent.name for p in specs}
    missing_domains = sorted(REQUIRED_SPEC_DOMAINS - domains)
    extra_domains = sorted(domains - REQUIRED_SPEC_DOMAINS)
    if missing_domains:
        errors.append("missing spec domains: " + ", ".join(missing_domains))
    if extra_domains:
        warnings.append("extra spec domains: " + ", ".join(extra_domains))
    for spec in specs:
        text = read(spec)
        rel = spec.relative_to(root)
        if "### Requirement:" not in text:
            errors.append(f"{rel} lacks `### Requirement:`")
        if "#### Scenario:" not in text:
            errors.append(f"{rel} lacks `#### Scenario:`")
        if re.search(r"^###\s+REQ-", text, re.M):
            errors.append(f"{rel} uses REQ heading instead of Requirement heading")
        reqs = re.findall(r"^### Requirement: (.+)$", text, re.M)
        duplicates = sorted({r for r in reqs if reqs.count(r) > 1})
        if duplicates:
            errors.append(f"{rel} has duplicate requirement headings: " + ", ".join(duplicates))
        if "MUST" not in text and "SHALL" not in text:
            warnings.append(f"{rel} lacks normative MUST/SHALL wording")

    schemas_dir = root / "schemas"
    found_schemas = {p.name for p in schemas_dir.glob("*.json")} if schemas_dir.exists() else set()
    missing_schemas = sorted(REQUIRED_SCHEMAS - found_schemas)
    if missing_schemas:
        errors.append("missing schemas: " + ", ".join(missing_schemas))
    for path in sorted(root.rglob("*.json")):
        if is_generated_path(path):
            continue
        try:
            json.loads(read(path))
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(root)}: {exc}")
    if manifest_path.exists():
        actual_manifest = json.loads(read(manifest_path))
        if actual_manifest != expected_manifest:
            errors.append(
                "manifest.generated.json is stale; run "
                "`python3 tools/validate_bundle.py --root . --write-manifest`"
            )

    eval_suite_path = root / "evals/spicetify-eval-suite.json"
    if eval_suite_path.exists():
        eval_suite = json.loads(read(eval_suite_path))
        cases = eval_suite.get("cases")
        mode_coverage = eval_suite.get("modeCoverage")
        if not isinstance(cases, list):
            errors.append("evals/spicetify-eval-suite.json cases must be an array")
            cases = []
        if not isinstance(mode_coverage, list):
            errors.append("evals/spicetify-eval-suite.json modeCoverage must be an array")
            mode_coverage = []
        covered_modes = {str(mode) for mode in mode_coverage}
        case_modes = {
            str(case.get("mode"))
            for case in cases
            if isinstance(case, dict) and isinstance(case.get("mode"), str)
        }
        missing_eval_modes = sorted(REQUIRED_EVAL_MODES - (covered_modes & case_modes))
        if missing_eval_modes:
            errors.append("eval suite missing modes: " + ", ".join(missing_eval_modes))
        if "evolve" not in case_modes:
            errors.append("eval suite must include an evolve mode case")
        ids = [
            str(case.get("id"))
            for case in cases
            if isinstance(case, dict) and isinstance(case.get("id"), str)
        ]
        duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
        if duplicate_ids:
            errors.append("eval suite duplicate case ids: " + ", ".join(duplicate_ids))
        fixture_dir = root / "tests/fixtures/evals"
        fixture_ids = (
            {p.parent.name for p in fixture_dir.glob("*/fixture.json")}
            if fixture_dir.exists()
            else set()
        )
        referenced_fixtures = {
            str(case.get("fixture"))
            for case in cases
            if isinstance(case, dict) and isinstance(case.get("fixture"), str)
        }
        missing_fixtures = sorted(referenced_fixtures - fixture_ids)
        unused_fixtures = sorted(fixture_ids - referenced_fixtures)
        if missing_fixtures:
            errors.append("eval suite references missing fixtures: " + ", ".join(missing_fixtures))
        if unused_fixtures:
            errors.append("eval fixtures unused by suite: " + ", ".join(unused_fixtures))
        for case in cases:
            if not isinstance(case, dict):
                continue
            case_id = str(case.get("id", "<unknown>"))
            activation = case.get("activation")
            if not isinstance(activation, dict) or activation.get("kind") not in {
                "direct-mode",
                "route-mode",
                "negative-trigger",
            }:
                errors.append(f"eval case {case_id} missing activation.kind")
            trace_oracle = case.get("traceOracle")
            if not isinstance(trace_oracle, dict) or trace_oracle.get("match") not in {
                "exact",
                "contains-in-order",
                "unordered-subset",
                "forbidden",
            }:
                errors.append(f"eval case {case_id} missing structured traceOracle")
            expected = case.get("expected") if isinstance(case.get("expected"), dict) else {}
            if (
                isinstance(expected, dict)
                and "fake-execute" in expected.get("trace", [])
                and expected.get("executeFake") is not True
            ):
                errors.append(f"eval case {case_id} has fake-execute without executeFake")

    modes_dir = planning / "modes"
    modes = {p.stem for p in modes_dir.glob("*.mdx")} if modes_dir.exists() else set()
    if sorted(REQUIRED_MODES - modes):
        errors.append("missing mode docs: " + ", ".join(sorted(REQUIRED_MODES - modes)))
    for mode in sorted(REQUIRED_MODES & modes):
        text = read(modes_dir / f"{mode}.mdx")
        for marker in [
            "## Purpose",
            "## Inputs",
            "## Preconditions",
            "## Plan output",
            "## Verification flow",
            "## Rollback flow",
        ]:
            if marker not in text:
                warnings.append(f"mode {mode} missing marker {marker}")

    workflows_dir = planning / "workflows"
    workflows = {p.stem for p in workflows_dir.glob("*.mdx")} if workflows_dir.exists() else set()
    if sorted(REQUIRED_WORKFLOWS - workflows):
        errors.append("missing workflows: " + ", ".join(sorted(REQUIRED_WORKFLOWS - workflows)))

    tasks = root / f"openspec/changes/{CHANGE}/tasks.md"
    if tasks.exists():
        t = read(tasks)
        if len(TASK_RE.findall(t)) < 10:
            warnings.append("tasks.md has fewer than 10 task IDs")
        for marker in ["Write scope", "Validation", "Done when"]:
            if marker not in t:
                errors.append(f"tasks.md missing {marker}")
    skill = root / "skills/spicetify/SKILL.md"
    if skill.exists():
        s = read(skill)
        if "/spicetify" not in s:
            errors.append("skill docs must mention /spicetify")
        if "name: spicetify" not in s or "description:" not in s:
            errors.append("skill frontmatter must include name and description")
        if len(s) > 9000:
            warnings.append("SKILL.md is large; keep skill top-level compact")
        for ref in sorted(REQUIRED_SKILL_REFERENCES):
            if ref not in s:
                errors.append(f"SKILL.md missing installed-payload reference {ref}")
            if not (skill.parent / ref).exists():
                errors.append(f"missing installed-payload reference skills/spicetify/{ref}")
        if any(escaped in s for escaped in ["../", "../../"]):
            errors.append("SKILL.md references paths outside the installed skill payload")
        if "spicetify-agent" not in s:
            errors.append("skill docs must name spicetify-agent as the helper command")
        if "official Spicetify CLI" not in s:
            errors.append("skill docs must state that the official Spicetify CLI is external")

    skill_dir = root / "skills/spicetify"
    if skill_dir.exists():
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            if (
                is_generated_path(path)
                or path.suffix in {".pyc", ".pyo"}
                or ".egg-info" in path.parts
            ):
                continue
            text = read(path)
            if path.suffix in {".md", ".json", ".yaml", ".yml", ".css", ".ini"}:
                if "../" in text:
                    errors.append(f"{rel} contains a path escaping the installed skill payload")
                if "/Users/" in text or "\\Users\\" in text:
                    errors.append(f"{rel} contains a private local user path")
                if re.search(
                    r"(?im)^\s*(curl|bash|sh|sudo|chmod|npm|pnpm|brew|apt|winget)\b",
                    text,
                ):
                    errors.append(f"{rel} includes an executable installer/package-manager line")
            if path.suffix == ".py" and re.search(r"\bshell\s*=\s*True\b", text):
                errors.append(f"{rel} enables shell=True")
        bundled_upstream = [
            path.relative_to(root).as_posix()
            for path in skill_dir.rglob("*")
            if path.is_file() and path.name == "spicetify"
        ]
        if bundled_upstream:
            errors.append(
                "skill payload must not bundle official spicetify CLI: "
                + ", ".join(bundled_upstream)
            )

    bundle_manifest = root / "agent-bundle.json"
    if bundle_manifest.exists():
        bundle = json.loads(read(bundle_manifest))
        if bundle.get("components", {}).get("skills") != "./skills/":
            errors.append("agent-bundle.json must point components.skills to ./skills/")
        install = bundle.get("adapters", {}).get("agent-skills-cli", {}).get("install", "")
        if "--skill spicetify" not in install or "npx skills add" not in install:
            errors.append("agent-bundle.json must document npx skills add --skill spicetify")
    for rel in [".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]:
        plugin_path = root / rel
        if plugin_path.exists():
            plugin = json.loads(read(plugin_path))
            if plugin.get("skills") != "./skills/":
                errors.append(f"{rel} must point skills to ./skills/")
            if "mcpServers" in plugin:
                errors.append(f"{rel} must not add MCP authority for the single-skill package")
    plans_path = planning / "plans.mdx"
    if plans_path.exists() and "TBD" in read(plans_path):
        errors.append("PLANS.md contains TBD placeholders; keep resumable state explicit")

    design_root = root / "DESIGN.md"
    if design_root.exists():
        d = read(design_root)
        if "Fumadocs" not in d or "shadcn" not in d or "/spicetify" not in d:
            errors.append("DESIGN.md must mention Fumadocs, shadcn, and /spicetify")
    docs_plan = planning / "fumadocs-site-plan.mdx"
    if docs_plan.exists():
        dp = read(docs_plan)
        for marker in [
            "apps/docs",
            "shadcn",
            "Fumadocs",
            "llms.txt",
            "approval-gated",
            "Validation",
        ]:
            if marker not in dp:
                errors.append(f"fumadocs-site-plan.md missing {marker}")
    docs_design = planning / "docs-site-design-system.mdx"
    if docs_design.exists():
        dd = read(docs_design)
        for marker in ["shadcn/ui", "RiskBadge", "Accessibility", "Copy rules"]:
            if marker not in dd:
                errors.append(f"docs-site-design-system.md missing {marker}")
    docs_content = planning / "docs-content-architecture.mdx"
    if docs_content.exists():
        dc = read(docs_content)
        for marker in ["Generated content", "sourcePath", "No release labels", "LLM"]:
            if marker not in dc:
                errors.append(f"docs-content-architecture.md missing {marker}")

    subagent_graph = planning / "subagent-task-graph.mdx"
    if subagent_graph.exists():
        sg = read(subagent_graph)
        for marker in [
            "A0 repository-preflight",
            "A8 final-review-red-team",
            "Standard subagent result envelope",
            "Merge protocol",
            "Single-agent fallback",
        ]:
            if marker not in sg:
                errors.append(f"subagent-task-graph.md missing {marker}")
    kickoff = planning / "codex-kickoff-prompt.mdx"
    if kickoff.exists():
        kp = read(kickoff)
        for marker in [
            "Read first",
            "subagent-task-graph.md",
            "Allowed write scope",
            "Validation to run",
            "Stop and report",
            "Final response",
        ]:
            if marker not in kp:
                errors.append(f"codex-kickoff-prompt.md missing {marker}")
    agents_spec = root / f"openspec/changes/{CHANGE}/specs/agents/spec.md"
    if agents_spec.exists():
        at = read(agents_spec)
        for marker in [
            "Bounded Subagent Task Graph",
            "Parallel Work Scope Isolation",
            "Subagent Result Envelope",
            "Codex Kickoff Prompt",
            "Sequential Fallback",
        ]:
            if marker not in at:
                errors.append(f"agents spec missing {marker}")

    root_readme = root / "README.md"
    if root_readme.exists() and ("spicetify" + "-skill engine") in read(root_readme):
        warnings.append("root README still contains an alternate product name; use /spicetify")

    release_label_allowed_roots = {
        ".claude-plugin",
        ".codex-plugin",
        "apps",
        "skills",
    }
    release_label_allowed_files = {
        "AGENTS.md",
        "CHANGELOG.md",
        "DESIGN.md",
        "README.md",
        "RELEASE.md",
        "agent-bundle.json",
        "manifest.md",
        "package.json",
        "pyproject.toml",
        "uv.lock",
    }

    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        project = tomllib.loads(read(pyproject_path)).get("project", {})
        if project.get("version") != RELEASE_VERSION:
            errors.append(f"pyproject.toml must declare version {RELEASE_VERSION}")

    uv_lock = root / "uv.lock"
    if uv_lock.exists() and f'name = "spicetify-agent"\nversion = "{RELEASE_VERSION}"' not in read(
        uv_lock
    ):
        errors.append(f"uv.lock must record spicetify-agent {RELEASE_VERSION}")

    cli_path = root / "skills/spicetify/scripts/spicetify_agent.py"
    if cli_path.exists() and f'__version__ = "{RELEASE_VERSION}"' not in read(cli_path):
        errors.append(f"spicetify_agent.py must expose {RELEASE_VERSION}")

    for rel in [
        "agent-bundle.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        "package.json",
        "apps/docs/package.json",
    ]:
        path = root / rel
        if path.exists() and read_json(path).get("version") != RELEASE_VERSION:
            errors.append(f"{rel} must declare version {RELEASE_VERSION}")

    agent_meta = root / "skills/spicetify/agents/openai.yaml"
    if agent_meta.exists() and f'version: "{RELEASE_VERSION}"' not in read(agent_meta):
        errors.append(f"skills/spicetify/agents/openai.yaml must declare {RELEASE_VERSION}")

    for rel in [
        "README.md",
        "CHANGELOG.md",
        "RELEASE.md",
        "skills/spicetify/references/runtime.md",
        "apps/docs/content/docs/index.mdx",
        "apps/docs/content/docs/quickstart.mdx",
        "apps/docs/content/docs/reference/release-checklist.mdx",
    ]:
        path = root / rel
        if path.exists() and RELEASE_TAG not in read(path):
            errors.append(f"{rel} must mention {RELEASE_TAG}")

    def allows_release_label(path: pathlib.Path) -> bool:
        rel = path.relative_to(root)
        return (
            rel.name in release_label_allowed_files or rel.parts[0] in release_label_allowed_roots
        )

    forbidden_patterns = [
        (r"spicetify_skill_planning_bundle_" + "v", "release-labeled bundle filename"),
        (r"source-refresh-" + r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", "dated source-refresh filename"),
        (r"profile\.v[0-9]+\b", "release-style profile schema constant"),
        (r"provenance-lock\.v[0-9]+\b", "release-style provenance schema constant"),
    ]
    release_label_pattern = re.compile(r"\bv[0-9]+(?:\.[0-9]+)+\b")
    for path in root.rglob("*"):
        if not path.is_file() or is_generated_path(path) or path.name.endswith(".zip"):
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yaml", ".yml"}:
            continue
        text = read(path)
        if release_label_pattern.search(text) and not allows_release_label(path):
            errors.append(
                f"{path.relative_to(root)} contains release label outside release metadata/docs"
            )
            continue
        for pattern, label in forbidden_patterns:
            if re.search(pattern, text):
                errors.append(
                    f"{path.relative_to(root)} contains {label}; "
                    "keep the canonical bundle free of release labels"
                )
                break

    result = {
        "root": str(root),
        "file_count": len(files),
        "spec_count": len(specs),
        "schema_count": len(found_schemas),
        "mode_doc_count": len(modes),
        "workflow_doc_count": len(workflows),
        "eval_count": len(json.loads(read(root / "evals/regression-prompts.json")).get("evals", []))
        if (root / "evals/regression-prompts.json").exists()
        else 0,
        "errors": errors,
        "warnings": warnings,
        "valid": not errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
