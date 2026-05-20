// /src/pages/MFACode.jsx

import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { toast } from "../components/ToastManager.jsx";

import AuthLayout from "../layouts/AuthLayout.jsx";
import "./MFACode.css";

export default function MFACode() {
  const navigate = useNavigate();
  const { verifyMfa, mfaPending } = useAuth();

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);

  // Redirect if user hits /mfa without login
  useEffect(() => {
    if (!mfaPending) {
      navigate("/login", { replace: true });
    }
  }, [mfaPending, navigate]);

  // Autofocus MFA input
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!code.trim()) {
      toast.error("MFA code is required.");
      return;
    }

    setLoading(true);
    const result = await verifyMfa(code);
    setLoading(false);

    if (result === "success") {
      navigate("/", { replace: true });
      return;
    }

    toast.error("Invalid MFA code.");
  }

  return (
    <AuthLayout>
      <form className="mfa-card" onSubmit={handleSubmit}>
        <h2 className="mfa-title">Multi‑Factor Authentication</h2>
        <p className="mfa-subtitle">Enter the 6‑digit code from your authenticator</p>

        {/* MFA CODE FIELD — FLOATING LABEL */}
        <div className="float-field">
          <label className="float-label">
            <input
              ref={inputRef}
              type="text"
              className="float-input"
              maxLength={6}
              value={code}
              onChange={(e) => {
                const digitsOnly = e.target.value.replace(/\D/g, "");
                setCode(digitsOnly);
              }}
              disabled={loading}
              autoComplete="one-time-code"
              required
            />
            <span>MFA Code</span>
          </label>
        </div>

        {/* SUBMIT BUTTON */}
        <button type="submit" className="mfa-submit-btn" disabled={loading}>
          {loading ? "Verifying..." : "Verify Code"}
        </button>
      </form>
    </AuthLayout>
  );
}
