# backend/app/reports/html/generate_report.py

from __future__ import annotations

from pathlib import Path

from backend.app.reports.html.anomaly_section import render_anomaly_section

OUTPUT_PATH = Path("report.html")


def generate_report() -> None:
    """
    Generate a full HTML report by assembling all sections.
    """
    html = f"""
    <html>
    <head>
        <title>SSRF Command Console — Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h2 {{
                color: #2c3e50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>SSRF Command Console — System Report</h1>

        {render_anomaly_section()}

    </body>
    </html>
    """

    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"[OK] HTML report generated at: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_report()
