from fastapi import FastAPI

# Router imports
from app.routers import pelm, pelm_stream

def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        description="Backend service for SSRF Command Console",
        version="1.0.0",
    )

    # Register routers
    app.include_router(pelm.router)
    app.include_router(pelm_stream.router)

    return app


app = create_app()
