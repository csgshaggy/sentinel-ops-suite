// /src/pages/Mfa.jsx

import { useState } from "react";                     // ✅ FIX: required hook
import { useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { toast } from "../components/ToastManager.jsx";

import "./Login.css"; // Reuse the same styling
import "../styles/theme.css";
import logo from "../assets/SentinelOps.jpg";

export default function Mfa() {
  const navigate = useNavigate();
  const { verifyMfa,  } = useAuth();

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const result = await verifyMfa(code);

    if (result === "success") {
      navigate("/dashboard");   // <-- FIXED
      return;
    }

    toast.error("Invalid MFA code.");
    setLoading(false);
  }

  // If user hits /mfa without pending MFA → redirect to login
  if (!) {
    navigate("/login");
    return null;
  }

  return (
    <div className="login-wrapper">
      <div className="login-card glass">
        <img src={logo} alt="SentinelOps" className="login-logo" />

        <h2 className="text-glow">Multi‑Factor Authentication</h2>

        <form className="login-form" onSubmit={handleSubmit}>
          <p className="mfa-text">Enter your 6‑digit authentication code</p>

          <input
            type="text"
            placeholder="123456"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
            maxLength={6}
            required
            autoComplete="one-time-code"
          />

          <button type="submit" disabled={loading}>
            {loading ? "Verifying..." : "Verify Code"}
          </button>
        </form>
      </div>
    </div>
  );
}
