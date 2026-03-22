#!/usr/bin/env python3
import json
import os
from datetime import datetime
from scripts.drift_detector import walk_tree, load_baseline, compare

OUTPUT_DIR = "docs/drift"
HISTORY_FILE = f"{OUTPUT_DIR}/history.json"
INDEX_HTML = f"{OUTPUT_DIR}/index.html"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_html(history, drift):
    html = []
    html.append("<html><head><title>Drift Dashboard</title>")
    html.append("<style>")
    html.append("body { font-family: Arial; padding: 20px; }")
    html.append(".good { color: green; }")
    html.append(".bad { color: red; }")
    html.append(".warn { color: orange; }")
    html.append("</style></head><body>")
    html.append("<h1>📊 Structure Drift Dashboard</h1>")

    # Current drift
    html.append("<h2>Current Status</h2>")
    if not any(drift.values()):
        html.append("<p class='good'>✔️ No drift detected</p>")
    else:
        html.append("<p class='bad'>⚠️ Drift detected</p>")
        if drift["new_paths"]:
            html.append("<h3>New Paths</h3><ul>")
            for p in drift["new_paths"]:
                html.append(f"<li class='good'>+ {p}</li>")
            html.append("</ul>")
        if drift["missing_paths"]:
            html.append("<h3>Missing Paths</h3><ul>")
            for p in drift["missing_paths"]:
                html.append(f"<li class='bad'>- {p}</li>")
            html.append("</ul>")
        if drift["modified_files"]:
            html.append("<h3>Modified Files</h3><ul>")
            for p in drift["modified_files"]:
                html.append(f"<li class='warn'>* {p}</li>")
            html.append("</ul>")

    # History
    html.append("<h2>History</h2><ul>")
    for entry in reversed(history):
        status = "No drift" if not entry["drift"] else "Drift detected"
        color = "good" if not entry["drift"] else "bad"
        html.append(f"<li class='{color}'>{entry['timestamp']}: {status}</li>")
    html.append("</ul>")

    html.append("</body></html>")
    return "\n".join(html)

def main():
    current = walk_tree()
    baseline = load_baseline()

    if baseline is None:
        print("[!] No baseline found. Dashboard cannot be generated.")
        return

    drift = compare(baseline, current)

    # Load history
    history = load_history()

    # Append new entry
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "drift": drift
    })

    save_history(history)

    # Generate HTML
    html = generate_html(history, drift)
    with open(INDEX_HTML, "w") as f:
        f.write(html)

    print("[+] Drift dashboard updated.")

if __name__ == "__main__":
    main()
