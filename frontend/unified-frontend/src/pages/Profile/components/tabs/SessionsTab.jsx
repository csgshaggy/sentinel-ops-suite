import { useAvatarContext } from "../../context/AvatarContext";
// /src/pages/Profile/components/tabs/SessionsTab.jsx
// SentinelOps — Sessions Tab (Safe + Placeholder Mode)

import "./SessionsTab.css";

export default function SessionsTab({ loading, sessions, onRefresh }) {
  const { avatarUrl } = useAvatarContext();
  // ⭐ SAFETY: ensure sessions is always an array
  const safeSessions = Array.isArray(sessions) ? sessions : [];

  if (loading) {
    return (
      <div className="sessions-skeleton">
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
      </div>
    );
  }

  // ⭐ If backend endpoint doesn't exist → show placeholder
  if (!Array.isArray(sessions)) {
    return (
      <div className="sessions-tab-container">
        <div className="sessions-header">
          <h3>Active Sessions</h3>
          <button className="btn-secondary" onClick={onRefresh}>
            Refresh
          </button>
        </div>

        <div className="sessions-empty glass">
          Session API not implemented on backend.
        </div>
      </div>
    );
  }

  return (
    <div className="sessions-tab-container">
      <div className="sessions-header">
        <h3>Active Sessions</h3>
        <button className="btn-secondary" onClick={onRefresh}>
          Refresh
        </button>
      </div>

      {safeSessions.length === 0 ? (
        <div className="sessions-empty glass">
          No active sessions found.
        </div>
      ) : (
        <table className="sessions-table glass">
          <thead>
            <tr>
              <th>IP Address</th>
              <th>Device</th>
              <th>Location</th>
              <th>Last Active</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {safeSessions.map((s, idx) => (
              <tr key={idx}>
                <td>{s.ip || "—"}</td>
                <td>{s.user_agent || "Unknown"}</td>
                <td>{s.location || "—"}</td>
                <td>
                  {s.last_active
                    ? new Date(s.last_active).toLocaleString()
                    : "—"}
                </td>
                <td>
                  <button className="btn-danger btn-small">
                    Terminate
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
