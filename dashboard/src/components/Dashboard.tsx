// dashboard/src/components/Dashboard.tsx

import React, { useEffect, useState, useMemo } from "react";
import { Plugin, TimingBucket } from "../types";

import { fetchPlugins, fetchTimingBuckets } from "../api/client";

import DetailDrawer from "./DetailDrawer";
import PluginTable from "./PluginTable";
import SearchBar from "./SearchBar";
import FilterBar from "./FilterBar";
import CategoryFilterBar from "./CategoryFilterBar";

import ChartsPanel from "../widgets/ChartsPanel";
import MakefileDiffViewer from "../widgets/MakefileDiffViewer";
import HealthSummaryWidget from "../widgets/HealthSummaryWidget";

import useAutoRefresh from "../hooks/useAutoRefresh";

export default function Dashboard() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [timing, setTiming] = useState<TimingBucket[]>([]);
  const [selectedPlugin, setSelectedPlugin] = useState<Plugin | null>(null);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("all");

  // ------------------------------------------------------------
  // Load plugin + timing data
  // ------------------------------------------------------------
  const loadData = async () => {
    try {
      const [pluginData, timingData] = await Promise.all([
        fetchPlugins(),
        fetchTimingBuckets(),
      ]);

      setPlugins(pluginData);
      setTiming(timingData);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  useAutoRefresh(loadData, 10000);

  // ------------------------------------------------------------
  // Dynamic categories
  // ------------------------------------------------------------
  const categories = useMemo(() => {
    const set = new Set<string>();
    plugins.forEach((p) => set.add(p.category));
    return Array.from(set).sort();
  }, [plugins]);

  // ------------------------------------------------------------
  // Filtering logic
  // ------------------------------------------------------------
  const filteredPlugins = plugins.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.id.toLowerCase().includes(search.toLowerCase());

    const matchesStatus = statusFilter === "all" || p.status === statusFilter;

    const matchesCategory =
      categoryFilter === "all" || p.category === categoryFilter;

    return matchesSearch && matchesStatus && matchesCategory;
  });

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  return (
    <div style={{ padding: "1.5rem" }}>
      <h1 style={{ marginBottom: "1rem" }}>Operator Console</h1>

      <div style={{ display: "flex", gap: "1.5rem" }}>
        {/* --------------------------------------------------------
            Sidebar column: Health + Makefile Panel
        -------------------------------------------------------- */}
        <div
          style={{
            width: "320px",
            flexShrink: 0,
            display: "flex",
            flexDirection: "column",
            gap: "1.5rem",
          }}
        >
          <HealthSummaryWidget />

          <div
            style={{
              background: "var(--bg-panel)",
              border: "1px solid var(--border)",
              borderRadius: "6px",
              padding: "1rem",
            }}
          >
            <h3 style={{ marginBottom: "0.75rem" }}>Makefile Status</h3>
            <MakefileDiffViewer />
          </div>
        </div>

        {/* --------------------------------------------------------
            Main column: Charts + Filters + Plugin Table
        -------------------------------------------------------- */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <ChartsPanel timing={timing} />

          <div style={{ marginTop: "1.5rem" }}>
            <SearchBar value={search} onChange={setSearch} />
            <FilterBar value={statusFilter} onChange={setStatusFilter} />
            <CategoryFilterBar
              value={categoryFilter}
              onChange={setCategoryFilter}
              categories={categories}
            />
          </div>

          <PluginTable
            plugins={filteredPlugins}
            onSelect={(plugin) => setSelectedPlugin(plugin)}
          />
        </div>
      </div>

      <DetailDrawer
        plugin={selectedPlugin}
        onClose={() => setSelectedPlugin(null)}
      />
    </div>
  );
}
