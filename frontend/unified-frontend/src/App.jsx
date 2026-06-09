// /src/App.jsx
// SentinelOps — Unified Application Router (Final, Corrected + AvatarProvider)

import { useEffect, useState, Suspense, lazy } from "react";
import { Routes, Route, useLocation } from "react-router-dom";

import { AuthProvider } from "./features/auth/AuthContext.jsx";
import { SettingsProvider } from "./context/SettingsContext.jsx";
import { AvatarProvider } from "./context/AvatarContext.jsx";   // ⭐ ADDED
import { ModalProvider } from "./components/ModalManager.jsx";

import ProtectedRoute from "./components/ProtectedRoute.jsx";
import RoleProtectedRoute from "./components/RoleProtectedRoute.jsx";

import RouteLoader from "./components/RouteLoader.jsx";
import SystemLockdown from "./components/SystemLockdown.jsx";
import RouteErrorBoundary from "./components/RouteErrorBoundary.jsx";
import ApiErrorOverlay from "./components/ApiErrorOverlay.jsx";

import { initSessionEventBridge } from "./services/sessionEventBridge.js";
import { isAuthRoute } from "./utils/isAuthRoute.js";

import Layout from "./components/Layout.jsx";

// ---------------- PUBLIC PAGES ----------------
const Login = lazy(() => import("./pages/Login.jsx"));
const ForgotPasswordRequest = lazy(() =>
  import("./pages/ForgotPasswordRequest.jsx")
);
const ResetPassword = lazy(() => import("./pages/ResetPassword.jsx"));

// ---------------- AUTHENTICATED PAGES ----------------
const Dashboard = lazy(() => import("./pages/Dashboard.jsx"));
const Security = lazy(() => import("./pages/Security.jsx"));
const Profile = lazy(() => import("./pages/Profile/Profile.jsx"));
const Preferences = lazy(() => import("./pages/Preferences.jsx"));
const SettingsPage = lazy(() => import("./pages/Settings.jsx"));

// ---------------- ADMIN PAGES ----------------
const AdminUsers = lazy(() => import("./pages/AdminUsers.jsx"));
const AdminAuditLogs = lazy(() => import("./pages/AdminAuditLogs.jsx"));
const AdminPreferences = lazy(() =>
  import("./pages/Admin/AdminPreferences.jsx")
);

// ---------------- ERROR PAGES ----------------
const NotFound = lazy(() => import("./pages/NotFound.jsx"));
const ServerError = lazy(() => import("./pages/ServerError.jsx"));

const LOCKDOWN_ENABLED = false;

export default function App() {
  const location = useLocation();
  const [loadingRoute, setLoadingRoute] = useState(false);

  // Dev-only session event bridge
  useEffect(() => {
    if (!import.meta.env.PROD) {
      initSessionEventBridge();
    }
  }, []);

  // Route transition loader
  useEffect(() => {
    Promise.resolve().then(() => setLoadingRoute(true));
    const t = setTimeout(() => setLoadingRoute(false), 350);
    return () => clearTimeout(t);
  }, [location.pathname]);

  const isPublic = isAuthRoute(location.pathname);

  if (LOCKDOWN_ENABLED) {
    return <SystemLockdown />;
  }

  return (
    <AuthProvider>
      <SettingsProvider>
        <AvatarProvider>   {/* ⭐ NEW GLOBAL AVATAR CONTEXT WRAPPER */}
          <ModalProvider>
            <ApiErrorOverlay />

            {!isPublic && loadingRoute && <RouteLoader />}

            <Suspense fallback={<RouteLoader />}>
              <RouteErrorBoundary>
                <Routes>

                  {/* ---------------- PUBLIC ROUTES ---------------- */}
                  <Route path="/login" element={<Login />} />
                  <Route path="/forgot-password" element={<ForgotPasswordRequest />} />
                  <Route path="/reset-password" element={<ResetPassword />} />

                  {/* ---------------- AUTHENTICATED ROUTES ---------------- */}
                  <Route element={<ProtectedRoute />}>
                    <Route element={<Layout />}>
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/security" element={<Security />} />
                      <Route path="/profile" element={<Profile />} />
                      <Route path="/preferences" element={<Preferences />} />
                      <Route path="/settings" element={<SettingsPage />} />
                    </Route>
                  </Route>

                  {/* ---------------- ADMIN ROUTES ---------------- */}
                  <Route element={<RoleProtectedRoute allowedRoles={["admin"]} />}>
                    <Route element={<Layout />}>
                      <Route path="/admin/users" element={<AdminUsers />} />
                      <Route path="/admin/audit-logs" element={<AdminAuditLogs />} />
                      <Route path="/admin/preferences" element={<AdminPreferences />} />
                    </Route>
                  </Route>

                  {/* ---------------- ERROR ROUTES ---------------- */}
                  <Route path="/500" element={<ServerError />} />
                  <Route path="*" element={<NotFound />} />

                </Routes>
              </RouteErrorBoundary>
            </Suspense>
          </ModalProvider>
        </AvatarProvider>
      </SettingsProvider>
    </AuthProvider>
  );
}
