import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      "\\.svg$": "/src/__mocks__/fileMock.ts",
    },
  },

  test: {
    environment: "jsdom",
    globals: true,
    mockReset: true,
    assetsInclude: ["**/*.svg"],
    setupFiles: ["./src/test/setup.ts"],
  },
});
