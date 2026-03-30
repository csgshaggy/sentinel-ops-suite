import React from "react";
import { Link } from "react-router-dom";

interface SidebarLayoutProps {
  children: React.ReactNode;
}

const SidebarLayout: React.FC<SidebarLayoutProps> = ({ children }) => {
  return (
    <div className="layout">
      <aside className="sidebar">
        <nav>
          <ul>
            <li>
              <Link to="/admin">Dashboard</Link>
            </li>
            <li>
              <Link to="/admin/users">Users</Link>
            </li>
            <li>
              <Link to="/admin/audit-logs">Audit Logs</Link>
            </li>
            <li>
              <Link to="/settings/mfa">MFA Settings</Link>
            </li>
          </ul>
        </nav>
      </aside>
      <main className="content">{children}</main>
    </div>
  );
};

export default SidebarLayout;
