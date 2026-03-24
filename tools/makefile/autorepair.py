from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Dict, Any


CANONICAL = Path(__file__).parent / "Makefile.canonical"
TARGET = Path(__file__).parents[2] / "Makefile"
BACKUP_DIR = Path(__file__).parents[2] / "backups"


def autorepair(dry_run: bool = False) -> Dict[str, Any]:
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"Makefile.backup.{timestamp}"

    if not dry_run:
        shutil.copy2(TARGET, backup_path)
        shutil.copy2(CANONICAL, TARGET)

    return {
        "repaired": not dry_run,
        "backup_path": str(backup_path),
        "canonical_used": str(CANONICAL),
        "target": str(TARGET),
    }
