import { useState } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../ToastManager.jsx";

export default function MFAVerifyModal({ userId, onSuccess }) {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!code || code.length < 6) {
      toast.error("Enter your 6-digit code");
      return;
    }

    setLoading(true);

    try {
      await apiClient.post("/api/mfa/verify", {
        user_id: userId,
        code,
      });

      toast.success("MFA verified");
      onSuccess(); // continue login flow
    } catch (err) {
      toast.error("Invalid MFA code");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal glass">
        <h2 className="text-glow">Multi‑Factor Authentication</h2>

        <p className="muted">
          Enter the 6‑digit code from your authenticator app.
        </p>

        <input
          type="text"
          maxLength={6}
          className="input"
          placeholder="123456"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{
            textAlign: "center",
            letterSpacing: "4px",
            fontSize: "1.4rem",
            marginTop: "16px",
          }}
        />

        <button
          className="btn-primary"
          onClick={verify}
          disabled={loading}
          style={{ marginTop: "20px", width: "100%" }}
        >
          {loading ? "Verifying..." : "Verify"}
        </button>
      </div>
    </div>
  );
}
