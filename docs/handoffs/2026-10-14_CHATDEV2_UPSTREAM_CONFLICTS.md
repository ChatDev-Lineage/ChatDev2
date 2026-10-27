# ChatDev 2 upstream integration: source-pinned conflict handoff

[Msg⛛{CHATDEV2-UPSTREAM-MERGE-20261014}]
Status: **blocked for automatic merge, testable for manual resolution**.

This is a projection of live Git ancestry and a hosted disposable `git
merge-tree`, **not** a second RosettaStone, Capability Atlas, deployment
authority, or ChatDev runtime configuration.

## Source receipts

- Owning fork: `ChatDev-Lineage/ChatDev2`, default branch `main`.
- Source upstream: `OpenBMB/ChatDev`, branch `main`.
- Pinned upstream tested: `4fb2db0ea90375ce1059f44fe03ffbd191a7a169`.
- Exact fork PR merge-ref tested: `17fe5b811a92549ff71c4066ab8b94b4fb6efd43`.
- Common ancestor: `4a6ee25d7945f183b437ab202a217909b3b59f2b`.
- Git ahead: **572** on the tested PR merge-ref, behind **124**.
  Fork default-branch-only observation before adding this PR: ahead **568**,
  behind **124**. Do not confuse merge-ref counts with default-branch counts.
- Changed vs ancestor: fork **32,609 files**, upstream **100 files**.
- Path intersection: **14**; Git content conflicts: **9**.
- Exact workflow run and downloadable machine receipt:
  https://github.com/ChatDev-Lineage/ChatDev2/actions/runs/38682567243
  (artifact `chatdev2-upstream-fork-preflight`, merge-tree exit **1**).
- The merge-admission action intentionally exited **2** on `CONFLICTED`.
  Its three deterministic no-network regression tests passed.
- The GitHub Actions runner did not check out a combined tree, run upstream
  project code, execute an agent, or modify either source branch.

## Nine actual merge conflicts

| Path | Acceptance priority |
| --- | --- |
| `.gitignore` | Union safe ignore rules; never expose secrets or local state |
| `README.md` | Preserve upstream product documentation and identify GSV overlays |
| `frontend/package-lock.json` | Regenerate only after resolving package manifest; `npm ci` gate |
| `frontend/package.json` | Reconcile Vue dependencies and scripts against the customized UI |
| `frontend/src/components/Sidebar.vue` | Preserve colony navigation and upstream changes; rendered UX proof |
| `pyproject.toml` | Resolve Python packaging and interpreter constraints |
| `requirements.txt` | Match dependency policy; no dependency downgrade by accident |
| `server/routes/__init__.py` | Security-critical: preserve admission, authentication and registered routes |
| `uv.lock` | Regenerate from resolved Python constraints and verify frozen install |

Additional **overlapping but automatically merged** paths that still require
human review: `Makefile`, `frontend/src/router/index.js`,
`runtime/node/executor/agent_executor.py`, `server/bootstrap.py`,
`yaml_instance/demo_human.yaml`. A clean textual merge is not evidence of
runtime or permission compatibility. The executor and bootstrap are
security-critical and require deny-case regressions.

## Safe successor plan

1. Make an isolated branch from the **latest** ChatDev2 `main`, fetch the
   latest upstream SHA and rerun `tools/fork_merge_probe.py`. Never force
   reset or fast-forward over GSV commits.
2. Resolve `server/routes/__init__.py` and the automatically merged
   executor/bootstrap alongside permission-denial tests. Source parser alone
   is insufficient.
3. Resolve Python dependency manifests/lock together; run clean lockfile
   installs, API/server unit tests and `/health` on an isolated environment.
4. Resolve frontend manifest, lock, sidebar and router together; run fresh
   `npm ci`, production build and screenshot/interaction smoke.
5. Resolve `.gitignore` and the dual-lineage README without exposing
   operator credentials, Dev-Mentor queues or local runtime paths.
6. Commit a **genuine two-parent merge** only after all nine conflicts are
   resolved, the five auto-merged paths are reviewed, and negative security
   tests pass. Then compare against pinned upstream: `behind=0`, with fork
   changes retained. Record the actual merge tree/commit SHA.
7. Keep the merge candidate as a draft PR until independent review and
   verified local/CI integration. **Do not** restart port 7338, promote a
   production image, bypass API auth or spend a model API budget as part of
   source syncing.

A badge for the preflight means only that the preflight ran. This document
deliberately distinguishes `MERGE_CONFLICTED` from `UPSTREAM_INTEGRATED`.
