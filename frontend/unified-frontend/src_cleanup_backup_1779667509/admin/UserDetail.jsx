// /src/pages/UserDetail.jsx

import { useState, useEffect, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/UserDetail.css";

export default function UserDetail() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  // ------------------------------------------------------------
  // fetchUser (React 18 safe)
  // ------------------------------------------------------------
  const fetchUser = useCallback(async () => {
    try {
      const res = await apiClient.get(`/users/${id}`);
      setUser(res.data);
    } catch {
      toast.error("Failed to load user.");
      navigate("");
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

  if (loading) {
    return <div className="userdetail-loading">Loading user…</div>;
  }

  if (!user) {
    return <div className="userdetail-error">User not found.</div>;
  }

  return (
    <div className="userdetail-container">
      <div className="userdetail-card">
        <h1 className="userdetail-title">User Details</h1>

        <div className="userdetail-grid">
          <div>
            <label>Full Name</label>
            <p>{user.full_name}</p>
          </div>

          <div>
            <label>Username</label>
            <p>{user.username}</p>
          </div>

          <div>
            <label>Email</label>
            <p>{user.email}</p>
          </div>

          <div>
            <label>Role</label>
            <p>{user.role}</p>
          </div>

          <div>
            <label>Active</label>
            <p className={user.active ? "active-yes" : "active-no"}>
              {user.active ? "Yes" : "No"}
            </p>
          </div>

          <div>
            <label>MFA Enabled</label>
            <p className={user.mfa_enabled ? "active-yes" : "active-no"}>
              {user.mfa_enabled ? "Yes" : "No"}
            </p>
          </div>

          <div>
            <label>Created At</label>
            <p>{new Date(user.created_at).toLocaleString()}</p>
          </div>

          <div>
            <label>Last Login</label>
            <p>
              {user.last_login
                ? new Date(user.last_login).toLocaleString()
                : "Never"}
            </p>
          </div>
        </div>

        <div className="userdetail-actions">
          <button
            className="btn-accent"
            onClick={() => navigate(`/users/${id}/edit`)}
          >
            Edit User
          </button>

          <button
            className="btn-secondary"
            onClick={() => navigate(`/users/${id}/toggle`)}
          >
            {user.active ? "Disable User" : "Enable User"}
          </button>

          <button
            className="btn-secondary"
            onClick={() => navigate(`/users/${id}/reset-password`)}
          >
            Reset Password
          </button>

          <button
            className="btn-danger"
            onClick={() => navigate(`/users/${id}/delete`)}
          >
            Delete User
          </button>
        </div>

        <div className="userdetail-footer">
          <a onClick={() => navigate("/users")}>Back to User List</a>
        </div>
      </div>
    </div>
  );
}
