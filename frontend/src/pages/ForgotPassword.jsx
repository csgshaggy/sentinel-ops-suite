// File: src/pages/ForgotPassword.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!username.trim()) {
      setError("Username is required");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
      });

      if (!res.ok) throw new Error("Request failed");

      setSuccess(true);
    } catch (err) {
      setError("Unable to process request");
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="forgot-page">
        <div className="forgot-container success-state">
          <h2>Password Reset Sent</h2>
          <p>
            If an account exists for <strong>{username}</strong>, a reset link
            has been emailed.
          </p>

          <button
            className="forgot-button"
            onClick={() => navigate("/login")}
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }
  return (
    <div className="forgot-page">
      <div className="forgot-container">

        {error && <div className="error-banner">{error}</div>}

        <form className="forgot-form" onSubmit={handleSubmit}>
          <h2 className="forgot-title">Reset Password</h2>

          <label className="forgot-label">Username</label>
          <input
            type="text"
            className="forgot-input"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setError("");
            }}
            disabled={loading}
          />
          <button
            type="submit"
            className="forgot-button"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </button>

          <div className="forgot-back-link">
            <span onClick={() => navigate("/login")}>
              Back to login
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}

