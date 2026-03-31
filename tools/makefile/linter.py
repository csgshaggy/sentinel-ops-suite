from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

TARGET = Path(__file__).parents[2] / "Makefile"


def lint_makefile(json_mode: bool = False) -> Dict[str, Any]:
    if not TARGET.exists():
        raise FileNotFoundError("Makefile missing")

    lines = TARGET.read_text().splitlines()

    issues = []

    for i, line in enumerate(lines, start=1):
        if line.startswith(" ") and "\t" not in line:
            issues.append(f"Line {i}: rule commands must start with a TAB")

        if re.match(r"^[A-Za-z0-9_-]+:", line) and " " in line.split(":")[0]:
            issues.append(f"Line {i}: target contains spaces")

    ok = len(issues) == 0

    result = {
        "ok": ok,
        "issues": issues,
        "line_count": len(lines),
    }

    if json_mode:
        print(json.dumps(result, indent=2))

    return result
