# tools/security/idrim/outputs/idrim_event.py

class IDRIMEvent:
    """
    Standardized event object for IAM Drift & Role Integrity Monitor (IDRIM).

    This ensures all drift events follow a strict, deterministic schema.

    Event structure:
    {
        "type": "role_change" | "group_change" | "privilege_drift" | "dormant_privilege_gain",
        "user": "username",
        "before": {...},
        "after": {...},
        "delta": {...},
        "severity": "low" | "medium" | "high",
        "timestamp": "ISO-8601"
    }
    """

    def __init__(self, type, user, before, after, delta, severity, timestamp):
        self.type = type
        self.user = user
        self.before = before
        self.after = after
        self.delta = delta
        self.severity = severity
        self.timestamp = timestamp

    def to_dict(self):
        """
        Returns the event as a deterministic dictionary.
        """
        return {
            "type": self.type,
            "user": self.user,
            "before": self.before,
            "after": self.after,
            "delta": self.delta,
            "severity": self.severity,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_delta(delta, severity, timestamp):
        """
        Factory method to build an IDRIMEvent from a delta object.
        """
        return IDRIMEvent(
            type=delta.get("type"),
            user=delta.get("user"),
            before=delta.get("before"),
            after=delta.get("after"),
            delta=delta.get("delta"),
            severity=severity,
            timestamp=timestamp
        )
