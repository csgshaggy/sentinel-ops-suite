// /src/pages/admin/ToggleUser.jsx

import { useState, useEffect, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/admin/ToggleUser.css";

export default function ToggleUser() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [saving, setSaving] = useState(false);

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
  // Toggle active status
  // ------------------------------------------------------------
  async function handleToggle() {
    setSaving(true);

    try {
      const res = await apiClient.patch(`/admin/users/${id}/toggle`);

      if (res.data?.success) {
        toast.success(
          user.active ? "User disabled successfully." : "User enabled successfully."
        );
        navigate(`/admin/users/${id}`);
        return;
      }

      toast.error("Failed to update user status.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error updating user.");
    }

    setSaving(false);
  }

  if (loading) {
    return <div className="toggleuser-loading">Loading user…</div>;
  }

  if (!user) {
    return <div className="toggleuser-error">User not found.</div>;
  }

  return (
    <div className="toggleuser-container">
      <div className="toggleuser-card">
        <h1 className="toggleuser-title">
          {user.active ? "Disable User" : "Enable User"}
        </h1>

        <p className="toggleuser-message">
          Are you sure you want to{" "}
          <strong>{user.active ? "disable" : "enable"}</strong> the account for:
        </p>

        <p className="toggleuser-username">{user.username}</p>

        <div className="toggleuser-actions">
          <button
            className="btn-accent"
            onClick={handleToggle}
            disabled={saving}
          >
            {saving
              ? user.active
                ? "Disabling..."
                : "Enabling..."
              : user.active
              ? "Disable User"
              : "Enable User"}
          </button>

          <button
            className="btn-secondary"
            onClick={() => navigate(`/admin/users/${id}`)}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
