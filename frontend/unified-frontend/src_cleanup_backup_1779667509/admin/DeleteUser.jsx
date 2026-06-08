// /src/pages/DeleteUser.jsx

import { useState, useEffect, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/DeleteUser.css";

export default function DeleteUser() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
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
      navigate("/users");
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
  // Delete user
  // ------------------------------------------------------------
  async function handleDelete() {
    setDeleting(true);

    try {
      const res = await apiClient.delete(`/users/${id}`);

      if (res.data?.success) {
        toast.success("User deleted successfully.");
        navigate("/users");
        return;
      }

      toast.error("Failed to delete user.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error deleting user.");
    }

    setDeleting(false);
  }

  if (loading) {
    return <div className="deleteuser-loading">Loading user…</div>;
  }

  if (!user) {
    return <div className="deleteuser-error">User not found.</div>;
  }

  return (
    <div className="deleteuser-container">
      <div className="deleteuser-card">
        <h1 className="deleteuser-title">Delete User</h1>

        <p className="deleteuser-warning">
          This action is <strong>permanent</strong> and cannot be undone.
        </p>

        <p className="deleteuser-message">
          Are you sure you want to delete the account for:
        </p>

        <p className="deleteuser-username">{user.username}</p>

        <div className="deleteuser-actions">
          <button
            className="btn-danger"
            onClick={handleDelete}
            disabled={deleting}
          >
            {deleting ? "Deleting..." : "Delete User"}
          </button>

          <button
            className="btn-secondary"
            onClick={() => navigate(`/users/${id}`)}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
