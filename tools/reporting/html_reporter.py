"""
HTML Report Generator for SuperDoctor
Location: tools/reporting/html_reporter.py

Generates a static HTML dashboard at:
    reports/superdoctor/index.html

Cross‑platform (Windows + Linux) and GitHub Pages‑safe.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from utils.paths import ensure_directory

# ------------------------------------------------------------
# HTML TEMPLATE
# ------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SuperDoctor Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 1100px;
            margin: 40px auto;
            background: white;
            padding: 20px 40px;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin-top: 0;
        }}
        .summary {{
            background: #eef3ff;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 30px;
        }}
        .summary strong {{
            display: inline-block;
            width: 160px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #fafafa;
            text-align: left;
        }}
        .status-ok {{ color: #2e8b57; font-weight: bold; }}
        .status-warn {{ color: #d4a017; font-weight: bold; }}
        .status-fail {{ color: #c0392b; font-weight: bold; }}
        .status-skip {{ color: #7f8c8d; font-weight: bold; }}
        .footer {{
            margin-top: 40px;
            font-size: 0.9em;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>SuperDoctor Report</h1>

    <div class="summary">
        <p><strong>Mode:</strong> {mode}</p>
        <p><strong>Health Score:</strong> {health_score}/100</p>
        <p><strong>Total Checks:</strong> {total_checks}</p>
        <p><strong>Passed:</strong> {passed}</p>
        <p><strong>Warnings:</strong> {warned}</p>
        <p><strong>Failed:</strong> {failed}</p>
        <p><strong>Skipped:</strong> {skipped}</p>
        <p><strong>Git SHA:</strong> {git_sha}</p>
        <p><strong>Branch:</strong> {branch}</p>
        <p><strong>Generated:</strong> {generated_at}</p>
    </div>

    <h2>Check Results</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Plugin</th>
            <th>Name</th>
            <th>Status</th>
            <th>Severity</th>
            <th>Details</th>
        </tr>
        {rows}
    </table>

    <div class="footer">
        SuperDoctor — Automated Environment & Project Health Console
    </div>
</div>
</body>
</html>
"""


# ------------------------------------------------------------
# HTML row builder
# ------------------------------------------------------------


def _build_row(result: Dict[str, Any]) -> str:
    status_class = f"status-{result['status']}"
    details = result.get("details") or ""
    details = details.replace("\n", "<br>")

    return f"""
    <tr>
        <td>{result["id"]}</td>
        <td>{result.get("plugin", "")}</td>
        <td>{result["name"]}</td>
        <td class="{status_class}">{result["status"].upper()}</td>
        <td>{result["severity"]}</td>
        <td>{details}</td>
    </tr>
    """


# ------------------------------------------------------------
# Main generator
# ------------------------------------------------------------


def generate_html_report(project_root: Path, payload: Dict[str, Any]) -> Path:
    """
    Generate a static HTML report at:
        reports/superdoctor/index.html
    """
    summary = payload["summary"]
    results = payload["results"]

    rows = "\n".join(_build_row(r) for r in results)

    html = HTML_TEMPLATE.format(
        mode=summary["mode"],
        health_score=summary["health_score"],
        total_checks=summary["total_checks"],
        passed=summary["passed"],
        warned=summary["warned"],
        failed=summary["failed"],
        skipped=summary["skipped"],
        git_sha=summary.get("git_sha") or "N/A",
        branch=summary.get("branch") or "N/A",
        generated_at=datetime.utcnow().isoformat() + "Z",
        rows=rows,
    )

    out_dir = project_root / "reports" / "superdoctor"
    ensure_directory(out_dir)

    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")

    return out_path
