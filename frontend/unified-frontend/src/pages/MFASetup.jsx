// /src/pages/MFASetup.jsx

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";
import { getMfaSetup, verifyMfaSetup } from "../api/auth";

import "../styles/auth/MFASetup.css";
import logo from "../assets/SentinelOps.jpg";

export default function MFASetup() {
  const navigate = useNavigate();

  const [qr, setQr] = useState("");
  const [secret, setSecret] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      const res = await getMfaSetup();
      if (res?.error) {
        toast.error(res.error);
        return;
      }
      setQr(res.qr);
      setSecret(res.secret);
    }
    load();
  }, []);

  async function handleVerify(e) {
    e.preventDefault();
    setLoading(true);

    const res = await verifyMfaSetup(code);
    setLoading(false);

    if (res?.error) {
      toast.error(res.error);
      return;
    }

    toast.success("MFA enabled.");
    navigate("/");
  }

  return (
    <AuthLayout>
      {/* Added glowing shield pulse wrapper */}
      <div className="auth-logo-container">
        <img src={logo} className="auth-logo" alt="Sentinel Ops" />
      </div>

      <div className="auth-card">
        <h2>Set Up MFA</h2>
        <p className="auth-subtitle">Scan the QR code with your authenticator app</p>

        <img src={qr} className="mfa-qr" alt="MFA QR Code" />

        <p className="mfa-secret">{secret}</p>

        <form onSubmit={handleVerify}>
          <input
            type="text"
            className="auth-input"
            placeholder="Enter 6‑digit code"
            maxLength="6"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
          />

          <button className="auth-btn" disabled={loading}>
            {loading ? "Verifying..." : "Verify & Enable"}
          </button>
        </form>
      </div>
    </AuthLayout>
  );
}
