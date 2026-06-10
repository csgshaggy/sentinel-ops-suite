import { useAvatarContext } from "../../context/AvatarContext";
import React, { memo, useState, useEffect } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";

import {
  LayoutDashboard,
  ShieldCheck,
  Users,
  FileSearch,
  Settings,
} from "lucide-react";

import "./Sidebar.css";

const sectionIds = [
  "overview",
  "backend-status",
  "user-identity",
  "session-info",
  "environment",
  "plugin-registry",
  "sandbox-logs",
];

function Sidebar() {
  const { avatarUrl } = useAvatarContext();
  const { user, loading, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const [activeSection, setActiveSection] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  if (loading) return null;
  if (!user) return null;

  const roles = user.roles || [];
  const isAdmin = roles.includes("admin");

  /* ---------------------------------------------
     DASHBOARD SECTION SCROLL TRACKING
  --------------------------------------------- */
  useEffect(() => {
    if (location.pathname !== "/dashboard") return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      {
        rootMargin: "-40% 0px -55% 0px",
        threshold: 0.1,
      }
    );

    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [location.pathname]);

  /* ---------------------------------------------
     LOGOUT HANDLER
  --------------------------------------------- */
  const handleLogout = async () => {
    try {
      if (logout) await logout();
    } catch (err) {
      console.error("Logout failed:", err);
    } finally {
      navigate("/login", { replace: true });
    }
  };

  /* ---------------------------------------------
     ACTIVE CLASS RESOLUTION
  --------------------------------------------- */
  const getClass = (isRouteActive, sectionId) => {
    if (location.pathname === "/dashboard") {
      return activeSection === sectionId
        ? "sidebar-item active-glow"
        : "sidebar-item";
    }
    return isRouteActive ? "sidebar-item active" : "sidebar-item";
  };

  return (
    <>
      {/* MOBILE TOGGLE */}
      <button className="sidebar-toggle" onClick={() => setOpen(true)}>
        ☰
      </button>

      {/* MOBILE BACKDROP */}
      {open && (
        <div className="sidebar-backdrop" onClick={() => setOpen(false)} />
      )}

      {/* SIDEBAR */}
      <aside className={`sidebar ${open ? "open" : ""}`}>
        <div className="sidebar-sections">

          {/* ⭐ AVATAR HEADER (required for global avatar system) */}
          <div className="sidebar-avatar-block">
            <img
              src={avatarUrl}
              alt="User avatar"
              className="sidebar-avatar"
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "50%",
                objectFit: "cover",
                marginBottom: "12px",
              }}
            />
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">
                {user.full_name || user.username || "User"}
              </div>
              <div className="sidebar-user-email">
                {user.email || ""}
              </div>
            </div>
          </div>

          {/* GENERAL SECTION */}
          <div className="sidebar-section">
            <div className="sidebar-section-label">GENERAL</div>

            <NavLink
              to="/dashboard"
              onClick={() => setOpen(false)}
              className={({ isActive }) => getClass(isActive, "overview")}
            >
              <LayoutDashboard className="sidebar-icon" />
              <span className="sidebar-item-label">Dashboard</span>
            </NavLink>

            <NavLink
              to="/security"
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                isActive ? "sidebar-item active" : "sidebar-item"
              }
            >
              <ShieldCheck className="sidebar-icon" />
              <span className="sidebar-item-label">Security</span>
            </NavLink>

            <NavLink
              to="/preferences"
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                isActive ? "sidebar-item active" : "sidebar-item"
              }
            >
              <Settings className="sidebar-icon" />
              <span className="sidebar-item-label">Preferences</span>
            </NavLink>
          </div>

          {/* ADMIN SECTION */}
          {isAdmin && (
            <div className="sidebar-section">
              <div className="sidebar-section-label">ADMIN</div>

              <NavLink
                to="/admin/users"
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  isActive ? "sidebar-item active" : "sidebar-item"
                }
              >
                <Users className="sidebar-icon" />
                <span className="sidebar-item-label">User Management</span>
              </NavLink>

              <NavLink
                to="/admin/audit-logs"
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  isActive ? "sidebar-item active" : "sidebar-item"
                }
              >
                <FileSearch className="sidebar-icon" />
                <span className="sidebar-item-label">Audit Logs</span>
              </NavLink>

              <NavLink
                to="/admin/preferences"
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  isActive ? "sidebar-item active" : "sidebar-item"
                }
              >
                <Settings className="sidebar-icon" />
                <span className="sidebar-item-label">Admin Preferences</span>
              </NavLink>
            </div>
          )}
        </div>

        {/* FOOTER */}
        <div className="sidebar-footer minimal">
          © {new Date().getFullYear()} SentinelOps
        </div>
      </aside>
    </>
  );
}

export default memo(Sidebar);
