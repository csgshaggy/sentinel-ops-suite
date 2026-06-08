// /src/pages/Login.jsx

import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import "./Login.css";
import logo from "../assets/SentinelOps.jpg";

export default function Login() {
  const { login, completeMfa, mfaUserId } = useAuth();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const redirectTo = searchParams.get("redirectTo") || "/dashboard";

  // Form state
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mfaCode, setMfaCode] = useState("");

  // UX state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------
  // Handle Login
  // -----------------------------
  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await login(username, password);

      if (res?.status === "mfa_required") {
        setLoading(false);
        return;
      }

      if (res?.status === "success") {
        navigate(redirectTo, { replace: true });
        return;
      }

      // fallback error
      setError("Invalid username or password.");
    } catch (err) {
      setError("Login failed. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Handle MFA
  // -----------------------------
  const handleMfa = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await completeMfa(mfaCode);

      if (result === "success") {
        navigate(redirectTo, { replace: true });
        return;
      }

      setError("Invalid MFA code.");
    } catch (err) {
      setError("MFA verification failed.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-layout">
      {/* ----------------------------- */}
      {/* Logo */}
      {/* ----------------------------- */}
      <div className="login-logo-container">
        <img
          src={logo}
          alt="Sentinel Ops"
          className="login-logo"
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = "/assets/fallback-logo.png";
          }}
        />
      </div>

      {/* ----------------------------- */}
      {/* Login Panel */}
      {/* ----------------------------- */}
      <div className="login-form glass-panel">
        <h2>Sign In</h2>
        <p className="login-subtitle">Access your Sentinel Ops Console</p>

        {/* Error Message */}
        {error && <div className="login-error">{error}</div>}

        {/* ----------------------------- */}
        {/* Username + Password */}
        {/* ----------------------------- */}
        {!mfaUserId && (
          <form onSubmit={handleLogin}>
            <div className="login-field">
              <label className="login-label">
                Username<span className="label-spacer" />
              </label>
              <input
                className="login-input"
                type="text"
                value={username}
                autoComplete="username"
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
                required
                disabled={loading}
              />
            </div>

            <div className="login-field">
              <label className="login-label">
                Password<span className="label-spacer" />
              </label>
              <input
                className="login-input"
                type="password"
                value={password}
                autoComplete="current-password"
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? "Signing in..." : "Login"}
            </button>
          </form>
        )}

        {/* ----------------------------- */}
        {/* MFA Step */}
        {/* ----------------------------- */}
        {mfaUserId && (
          <form onSubmit={handleMfa}>
            <div className="login-field">
              <label className="login-label">
                MFA Code<span className="label-spacer" />
              </label>
              <input
                className="login-input"
                type="text"
                value={mfaCode}
                autoComplete="one-time-code"
                onChange={(e) => setMfaCode(e.target.value)}
                autoFocus
                required
                disabled={loading}
              />
            </div>

            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? "Verifying..." : "Verify MFA"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
