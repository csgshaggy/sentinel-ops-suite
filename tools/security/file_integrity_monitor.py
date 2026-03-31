from __future__ import annotations

import hashlib
import json
import os
import stat
import time
from pathlib import Path
from typing import Any, Dict, List

BASELINE_PATH = Path("state/fim_baseline.json")
EVENT_LOG = Path("logs/events.log")


# ------------------------------------------------------------
# Safe Hashing (Handles PermissionError)
# ------------------------------------------------------------


def _sha256(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, OSError):
        return None


# ------------------------------------------------------------
# Safe Metadata Collection (Handles PermissionError)
# ------------------------------------------------------------


def _collect_metadata(path: Path) -> Dict[str, Any]:
    try:
        st = path.stat()
    except (PermissionError, OSError):
        return {
            "path": str(path),
            "unreadable": True,
            "sha256": None,
            "size": None,
            "mtime": None,
            "mode": None,
            "owner": None,
            "group": None,
        }

    return {
        "path": str(path),
        "unreadable": False,
        "size": st.st_size,
        "mtime": st.st_mtime,
        "mode": stat.filemode(st.st_mode),
        "owner": st.st_uid,
        "group": st.st_gid,
        "sha256": _sha256(path),
    }


# ------------------------------------------------------------
# Event Logging
# ------------------------------------------------------------


def _write_event(event: Dict[str, Any]) -> None:
    EVENT_LOG.parent.mkdir(exist_ok=True)
    with EVENT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


# ------------------------------------------------------------
# Baseline Builder
# ------------------------------------------------------------


def build_baseline(targets: List[str]) -> Dict[str, Any]:
    baseline = {}

    for t in targets:
        p = Path(t)

        if p.is_file():
            baseline[str(p)] = _collect_metadata(p)

        elif p.is_dir():
            for root, _, files in os.walk(p):
                for f in files:
                    fp = Path(root) / f
                    baseline[str(fp)] = _collect_metadata(fp)

    BASELINE_PATH.parent.mkdir(exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2))

    return baseline


# ------------------------------------------------------------
# Baseline Loader
# ------------------------------------------------------------


def load_baseline() -> Dict[str, Any]:
    if not BASELINE_PATH.exists():
        return {}
    return json.loads(BASELINE_PATH.read_text())


# ------------------------------------------------------------
# FIM Scan
# ------------------------------------------------------------


def scan(targets: List[str]) -> Dict[str, Any]:
    baseline = load_baseline()
    current = {}

    # Collect current metadata
    for t in targets:
        p = Path(t)

        if p.is_file():
            current[str(p)] = _collect_metadata(p)

        elif p.is_dir():
            for root, _, files in os.walk(p):
                for f in files:
                    fp = Path(root) / f
                    current[str(fp)] = _collect_metadata(fp)

    anomalies = []

    # Detect modifications & deletions
    for path, old_meta in baseline.items():
        # Deleted file
        if path not in current:
            anomalies.append({"type": "deleted", "path": path})
            _write_event(
                {"timestamp": time.time(), "event": "file_deleted", "path": path}
            )
            continue

        new_meta = current[path]

        # Permission or metadata changes
        if not old_meta.get("unreadable") and not new_meta.get("unreadable"):
            if old_meta["mode"] != new_meta["mode"]:
                anomalies.append({"type": "perm_changed", "path": path})
                _write_event(
                    {
                        "timestamp": time.time(),
                        "event": "permission_changed",
                        "path": path,
                    }
                )

            if old_meta["sha256"] != new_meta["sha256"]:
                anomalies.append({"type": "modified", "path": path})
                _write_event(
                    {"timestamp": time.time(), "event": "file_modified", "path": path}
                )

        # File became unreadable
        if old_meta.get("unreadable") != new_meta.get("unreadable"):
            anomalies.append({"type": "readability_changed", "path": path})
            _write_event(
                {"timestamp": time.time(), "event": "readability_changed", "path": path}
            )

    # Detect new files
    for path in current:
        if path not in baseline:
            anomalies.append({"type": "added", "path": path})
            _write_event(
                {"timestamp": time.time(), "event": "file_added", "path": path}
            )

    return {
        "timestamp": time.time(),
        "baseline_count": len(baseline),
        "current_count": len(current),
        "anomalies": anomalies,
        "ok": len(anomalies) == 0,
    }
