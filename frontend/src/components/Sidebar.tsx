import React from "react";
import { Link, useLocation } from "react-router-dom";

const navItems = [
  // ---------------------------------------------------------
  // Core Dashboard
  // ---------------------------------------------------------
  {
    id: "dashboard",
    label: "Dashboard",
    icon: "📊",
    route: "/",
  },

  // ---------------------------------------------------------
  // Health & Observability
  // ---------------------------------------------------------
  {
    id: "health-score",
    label: "Health Score",
    icon: "💠",
    route: "/health-score",
  },
  {
    id: "health-trend",
    label: "Health Trend",
    icon: "📈",
    route: "/health-trend",
  },
  {
    id: "health-predict",
    label: "Predictive Health",
    icon: "🔮",
    route: "/health-predict",
  },
  {
    id: "observability",
    label: "Observability",
    icon: "🛰️",
    route: "/observability",
  },

  // ---------------------------------------------------------
  // Anomalies & Alerts
  // ---------------------------------------------------------
  {
    id: "anomaly-correlation",
    label: "Anomaly Correlation",
    icon: "🧩",
    route: "/anomaly-correlation",
  },
  {
    id: "alerts",
    label: "Alerts",
    icon: "🚨",
    route: "/alerts",
  },

  // ---------------------------------------------------------
  // Governance
  // ---------------------------------------------------------
  {
    id: "makefile-dashboard",
    label: "Makefile Dashboard",
    icon: "🧱",
    route: "/makefile-dashboard",
  },

  // ---------------------------------------------------------
  // PELM
  // ---------------------------------------------------------
  {
    id: "pelm-health",
    label: "PELM Health",
    icon: "🩺",
    route: "/pelm-health",
  },
  {
    id: "pelm-stream",
    label: "PELM Stream",
    icon: "📡",
    route: "/pelm-stream",
  },
  {
    id: "pelm-console",
    label: "PELM Console",
    icon: "🛡️",
    route: "/pelm-console",
  },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div
      style={{
        width: "240px",
        background: "#1e1e1e",
        color: "#fff",
        padding: "20px 0",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      <h2 style={{ paddingLeft: 20, marginBottom: 20 }}>SSRF Console</h2>

      {navItems.map((item) => {
        const active = location.pathname === item.route;

        return (
          <Link
            key={item.id}
            to={item.route}
            style={{
              padding: "12px 20px",
              display: "flex",
              alignItems: "center",
              textDecoration: "none",
              color: active ? "#00eaff" : "#fff",
              background: active ? "#333" : "transparent",
              fontWeight: active ? "bold" : "normal",
            }}
          >
            <span style={{ marginRight: 10 }}>{item.icon}</span>
            {item.label}
          </Link>
        );
      })}
    </div>
  );
}
