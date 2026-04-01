# tools/security/idrim/collectors/iam_collector.py

class IAMCollector:
    """
    Collects IAM user/account metadata.
    This is intentionally generic so it can be backed by:
    - Local JSON datasets
    - LDAP / Active Directory queries
    - Database tables
    - API calls
    - Mock data for testing

    The output MUST be deterministic and follow this structure:
    {
        "username": {
            "roles": [...],
            "groups": [...],
            "flags": {
                "disabled": bool,
                "dormant": bool,
                "locked": bool
            }
        },
        ...
    }
    """

    def __init__(self, data_source=None):
        """
        Optional data_source allows injection for testing or custom backends.
        """
        self.data_source = data_source

    def collect(self):
        """
        Returns IAM user state.
        Replace the mock block with real data collection logic.
        """
        if self.data_source:
            return self.data_source()

        # --- MOCK DATA (safe default structure) ---
        # This ensures the module runs end-to-end even before integration.
        return {
            "alice": {
                "roles": ["user"],
                "groups": ["engineering"],
                "flags": {
                    "disabled": False,
                    "dormant": False,
                    "locked": False
                }
            },
            "bob": {
                "roles": ["admin"],
                "groups": ["security"],
                "flags": {
                    "disabled": False,
                    "dormant": False,
                    "locked": False
                }
            },
            "charlie": {
                "roles": ["user", "analyst"],
                "groups": ["operations"],
                "flags": {
                    "disabled": False,
                    "dormant": True,
                    "locked": False
                }
            }
        }
