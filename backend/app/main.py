from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Only route that currently exists
from app.routes.pelm_status_route import router as pelm_status_router


def create_app() -> FastAPI:
    """
    Sentinel Ops Suite Backend
    Minimal, correct, and aligned with the actual filesystem.
    """

    app = FastAPI(
        title="Sentinel Ops Suite Backend",
        description="Backend API for observability, PELM, anomaly detection, and operator tooling.",
        version="1.0.0",
    )

    # CORS (frontend compatibility)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register the only existing route
    app.include_router(pelm_status_router, prefix="/api")

    return app


app = create_app()
