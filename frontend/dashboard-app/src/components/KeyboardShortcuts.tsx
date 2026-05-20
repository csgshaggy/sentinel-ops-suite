// frontend/dashboard-app/src/components/KeyboardShortcuts.tsx

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface KeyboardShortcutsProps {
  openPalette: () => void;
  closePalette: () => void;
  toggleTheme: () => void;
  openSettings: () => void;
}

export default function KeyboardShortcuts({
  openPalette,
  closePalette,
  toggleTheme,
  openSettings
}: KeyboardShortcutsProps) {
  const navigate = useNavigate();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;

      // Ignore shortcuts while typing
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;

      // ============================
      // COMMAND PALETTE SHORTCUTS
      // ============================

      // Ctrl+K or Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        openPalette();
        return;
      }

      // Shift+P
      if (e.shiftKey && e.key.toLowerCase() === "p") {
        e.preventDefault();
        openPalette();
        return;
      }

      // "/" opens palette
      if (e.key === "/") {
        e.preventDefault();
        openPalette();
        return;
      }

      // Escape closes palette
      if (e.key === "Escape") {
        closePalette();
        return;
      }

      // ============================
      // THEME TOGGLE
      // ============================
      if (e.altKey && e.key.toLowerCase() === "t") {
        e.preventDefault();
        toggleTheme();
        return;
      }

      // ============================
      // SETTINGS MODAL
      // ============================
      if (e.altKey && e.key.toLowerCase() === "s") {
        e.preventDefault();
        openSettings();
        return;
      }

      // ============================
      // ALT + NUMBER NAVIGATION
      // (Preserved from original)
      // ============================
      const shortcuts: Record<string, string> = {
        "1": "/admin",
        "2": "/admin/pelm",
        "3": "/admin/anomaly",
        "4": "/admin/idrim",
        "5": "/admin/validators",
        "6": "/admin/repo-health",
        "7": "/admin/git-health"
      };

      if (e.altKey && shortcuts[e.key]) {
        e.preventDefault();
        navigate(shortcuts[e.key]);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [navigate, openPalette, closePalette, toggleTheme, openSettings]);

  return null;
}
