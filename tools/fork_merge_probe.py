"""Read-only fork merge admission: no checkout, merge, API call or service.

git merge-tree --write-tree creates disposable local Git objects, not a commit,
branch update, index entry, worktree edit or network operation.
Fetch upstream separately using an explicit public Git remote.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

def _git(*args: str, cwd: Path | None = None, allow_failure: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True,
        check=False, timeout=600,
    )
    if result.returncode and not allow_failure:
        raise RuntimeError("git " + " ".join(args[:3]) + " failed: " + result.stderr[:500])
    return result

def _changed(base: str, target: str, cwd: Path | None) -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z", base, target],
        cwd=cwd, capture_output=True, check=True, timeout=240,
    )
    return {s.decode("utf-8", errors="replace") for s in result.stdout.split(b"\0") if s}

def probe(fork: str, upstream: str, cwd: Path | None = None) -> tuple[dict, str]:
    """Report exact ancestry, path overlap and disposable merge-tree result."""
    fork_sha = _git("rev-parse", "--verify", f"{fork}^{{commit}}", cwd=cwd).stdout.strip()
    up_sha = _git("rev-parse", "--verify", f"{upstream}^{{commit}}", cwd=cwd).stdout.strip()
    base_run = _git("merge-base", fork_sha, up_sha, cwd=cwd, allow_failure=True)
    if base_run.returncode:
        raise RuntimeError("no common history; fork merge denied")
    base_sha = base_run.stdout.strip()
    ahead = int(_git("rev-list", "--count", f"{up_sha}..{fork_sha}", cwd=cwd).stdout)
    behind = int(_git("rev-list", "--count", f"{fork_sha}..{up_sha}", cwd=cwd).stdout)
    fork_paths = _changed(base_sha, fork_sha, cwd)
    up_paths = _changed(base_sha, up_sha, cwd)
    merge = _git("merge-tree", "--write-tree", fork_sha, up_sha,
                 cwd=cwd, allow_failure=True)
    if merge.returncode not in (0, 1):
        raise RuntimeError(f"merge-tree failed ({merge.returncode}): {merge.stderr[:500]}")
    combined = merge.stdout + ("\n" + merge.stderr if merge.stderr else "")
    report = {
        "schema": "gsv.fork-sync-preflight/v1",
        "authority": "LOCAL_GIT_HISTORY_ONLY",
        "fork_sha": fork_sha, "upstream_sha": up_sha,
        "merge_base_sha": base_sha, "ahead": ahead, "behind": behind,
        "fork_touched_files": len(fork_paths),
        "upstream_touched_files": len(up_paths),
        "overlap_count": len(fork_paths & up_paths),
        "overlap_paths": sorted(fork_paths & up_paths),
        "merge_tree_status": "CLEAN" if merge.returncode == 0 else "CONFLICTED",
        "candidate_tree_sha": combined.splitlines()[0] if merge.returncode == 0 else None,
        "safe_to_auto_merge": False,
        "runtime_qualified": False,
    }
    return report, combined

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fork", default="HEAD")
    parser.add_argument("--upstream", default="refs/remotes/upstream/main")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        report, log = probe(args.fork, args.upstream)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "fork-sync-report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8")
        (args.output / "merge-tree.log").write_text(log, encoding="utf-8")
        print(json.dumps({
            "admission": report["merge_tree_status"],
            "ahead": report["ahead"], "behind": report["behind"],
            "overlap_count": report["overlap_count"],
            "report": str(args.output / "fork-sync-report.json"),
            "auto_merge": False,
        }, sort_keys=True))
        return 0 if report["merge_tree_status"] == "CLEAN" else 2
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"admission": "UNAVAILABLE", "error": str(exc)}), file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
