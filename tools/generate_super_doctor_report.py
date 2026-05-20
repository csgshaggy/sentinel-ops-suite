import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path.home() / "ssrf-command-console"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
LOG_PATH = RUNTIME_DIR / "super_doctor_report.json"
HISTORY_DIR = RUNTIME_DIR / "history"
OUTPUT_LATEST = PROJECT_ROOT / "docs" / "super_doctor_latest.html"
OUTPUT_INDEX = PROJECT_ROOT / "docs" / "index.html"

SEVERITY_ORDER = {"FAIL": 0, "WARN": 1, "INFO": 2}


def load_report(path):
    if not path.exists():
        print(f"[FAIL] Report not found: {path}")
        return []
    with path.open() as f:
        return json.load(f)


def load_latest():
    return load_report(LOG_PATH)


def load_history():
    if not HISTORY_DIR.exists():
        return []
    files = sorted(HISTORY_DIR.glob("super_doctor_*.json"))
    history = []
    for f in files:
        entries = load_report(f)
        counts = Counter(e["severity"] for e in entries)
        ts_str = f.stem.replace("super_doctor_", "")
        history.append(
            {
                "timestamp": ts_str,
                "counts": {
                    "FAIL": counts.get("FAIL", 0),
                    "WARN": counts.get("WARN", 0),
                    "INFO": counts.get("INFO", 0),
                },
            }
        )
    return history


def sort_entries(entries):
    return sorted(
        entries,
        key=lambda e: (SEVERITY_ORDER.get(e["severity"], 99), e["message"]),
    )


def generate_html(entries, history):
    counts = Counter(e["severity"] for e in entries)
    timestamp = datetime.now(timezone.utc).isoformat()

    sorted_entries = sort_entries(entries)

    rows = "\n".join(
        f"<tr><td><span class='badge {e['severity']}'>{e['severity']}</span></td><td>{e['message']}</td></tr>"
        for e in sorted_entries
    )

    history_rows = "\n".join(
        f"<tr><td>{h['timestamp']}</td>"
        f"<td class='FAIL'>{h['counts']['FAIL']}</td>"
        f"<td class='WARN'>{h['counts']['WARN']}</td>"
        f"<td class='INFO'>{h['counts']['INFO']}</td></tr>"
        for h in history
    )

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Super Doctor Report</title>
  <style>
    body {{ font-family: sans-serif; margin: 20px; }}
    h1 {{ margin-bottom: 5px; }}
    .summary p {{ margin: 4px 0; }}
    .badge {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.85em;
      color: #fff;
    }}
    .FAIL {{ background: #d32f2f; }}
    .WARN {{ background: #f9a825; }}
    .INFO {{ background: #388e3c; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 10px; }}
    th {{ background: #f0f0f0; }}
    .trend-table {{ margin-top: 30px; }}
  </style>
</head>
<body>
  <h1>Super Doctor Report</h1>
  <p>Generated: {timestamp}</p>

  <div class="summary">
    <p><span class="badge FAIL">FAIL: {counts.get("FAIL", 0)}</span></p>
    <p><span class="badge WARN">WARN: {counts.get("WARN", 0)}</span></p>
    <p><span class="badge INFO">INFO: {counts.get("INFO", 0)}</span></p>
  </div>

  <h2>Trend (History)</h2>
  <table class="trend-table">
    <thead>
      <tr><th>Run Timestamp</th><th>FAIL</th><th>WARN</th><th>INFO</th></tr>
    </thead>
    <tbody>
      {history_rows}
    </tbody>
  </table>

  <h2>Detailed Entries</h2>
  <table>
    <thead>
      <tr><th>Severity</th><th>Message</th></tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
"""


def generate_index(history):
    links = []
    for h in history:
        ts = h["timestamp"]
        links.append(f"<li><a href='super_doctor_{ts}.html'>{ts}</a></li>")

    links_html = "\n".join(links) if links else "<li>No reports yet.</li>"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Super Doctor Reports Index</title>
  <style>
    body {{ font-family: sans-serif; margin: 20px; }}
  </style>
</head>
<body>
  <h1>Super Doctor Reports</h1>
  <p><a href="super_doctor_latest.html">Latest Report</a></p>
  <h2>Historical Reports</h2>
  <ul>
    {links_html}
  </ul>
</body>
</html>
"""


def main():
    entries = load_latest()
    if not entries:
        return

    history = load_history()

    html = generate_html(entries, history)
    OUTPUT_LATEST.write_text(html, encoding="utf-8")
    print(f"[OK] Latest report written to: {OUTPUT_LATEST}")

    # per-run HTML snapshots (reuse latest content for now)
    for h in history:
        ts = h["timestamp"]
        per_run_path = PROJECT_ROOT / "docs" / f"super_doctor_{ts}.html"
        per_run_path.write_text(html, encoding="utf-8")

    index_html = generate_index(history)
    OUTPUT_INDEX.write_text(index_html, encoding="utf-8")
    print(f"[OK] Index written to: {OUTPUT_INDEX}")


if __name__ == "__main__":
    main()
