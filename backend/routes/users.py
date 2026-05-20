from fastapi import APIRouter, Depends, HTTPException, Request
from app.utils.sessions import validate_session

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me")
async def get_me(request: Request):
    user = await validate_session(request)
    if not user:
        raise HTTPException(status_code=404, detail="No active session")
    return user
