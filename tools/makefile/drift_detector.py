from __future__ import annotations

import difflib
import json
import time
from pathlib import Path
from typing import Dict, Any


CANONICAL = Path(__file__).parent / "Makefile.canonical"
TARGET = Path(__file__).parents[2] / "Makefile"


def detect_drift(json_mode: bool = False) -> Dict[str, Any]:
    if not CANONICAL.exists():
        raise FileNotFoundError("Canonical Makefile missing")

    if not TARGET.exists():
        raise FileNotFoundError("Project Makefile missing")

    canonical = CANONICAL.read_text().splitlines()
    target = TARGET.read_text().splitlines()

    diff = list(
        difflib.unified_diff(
            canonical,
            target,
            fromfile="Makefile.canonical",
            tofile="Makefile",
            lineterm="",
        )
    )

    drift = len(diff) > 0

    result = {
        "timestamp": time.time(),
        "drift": drift,
        "diff": diff,
        "canonical_path": str(CANONICAL),
        "target_path": str(TARGET),
    }

    if json_mode:
        print(json.dumps(result, indent=2))

    return result
