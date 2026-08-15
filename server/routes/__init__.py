"""Aggregates API routers."""

from . import artifacts, batch, bridge, ecosystem, execute, execute_sync, health, nusyq_bridge, orchestrator, sessions, tools, uploads, vuegraphs, websocket, workflows

ALL_ROUTERS = [
    health.router,
    bridge.router,
    ecosystem.router,
    nusyq_bridge.router,
    orchestrator.router,
    vuegraphs.router,
    workflows.router,
    uploads.router,
    artifacts.router,
    sessions.router,
    batch.router,
    execute.router,
    execute_sync.router,
    tools.router,
    websocket.router,
]

__all__ = ["ALL_ROUTERS"]