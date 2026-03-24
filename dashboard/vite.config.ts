import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      // Mock SVG imports during tests
      "\\.svg$": "/src/__mocks__/fileMock.ts",
    },
  },

  test: {
    environment: "jsdom",
    globals: true,
    mockReset: true,

    // Allow Vitest to treat SVGs as static assets
    assetsInclude: ["**/*.svg"],

    // Load React Testing Library matchers
    setupFiles: ["./src/test/setup.ts"],
  },
});
