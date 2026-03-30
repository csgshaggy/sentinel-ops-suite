import React from "react";
import ReactDOM from "react-dom/client";
import AppRouter from "./router/AppRouter";
import { AuthProvider } from "./context/AuthContext";
import NotificationCenter from "./components/NotificationCenter";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <AuthProvider>
      <NotificationCenter />
      <AppRouter />
    </AuthProvider>
  </React.StrictMode>,
);
