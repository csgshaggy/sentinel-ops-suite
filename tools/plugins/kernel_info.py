from __future__ import annotations

import platform
import subprocess
from typing import Any, Dict, Optional

PLUGIN_INFO = {
    "name": "kernel_info",
    "category": "kernel",
    "entrypoint": "get_kernel_info",
}


def _run_uname(flag: str) -> Optional[str]:
    """
    Run uname with a specific flag and return output or None on failure.
    """
    try:
        result = subprocess.run(
            ["uname", flag],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=1,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def get_kernel_info() -> Dict[str, Any]:
    """
    Collect kernel and platform information.
    """
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()

    return {
        "success": True,
        "platform": {
            "system": system,
            "release": release,
            "version": version,
            "machine": machine,
            "processor": processor,
        },
        "uname": {
            "kernel_name": _run_uname("-s"),
            "kernel_release": _run_uname("-r"),
            "kernel_version": _run_uname("-v"),
            "machine": _run_uname("-m"),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_kernel_info(), indent=2))
