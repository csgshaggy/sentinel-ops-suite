from fastapi import APIRouter
from app.utils.router_loader import auto_discover_routers
from tools.security.idrim.idrim_engine import IDRIMEngine

router = APIRouter(prefix="/dashboard-health", tags=["Dashboard Health"])

idrim = IDRIMEngine()


@router.get("/")
def dashboard_health():
    routers = auto_discover_routers()
    router_status = {name: "loaded" for name, _ in routers}

    return {
        "status": "ok",
        "routers": router_status,
        "subsystems": {
            "idrim": {"version": idrim.version, "status": "ok"},
            "makefile": {"status": "ok"},
            "repo": {"status": "ok"},
            "drift": {"status": "ok"},
            "pelm": {"status": "ok"},
        }
    }
