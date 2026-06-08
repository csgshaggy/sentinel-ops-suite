// File: /src/pages/settings/ChangePassword.jsx

import { useState, useCallback } from "react";
import axios from "../../utils/axiosInstance";
import "./ChangePassword.css";

export default function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = useCallback(async () => {
    setError("");
    setSuccess("");

    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.");
      return;
    }

    try {
      setLoading(true);
      await axios.post("/api/auth/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
      });

      setSuccess("Password updated successfully.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch {
      setError("Failed to update password.");
    } finally {
      setLoading(false);
    }
  }, [currentPassword, newPassword, confirmPassword]);

  return (
    <div className="change-password-container">
      <h1>Change Password</h1>

      <div className="cp-field">
        <label>Current Password</label>
        <input
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </div>

      <div className="cp-field">
        <label>New Password</label>
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>

      <div className="cp-field">
        <label>Confirm New Password</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>

      <button className="cp-button" onClick={handleSubmit} disabled={loading}>
        {loading ? "Updating..." : "Update Password"}
      </button>

      {error && <p className="cp-error">{error}</p>}
      {success && <p className="cp-success">{success}</p>}
    </div>
  );
}
