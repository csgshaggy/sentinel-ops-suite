#!/usr/bin/env python3
"""
Generate README badge markdown from the latest Super Doctor JSON report.

Reads:
  • runtime/super_doctor_report.json

Outputs to stdout:
  • Markdown badge block for README
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

PROJECT_ROOT = Path.home() / "ssrf-command-console"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
LATEST_JSON = RUNTIME_DIR / "super_doctor_report.json"

def load_latest():
    if not LATEST_JSON.exists():
        return []
    return json.loads(LATEST_JSON.read_text(encoding="utf-8"))

def extract_health_score(entries):
    for e in entries:
        if e["severity"] == "INFO" and "Project health score:" in e["message"]:
            try:
                part = e["message"].split("Project health score:")[1].strip()
                num = part.split("/")[0].strip()
                return int(num)
            except Exception:
                return None
    return None

def compute_color_for_score(score):
    if score is None:
        return "lightgrey"
    if score >= 90:
        return "2ea44f"  # green
    if score >= 70:
        return "f9a825"  # yellow
    return "d32f2f"      # red

def main():
    entries = load_latest()
    if not entries:
        print("<!-- No Super Doctor report found -->")
        return

    counts = Counter(e["severity"] for e in entries)
    score = extract_health_score(entries)

    fail = counts.get("FAIL", 0)
    warn = counts.get("WARN", 0)
    info = counts.get("INFO", 0)

    # Last run from file mtime
    mtime = datetime.fromtimestamp(LATEST_JSON.stat().st_mtime)
    last_run_str = mtime.strftime("%Y--%m--%d")  # double dash for URL safety

    score_color = compute_color_for_score(score)
    score_label = f"{score}/100" if score is not None else "N/A"

    print("## Super Doctor Status\n")
    print(f"![Health Score](https://img.shields.io/badge/health-{score_label.replace('/', '%2F')}-{score_color})")
    print(f"![Last Run](https://img.shields.io/badge/last_run-{last_run_str}-blue)")
    print(f"![Failures](https://img.shields.io/badge/fail-{fail}-d32f2f)")
    print(f"![Warnings](https://img.shields.io/badge/warn-{warn}-f9a825)")
    print(f"![Info](https://img.shields.io/badge/info-{info}-388e3c)")

if __name__ == "__main__":
    main()
