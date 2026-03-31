import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Anomaly detector
from .anomaly_detector import detect_anomalies

# Health scoring engine
from .health_score import compute_health_score

# Predictive model
from .predictive_model import predict_health

# Repair engine
from .repair_engine import run_repair

# Routers
from .routers import admin, auth, doctor, makefile_admin, plugins

# Sync history parser
from .sync_history import parse_sync_history


def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console Backend",
        description="Operator‑grade backend API",
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
    # ROUTERS
    # ---------------------------------------------------------
    app.include_router(plugins.router, prefix="/plugins", tags=["plugins"])
    app.include_router(makefile_admin.router, prefix="/makefile", tags=["makefile"])
    app.include_router(doctor.router, prefix="/doctor", tags=["doctor"])
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])

    # ---------------------------------------------------------
    # SYNC HISTORY API
    # ---------------------------------------------------------
    @app.get("/sync/history", tags=["sync"])
    def get_sync_history(limit: int = 20):
        return {"history": parse_sync_history(limit)}

    # ---------------------------------------------------------
    # HEALTH SCORE API
    # ---------------------------------------------------------
    @app.get("/health/score", tags=["health"])
    def get_health_score():
        return compute_health_score()

    # ---------------------------------------------------------
    # HEALTH TREND HISTORY API
    # ---------------------------------------------------------
    history_file = Path("health_history.jsonl")

    @app.get("/health/history", tags=["health"])
    def get_health_history(limit: int = 50):
        if not history_file.exists():
            return {"history": []}

        lines = history_file.read_text().strip().split("\n")[-limit:]
        return {"history": [json.loads(line) for line in lines]}

    # ---------------------------------------------------------
    # HEALTH ANOMALIES API
    # ---------------------------------------------------------
    @app.get("/health/anomalies", tags=["health"])
    def get_anomalies():
        return {"anomalies": detect_anomalies()}

    # ---------------------------------------------------------
    # AUTO‑REPAIR API
    # ---------------------------------------------------------
    @app.post("/repair/auto", tags=["repair"])
    def auto_repair():
        return run_repair()

    @app.get("/repair/history", tags=["repair"])
    def repair_history(limit: int = 20):
        repair_file = Path("repair_history.jsonl")
        if not repair_file.exists():
            return {"history": []}

        lines = repair_file.read_text().strip().split("\n")[-limit:]
        return {"history": [json.loads(line) for line in lines]}

    # ---------------------------------------------------------
    # PREDICTIVE HEALTH API
    # ---------------------------------------------------------
    @app.get("/health/predict", tags=["health"])
    def predict(n_future: int = 5):
        """
        Predict future health scores using ML-lite linear regression.
        """
        return predict_health(n_future)

    return app


# ---------------------------------------------------------
# Entry point for: python -m backend.app.main
# ---------------------------------------------------------
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
