// /src/pages/Profile/components/tabs/MFATab.jsx
// SentinelOps — MFA Tab (Enable, QR, Verify, Disable)

import { useState } from "react";
import "./MFATab.css";

export default function MFATab({
  enabled,
  qr,
  secret,
  onStart,
  onVerify,
  onDisable,
}) {
  const [code, setCode] = useState("");

  // ------------------------------------------------------------
  // Render: MFA Enabled
  // ------------------------------------------------------------
  if (enabled && !qr) {
    return (
      <div className="mfa-tab-container">
        <div className="mfa-status-block enabled glass">
          <h3>MFA is Enabled</h3>
          <p>Your account is protected with multi‑factor authentication.</p>

          <button className="btn-danger" onClick={onDisable}>
            Disable MFA
          </button>
        </div>
      </div>
    );
  }

  // ------------------------------------------------------------
  // Render: MFA Setup Started (QR + Secret)
  // ------------------------------------------------------------
  if (qr && secret) {
    return (
      <div className="mfa-tab-container">
        <div className="mfa-setup-block glass">
          <h3>Scan the QR Code</h3>

          <img src={qr} alt="MFA QR Code" className="mfa-qr" />

          <p className="mfa-secret-label">
            Or enter this secret manually:
          </p>
          <div className="mfa-secret-box">{secret}</div>

          <div className="mfa-code-input-group">
            <label className="form-label">Enter 6‑digit Code</label>
            <input
              className="form-input mfa-code-input"
              type="text"
              maxLength={6}
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
              onKeyDown={(e) => {
                if (e.key === "Enter" && code.length === 6) {
                  onVerify(code);
                }
              }}
            />
          </div>

          <button
            className="btn-primary"
            disabled={code.length !== 6}
            onClick={() => onVerify(code)}
          >
            Verify & Enable MFA
          </button>
        </div>
      </div>
    );
  }

  // ------------------------------------------------------------
  // Render: MFA Disabled (Start Setup)
  // ------------------------------------------------------------
  return (
    <div className="mfa-tab-container">
      <div className="mfa-status-block disabled glass">
        <h3>MFA is Disabled</h3>
        <p>Enable MFA to protect your account with an extra layer of security.</p>

        <button className="btn-primary" onClick={onStart}>
          Enable MFA
        </button>
      </div>
    </div>
  );
}
