// /src/features/auth/MFASetup.jsx
// ============================================================
// SentinelOps — MFA Setup (Neon‑Glassy Unified Theme)
// - Works with unified backend
// - Works with unified AuthContext
// - Matches Security.css + AdminPanel.css
// ============================================================

import { useState, useEffect } from "react";
import client from "../../api/apiClient.js";
import { useAuth } from "./AuthContext.jsx";
import { toast } from "../../components/ToastManager.jsx";

export default function MFASetup() {
  const { user, refreshUser } = useAuth();

  const [qrCode, setQrCode] = useState(null);
  const [secret, setSecret] = useState(null);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------
  // Load MFA setup data (QR + secret)
  // ------------------------------------------------------------
  useEffect(() => {
    if (!user) return;

    (async () => {
      const res = await client.get("/mfa/setup");

      if (!res.ok) {
        toast.error("Failed to load MFA setup.");
        return;
      }

      setQrCode(res.data.qr_code);
      setSecret(res.data.secret);
    })();
  }, [user]);

  // ------------------------------------------------------------
  // Enable MFA
  // ------------------------------------------------------------
  async function handleEnable(e) {
    e.preventDefault();
    setLoading(true);

    const res = await client.post("/mfa/enable", { code });

    setLoading(false);

    if (!res.ok) {
      toast.error("Invalid MFA code.");
      return;
    }

    toast.success("MFA enabled successfully.");
    await refreshUser();
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
    await refreshUser();
  }

  return (
    <div className="mfa-setup-container">
      <h2 className="mfa-title">Multi‑Factor Authentication</h2>

      {/* ============================================================
          MFA DISABLED → SHOW SETUP
          ============================================================ */}
      {!user?.mfa_enabled && (
        <div className="mfa-card">
          <p className="mfa-description">
            Scan this QR code with your authenticator app:
          </p>

          {qrCode && (
            <div className="mfa-qr-wrapper">
              <img src={qrCode} alt="MFA QR Code" className="mfa-qr" />
            </div>
          )}

          {secret && (
            <p className="mfa-secret">
              Secret: <span>{secret}</span>
            </p>
          )}

          <form onSubmit={handleEnable} className="mfa-form">
            <input
              type="text"
              inputMode="numeric"
              maxLength={6}
              className="mfa-input"
              placeholder="Enter 6‑digit code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />

            <button type="submit" className="mfa-btn" disabled={loading}>
              {loading ? "Enabling..." : "Enable MFA"}
            </button>
          </form>
        </div>
      )}

      {/* ============================================================
          MFA ENABLED → SHOW DISABLE FORM
          ============================================================ */}
      {user?.mfa_enabled && (
        <div className="mfa-card">
          <p className="mfa-description">
            MFA is currently <strong>enabled</strong> on your account.
          </p>

          <form onSubmit={handleDisable} className="mfa-form">
            <input
              type="text"
              inputMode="numeric"
              maxLength={6}
              className="mfa-input"
              placeholder="Enter 6‑digit code to disable"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />

            <button type="submit" className="mfa-btn mfa-btn-danger" disabled={loading}>
              {loading ? "Disabling..." : "Disable MFA"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
