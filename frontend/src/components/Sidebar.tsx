import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const Sidebar = () => {
  const { user } = useAuth();
  const role = user?.role || "user";

  const baseLinks = [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/alerts", label: "Alerts" },
    { to: "/system-health", label: "System Health" },
    { to: "/workflow-runs", label: "Workflow Runs" },
    { to: "/health-trend", label: "Health Trend" },
    { to: "/health-predict", label: "Health Predict" },
    { to: "/makefile-health", label: "Makefile Health" },
    { to: "/repo-health", label: "Repo Health" },
    { to: "/router-drift", label: "Router Drift" },
    { to: "/plugins", label: "Plugins" },
    { to: "/observability", label: "Observability" },
  ];

  const adminLinks = [
    { to: "/pelm-dashboard", label: "PELM Dashboard" },
    { to: "/pelm-console", label: "PELM Console" },
    { to: "/pelm-status", label: "PELM Status" },
    { to: "/pelm-tools", label: "PELM Tools" },
  ];

  const links = role === "admin" ? [...baseLinks, ...adminLinks] : baseLinks;

  return (
    <div style={{ width: "240px", padding: "1rem", background: "#111", color: "#fff" }}>
      <h2 style={{ marginBottom: "1rem" }}>Sentinel Ops</h2>
      <nav>
        {links.map((link) => (
          <div key={link.to} style={{ marginBottom: "0.75rem" }}>
            <Link style={{ color: "#0ff" }} to={link.to}>
              {link.label}
            </Link>
          </div>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
