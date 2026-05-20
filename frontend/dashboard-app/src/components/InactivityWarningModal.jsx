import React, { useEffect, useState } from "react";
import "./inactivity-warning.css";

export default function InactivityWarningModal({ visible, onStayLoggedIn, onLogout }) {
  const [secondsLeft, setSecondsLeft] = useState(60);

  useEffect(() => {
    if (!visible) {
      setSecondsLeft(60);
      return;
    }

    const interval = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onLogout();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [visible, onLogout]);

  if (!visible) return null;

  return (
    <div className="inactivity-modal-overlay">
      <div className="inactivity-modal">
        <h2>Session Expiring Soon</h2>
        <p>You’ve been inactive for a while.</p>
        <p>Your session will end in <strong>{secondsLeft}</strong> seconds.</p>

        <div className="inactivity-modal-actions">
          <button className="stay-button" onClick={onStayLoggedIn}>
            Stay Logged In
          </button>

          <button className="logout-button" onClick={onLogout}>
            Logout Now
          </button>
        </div>
      </div>
    </div>
  );
}
