// frontend/src/layouts/Admin/Topbar.tsx
// SentinelOps — Session‑Aware Topbar

import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import "./Topbar.css";

export default function Topbar() {
  const { user } = useContext(AuthContext);

  return (
    <header className="topbar">
      <h1 className="topbar-title">SentinelOps</h1>

      <div className="topbar-user">
        {user && (
          <>
            <span className="topbar-email">{user.email}</span>
          </>
        )}
      </div>
    </header>
  );
}
