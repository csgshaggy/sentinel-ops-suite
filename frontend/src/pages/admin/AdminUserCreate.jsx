// =====================================================================
// SSRF Command Console — Admin Create User Page
// Session Cookie Auth • Create User
// =====================================================================

import { useState } from "react";
import { createUser } from "../../api/admin";

export default function AdminUserCreate() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await createUser({ email, password, role });
      setSuccess("User created successfully");
      setEmail("");
      setPassword("");
      setRole("viewer");
    } catch {
      setError("Failed to create user");
    }
  }

  return (
    <div className="panel" style={{ margin: "2rem", maxWidth: "400px" }}>
      <h2>Create User</h2>

      {error && <div className="error">{error}</div>}
      {success && <div className="info">{success}</div>}

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
      >
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          placeholder="Temporary Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="viewer">Viewer</option>
          <option value="operator">Operator</option>
          <option value="admin">Admin</option>
        </select>

        <button type="submit">Create</button>
      </form>
    </div>
  );
}
