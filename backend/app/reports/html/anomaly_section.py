# app/reports/html/anomaly_section.py

from __future__ import annotations

from typing import Dict, List

from app.anomaly_engine import load_anomaly_history


def render_anomaly_section() -> str:
    """
    Render the anomaly section for the HTML report.
    """
    history: List[Dict] = load_anomaly_history()

    rows = []
    for record in history[-100:]:  # last 100 anomalies
        rows.append(
            f"""
            <tr>
                <td>{record.get("timestamp", "")}</td>
                <td>{record.get("type", "")}</td>
                <td>{record.get("severity", "")}</td>
                <td>{record.get("details", "")}</td>
            </tr>
            """
        )

    return f"""
    <section>
        <h2>Anomaly History</h2>
        <table border="1" cellspacing="0" cellpadding="6">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
    """
