# /home/ubuntu/sentinel-ops-suite/backend/app/utils/sessions.py

from datetime import datetime, timedelta
from fastapi import Request
from sqlalchemy.orm import Session as DBSession

# Correct models
from auth.models import Session as SessionModel, User

COOKIE_NAME = "session_id"

# Sliding inactivity timeout (15 minutes)
INACTIVITY_MINUTES = 15

# Absolute max session lifetime (24 hours)
ABSOLUTE_MAX_MINUTES = 60 * 24


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _get_cookie(request: Request):
    return request.cookies.get(COOKIE_NAME)


def _fetch_session(db: DBSession, token: str) -> SessionModel | None:
    return (
        db.query(SessionModel)
        .filter(SessionModel.session_id == token)
        .first()
    )


def _is_absolute_expired(sess: SessionModel) -> bool:
    now = datetime.utcnow()
    absolute_expiry = sess.created_at + timedelta(minutes=ABSOLUTE_MAX_MINUTES)
    return now > absolute_expiry


def _is_ip_mismatch(request: Request, sess: SessionModel) -> bool:
    request_ip = request.client.host
    return sess.ip_address is not None and sess.ip_address != request_ip


def _is_ua_mismatch(request: Request, sess: SessionModel) -> bool:
    request_ua = request.headers.get("user-agent", "")
    return sess.user_agent is not None and sess.user_agent != request_ua


def _is_inactive(sess: SessionModel) -> bool:
    now = datetime.utcnow()
    if not sess.last_activity_at:
        return False
    return sess.last_activity_at < now - timedelta(minutes=INACTIVITY_MINUTES)


# ---------------------------------------------------------
# Session Validators
# ---------------------------------------------------------

def validate_session(request: Request, db: DBSession) -> User | None:
    token = _get_cookie(request)
    if not token:
        return None

    sess = _fetch_session(db, token)
    if not sess:
        return None

    now = datetime.utcnow()

    if _is_ip_mismatch(request, sess):
        return None

    if _is_ua_mismatch(request, sess):
        return None

    if _is_absolute_expired(sess):
        return None

    if sess.expires_at < now:
        return None

    if _is_inactive(sess):
        return None

    return sess.user


def restore_session(request: Request, db: DBSession):
    token = _get_cookie(request)
    if not token:
        return None

    sess = _fetch_session(db, token)
    if not sess:
        return None

    now = datetime.utcnow()

    if _is_ip_mismatch(request, sess):
        return None

    if _is_ua_mismatch(request, sess):
        return None

    if _is_absolute_expired(sess):
        return None

    if sess.expires_at < now:
        return None

    if _is_inactive(sess):
        return None

    # Update sliding timestamps
    sess.last_activity_at = now
    sess.last_seen_at = now
    db.add(sess)
    db.commit()

    return {
        "session_token": sess.session_id,
        "user": {
            "id": sess.user.id,
            "email": sess.user.email,
            "username": sess.user.username,
        },
    }


def heartbeat(request: Request, db: DBSession) -> bool:
    token = _get_cookie(request)
    if not token:
        return False

    sess = _fetch_session(db, token)
    if not sess:
        return False

    now = datetime.utcnow()

    if _is_ip_mismatch(request, sess):
        return False

    if _is_ua_mismatch(request, sess):
        return False

    if _is_absolute_expired(sess):
        return False

    if sess.expires_at < now:
        return False

    if _is_inactive(sess):
        return False

    sess.last_seen_at = now
    sess.last_activity_at = now
    db.add(sess)
    db.commit()

    return True
