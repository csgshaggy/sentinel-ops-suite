import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",   // ⭐ REQUIRED for session cookies
        body: JSON.stringify({ username, password })
      });

      if (response.ok) {
        navigate("/");            // ⭐ Redirect to dashboard
      } else {
        const data = await response.json().catch(() => ({}));
        setError(data.detail || "Login failed");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  return (
    <div className="login-container">
      <h1>Sign In</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <p className="error">{error}</p>}

        <button type="submit">Login</button>
      </form>
    </div>
  );
}
