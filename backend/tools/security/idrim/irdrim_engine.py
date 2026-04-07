# backend/tools/security/idrim/idrim_engine.py

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List

from .idrim_models import (
    IDRIMBaseline,
    IDRIMSnapshot,
    IDRIMDriftEvent,
    IDRIMDriftSection,
    IDRIMDriftResult,
    IDRIMAnalysisResult,
)


class IDRIMEngine:
    """
    Core IDRIM engine: baseline management, drift detection, scoring, analysis.
    """

    def __init__(self, storage_path: str = "data/idrim"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.baseline_file = self.storage_path / "baseline.json"

    # ---------------- Baseline ----------------

    def baseline_exists(self) -> bool:
        return self.baseline_file.exists()

    def load_baseline(self) -> IDRIMBaseline:
        if not self.baseline_exists():
            return IDRIMBaseline()
        data = json.loads(self.baseline_file.read_text())
        return IDRIMBaseline(**data)

    def save_baseline(self, snapshot: IDRIMSnapshot) -> IDRIMBaseline:
        baseline = IDRIMBaseline(**snapshot.dict())
        self.baseline_file.write_text(json.dumps(baseline.dict(), indent=2))
        return baseline

    def rebuild_baseline(self, snapshot: IDRIMSnapshot) -> IDRIMBaseline:
        return self.save_baseline(snapshot)

    # ---------------- Drift ----------------

    @staticmethod
    def _diff_dict(a: Dict[str, Any], b: Dict[str, Any]) -> IDRIMDriftSection:
        added = {k: b[k] for k in b if k not in a}
        removed = {k: a[k] for k in a if k not in b}
        changed = {
            k: {"before": a[k], "after": b[k]}
            for k in a
            if k in b and a[k] != b[k]
        }
        return IDRIMDriftSection(added=added, removed=removed, changed=changed)

    def detect_drift(self, snapshot: IDRIMSnapshot) -> IDRIMDriftResult:
        baseline = self.load_baseline()
        return IDRIMDriftResult(
            roles=self._diff_dict(baseline.roles, snapshot.roles),
            permissions=self._diff_dict(baseline.permissions, snapshot.permissions),
            users=self._diff_dict(baseline.users, snapshot.users),
        )

    # ---------------- Scoring ----------------

    @staticmethod
    def _score_from_drift(drift: IDRIMDriftResult) -> int:
        def count_changes(section: IDRIMDriftSection) -> int:
            return (
                len(section.added)
                + len(section.removed)
                + len(section.changed)
            )

        total = (
            count_changes(drift.roles)
            + count_changes(drift.permissions)
            + count_changes(drift.users)
        )
        return max(0, 100 - total * 2)

    # ---------------- Analysis ----------------

    @staticmethod
    def _flatten_drift(drift: IDRIMDriftResult) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []

        def add_events(section_name: str, section: IDRIMDriftSection):
            for k, v in section.added.items():
                events.append(
                    {"event_type": f"{section_name}_added", "key": k, "details": v}
                )
            for k, v in section.removed.items():
                events.append(
                    {"event_type": f"{section_name}_removed", "key": k, "details": v}
                )
            for k, v in section.changed.items():
                events.append(
                    {"event_type": f"{section_name}_changed", "key": k, "details": v}
                )

        add_events("role", drift.roles)
        add_events("permission", drift.permissions)
        add_events("user", drift.users)
        return events

    def analyze(self, snapshot: IDRIMSnapshot) -> IDRIMAnalysisResult:
        drift = self.detect_drift(snapshot)
        score = self._score_from_drift(drift)
        summary = f"Integrity score {score}. Drift detected across roles/permissions/users."

        return IDRIMAnalysisResult(
            timestamp=datetime.utcnow().isoformat() + "Z",
            integrity_score=score,
            summary=summary,
            drift_events=self._flatten_drift(drift),
            roles=snapshot.roles,
            permissions=snapshot.permissions,
            users=snapshot.users,
        )
