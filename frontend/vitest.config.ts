import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

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
