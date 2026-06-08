// /src/components/profile/MFAToggle.jsx
// SentinelOps — MFA Toggle (Unified + Neon‑Glassy)

import React, { useState } from "react";
import { toast } from "../../components/ToastManager.jsx";

export default function MFAToggle({
  enabled,
  qr,
  secret,
  onStart,
  onVerify,
  onDisable,
}) {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------
  // Start MFA enrollment
  // ------------------------------------------------------------
  const handleStart = async () => {
    try {
      setLoading(true);
      await onStart();
      toast.success("MFA setup started. Scan the QR code.");
    } catch (err) {
      console.error("MFA start failed:", err);
      toast.error("Failed to start MFA setup.");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------------------------
  // Verify MFA code
  // ------------------------------------------------------------
  const handleVerify = async () => {
    if (!code || code.length !== 6) {
      toast.error("Enter your 6‑digit MFA code.");
      return;
    }

    try {
      setLoading(true);
      await onVerify(code);
      setCode("");
      toast.success("MFA enabled successfully.");
    } catch (err) {
      console.error("MFA verify failed:", err);
      toast.error("Invalid MFA code.");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------------------------
  // Disable MFA
  // ------------------------------------------------------------
  const handleDisable = async () => {
    try {
      setLoading(true);
      await onDisable();
      toast.success("MFA disabled.");
    } catch (err) {
      console.error("MFA disable failed:", err);
      toast.error("Failed to disable MFA.");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------------------------
  // RENDER
  // ------------------------------------------------------------
  return (
    <div className="profile-section">
      <h2 className="profile-section-title">Multi‑Factor Authentication</h2>

      {/* ENABLE MFA */}
      {!enabled && !qr && (
        <>
          <p>Enable MFA to add an extra layer of security to your account.</p>

          <button
            className="profile-button"
            onClick={handleStart}
            disabled={loading}
          >
            {loading ? "Starting…" : "Enable MFA"}
          </button>
        </>
      )}

      {/* MFA SETUP (QR + CODE ENTRY) */}
      {!enabled && qr && (
        <div className="mfa-setup">
          <p>Scan this QR code with your authenticator app:</p>

          <img src={qr} alt="MFA QR" className="mfa-qr" />

          {secret && (
            <p style={{ marginTop: "8px", color: "#8be8ff" }}>
              Or enter this secret manually:{" "}
              <strong style={{ color: "#00ffff" }}>{secret}</strong>
            </p>
          )}

          <input
            className="profile-input"
            placeholder="Enter 6‑digit code"
            value={code}
            maxLength={6}
            onChange={(e) => {
              const v = e.target.value.replace(/\D/g, "");
              setCode(v);
            }}
          />

          <button
            className="profile-button"
            disabled={loading || code.length !== 6}
            onClick={handleVerify}
          >
            {loading ? "Verifying…" : "Verify & Enable"}
          </button>
        </div>
      )}

      {/* DISABLE MFA */}
      {enabled && !qr && (
        <>
          <p>Your account is currently protected with MFA.</p>

          <button
            className="profile-button danger"
            onClick={handleDisable}
            disabled={loading}
          >
            {loading ? "Disabling…" : "Disable MFA"}
          </button>
        </>
      )}
    </div>
  );
}
