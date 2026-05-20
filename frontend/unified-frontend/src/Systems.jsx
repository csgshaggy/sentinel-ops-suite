/* Required global + component CSS */
import "./styles/panels.css";
import "./styles/tables.css";
import "./styles/icons.css";
import "./styles/animations.css";
import "./styles/buttons.css";
import "./styles/forms.css";

/* If you have a dedicated Systems.css, import it here */
// import "./styles/systems.css";

export default function Systems() {
  // Temporary static data — replace with API call later
  const systems = [
    { name: "Authentication Service", status: "online", version: "1.4.2", latency: "32ms" },
    { name: "User Directory", status: "online", version: "2.1.0", latency: "28ms" },
    { name: "Alert Engine", status: "degraded", version: "3.0.1", latency: "85ms" },
    { name: "Metrics Collector", status: "online", version: "1.9.8", latency: "41ms" },
    { name: "Notification Hub", status: "offline", version: "2.0.4", latency: "—" },
  ];

  const statusClass = (status) => {
    switch (status) {
      case "online":
        return "table-status low";
      case "degraded":
        return "table-status high";
      case "offline":
        return "table-status critical";
      default:
        return "table-status";
    }
  };

  return (
    <div className="page fade-in">
      {/* Overview Panel */}
      <div className="panel glass-panel">
        <div className="panel-header">
          <h2 className="panel-title">Systems Overview</h2>
        </div>

        <div className="panel-body">
          <div className="systems-overview-grid">
            <div className="overview-item">
              <span className="overview-label">Total Systems</span>
              <span className="overview-value">{systems.length}</span>
            </div>

            <div className="overview-item">
              <span className="overview-label">Online</span>
              <span className="overview-value">
                {systems.filter((s) => s.status === "online").length}
              </span>
            </div>

            <div className="overview-item">
              <span className="overview-label">Degraded</span>
              <span className="overview-value">
                {systems.filter((s) => s.status === "degraded").length}
              </span>
            </div>

            <div className="overview-item">
              <span className="overview-label">Offline</span>
              <span className="overview-value">
                {systems.filter((s) => s.status === "offline").length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Systems Table */}
      <div className="panel glass-panel" style={{ marginTop: "1.5rem" }}>
        <div className="panel-header">
          <h2 className="panel-title">System Status</h2>
        </div>

        <div className="panel-body">
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>System</th>
                  <th>Status</th>
                  <th>Version</th>
                  <th>Latency</th>
                </tr>
              </thead>

              <tbody>
                {systems.map((sys, idx) => (
                  <tr key={idx}>
                    <td>{sys.name}</td>
                    <td>
                      <span className={statusClass(sys.status)}>
                        {sys.status.toUpperCase()}
                      </span>
                    </td>
                    <td>{sys.version}</td>
                    <td>{sys.latency}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
