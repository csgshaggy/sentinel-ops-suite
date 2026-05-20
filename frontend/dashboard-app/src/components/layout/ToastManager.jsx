// src/components/layout/ToastManager.jsx

import { useEffect, useState } from "react";
import { useSettings } from "../../services/SettingsContext.jsx";

export default function ToastManager() {
  const { settings } = useSettings();
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const handler = (event) => {
      const { message, type = "info" } = event.detail;

      const id = crypto.randomUUID();
      const duration = settings.toast_duration || 4000;

      setToasts((prev) => [...prev, { id, message, type }]);

      // Auto-remove
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, duration);

      // Optional sound
      if (settings.toast_sound) {
        const audio = new Audio("/sounds/notify.mp3");
        audio.volume = 0.4;
        audio.play().catch(() => {});
      }
    };

    window.addEventListener("global-toast", handler);
    return () => window.removeEventListener("global-toast", handler);
  }, [settings]);

  if (!settings) return null;

  const position = settings.toast_position || "top-right";

  return (
    <div className={`toast-container ${position}`}>
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      ))}
    </div>
  );
}
