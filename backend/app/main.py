from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------------------------------
# PELM Imports (all modules created across Step 23)
# ------------------------------------------------------------
from app.pelm.pelm_status import get_pelm_status
from app.pelm.pelm_run import run_pelm
from app.pelm.pelm_trend import get_pelm_trend
from app.pelm.pelm_snapshots import (
    list_snapshots,
    get_snapshot,
    diff_snapshots,
)
from app.pelm.pelm_regression import get_regression
from app.pelm.pelm_governance import repair_governance
from app.pelm.pelm_report import (
    generate_html_report,
    generate_markdown_report,
)

# ------------------------------------------------------------
# FastAPI App
# ------------------------------------------------------------
app = FastAPI(title="PELM Backend")

# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Root
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "PELM backend running"}


# ------------------------------------------------------------
# PELM Status
# ------------------------------------------------------------
@app.get("/pelm/status")
def pelm_status():
    return get_pelm_status()


# ------------------------------------------------------------
# Run PELM
# ------------------------------------------------------------
@app.get("/pelm/run")
def pelm_run():
    return run_pelm()


# ------------------------------------------------------------
# Trend
# ------------------------------------------------------------
@app.get("/pelm/trend")
def pelm_trend():
    return get_pelm_trend()


# ------------------------------------------------------------
# Snapshots
# ------------------------------------------------------------
@app.get("/pelm/snapshots/list")
def pelm_snapshot_list():
    return list_snapshots()


@app.get("/pelm/snapshots/get/{name}")
def pelm_snapshot_get(name: str):
    return get_snapshot(name)


@app.get("/pelm/snapshots/diff")
def pelm_snapshot_diff(left: str, right: str):
    return diff_snapshots(left, right)


# ------------------------------------------------------------
# Regression
# ------------------------------------------------------------
@app.get("/pelm/regression")
def pelm_regression():
    return get_regression()


# ------------------------------------------------------------
# Governance Repair
# ------------------------------------------------------------
@app.post("/pelm/governance/repair")
def pelm_governance_repair():
    return repair_governance()


# ------------------------------------------------------------
# Reports
# ------------------------------------------------------------
@app.get("/pelm/report/html")
def pelm_report_html():
    return generate_html_report()


@app.get("/pelm/report/markdown")
def pelm_report_markdown():
    return generate_markdown_report()
