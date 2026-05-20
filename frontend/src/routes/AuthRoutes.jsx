// ============================================
// AuthRoutes.jsx — Unified Auth Routing Layer
// Dark‑Ops Auth Stack (Login, Signup, MFA, Reset)
// ============================================

import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

// ---------- AUTH SCREENS ----------
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import ForgotPassword from "../pages/ForgotPassword";
import ResetPassword from "../pages/ResetPassword";
import MfaChallenge from "../pages/MfaChallenge";

const AuthRoutes = () => {
  return (
    <Routes>

      {/* ---------- LOGIN ---------- */}
      <Route path="/login" element={<Login />} />

      {/* ---------- SIGNUP ---------- */}
      <Route path="/signup" element={<Signup />} />

      {/* ---------- FORGOT PASSWORD ---------- */}
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* ---------- RESET PASSWORD ---------- */}
      <Route path="/reset-password" element={<ResetPassword />} />

      {/* ---------- MFA CHALLENGE ---------- */}
      <Route path="/mfa" element={<MfaChallenge />} />

      {/* ---------- FALLBACK ---------- */}
      <Route path="*" element={<Navigate to="/login" replace />} />

    </Routes>
  );
};

export default AuthRoutes;
