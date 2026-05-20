// /src/components/UserMenu.jsx
import React, { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import "./UserMenu.css";

export default function UserMenu({ initials = "U" }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [open, setOpen] = useState(false);
  const [submenuOpen, setSubmenuOpen] = useState(false);

  const avatarRef = useRef(null);
  const dropdownRef = useRef(null);
  const submenuRef = useRef(null);

  const toggle = () => setOpen((v) => !v);

  /* -----------------------------------------------------------
     CLICK OUTSIDE
  ------------------------------------------------------------ */
  useEffect(() => {
    if (!open) return;

    const handleClick = (e) => {
      const avatar = avatarRef.current;
      const dropdown = dropdownRef.current;

      if (!avatar || !dropdown) return;

      const insideAvatar = avatar.contains(e.target);
      const insideDropdown = dropdown.contains(e.target);

      if (!insideAvatar && !insideDropdown) {
        setOpen(false);
        setSubmenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClick);
    document.addEventListener("touchstart", handleClick);

    return () => {
      document.removeEventListener("mousedown", handleClick);
      document.removeEventListener("touchstart", handleClick);
    };
  }, [open]);

  /* -----------------------------------------------------------
     POSITION DROPDOWN
  ------------------------------------------------------------ */
  const [coords, setCoords] = useState({ top: 0, left: 0 });

  useEffect(() => {
    if (!open || !avatarRef.current) return;

    const rect = avatarRef.current.getBoundingClientRect();
    const isMobile = window.innerWidth < 600;
    const dropdownWidth = isMobile ? 220 : 180;
    const margin = 8;

    let left = rect.left - 70;
    let top = rect.bottom + margin;

    const maxLeft = window.innerWidth - dropdownWidth - margin;
    const minLeft = margin;
    left = Math.max(minLeft, Math.min(left, maxLeft));

    const dropdownHeight = isMobile ? 300 : 240;
    const maxTop = window.innerHeight - dropdownHeight - margin;
    top = Math.max(margin, Math.min(top, maxTop));

    setCoords({ top, left });
  }, [open]);

  /* -----------------------------------------------------------
     REPOSITION ON RESIZE
  ------------------------------------------------------------ */
  useEffect(() => {
    if (!open) return;

    const handleRecalc = () => {
      if (!avatarRef.current) return;
      const rect = avatarRef.current.getBoundingClientRect();
      setCoords({
        top: rect.bottom + 8,
        left: rect.left - 70,
      });
    };

    window.addEventListener("resize", handleRecalc);
    window.addEventListener("orientationchange", handleRecalc);

    return () => {
      window.removeEventListener("resize", handleRecalc);
      window.removeEventListener("orientationchange", handleRecalc);
    };
  }, [open]);

  /* -----------------------------------------------------------
     KEYBOARD NAVIGATION
  ------------------------------------------------------------ */
  const handleKeyDown = (e) => {
    if (!open) return;

    switch (e.key) {
      case "Escape":
        setOpen(false);
        setSubmenuOpen(false);
        break;

      case "ArrowRight":
        if (!submenuOpen) setSubmenuOpen(true);
        break;

      case "ArrowLeft":
        if (submenuOpen) setSubmenuOpen(false);
        break;

      default:
        break;
    }
  };

  /* -----------------------------------------------------------
     ICONS
  ------------------------------------------------------------ */
  const IconProfile = (
    <svg className="icon menu-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
      <circle cx="12" cy="7" r="4" />
      <path d="M5.5 21a6.5 6.5 0 0 1 13 0" />
    </svg>
  );

  const IconSettings = (
    <svg className="icon menu-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 
               2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 
               1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 
               1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 
               2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 
               1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 
               1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 
               2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01A1.65 
               1.65 0 0 0 9 3.09V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 
               1 1.51h.01a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 
               2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01A1.65 
               1.65 0 0 0 21 12h.09a2 2 0 1 1 0 4h-.09a1.65 
               1.65 0 0 0-1.51 1z" />
    </svg>
  );

  const IconLogout = (
    <svg className="icon menu-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" strokeWidth="2">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  );

  /* -----------------------------------------------------------
     RENDER
  ------------------------------------------------------------ */
  return (
    <div className="user-menu">
      <div
        className="user-avatar"
        ref={avatarRef}
        onClick={toggle}
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="User menu"
      >
        <span className="ripple-layer"></span>
        <span className="hud-inner-ring"></span>
        {initials}
      </div>

      {open &&
        createPortal(
          <div
            className={`user-dropdown ${open ? "open" : "closing"}`}
            ref={dropdownRef}
            onKeyDown={handleKeyDown}
            role="menu"
            style={{
              position: "fixed",
              top: coords.top,
              left: coords.left,
            }}
          >
            {/* PROFILE — NOW WITH CONSOLE LOG */}
            <button
              className="dropdown-item"
              role="menuitem"
              onClick={() => {
                console.log("PROFILE CLICKED");
                navigate("/profile");
                setOpen(false);
                setSubmenuOpen(false);
              }}
            >
              {IconProfile}
              Profile
            </button>

            <div className="submenu-wrapper">
              <button
                className="dropdown-item"
                role="menuitem"
                aria-haspopup="true"
                aria-expanded={submenuOpen}
                onClick={() => setSubmenuOpen((v) => !v)}
              >
                {IconSettings}
                Settings
              </button>

              {submenuOpen && (
                <div className="submenu" ref={submenuRef} role="menu">
                  <button
                    className="submenu-item"
                    role="menuitem"
                    onClick={() => {
                      navigate("/profile");
                      setOpen(false);
                      setSubmenuOpen(false);
                    }}
                  >
                    Account
                  </button>

                  <button
                    className="submenu-item"
                    role="menuitem"
                    onClick={() => {
                      navigate("/profile");
                      setOpen(false);
                      setSubmenuOpen(false);
                    }}
                  >
                    Security
                  </button>

                  <button
                    className="submenu-item"
                    role="menuitem"
                    onClick={() => {
                      navigate("/profile");
                      setOpen(false);
                      setSubmenuOpen(false);
                    }}
                  >
                    Preferences
                  </button>
                </div>
              )}
            </div>

            <div className="user-menu-divider"></div>

            <button
              className="dropdown-item logout"
              role="menuitem"
              onClick={() => logout()}
            >
              {IconLogout}
              Logout
            </button>
          </div>,
          document.body
        )}
    </div>
  );
}
