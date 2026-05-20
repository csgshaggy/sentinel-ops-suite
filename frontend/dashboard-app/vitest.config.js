// vitest.config.js — React 19 + Vite 5
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./setupTests.js",
    coverage: {
      reporter: ["text", "html"],
    }
  }
});
