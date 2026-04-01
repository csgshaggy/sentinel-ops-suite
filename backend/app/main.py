from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import (
    health,
    admin,
    git_snapshots,
    pelm,
    pelm_stream,   # NEW
)

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(admin.router)
    app.include_router(git_snapshots.router)
    app.include_router(pelm.router)
    app.include_router(pelm_stream.router)  # NEW

    return app


app = create_app()
