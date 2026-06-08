// /src/pages/Profile/components/ProfileBreadcrumbs.jsx
// SentinelOps — Profile Breadcrumbs (Neon‑Glassy)

import { Link } from "react-router-dom";
import "./ProfileBreadcrumbs.css";

export default function ProfileBreadcrumbs({ path = [] }) {
  if (!Array.isArray(path) || path.length === 0) return null;

  return (
    <nav className="profile-breadcrumbs" aria-label="Breadcrumb">
      {path.map((segment, idx) => {
        const isLast = idx === path.length - 1;

        return (
          <span key={idx} className="breadcrumb-segment">
            {!isLast ? (
              <Link to={`/${segment.toLowerCase()}`} className="breadcrumb-link">
                {segment}
              </Link>
            ) : (
              <span className="breadcrumb-current">{segment}</span>
            )}

            {!isLast && <span className="breadcrumb-separator">/</span>}
          </span>
        );
      })}
    </nav>
  );
}
