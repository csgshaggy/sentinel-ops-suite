import React from "react";
import "./session-expiry-modal.css";

export default function SessionExpiryModal({
  visible,
  countdown,
  onStayLoggedIn,
  onLogout,
}) {
  if (!visible) return null;

  return (
    <div className="session-expiry-backdrop">
      <div className="session-expiry-modal">
        <h2>Session Expiring Soon</h2>

        <p>Your session will expire in:</p>

        <div className="session-expiry-timer">
          {countdown}s
        </div>

        <div className="session-expiry-actions">
          <button className="stay-btn" onClick={onStayLoggedIn}>
            Stay Logged In
          </button>

          <button className="logout-btn" onClick={onLogout}>
            Logout Now
          </button>
        </div>
      </div>
    </div>
  );
}
