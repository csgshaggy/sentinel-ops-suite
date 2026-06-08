# /app/main.py
# SentinelOps API – Unified, cookie‑compatible FastAPI entrypoint

from dotenv import load_dotenv
load_dotenv()

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Settings ---
from app.core.config import settings

# --- Database Session Middleware ---
from app.db.session import SessionLocal

# --- REAL AUTH ROUTER (contains /login + MFA + logout + cookie logic)
from app.auth.router import router as auth_router

# --- Other Routers ---
from app.routers.users import router as users_router
from app.routers.admin import router as admin_router
from app.routers.health import router as health_router
from app.routers.profile import router as profile_router

# ✅ NEW: Settings Router
from app.routers.settings import router as settings_router

# ⚠️ DO NOT IMPORT THESE — THEY BREAK AUTH
# from app.routers.sessions import router as sessions_router
# from app.routers.api_keys import router as api_keys_router
# from app.routers.session_status import router as session_status_router


# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("startup")


# -------------------------------------------------
# FastAPI application
# -------------------------------------------------
app = FastAPI(
    title="SentinelOps API",
    version="1.0.0",
)


# -------------------------------------------------
# Startup Logging
# -------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("=== SentinelOps Backend Startup ===")

    logger.info(f"ENVIRONMENT: {settings.ENVIRONMENT}")
    logger.info(f"LOG_LEVEL: {settings.LOG_LEVEL}")

    try:
        sanitized_db_url = settings.DATABASE_URL.replace(settings.DB_PASSWORD, "***")
    except Exception:
        sanitized_db_url = "UNAVAILABLE"

    logger.info(f"DATABASE_URL: {sanitized_db_url}")

    logger.info(f"SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
    logger.info(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    logger.info(f"SESSION_COOKIE_HTTPONLY: {settings.SESSION_COOKIE_HTTPONLY}")
    logger.info(f"SESSION_COOKIE_SAMESITE: {settings.SESSION_COOKIE_SAMESITE}")
    logger.info(f"SESSION_EXPIRE_HOURS: {settings.SESSION_EXPIRE_HOURS}")

    logger.info(f"JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
    logger.info(f"JWT_ACCESS_TOKEN_EXPIRE_MINUTES: {settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}")
    logger.info(f"JWT_REFRESH_TOKEN_EXPIRE_DAYS: {settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS}")

    logger.info(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")

    logger.info("=== Startup Validation Complete ===")


# -------------------------------------------------
# Static files
# -------------------------------------------------
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


# -------------------------------------------------
# CORS (FIXED: removed malformed HTML wrapper)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crcybercop.dpdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# DB session per request
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
# Routers (Unified + FIXED)
# -------------------------------------------------

# ✅ REAL AUTH ROUTER → /api/auth/*
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# Users → /api/users/*
app.include_router(users_router, prefix="/api/users", tags=["users"])

# Admin → /api/admin/*
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

# Health → /api/health/*
app.include_router(health_router, prefix="/api/health", tags=["health"])

# Profile → /api/profile/*
app.include_router(profile_router, prefix="/api/profile", tags=["profile"])

# ✅ NEW: Settings → /api/settings/*
app.include_router(settings_router, prefix="/api/settings", tags=["settings"])


# -------------------------------------------------
# Root Health Check
# -------------------------------------------------
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
``
