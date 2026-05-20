import difflib
from pathlib import Path

from backend.ci.makefile_canonical import CANONICAL_MAKEFILE

MAKEFILE_PATH = Path("Makefile")


def read_current_makefile() -> str:
    if not MAKEFILE_PATH.exists():
        return ""
    return MAKEFILE_PATH.read_text()


def validate_makefile() -> dict:
    current = read_current_makefile()
    is_match = current.strip() == CANONICAL_MAKEFILE.strip()
    return {
        "match": is_match,
        "length_current": len(current),
        "length_canonical": len(CANONICAL_MAKEFILE),
    }


def detect_drift() -> dict:
    current = read_current_makefile().splitlines(keepends=True)
    canonical = CANONICAL_MAKEFILE.splitlines(keepends=True)

    diff = list(
        difflib.unified_diff(
            canonical,
            current,
            fromfile="Makefile.canonical",
            tofile="Makefile",
        )
    )

    return {
        "drift": len(diff) > 0,
        "diff": "".join(diff),
    }


def auto_repair() -> dict:
    MAKEFILE_PATH.write_text(CANONICAL_MAKEFILE)
    return {
        "repaired": True,
        "path": str(MAKEFILE_PATH),
    }


def get_status() -> dict:
    validation = validate_makefile()
    drift = detect_drift()
    return {
        "validation": validation,
        "drift": {
            "drift": drift["drift"],
            "has_diff": bool(drift["diff"]),
        },
    }
