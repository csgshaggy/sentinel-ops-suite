// /src/components/profile/MFAToggle.jsx

import React, { useState } from "react";

export default function MFAToggle({
  enabled,
  qr,
  secret,
  onStart,
  onVerify,
  onDisable,
}) {
  const [code, setCode] = useState("");
  const [verifying, setVerifying] = useState(false);

  const handleVerify = async () => {
    if (!code || code.length !== 6) {
      return;
    }

    try {
      setVerifying(true);
      await onVerify(code);
      setCode("");
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="mfa-container">
      {/* Enable MFA */}
      {!enabled && !qr && (
        <button className="profile-button" onClick={onStart}>
          Enable MFA
        </button>
      )}

      {/* MFA Setup (QR + Code Entry) */}
      {qr && (
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
            placeholder="Enter 6-digit code"
            value={code}
            maxLength={6}
            onChange={(e) => {
              const v = e.target.value.replace(/\D/g, "");
              setCode(v);
            }}
          />

          <button
            className="profile-button"
            disabled={verifying || code.length !== 6}
            onClick={handleVerify}
          >
            {verifying ? "Verifying..." : "Verify & Enable"}
          </button>
        </div>
      )}

      {/* Disable MFA */}
      {enabled && !qr && (
        <button className="profile-button danger" onClick={onDisable}>
          Disable MFA
        </button>
      )}
    </div>
  );
}
