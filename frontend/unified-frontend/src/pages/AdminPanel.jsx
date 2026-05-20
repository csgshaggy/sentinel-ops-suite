// /src/pages/AdminPanel.jsx

import "./AdminPanel.css";

export default function AdminPanel() {
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
