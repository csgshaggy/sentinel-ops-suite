// /src/components/Breadcrumbs.jsx

import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Breadcrumbs.css";

export default function Breadcrumbs() {
  const location = useLocation();
  const path = location.pathname;

  // Split path into segments
  const segments = path.split("/").filter(Boolean);

  // ⭐ Explicit label overrides for deterministic breadcrumbs
  const LABEL_MAP = {
    admin: "Admin",
    dashboard: "Dashboard",
    security: "Security",
    users: "Users",
    "audit-logs": "Audit Logs",
    "session-metrics": "Session Metrics",

    // NEW
    settings: "Settings",
  };

  // Convert segment → readable label
  const formatLabel = (segment) => {
    if (LABEL_MAP[segment]) return LABEL_MAP[segment];

    return segment
      .replace(/-/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  // Build breadcrumb objects
  const crumbs = segments.map((segment, index) => {
    const url = "/" + segments.slice(0, index + 1).join("/");
    return {
      label: formatLabel(segment),
      url,
    };
  });

  // Special case: root or login
  if (path === "/" || path.startsWith("/login")) {
    return null;
  }

  return (
    <nav className="breadcrumbs">
      {crumbs.map((crumb, index) => (
        <span key={crumb.url} className="crumb">
          <Link to={crumb.url} className="crumb-link">
            {crumb.label}
          </Link>

          {index < crumbs.length - 1 && (
            <span className="crumb-separator">›</span>
          )}
        </span>
      ))}
    </nav>
  );
}
