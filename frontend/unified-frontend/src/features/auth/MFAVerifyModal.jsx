// /src/features/auth/MFAVerifyModal.jsx
// ============================================================
// SentinelOps — Unified MFA Verification Modal
// - Works with new AuthContext.completeMfa()
// - Works with unified backend
// ============================================================

import { useState } from "react";
import { useAuth } from "./AuthContext.jsx";
import { toast } from "../../components/ToastManager.jsx";

export default function MFAVerifyModal({ userId, onComplete, onCancel }) {
  const { completeMfa } = useAuth();
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleVerify(e) {
    e.preventDefault();
    if (!userId) {
      toast.error("Missing MFA session.");
      return;
    }

    setLoading(true);
    const result = await completeMfa(userId);
    setLoading(false);

    if (result === "success") {
      onComplete?.();
      return;
    }

    toast.error("Invalid MFA code.");
  }

  return (
    <div className="mfa-modal-backdrop">
      <div className="mfa-modal">
        <h2>MFA Verification</h2>
        <p>Enter the 6‑digit code from your authenticator app.</p>

        <form onSubmit={handleVerify}>
          <input
            type="text"
            inputMode="numeric"
            maxLength={6}
            className="mfa-input"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            autoFocus
            disabled={loading}
          />

          <button type="submit" className="mfa-btn" disabled={loading}>
            {loading ? "Verifying..." : "Verify"}
          </button>

          <button
            type="button"
            className="mfa-cancel-btn"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
}
