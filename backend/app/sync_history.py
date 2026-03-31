from pathlib import Path

LOG_PATH = Path("sync.log")


def parse_sync_history(limit: int = 20):
    """
    Parses sync.log into structured sync history blocks.

    Each block begins with:
        "=== One‑Command Sync ==="
    and ends when the next block begins or the file ends.
    """

    if not LOG_PATH.exists():
        return []

    lines = LOG_PATH.read_text().splitlines()
    blocks = []
    current_block = []

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
    parsed_entries = []
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
