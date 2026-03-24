from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Admin routers
from app.routers.admin.home import router as home_router
from app.routers.admin.logs import router as logs_router
from app.routers.admin.system import router as system_router
from app.routers.admin.docs import router as docs_router
from app.routers.admin.superdoctor import router as superdoctor_router

# Settings / config
from utils.settings import Settings
from utils.logging import init_logging


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    This is the authoritative entrypoint for the backend.
    """

    # Load settings
    settings = Settings()

    # Initialize logging early
    init_logging()

    app = FastAPI(
        title="SSRF Console Backend",
        description="Operator-grade backend with diagnostics, admin panels, and observability.",
        version="1.0.0",
    )

    # ------------------------------------------------------------
    # CORS (optional, but common for dashboards)
    # ------------------------------------------------------------
    if settings.enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # ------------------------------------------------------------
    # Register routers
    # ------------------------------------------------------------
    app.include_router(home_router, prefix="/admin")
    app.include_router(logs_router, prefix="/admin")
    app.include_router(system_router, prefix="/admin")
    app.include_router(docs_router, prefix="/admin")
    app.include_router(superdoctor_router, prefix="/admin")

    # ------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


# ------------------------------------------------------------
# ASGI entrypoint
# ------------------------------------------------------------
app = create_app()
