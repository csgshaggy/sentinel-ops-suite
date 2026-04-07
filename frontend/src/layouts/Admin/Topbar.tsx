// File: src/layouts/Admin/Topbar.tsx

import React from "react";
import { useAuth } from "../../context/AuthContext";

export default function Topbar() {
  const { user, logout } = useAuth();

  return (
    <header className="admin-topbar">
      <div className="topbar-left">
        <h1>Sentinel Ops — Admin</h1>
      </div>

      <div className="topbar-right">
        <span className="topbar-user">
          {user ? `Logged in as: ${user.username}` : "Not authenticated"}
        </span>

        <button className="logout-button" onClick={logout}>
          Logout
        </button>
      </div>
    </header>
  );
}
