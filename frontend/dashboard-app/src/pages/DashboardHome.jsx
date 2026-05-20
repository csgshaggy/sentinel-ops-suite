// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/pages/DashboardHome.jsx

import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../services/AuthContext";

import Layout from "../components/layout/Layout.jsx";

import "../styles/panels.css";

export default function DashboardHome() {
  const navigate = useNavigate();
  const { isAuthenticated, hasRole } = useAuth();

  const isAdmin = hasRole("admin");

  const panels = [
    { name: "PELM Panel", path: "/admin/pelm" },
    { name: "Anomaly Detection", path: "/admin/anomaly" },
    { name: "IDRIM Panel", path: "/admin/idrim" },
    { name: "Validators", path: "/admin/validators", adminOnly: true },
    { name: "Repo Health", path: "/admin/repo-health", adminOnly: true },
    { name: "Git Health", path: "/admin/git-health", adminOnly: true },
  ];

  return (
    <Layout>
      <div className="panel">

        {/* Header Panel */}
        <h2 className="panel-title">Sentinel Ops Suite</h2>

        {isAuthenticated() && (
          <p className="panel-body">● Session Active</p>
        )}
      </div>

      {/* Panels Grid */}
      <div className="panel">
        <h2 className="panel-title">Available Panels</h2>

        <div className="panel-grid two-col">
          {panels
            .filter((panel) => !panel.adminOnly || isAdmin)
            .map((panel) => (
              <div
                key={panel.path}
                className="dashboard-card"
                onClick={() => navigate(panel.path)}
              >
                <span className="dashboard-card-title">{panel.name}</span>
              </div>
            ))}
        </div>
      </div>
    </Layout>
  );
}
