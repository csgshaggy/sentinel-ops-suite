// =====================================================================
// SSRF Command Console — Admin Users Page
// Session Cookie Auth • CRUD • Password Reset
// =====================================================================

import { useEffect, useState } from "react";

import { fetchUsers, resetUserPassword, updateUser } from "../../api/admin";
import Table from "../../components/Table";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadUsers() {
    try {
      const data = await fetchUsers();
      setUsers(data);
      setError("");
    } catch {
      setError("Failed to load users");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function handleResetPassword(id) {
    try {
      const result = await resetUserPassword(id);
      alert(`Temporary password: ${result.temporary_password}`);
    } catch {
      alert("Failed to reset password");
    }
  }

  async function toggleActive(user) {
    try {
      await updateUser(user.id, {
        role: user.role,
        is_active: !user.is_active,
      });
      loadUsers();
    } catch {
      alert("Failed to update user");
    }
  }

  if (loading) {
    return (
      <div className="panel" style={{ margin: "2rem" }}>
        Loading...
      </div>
    );
  }

  return (
    <div className="panel" style={{ margin: "2rem" }}>
      <h2>User Management</h2>

      {error && <div className="error">{error}</div>}

      <Table
        columns={["id", "email", "role", "is_active", "actions"]}
        data={users.map((u) => ({
          id: u.id,
          email: u.email,
          role: u.role,
          is_active: u.is_active ? "Yes" : "No",
          actions: (
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <button onClick={() => handleResetPassword(u.id)}>Reset Password</button>

              <button
                style={{
                  background: u.is_active ? "var(--danger)" : "var(--accent)",
                }}
                onClick={() => toggleActive(u)}
              >
                {u.is_active ? "Disable" : "Enable"}
              </button>
            </div>
          ),
        }))}
      />
    </div>
  );
}
