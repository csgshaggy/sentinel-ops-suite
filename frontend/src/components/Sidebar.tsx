// File: /home/ubuntu/sentinel-ops-suite/frontend/src/components/Sidebar.tsx

import React from "react";
import { Link } from "react-router-dom";

// ✅ Corrected import — now using the real AuthContext
import { useAuth } from "../context/AuthContext";

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Sentinel Ops</h2>
      </div>

      <nav className="sidebar-nav">
        <ul>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>

          {user?.role === "admin" && (
            <li>
              <Link to="/admin">Admin Panel</Link>
            </li>
          )}
        </ul>
      </nav>
    </aside>
  );
}
