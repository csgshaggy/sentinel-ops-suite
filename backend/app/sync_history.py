import re
from pathlib import Path

LOG_PATH = Path("sync.log")

def parse_sync_history(limit: int = 20):
    if not LOG_PATH.exists():
        return []

    content = LOG_PATH.read_text().splitlines()
    entries = []
    current = []

    for line in content:
        if "=== One‑Command Sync ===" in line:
            if current:
                entries.append(current)
                current = []
        current.append(line)

    if current:
        entries.append(current)

    # Convert to structured objects
    parsed = []
    for block in entries[-limit:]:
        parsed.append({
            "raw": block,
            "start": next((l for l in block if "One‑Command Sync" in l), None),
            "end": next((l for l in block if "Sync Complete" in l), None),
            "commit": next((l for l in block if "sync:" in l), None),
        })

    return parsed
