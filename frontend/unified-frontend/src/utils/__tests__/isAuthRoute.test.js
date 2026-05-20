// /src/utils/__tests__/isAuthRoute.test.js

import { describe, it, expect } from "vitest";
import { isAuthRoute } from "../isAuthRoute.js";

describe("isAuthRoute()", () => {
  // PUBLIC / AUTH ROUTES
  const publicRoutes = [
    "/login",
    "/login/reset",
    "/login/mfa",
    "/mfa",
    "/mfa/verify",
    "/reset-password",
    "/reset-password/123",
    "/reset-password-request",
    "/forgot-password",
    "/auth",
    "/auth/callback"
  ];

  publicRoutes.forEach((route) => {
    it(`should treat PUBLIC route "${route}" as public`, () => {
      expect(isAuthRoute(route)).toBe(true);
    });
  });

  // ADMIN ROUTES (NEVER PUBLIC)
  const adminRoutes = [
    "/admin",
    "/admin/",
    "/admin/dashboard",
    "/admin/security",
    "/admin/settings",
    "/admin/users",
    "/admin/audit-logs",
    "/admin/session-metrics"
  ];

  adminRoutes.forEach((route) => {
    it(`should NOT treat ADMIN route "${route}" as public`, () => {
      expect(isAuthRoute(route)).toBe(false);
    });
  });

  // RANDOM NON-AUTH ROUTES
  const privateRoutes = [
    "/",
    "/home",
    "/status",
    "/health",
    "/docs",
    "/api",
    "/something-else"
  ];

  privateRoutes.forEach((route) => {
    it(`should NOT treat PRIVATE route "${route}" as public`, () => {
      expect(isAuthRoute(route)).toBe(false);
    });
  });

  // SUBSTRING COLLISION PROTECTION
  it("should NOT treat '/admin/security/reset-password' as public", () => {
    expect(isAuthRoute("/admin/security/reset-password")).toBe(false);
  });

  it("should treat '/reset-password/flow' as public", () => {
    expect(isAuthRoute("/reset-password/flow")).toBe(true);
  });

  // EXACT MATCH VS PREFIX MATCH
  it("should treat '/auth' as public", () => {
    expect(isAuthRoute("/auth")).toBe(true);
  });

  it("should treat '/auth/anything' as public", () => {
    expect(isAuthRoute("/auth/anything")).toBe(true);
  });

  it("should NOT treat '/authentication' as public", () => {
    expect(isAuthRoute("/authentication")).toBe(false);
  });
});
