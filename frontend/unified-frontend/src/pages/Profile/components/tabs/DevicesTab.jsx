// /src/pages/Profile/components/tabs/DevicesTab.jsx
// SentinelOps — Devices Tab (Trusted Devices + Revocation, Null‑Safe)

import "./DevicesTab.css";

export default function DevicesTab({ loading, devices, onRefresh }) {
  // ⭐ Null-safe fallback
  const safeDevices = Array.isArray(devices) ? devices : [];

  if (loading) {
    return (
      <div className="devices-skeleton">
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
      </div>
    );
  }

  return (
    <div className="devices-tab-container">
      <div className="devices-header">
        <h3>Trusted Devices</h3>
        <button className="btn-secondary" onClick={onRefresh}>
          Refresh
        </button>
      </div>

      {safeDevices.length === 0 ? (
        <div className="devices-empty glass">
          No trusted devices found.
        </div>
      ) : (
        <table className="devices-table glass">
          <thead>
            <tr>
              <th>Device</th>
              <th>IP Address</th>
              <th>Last Seen</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {safeDevices.map((d, idx) => (
              <tr key={idx}>
                <td>{d.device_name || d.name || "Unknown Device"}</td>
                <td>{d.ip || "—"}</td>
                <td>
                  {d.last_seen || d.last_used
                    ? new Date(d.last_seen || d.last_used).toLocaleString()
                    : "—"}
                </td>
                <td>
                  <button className="btn-danger btn-small">
                    Revoke
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
