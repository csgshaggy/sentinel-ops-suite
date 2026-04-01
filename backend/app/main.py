from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core Routers
from backend.app.routers import (
    health,
    admin,
    git_snapshots,   # NEW: Snapshot HTML viewer route
)

# Settings (if you have a settings module)
try:
    from backend.app.core.settings import settings
except Exception:
    settings = None


def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        description="Operator‑grade backend for SSRF Command Console",
        version="1.0.0",
    )

    # ------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------
    # Routers
    # ------------------------------------------------------------
    app.include_router(health.router)
    app.include_router(admin.router)
    app.include_router(git_snapshots.router)  # NEW

    return app


app = create_app()
