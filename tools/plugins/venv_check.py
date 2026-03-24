from __future__ import annotations

import os
import sys
from typing import Dict, Any

PLUGIN_INFO = {
    "name": "venv_check",
    "category": "python",
    "entrypoint": "get_venv_status",
}


def _detect_venv() -> Dict[str, Any]:
    """
    Detect whether Python is running inside a virtual environment.
    """
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    in_venv = sys.prefix != base_prefix
    venv_env = os.environ.get("VIRTUAL_ENV")

    return {
        "in_venv": in_venv or venv_env is not None,
        "sys_prefix": sys.prefix,
        "base_prefix": base_prefix,
        "virtual_env_var": venv_env,
    }


def _detect_python_executable() -> Dict[str, Any]:
    """
    Return information about the Python executable.
    """
    exe = sys.executable
    return {
        "executable": exe,
        "exists": os.path.exists(exe),
    }


def get_venv_status() -> Dict[str, Any]:
    """
    Return combined virtual environment + Python executable status.
    """
    return {
        "success": True,
        "venv": _detect_venv(),
        "python": _detect_python_executable(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_venv_status(), indent=2))
