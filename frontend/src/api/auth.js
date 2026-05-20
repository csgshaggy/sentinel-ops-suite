// File: src/api/auth.js

import api from "./client";

export async function login(username, password) {
  const res = await api.post("/auth/login", { username, password });
  return res.data;
}

export async function getCurrentUser() {
  const res = await api.get("/api/users/me");
  return res.data;
}
