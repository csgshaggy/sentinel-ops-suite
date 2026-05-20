# /app/main.py
# SentinelOps API – Clean, cookie‑compatible FastAPI entrypoint

# -------------------------------------------------
# Global Structured Logging (MUST be first)
# -------------------------------------------------
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logging.getLogger("session").setLevel(logging.INFO)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Custom Hardened Session Manager ---
from app.core.session import SessionManagerMiddleware

# --- Database Session Middleware ---
from app.db.session import SessionLocal

# --- Routers ---
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.admin import router as admin_router
from app.routers.session_status import router as session_status_router
from app.routers.profile import router as profile_router   # ⭐ Profile + Avatar routes

# --- Settings ---
try:
    from app.core.config import settings
    SESSION_SECRET = settings.SESSION_SECRET
except Exception:
    SESSION_SECRET = "CHANGE_ME_TO_A_SECURE_RANDOM_KEY"


# -------------------------------------------------
# FastAPI application
# -------------------------------------------------
app = FastAPI(
    title="SentinelOps API",
    version="1.0.0",
)


# -------------------------------------------------
# Static file serving (required for avatar images)
# -------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------------------------
# Middleware
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionManagerMiddleware,
    session_secret=SESSION_SECRET,
)


# -------------------------------------------------
# Dependency: DB session per request
# -------------------------------------------------
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profile_router, prefix="/api/auth", tags=["profile"])  # ⭐ Avatar + Profile
app.include_router(session_status_router, tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])


# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
