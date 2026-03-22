#!/usr/bin/env python3
import json
import os
from datetime import datetime

OUTPUT_DIR = "docs/doctor"
HISTORY_FILE = f"{OUTPUT_DIR}/history.json"
INDEX_HTML = f"{OUTPUT_DIR}/index.html"
RESULTS_FILE = "runtime/doctor_results.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_html(history, results):
    html = []
    html.append("<html><head><title>Doctor Dashboard</title>")
    html.append("<style>")
    html.append("body { font-family: Arial; padding: 20px; }")
    html.append(".ok { color: green; }")
    html.append(".fail { color: red; }")
    html.append(".error { color: orange; }")
    html.append("</style></head><body>")
    html.append("<h1>🩺 Doctor Suite Dashboard</h1>")

    # Current results
    html.append("<h2>Current Status</h2>")
    for r in results:
        status = r["status"]
        color = "ok" if status == "ok" else ("fail" if status == "fail" else "error")
        html.append(f"<p class='{color}'><b>{r['name']}</b>: {status.upper()}</p>")

    # History
    html.append("<h2>History</h2><ul>")
    for entry in reversed(history):
        status = "OK" if entry["status"] == "ok" else "FAIL"
        color = "ok" if entry["status"] == "ok" else "fail"
        html.append(f"<li class='{color}'>{entry['timestamp']}: {status}</li>")
    html.append("</ul>")

    html.append("</body></html>")
    return "\n".join(html)

def main():
    if not os.path.exists(RESULTS_FILE):
        print("[!] No doctor results found. Run doctor suite first.")
        return

    with open(RESULTS_FILE, "r") as f:
        results = json.load(f)

    # Determine overall status
    overall_status = "ok"
    for r in results:
        if r["status"] != "ok":
            overall_status = "fail"
            break

    # Load history
    history = load_history()

    # Append new entry
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "status": overall_status,
        "results": results
    })

    save_history(history)

    # Generate HTML
    html = generate_html(history, results)
    with open(INDEX_HTML, "w") as f:
        f.write(html)

    print("[+] Doctor dashboard updated.")

if __name__ == "__main__":
    main()
