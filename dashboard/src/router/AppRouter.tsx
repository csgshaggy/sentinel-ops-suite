// dashboard/src/router/AppRouter.tsx

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import SidebarLayout from "../layout/SidebarLayout";
import Dashboard from "../components/Dashboard";
import PluginsPage from "../pages/PluginsPage";
import HealthPage from "../pages/HealthPage";
import DiffsPage from "../pages/DiffsPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <SidebarLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/plugins" element={<PluginsPage />} />
          <Route path="/health" element={<HealthPage />} />
          <Route path="/diffs" element={<DiffsPage />} />
        </Routes>
      </SidebarLayout>
    </BrowserRouter>
  );
}
