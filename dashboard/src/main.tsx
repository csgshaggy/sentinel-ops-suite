// =====================================================================
// SSRF Command Console — Root Entrypoint (main.tsx)
// Wraps entire app in global providers + router
// =====================================================================

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import AppRoutes from "./routes/AppRoutes";

// Global Providers
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import { LayoutProvider } from "./context/LayoutContext";
import { NotificationProvider } from "./context/NotificationContext";

// Global UI
import NotificationCenter from "./components/NotificationCenter";

// Global Styles
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <ThemeProvider>
        <NotificationProvider>
          <LayoutProvider>
            <BrowserRouter>
              <AppRoutes />
              <NotificationCenter />
            </BrowserRouter>
          </LayoutProvider>
        </NotificationProvider>
      </ThemeProvider>
    </AuthProvider>
  </React.StrictMode>
);
