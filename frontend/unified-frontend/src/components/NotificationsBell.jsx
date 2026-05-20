// /src/components/NotificationsBell.jsx

import React, { useState, useEffect, useRef } from "react";
import "./NotificationsBell.css";

export default function NotificationsBell() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const bellRef = useRef(null);

  // Placeholder fetch — replace with real API later
  const fetchNotifications = async () => {
    // Example stubbed data
    return [
      { id: 1, message: "New login from trusted device", time: "2m ago" },
      { id: 2, message: "Password changed successfully", time: "1h ago" },
    ];
  };

  useEffect(() => {
    fetchNotifications().then(setNotifications);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClick = (e) => {
      if (bellRef.current && !bellRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const unreadCount = notifications.length;

  return (
    <div className="notif-wrapper" ref={bellRef}>
      <button
        className="notif-bell"
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Notifications"
      >
        🔔
        {unreadCount > 0 && (
          <span className="notif-count">{unreadCount}</span>
        )}
      </button>

      {open && (
        <div className="notif-dropdown">
          <div className="notif-header">Notifications</div>

          {notifications.length === 0 ? (
            <div className="notif-empty">No notifications</div>
          ) : (
            notifications.map((n) => (
              <div key={n.id} className="notif-item">
                <div className="notif-message">{n.message}</div>
                <div className="notif-time">{n.time}</div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
