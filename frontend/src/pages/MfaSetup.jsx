// ============================================
// MfaSetup.jsx — MFA Enrollment Screen
// ============================================

import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import UnifiedAuthShell from "../components/auth/UnifiedAuthShell";
import "./MfaSetup.css";

const MfaSetup = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // User ID passed from dashboard or login
  const userId = location.state?.userId;

  const [qrCode, setQrCode] = useState("");
  const [secret, setSecret] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // --------------------------------------------
  // FETCH MFA SECRET + QR CODE
  // --------------------------------------------
  useEffect(() => {
    const fetchMfaData = async () => {
      try {
        const response = await fetch("/api/auth/mfa/initiate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: userId }),
        });

        const data = await response.json();

        if (!response.ok) {
          setError(data.detail || "Failed to initialize MFA.");
          return;
        }

        setQrCode(data.qr_code);
        setSecret(data.secret);
      } catch (err) {
        setError("Network error. Please try again.");
      }
    };

    fetchMfaData();
  }, [userId]);

  // --------------------------------------------
  // VERIFY TOTP CODE
  // --------------------------------------------
  const handleVerify = async () => {
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/mfa/verify-setup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          code,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Invalid code. Try again.");
        setLoading(false);
        return;
      }

      setSuccess(true);
      setLoading(false);

    } catch (err) {
      setError("Network error. Please try again.");
      setLoading(false);
    }
  };

  // --------------------------------------------
  // RENDER
  // --------------------------------------------
  return (
    <UnifiedAuthShell>
      <div className="mfa-setup-card">

        {success ? (
          <div className="mfa-setup-success">
            <h2 className="mfa-title">MFA Enabled</h2>
            <p className="mfa-description">
              Multi‑factor authentication is now active on your account.
            </p>

            <button
              className="mfa-return-btn"
              onClick={() => navigate("/dashboard")}
            >
              Continue to Dashboard
            </button>
          </div>
        ) : (
          <>
            <h2 className="mfa-title">Enable Multi‑Factor Authentication</h2>
            <p className="mfa-description">
              Scan the QR code with your authenticator app, then enter the 6‑digit code.
            </p>

            {error && <div className="mfa-error">{error}</div>}

            {/* QR CODE */}
            {qrCode && (
              <img
                src={qrCode}
                alt="MFA QR Code"
                className="mfa-qr"
              />
            )}

            {/* SECRET (optional display) */}
            {secret && (
              <div className="mfa-secret">
                <span>Secret:</span> {secret}
              </div>
            )}

            {/* CODE INPUT */}
            <input
              type="text"
              className="mfa-input"
              placeholder="Enter 6‑digit code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              maxLength={6}
            />

            <button
              className="mfa-submit"
              onClick={handleVerify}
              disabled={loading}
            >
              {loading ? "Verifying..." : "Verify & Enable MFA"}
            </button>
          </>
        )}
      </div>
    </UnifiedAuthShell>
  );
};

export default MfaSetup;
