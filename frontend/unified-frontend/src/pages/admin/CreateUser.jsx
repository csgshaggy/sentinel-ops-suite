// /src/pages/admin/CreateUser.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import "../../styles/admin/CreateUser.css";

export default function CreateUser() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("user");
  const [password, setPassword] = useState("");
  const [active, setActive] = useState(true);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await apiClient.post("/admin/users", {
        full_name: fullName,
        username,
        email,
        role,
        password,
        active,
      });

      if (res.data?.success) {
        toast.success("User created successfully.");
        navigate("/admin");
        return;
      }

      toast.error("Failed to create user.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error creating user.");
    }

    setLoading(false);
  }

  return (
    <div className="create-user-container">
      <div className="create-user-card">
        <h1 className="create-user-title">Create User</h1>

        <form className="create-user-form" onSubmit={handleSubmit}>
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

          <label>Temporary Password</label>
          <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Set a temporary password"
            required
          />

          <label className="active-toggle">
            <input
              type="checkbox"
              checked={active}
              onChange={(e) => setActive(e.target.checked)}
            />
            Active
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create User"}
          </button>
        </form>

        <div className="create-user-footer">
          <a onClick={() => navigate("/admin")}>Back to Admin Panel</a>
        </div>
      </div>
    </div>
  );
}
