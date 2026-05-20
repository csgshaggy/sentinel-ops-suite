// /src/state/commandPaletteState.js

import { create } from "zustand";

// -------------------------------
// ROUTE MAP (auto-discovered from your router)
// -------------------------------
const ROUTES = [
  // Public
  { path: "/login", label: "Login", icon: "🔐" },

  // Admin
  { path: "/admin", label: "Admin Home", icon: "📊" },
  { path: "/admin/dashboard", label: "Dashboard", icon: "📊" },

  // Security
  { path: "/admin/security", label: "Security", icon: "🔐" },
  { path: "/admin/security/change-password", label: "Change Password", icon: "🔑" },
  { path: "/admin/security/mfa-disable", label: "Disable MFA", icon: "🔑" },
  { path: "/admin/security/recovery", label: "Recovery Options", icon: "🛟" },
  { path: "/admin/security/backup-codes", label: "Backup Codes", icon: "📄" },
  { path: "/admin/security/device-trust", label: "Device Trust", icon: "🖥️" },
  { path: "/admin/security/login-alerts", label: "Login Alerts", icon: "🚨" },
  { path: "/admin/security/notifications", label: "Security Notifications", icon: "🔔" },

  // Admin-only
  { path: "/admin/audit-logs", label: "Audit Logs", icon: "📜" },
  { path: "/admin/users", label: "Users", icon: "👥" },
];

// -------------------------------
// FUZZY MATCHING
// -------------------------------
function fuzzyMatch(query, text) {
  if (!query) return true;
  return text.toLowerCase().includes(query.toLowerCase());
}

// -------------------------------
// GLOBAL STATE (Zustand)
// -------------------------------
export const useCommandPalette = create((set, get) => ({
  isOpen: false,
  query: "",
  results: ROUTES,
  selectedIndex: 0,

  // Open / Close
  openPalette: () => set({ isOpen: true }),
  closePalette: () => set({ isOpen: false, query: "", selectedIndex: 0 }),

  // Query handling
  setQuery: (q) => {
    const filtered = ROUTES.filter(
      (r) =>
        fuzzyMatch(q, r.label) ||
        fuzzyMatch(q, r.path)
    );

    set({
      query: q,
      results: filtered,
      selectedIndex: 0,
    });
  },

  // Keyboard navigation
  moveSelectionDown: () => {
    const { selectedIndex, results } = get();
    if (results.length === 0) return;
    const next = (selectedIndex + 1) % results.length;
    set({ selectedIndex: next });
  },

  moveSelectionUp: () => {
    const { selectedIndex, results } = get();
    if (results.length === 0) return;
    const next = (selectedIndex - 1 + results.length) % results.length;
    set({ selectedIndex: next });
  },

  selectCurrent: () => {
    const { results, selectedIndex } = get();
    return results[selectedIndex] || null;
  },
}));

// -------------------------------
// GLOBAL KEYBOARD SHORTCUT (Ctrl+K)
// -------------------------------
window.addEventListener("keydown", (e) => {
  const { openPalette, isOpen, closePalette } = useCommandPalette.getState();

  // Ctrl+K opens palette
  if (e.ctrlKey && e.key.toLowerCase() === "k") {
    e.preventDefault();
    if (!isOpen) openPalette();
  }

  // ESC closes palette (handled in component too)
  if (e.key === "Escape" && isOpen) {
    closePalette();
  }
});
