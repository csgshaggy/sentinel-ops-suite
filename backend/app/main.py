from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

# Routers
from .routers import plugins
from .routers import makefile_admin
from .routers import doctor
from .routers import admin
from .routers import auth

# Sync history parser
from .sync_history import parse_sync_history

# Health scoring engine
from .health_score import compute_health_score

# Anomaly detector
from .anomaly_detector import detect_anomalies

# Repair engine
from .repair_engine import run_repair

# Predictive model (Item #14)
from .predictive_model import predict_health


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
    HISTORY_FILE = Path("health_history.jsonl")

    @app.get("/health/history", tags=["health"])
    def get_health_history(limit: int = 50):
        if not HISTORY_FILE.exists():
            return {"history": []}

        lines = HISTORY_FILE.read_text().strip().split("\n")[-limit:]
        return {"history": [json.loads(l) for l in lines]}

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
        f = Path("repair_history.jsonl")
        if not f.exists():
            return {"history": []}

        lines = f.read_text().strip().split("\n")[-limit:]
        return {"history": [json.loads(l) for l in lines]}

    # ---------------------------------------------------------
    # PREDICTIVE HEALTH API (Item #14 Step 2)
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
