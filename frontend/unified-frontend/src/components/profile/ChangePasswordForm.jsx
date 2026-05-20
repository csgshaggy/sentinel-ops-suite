// /src/components/profile/ChangePasswordForm.jsx

import React, { useState } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

const ChangePasswordForm = () => {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      toast.error("New passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      await apiClient.post("/api/auth/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
      });

      toast.success("Password updated successfully.");

      // Reset fields
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      console.error("Password update failed:", err);

      const detail =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Failed to update password.";

      toast.error(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <label className="profile-label">Current Password</label>
      <input
        type="password"
        className="profile-input"
        value={currentPassword}
        onChange={(e) => setCurrentPassword(e.target.value)}
        required
      />

      <label className="profile-label">New Password</label>
      <input
        type="password"
        className="profile-input"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
        required
      />

      <label className="profile-label">Confirm New Password</label>
      <input
        type="password"
        className="profile-input"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        required
      />

      <button className="profile-button" disabled={loading}>
        {loading ? "Updating..." : "Update Password"}
      </button>
    </form>
  );
};

export default ChangePasswordForm;

