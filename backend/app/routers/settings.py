# app/routers/settings.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_settings():
    return {
        "theme": "dark",
        "notifications": True,
        "app_name": "SentinelOps",
        "version": "1.0.0",
    }
