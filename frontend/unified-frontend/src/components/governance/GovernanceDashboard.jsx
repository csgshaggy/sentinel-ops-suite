import React from "react";
import "./GovernanceDashboard.css";

const GovernanceDashboard = () => {
  // Placeholder data – will be replaced by KPI logic + API wiring
  const kpis = [
    { label: "Compliance Coverage", value: "92%" },
    { label: "Open Governance Actions", value: "14" },
    { label: "SLA Drift (Last 30d)", value: "3.2%" },
    { label: "Policy Exceptions", value: "7" },
  ];

  const policies = [
    { name: "Access Control Policy", status: "Active", owner: "Security" },
    { name: "Data Retention Policy", status: "Review Due", owner: "Compliance" },
  ];

  const reviews = [
    { name: "Quarterly Access Review", status: "In Progress", owner: "IAM" },
    { name: "Vendor Risk Review", status: "Scheduled", owner: "Risk" },
  ];

  const exceptions = [
    { name: "Prod DB Access Exception", status: "Approved", owner: "Security" },
    { name: "Legacy App Whitelist", status: "Pending Review", owner: "Ops" },
  ];

  const hasActionRequired = true;

  return (
    <div className="governance-dashboard">
      {/* KPI Tiles */}
      <div className="kpi-grid">
        {kpis.map((kpi, idx) => (
          <div key={idx} className="kpi-tile">
            <div className="kpi-label">{kpi.label}</div>
            <div className="kpi-value">{kpi.value}</div>
          </div>
        ))}
      </div>

      {/* Alert Banner */}
      {hasActionRequired && (
        <div className="gov-alert">
          Action required: Review pending governance exceptions and open actions.
        </div>
      )}

      {/* Policies Section */}
      <div className="section-block">
        <div className="section-title">Policies</div>
        <table className="gov-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {policies.map((p, idx) => (
              <tr key={idx}>
                <td>{p.name}</td>
                <td>{p.status}</td>
                <td>{p.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Reviews Section */}
      <div className="section-block">
        <div className="section-title">Reviews</div>
        <table className="gov-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {reviews.map((r, idx) => (
              <tr key={idx}>
                <td>{r.name}</td>
                <td>{r.status}</td>
                <td>{r.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Exceptions Section */}
      <div className="section-block">
        <div className="section-title">Exceptions</div>
        <table className="gov-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {exceptions.map((e, idx) => (
              <tr key={idx}>
                <td>{e.name}</td>
                <td>{e.status}</td>
                <td>{e.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default GovernanceDashboard;
