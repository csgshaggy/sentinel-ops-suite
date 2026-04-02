from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core Routers
from routes.health import router as health_router
from routes.repo_health import router as repo_health_router
from routes.sync_history import router as sync_history_router

# Admin / Module Routers
from routes.mfa import router as mfa_router
from routes.docs import router as docs_router
from routes.structure import router as structure_router
from routes.deps import router as deps_router
from routes.makefile_health import router as makefile_health_router

app = FastAPI(
    title="Sentinel Ops Suite Backend",
    description="Backend API for operator console, repo governance, and dashboard systems.",
    version="1.0.0",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

# Core
app.include_router(health_router)
app.include_router(repo_health_router)
app.include_router(sync_history_router)

# Governance / Admin Modules
app.include_router(mfa_router)
app.include_router(docs_router)
app.include_router(structure_router)
app.include_router(deps_router)
app.include_router(makefile_health_router)

# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"status": "ok", "service": "Sentinel Ops Suite Backend"}
