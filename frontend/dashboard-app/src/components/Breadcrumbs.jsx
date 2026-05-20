import React from "react";
import { useLocation, Link } from "react-router-dom";
import "../styles/breadcrumbs.css";

export default function Breadcrumbs() {
  const location = useLocation();

  // Split path into segments
  const segments = location.pathname
    .split("/")
    .filter((seg) => seg.length > 0);

  // Build breadcrumb objects
  const crumbs = segments.map((seg, idx) => {
    const path = "/" + segments.slice(0, idx + 1).join("/");
    return { label: formatLabel(seg), path };
  });

  return (
    <div className="breadcrumbs">
      <Link to="/pelm" className="breadcrumb-link">
        Home
      </Link>

      {crumbs.map((crumb, idx) => (
        <span key={idx} className="breadcrumb-item">
          <span className="breadcrumb-separator">/</span>
          <Link to={crumb.path} className="breadcrumb-link">
            {crumb.label}
          </Link>
        </span>
      ))}
    </div>
  );
}

function formatLabel(seg) {
  return seg
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
