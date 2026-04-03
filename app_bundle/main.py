from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auto_discover_routers

# Explicit imports for PELM-related routers
from app.routers import pelm_reports
from app.routers import pelm_trend
from app.routers import pelm_diff
from app.routers import pelm_regression


def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        description="Backend API for Observability, Governance, and PELM",
        version="1.0.0",
    )

    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------
    # Auto-discover all routers in app/routers/
    # ---------------------------------------------------------
    auto_discover_routers(app)

    # ---------------------------------------------------------
    # Explicit router registration (safe even with auto-discovery)
    # Ensures PELM endpoints are always available.
    # ---------------------------------------------------------
    app.include_router(pelm_reports.router)
    app.include_router(pelm_trend.router)
    app.include_router(pelm_diff.router)
    app.include_router(pelm_regression.router)

    return app


app = create_app()
