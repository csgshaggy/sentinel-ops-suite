// /src/pages/admin/ResetUserPassword.jsx

import { useState, useEffect, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/admin/ResetUserPassword.css";

export default function ResetUserPassword() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [user, setUser] = useState(null);
  const [tempPassword, setTempPassword] = useState("");

  // ------------------------------------------------------------
  // fetchUser (React 18 safe)
  // ------------------------------------------------------------
  const fetchUser = useCallback(async () => {
    try {
      const res = await apiClient.get(`/admin/users/${id}`);
      setUser(res.data);
    } catch {
      toast.error("Failed to load user.");
      navigate("/admin/users");
    } finally {
      setLoading(false);
    }
  }, [id, navigate]);

  // ------------------------------------------------------------
  // Trigger fetch (wrapped in microtask)
  // ------------------------------------------------------------
  useEffect(() => {
    Promise.resolve().then(() => fetchUser());
  }, [fetchUser]);

  // ------------------------------------------------------------
  // Reset password
  // ------------------------------------------------------------
  async function handleReset() {
    setSaving(true);

    try {
      const res = await apiClient.post(`/admin/users/${id}/reset-password`);

      if (res.data?.success) {
        setTempPassword(res.data.temp_password);
        toast.success("Password reset successfully.");
        return;
      }

      toast.error("Failed to reset password.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error resetting password.");
    }

    setSaving(false);
  }

  if (loading) {
    return <div className="resetpw-loading">Loading user…</div>;
  }

  if (!user) {
    return <div className="resetpw-error">User not found.</div>;
  }

  return (
    <div className="resetpw-container">
      <div className="resetpw-card">
        <h1 className="resetpw-title">Reset Password</h1>

        {!tempPassword ? (
          <>
            <p className="resetpw-message">Reset the password for user:</p>

            <p className="resetpw-username">{user.username}</p>

            <p className="resetpw-warning">
              This will generate a new temporary password and require the user to
              change it on next login.
            </p>

            <div className="resetpw-actions">
              <button
                className="btn-accent"
                onClick={handleReset}
                disabled={saving}
              >
                {saving ? "Resetting..." : "Reset Password"}
              </button>

              <button
                className="btn-secondary"
                onClick={() => navigate(`/admin/users/${id}`)}
              >
                Cancel
              </button>
            </div>
          </>
        ) : (
          <>
            <p className="resetpw-success">Temporary password generated:</p>

            <div className="resetpw-temp-box">{tempPassword}</div>

            <p className="resetpw-note">
              Provide this password to the user. They will be required to change it
              on next login.
            </p>

            <div className="resetpw-actions">
              <button
                className="btn-accent"
                onClick={() => navigate(`/admin/users/${id}`)}
              >
                Done
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
