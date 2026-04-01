# tools/security/idrim/analyzers/privilege_delta.py

class PrivilegeDelta:
    """
    Computes fine-grained deltas between baseline and current IAM state.

    Output format for each delta:
    {
        "type": "role_change" | "group_change" | "privilege_drift",
        "user": "username",
        "before": {...},
        "after": {...},
        "delta": {
            "added_roles": [...],
            "removed_roles": [...],
            "added_groups": [...],
            "removed_groups": [...],
            "privilege_gain": bool,
            "privilege_loss": bool
        }
    }
    """

    def compute_deltas(self, baseline, current):
        """
        Entry point for computing all deltas.
        Returns a list of delta objects.
        """
        deltas = []

        baseline_users = baseline.get("users", {})
        current_users = current.get("users", {})

        for user, current_info in current_users.items():
            baseline_info = baseline_users.get(user, {
                "roles": [],
                "groups": [],
                "flags": {}
            })

            delta = self._compute_user_delta(user, baseline_info, current_info)
            if delta:
                deltas.append(delta)

        return deltas

    def _compute_user_delta(self, user, before, after):
        """
        Computes role/group deltas for a single user.
        Returns None if no drift detected.
        """
        before_roles = set(before.get("roles", []))
        after_roles = set(after.get("roles", []))

        before_groups = set(before.get("groups", []))
        after_groups = set(after.get("groups", []))

        added_roles = sorted(list(after_roles - before_roles))
        removed_roles = sorted(list(before_roles - after_roles))

        added_groups = sorted(list(after_groups - before_groups))
        removed_groups = sorted(list(before_groups - after_groups))

        # No drift → return None
        if not (added_roles or removed_roles or added_groups or removed_groups):
            return None

        # Privilege gain/loss flags
        privilege_gain = bool(added_roles or added_groups)
        privilege_loss = bool(removed_roles or removed_groups)

        return {
            "type": self._classify_delta(added_roles, removed_roles, added_groups, removed_groups),
            "user": user,
            "before": before,
            "after": after,
            "delta": {
                "added_roles": added_roles,
                "removed_roles": removed_roles,
                "added_groups": added_groups,
                "removed_groups": removed_groups,
                "privilege_gain": privilege_gain,
                "privilege_loss": privilege_loss
            }
        }

    def _classify_delta(self, added_roles, removed_roles, added_groups, removed_groups):
        """
        Classifies the drift type based on what changed.
        """
        if added_roles or removed_roles:
            return "role_change"

        if added_groups or removed_groups:
            return "group_change"

        return "privilege_drift"
