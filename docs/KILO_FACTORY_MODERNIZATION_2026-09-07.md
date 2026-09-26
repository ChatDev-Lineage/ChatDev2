# Kilo ChatDev Factory Modernization — 2026-09-07

## Purpose

Preserve the Kilo-specific ChatDev/DevAll product lineage while selectively
adopting useful upstream work and connecting ChatDev to the colony's real game
portfolio, toolchain, evidence systems and token-saving workflow doctrine.

This is **not** a plan to overwrite the fork with upstream `main`.

## Current fork truth

Direct GitHub comparison on 2026-09-07 shows:

```text
OpenBMB/ChatDev main: 4fb2db0ea90375ce1059f44fe03ffbd191a7a169
KiloMusician/ChatDev2 main: a9bd768d952609807f13f03f26daf3459415fab3
merge base: 4a6ee25d7945f183b437ab202a217909b3b59f2b (2026-02-11)
status: diverged
fork ahead: 558 commits
fork behind: 124 commits
```

Therefore:

```text
fork != stale mirror
upstream update != blind merge/rebase
```

The modernization method is **patch-quarry + compatibility gates**.

## Kilo-specific capabilities already present

The current fork already contains substantial non-vanilla development work:

- `CLAUDE.md` frames ChatDev2 as part of the NuSyQ Colony rather than an isolated app.
- `INTEGRATION_GUIDE.md` describes NuSyQ-Hub, LiteLLM, Ollama, Idler and MCP integration.
- `tools/chatdev_colony_doctor.py` distinguishes live service truth from checkout truth.
- `tools/chatdev_gamedev_lane.ps1` provides bounded doctor/start/stop/bootstrap/smoke/status operations.
- `tools/workflow_smoke_runner.py` stops bounded runs on evidence thresholds rather than letting a swarm spend indefinitely.
- local LiteLLM/Ollama defaults support token-conscious local-first proof.
- smoke receipts preserve artifacts, bounded-stop reasons, token progress and runtime validation.
- Windows-specific lifecycle fixes and game-dev Python environment handling already exist.

This is a product lineage worth preserving.

## Historical Kilo ChatDev lineage

`ChatDev1.2` is a separate Kilo repository created in November 2023, not marked
as a GitHub fork. One early commit is named `commandFlowEnhancer`. Inspection
shows that commit primarily captures a generated ChatDev Warehouse experiment
whose task was to integrate a CommandRepository, FileManager and StateManager
for workflow automation.

Safe classification:

```text
2023 CommandFlowEnhancer = historical ChatDev-generated workflow experiment
```

It is **not yet evidence that ChatDev core itself implemented a modern workflow
engine**. It is, however, a useful concept-lineage specimen for today's Culture
Ship / command-flow work.

Before deleting or ignoring `ChatDev1`, `ChatDev1.1`, or `ChatDev1.2`, mine them
for unique prompts, role configurations, Warehouse outputs and experiments.

## Upstream patch quarry

Do not cherry-pick by title alone. For each upstream candidate:

1. inspect exact patch;
2. compare touched files against Kilo fork changes;
3. port or reimplement the intent in an isolated branch;
4. run focused tests;
5. run current Kilo game-dev/colony gates;
6. retain a source receipt identifying upstream commit/PR.

High-value upstream/current-community candidates to evaluate include:

- safer YAML loading / path validation hardening;
- bounded thread-pool worker counts;
- workflow/subgraph cache invalidation on YAML edits;
- persistent/vector-memory work where it complements rather than duplicates MemPalace/Serena;
- Windows encoding and `make.ps1` improvements;
- runtime import-cycle / OpenAI-protocol forwarding fixes;
- OpenAI-compatible streaming support for long Anthropic-backed gateway turns;
- schema/validation and workflow-authoring improvements;
- provider improvements only where they fit the local LiteLLM abstraction.

Open upstream PRs are **candidates**, not evidence that the fixes are already in
upstream main or in this fork.

## Kilo game factory direction

The first portfolio manifest is `config/kilo_game_factory.json`.

Initial projects:

```text
Project 144          P0  deterministic simulation + agent-native semantic CLI
Ash & Anvil          P0  large Godot RPG / persistence / player-agent protocol
Player Two           P0  training/orchestration brain + GAL provenance
Furyline             P1  Godot terrain/missions/procedural-audio vertical
Game Archaeology Lab P1  instrumentation/capture/memory-state investigation lab
```

This is deliberately **declarative**. The manifest does not claim that any
checkout exists on a particular machine. `tools/chatdev_factory_scout.py`
observes local truth and keeps missing local paths as UNKNOWN.

## Factory workflow

Target shape:

```text
intent / Culture Ship hotkey
  -> Intermediary intent compiler
  -> Factory Scout + Keeper/Fleet observations
  -> Serena/GitNexus repository intelligence
  -> minimal context packet
  -> select one ChatDev workflow / specialist team
  -> isolated worktree
  -> bounded local-model run
  -> native project tests / semantic CLI / headless game gate
  -> GSV verification
  -> receipt
  -> MemPalace / Second Brain / RSEV cultivation
```

ChatDev is a **worker/orchestrator**, not the authority layer.

## CLI-Anything convergence

