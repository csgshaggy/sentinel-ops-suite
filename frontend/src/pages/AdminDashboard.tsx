import React, { useEffect, useState } from "react";

const AdminDashboard: React.FC = () => {
  const [user, setUser] = useState<{ username: string; role: string } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));

      // Enforce admin‑only access
      if (payload.role !== "admin") {
        window.location.href = "/dashboard";
        return;
      }

      setUser({
        username: payload.sub,
        role: payload.role,
      });
    } catch (err) {
      console.error("Invalid token", err);
      window.location.href = "/login";
    }
  }, []);

  return (
    <div style={{ padding: "2rem", color: "#fff" }}>
      <h1>SentinelOps Administrator Console</h1>

      {user && (
        <p>
          Logged in as <strong>{user.username}</strong> ({user.role})
        </p>
      )}

      <div style={{ marginTop: "2rem" }}>
        <p>Welcome, Administrator. System‑wide controls, user management, audit logs, and operational health tiles will appear here.</p>
      </div>
    </div>
  );
};

export default AdminDashboard;
