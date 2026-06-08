// /src/pages/MFASetup.jsx

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout.jsx";
import { toast } from "../components/ToastManager.jsx";
import apiClient from "../api/apiClient.js";

import "../styles/auth/MFASetup.css";
import logo from "../assets/SentinelOps.jpg";

export default function MFASetup() {
  const navigate = useNavigate();

  const [qrUri, setQrUri] = useState("");
  const [secret, setSecret] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------
  // Load MFA setup (secret + provisioning URI)
  // ------------------------------------------------------------
  useEffect(() => {
    async function load() {
      try {
        const res = await apiClient.get("/api/mfa/setup");

        setSecret(res.data.secret);
        setQrUri(res.data.provisioning_uri);
      } catch (err) {
        toast.error("Failed to load MFA setup");
      }
    }
    load();
  }, []);

  // ------------------------------------------------------------
  // Verify + Enable MFA
  // ------------------------------------------------------------
  async function handleVerify(e) {
    e.preventDefault();
    setLoading(true);

    try {
      await apiClient.post("/api/mfa/enable", { code });

      toast.success("MFA enabled.");
      navigate("/");
    } catch (err) {
      toast.error("Invalid MFA code");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout>
      {/* Glowing shield pulse wrapper (kept from your version) */}
      <div className="auth-logo-container">
        <img src={logo} className="auth-logo" alt="Sentinel Ops" />
      </div>

      <div className="auth-card">
        <h2>Set Up MFA</h2>
        <p className="auth-subtitle">
          Scan the QR code with your authenticator app
        </p>

        {/* QR Code (generated from provisioning URI) */}
        {qrUri && (
          <img
            src={`https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(
              qrUri
            )}`}
            className="mfa-qr"
            alt="MFA QR Code"
          />
        )}

        {/* Secret (manual entry) */}
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
