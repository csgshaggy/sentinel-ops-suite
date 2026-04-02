import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

import { NAV_SCHEMA } from "../navigation/schema";

export default function SidebarLayout() {
  const location = useLocation();

  const categories = [
    { id: "core", label: "Core" },
    { id: "health", label: "Health" },
    { id: "observability", label: "Observability" },
    { id: "anomalies", label: "Anomalies & Alerts" },
    { id: "governance", label: "Governance" },
    { id: "pelm", label: "PELM" },
  ];

  const [open, setOpen] = useState({
    core: true,
    health: true,
    observability: true,
    anomalies: true,
    governance: true,
    pelm: true,
  });

  return (
    <div
      style={{
        width: 260,
        background: "#1e1e1e",
        color: "#fff",
        padding: "20px 0",
        height: "100vh",
        overflowY: "auto",
      }}
    >
      <h2 style={{ paddingLeft: 20 }}>SSRF Console</h2>

      {categories.map((cat) => {
        const items = NAV_SCHEMA.filter((x) => x.category === cat.id);

        return (
          <div key={cat.id} style={{ marginBottom: 10 }}>
            <div
              onClick={() =>
                setOpen((prev) => ({ ...prev, [cat.id]: !prev[cat.id] }))
              }
              style={{
                padding: "10px 20px",
                cursor: "pointer",
                fontWeight: "bold",
                background: "#2a2a2a",
              }}
            >
              {cat.label}
            </div>

            {open[cat.id] &&
              items.map((item) => {
                const active = location.pathname === item.route;

                return (
                  <Link
                    key={item.id}
                    to={item.route}
                    style={{
                      padding: "10px 30px",
                      display: "block",
                      textDecoration: "none",
                      color: active ? "#00eaff" : "#fff",
                      background: active ? "#333" : "transparent",
                    }}
                  >
                    {item.icon} {item.label}
                  </Link>
                );
              })}
          </div>
        );
      })}
    </div>
  );
}
