import React, { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell,
  Settings,
  User,
  LogOut,
  Shield,
  Wrench,
} from "lucide-react";
import "./TopBar.css";

export default function TopBar({ userRole = "user" }) {
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);

  const wrapperRef = useRef(null);
  const avatarButtonRef = useRef(null);
  const menuRef = useRef(null);

  const menuId = "topbar-avatar-menu";

  const menuItems = useMemo(() => {
    const baseItems = [
      {
        key: "profile",
        label: "Profile",
        icon: <User size={16} />,
        action: () => navigate("/profile"),
      },
      {
        key: "settings",
        label: "Settings",
        icon: <Settings size={16} />,
        action: () => navigate("/settings"),
      },
    ];

    const adminItems =
      userRole === "admin"
        ? [
            {
              key: "admin-panel",
              label: "Admin Panel",
              icon: <Shield size={16} />,
              action: () => navigate("/admin"),
            },
            {
              key: "system-tools",
              label: "System Tools",
              icon: <Wrench size={16} />,
              action: () => navigate("/admin/tools"),
            },
          ]
        : [];

    const endItems = [
      {
        key: "logout",
        label: "Logout",
        icon: <LogOut size={16} />,
        action: () => navigate("/logout"),
      },
    ];

    return [...baseItems, ...adminItems, ...endItems];
  }, [navigate, userRole]);

  const closeMenu = () => {
    setMenuOpen(false);
    avatarButtonRef.current?.focus();
  };

  const openMenu = () => {
    setMenuOpen(true);
  };

  const toggleMenu = () => {
    setMenuOpen((prev) => !prev);
  };

  // ✅ Click-outside close + ESC close
  useEffect(() => {
    function handleMouseDown(event) {
      if (!wrapperRef.current?.contains(event.target)) {
        setMenuOpen(false);
      }
    }

    function handleKeyDown(event) {
      if (event.key === "Escape") {
        setMenuOpen(false);
        avatarButtonRef.current?.focus();
      }
    }

    if (menuOpen) {
      document.addEventListener("mousedown", handleMouseDown);
      document.addEventListener("keydown", handleKeyDown);
    }

    return () => {
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [menuOpen]);

  // ✅ Move focus into menu when opened
  useEffect(() => {
    if (menuOpen && menuRef.current) {
      const firstItem = menuRef.current.querySelector('[role="menuitem"]');
      firstItem?.focus();
    }
  }, [menuOpen]);

  // ✅ Keyboard support on avatar button
  const handleAvatarKeyDown = (event) => {
    switch (event.key) {
      case "Enter":
      case " ":
        event.preventDefault();
        toggleMenu();
        break;
      case "ArrowDown":
        event.preventDefault();
        if (!menuOpen) {
          openMenu();
        } else {
          const firstItem = menuRef.current?.querySelector('[role="menuitem"]');
          firstItem?.focus();
        }
        break;
      default:
        break;
    }
  };

  // ✅ Keyboard navigation inside the menu
  const handleMenuKeyDown = (event) => {
    const items = menuRef.current?.querySelectorAll('[role="menuitem"]');
    if (!items || items.length === 0) return;

    const currentIndex = Array.from(items).indexOf(document.activeElement);

    if (event.key === "ArrowDown") {
      event.preventDefault();
      const nextIndex = (currentIndex + 1) % items.length;
      items[nextIndex].focus();
    }

    if (event.key === "ArrowUp") {
      event.preventDefault();
      const previousIndex = (currentIndex - 1 + items.length) % items.length;
      items[previousIndex].focus();
    }

    if (event.key === "Home") {
      event.preventDefault();
      items[0].focus();
    }

    if (event.key === "End") {
      event.preventDefault();
      items[items.length - 1].focus();
    }

    if (event.key === "Tab") {
      setMenuOpen(false);
    }

    if (event.key === "Escape") {
      event.preventDefault();
      closeMenu();
    }
  };

  const handleMenuItemClick = (action) => {
    setMenuOpen(false);
    action();
  };

  return (
    <header className="topbar-container">
      {/* LEFT — LOGO + TITLE */}
      <div className="topbar-left">
        <img
          src="/logo.png"
          alt="SentinelOps Logo"
          className="topbar-logo"
        />
        <span className="topbar-title">Sentinel Ops Suite</span>
      </div>

      {/* CENTER — OPTIONAL */}
      <div className="topbar-center" />

      {/* RIGHT — ICON CLUSTER */}
      <div className="topbar-right">
        {/* Notifications */}
        <button
          type="button"
          className="topbar-icon topbar-icon-button"
          onClick={() => navigate("/notifications")}
          aria-label="Notifications"
        >
          <Bell size={18} />
        </button>

        {/* Avatar + Dropdown */}
        <div className="avatar-wrapper" ref={wrapperRef}>
          <button
            type="button"
            ref={avatarButtonRef}
            className="topbar-avatar-button"
            onClick={toggleMenu}
            onKeyDown={handleAvatarKeyDown}
            aria-label="Open user menu"
            aria-haspopup="menu"
            aria-expanded={menuOpen}
            aria-controls={menuId}
          >
            <img
              src="/default-avatar.png"
              alt="User Avatar"
              className="topbar-avatar"
            />
          </button>

          {menuOpen && (
            <div
              id={menuId}
              className="avatar-dropdown"
              role="menu"
              aria-label="User menu"
              ref={menuRef}
              onKeyDown={handleMenuKeyDown}
            >
              {menuItems.map((item, index) => {
                const showDividerBefore =
                  userRole === "admin" &&
                  item.key === "logout" &&
                  menuItems.some((entry) => entry.key === "admin-panel");

                return (
                  <React.Fragment key={item.key}>
                    {showDividerBefore && <div className="dropdown-divider" />}
                    <button
                      type="button"
                      className="dropdown-item"
                      role="menuitem"
                      onClick={() => handleMenuItemClick(item.action)}
                    >
                      {item.icon}
                      <span>{item.label}</span>
                    </button>
                  </React.Fragment>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
