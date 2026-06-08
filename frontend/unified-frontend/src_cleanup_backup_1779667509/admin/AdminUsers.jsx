// /src/pages/AdminUsers.jsx

import { Navigate } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthContext.jsx";
import "./AdminUsers.css";

export default function AdminUsers() {
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
    <div className="admin-users-panel">
      <h2 className="text-glow">User Management</h2>

      <div className="admin-users-grid">
        <div className="admin-users-card">
          <h3>Manage Users</h3>
          <p>View, edit, and manage user accounts and access levels.</p>
        </div>

        <div className="admin-users-card">
          <h3>Roles & Permissions</h3>
          <p>Assign roles, update privileges, and enforce RBAC policies.</p>
        </div>

        <div className="admin-users-card">
          <h3>Account Status</h3>
          <p>Monitor active, locked, or suspended accounts.</p>
        </div>
      </div>
    </div>
  );
}
