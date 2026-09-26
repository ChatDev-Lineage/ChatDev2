#!/usr/bin/env python3
"""Read-only Kilo ChatDev factory/portfolio scout.

Answers what this checkout/machine can contribute to a ChatDev game-development
run without starting services, installing packages, invoking models, or mutating
repositories. "Not detected here" is UNKNOWN, never global absence.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "config" / "kilo_game_factory.json"

TOOL_GROUPS: dict[str, tuple[str, ...]] = {
    "source": ("git", "gh", "rg"),
    "python": ("python", "py", "uv", "aider"),
    "javascript": ("node", "npm", "pnpm"),
    "agents": ("claude", "codex", "goose", "openclaw"),
    "runtime": ("docker", "ollama", "wsl"),
    "game": ("godot", "godot4", "blender"),
    "context": ("repomix", "obsidian-cli"),
    "cli_anything": ("cli-hub",),
    "windows": (
        "powershell", "pwsh", "winget", "procmon", "procmon64", "procdump",
        "procdump64", "autoruns", "autorunsc", "sigcheck", "handle", "psping",
        "tcpview", "rammap", "vmmap", "procexp", "procexp64", "streams", "listdlls",
    ),
    "powertoys": ("PowerToys", "PowerToys.CommandPalette"),
}

CONTRACT_MARKERS: tuple[tuple[str, str], ...] = (
    ("project.godot", "godot"), ("pyproject.toml", "python"),
    ("requirements.txt", "python"), ("package.json", "javascript"),
    ("Makefile", "make"), ("docker-compose.yml", "compose"),
    ("compose.yaml", "compose"), ("AGENTS.md", "agent_guidance"),
    ("CLAUDE.md", "agent_guidance"), ("README.md", "readme"),
    ("tests", "tests"), ("test", "tests"), ("tools/p144.py", "semantic_cli"),
    ("agent-harness", "cli_anything_harness"), (".gsv", "gsv"),
)

@dataclass(frozen=True)
class GitSnapshot:
    ok: bool
    branch: str | None = None
    head: str | None = None
    dirty: bool | None = None
    remote: str | None = None
    error: str | None = None


def _run(args: list[str], *, cwd: Path | None = None, timeout: float = 2.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(cwd) if cwd else None, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout,
                          check=False)


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "kilo.chatdev.game-portfolio/v1":
        raise ValueError("unsupported or missing portfolio schema")
    projects = payload.get("projects")
    if not isinstance(projects, list) or not projects:
        raise ValueError("portfolio must contain at least one project")
    seen: set[str] = set()
    for project in projects:
        if not isinstance(project, dict):
            raise ValueError("project entries must be objects")
        project_id, repo = project.get("id"), project.get("repo")
        if not isinstance(project_id, str) or not project_id:
            raise ValueError("every project needs an id")
        if project_id in seen:
            raise ValueError(f"duplicate project id: {project_id}")
        seen.add(project_id)
        if not isinstance(repo, str) or "/" not in repo:
            raise ValueError(f"project {project_id} needs owner/repo")
    return payload


def detect_tools(which=shutil.which) -> dict[str, Any]:
    return {
        group: {name: {"detected": (resolved := which(name)) is not None, "path": resolved}
                for name in names}
        for group, names in TOOL_GROUPS.items()
    }


def _expand_candidate(candidate: str, *, active_root: Path | None) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(candidate))
    if "{ACTIVE_ROOT}" in expanded:
        root = active_root or Path(os.environ.get("KILO_ACTIVE_ROOT", r"C:\dev\Active"))
        expanded = expanded.replace("{ACTIVE_ROOT}", str(root))
    return Path(expanded)


def resolve_project_path(project: dict[str, Any], *, active_root: Path | None = None) -> tuple[Path | None, list[str]]:
    checked: list[str] = []
    env_name = project.get("path_env")
    if isinstance(env_name, str) and (value := os.environ.get(env_name)):
        path = Path(os.path.expanduser(os.path.expandvars(value)))
        checked.append(str(path))
        if path.exists():
            return path, checked
    for raw in project.get("local_candidates", []):
        if not isinstance(raw, str):
            continue
        path = _expand_candidate(raw, active_root=active_root)
        checked.append(str(path))
        if path.exists():
            return path, checked
    return None, checked


def git_snapshot(path: Path) -> GitSnapshot:
    if not (path / ".git").exists():
        return GitSnapshot(ok=False, error="not_git_checkout")
    try:
        head = _run(["git", "rev-parse", "HEAD"], cwd=path)
        branch = _run(["git", "branch", "--show-current"], cwd=path)
        status = _run(["git", "status", "--porcelain"], cwd=path)
        remote = _run(["git", "remote", "get-url", "origin"], cwd=path)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return GitSnapshot(ok=False, error=f"{type(exc).__name__}: {exc}")
    if head.returncode != 0:
        return GitSnapshot(ok=False, error=head.stderr.strip()[-240:] or "git_rev_parse_failed")
    return GitSnapshot(ok=True, branch=branch.stdout.strip() or None, head=head.stdout.strip(),
                       dirty=bool(status.stdout.strip()) if status.returncode == 0 else None,
                       remote=remote.stdout.strip() if remote.returncode == 0 else None)


def contract_markers(path: Path) -> list[dict[str, str]]:
    return [{"path": relative, "kind": kind} for relative, kind in CONTRACT_MARKERS
            if (path / relative).exists()]


def project_report(project: dict[str, Any], *, active_root: Path | None = None) -> dict[str, Any]:
    path, checked = resolve_project_path(project, active_root=active_root)
    report: dict[str, Any] = {
        "id": project["id"], "repo": project["repo"], "engine": project.get("engine"),
        "harvest_role": project.get("harvest_role"), "priority": project.get("priority"),
        "declared": {"semantic_cli": project.get("semantic_cli"),
                     "native_checks": project.get("native_checks", []),
                     "chatdev_roles": project.get("chatdev_roles", [])},
        "local": {"detected": path is not None, "path": str(path) if path else None, "checked": checked},
        "contracts": [], "git": None,
    }
    if path is not None:
        report["contracts"] = contract_markers(path)
        report["git"] = asdict(git_snapshot(path))
    return report


def build_report(manifest_path: Path, *, active_root: Path | None = None) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    projects = [project_report(p, active_root=active_root) for p in manifest["projects"]]
    tools = detect_tools()
    return {
        "schema": "kilo.chatdev.factory-scout/v1", "mode": "read-only",
        "authority_granted": False, "manifest": str(manifest_path),
        "host": {"platform": sys.platform, "python": sys.version.split()[0]},
        "summary": {
            "projects_declared": len(projects),
            "projects_detected_local": sum(1 for p in projects if p["local"]["detected"]),
            "tools_detected": sum(1 for entries in tools.values() for item in entries.values() if item["detected"]),
            "tools_checked": sum(len(entries) for entries in tools.values()),
        },
        "tools": tools, "projects": projects,
        "notes": [
            "not detected on this host != absent from the fleet",
            "installed/path detected != semantically ready",
            "portfolio declaration != repository evidence",
            "this scout never starts services, installs software, invokes models, or mutates repositories",
        ],
    }


def _human(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = ["ChatDev Kilo Factory Scout",
             f"projects local: {summary['projects_detected_local']}/{summary['projects_declared']}",
             f"tools detected: {summary['tools_detected']}/{summary['tools_checked']}", "", "Projects:"]
    for project in report["projects"]:
        state = "LOCAL" if project["local"]["detected"] else "UNKNOWN"
        markers = ",".join(m["kind"] for m in project["contracts"]) or "-"
        lines.append(f"  {state:7} {project['id']:<22} {project['repo']} [{markers}]")
    lines.extend(["", "Detected tool groups:"])
    for group, entries in report["tools"].items():
        names = [name for name, item in entries.items() if item["detected"]]
        if names:
            lines.append(f"  {group}: {', '.join(names)}")
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--active-root", help="Override Kilo active-repository root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", help="Optional JSON receipt path")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = build_report(Path(args.manifest).expanduser().resolve(),
                              active_root=Path(args.active_root).expanduser().resolve() if args.active_root else None)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"factory scout error: {exc}", file=sys.stderr)
        return 2
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else _human(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
