from __future__ import annotations

import importlib
import json
import pkgutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional


PLUGIN_PACKAGE = "tools.plugins"


# ------------------------------------------------------------
# Plugin Discovery
# ------------------------------------------------------------


def _iter_plugin_modules() -> List[str]:
    """
    Discover plugin modules under tools.plugins.
    Skips packages and private modules.
    """
    package = importlib.import_module(PLUGIN_PACKAGE)
    path = package.__path__  # type: ignore[attr-defined]

    modules: List[str] = []
    for _finder, name, ispkg in pkgutil.iter_modules(path):
        if ispkg:
            continue
        if name.startswith("_"):
            continue
        modules.append(name)
    return modules


def _load_plugin_metadata(module_name: str) -> Optional[Dict[str, Any]]:
    """
    Load plugin metadata from a module.

    Convention:
      - Optional PLUGIN_INFO dict:
          {
            "name": "git_status",
            "category": "scm",
            "entrypoint": "get_git_status",
          }

      - If PLUGIN_INFO is missing, we infer:
          name = module_name
          category = "general"
          entrypoint = first callable starting with "get_"
    """
    module = importlib.import_module(f"{PLUGIN_PACKAGE}.{module_name}")

    info: Dict[str, Any] = {
        "name": module_name,
        "category": "general",
        "entrypoint": None,
    }

    plugin_info = getattr(module, "PLUGIN_INFO", None)
    if isinstance(plugin_info, dict):
        info.update(plugin_info)

    if not info.get("entrypoint"):
        for attr_name in dir(module):
            if attr_name.startswith("get_"):
                candidate = getattr(module, attr_name)
                if callable(candidate):
                    info["entrypoint"] = attr_name
                    break

    if not info.get("entrypoint"):
        return None

    return info


def _load_plugin_callable(meta: Dict[str, Any]) -> Callable[[], Dict[str, Any]]:
    """
    Resolve the plugin callable from metadata.
    """
    module_name = meta["module"]
    entrypoint = meta["entrypoint"]
    module = importlib.import_module(f"{PLUGIN_PACKAGE}.{module_name}")
    func = getattr(module, entrypoint)
    if not callable(func):
        raise TypeError(f"Entrypoint {entrypoint} in {module_name} is not callable")
    return func


def _discover_plugins(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Discover plugins and apply config-based filtering.

    Config:
      - plugins: optional list of plugin names to run
    """
    enabled = config.get("plugins")
    modules = _iter_plugin_modules()

    plugins: List[Dict[str, Any]] = []
    for module_name in modules:
        meta = _load_plugin_metadata(module_name)
        if not meta:
            continue

        meta["module"] = module_name
        name = meta.get("name", module_name)

        if enabled is not None and name not in enabled:
            continue

        plugins.append(meta)

    return plugins


# ------------------------------------------------------------
# Plugin Execution
# ------------------------------------------------------------


def _run_plugin(
    meta: Dict[str, Any],
    func: Callable[[], Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Execute a plugin safely with timing and structured output.
    """
    name = meta.get("name", meta["module"])
    category = meta.get("category", "general")

    started = time.time()
    try:
        result = func()
        success = bool(result.get("success", True))
        status = "pass" if success else "fail"
        error: Optional[str] = None
    except Exception as exc:
        result = {"success": False, "error": str(exc)}
        success = False
        status = "fail"
        error = str(exc)
    finished = time.time()

    return {
        "plugin": name,
        "category": category,
        "status": status,
        "success": success,
        "error": error,
        "duration_seconds": round(finished - started, 4),
        "result": result,
    }


# ------------------------------------------------------------
# Health Scoring
# ------------------------------------------------------------


def _compute_health_score(checks: List[Dict[str, Any]], config: Dict[str, Any]) -> int:
    """
    Compute a 0-100 health score based on plugin results and optional weights.

    Config example:
      {
        "weights": {
          "scm": 2.0,
          "kernel": 1.5,
          "os": 1.0,
          "python": 1.0,
          "general": 1.0
        }
      }
    """
    weights_cfg: Dict[str, float] = config.get("weights", {})
    total_weight = 0.0
    passed_weight = 0.0

    for check in checks:
        category = check.get("category", "general")
        weight = float(weights_cfg.get(category, 1.0))
        total_weight += weight
        if check.get("success"):
            passed_weight += weight

    if total_weight == 0:
        return 100

    score = int(round((passed_weight / total_weight) * 100))
    return max(0, min(100, score))


# ------------------------------------------------------------
# Doctor Orchestration
# ------------------------------------------------------------


def run_super_doctor(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Execute all discovered plugins (optionally filtered) in parallel
    and return structured results with health scoring.
    """
    config = config or {}
    max_workers = int(config.get("max_workers", 4))

    plugins_meta = _discover_plugins(config)
    checks: List[Dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _run_plugin,
                meta,
                _load_plugin_callable(meta),
            ): meta
            for meta in plugins_meta
        }

        for future in as_completed(futures):
            meta = futures[future]
            name = meta.get("name", meta["module"])
            try:
                checks.append(future.result())
            except Exception as exc:
                checks.append(
                    {
                        "plugin": name,
                        "category": "general",
                        "status": "fail",
                        "success": False,
                        "error": str(exc),
                        "duration_seconds": 0.0,
                        "result": {"success": False, "error": str(exc)},
                    }
                )

    passed = sum(1 for c in checks if c.get("success"))
    failed = sum(1 for c in checks if not c.get("success"))
    health_score = _compute_health_score(checks, config)

    return {
        "success": failed == 0,
        "summary": {
            "total": len(checks),
            "passed": passed,
            "failed": failed,
            "overall_status": "healthy" if failed == 0 else "issues_detected",
            "health_score": health_score,
        },
        "checks": checks,
        "config_used": config,
    }


if __name__ == "__main__":
    print(json.dumps(run_super_doctor(), indent=2))
