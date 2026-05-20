// =====================================================================
// SSRF Command Console — Metric Card Component
// =====================================================================

export default function MetricCard({ label, value }) {
  return (
    <div
      className="panel"
      style={{
        padding: "1.5rem",
        textAlign: "center",
        minWidth: "180px",
        flex: "1",
      }}
    >
      <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{value}</div>
      <div className="text-muted" style={{ marginTop: "0.5rem" }}>
        {label}
      </div>
    </div>
  );
}
