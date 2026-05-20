// ============================================================================
// AdminUsers.tsx
// SentinelOps — Admin Console
// Session‑Cookie Auth • User Management • Operator‑Grade UI
// ============================================================================

import React, { useEffect, useState } from "react";
import {
  fetchUsers,
  updateUser,
  resetUserPassword,
} from "../../api/admin"; // <-- your unified admin API client
import "./AdminUsers.css"; // optional, safe if exists

interface User {
  id: number;
  email: string;
  role: string;
  is_active: boolean;
  created_at?: string;
}

export default function AdminUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ------------------------------------------------------------
  // Load Users
  // ------------------------------------------------------------
  async function loadUsers() {
    try {
      const data = await fetchUsers();
      setUsers(data);
      setError("");
    } catch (err) {
      console.error("Failed to load users:", err);
      setError("Failed to load users");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  // ------------------------------------------------------------
  // Toggle Active Status
  // ------------------------------------------------------------
  async function handleToggleActive(user: User) {
    try {
      await updateUser(user.id, {
        role: user.role,
        is_active: !user.is_active,
      });
      loadUsers();
    } catch (err) {
      console.error("Failed to update user:", err);
      alert("Failed to update user");
    }
  }

  // ------------------------------------------------------------
  // Reset Password
  // ------------------------------------------------------------
  async function handleResetPassword(id: number) {
    try {
      const result = await resetUserPassword(id);
      alert(`Temporary password: ${result.temporary_password}`);
    } catch (err) {
      console.error("Failed to reset password:", err);
      alert("Failed to reset password");
    }
  }

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  if (loading) {
    return (
      <div className="panel" style={{ margin: "2rem" }}>
        Loading users…
      </div>
    );
  }

  return (
    <div className="panel" style={{ margin: "2rem" }}>
      <h2>User Management</h2>

      {error && <div className="error">{error}</div>}

      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Role</th>
            <th>Active</th>
            <th>Created</th>
            <th style={{ width: "180px" }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.email}</td>
              <td>{u.role}</td>
              <td>{u.is_active ? "Yes" : "No"}</td>
              <td>{u.created_at ? new Date(u.created_at).toLocaleString() : "—"}</td>

              <td>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  <button
                    className="btn-accent"
                    onClick={() => handleResetPassword(u.id)}
                  >
                    Reset Password
                  </button>

                  <button
                    className={u.is_active ? "btn-danger" : "btn-accent"}
                    onClick={() => handleToggleActive(u)}
                  >
                    {u.is_active ? "Disable" : "Enable"}
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
