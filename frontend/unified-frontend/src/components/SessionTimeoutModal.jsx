// /src/components/SessionTimeoutModal.jsx

import { useEffect, useState, useRef } from "react";
import { createPortal } from "react-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { toast } from "./ToastManager.jsx";
import "./SessionTimeoutModal.css";

/**
 * SessionTimeoutModal
 * - Neon-glass modal
 * - Countdown timer
 * - Stay Logged In + Logout Now
 * - ESC closes (Stay Logged In)
 * - Focus trap
 */
export default function SessionTimeoutModal({
  isOpen,
  onStayLoggedIn,
  onLogout,
}) {
  const [countdown, setCountdown] = useState(10);
  const { user } = useAuth();
  const modalRef = useRef(null);

  /* ------------------------------------------------------------
     Reset countdown when modal opens
  ------------------------------------------------------------ */
  useEffect(() => {
    if (isOpen) setCountdown(10);
  }, [isOpen]);

  /* ------------------------------------------------------------
     Countdown timer
  ------------------------------------------------------------ */
  useEffect(() => {
    if (!isOpen) return;

    if (countdown <= 0) {
      onLogout();
      return;
    }

    const timer = setTimeout(() => setCountdown((c) => c - 1), 1000);
    return () => clearTimeout(timer);
  }, [isOpen, countdown, onLogout]);

  /* ------------------------------------------------------------
     ESC closes modal (Stay Logged In)
  ------------------------------------------------------------ */
  useEffect(() => {
    if (!isOpen) return;

    function handleKey(e) {
      if (e.key === "Escape") onStayLoggedIn();
    }

    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [isOpen, onStayLoggedIn]);

  /* ------------------------------------------------------------
     Focus trap when modal opens
  ------------------------------------------------------------ */
  useEffect(() => {
    if (!isOpen) return;

    const focusable = modalRef.current?.querySelectorAll(
      "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
    );

    if (focusable && focusable.length > 0) {
      focusable[0].focus();
    }
  }, [isOpen]);

  if (!isOpen || !user) return null;

  return createPortal(
    <div className="session-timeout-overlay">
      <div className="session-timeout-modal glass-panel" ref={modalRef}>
        <h2 className="session-timeout-title">Session Expiring</h2>

        <p className="session-timeout-text">
          You will be logged out in{" "}
          <span className="session-timeout-count">{countdown}</span> seconds.
        </p>

        <div className="session-timeout-actions">
          <button
            className="session-btn stay-btn"
            onClick={() => {
              toast.success("Session extended.");
              onStayLoggedIn();
            }}
          >
            Stay Logged In
          </button>

          <button
            className="session-btn logout-btn"
            onClick={() => {
              toast.info("Logging out...");
              onLogout();
            }}
          >
            Logout Now
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
}

