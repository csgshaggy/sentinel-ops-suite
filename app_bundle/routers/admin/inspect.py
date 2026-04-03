from __future__ import annotations

import inspect
import sys
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/admin/inspect", tags=["admin-inspect"])


def _safe_getattr(obj: Any, name: str) -> Any:
    """
    Safely retrieve an attribute without raising unexpected exceptions.
    """
    try:
        return getattr(obj, name)
    except Exception:
        return "<unavailable>"


def _describe_object(obj: Any) -> Dict[str, Any]:
    """
    Provide a structured description of a Python object.
    """
    return {
        "type": type(obj).__name__,
        "module": getattr(obj, "__module__", None),
        "doc": inspect.getdoc(obj),
        "repr": repr(obj),
    }


@router.get("/modules", summary="List loaded Python modules")
def list_loaded_modules() -> Dict[str, Any]:
    """
    Return a list of currently loaded Python modules.
    """
    modules = sorted(sys.modules.keys())
    return {
        "count": len(modules),
        "modules": modules,
    }


@router.get("/module/{module_name}", summary="Inspect a specific module")
def inspect_module(module_name: str) -> Dict[str, Any]:
    """
    Inspect a specific module by name.
    """
    module = sys.modules.get(module_name)
    if module is None:
        return {
            "found": False,
            "error": f"Module '{module_name}' is not loaded.",
        }

    attributes: List[str] = []
    try:
        attributes = sorted(dir(module))
    except Exception:
        attributes = []

    return {
        "found": True,
        "module": module_name,
        "attributes": attributes,
        "description": _describe_object(module),
    }


@router.get("/object/{module_name}/{attr}", summary="Inspect an attribute of a module")
def inspect_object(module_name: str, attr: str) -> Dict[str, Any]:
    """
    Inspect a specific attribute inside a module.
    """
    module = sys.modules.get(module_name)
    if module is None:
        return {
            "found": False,
            "error": f"Module '{module_name}' is not loaded.",
        }

    obj = _safe_getattr(module, attr)
    return {
        "module": module_name,
        "attribute": attr,
        "description": _describe_object(obj),
    }
