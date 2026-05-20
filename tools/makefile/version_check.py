from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict

TARGET = Path(__file__).parents[2] / "Makefile"
VERSION_REGEX = re.compile(r"^VERSION\s*=\s*(.+)$")


def check_version(json_mode: bool = False) -> Dict[str, Any]:
    if not TARGET.exists():
        raise FileNotFoundError("Makefile missing")

    version = None
    found = False

    for line in TARGET.read_text().splitlines():
        m = VERSION_REGEX.match(line)
        if m:
            version = m.group(1).strip()
            found = True
            break

    result = {
        "found": found,
        "version": version,
    }

    if json_mode:
        import json

        print(json.dumps(result, indent=2))

    return result
