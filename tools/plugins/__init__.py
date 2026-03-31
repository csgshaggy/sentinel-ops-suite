"""
Canonical plugin registry for SuperDoctor.

This file is the authoritative source of truth for:
- plugin imports
- plugin metadata
- plugin entrypoints
- sync/async mode declarations

SuperDoctor imports ONLY from this registry.
No dynamic imports. No drift. No ambiguity.
"""

from __future__ import annotations

from typing import Callable, Dict

# --- Explicit plugin imports (alphabetical, deterministic) ---
from .cpu_load import run as cpu_load
from .dependency_drift import run as dependency_drift
from .disk_space import run as disk_space
from .env_vars import run as env_vars
from .file_system import run as file_system
from .git_status import run as git_status
from .kernel_info import run as kernel_info
from .logging_config import run as logging_config
from .makefile_health import run as makefile_health
from .memory_health import run as memory_health
from .network_health import run as network_health
from .os_info import run as os_info
from .os_release import run as os_release
from .package_integrity import run as package_integrity
from .process_health import run as process_health
from .python_version import run as python_version
from .requirements_lock import run as requirements_lock
from .security_baseline import run as security_baseline
from .shell_env import run as shell_env
from .storage_health import run as storage_health
from .system_limits import run as system_limits
from .system_services import run as system_services
from .system_uptime import run as system_uptime
from .temp_sensors import run as temp_sensors
from .time_sync import run as time_sync
from .user_sessions import run as user_sessions
from .virtualization import run as virtualization
from .zombie_processes import run as zombie_processes

# --- Canonical plugin registry map ---

PLUGIN_REGISTRY: Dict[str, Callable] = {
    "cpu_load": cpu_load,
    "dependency_drift": dependency_drift,
    "disk_space": disk_space,
    "env_vars": env_vars,
    "file_system": file_system,
    "git_status": git_status,
    "kernel_info": kernel_info,
    "logging_config": logging_config,
    "makefile_health": makefile_health,
    "memory_health": memory_health,
    "network_health": network_health,
    "os_info": os_info,
    "os_release": os_release,
    "package_integrity": package_integrity,
    "process_health": process_health,
    "python_version": python_version,
    "requirements_lock": requirements_lock,
    "security_baseline": security_baseline,
    "shell_env": shell_env,
    "storage_health": storage_health,
    "system_limits": system_limits,
    "system_services": system_services,
    "system_uptime": system_uptime,
    "temp_sensors": temp_sensors,
    "time_sync": time_sync,
    "user_sessions": user_sessions,
    "virtualization": virtualization,
    "zombie_processes": zombie_processes,
}

__all__ = ["PLUGIN_REGISTRY"]
