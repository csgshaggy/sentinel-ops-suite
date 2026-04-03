from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.startup_validator import validate_backend_startup
from app.utils.router_loader import auto_discover_routers

from app.routers.dashboard_health import router as dashboard_health_router

app = FastAPI(
    title="Sentinel Ops Backend",
    description="Backend API for Sentinel Ops Suite",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-discovered routers
for name, router in auto_discover_routers():
    app.include_router(router)

# Dashboard health
app.include_router(dashboard_health_router)


@app.on_event("startup")
async def startup_event():
    validate_backend_startup()
    print("🚀 Backend startup complete.")


@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "Sentinel Ops Backend Running"}
