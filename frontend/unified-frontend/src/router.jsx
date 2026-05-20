// /src/router.jsx

import React from "react";
import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";

import App from "./App.jsx";

// Public pages
import LoginPage from "./pages/Login.jsx";
import MFACode from "./pages/MFACode.jsx";

// User pages
import Dashboard from "./pages/Dashboard.jsx";
import SettingsPage from "./pages/settings.jsx";
import Profile from "./pages/Profile/Profile.jsx";   // <-- ADDED

// Admin pages
import AdminPanel from "./pages/AdminPanel.jsx";
import DashboardPage from "./pages/admin/DashboardPage.jsx";
import SecurityPage from "./pages/admin/SecurityPage.jsx";
import UsersPage from "./pages/admin/UsersPage.jsx";
import AuditLogsPage from "./pages/admin/AuditLogsPage.jsx";

// Layouts
import Layout from "./components/Layout.jsx";
import ProtectedLayout from "./layouts/ProtectedLayout.jsx";

// Route guards
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import RoleProtectedRoute from "./components/RoleProtectedRoute.jsx";

// Errors
import NotFound from "./pages/NotFound.jsx";
import ServerError from "./pages/ServerError.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      //
      // PUBLIC ROUTES
      //
      { index: true, element: <Navigate to="/login" replace /> },
      { path: "login", element: <LoginPage /> },
      { path: "mfa", element: <MFACode /> },

      //
      // AUTHENTICATED ROUTES
      //
      {
        element: (
          <ProtectedRoute>
            <Outlet />
          </ProtectedRoute>
        ),
        children: [
          {
            element: <ProtectedLayout />,
            children: [
              {
                element: <Layout />,
                children: [
                  //
                  // USER ROUTES
                  //
                  { path: "dashboard", element: <Dashboard /> },
                  { path: "settings", element: <SettingsPage /> },
                  { path: "profile", element: <Profile /> },   // <-- ADDED HERE

                  //
                  // ADMIN ROUTES
                  //
                  {
                    path: "admin",
                    element: (
                      <RoleProtectedRoute allowedRoles={["admin"]}>
                        <Outlet />
                      </RoleProtectedRoute>
                    ),
                    children: [
                      { index: true, element: <AdminPanel /> },
                      { path: "dashboard", element: <DashboardPage /> },
                      { path: "security", element: <SecurityPage /> },
                      { path: "users", element: <UsersPage /> },
                      { path: "audit-logs", element: <AuditLogsPage /> },
                      { path: "settings", element: <SettingsPage /> },
                    ],
                  },
                ],
              },
            ],
          },
        ],
      },

      //
      // ERROR ROUTES
      //
      { path: "500", element: <ServerError /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

export default router;
