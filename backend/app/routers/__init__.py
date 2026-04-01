from .system import router as system
from .admin import router as admin
from .git_snapshots import router as git_snapshots
from .pelm import router as pelm
from .pelm_stream import router as pelm_stream
from .plugins import router as plugins

from .workflow_runs import router as workflow_runs
from .makefile_diff import router as makefile_diff
from .makefile_health import router as makefile_health
from .router_drift import router as router_drift
from .repo_health import router as repo_health
from .ci_summary import router as ci_summary

__all__ = [
    "system",
    "admin",
    "git_snapshots",
    "pelm",
    "pelm_stream",
    "plugins",
    "workflow_runs",
    "makefile_diff",
    "makefile_health",
    "router_drift",
    "repo_health",
    "ci_summary",
]
