import React from "react";

export default function SessionExpireModal({ seconds, onExtend, onLogout }) {
  return (
    <div className="session-expire-backdrop" role="dialog" aria-modal="true">
      <div className="session-expire-modal">
        <h2 className="session-expire-title">Session Expiring</h2>
        <p className="session-expire-text">
          Your session will expire in{" "}
          <span className="session-expire-count">{seconds}</span> seconds.
        </p>

        <div className="session-expire-actions">
          <button
            type="button"
            className="session-expire-btn session-expire-btn-primary"
            onClick={onExtend}
          >
            Stay signed in
          </button>
          <button
            type="button"
            className="session-expire-btn session-expire-btn-secondary"
            onClick={onLogout}
          >
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
}
