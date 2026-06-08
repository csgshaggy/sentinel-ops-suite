// /src/pages/AdminUsers.jsx
// ============================================================
// SentinelOps — Admin: User Management (Unified + Neon‑Glassy)
// - RBAC protected (admin only)
// - Uses unified apiClient.js
// - Uses unified AuthContext
// - Deterministic operator‑grade UI
// ============================================================

import React, { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { useNavigate } from "react-router-dom";
import client from "../api/apiClient.js";
import { toast } from "../components/ToastManager.jsx";
import "./AdminPanel.css"; // unified admin theme

export default function AdminUsers() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(true);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "user",
  });

  const [editingId, setEditingId] = useState(null);

  // ------------------------------------------------------------
  // RBAC: Only admins may enter
  // ------------------------------------------------------------
  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/login", { replace: true });
      } else if (user.role !== "admin") {
        navigate("/dashboard", { replace: true });
      }
    }
  }, [user, loading, navigate]);

  // ------------------------------------------------------------
  // Load users
  // ------------------------------------------------------------
  async function loadUsers() {
    setLoadingUsers(true);

    const res = await client.get("/users");

    setLoadingUsers(false);

    if (!res.ok) {
      toast.error("Failed to load users.");
      return;
    }

    setUsers(res.data || []);
  }

  useEffect(() => {
    if (user?.role === "admin") {
      loadUsers();
    }
  }, [user]);

  // ------------------------------------------------------------
  // Form helpers
  // ------------------------------------------------------------
  function updateForm(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function resetForm() {
    setForm({
      username: "",
      email: "",
      password: "",
      role: "user",
    });
    setEditingId(null);
  }

  // ------------------------------------------------------------
  // Create user
  // ------------------------------------------------------------
  async function handleCreate(e) {
    e.preventDefault();

    const res = await client.post("/users", form);

    if (!res.ok) {
      toast.error("Failed to create user.");
      return;
    }

    toast.success("User created.");
    resetForm();
    loadUsers();
  }

  // ------------------------------------------------------------
  // Edit user
  // ------------------------------------------------------------
  function startEdit(u) {
    setEditingId(u.id);
    setForm({
      username: u.username,
      email: u.email || "",
      password: "",
      role: u.role,
    });
  }

  async function handleUpdate(e) {
    e.preventDefault();

    const res = await client.put(`/users/${editingId}`, form);

    if (!res.ok) {
      toast.error("Failed to update user.");
      return;
    }

    toast.success("User updated.");
    resetForm();
    loadUsers();
  }

  // ------------------------------------------------------------
  // Delete user
  // ------------------------------------------------------------
  async function handleDelete(id) {
    if (!window.confirm("Delete this user?")) return;

    const res = await client.delete(`/users/${id}`);

    if (!res.ok) {
      toast.error("Failed to delete user.");
      return;
    }

    toast.success("User deleted.");
    loadUsers();
  }

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  if (loading || !user || user.role !== "admin") {
    return <div className="admin-panel">Loading...</div>;
  }

  return (
    <div className="admin-panel">
      <h1 className="admin-title">User Management</h1>

      {/* ============================================================
         USER FORM (Create / Edit)
         ============================================================ */}
      <div className="admin-table-wrapper" style={{ marginBottom: "20px" }}>
        <form
          className="admin-form"
          onSubmit={editingId ? handleUpdate : handleCreate}
        >
          <h2 className="admin-form-title">
            {editingId ? "Edit User" : "Create User"}
          </h2>

          <div className="admin-form-grid">
            <input
              type="text"
              placeholder="Username"
              value={form.username}
              onChange={(e) => updateForm("username", e.target.value)}
              required
            />

            <input
              type="email"
              placeholder="Email (optional)"
              value={form.email}
              onChange={(e) => updateForm("email", e.target.value)}
            />

            <input
              type="password"
              placeholder={editingId ? "New Password (optional)" : "Password"}
              value={form.password}
              onChange={(e) => updateForm("password", e.target.value)}
              required={!editingId}
            />

            <select
              value={form.role}
              onChange={(e) => updateForm("role", e.target.value)}
            >
              <option value="user">User</option>
              <option value="operator">Operator</option>
              <option value="analyst">Analyst</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div className="admin-actions" style={{ marginTop: "12px" }}>
            <button type="submit" className="admin-btn">
              {editingId ? "Update User" : "Create User"}
            </button>

            {editingId && (
              <button
                type="button"
                className="admin-btn admin-btn-danger"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* ============================================================
         USER TABLE
         ============================================================ */}
      <div className="admin-table-wrapper">
        <h2 className="admin-form-title">Existing Users</h2>

        {loadingUsers ? (
          <div className="admin-empty">Loading users...</div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>MFA</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.username}</td>
                  <td>{u.email || "—"}</td>
                  <td>{u.role}</td>
                  <td>
                    <span
                      className={
                        u.mfa_enabled
                          ? "admin-status status-active"
                          : "admin-status status-disabled"
                      }
                    >
                      {u.mfa_enabled ? "Enabled" : "Disabled"}
                    </span>
                  </td>

                  <td>
                    <div className="admin-actions">
                      <button
                        className="admin-btn"
                        onClick={() => startEdit(u)}
                      >
                        Edit
                      </button>

                      <button
                        className="admin-btn admin-btn-danger"
                        onClick={() => handleDelete(u.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
