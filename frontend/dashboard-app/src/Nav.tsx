// frontend/dashboard-app/src/Nav.tsx

import React from "react";
import { NavLink } from "react-router-dom";
import { navConfig } from "./config/navConfig";
import { useAuth } from "./services/AuthContext";

/**
 * Nav (dashboard-app)
 *
 * - Supports collapsed mode
 * - Filters items by role (RBAC)
 * - Highlights active route using NavLink
 * - Integrates AuthContext for future user-aware UI
 */

export default function Nav({
  collapsed,
  roles = [],
}: {
  collapsed: boolean;
  roles?: string[];
}) {
  const { token } = useAuth(); // future-proofing for user-aware nav

  // RBAC filtering
  const allowed = navConfig.filter(
    (item) => !item.roles || item.roles.some((r) => roles.includes(r))
  );

  return (
    <ul className="mt-4 space-y-1">
      {allowed.map((item) => (
        <li key={item.path}>
          <NavLink
            to={item.path}
            className={({ isActive }) =>
              [
                "flex items-center px-3 py-2 rounded transition-colors",
                "hover:bg-gray-700 dark:hover:bg-gray-800",
                isActive ? "bg-gray-800 dark:bg-gray-900 font-semibold" : "",
              ].join(" ")
            }
          >
            {/* Icon always visible */}
            <span className="text-lg">{item.icon}</span>

            {/* Label hidden when collapsed */}
            {!collapsed && (
              <span className="ml-3 text-sm font-medium whitespace-nowrap">
                {item.name}
              </span>
            )}
          </NavLink>
        </li>
      ))}
    </ul>
  );
}
