// src/components/layout/Breadcrumbs.jsx

import { useLocation, Link } from "react-router-dom";

export default function Breadcrumbs() {
  const location = useLocation();

  // Split path into segments
  const segments = location.pathname
    .split("/")
    .filter(Boolean);

  // Convert segment names into readable labels
  const formatLabel = (segment) => {
    return segment
      .replace(/-/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  // Build breadcrumb paths
  const paths = segments.map((_, idx) => {
    return "/" + segments.slice(0, idx + 1).join("/");
  });

  return (
    <div className="breadcrumb">
      <Link to="/dashboard" className="breadcrumb-root">
        Sentinel Ops
      </Link>

      {segments.map((segment, idx) => (
        <span key={idx} className="breadcrumb-segment">
          <span className="breadcrumb-separator">›</span>
          <Link to={paths[idx]}>
            {formatLabel(segment)}
          </Link>
        </span>
      ))}
    </div>
  );
}
