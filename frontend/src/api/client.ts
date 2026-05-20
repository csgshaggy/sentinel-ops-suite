// SentinelOps Unified API Client (fetch-based)
// Deterministic, drift-proof, aligned with backend router corrections.

export const API_BASE = "/api";

// ---------------------------------------------------------------------------
// Core request helper
// ---------------------------------------------------------------------------

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("access_token");

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers,
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

export const AuthAPI = {
  login: (data: { username: string; password: string }) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  logout: () => request("/auth/logout", { method: "POST" }),

  me: () => request("/auth/me"),
};

// ---------------------------------------------------------------------------
// Users
// ---------------------------------------------------------------------------

export const UsersAPI = {
  list: () => request("/users"),
  get: (userId: number) => request(`/users/${userId}`),
  create: (data: any) =>
    request("/users", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

// ---------------------------------------------------------------------------
// Admin
// ---------------------------------------------------------------------------

export const AdminAPI = {
  createUser: (data: any) =>
    request("/admin/create-user", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

// ---------------------------------------------------------------------------
// Sessions
// ---------------------------------------------------------------------------

export const SessionsAPI = {
  create: (data: any) =>
    request("/sessions", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listForUser: (userId: number) =>
    request(`/sessions/user/${userId}`),

  invalidate: (sessionId: number) =>
    request(`/sessions/${sessionId}`, {
      method: "DELETE",
    }),

  listAll: () => request("/sessions/all"),
};

// ---------------------------------------------------------------------------
// Logs (SSE)
// ---------------------------------------------------------------------------

export const LogsAPI = {
  stream: () => new EventSource(`${API_BASE}/stream/logs`),
};

// ---------------------------------------------------------------------------
// Plugins
// ---------------------------------------------------------------------------

export const PluginsAPI = {
  list: () => request("/plugins"),
  get: (pluginId: string) => request(`/plugins/${pluginId}`),
  run: (pluginId: string) =>
    request(`/plugins/${pluginId}/run`, {
      method: "POST",
    }),
  logs: (pluginId: string) => request(`/plugins/${pluginId}/logs`),
  timing: () => request("/plugins/timing"),
};

// ---------------------------------------------------------------------------
// Repo Health
// ---------------------------------------------------------------------------

export const RepoHealthAPI = {
  health: () => request("/repo/health"),
};

// ---------------------------------------------------------------------------
// Router Drift
// ---------------------------------------------------------------------------

export const RouterDriftAPI = {
  scan: () => request("/plugins/router-drift"),
};

// ---------------------------------------------------------------------------
// CI Summary
// ---------------------------------------------------------------------------

export const CISummaryAPI = {
  summary: () => request("/ci/summary"),
};

// ---------------------------------------------------------------------------
// Workflow Runs
// ---------------------------------------------------------------------------

export const WorkflowRunsAPI = {
  list: (limit = 20) => request(`/workflow-runs/?limit=${limit}`),
};
