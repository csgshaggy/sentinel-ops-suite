// /src/pages/AdminPanel.jsx
// ============================================================
// SentinelOps — Admin Panel (Unified Landing Page)
// - RBAC protected
// - Neon‑glassy theme
// - Links to Users, Audit Logs, Preferences, Security
// ============================================================

import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import "./AdminPanel.css";

export default function AdminPanel() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  // ------------------------------------------------------------
  // RBAC: Only admins may enter
  // ------------------------------------------------------------
  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/login", { replace: true });
      } else if (!user.roles?.includes("admin")) {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [user, loading, navigate]);

  if (loading || !user) {
    return <div className="admin-panel">Loading admin panel...</div>;
  }

  return (
    <div className="admin-panel">
      <h1 className="admin-title">Admin Panel</h1>

      <div className="admin-table-wrapper">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Section</th>
              <th>Description</th>
              <th>Navigate</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Users</td>
              <td>Manage user accounts, roles, and access.</td>
              <td>
                <button
                  className="admin-btn"
                  onClick={() => navigate("/admin/users")}
                >
                  Open
                </button>
              </td>
            </tr>

            <tr>
              <td>Audit Logs</td>
              <td>Review system activity and security events.</td>
              <td>
                <button
                  className="admin-btn"
                  onClick={() => navigate("/admin/audit")}
                >
                  Open
                </button>
              </td>
            </tr>

            <tr>
              <td>Preferences</td>
              <td>System‑wide admin preferences and defaults.</td>
              <td>
                <button
                  className="admin-btn"
                  onClick={() => navigate("/admin/preferences")}
                >
                  Open
                </button>
              </td>
            </tr>

            <tr>
              <td>Security</td>
              <td>Security policies, MFA enforcement, and RBAC rules.</td>
              <td>
                <button
                  className="admin-btn"
                  onClick={() => navigate("/admin/security")}
                >
                  Open
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
