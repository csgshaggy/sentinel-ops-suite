from fastapi import FastAPI

# Router imports
from app.routers import (
    pelm,
    pelm_stream,
    health_score,
    health_trend,
    anomaly_correlation,
    alerts,
    makefile_status,
    health_predict,
)

def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        description="Backend service for SSRF Command Console",
        version="1.0.0",
    )

    # ---------------------------------------------------------
    # Router Registration (deterministic order)
    # ---------------------------------------------------------
    app.include_router(pelm.router)
    app.include_router(pelm_stream.router)
    app.include_router(health_score.router)
    app.include_router(health_trend.router)
    app.include_router(anomaly_correlation.router)
    app.include_router(alerts.router)
    app.include_router(makefile_status.router)
    app.include_router(health_predict.router)

    return app


app = create_app()
