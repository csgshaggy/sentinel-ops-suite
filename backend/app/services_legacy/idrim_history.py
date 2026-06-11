# app/services/idrim_history.py

import json
from pathlib import Path
from datetime import datetime


class IDRIMHistory:
    def __init__(self, path="data/idrim/history"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def _timestamp(self):
        return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    def store_snapshot(self, snapshot: dict):
        ts = self._timestamp()
        file = self.path / f"{ts}.json"
        file.write_text(json.dumps(snapshot, indent=2))
        return ts

    def list_snapshots(self):
        return sorted([p.stem for p in self.path.glob("*.json")])

    def load_snapshot(self, ts: str):
        file = self.path / f"{ts}.json"
        if not file.exists():
            return None
        return json.loads(file.read_text())

    def diff_chain(self, diff_func):
        snapshots = self.list_snapshots()
        chain = []

        for i in range(1, len(snapshots)):
            before = self.load_snapshot(snapshots[i - 1])
            after = self.load_snapshot(snapshots[i])
            diff = diff_func(before, after)
            chain.append(
                {
                    "from": snapshots[i - 1],
                    "to": snapshots[i],
                    "diff": diff,
                }
            )

        return chain
