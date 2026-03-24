import { vi } from "vitest";

/**
 * A lightweight mock of an authenticated page object.
 * This replaces the Playwright-based fixture and allows
 * Vitest to run without a browser environment.
 */
export async function authPage() {
  return {
    getByText: (pattern: RegExp) => {
      // Simulate a DOM lookup
      if (/dashboard/i.test(pattern.source)) {
        return { textContent: "Dashboard" };
      }
      return null;
    },
    goto: vi.fn(),
    fill: vi.fn(),
    click: vi.fn(),
    waitForURL: vi.fn(),
  };
}
