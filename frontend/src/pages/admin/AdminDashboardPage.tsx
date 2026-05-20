export default function AdminDashboardPage() {
  return (
    <div>
      <h2>Admin Dashboard</h2>

      <div className="dashboard-grid">
        <div className="tile">
          <h3>Active Sessions</h3>
          <p>3</p>
        </div>

        <div className="tile">
          <h3>Alerts</h3>
          <p>0</p>
        </div>

        <div className="tile">
          <h3>System Health</h3>
          <p>OK</p>
        </div>
      </div>
    </div>
  );
}
