export const roles = {
  admin: {
    canAccess: ["ci-summary", "repo-health", "workflow-runs"],
  },
  operator: {
    canAccess: ["ci-summary", "repo-health"],
  },
  viewer: {
    canAccess: ["ci-summary"],
  },
};
