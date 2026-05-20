// frontend/dashboard-app/src/services/healthService.js

import { get } from "./apiService";

export function getSystemHealth() {
  return get("/health/system");
}

export function getRepoHealth() {
  return get("/health/repo");
}

export function getGitHealth() {
  return get("/health/git");
}

export function getServiceStatus() {
  return get("/health/services");
}
