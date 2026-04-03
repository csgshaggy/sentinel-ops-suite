from fastapi import APIRouter
from backend.pelm import pelm_plugin
from backend.pelm.pelm_tools import (
    detect_pelm_drift,
    detect_pelm_regression,
    validate_pelm_contract,
)
from backend.pelm.report_generator import (
    generate_html_report,
    generate_markdown_report,
)
from backend.pelm.pelm_tools import snapshot_pelm_output
from pathlib import Path
import json

router = APIRouter(prefix="/pelm", tags=["PELM Reports"])

SNAPSHOT_DIR = Path("backend/pelm/snapshots")


@router.get("/run")
def run_pelm():
    output = pelm_plugin.run_pelm()
    contract = validate_pelm_contract(output)
    snapshot_pelm_output(output)
    return {"output": output, "contract": contract}


@router.get("/status")
def pelm_status():
    output = pelm_plugin.run_pelm()
    drift = detect_pelm_drift()
    regression = detect_pelm_regression()
    contract = validate_pelm_contract(output)
    return {
        "output": output,
        "drift": drift,
        "regression": regression,
        "contract": contract,
    }


@router.get("/report/html")
def pelm_report_html():
    output = pelm_plugin.run_pelm()
    drift = detect_pelm_drift()
    regression = detect_pelm_regression()
    contract = validate_pelm_contract(output)
    snapshots = list(SNAPSHOT_DIR.glob("*.json"))
    snapshots = [json.loads(p.read_text()) for p in snapshots]

    return generate_html_report(output, drift, regression, snapshots, contract)


@router.get("/report/markdown")
def pelm_report_markdown():
    output = pelm_plugin.run_pelm()
    drift = detect_pelm_drift()
    regression = detect_pelm_regression()
    contract = validate_pelm_contract(output)
    snapshots = list(SNAPSHOT_DIR.glob("*.json"))
    snapshots = [json.loads(p.read_text()) for p in snapshots]

    return generate_markdown_report(output, drift, regression, snapshots, contract)


@router.get("/snapshots/list")
def pelm_snapshot_list():
    return [p.name for p in SNAPSHOT_DIR.glob("*.json")]


@router.get("/snapshots/get/{name}")
def pelm_snapshot_get(name: str):
    path = SNAPSHOT_DIR / name
    if not path.exists():
        return {"error": "Snapshot not found"}
    return json.loads(path.read_text())
