// ============================================
// Dashboard.jsx — Full Regeneration
// Includes MFA Status Banner + Session Awareness
// ============================================

import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Dashboard.css";

// ============================================
// MFA Status Banner (Inline Component)
// ============================================

const MfaStatusBanner = ({ mfaEnabled, userId, navigate }) => {
  if (mfaEnabled) return null;

  return (
    <div className="mfa-banner">
      <p className="mfa-banner-text">
        Your account is not protected with Multi‑Factor Authentication.
      </p>

      <button
        className="mfa-banner-btn"
        onClick={() => navigate("/mfa/setup", { state: { userId } })}
      >
        Enable MFA
      </button>
    </div>
  );
};

// ============================================
// MAIN DASHBOARD COMPONENT
// ============================================

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  // ---------- LOADING STATE ----------
  if (loading) {
    return (
      <div className="dashboard-loading">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  // ---------- UNAUTHENTICATED REDIRECT ----------
  if (!user) {
    navigate("/login");
    return null;
  }

  return (
    <div className="dashboard-container">

      {/* ---------- MFA STATUS BANNER ---------- */}
      <MfaStatusBanner
        mfaEnabled={user?.mfa_enabled}
        userId={user?.id}
        navigate={navigate}
      />

      {/* ---------- DASHBOARD HEADER ---------- */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Welcome, {user.username}</h1>
        <p className="dashboard-subtitle">
          Your operational console is ready.
        </p>
      </div>

      {/* ---------- MAIN DASHBOARD CONTENT ---------- */}
      <div className="dashboard-content">
        {/* 
          Insert your tiles, charts, panels, 
          operator console widgets, etc.
        */}
      </div>

    </div>
  );
};

export default Dashboard;
