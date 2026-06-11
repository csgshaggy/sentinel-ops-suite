# app/routers/iam_fetch.py

from fastapi import APIRouter

# Option A: backend/ is the package root → remove "backend."
from app.providers.iam.registry import get_provider

router = APIRouter(prefix="/iam", tags=["IAM"])


@router.get("/{provider}")
async def fetch_iam(provider: str):
    p = get_provider(provider)
    return p.fetch_all()
