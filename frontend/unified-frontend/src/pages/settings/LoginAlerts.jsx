// File: /src/pages/settings/LoginAlerts.jsx

import { useState, useEffect, useCallback } from "react";
import axios from "../../utils/axiosInstance";
import "./LoginAlerts.css";

export default function LoginAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadAlerts = useCallback(async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/auth/login-alerts");
      setAlerts(res.data.alerts || []);
      setEnabled(res.data.enabled || false);
    } catch {
      setError("Failed to load login alerts.");
    } finally {
      setLoading(false);
    }
  }, []);

  const saveSettings = useCallback(async () => {
    try {
      setSaving(true);
      setError("");
      setSuccess("");

      await axios.post("/api/auth/login-alerts/settings", {
        enabled,
      });

      setSuccess("Login alert settings updated.");
    } catch {
      setError("Failed to update settings.");
    } finally {
      setSaving(false);
    }
  }, [enabled]);

  useEffect(() => {
    // React 18 safe: schedule async loader in a microtask
    Promise.resolve().then(loadAlerts);
  }, [loadAlerts]);

  return (
    <div className="login-alerts-container">
      <h1>Login Alerts</h1>

      <p>
        Receive alerts when a new login occurs on your account. This helps detect
        unauthorized access quickly.
      </p>

      <div className="login-alerts-toggle">
        <label>
          <input
            type="checkbox"
            checked={enabled}
            onChange={(e) => setEnabled(e.target.checked)}
          />
          Enable Login Alerts
        </label>
      </div>

      <button
        className="login-alerts-button"
        onClick={saveSettings}
        disabled={saving}
      >
        {saving ? "Saving..." : "Save Settings"}
      </button>

      {error && <p className="login-alerts-error">{error}</p>}
      {success && <p className="login-alerts-success">{success}</p>}

      <h2>Recent Login Activity</h2>

      {loading ? (
        <p>Loading...</p>
      ) : alerts.length === 0 ? (
        <p>No recent login alerts.</p>
      ) : (
        <ul className="login-alerts-list">
          {alerts.map((alert, idx) => (
            <li key={idx} className="login-alert-item">
              <strong>{alert.event}</strong>
              <br />
              {alert.timestamp} — IP: {alert.ip}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
