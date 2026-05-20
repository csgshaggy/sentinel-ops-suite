import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";
import { verifyMfa } from "../api/auth";

import "../styles/auth/MFA.css";
import logo from "../assets/SentinelOps.jpg";

export default function MFA() {
  const navigate = useNavigate();
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const res = await verifyMfa(code);
    setLoading(false);

    if (res?.error) {
      toast.error(res.error);
      return;
    }

    toast.success("MFA verified.");
    navigate("/");
  }

  return (
    <AuthLayout>
      {/* Added glowing shield pulse wrapper */}
      <div className="auth-logo-container">
        <img src={logo} className="auth-logo" alt="Sentinel Ops" />
      </div>

      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>MFA Verification</h2>
        <p className="auth-subtitle">Enter your 6‑digit code</p>

        <input
          type="text"
          className="auth-input"
          maxLength="6"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          required
        />

        <button className="auth-btn" disabled={loading}>
          {loading ? "Verifying..." : "Verify"}
        </button>
      </form>
    </AuthLayout>
  );
}
