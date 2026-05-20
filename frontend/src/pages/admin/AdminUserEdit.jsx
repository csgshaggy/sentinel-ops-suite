// =====================================================================
// SSRF Command Console — Admin Edit User Page
// Session Cookie Auth • Update Role • Enable/Disable
// =====================================================================

import { useEffect, useState } from "react";

import { fetchUsers, updateUser } from "../../api/admin";

export default function AdminUserEdit({ userId }) {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState("viewer");
  const [isActive, setIsActive] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const users = await fetchUsers();
        const u = users.find((x) => x.id === userId);
        if (!u) {
          setError("User not found");
          return;
        }
        setUser(u);
        setRole(u.role);
        setIsActive(u.is_active);
      } catch {
        setError("Failed to load user");
      }
    }
    load();
  }, [userId]);

  async function handleSave() {
    try {
      await updateUser(userId, { role, is_active: isActive });
      setSuccess("User updated successfully");
    } catch {
      setError("Failed to update user");
    }
  }

  if (!user) {
    return (
      <div className="panel" style={{ margin: "2rem" }}>
        Loading...
      </div>
    );
  }

  return (
    <div className="panel" style={{ margin: "2rem", maxWidth: "400px" }}>
      <h2>Edit User</h2>

      {error && <div className="error">{error}</div>}
      {success && <div className="info">{success}</div>}

      <div>Email: {user.email}</div>

      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="viewer">Viewer</option>
        <option value="operator">Operator</option>
        <option value="admin">Admin</option>
      </select>

      <label style={{ marginTop: "1rem" }}>
        <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} />
        Active
      </label>

      <button style={{ marginTop: "1rem" }} onClick={handleSave}>
        Save
      </button>
    </div>
  );
}
