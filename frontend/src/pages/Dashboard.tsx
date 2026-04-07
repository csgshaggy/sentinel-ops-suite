import React, { useEffect, useState } from "react";

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<{ username: string; role: string } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    // Decode JWT payload
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
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
      <h1>SentinelOps Analyst Dashboard</h1>

      {user && (
        <p>
          Logged in as <strong>{user.username}</strong> ({user.role})
        </p>
      )}

      <div style={{ marginTop: "2rem" }}>
        <p>Welcome to the operational dashboard. Your tiles, alerts, and system metrics will appear here.</p>
      </div>
    </div>
  );
};

export default Dashboard;
