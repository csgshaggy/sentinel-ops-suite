# backend/app/sync_history.py

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

LOG_PATH = Path("sync.log")


def parse_sync_history(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Parse sync.log into structured sync history blocks.

    Each block begins with:
        "=== One‑Command Sync ==="
    and ends when the next block begins or the file ends.

    Returns a list of structured entries:
        {
            "raw": [...],
            "start": "...",
            "end": "...",
            "commit": "..."
        }
    """

    if not LOG_PATH.exists():
        return []

    lines = LOG_PATH.read_text().splitlines()
    blocks: List[List[str]] = []
    current_block: List[str] = []

    for line in lines:
        # Start of a new sync block
        if "=== One‑Command Sync ===" in line:
            if current_block:
                blocks.append(current_block)
                current_block = []
        current_block.append(line)

    # Append final block if present
    if current_block:
        blocks.append(current_block)

    # Convert raw blocks into structured objects
    parsed_entries: List[Dict[str, Any]] = []
    for block in blocks[-limit:]:
        parsed_entries.append(
            {
                "raw": block,
                "start": next(
                    (line for line in block if "One‑Command Sync" in line), None
                ),
                "end": next((line for line in block if "Sync Complete" in line), None),
                "commit": next((line for line in block if "sync:" in line), None),
            }
        )

    return parsed_entries


def load_sync_history(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Canonical wrapper used by anomaly_engine and other modules.

    This ensures a stable API even if the underlying parser changes.
    """
    return parse_sync_history(limit=limit)
