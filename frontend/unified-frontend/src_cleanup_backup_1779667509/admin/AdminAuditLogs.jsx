// /src/pages/AdminAuditLogs.jsx

import { Navigate } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthContext.jsx";
import "./AdminAuditLogs.css";

export default function AdminAuditLogs() {
  const { user, loading } = useAuth();

  // Avoid flicker during session restore
  if (loading) return null;

  // No session → redirect to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // RBAC: Only admins allowed
  if (user.role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="admin-audit-panel">
      <h2 className="text-glow">Audit Logs</h2>

      <div className="admin-audit-grid">
        <div className="admin-audit-card">
          <h3>System Activity</h3>
          <p>Review authentication events, access attempts, and system actions.</p>
        </div>

        <div className="admin-audit-card">
          <h3>Security Events</h3>
          <p>Monitor alerts, escalations, and policy violations.</p>
        </div>

        <div className="admin-audit-card">
          <h3>Change History</h3>
          <p>Track configuration changes, role updates, and administrative actions.</p>
        </div>
      </div>
    </div>
  );
}
