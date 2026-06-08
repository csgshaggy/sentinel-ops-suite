// /src/pages/AdminAuditLogs.jsx
// ============================================================
// SentinelOps — Admin Audit Logs (Unified + Neon‑Glassy)
// - RBAC protected (admin only)
// - Uses unified apiClient.js
// - Uses unified AuthContext
// - Matches AdminPanel.css theme
// ============================================================

import React, { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { useNavigate } from "react-router-dom";
import client from "../api/apiClient.js";
import { toast } from "../components/ToastManager.jsx";
import "./AdminPanel.css"; // unified admin theme

export default function AdminAuditLogs() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [logs, setLogs] = useState([]);
  const [loadingLogs, setLoadingLogs] = useState(true);

  // ------------------------------------------------------------
  // RBAC: Only admins may enter
  // ------------------------------------------------------------
  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/login", { replace: true });
      } else if (user.role !== "admin") {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [user, loading, navigate]);

  // ------------------------------------------------------------
  // Load audit logs
  // ------------------------------------------------------------
  async function loadLogs() {
    setLoadingLogs(true);

    const res = await client.get("/admin/audit-logs");

    setLoadingLogs(false);

    if (!res.ok) {
      toast.error("Failed to load audit logs.");
      return;
    }

    setLogs(res.data || []);
  }

  useEffect(() => {
    if (user?.role === "admin") {
      loadLogs();
    }
  }, [user]);

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  if (loading || !user || user.role !== "admin") {
    return <div className="admin-panel">Loading...</div>;
  }

  return (
    <div className="admin-panel">
      <h1 className="admin-title">Audit Logs</h1>

      <div className="admin-table-wrapper">
        {loadingLogs ? (
          <div className="admin-empty">Loading logs...</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Action</th>
                <th>IP</th>
                <th>Timestamp</th>
              </tr>
            </thead>

            <tbody>
              {logs.length === 0 ? (
                <tr>
                  <td colSpan="5" className="admin-empty">
                    No audit logs found.
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id}>
                    <td>{log.id}</td>
                    <td>{log.username || "Unknown"}</td>
                    <td>{log.action}</td>
                    <td>{log.ip_address || "—"}</td>
                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