The colony's independent CLI-Anything doctrine and the current external
CLI-Anything ecosystem converge on the same useful requirements:

- machine-readable `--json` output;
- one-shot commands plus optional REPL;
- installable PATH entrypoints;
- generated agent `SKILL.md`;
- explicit tests;
- `--dry-run` for stateful mutation;
- semantic interfaces preferred over screenshot automation.

Project 144 already demonstrates this style through `tools/p144.py`.

Next candidates for harnessing should be chosen by leverage, not novelty:

1. Godot project inspection/headless test/build operations;
2. Blender asset inspection/export pipelines used by games;
3. PowerToys Command Palette as a Windows Culture Ship launcher surface;
4. bounded Sysinternals investigative wrappers;
5. internal MC/Ecos program operations lacking semantic CLIs.

## Windows investigative deck

Sysinternals should be treated primarily as **evidence sensors**:

```text
Procmon     -> file/Registry/process/thread/IPC observations
ProcessExp  -> process ownership, loaded DLLs, handles
Handle      -> who owns a file/object
TCPView     -> network/socket observation
PsPing      -> network latency/throughput probe
ProcDump    -> bounded crash/hang/CPU dump capture
Autoruns    -> startup persistence inventory
Sigcheck    -> signature/version/hash evidence
Streams     -> NTFS alternate-data-stream evidence
ListDLLs    -> loaded-module evidence
RAMMap/VMMap-> memory-pressure/mapping evidence
Sysmon      -> durable host event telemetry where configured
```

Wrappers should emit normalized JSON and never equate `tool ran` with
`conclusion proven`.

## PowerToys / command palette

PowerToys Command Palette is a natural Windows operator surface for the Culture
Ship macro deck. It should launch existing authoritative CLIs/workflows rather
than contain business logic itself.

Potential entries:

```text
Cold Iron
Serena First
Search Escalator
Factory Scout
Model Weather
Forge
Prime Dig
ChatDev Game Sprint
Special Circumstances
Captain's Log
```

Hotkey selection never grants authority.

## Agent roster for large games

Do not use a generic broadcast swarm. Compose task-specific teams, for example:

```text
Investigator        Serena/GitNexus/requirements archaeology
Systems Designer    mechanics/state/data architecture
Gameplay Programmer bounded implementation lane
Content Designer    data/content using existing schemas
Test Engineer       native/headless/semantic checks
Performance Hunter  profiling + Sysinternals/runtime evidence
Integration Steward cross-repo contracts and receipts
Archivist           provenance/decision/RSEV/Second Brain updates
```

The Intermediary should select the smallest team that can resolve the task.

## First game-development campaigns

### Project 144

Use its semantic CLI as the gold-standard no-screenshot playtest surface.
ChatDev tasks should be narrow mechanics, regression scenarios, generator/content
work and headless simulation tests.

### Ash & Anvil

Prioritize infrastructure that multiplies future development speed: semantic
headless inspection, content validators, save/provenance tests, player-agent
protocols, deterministic recipe/economy checks, then content expansion.

### Player Two + GAL

Use GAL as the investigative laboratory and Player Two as the training/decision
product boundary. Preserve explicit provenance between them rather than copying
lab experiments invisibly.

### Furyline

Exploit deterministic terrain/missions and procedural systems for short parallel
ChatDev lanes with strong regression tests.

## Factory Scout contract

`tools/chatdev_factory_scout.py` is intentionally read-only.

It observes:

- PATH-visible source/build/agent/game/context tools;
- CLI-Anything / PowerToys / Sysinternals executables when discoverable;
- declared game portfolio;
- local project checkout candidates;
- Git branch/HEAD/dirty/origin when a checkout is present;
- native contract markers such as Godot, Python, tests, GSV and semantic CLI.

It does not:

- install or update tools;
- start services;
- fetch repositories;
- invoke any model;
- run project tests;
- mutate Git;
- infer fleet-wide absence from one host;
- grant authority.

## Next implementation wave

1. Run Factory Scout on MSI and desktop and preserve receipts.
2. Add project-specific contract adapters for the detected local game checkouts.
3. Add `portfolio-plan`: repo intelligence -> compact ChatDev task packet.
4. Add `portfolio-smoke`: run a project's native bounded validation contract.
5. Build a Sysinternals JSON sensor pack for Listener Truth / Ghost Hunter / Split-Brain Detector.
6. Generate PowerToys Command Palette entries for read-only Culture Ship macros first.
7. Evaluate upstream's 124 missing commits in batches by subsystem, starting with security/runtime correctness.
8. Mine ChatDev1/1.1/1.2 for unique Kilo experiments and role/prompt ideas.
9. Connect ChatDev dispatch into Intermediary/Culture Ship so `chatdev_status` is no longer the only commonly exercised operation.
10. Dogfood one real Project 144 task end-to-end before widening to Ash & Anvil.

## Invariants

```text
upstream newer != upstream better for the Kilo fork
fork divergence != technical debt by itself
installed tool != ready capability
not detected here != absent from fleet
workflow selected != operation authorized
agent output != verified artifact
source tests != game runtime proof
semantic metadata != authority
large game scope != permission for unbounded swarm execution
```
