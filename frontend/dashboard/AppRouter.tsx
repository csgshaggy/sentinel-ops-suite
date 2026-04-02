import React from "react";
import { BrowserRouter, Route,Routes } from "react-router-dom";

import Layout from "./Layout";
import DashboardHome from "./pages/DashboardHome";
import AnomalyPanel from "./panels/AnomalyPanel";
import GitHealthPanel from "./panels/GitHealthPanel";
import IDRIMPanel from "./panels/IDRIMPanel";
import PELMPanel from "./panels/PELMPanel";
import RepoHealthPanel from "./panels/RepoHealthPanel";
import ValidatorPanel from "./panels/ValidatorPanel";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardHome />} />

          <Route path="/pelm" element={<PELMPanel />} />
          <Route path="/anomaly" element={<AnomalyPanel />} />
          <Route path="/idrim" element={<IDRIMPanel />} />

          <Route path="/validators" element={<ValidatorPanel />} />
          <Route path="/repo-health" element={<RepoHealthPanel />} />
          <Route path="/git-health" element={<GitHealthPanel />} />

          <Route path="*" element={<DashboardHome />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
