// File: src/pages/MfaChallenge.jsx

import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./MfaChallenge.css";

export default function MfaChallenge() {
  const navigate = useNavigate();
  const location = useLocation();
  const mfaToken = location?.state?.token || null;

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  if (!mfaToken) {
    return (
      <div className="mfa-page">
        <div className="mfa-container">
          <div className="error-banner">
            Missing MFA token — please log in again.
          </div>

          <button
            className="mfa-button"
            onClick={() => navigate("/login")}
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }
  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!code.trim()) {
      setError("MFA code is required");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/auth/mfa/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: mfaToken,
          code,
        }),
      });

      if (!res.ok) throw new Error("Invalid code");

      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError("Invalid or expired MFA code");
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="mfa-page">
      <div className="mfa-container">

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <form className="mfa-form" onSubmit={handleSubmit}>
          <h2 className="mfa-title">Multi‑Factor Authentication</h2>
          <p className="mfa-instructions">
            Enter the 6‑digit code from your authenticator app.
          </p>
          <label className="mfa-label">Authentication Code</label>
          <input
            type="text"
            maxLength={6}
            className="mfa-input"
            value={code}
            onChange={(e) => {
              setCode(e.target.value);
              setError("");
            }}
            disabled={loading}
          />
          <button
            type="submit"
            className="mfa-button"
            disabled={loading}
          >
            {loading ? "Verifying..." : "Verify Code"}
          </button>

          <div className="mfa-back-link">
            <span onClick={() => navigate("/login")}>
              Back to login
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}
