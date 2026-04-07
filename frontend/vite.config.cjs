import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      "@loginStyles": path.resolve(__dirname, "src/pages/Login.css"),
    },
  },

  // Ensure Vite processes index.html and bundles the app
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, "index.html"),
    },
  },

  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
