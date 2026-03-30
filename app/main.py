from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core settings
from app.core.config import settings

# Routers
from app.api.routes.auth import router as auth_router
from app.auth.mfa import router as mfa_router
# Add additional routers here as your project grows:
# from app.api.routes.users import router as users_router
# from app.api.routes.admin import router as admin_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # -----------------------------
    # CORS
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # Routers
    # -----------------------------
    app.include_router(auth_router, prefix="/auth")
    app.include_router(mfa_router, prefix="/auth")  # MFA lives under /auth/mfa/*

    # Example future routers:
    # app.include_router(users_router, prefix="/users")
    # app.include_router(admin_router, prefix="/admin")

    return app


app = create_app()
