from __future__ import annotations

import os
from typing import List

from fastapi import APIRouter, HTTPException

from backend.app.core.plugin_loader import (
    get_all_plugins,
    get_plugin_by_id,
    run_plugin,
)
from backend.app.core.metrics import get_timing_histogram
from backend.app.models.plugin_models import PluginResponse, TimingBucketResponse

router = APIRouter()


# ------------------------------------------------------------
# Plugin Listing
# ------------------------------------------------------------
@router.get("/plugins", response_model=List[PluginResponse])
async def list_plugins() -> List[PluginResponse]:
    """
    Return metadata for all available plugins.
    """
    plugins = get_all_plugins()
    return [p.to_dict() for p in plugins]


# ------------------------------------------------------------
# Plugin Details
# ------------------------------------------------------------
@router.get("/plugins/{plugin_id}", response_model=PluginResponse)
async def get_plugin(plugin_id: str) -> PluginResponse:
    """
    Return metadata for a single plugin.
    """
    plugin = get_plugin_by_id(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return plugin.to_dict()


# ------------------------------------------------------------
# Plugin Execution
# ------------------------------------------------------------
@router.post("/plugins/{plugin_id}/run")
async def execute_plugin(plugin_id: str) -> dict:
    """
    Execute a plugin and return its result.
    """
    plugin = get_plugin_by_id(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")

    result = await run_plugin(plugin)
    return {"status": "ok", "result": result}


# ------------------------------------------------------------
# Timing Metrics
# ------------------------------------------------------------
@router.get("/metrics/timing", response_model=List[TimingBucketResponse])
async def get_timing_buckets() -> List[TimingBucketResponse]:
    """
    Return timing histogram buckets for plugin execution.
    """
    return get_timing_histogram()


# ------------------------------------------------------------
# Plugin Logs
# ------------------------------------------------------------
@router.get("/plugins/{plugin_id}/logs", response_model=List[str])
async def get_plugin_logs(plugin_id: str) -> List[str]:
    """
    Return the last 200 log lines for a plugin.
    """
    log_path = f"/var/log/superdoctor/{plugin_id}.log"

    if not os.path.exists(log_path):
        return ["No logs found for this plugin."]

    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {exc}")

    return [line.rstrip("\n") for line in lines[-200:]]
