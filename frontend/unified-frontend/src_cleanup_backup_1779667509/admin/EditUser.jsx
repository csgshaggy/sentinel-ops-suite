// /src/pages/EditUser.jsx

import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/EditUser.css";

export default function EditUser() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("user");
  const [active, setActive] = useState(true);

  // Fetch user details
  useEffect(() => {
    async function fetchUser() {
      try {
        const res = await apiClient.get(`/users/${id}`);
        const u = res.data;

        setFullName(u.full_name);
        setUsername(u.username);
        setEmail(u.email);
        setRole(u.role);
        setActive(u.active);
      } catch (err) {
        toast.error("Failed to load user.");
        navigate("");
      }

      setLoading(false);
    }

    fetchUser();
  }, [id, navigate]);

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);

    try {
      const res = await apiClient.put(`/users/${id}`, {
        full_name: fullName,
        username,
        email,
        role,
        active,
      });

      if (res.data?.success) {
        toast.success("User updated successfully.");
        navigate("");
        return;
      }

      toast.error("Failed to update user.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error updating user.");
    }

    setSaving(false);
  }

  if (loading) {
    return (
      <div className="edit-user-loading">
        Loading user…
      </div>
    );
  }

  return (
    <div className="edit-user-container">
      <div className="edit-user-card">
        <h1 className="edit-user-title">Edit User</h1>

        <form className="edit-user-form" onSubmit={handleSubmit}>
          <label>Full Name</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />

          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Role</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>

          <label className="active-toggle">
            <input
              type="checkbox"
              checked={active}
              onChange={(e) => setActive(e.target.checked)}
            />
            Active
          </label>

          <button type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </form>

        <div className="edit-user-footer">
          <a onClick={() => navigate("")}>Back to Admin Panel</a>
        </div>
      </div>
    </div>
  );
}
