"""
SuperDoctor Plugin Loader

Responsible for:
- Selecting plugins (by id, category, or 'all')
- Executing them with a given Mode and project_root
- Aggregating CheckResult objects
"""

from pathlib import Path
from typing import Dict, Iterable, List

from tools.plugins import PluginMeta, get_plugin, list_plugins
from tools.super_doctor import CheckResult
from utils.modes import Mode


def run_selected_plugins(
    plugin_ids: Iterable[str] | None,
    mode: Mode,
    project_root: Path | None,
) -> Dict[str, List[CheckResult]]:
    """
    Run a specific set of plugins.
    If plugin_ids is None, run all.
    Returns mapping: plugin_id -> list[CheckResult]
    """
    results: Dict[str, List[CheckResult]] = {}

    if plugin_ids is None:
        plugins: Iterable[PluginMeta] = list_plugins()
    else:
        plugins = [get_plugin(pid) for pid in plugin_ids]

    for meta in plugins:
        try:
            checks = meta.fn(mode, project_root)
        except Exception as exc:
            checks = [
                CheckResult(
                    id=f"{meta.id}.error",
                    name=f"{meta.name} failed",
                    description=f"Plugin raised an exception: {exc}",
                    status="fail",
                    severity="high",
                    plugin=meta.id,
                )
            ]
        results[meta.id] = checks

    return results


def run_by_category(
    category: str,
    mode: Mode,
    project_root: Path | None,
) -> Dict[str, List[CheckResult]]:
    plugins = [p for p in list_plugins() if p.category == category]
    return run_selected_plugins([p.id for p in plugins], mode, project_root)
