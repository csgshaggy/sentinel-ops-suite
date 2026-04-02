import React, { useEffect,useState } from "react";

import Breadcrumbs from "./components/Breadcrumbs";
import CommandPalette from "./components/CommandPalette";
import KeyboardShortcuts from "./components/KeyboardShortcuts";
import MobileDrawer from "./components/MobileDrawer";
import NotificationCenter from "./components/NotificationCenter";
import OpsAlerts from "./components/OpsAlerts";
import StatusBar from "./components/StatusBar";
import Nav from "./Nav";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(true);
  const [mobile, setMobile] = useState(false);

  // Example RBAC roles (replace with real auth later)
  const roles = ["admin", "analyst"];

  // Detect mobile mode
  useEffect(() => {
    const handleResize = () => setMobile(window.innerWidth < 768);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const toggleSidebar = () => setOpen((o) => !o);

  return (
    <div className="flex h-screen bg-gray-800 text-gray-200 dark:bg-gray-950 dark:text-gray-100">

      {/* Mobile Drawer */}
      <MobileDrawer open={mobile && open} onClose={() => setOpen(false)} roles={roles} />

      {/* Desktop Sidebar */}
      <div
        className={`hidden md:block transition-all duration-300 border-r border-gray-700 dark:border-gray-800
          ${open ? "w-64" : "w-16"}
          bg-gray-900 dark:bg-gray-900`}
      >
        <button
          onClick={toggleSidebar}
          className="w-full text-left px-4 py-2 bg-gray-700 hover:bg-gray-600 dark:bg-gray-800 dark:hover:bg-gray-700"
        >
          {open ? "Collapse ◀" : "▶"}
        </button>

        <Nav collapsed={!open} roles={roles} />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">

        {/* Status Bar */}
        <StatusBar />

        {/* Command Palette (Ctrl+K) */}
        <CommandPalette />

        {/* Global Keyboard Shortcuts */}
        <KeyboardShortcuts />

        {/* Global Notification Center */}
        <NotificationCenter />

        {/* SSE‑Driven Ops Alerts */}
        <OpsAlerts />

        {/* Breadcrumbs */}
        <Breadcrumbs />

        {/* Routed Content */}
        <main className="flex-1 overflow-auto p-4">
          {children}
        </main>
      </div>
    </div>
  );
}
