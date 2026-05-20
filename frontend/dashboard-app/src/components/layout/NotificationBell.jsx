// src/components/layout/NotificationBell.jsx

import { useState, useRef, useEffect } from "react";

export default function NotificationBell() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const bellRef = useRef(null);

  const toggle = () => setOpen((prev) => !prev);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (bellRef.current && !bellRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  // Listen for global notifications
  useEffect(() => {
    const handler = (event) => {
      const { message, type = "info" } = event.detail;
      const id = crypto.randomUUID();
      const timestamp = new Date().toISOString();

      setNotifications((prev) => [
        { id, message, type, timestamp },
        ...prev,
      ]);
    };

    window.addEventListener("global-notification", handler);
    return () => window.removeEventListener("global-notification", handler);
  }, []);

  const unreadCount = notifications.length;

  return (
    <div className="notification-wrapper" ref={bellRef}>
      <button className="notification-bell" onClick={toggle}>
        🔔
        {unreadCount > 0 && (
          <span className="notification-count">{unreadCount}</span>
        )}
      </button>

      {open && (
        <div className="notification-dropdown">
          <div className="notification-header">
            Notifications
          </div>

          {notifications.length === 0 && (
            <div className="notification-empty">
              No notifications
            </div>
          )}

          {notifications.map((n) => (
            <div key={n.id} className={`notification-item ${n.type}`}>
              <div className="notification-message">{n.message}</div>
              <div className="notification-time">
                {new Date(n.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
