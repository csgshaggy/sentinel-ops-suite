"""
Sentinel Ops Suite — FastAPI Entrypoint
Clean, deterministic, operator‑grade backend initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from api.dashboard_health import router as dashboard_health_router

# If you have additional routers, import them here:
# from api.auth import router as auth_router
# from api.users import router as users_router
# from api.makefile import router as makefile_router
# from api.system import router as system_router

# -------------------------------------------------------------------
# Application Factory
# -------------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sentinel Ops Suite Backend",
        description="Backend API for Sentinel Ops Suite dashboard, health, and tooling.",
        version="1.0.0",
    )

    # ---------------------------------------------------------------
    # CORS (dev‑friendly defaults)
    # ---------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten later if needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------------
    # Router Registration
    # ---------------------------------------------------------------
    app.include_router(dashboard_health_router, prefix="/api/dashboard")

    # Example additional routers:
    # app.include_router(auth_router, prefix="/api/auth")
    # app.include_router(users_router, prefix="/api/users")
    # app.include_router(makefile_router, prefix="/api/makefile")
    # app.include_router(system_router, prefix="/api/system")

    return app


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
