from __future__ import annotations

import os
import platform
import shutil
import sys
from typing import Any, Dict, List


def _check_python() -> Dict[str, Any]:
    """
    Validate Python runtime and environment.
    """
    return {
        "version": sys.version,
        "executable": sys.executable,
        "implementation": platform.python_implementation(),
        "ok": True,
    }


def _check_binaries(binaries: List[str]) -> List[Dict[str, Any]]:
    """
    Check whether required binaries exist in PATH.
    """
    results: List[Dict[str, Any]] = []

    for binary in binaries:
        path = shutil.which(binary)
        results.append(
            {
                "binary": binary,
                "found": path is not None,
                "path": path,
            }
        )

    return results


def _check_directories(directories: List[str]) -> List[Dict[str, Any]]:
    """
    Check whether required directories exist.
    """
    results: List[Dict[str, Any]] = []

    for directory in directories:
        exists = os.path.isdir(directory)
        results.append(
            {
                "directory": directory,
                "exists": exists,
            }
        )

    return results


def _check_files(files: List[str]) -> List[Dict[str, Any]]:
    """
    Check whether required files exist.
    """
    results: List[Dict[str, Any]] = []

    for file_path in files:
        exists = os.path.isfile(file_path)
        results.append(
            {
                "file": file_path,
                "exists": exists,
            }
        )

    return results


def run_preflight_scan() -> Dict[str, Any]:
    """
    Perform a full preflight scan of the environment.
    """
    required_binaries = ["python3", "pip", "git"]
    required_directories = ["backend", "dashboard", "tools"]
    required_files = ["Makefile", "README.md"]

    python_info = _check_python()
    binaries = _check_binaries(required_binaries)
    directories = _check_directories(required_directories)
    files = _check_files(required_files)

    return {
        "python": python_info,
        "binaries": binaries,
        "directories": directories,
        "files": files,
        "success": all(
            [
                python_info["ok"],
                all(b["found"] for b in binaries),
                all(d["exists"] for d in directories),
                all(f["exists"] for f in files),
            ]
        ),
    }


if __name__ == "__main__":
    import json

    results = run_preflight_scan()
    print(json.dumps(results, indent=2))
