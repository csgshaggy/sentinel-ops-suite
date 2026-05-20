import React, { useEffect } from "react";
import "./session-expired-toast.css";

export default function SessionExpiredToast({ visible, onClose }) {
  useEffect(() => {
    if (!visible) return;

    const timer = setTimeout(() => {
      onClose();
    }, 4000); // auto-hide after 4 seconds

    return () => clearTimeout(timer);
  }, [visible, onClose]);

  if (!visible) return null;

  return (
    <div className="session-toast">
      <div className="session-toast-content">
        <strong>Session Expired</strong>
        <p>You were logged out due to inactivity.</p>
      </div>
    </div>
  );
}
