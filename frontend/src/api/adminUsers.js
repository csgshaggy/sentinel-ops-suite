// src/api/adminUsers.js

export async function fetchUsers() {
  const res = await fetch("/api/admin/users", {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function toggleUserActive(id, is_active) {
  const res = await fetch(`/api/admin/users/${id}/active`, {
    method: "PATCH",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_active }),
  });
  if (!res.ok) throw new Error("Failed to update user");
  return res.json();
}

export async function resetUserPassword(id) {
  const res = await fetch(`/api/admin/users/${id}/reset-password`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to reset password");
  return res.json();
}

