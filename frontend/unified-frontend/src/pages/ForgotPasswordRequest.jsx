// /src/pages/ForgotPasswordRequest.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";
import { requestPasswordReset } from "../api/auth";

import "../styles/auth/ForgotPassword.css";
import logo from "../assets/SentinelOps.jpg";

export default function ForgotPasswordRequest() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const res = await requestPasswordReset(email);
    setLoading(false);

    if (res?.error) {
      toast.error(res.error);
      return;
    }

    toast.success("Password reset link sent.");
    navigate("/login");
  }

  return (
    <AuthLayout>
      <img src={logo} className="auth-logo" alt="Sentinel Ops" />

      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Reset Password</h2>
        <p className="auth-subtitle">Enter your email to continue</p>

        <input
          type="email"
          className="auth-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button className="auth-btn" disabled={loading}>
          {loading ? "Sending..." : "Send Reset Link"}
        </button>

        <div className="auth-footer">
          <a onClick={() => navigate("/login")}>Back to Login</a>
        </div>
      </form>
    </AuthLayout>
  );
}
