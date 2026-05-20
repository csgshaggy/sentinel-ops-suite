# app/api/api_v1.py

from fastapi import APIRouter

from app.routers import auth              # ✅ auth lives here
from app.api.routes import settings       # ✅ settings router we created

router = APIRouter()

# -----------------------------
# AUTH ROUTES
# -----------------------------
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

# -----------------------------
# SETTINGS ROUTES
# -----------------------------
router.include_router(
    settings.router,
    prefix="/settings",
    tags=["settings"],
)
