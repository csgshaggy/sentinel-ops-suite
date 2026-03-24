from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

from tools.super_doctor import run_super_doctor


def _load_config(path: str) -> Dict[str, Any]:
    """
    Load a JSON configuration file safely.
    """
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_results(path: str, results: Dict[str, Any]) -> None:
    """
    Save doctor results to a JSON file.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    except Exception as exc:
        print(f"Failed to save results: {exc}", file=sys.stderr)


def _format_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a high-level summary of doctor results.
    """
    checks = results.get("checks", [])
    passed = sum(1 for c in checks if c.get("status") == "pass")
    failed = sum(1 for c in checks if c.get("status") == "fail")

    return {
        "total_checks": len(checks),
        "passed": passed,
        "failed": failed,
        "overall_status": "healthy" if failed == 0 else "issues_detected",
    }


def run_doctor(
    config_path: str | None = None, output_path: str | None = None
) -> Dict[str, Any]:
    """
    Execute the Super Doctor with optional config and output paths.
    """
    config = _load_config(config_path) if config_path else {}

    try:
        results = run_super_doctor(config)
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "config_used": config,
        }

    summary = _format_summary(results)

    final = {
        "success": True,
        "summary": summary,
        "results": results,
        "config_used": config,
    }

    if output_path:
        _save_results(output_path, final)

    return final


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the SSRF Super Doctor.")
    parser.add_argument("--config", help="Path to doctor config JSON", default=None)
    parser.add_argument("--output", help="Path to save results JSON", default=None)

    args = parser.parse_args()

    output = run_doctor(args.config, args.output)
    print(json.dumps(output, indent=2))
