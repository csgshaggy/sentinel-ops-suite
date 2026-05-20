import React from "react";
import "./SessionExpireModal.css";

export default function SessionExpireModal({ visible, onLogout }) {
  if (!visible) return null;

  return (
    <div className="session-expire-overlay">
      <div className="session-expire-modal">
        <h2>Session Expired</h2>
        <p>Your session has ended due to inactivity.</p>

        <div className="session-expire-actions">
          <button className="logout-btn" onClick={onLogout}>
            Log Out
          </button>
        </div>
      </div>
    </div>
  );
}
