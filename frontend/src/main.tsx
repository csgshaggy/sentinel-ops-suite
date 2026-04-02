import "./index.css";

import React from "react";
import ReactDOM from "react-dom/client";

import NotificationCenter from "./components/NotificationCenter";
import { AuthProvider } from "./context/AuthContext";
import AppRouter from "./router/AppRouter";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <AuthProvider>
      <NotificationCenter />
      <AppRouter />
    </AuthProvider>
  </React.StrictMode>
);
