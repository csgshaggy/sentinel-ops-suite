from fastapi import APIRouter
import pkgutil
import importlib

router = APIRouter()

# Auto-discover all modules in this package
for module in pkgutil.iter_modules(__path__):
    if module.name.startswith("_"):
        continue

    mod = importlib.import_module(f"{__name__}.{module.name}")

    if hasattr(mod, "router"):
        router.include_router(mod.router)
