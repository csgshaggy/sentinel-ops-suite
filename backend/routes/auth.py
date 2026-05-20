from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session as DBSession

from app.models.user import User
from app.utils.sessions import validate_session, restore_session, heartbeat
from app.db.session import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/session/restore")
async def session_restore(request: Request, db: DBSession = Depends(get_db)):
    session = restore_session(request, db)
    if not session:
        raise HTTPException(status_code=404, detail="No active session")
    return session


@router.post("/heartbeat")
async def session_heartbeat(request: Request, db: DBSession = Depends(get_db)):
    ok = heartbeat(request, db)
    if not ok:
        raise HTTPException(status_code=401, detail="Session expired")
    return {"status": "ok"}


@router.post("/logout")
async def logout(request: Request):
    response = JSONResponse({"status": "logged_out"})
    response.delete_cookie("session_id")
    return response
