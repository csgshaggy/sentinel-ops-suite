from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# -------------------------
# Admin Routers (All Panels You Have)
# -------------------------

from app.routers.admin.index import router as admin_index_router
from app.routers.admin.home import router as admin_home_router
from app.routers.admin.logs import router as admin_logs_router
from app.routers.admin.system import router as admin_system_router
from app.routers.admin.processes import router as admin_processes_router
from app.routers.admin.network import router as admin_network_router
from app.routers.admin.services import router as admin_services_router
from app.routers.admin.security import router as admin_security_router
from app.routers.admin.config import router as admin_config_router
from app.routers.admin.storage import router as admin_storage_router
from app.routers.admin.firewall import router as admin_firewall_router
from app.routers.admin.users import router as admin_users_router
from app.routers.admin.metrics import router as admin_metrics_router
from app.routers.admin.tasks import router as admin_tasks_router
from app.routers.admin.scheduler import router as admin_scheduler_router
from app.routers.admin.events import router as admin_events_router
from app.routers.admin.audit import router as admin_audit_router
from app.routers.admin.packages import router as admin_packages_router
from app.routers.admin.kernel import router as admin_kernel_router
from app.routers.admin.hardware import router as admin_hardware_router
from app.routers.admin.boot import router as admin_boot_router
from app.routers.admin.performance import router as admin_performance_router
from app.routers.admin.health import router as admin_health_router
from app.routers.admin.runtime import router as admin_runtime_router
from app.routers.admin.env import router as admin_env_router
from app.routers.admin.limits import router as admin_limits_router
from app.routers.admin.threads import router as admin_threads_router
from app.routers.admin.paths import router as admin_paths_router
from app.routers.admin.inspect import router as admin_inspect_router
from app.routers.admin.cache import router as admin_cache_router
from app.routers.admin.sockets import router as admin_sockets_router
from app.routers.admin.timers import router as admin_timers_router
from app.routers.admin.locks import router as admin_locks_router
from app.routers.admin.signals import router as admin_signals_router
from app.routers.admin.deadlock import router as admin_deadlock_router
from app.routers.admin.async_panel import router as admin_async_router   # FIXED


# -------------------------
# FastAPI App
# -------------------------

app = FastAPI(
    title="Operator Console",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Serve static files (dark mode CSS, etc.)
app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")


# -------------------------
# Root Redirect
# -------------------------

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(
        '<html><head><meta http-equiv="refresh" content="0; url=/admin/index" /></head><body></body></html>'
    )


# -------------------------
# Admin Router Includes
# -------------------------

app.include_router(admin_index_router)
app.include_router(admin_home_router)
app.include_router(admin_logs_router)
app.include_router(admin_system_router)
app.include_router(admin_processes_router)
app.include_router(admin_network_router)
app.include_router(admin_services_router)
app.include_router(admin_security_router)
app.include_router(admin_config_router)
app.include_router(admin_storage_router)
app.include_router(admin_firewall_router)
app.include_router(admin_users_router)
app.include_router(admin_metrics_router)
app.include_router(admin_tasks_router)
app.include_router(admin_scheduler_router)
app.include_router(admin_events_router)
app.include_router(admin_audit_router)
app.include_router(admin_packages_router)
app.include_router(admin_kernel_router)
app.include_router(admin_hardware_router)
app.include_router(admin_boot_router)
app.include_router(admin_performance_router)
app.include_router(admin_health_router)
app.include_router(admin_runtime_router)
app.include_router(admin_env_router)
app.include_router(admin_limits_router)
app.include_router(admin_threads_router)
app.include_router(admin_paths_router)
app.include_router(admin_inspect_router)
app.include_router(admin_cache_router)
app.include_router(admin_sockets_router)
app.include_router(admin_timers_router)
app.include_router(admin_locks_router)
app.include_router(admin_signals_router)
app.include_router(admin_deadlock_router)
app.include_router(admin_async_router)
