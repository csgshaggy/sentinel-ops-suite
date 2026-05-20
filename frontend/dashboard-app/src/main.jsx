import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

import "./index.css";

// GLOBAL LAYOUT STYLES (Option A)
import "./styles/topbar.css";
import "./styles/sidebar.css";
import "./styles/layout.css";

// SETTINGS UI (Unified CSS)
import "./styles/settings.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
