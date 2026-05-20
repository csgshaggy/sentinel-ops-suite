// /src/pages/ResetPassword.jsx

import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";
import { resetPassword } from "../api/auth";

import "../styles/auth/ResetPassword.css";
import logo from "../assets/SentinelOps.jpg";

export default function ResetPassword() {
  const navigate = useNavigate();
  const { token } = useParams();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (password !== confirm) {
      toast.error("Passwords do not match.");
      return;
    }

    setLoading(true);
    const res = await resetPassword(token, password);
    setLoading(false);

    if (res?.error) {
      toast.error(res.error);
      return;
    }

    toast.success("Password updated.");
    navigate("/login");
  }

  return (
    <AuthLayout>
      {/* Logo */}
      <div className="auth-logo-container">
        <img src={logo} className="auth-logo" alt="Sentinel Ops" />
      </div>

      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create New Password</h2>

        {/* NEW PASSWORD FIELD */}
        <div className="float-field">
          <label className="float-label">
            <input
              type="password"
              className="float-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="new-password"
              required
            />
            <span>New Password</span>
          </label>
        </div>

        {/* CONFIRM PASSWORD FIELD */}
        <div className="float-field">
          <label className="float-label">
            <input
              type="password"
              className="float-input"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              autoComplete="new-password"
              required
            />
            <span>Confirm Password</span>
          </label>
        </div>

        {/* SUBMIT BUTTON */}
        <button className="auth-btn" disabled={loading}>
          {loading ? "Updating..." : "Update Password"}
        </button>
      </form>
    </AuthLayout>
  );
}
