import React from "react";
import { Link } from "react-router-dom";

import { navConfig } from "./config/navConfig";

export default function Nav({
  collapsed,
  roles = [],
}: {
  collapsed: boolean;
  roles?: string[];
}) {
  const allowed = navConfig.filter(
    (item) => !item.roles || item.roles.some((r) => roles.includes(r))
  );

  return (
    <ul className="mt-4 space-y-1">
      {allowed.map((item) => (
        <li key={item.path}>
          <Link
            to={item.path}
            className="flex items-center px-3 py-2 rounded hover:bg-gray-700 dark:hover:bg-gray-800 transition-colors"
          >
            <span className="text-lg">{item.icon}</span>

            {!collapsed && (
              <span className="ml-3 text-sm font-medium whitespace-nowrap">
                {item.name}
              </span>
            )}
          </Link>
        </li>
      ))}
    </ul>
  );
}
