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
  const isAdmin = userRole === "admin";

  const menuItems = useMemo(() => {
    const items = [
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

    if (isAdmin) {
      items.push(
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
        }
      );
    }

    items.push({
      key: "logout",
      label: "Logout",
      icon: <LogOut size={16} />,
      action: () => navigate("/logout"),
    });

    return items;
  }, [navigate, isAdmin]);

  const closeMenu = (restoreFocus = true) => {
    setMenuOpen(false);

    if (restoreFocus) {
      requestAnimationFrame(() => {
        avatarButtonRef.current?.focus();
      });
    }
  };

  const openMenu = () => {
    setMenuOpen(true);
  };

  const toggleMenu = () => {
    setMenuOpen((prev) => !prev);
  };

  const focusFirstMenuItem = () => {
    const firstItem = menuRef.current?.querySelector('[role="menuitem"]');
    firstItem?.focus();
  };

  // Click-outside close + ESC close
  useEffect(() => {
    if (!menuOpen) return;

    const handleMouseDown = (event) => {
      if (!wrapperRef.current?.contains(event.target)) {
        setMenuOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        closeMenu(true);
      }
    };

    document.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [menuOpen]);

  // Move focus into menu when opened
  useEffect(() => {
    if (menuOpen) {
      requestAnimationFrame(() => {
        focusFirstMenuItem();
      });
    }
  }, [menuOpen]);

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
          focusFirstMenuItem();
        }
        break;

      default:
        break;
    }
  };

  const handleMenuKeyDown = (event) => {
    const items = menuRef.current?.querySelectorAll('[role="menuitem"]');
    if (!items || items.length === 0) return;

    const itemArray = Array.from(items);
    const currentIndex = itemArray.indexOf(document.activeElement);

    switch (event.key) {
      case "ArrowDown": {
        event.preventDefault();
        const nextIndex = currentIndex < 0 ? 0 : (currentIndex + 1) % itemArray.length;
        itemArray[nextIndex].focus();
        break;
      }

      case "ArrowUp": {
        event.preventDefault();
        const previousIndex =
          currentIndex < 0
            ? itemArray.length - 1
            : (currentIndex - 1 + itemArray.length) % itemArray.length;
        itemArray[previousIndex].focus();
        break;
      }

      case "Home":
        event.preventDefault();
        itemArray[0].focus();
        break;

      case "End":
        event.preventDefault();
        itemArray[itemArray.length - 1].focus();
        break;

      case "Tab":
        setMenuOpen(false);
        break;

      case "Escape":
        event.preventDefault();
        closeMenu(true);
        break;

      default:
        break;
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
              {menuItems.map((item) => {
                const showDividerBeforeLogout = isAdmin && item.key === "logout";

                return (
                  <React.Fragment key={item.key}>
                    {showDividerBeforeLogout && (
                      <div className="dropdown-divider" aria-hidden="true" />
                    )}

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
