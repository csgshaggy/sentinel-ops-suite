from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import (
    plugins,
    makefile_admin,
    system,
)


def create_app() -> FastAPI:
    """
    Application factory for the SSRF Command Console backend.
    Initializes FastAPI, CORS, and all routers.
    """
    app = FastAPI(
        title="SSRF Command Console API",
        version="1.0.0",
        description="Backend API powering the SSRF Operator Dashboard",
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Routers
    app.include_router(plugins.router, prefix="/api")
    app.include_router(makefile_admin.router, prefix="/api")
    app.include_router(system.router, prefix="/api")

    return app


# Expose the FastAPI app for Uvicorn
app = create_app()


# Allow `python -m backend.app.main` to start the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=5001,
        reload=True,
    )
