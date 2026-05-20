// File: /src/pages/settings/RecoveryOptions.jsx

import { useState, useEffect, useCallback } from "react";
import axios from "../../utils/axiosInstance";
import "./RecoveryOptions.css";

export default function RecoveryOptions() {
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadRecovery = useCallback(async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/auth/recovery");
      setEmail(res.data.email || "");
      setPhone(res.data.phone || "");
    } catch {
      setError("Failed to load recovery options.");
    } finally {
      setLoading(false);
    }
  }, []);

  const saveRecovery = useCallback(
    async () => {
      try {
        setSaving(true);
        setError("");
        setSuccess("");

        await axios.post("/api/auth/recovery", {
          email,
          phone,
        });

        setSuccess("Recovery options updated.");
      } catch {
        setError("Failed to update recovery options.");
      } finally {
        setSaving(false);
      }
    },
    [email, phone]
  );

  useEffect(() => {
    // React 18 safe: schedule async loader in a microtask
    Promise.resolve().then(loadRecovery);
  }, [loadRecovery]);

  return (
    <div className="recovery-container">
      <h1>Recovery Options</h1>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <div className="recovery-field">
            <label>Recovery Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="recovery-field">
            <label>Recovery Phone</label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </div>

          <button
            className="recovery-button"
            onClick={saveRecovery}
            disabled={saving}
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>

          {error && <p className="recovery-error">{error}</p>}
          {success && <p className="recovery-success">{success}</p>}
        </>
      )}
    </div>
  );
}

