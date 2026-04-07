// File: /home/ubuntu/sentinel-ops-suite/frontend/src/main.tsx

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import "./index.css";

// ✅ Correct AuthProvider import
import { AuthProvider } from "./context/AuthContext";

console.log("SENTINEL_TEST_MARKER");

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* ⭐ This was missing — now your login page can mount */}
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
