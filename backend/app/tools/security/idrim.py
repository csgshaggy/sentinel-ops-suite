# tools/security/idrim.py

from pathlib import Path
import json
from datetime import datetime


class IDRIMService:
    def __init__(self, storage_path="data/idrim"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.baseline_file = self.storage_path / "baseline.json"

    # -----------------------------
    # Baseline
    # -----------------------------
    def baseline_exists(self) -> bool:
        return self.baseline_file.exists()

    def load_baseline(self) -> dict:
        if not self.baseline_exists():
            return {"roles": {}, "permissions": {}, "users": {}}
        return json.loads(self.baseline_file.read_text())

    def save_baseline(self, data: dict) -> dict:
        self.baseline_file.write_text(json.dumps(data, indent=2))
        return data

    def rebuild_baseline(self, snapshot: dict) -> dict:
        return self.save_baseline(snapshot)

    # -----------------------------
    # Drift & Analysis
    # -----------------------------
    @staticmethod
    def _diff_dict(a, b):
        added = {k: b[k] for k in b if k not in a}
        removed = {k: a[k] for k in a if k not in b}
        changed = {
            k: {"before": a[k], "after": b[k]}
            for k in a
            if k in b and a[k] != b[k]
        }
        return {"added": added, "removed": removed, "changed": changed}

    def detect_drift(self, snapshot: dict) -> dict:
        baseline = self.load_baseline()
        return {
            "roles": self._diff_dict(baseline.get("roles", {}), snapshot.get("roles", {})),
            "permissions": self._diff_dict(
                baseline.get("permissions", {}), snapshot.get("permissions", {})
            ),
            "users": self._diff_dict(baseline.get("users", {}), snapshot.get("users", {})),
        }

    def _score_from_drift(self, drift: dict) -> int:
        def count_changes(section):
            return (
                len(section["added"])
                + len(section["removed"])
                + len(section["changed"])
            )

        total = (
            count_changes(drift["roles"])
            + count_changes(drift["permissions"])
            + count_changes(drift["users"])
        )
        score = max(0, 100 - total * 2)
        return score

    def analyze(self, snapshot: dict) -> dict:
        drift = self.detect_drift(snapshot)
        score = self._score_from_drift(drift)
        summary = f"Integrity score {score}. Drift detected across roles/permissions/users."

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "integrity_score": score,
            "summary": summary,
            "drift_events": self._flatten_drift(drift),
            "roles": snapshot.get("roles", {}),
            "permissions": snapshot.get("permissions", {}),
            "users": snapshot.get("users", {}),
        }

    @staticmethod
    def _flatten_drift(drift: dict):
        events = []

        def add_events(section_name, section):
            for k, v in section["added"].items():
                events.append(
                    {
                        "event_type": f"{section_name}_added",
                        "key": k,
                        "details": v,
                    }
                )
            for k, v in section["removed"].items():
                events.append(
                    {
                        "event_type": f"{section_name}_removed",
                        "key": k,
                        "details": v,
                    }
                )
            for k, v in section["changed"].items():
                events.append(
                    {
                        "event_type": f"{section_name}_changed",
                        "key": k,
                        "details": v,
                    }
                )

        add_events("role", drift["roles"])
        add_events("permission", drift["permissions"])
        add_events("user", drift["users"])
        return events


class IDRIMTasks:
    def __init__(self, storage_path="data/idrim"):
        self.service = IDRIMService(storage_path=storage_path)

    def analysis_task(self, snapshot: dict):
        _ = self.service.analyze(snapshot)
