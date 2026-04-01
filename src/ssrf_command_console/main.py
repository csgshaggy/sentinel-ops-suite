from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ssrf_command_console.auth.login import router as login_router
from ssrf_command_console.auth.mfa import router as mfa_router

app = FastAPI(
    title="SSRF Command Console Backend",
    description="Backend API for the SSRF Command Console operator dashboard",
    version="1.0.0",
)

# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------
app.include_router(mfa_router)
app.include_router(login_router)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ssrf_command_console.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
