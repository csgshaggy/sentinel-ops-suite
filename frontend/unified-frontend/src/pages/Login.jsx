// /src/pages/Login.jsx

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";

import { useAuth } from "../features/auth/AuthContext.jsx";
import logo from "../assets/SentinelOps.jpg";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const { login: authLogin, mfaPending } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // iOS viewport fix
  useEffect(() => {
    const setVH = () => {
      document.documentElement.style.setProperty(
        "--vh",
        `${window.innerHeight * 0.01}px`
      );
    };
    setVH();
    window.addEventListener("resize", setVH);
    return () => window.removeEventListener("resize", setVH);
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const result = await authLogin(username, password);
    setLoading(false);

    if (result === "error") {
      // AuthContext already showed a toast; nothing else to do
      return;
    }

    if (result === "mfa_required" || mfaPending) {
      navigate("/mfa");
      return;
    }

    if (result === "success") {
      // AuthContext has set `user`; ProtectedRoute will now pass
      toast.success("Welcome back.");
      navigate("/admin");
      return;
    }

    // Fallback (shouldn't normally hit)
    toast.error("Unexpected login response.");
  }

  return (
    <AuthLayout>
      <div className="login-logo-container">
        <img src={logo} alt="Sentinel Ops Logo" className="login-logo" />
      </div>

      <form className="login-form" onSubmit={handleSubmit}>
        {/* USERNAME FIELD */}
        <div className="login-field">
          <label className="login-label" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            type="text"
            className="login-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </div>

        {/* PASSWORD FIELD */}
        <div className="login-field">
          <label className="login-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="login-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </div>

        {/* SUBMIT BUTTON */}
        <button type="submit" className="login-btn" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </button>

        <div className="login-footer">
          <a onClick={() => navigate("/reset-password-request")}>
            Forgot Password?
          </a>
        </div>
      </form>
    </AuthLayout>
  );
}
