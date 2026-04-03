import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

const Layout = () => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />
      <div style={{ flex: 1, overflowY: "auto", background: "#0a0a0a", color: "#fff" }}>
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
