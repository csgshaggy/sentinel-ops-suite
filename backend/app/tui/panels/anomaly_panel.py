# app/tui/panels/anomaly_panel.py

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from app.anomaly_engine import load_anomaly_history


def render_anomaly_panel() -> None:
    """
    Render a TUI panel showing recent anomalies.
    """
    console = Console()
    history = load_anomaly_history()

    table = Table(title="Anomaly History", show_lines=True)
    table.add_column("Timestamp", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Severity", style="red")
    table.add_column("Details", style="white")

    for record in history[-50:]:  # show last 50 anomalies
        table.add_row(
            record.get("timestamp", ""),
            record.get("type", ""),
            record.get("severity", ""),
            str(record.get("details", "")),
        )

    console.print(table)
