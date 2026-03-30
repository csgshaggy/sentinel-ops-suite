// =====================================================================
// SSRF Command Console — Admin API Client
// Users • Password Reset • Audit Logs • Metrics
// =====================================================================

export async function fetchUsers() {
  const res = await fetch("/admin/users", {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function createUser(payload) {
  const res = await fetch("/admin/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create user");
  return res.json();
}

export async function updateUser(id, payload) {
  const res = await fetch(`/admin/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update user");
  return res.json();
}

export async function resetUserPassword(id) {
  const res = await fetch(`/admin/users/${id}/reset-password`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to reset password");
  return res.json();
}

export async function fetchAuditLogs() {
  const res = await fetch("/admin/audit-logs", {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to fetch audit logs");
  return res.json();
}

export async function fetchMetrics() {
  const res = await fetch("/admin/metrics", {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to fetch metrics");
  return res.json();
}
