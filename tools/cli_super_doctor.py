from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from tools.super_doctor import run_super_doctor


def _load_config(path: str | None) -> Dict[str, Any]:
    """
    Load a JSON config file if provided.
    """
    if not path:
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        return {
            "error": f"Failed to load config: {exc}",
            "config_path": path,
        }


def _write_output(path: str, data: Dict[str, Any]) -> None:
    """
    Write results to a JSON file.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as exc:
        print(f"Failed to write output: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the SSRF Super Doctor from the CLI."
    )
    parser.add_argument("--config", help="Path to config JSON", default=None)
    parser.add_argument("--output", help="Path to save results JSON", default=None)
    parser.add_argument(
        "--min-health",
        type=int,
        default=None,
        help="Minimum health score required for success (0-100).",
    )

    args = parser.parse_args()

    config = _load_config(args.config)

    try:
        results = run_super_doctor(config)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        sys.exit(1)

    final = {
        "success": results.get("success", False),
        "results": results,
        "config_used": config,
    }

    if args.output:
        _write_output(args.output, final)

    print(json.dumps(final, indent=2))

    # ------------------------------------------------------------
    # CI Enforcement Logic
    # ------------------------------------------------------------
    summary = results.get("summary", {})
    health_score = summary.get("health_score", 0)

    exit_code = 0

    # Fail if any plugin failed
    if not results.get("success", False):
        exit_code = 1

    # Fail if health score below threshold
    if args.min_health is not None and health_score < args.min_health:
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
