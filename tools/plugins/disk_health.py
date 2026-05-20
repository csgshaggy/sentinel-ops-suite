"""
Disk health check plugin (sync).

Performs a basic read/write sanity check on the filesystem to ensure
the disk is responsive and not exhibiting immediate I/O failures.
"""

from __future__ import annotations

import os
import tempfile
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Performs a basic disk read/write health check.",
    "entrypoint": "run",
    "mode": "sync",
}


def _disk_rw_test() -> bool:
    """
    Perform a simple write/read/delete test in the system temp directory.
    Returns True if successful, False otherwise.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            test_path = tmp.name
            tmp.write(b"ssrf-console-disk-health-test")
            tmp.flush()

        # Read back
        with open(test_path, "rb") as f:
            content = f.read()

        # Cleanup
        os.remove(test_path)

        return content == b"ssrf-console-disk-health-test"
    except Exception:
        return False


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous disk health check.
    """
    try:
        ok = _disk_rw_test()

        if ok:
            status = Status.OK
            message = "Disk read/write test passed."
        else:
            status = Status.FAIL
            message = "Disk read/write test failed."

        data = {
            "rw_test_passed": ok,
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=status,
            message=message,
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Disk health plugin failed: {exc}",
        )
