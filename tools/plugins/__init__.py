"""
SuperDoctor Plugin Registry

Central index of all plugins and their human-readable metadata.
Each plugin must expose:

    run_checks(mode: Mode, project_root: Path | None) -> List[CheckResult]
"""

from pathlib import Path
from typing import Callable, Dict, List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# Import all plugin modules
from . import (
    async_health,
    build_artifacts,
    config_files,
    cpu_load,
    dependency_lock,
    disk_health,
    env_vars,
    event_loop,
    file_system,
    git_status,
    import_latency,
    kernel_info,
    logging_config,
    memory_health,
    module_conflicts,
    network_health,
    os_release,
    package_integrity,
    path_sanity,
    pip_health,
    process_tree,
    project_structure,
    python_flags,
    python_paths,
    python_process,
    python_version,
    runtime_limits,
    security_basics,
    signals,
    site_packages,
    symlink_safety,
    temp_files,
    thread_deadlock,
    trace_hooks,
    uptime_clock,
    virtualenv,
)

PluginFn = Callable[[Mode, Optional[Path]], List[CheckResult]]


class PluginMeta:
    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        module: object,
        entrypoint: str = "run_checks",
        description: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.module = module
        self.entrypoint = entrypoint
        self.description = description or name

    @property
    def fn(self) -> PluginFn:
        return getattr(self.module, self.entrypoint)


# Central registry
PLUGINS: Dict[str, PluginMeta] = {
    # System & OS Health
    "cpu_load": PluginMeta("cpu_load", "CPU Load & Saturation", "system", cpu_load),
    "memory_health": PluginMeta(
        "memory_health", "Memory Health", "system", memory_health
    ),
    "disk_health": PluginMeta(
        "disk_health", "Disk Health & Storage", "system", disk_health
    ),
    "network_health": PluginMeta(
        "network_health", "Network Health", "system", network_health
    ),
    "file_system": PluginMeta(
        "file_system", "Filesystem Sanity", "system", file_system
    ),
    "runtime_limits": PluginMeta(
        "runtime_limits", "Runtime Limits", "system", runtime_limits
    ),
    "process_tree": PluginMeta("process_tree", "Process Tree", "system", process_tree),
    "kernel_info": PluginMeta("kernel_info", "Kernel Info", "system", kernel_info),
    "os_release": PluginMeta("os_release", "OS Release", "system", os_release),
    "uptime_clock": PluginMeta(
        "uptime_clock", "Uptime & Clock", "system", uptime_clock
    ),
    # Python Environment
    "python_paths": PluginMeta("python_paths", "Python Paths", "python", python_paths),
    "python_process": PluginMeta(
        "python_process", "Python Process", "python", python_process
    ),
    "python_version": PluginMeta(
        "python_version", "Python Version", "python", python_version
    ),
    "virtualenv": PluginMeta(
        "virtualenv", "Virtualenv Integrity", "python", virtualenv
    ),
    "package_integrity": PluginMeta(
        "package_integrity", "Package Integrity", "python", package_integrity
    ),
    "pip_health": PluginMeta("pip_health", "pip Health", "python", pip_health),
    "site_packages": PluginMeta(
        "site_packages", "site-packages Layout", "python", site_packages
    ),
    "import_latency": PluginMeta(
        "import_latency", "Import Latency", "python", import_latency
    ),
    "module_conflicts": PluginMeta(
        "module_conflicts", "Module Conflicts", "python", module_conflicts
    ),
    "python_flags": PluginMeta("python_flags", "Python Flags", "python", python_flags),
    # Project / Repo Integrity
    "git_status": PluginMeta("git_status", "Git Status", "project", git_status),
    "env_vars": PluginMeta("env_vars", "Environment Variables", "project", env_vars),
    "security_basics": PluginMeta(
        "security_basics", "Security Basics", "project", security_basics
    ),
    "temp_files": PluginMeta("temp_files", "Temporary Files", "project", temp_files),
    "project_structure": PluginMeta(
        "project_structure", "Project Structure", "project", project_structure
    ),
    "config_files": PluginMeta("config_files", "Config Files", "project", config_files),
    "dependency_lock": PluginMeta(
        "dependency_lock", "Dependency Lock", "project", dependency_lock
    ),
    "build_artifacts": PluginMeta(
        "build_artifacts", "Build Artifacts", "project", build_artifacts
    ),
    "symlink_safety": PluginMeta(
        "symlink_safety", "Symlink Safety", "project", symlink_safety
    ),
    "path_sanity": PluginMeta("path_sanity", "Path Sanity", "project", path_sanity),
    # Observability & Diagnostics
    "logging_config": PluginMeta(
        "logging_config", "Logging Config", "observability", logging_config
    ),
    "trace_hooks": PluginMeta(
        "trace_hooks", "Trace Hooks", "observability", trace_hooks
    ),
    "thread_deadlock": PluginMeta(
        "thread_deadlock", "Thread Deadlock", "observability", thread_deadlock
    ),
    "async_health": PluginMeta(
        "async_health", "Async Health", "observability", async_health
    ),
    "signals": PluginMeta("signals", "Signal Handling", "observability", signals),
    "event_loop": PluginMeta("event_loop", "Event Loop", "observability", event_loop),
}


def list_plugins(category: str | None = None) -> List[PluginMeta]:
    if category is None:
        return list(PLUGINS.values())
    return [p for p in PLUGINS.values() if p.category == category]


def get_plugin(plugin_id: str) -> PluginMeta:
    return PLUGINS[plugin_id]
