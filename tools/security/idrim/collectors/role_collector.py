# tools/security/idrim/collectors/role_collector.py

class RoleCollector:
    """
    Collects role definitions and their associated permissions.

    Output MUST follow this deterministic structure:
    {
        "role_name": {
            "permissions": [...],
            "metadata": {
                "description": str,
                "system_role": bool
            }
        },
        ...
    }

    This structure ensures compatibility with:
    - DriftAnalyzer
    - PrivilegeDelta
    - BaselineManager
    - Dashboard diff viewer
    """

    def __init__(self, data_source=None):
        """
        Optional data_source allows injection for:
        - LDAP / AD role queries
        - Database-backed RBAC tables
        - API-driven IAM systems
        - Mock datasets for testing
        """
        self.data_source = data_source

    def collect(self):
        """
        Returns role → permission mappings.
        Replace the mock block with real data collection logic.
        """
        if self.data_source:
            return self.data_source()

        # --- MOCK DATA (safe deterministic defaults) ---
        return {
            "user": {
                "permissions": [
                    "read_profile",
                    "update_own_settings"
                ],
                "metadata": {
                    "description": "Standard user role",
                    "system_role": False
                }
            },
            "analyst": {
                "permissions": [
                    "read_logs",
                    "view_reports",
                    "query_metrics"
                ],
                "metadata": {
                    "description": "Operational analyst role",
                    "system_role": False
                }
            },
            "admin": {
                "permissions": [
                    "read_profile",
                    "update_own_settings",
                    "manage_users",
                    "modify_roles",
                    "access_security_panels"
                ],
                "metadata": {
                    "description": "Full administrative privileges",
                    "system_role": True
                }
            }
        }
