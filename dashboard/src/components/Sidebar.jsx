// =====================================================================
// SSRF Command Console — Sidebar Navigation
// Admin Console Navigation • Session Cookie Auth
// =====================================================================

import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="sidebar-title">Admin Console</h2>

      <ul className="sidebar-nav">

        {/* Dashboard */}
        <li>
          <Link to="/admin/dashboard">Dashboard</Link>
        </li>

        {/* User Management */}
        <li>
          <Link to="/admin/users">Users</Link>
        </li>
        <li>
          <Link to="/admin/users/create">Create User</Link>
        </li>

        {/* Audit Logs */}
        <li>
          <Link to="/admin/audit-logs">Audit Logs</Link>
        </li>

      </ul>
    </div>
  );
}
