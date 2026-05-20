// src/components/layout/TopBar.jsx

import { useSettings } from "../../services/SettingsContext.jsx";
import Clock from "./Clock.jsx";
import UserMenu from "./UserMenu.jsx";
import Breadcrumbs from "./Breadcrumbs.jsx";
import NotificationBell from "./NotificationBell.jsx";

export default function TopBar({ onOpenSettings }) {
  const { settings } = useSettings();

  if (!settings) return null;

  const {
    show_clock,
    use_24h,
    show_seconds,
    show_day,
  } = settings;

  return (
    <header className="topbar">

      {/* LEFT SIDE: Dynamic Breadcrumbs */}
      <div className="topbar-left">
        <Breadcrumbs />
      </div>

      {/* CENTER: Clock (if enabled) */}
      <div className="topbar-center">
        {show_clock && (
          <Clock
            use24h={use_24h}
            showSeconds={show_seconds}
            showDay={show_day}
          />
        )}
      </div>

      {/* RIGHT SIDE: Notification Bell + User Menu */}
      <div className="topbar-right">
        <NotificationBell />
        <UserMenu onOpenSettings={onOpenSettings} />
      </div>
    </header>
  );
}
