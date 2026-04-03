import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";

// Global theme provider (dark/light + tokens)
import { ThemeProvider } from "./theme/ThemeProvider";

// Global CSS resets or base styles (optional but recommended)
import "./styles/global.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
