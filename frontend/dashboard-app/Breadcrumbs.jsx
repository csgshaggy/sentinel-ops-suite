import React from "react";
import { useLocation, Link } from "react-router-dom";

import "./../styles/breadcrumbs.css";

export default function Breadcrumbs() {
  const location = useLocation();

  // Remove leading slash and split into segments
  const segments = location.pathname
    .replace(/^\/+/, "")
    .split("/")
    .filter(Boolean);

  // Build breadcrumb objects
  const crumbs = segments.map((seg, index) => {
    const path = "/" + segments.slice(0, index + 1).join("/");

    // Convert segment to readable label
    const label = seg
      .replace(/-/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());

    return { label, path };
  });

  return (
    <div className="breadcrumbs">
      <Link to="/" className="breadcrumb-segment">
        Dashboard
      </Link>

      {crumbs.map((crumb, idx) => (
        <React.Fragment key={crumb.path}>
          <span className="breadcrumb-divider">/</span>

          {idx === crumbs.length - 1 ? (
            <span className="breadcrumb-segment active">
              {crumb.label}
            </span>
          ) : (
            <Link to={crumb.path} className="breadcrumb-segment">
              {crumb.label}
            </Link>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
