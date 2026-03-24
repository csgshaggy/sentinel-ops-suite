from __future__ import annotations

import os
from typing import Dict, Optional

PLUGIN_INFO = {
    "name": "os_release",
    "category": "os",
    "entrypoint": "get_os_release_info",
}


def _parse_line(line: str) -> Optional[tuple[str, str]]:
    """
    Parse a KEY=VALUE line from /etc/os-release.
    """
    if "=" not in line:
        return None

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"')

    if not key:
        return None

    return key, value


def _read_os_release(path: str = "/etc/os-release") -> Dict[str, str]:
    """
    Read and parse /etc/os-release into a dict.
    """
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return {}

    data: Dict[str, str] = {}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parsed = _parse_line(line)
        if parsed:
            key, value = parsed
            data[key] = value

    return data


def get_os_release_info() -> Dict[str, object]:
    """
    Return parsed OS release metadata.
    """
    data = _read_os_release()

    return {
        "success": len(data) > 0,
        "fields": data,
        "pretty_name": data.get("PRETTY_NAME"),
        "name": data.get("NAME"),
        "version": data.get("VERSION"),
        "id": data.get("ID"),
        "id_like": data.get("ID_LIKE"),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_os_release_info(), indent=2))
