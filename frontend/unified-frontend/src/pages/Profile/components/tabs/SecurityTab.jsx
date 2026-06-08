// /src/pages/Profile/components/tabs/SecurityTab.jsx
// SentinelOps — Full Security Dashboard (Password Change + Account Security Overview)

import { useState } from "react";
import PasswordStrengthMeter from "../PasswordStrengthMeter.jsx";
import "./SecurityTab.css";

export default function SecurityTab({ profile }) {
  // ------------------------------------------------------------
  // Password Change State
  // ------------------------------------------------------------
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [confirm, setConfirm] = useState("");

  const passwordsMatch = next && confirm && next === confirm;

  const handleSubmit = () => {
    if (!passwordsMatch) return;

    // NOTE: Real API call will be wired in Phase 3
  };

  // ------------------------------------------------------------
  // Derived Security Data
  // ------------------------------------------------------------
  const trustedDevices = profile.trusted_devices || [];
  const riskScore = profile.risk_score || 0;

  return (
    <div className="security-tab-container fade-in">

      {/* ------------------------------------------------------------
          SECTION: Account Security Overview
      ------------------------------------------------------------ */}
      <h2 className="tab-title">Account Security Overview</h2>

      <div className="security-grid">
        <div className="security-item glass">
          <label>Password Last Changed</label>
          <div>{profile.password_changed || "Unknown"}</div>
        </div>

        <div className="security-item glass">
          <label>MFA Enabled</label>
          <div>{profile.mfa_enabled ? "Yes" : "No"}</div>
        </div>

        <div className="security-item glass">
          <label>Account Status</label>
          <div>{profile.active ? "Active" : "Disabled"}</div>
        </div>

        <div className="security-item glass">
          <label>Trusted Devices</label>
          <div>{trustedDevices.length}</div>
        </div>

        <div className="security-item glass">
          <label>Risk Score</label>
          <div>{riskScore}</div>
        </div>
      </div>

      {/* ------------------------------------------------------------
          SECTION: Password Change
      ------------------------------------------------------------ */}
      <h2 className="tab-title" style={{ marginTop: "2rem" }}>
        Change Password
      </h2>

      <div className="form-group">
        <label className="form-label">Current Password</label>
        <input
          className="form-input"
          type="password"
          value={current}
          onChange={(e) => setCurrent(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label className="form-label">New Password</label>
        <input
          className="form-input"
          type="password"
          value={next}
          onChange={(e) => setNext(e.target.value)}
        />
        <PasswordStrengthMeter password={next} />
      </div>

      <div className="form-group">
        <label className="form-label">Confirm New Password</label>
        <input
          className="form-input"
          type="password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
        />
      </div>

      <button
        className="btn-primary"
        disabled={!passwordsMatch || !next || !current}
        onClick={handleSubmit}
      >
        Update Password
      </button>

      {/* ------------------------------------------------------------
          SECTION: Security Recommendations
      ------------------------------------------------------------ */}
      <h2 className="tab-title" style={{ marginTop: "2rem" }}>
        Security Recommendations
      </h2>

      <ul className="security-recommendations glass">
        {!profile.mfa_enabled && (
          <li>Enable MFA to significantly increase account security.</li>
        )}
        {riskScore > 50 && (
          <li>Your risk score is elevated. Review recent login activity.</li>
        )}
        {trustedDevices.length === 0 && (
          <li>No trusted devices detected. Consider adding one.</li>
        )}
        <li>Use a strong, unique password and rotate it regularly.</li>
      </ul>
    </div>
  );
}
