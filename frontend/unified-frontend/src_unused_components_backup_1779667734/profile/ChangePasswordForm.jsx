// /src/components/profile/ChangePasswordForm.jsx
// SentinelOps — Change Password Form (Unified + Secure + Neon‑Glassy)

import React, { useState } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

export default function ChangePasswordForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------
  // Validation
  // ------------------------------------------------------------
  const validate = () => {
    if (!currentPassword.trim() || !newPassword.trim() || !confirmPassword.trim()) {
      toast.error("All fields are required.");
      return false;
    }

    if (newPassword.length < 8) {
      toast.error("New password must be at least 8 characters.");
      return false;
    }

    if (newPassword !== confirmPassword) {
      toast.error("New passwords do not match.");
      return false;
    }

    return true;
  };

  // ------------------------------------------------------------
  // Submit handler
  // ------------------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      setLoading(true);

      await apiClient.post(
        "/profile/change-password",
        {
          current_password: currentPassword,
          new_password: newPassword,
        },
        { withCredentials: true }
      );

      toast.success("Password updated successfully.");

      // Reset fields
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      console.error("Password update failed:", err);

      if (err.response?.status === 401) {
        toast.error("Current password is incorrect.");
      } else {
        const detail =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          "Failed to update password.";

        toast.error(detail);
      }
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------------------------
  // RENDER
  // ------------------------------------------------------------
  return (
    <div className="profile-section">
      <h2 className="profile-section-title">Change Password</h2>

      <form className="profile-form" onSubmit={handleSubmit}>
        <label className="profile-label">Current Password</label>
        <input
          type="password"
          className="profile-input"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          autoComplete="current-password"
          required
        />

        <label className="profile-label">New Password</label>
        <input
          type="password"
          className="profile-input"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          autoComplete="new-password"
          required
        />

        <label className="profile-label">Confirm New Password</label>
        <input
          type="password"
          className="profile-input"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          autoComplete="new-password"
          required
        />

        <button className="profile-button" disabled={loading}>
          {loading ? "Updating…" : "Update Password"}
        </button>
      </form>
    </div>
  );
}
