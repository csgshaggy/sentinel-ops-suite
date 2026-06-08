// /src/components/Dashboard/DashboardGrid.jsx

import React, { memo } from "react";
import "./DashboardGrid.css";

/**
 * Sentinel Ops — Dashboard Grid
 * Operator-grade responsive grid for dashboard widgets.
 *
 * - Auto-fit columns
 * - Neon-glass compatible
 * - Clean, modular layout
 */
function DashboardGrid({ children }) {
  return (
    <div className="dashboard-grid">
      {children}
    </div>
  );
}

export default memo(DashboardGrid);
