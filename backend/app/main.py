from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    system,
    admin,
    git_snapshots,
    pelm,
    pelm_stream,
    plugins,
    workflow_runs,
    makefile_diff,
    makefile_health,
    router_drift,
    repo_health,
    ci_summary,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        description=(
            "Operator-grade backend for anomaly detection, correlation, "
            "snapshots, router health, and system diagnostics."
        ),
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(system.router)
    app.include_router(admin.router)
    app.include_router(git_snapshots.router)
    app.include_router(pelm.router)
    app.include_router(pelm_stream.router)
    app.include_router(plugins.router)

    app.include_router(workflow_runs.router)
    app.include_router(makefile_diff.router)
    app.include_router(makefile_health.router)
    app.include_router(router_drift.router)
    app.include_router(repo_health.router)
    app.include_router(ci_summary.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
