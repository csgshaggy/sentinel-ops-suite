# app/api/api_v1.py
# SentinelOps — API v1 Router (Settings Only)

from fastapi import APIRouter
from app.api.routes import settings

router = APIRouter()

# -----------------------------
# SETTINGS ROUTES
# -----------------------------
router.include_router(
    settings.router,
    prefix="/settings",
    tags=["settings"],
)
