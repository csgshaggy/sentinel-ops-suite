from fastapi import APIRouter
from tools.plugins import PLUGINS

router = APIRouter(prefix="/pelm", tags=["PELM"])

@router.get("/health")
def pelm_health():
    return {"status": "ok", "plugins_loaded": list(PLUGINS.keys())}

@router.post("/plugin")
def pelm_run_plugin(name: str = "pelm"):
    plugin = PLUGINS.get(name)
    if not plugin:
        return {"error": f"Plugin '{name}' not found"}

    return plugin.run()
