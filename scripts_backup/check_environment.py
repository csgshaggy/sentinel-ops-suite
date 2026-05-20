from __future__ import annotations

import os
import platform
import sys
from typing import Any, Dict


def check(value: Any) -> bool:
    """
    Replacement for the old lambda-based check.
    Returns True if the value is not None.
    """
    return value is not None


def get_python_info() -> Dict[str, Any]:
    """
    Return structured information about the Python runtime.
    """
    return {
        "version": sys.version,
        "executable": sys.executable,
        "prefix": sys.prefix,
        "implementation": platform.python_implementation(),
    }


def get_os_info() -> Dict[str, Any]:
    """
    Return structured information about the operating system.
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def get_env_vars(prefix: str | None = None) -> Dict[str, str]:
    """
    Return environment variables, optionally filtered by prefix.
    """
    env = dict(os.environ)
    if prefix:
        env = {k: v for k, v in env.items() if k.startswith(prefix)}
    return env


def run_environment_check() -> Dict[str, Any]:
    """
    Perform a full environment diagnostic pass.
    """
    return {
        "python": get_python_info(),
        "os": get_os_info(),
        "environment_variables": get_env_vars(),
        "cwd": os.getcwd(),
        "path_entries": sys.path,
    }


if __name__ == "__main__":
    # Allow this script to be run directly for debugging
    import json

    print(json.dumps(run_environment_check(), indent=2))
