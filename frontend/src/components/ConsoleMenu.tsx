import React from "react";
import { Link } from "react-router-dom";

interface MenuItem {
  id: string;
  label: string;
  icon?: string;
  route: string;
}

const menuItems: MenuItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: "📊",
    route: "/",
  },
  {
    id: "logs",
    label: "Logs",
    icon: "📜",
    route: "/logs",
  },
  {
    id: "anomalies",
    label: "Anomalies",
    icon: "🧪",
    route: "/anomalies",
  },
  {
    id: "health",
    label: "Health",
    icon: "❤️",
    route: "/health",
  },
  {
    id: "pelm",
    label: "PELM Module",
    icon: "⚙️",
    route: "/pelm",
  },
];

export default function ConsoleMenu() {
  return (
    <nav className="console-menu">
      <ul>
        {menuItems.map((item) => (
          <li key={item.id}>
            <Link to={item.route}>
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
