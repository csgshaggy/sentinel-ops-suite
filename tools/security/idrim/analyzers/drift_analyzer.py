# tools/security/idrim/analyzers/drift_analyzer.py

from datetime import datetime
from .privilege_delta import PrivilegeDelta


class DriftAnalyzer:
    """
    Computes IAM drift between baseline and current state.

    Responsibilities:
    - Detect role changes
    - Detect group membership changes
    - Detect privilege accumulation
    - Detect dormant → privileged transitions
    - Produce structured drift events
    - Provide diff output for dashboard visualization
    """

    def __init__(self):
        self.delta_engine = PrivilegeDelta()

    def analyze(self, baseline, current):
        """
        Main drift detection entrypoint.
        Returns a list of drift events.
        """
        baseline_data = baseline.get("data", {})
        current_data = current

        events = []

        # Compute deltas using the PrivilegeDelta engine
        deltas = self.delta_engine.compute_deltas(
            baseline=baseline_data,
            current=current_data
        )

        # Convert deltas into drift events
        for delta in deltas:
            events.append(self._build_event(delta))

        return events

    def compute_diff(self, baseline, current):
        """
        Returns a structured diff object for dashboard rendering.
        Does NOT emit events.
        """
        baseline_data = baseline.get("data", {})
        current_data = current

        return self.delta_engine.compute_deltas(
            baseline=baseline_data,
            current=current_data
        )

    def _build_event(self, delta):
        """
        Converts a delta object into a standardized drift event.
        """
        return {
            "type": delta.get("type"),
            "user": delta.get("user"),
            "before": delta.get("before"),
            "after": delta.get("after"),
            "delta": delta.get("delta"),
            "severity": self._compute_severity(delta),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _compute_severity(self, delta):
        """
        Assigns severity based on drift type and magnitude.
        """
        drift_type = delta.get("type")
        change = delta.get("delta", {})

        # High severity: privilege escalation, admin role gain
        if drift_type == "role_change":
            if "admin" in change.get("added_roles", []):
                return "high"

        # Medium severity: new roles, new groups
        if drift_type in ("role_change", "group_change"):
            if change.get("added_roles") or change.get("added_groups"):
                return "medium"

        # Low severity: removals or minor changes
        return "low"
