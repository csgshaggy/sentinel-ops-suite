# =====================================================================
# SSRF Command Console — FastAPI Application Entry Point
# =====================================================================

from fastapi import FastAPI

from backend.auth.routes import router as auth_router
from backend.admin.routes import router as admin_router

app = FastAPI(
    title="SSRF Command Console",
    version="0.1.0",
    description="Operator-grade backend for the SSRF Command Console.",
)

# ---------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------

app.include_router(auth_router)
app.include_router(admin_router)

# ---------------------------------------------------------------------
# Health / Meta
# ---------------------------------------------------------------------

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["meta"])
def root():
    return {"message": "SSRF Command Console backend is running"}
