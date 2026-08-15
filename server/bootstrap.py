"""Application bootstrap helpers for the FastAPI server."""
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server import state
from server.config_schema_router import router as config_schema_router
from server.routes import ALL_ROUTERS
from utils.error_handler import add_exception_handlers
from utils.middleware import add_middleware

_ECO_PARENT = Path(__file__).resolve().parents[1]
if str(_ECO_PARENT) not in sys.path:
    sys.path.insert(0, str(_ECO_PARENT))


def init_app(app: FastAPI) -> None:
    """Apply shared middleware, routers, and global state to ``app``."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(app)
    add_middleware(app)

    state.init_state()

    for router in ALL_ROUTERS:
        app.include_router(router)

    app.include_router(config_schema_router)

    # ── CHUG Daemon startup ────────────────────────────────────────────────
    @app.on_event("startup")
    async def _start_chug_daemon():
        try:
            from ecosystem.chug_daemon import start as daemon_start
            result = daemon_start(interval_s=600)  # 10-minute default
            import logging
            logging.getLogger("bootstrap").info(
                "CHUG daemon: %s (interval=%ds)",
                result["status"], result.get("interval_s", 600)
            )
        except Exception as e:
            import logging
            logging.getLogger("bootstrap").warning("CHUG daemon start failed: %s", e)
