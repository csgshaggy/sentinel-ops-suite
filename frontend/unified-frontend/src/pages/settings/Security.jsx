// File: /src/pages/settings/Security.jsx

import { useContext, useState, useEffect } from "react";
import axios from "../../utils/axiosInstance.js";
import { AuthContext } from "../../features/auth/AuthContext.jsx";
import "./Security.css";

export default function Security() {
  const { user } = useContext(AuthContext);

  const [sessions, setSessions] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [loadingLogs, setLoadingLogs] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------
  // Load Active Sessions
  // -----------------------------
  const loadSessions = async () => {
    try {
      setLoadingSessions(true);
      const res = await axios.get("/api/auth/sessions");
      setSessions(res.data.sessions || []);
    } catch (err) {
      setError("Failed to load active sessions.");
    } finally {
      setLoadingSessions(false);
    }
  };

  // -----------------------------
  // Load Security Logs
  // -----------------------------
  const loadLogs = async () => {
    try {
      setLoadingLogs(true);
      const res = await axios.get("/api/auth/security-logs");
      setLogs(res.data.logs || []);
    } catch (err) {
      setError("Failed to load security logs.");
    } finally {
      setLoadingLogs(false);
    }
  };

  // -----------------------------
  // Terminate Other Sessions
  // -----------------------------
  const terminateOtherSessions = async () => {
    try {
      await axios.post("/api/auth/sessions/terminate-others");
      loadSessions();
    } catch (err) {
      setError("Failed to terminate other sessions.");
    }
  };

  useEffect(() => {
    loadSessions();
    loadLogs();
  }, []);

  return (
    <div className="security-container">
      <h1>Security</h1>

      {error && <p className="security-error">{error}</p>}

      {/* -----------------------------
          Password Management
      ------------------------------ */}
      <div className="security-card">
        <h2>Password</h2>
        <p>Update your password to keep your account secure.</p>
        <button
          className="security-button"
          onClick={() =>
            (window.location.href = "/admin/security/change-password")
          }
        >
          Change Password
        </button>
      </div>

      {/* -----------------------------
          MFA Status
      ------------------------------ */}
      <div className="security-card">
        <h2>Multi‑Factor Authentication</h2>

        {user?.mfa_enabled ? (
          <>
            <p>
              MFA is currently <strong>enabled</strong> on your account.
            </p>
            <button
              className="security-button danger"
              onClick={() =>
                (window.location.href = "/admin/security/mfa-disable")
              }
            >
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
              onClick={() =>
                (window.location.href = "/admin/security/mfa-setup")
              }
            >
              Enable MFA
            </button>
          </>
        )}
      </div>

      {/* -----------------------------
          Active Sessions
      ------------------------------ */}
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
                  <strong>{s.device || "Unknown Device"}</strong>
                  <br />
                  IP: {s.ip}
                  <br />
                  Last Active: {s.last_active}
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

      {/* -----------------------------
          Security Logs
      ------------------------------ */}
      <div className="security-card">
        <h2>Security Logs</h2>

        {loadingLogs ? (
          <p>Loading logs...</p>
        ) : logs.length === 0 ? (
          <p>No security logs found.</p>
        ) : (
          <ul className="log-list">
            {logs.map((log, idx) => (
              <li key={idx} className="log-item">
                <strong>{log.action}</strong> — {log.timestamp}
                <br />
                {log.details}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
