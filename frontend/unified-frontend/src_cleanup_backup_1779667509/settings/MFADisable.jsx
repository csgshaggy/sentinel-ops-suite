// File: /src/pages/settings/MFADisable.jsx

import { useContext, useState, useCallback } from "react";
import axios from "../../utils/axiosInstance.js";
import { AuthContext } from "../../features/auth/AuthContext.jsx";
import "./MFADisable.css";

export default function MFADisable() {
  const { setUser } = useContext(AuthContext);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const disableMFA = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const res = await axios.post("/api/auth/mfa/disable", { code });

      if (res.data.success) {
        setUser((prev) => ({ ...prev, mfa_enabled: false }));
        window.location.href = "/security";
      } else {
        setError("Invalid code.");
      }
    } catch {
      setError("Failed to disable MFA.");
    } finally {
      setLoading(false);
    }
  }, [code, setUser]);

  return (
    <div className="mfa-disable-container">
      <h1>Disable MFA</h1>

      <p>Enter a valid MFA code to disable Multi‑Factor Authentication.</p>

      <input
        type="text"
        maxLength="6"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="mfa-disable-input"
      />

      <button
        className="mfa-disable-button danger"
        onClick={disableMFA}
        disabled={loading}
      >
        {loading ? "Disabling..." : "Disable MFA"}
      </button>

      {error && <p className="mfa-disable-error">{error}</p>}
    </div>
  );
}
