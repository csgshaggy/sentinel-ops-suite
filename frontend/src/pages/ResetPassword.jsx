// File: src/pages/ResetPassword.jsx

import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ResetPassword.css";

export default function ResetPassword() {
  const navigate = useNavigate();
  const { token } = useParams();
  if (!token) {
    return (
      <div className="reset-page">
        <div className="reset-container">
          <div className="error-banner">
            Invalid or missing reset token.
          </div>

          <button
            className="reset-button"
            onClick={() => navigate("/login")}
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  function validate() {
    if (!password.trim()) {
      setError("Password is required");
      return false;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return false;
    }

    if (password !== confirm) {
      setError("Passwords do not match");
      return false;
    }

    return true;
  }
  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!validate()) return;

    setLoading(true);

    try {
      const res = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token,
          password,
        }),
      });

      if (!res.ok) throw new Error("Reset failed");

      setSuccess(true);
    } catch (err) {
      setError("Unable to reset password. Token may be expired.");
    } finally {
      setLoading(false);
    }
  }
  if (success) {
    return (
      <div className="reset-page">
        <div className="reset-container success-state">
          <h2>Password Reset Successful</h2>
          <p>Your password has been updated.</p>

          <button
            className="reset-button"
            onClick={() => navigate("/login")}
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reset-page">
      <div className="reset-container">

        {error && <div className="error-banner">{error}</div>}

        <form className="reset-form" onSubmit={handleSubmit}>
          <h2 className="reset-title">Set New Password</h2>

          <label className="reset-label">New Password</label>
          <input
            type="password"
            className="reset-input"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setError("");
            }}
            disabled={loading}
          />

          <label className="reset-label">Confirm Password</label>
          <input
            type="password"
            className="reset-input"
            value={confirm}
            onChange={(e) => {
              setConfirm(e.target.value);
              setError("");
            }}
            disabled={loading}
          />
          <button
            type="submit"
            className="reset-button"
            disabled={loading}
          >
            {loading ? "Updating..." : "Update Password"}
          </button>

          <div className="reset-back-link">
            <span onClick={() => navigate("/login")}>
              Back to login
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}
