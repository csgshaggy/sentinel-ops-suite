from fastapi import APIRouter
from fastapi.routing import APIRoute
import importlib
import pkgutil
from typing import Dict, List, Any

router = APIRouter(prefix="/docs", tags=["docs"])


def _discover_admin_routes() -> List[Dict[str, Any]]:
    """
    Dynamically discover all routers under app.routers.admin
    and extract their routes for documentation.
    """
    import app.routers.admin as admin_pkg

    routes_info = []

    # Iterate through all modules in app/routers/admin
    for _, module_name, ispkg in pkgutil.iter_modules(admin_pkg.__path__):
        if ispkg:
            continue

        module = importlib.import_module(f"app.routers.admin.{module_name}")

        # Skip modules without a router
        router_obj = getattr(module, "router", None)
        if router_obj is None:
            continue

        module_routes = []

        for route in router_obj.routes:
            if isinstance(route, APIRoute):
                module_routes.append(
                    {
                        "path": route.path,
                        "methods": list(route.methods),
                        "name": route.name,
                        "summary": route.summary,
                        "endpoint": route.endpoint.__name__,
                    }
                )

        routes_info.append(
            {
                "module": module_name,
                "prefix": router_obj.prefix,
                "tags": router_obj.tags,
                "routes": module_routes,
            }
        )

    return routes_info


@router.get("/")
def admin_docs_index():
    """
    Returns a structured index of all admin routers and their routes.
    Perfect for building a documentation UI in the browser.
    """
    return {
        "title": "Admin API Documentation",
        "description": "Auto‑generated index of all admin routers and endpoints.",
        "modules": _discover_admin_routes(),
    }
