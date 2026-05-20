// /src/main.jsx

import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import router from "./router.jsx";
import { AuthProvider } from "./features/auth/AuthContext.jsx";

import "./styles/theme.css";
import "./styles/global.css";
import "./styles/session-expire.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <AuthProvider>
    <RouterProvider router={router} />
  </AuthProvider>
);
