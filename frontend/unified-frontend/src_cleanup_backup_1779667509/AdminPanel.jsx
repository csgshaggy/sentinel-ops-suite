// /src/pages/AdminPanel.jsx

import { Navigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import "./AdminPanel.css";

export default function AdminPanel() {
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
    <div className="admin-panel">
      <h2 className="text-glow">Admin Panel</h2>

      <div className="admin-grid">
        <div className="admin-card">
          <h3>System Controls</h3>
          <p>Administrative tools and elevated controls for system management.</p>
        </div>

        <div className="admin-card">
          <h3>User Management</h3>
          <p>Manage user roles, permissions, and access levels.</p>
        </div>

        <div className="admin-card">
          <h3>Audit & Logs</h3>
          <p>Review system activity, security events, and audit trails.</p>
        </div>
      </div>
    </div>
  );
}
