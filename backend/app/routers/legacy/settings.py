# app/routers/settings.py

from fastapi import APIRouter, Request

router = APIRouter()

# -------------------------------------------------
# GET settings
# -------------------------------------------------
@router.get("/")
def get_settings():
    return {
        "theme": "dark",
        "notifications": True,
        "app_name": "SentinelOps",
        "version": "1.0.0",
    }


# -------------------------------------------------
# PATCH settings (FIXES YOUR ERROR)
# -------------------------------------------------
@router.patch("/")
async def update_settings(request: Request):
    payload = await request.json()

    # ✅ For now, just echo back what frontend sends
    # (prevents errors + confirms integration works)
    return {
        "status": "success",
        "updated": payload,
    }
