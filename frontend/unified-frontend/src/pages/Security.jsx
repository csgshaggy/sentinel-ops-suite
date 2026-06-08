// /src/pages/Security.jsx
// ============================================================
// SentinelOps — Security Settings (Unified + Neon‑Glassy)
// - Shows MFA status
// - Allows enabling/disabling MFA
// - Uses unified MFASetup.jsx
// - Uses unified backend + AuthContext
// ============================================================

import { useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";
import client from "../api/apiClient.js";
import { toast } from "../components/ToastManager.jsx";
import MFASetup from "../features/auth/MFASetup.jsx";
import "./AdminPanel.css"; // neon‑glassy theme for cards + tables

export default function Security() {
  const { user, refreshUser } = useAuth();

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [showSetup, setShowSetup] = useState(false);

  if (!user) {
    return <div className="admin-panel">Loading...</div>;
  }

  // ------------------------------------------------------------
  // Disable MFA
  // ------------------------------------------------------------
  async function handleDisable(e) {
    e.preventDefault();
    setLoading(true);

    const res = await client.post("/mfa/disable", { code });

    setLoading(false);

    if (!res.ok) {
      toast.error("Invalid MFA code.");
      return;
    }

    toast.success("MFA disabled.");
    setCode("");
    await refreshUser();
  }

  return (
    <div className="admin-panel">
      <h1 className="admin-title">Security Settings</h1>

      {/* ============================================================
          MFA ENABLED
          ============================================================ */}
      {user.mfa_enabled && (
        <div className="admin-table-wrapper" style={{ marginBottom: "20px" }}>
          <h2 className="admin-form-title">MFA Status</h2>
          <p>
            MFA is currently <strong>enabled</strong> on your account.
          </p>

          <form onSubmit={handleDisable} className="admin-form" style={{ marginTop: "12px" }}>
            <div className="admin-form-grid">
              <input
                type="text"
                inputMode="numeric"
                maxLength={6}
                placeholder="Enter 6‑digit code to disable"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                required
              />
            </div>

            <div className="admin-actions" style={{ marginTop: "12px" }}>
              <button type="submit" className="admin-btn admin-btn-danger" disabled={loading}>
                {loading ? "Disabling..." : "Disable MFA"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ============================================================
          MFA DISABLED
          ============================================================ */}
      {!user.mfa_enabled && (
        <div className="admin-table-wrapper">
          <h2 className="admin-form-title">MFA Status</h2>
          <p>
            MFA is currently <strong>disabled</strong>.
          </p>

          <div className="admin-actions" style={{ marginTop: "12px" }}>
            <button className="admin-btn" onClick={() => setShowSetup(true)}>
              Enable MFA
            </button>
          </div>
        </div>
      )}

      {/* ============================================================
          MFA SETUP MODAL (Unified Neon‑Glassy Modal)
          ============================================================ */}
      {showSetup && (
        <div className="mfa-setup-modal">
          <div className="mfa-setup-content">
            <button className="mfa-close-btn" onClick={() => setShowSetup(false)}>
              ✕
            </button>

            <MFASetup />
          </div>
        </div>
      )}
    </div>
  );
}
