// File: /home/ubuntu/sentinel-ops-suite/frontend/src/features/dashboard/Dashboard.jsx

import { useEffect, useState } from "react";
import "./dashboard.css";

export default function Dashboard() {
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        const storedId = localStorage.getItem("user_id");
        setUserId(storedId);
    }, []);

    return (
        <div className="dashboard-root">
            {/* Sidebar */}
            <aside className="dashboard-sidebar">
                <h2 className="sidebar-title">SentinelOps</h2>
                <nav className="sidebar-nav">
                    <a href="/dashboard">Dashboard</a>
                    <a href="/alerts">Alerts</a>
                    <a href="/systems">Systems</a>
                    <a href="/settings">Settings</a>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="dashboard-main">
                <header className="dashboard-header">
                    <h1>Analyst Dashboard</h1>
                    <span className="user-info">Logged in as {userId}</span>
                </header>

                <section className="dashboard-content">
                    <p className="welcome-msg">
                        Welcome to the operational dashboard. Your tiles, alerts, and system metrics will appear here.
                    </p>

                    {/* Tile Grid Placeholder */}
                    <div className="tile-grid">
                        {/* Tiles will be added in later steps */}
                    </div>
                </section>
            </main>
        </div>
    );
}
