// File: /src/pages/settings/Security.jsx

import { useContext, useState, useEffect } from "react";
import axios from "../../utils/axiosInstance.js";
import { AuthContext } from "../../features/auth/AuthContext.jsx";
import "./Security.css";

export default function Security() {
  const { user, refreshUser } = useContext(AuthContext);

  const [sessions, setSessions] = useState([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [error, setError] = useState("");

  // ------------------------------------------------------------
  // Load Active Sessions (Unified Backend)
  // ------------------------------------------------------------
  const loadSessions = async () => {
    try {
      setLoadingSessions(true);
      const res = await axios.get("/api/sessions");
      setSessions(res.data.sessions || []);
    } catch (err) {
      setError("Failed to load active sessions.");
    } finally {
      setLoadingSessions(false);
    }
  };

  // ------------------------------------------------------------
  // Terminate Other Sessions
  // ------------------------------------------------------------
  const terminateOtherSessions = async () => {
    try {
      await axios.post("/api/sessions/terminate-others");
      loadSessions();
    } catch (err) {
      setError("Failed to terminate other sessions.");
    }
  };

  // ------------------------------------------------------------
  // Disable MFA
  // ------------------------------------------------------------
  const disableMFA = async () => {
    try {
      await axios.post("/api/mfa/disable");
      await refreshUser();
    } catch (err) {
      setError("Failed to disable MFA.");
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  return (
    <div className="security-container">
      <h1>Security</h1>

      {error && <p className="security-error">{error}</p>}

      {/* ------------------------------------------------------------
          Password Management
      ------------------------------------------------------------ */}
      <div className="security-card">
        <h2>Password</h2>
        <p>Update your password to keep your account secure.</p>
        <button
          className="security-button"
          onClick={() => (window.location.href = "/change-password")}
        >
          Change Password
        </button>
      </div>

      {/* ------------------------------------------------------------
          MFA Status (Unified Backend)
      ------------------------------------------------------------ */}
      <div className="security-card">
        <h2>Multi‑Factor Authentication</h2>

        {user?.mfa_enabled ? (
          <>
            <p>
              MFA is currently <strong>enabled</strong> on your account.
            </p>
            <button className="security-button danger" onClick={disableMFA}>
              Disable MFA
            </button>
          </>
        ) : (
          <>
            <p>
              MFA is <strong>not enabled</strong>. Enable it to increase
              security.
            </p>
            <button
              className="security-button"
              onClick={() => (window.location.href = "/mfa-setup")}
            >
              Enable MFA
            </button>
          </>
        )}
      </div>

      {/* ------------------------------------------------------------
          Active Sessions (Unified Backend)
      ------------------------------------------------------------ */}
      <div className="security-card">
        <h2>Active Sessions</h2>

        {loadingSessions ? (
          <p>Loading sessions...</p>
        ) : sessions.length === 0 ? (
          <p>No active sessions found.</p>
        ) : (
          <ul className="session-list">
            {sessions.map((s, idx) => (
              <li key={idx} className="session-item">
                <div>
                  <strong>Session ID:</strong> {s.session_id}
                  <br />
                  <strong>Created:</strong> {s.created_at}
                  <br />
                  <strong>Expires:</strong> {s.expires_at}
                </div>
              </li>
            ))}
          </ul>
        )}

        <button
          className="security-button danger"
          onClick={terminateOtherSessions}
        >
          Terminate Other Sessions
        </button>
      </div>

      {/* ------------------------------------------------------------
          Security Logs (Removed — Not Implemented in Unified Backend)
      ------------------------------------------------------------ */}
      <div className="security-card">
        <h2>Security Logs</h2>
        <p>Security logs are not yet implemented.</p>
      </div>
    </div>
  );
}
