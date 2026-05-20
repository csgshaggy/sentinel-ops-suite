// ============================================================
// FILE: src/pages/Signup.jsx
// Full regeneration with MFA integration
// ============================================================

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import UnifiedAuthShell from "../components/auth/UnifiedAuthShell";
import "./Signup.css";

const Signup = () => {
  const navigate = useNavigate();

  // ----------------------------------------------------------
  // FORM STATE
  // ----------------------------------------------------------
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // ----------------------------------------------------------
  // UI STATE
  // ----------------------------------------------------------
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // ----------------------------------------------------------
  // MFA STATE
  // ----------------------------------------------------------
  const [mfaRequired, setMfaRequired] = useState(false);
  const [mfaQr, setMfaQr] = useState("");
  const [mfaSecret, setMfaSecret] = useState("");
  const [mfaCode, setMfaCode] = useState("");
  const [mfaError, setMfaError] = useState("");
  // ==========================================================
  // HANDLE SIGNUP SUBMIT
  // ==========================================================
  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      const res = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          username,
          password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.message || "Signup failed.");
        return;
      }

      // If backend says MFA is required, show QR + secret
      if (data.mfaRequired) {
        setMfaRequired(true);
        setMfaQr(data.qrCode);
        setMfaSecret(data.secret);
        return;
      }

      setSuccess(true);
    } catch (err) {
      setError("Network error during signup.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // HANDLE MFA VERIFICATION
  // ==========================================================
  const handleVerifyMfa = async () => {
    setMfaError("");

    try {
      const res = await fetch("/api/auth/verify-mfa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          code: mfaCode,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMfaError(data.message || "Invalid MFA code.");
        return;
      }

      setSuccess(true);
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setMfaError("Network error verifying MFA.");
    }
  };

  // ==========================================================
  // RENDER: MFA SETUP SCREEN
  // ==========================================================
  if (mfaRequired) {
    return (
      <UnifiedAuthShell title="Multi‑Factor Authentication Setup">
        <div className="signup-container">
          <p className="signup-instructions">
            Scan the QR code below with your authenticator app, then enter the 6‑digit code.
          </p>

          <div className="mfa-qr-wrapper">
            <img src={mfaQr} alt="MFA QR Code" className="mfa-qr" />
          </div>

          <p className="mfa-secret">Secret Key: {mfaSecret}</p>

          <input
            type="text"
            placeholder="Enter 6‑digit code"
            value={mfaCode}
            onChange={(e) => setMfaCode(e.target.value)}
            className="signup-input"
          />

          {mfaError && <p className="error-text">{mfaError}</p>}

          <button
            className="signup-button"
            onClick={handleVerifyMfa}
            disabled={loading}
          >
            {loading ? "Verifying..." : "Verify MFA"}
          </button>
        </div>
      </UnifiedAuthShell>
    );
  }
  // ==========================================================
  // RENDER: SUCCESS STATE
  // ==========================================================
  if (success) {
    return (
      <UnifiedAuthShell title="Signup Successful">
        <div className="signup-container">
          <p className="success-text">
            Account created successfully. Redirecting to login...
          </p>
        </div>
      </UnifiedAuthShell>
    );
  }

  // ==========================================================
  // RENDER: MAIN SIGNUP FORM
  // ==========================================================
  return (
    <UnifiedAuthShell title="Create Your Account">
      <form className="signup-container" onSubmit={handleSignup}>
        <p className="signup-instructions">
          Create your SentinelOps account to access the operator console.
        </p>

        {/* EMAIL */}
        <input
          type="email"
          placeholder="Email Address"
          className="signup-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        {/* USERNAME */}
        <input
          type="text"
          placeholder="Username"
          className="signup-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        {/* PASSWORD */}
        <input
          type="password"
          placeholder="Password"
          className="signup-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {/* CONFIRM PASSWORD */}
        <input
          type="password"
          placeholder="Confirm Password"
          className="signup-input"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        {/* ERROR */}
        {error && <p className="error-text">{error}</p>}

        {/* SUBMIT BUTTON */}
        <button className="signup-button" type="submit" disabled={loading}>
          {loading ? "Creating Account..." : "Sign Up"}
        </button>

        {/* LOGIN LINK */}
        <p className="signup-footer">
          Already have an account?{" "}
          <span
            className="signup-link"
            onClick={() => navigate("/login")}
          >
            Log in
          </span>
        </p>
      </form>
    </UnifiedAuthShell>
  );
};

export default Signup;
