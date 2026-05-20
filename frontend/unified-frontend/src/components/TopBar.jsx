// /src/components/TopBar.jsx
import React from "react";
import UserMenu from "./UserMenu.jsx";   // ensure .jsx extension for Vite consistency
import "./TopBar.css";

export default function TopBar({ user }) {
  // Derive initials safely (matches new UserMenu.jsx)
  const initials =
    user?.initials ||
    (user?.name?.trim()
      ? user.name.charAt(0).toUpperCase()
      : user?.email
      ? user.email.charAt(0).toUpperCase()
      : "U");

  return (
    <header className="topbar topbar-zfix">
      {/* LEFT: reserved for breadcrumbs, status, etc. */}
      <div className="topbar-left" />

      {/* CENTER: layout balancer */}
      <div className="topbar-center" />

      {/* RIGHT: User Menu (portal-based dropdown) */}
      <div className="topbar-right">
        <UserMenu initials={initials} />
      </div>
    </header>
  );
}
