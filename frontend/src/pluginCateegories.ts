// ---------------------------------------------
// Plugin Category Definitions (Typed)
// ---------------------------------------------

export type PluginCategoryId = "system" | "python" | "project" | "observability";

export interface PluginCategory {
  id: PluginCategoryId;
  label: string;
  description?: string;
}

// Central registry of plugin categories
export const pluginCategories: PluginCategory[] = [
  {
    id: "system",
    label: "System & OS Health",
    description: "Kernel, hardware, processes, memory, CPU, disk, and OS-level diagnostics.",
  },
  {
    id: "python",
    label: "Python Environment",
    description: "Interpreter, venv, packages, dependency drift, and runtime validation.",
  },
  {
    id: "project",
    label: "Project / Repo Integrity",
    description: "Repo structure, docs, Makefile, CI config, linting, and code health.",
  },
  {
    id: "observability",
    label: "Observability & Diagnostics",
    description: "Logging, metrics, tracing, performance, and runtime instrumentation.",
  },
];

// Helper to look up category metadata
export function getCategory(id: string): PluginCategory | undefined {
  return pluginCategories.find((c) => c.id === id);
}
