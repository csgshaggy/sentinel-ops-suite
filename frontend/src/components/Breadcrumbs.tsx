// =====================================================================
// SSRF Command Console — Breadcrumbs
// Dynamic route-based breadcrumbs • Theme-compatible
// =====================================================================

import { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

import { useLayout } from "../context/LayoutContext";

export default function Breadcrumbs() {
  const location = useLocation();
  const { breadcrumbs, setBreadcrumbs } = useLayout();

  useEffect(() => {
    const parts = location.pathname.split("/").filter(Boolean);

    const mapped = parts.map((part, idx) => {
      const label = part.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()) || "Home";

      return {
        label,
        path: "/" + parts.slice(0, idx + 1).join("/"),
      };
    });

    setBreadcrumbs(mapped);
  }, [location.pathname, setBreadcrumbs]);

  if (!breadcrumbs.length) return null;

  return (
    <nav className="breadcrumbs">
      {breadcrumbs.map((b, idx) => (
        <span key={b.path}>
          {idx > 0 && <span className="breadcrumbs-sep">/</span>}
          <Link to={b.path}>{b.label}</Link>
        </span>
      ))}
    </nav>
  );
}
