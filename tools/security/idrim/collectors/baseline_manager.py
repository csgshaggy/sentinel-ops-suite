# tools/security/idrim/baselines/baseline_manager.py

import json
import os
from datetime import datetime


class BaselineManager:
    """
    Manages IAM baseline snapshots for IDRIM.

    Responsibilities:
    - Load baseline from disk
    - Save new baseline snapshots
    - Ensure deterministic structure
    - Provide timestamped baseline metadata

    Baseline file format:
    {
        "timestamp": "...",
        "data": {
            "users": {...},
            "roles": {...},
            "groups": {...}
        }
    }
    """

    def __init__(self, baseline_path="idrim_baseline.json"):
        """
        baseline_path can be overridden for:
        - Testing
        - Multi-environment setups
        - CI pipelines
        """
        self.baseline_path = baseline_path

    def load_baseline(self):
        """
        Loads the IAM baseline from disk.
        Returns a deterministic structure.
        If no baseline exists, returns an empty baseline.
        """
        if not os.path.exists(self.baseline_path):
            return {
                "timestamp": None,
                "data": {
                    "users": {},
                    "roles": {},
                    "groups": {}
                }
            }

        try:
            with open(self.baseline_path, "r") as f:
                return json.load(f)
        except Exception:
            # Fail-safe: return empty baseline if corrupted
            return {
                "timestamp": None,
                "data": {
                    "users": {},
                    "roles": {},
                    "groups": {}
                }
            }

    def save_baseline(self, current_state):
        """
        Saves a new IAM baseline snapshot.
        current_state must follow the deterministic structure produced by collectors.
        """
        baseline = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": current_state
        }

        with open(self.baseline_path, "w") as f:
            json.dump(baseline, f, indent=2)

        return baseline

    def baseline_exists(self):
        """
        Returns True if a baseline file exists.
        """
        return os.path.exists(self.baseline_path)
