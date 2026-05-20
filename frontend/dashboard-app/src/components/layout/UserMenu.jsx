// src/components/layout/UserMenu.jsx

import { useState, useRef, useEffect } from "react";
import { useAuth } from "../../services/AuthContext.jsx";

export default function UserMenu({ onOpenSettings }) {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);

  const toggle = () => setOpen((prev) => !prev);

  // Close menu when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div className="user-menu-wrapper" ref={menuRef}>
      <button className="user-menu-button" onClick={toggle}>
        {user?.username || "User"} ▾
      </button>

      {open && (
        <div className="user-menu-dropdown">
          <div className="user-menu-header">
            <div className="user-menu-name">{user?.username}</div>
            <div className="user-menu-email">{user?.email}</div>
          </div>

          <button
            className="user-menu-item"
            onClick={() => {
              setOpen(false);
              onOpenSettings();
            }}
          >
            Preferences
          </button>

          <button
            className="user-menu-item logout"
            onClick={() => {
              setOpen(false);
              logout();
            }}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
