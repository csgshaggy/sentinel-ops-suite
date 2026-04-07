#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
backend/app/main.py
FastAPI entrypoint with deterministic router loading, session middleware,
CORS, DB initialization, and operator‑grade structure.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.database import init_db
from app.routers import (
    auth,
    dashboard,
    users,
)

# ---------------------------------------------------------------------------
# APPLICATION INITIALIZATION
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SentinelOps Backend",
    description="Backend API for SentinelOps Analyst Dashboard",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# SESSION MIDDLEWARE (Corrected for HTTPS + Chrome)
# ---------------------------------------------------------------------------

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_ME_TO_A_SECURE_RANDOM_KEY",
    session_cookie="sentinel_session",
    same_site="none",        # Required for HTTPS + cross-site cookies
    https_only=True,         # Marks cookie as Secure
)

# ---------------------------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------------------------

ALLOWED_ORIGINS = [
    "https://crcybercop.dpdns.org",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# ROUTER REGISTRATION
# ---------------------------------------------------------------------------

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(users.router)

# ---------------------------------------------------------------------------
# STARTUP EVENTS
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    """Initialize database and any required services."""
    init_db()

# ---------------------------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "SentinelOps backend online",
        "routes": [
            "/auth/*",
            "/dashboard/*",
            "/users/*",
        ],
    }

# ---------------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
