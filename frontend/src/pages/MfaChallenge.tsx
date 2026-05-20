import React, { useState } from "react";
import "./Login.css";

const MfaChallenge: React.FC = () => {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const username = localStorage.getItem("pending_username");

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("/auth/mfa/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, code }),
      });

      if (!res.ok) {
        throw new Error("Invalid MFA code");
      }

      const data = await res.json();
      localStorage.removeItem("pending_username");
      localStorage.setItem("access_token", data.access_token);

      // ROLE‑BASED REDIRECT
      if (data.role === "admin") {
        window.location.href = "/admin";
      } else {
        window.location.href = "/dashboard";
      }
    } catch (err: any) {
      setError(err.message || "MFA verification failed");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">MFA Verification</h2>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleVerify}>
          <label className="login-label">Enter MFA Code</label>
          <input
            type="text"
            className="login-input"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="123456"
            required
          />

          <button className="login-button" type="submit">
            Verify
          </button>
        </form>
      </div>
    </div>
  );
};

export default MfaChallenge;
