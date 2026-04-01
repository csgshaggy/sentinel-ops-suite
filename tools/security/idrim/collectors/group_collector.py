# tools/security/idrim/collectors/group_collector.py

class GroupCollector:
    """
    Collects group membership information.

    Output MUST follow this deterministic structure:
    {
        "group_name": {
            "members": [...],
            "metadata": {
                "description": str,
                "nested": bool
            }
        },
        ...
    }

    This ensures compatibility with:
    - DriftAnalyzer
    - PrivilegeDelta
    - BaselineManager
    - Dashboard diff viewer
    """

    def __init__(self, data_source=None):
        """
        Optional data_source allows injection for:
        - LDAP / AD group queries
        - Database-backed group tables
        - API-driven IAM systems
        - Mock datasets for testing
        """
        self.data_source = data_source

    def collect(self):
        """
        Returns group → member mappings.
        Replace the mock block with real data collection logic.
        """
        if self.data_source:
            return self.data_source()

        # --- MOCK DATA (safe deterministic defaults) ---
        return {
            "engineering": {
                "members": ["alice"],
                "metadata": {
                    "description": "Engineering department",
                    "nested": False
                }
            },
            "security": {
                "members": ["bob"],
                "metadata": {
                    "description": "Security operations group",
                    "nested": False
                }
            },
            "operations": {
                "members": ["charlie"],
                "metadata": {
                    "description": "Operations team",
                    "nested": False
                }
            }
        }
