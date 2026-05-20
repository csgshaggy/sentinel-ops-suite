from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from app.utils.modes import Mode
from tools.super_doctor import run_super_doctor


def run_super_doctor_runner(
    project_root: Path,
    mode: Mode = Mode.LOCAL,
) -> Dict[str, Any]:
    """
    Wrapper around run_super_doctor() that normalizes output for API/TUI usage.

    - Accepts a project root and Mode enum
    - Passes config into run_super_doctor()
    - Returns a stable, predictable JSON structure
    """

    # Convert Mode enum into config
    config = {
        "mode": mode.value,
        "project_root": str(project_root),
    }

    # Execute the doctor
    result = run_super_doctor(config=config)

    # Normalize output for API consumers
    return {
        "summary": result["summary"],
        "checks": result["checks"],
        "config_used": result.get("config_used", config),
    }


# CLI entrypoint for manual testing
if __name__ == "__main__":
    import json

    output = run_super_doctor_runner(
        project_root=Path("."),
        mode=Mode.LOCAL,
    )
    print(json.dumps(output, indent=2))
