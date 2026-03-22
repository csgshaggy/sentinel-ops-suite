#!/usr/bin/env python3
"""
Generate an HTML report from reports/superdoctor_report.json
for GitHub Pages publishing.
"""

import json
from pathlib import Path
from datetime import datetime

REPORT_JSON = Path("reports/superdoctor_report.json")
REPORT_HTML = Path("reports/superdoctor_report.html")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SuperDoctor Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #333;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        pre {{
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h1>SuperDoctor Report</h1>
    <div class="timestamp">Generated: {timestamp}</div>
    <pre>{content}</pre>
</body>
</html>
"""

def main():
    if not REPORT_JSON.exists():
        print("No JSON report found. Run SuperDoctor first.")
        return

    data = json.loads(REPORT_JSON.read_text())
    pretty = json.dumps(data, indent=4)

    html = TEMPLATE.format(
        timestamp=datetime.utcnow().isoformat(),
        content=pretty
    )

    REPORT_HTML.write_text(html)
    print(f"HTML report written to {REPORT_HTML}")

if __name__ == "__main__":
    main()
