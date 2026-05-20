import json
import os
from functools import lru_cache
from pathlib import Path
from fastapi import HTTPException

# Absolute paths to Vite manifests
LOGIN_MANIFEST = Path(
    "/home/ubuntu/sentinel-ops-suite/frontend/login-app/dist/.vite/manifest.json"
)

DASHBOARD_MANIFEST = Path(
    "/home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/dist/.vite/manifest.json"
)


def _load_manifest(path: Path) -> dict:
    """
    Load a Vite manifest from disk with strict validation.
    Raises clear operator-grade errors if missing or invalid.
    """
    if not path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Vite manifest not found: {path}. "
                   f"Did you run the frontend build?"
        )

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Vite manifest at {path}: {e}"
        )


@lru_cache(maxsize=4)
def get_login_manifest() -> dict:
    """Cached loader for login-app manifest."""
    return _load_manifest(LOGIN_MANIFEST)


@lru_cache(maxsize=4)
def get_dashboard_manifest() -> dict:
    """Cached loader for dashboard-app manifest."""
    return _load_manifest(DASHBOARD_MANIFEST)


def asset_url(app: str, entry: str) -> str:
    """
    Resolve a built asset URL from the correct manifest.
    app: "login" or "dashboard"
    entry: e.g. "src/main.jsx"
    """
    if app == "login":
        manifest = get_login_manifest()
    elif app == "dashboard":
        manifest = get_dashboard_manifest()
    else:
        raise ValueError(f"Unknown app: {app}")

    if entry not in manifest:
        raise HTTPException(
            status_code=500,
            detail=f"Entry '{entry}' not found in {app} manifest."
        )

    return "/" + manifest[entry]["file"]
