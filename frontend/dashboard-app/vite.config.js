import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // Ensures all JS/CSS assets resolve under /admin/
  base: "/admin/",

  plugins: [react()],

  build: {
    // Required for NGINX + multi-app deployments
    manifest: true,
    manifestFileName: "manifest.json",

    // Output directory for the admin-app
    outDir: "dist",

    // Assets folder inside dist
    assetsDir: "assets",

    // Ensures old builds don't linger and cause drift
    emptyOutDir: true,

    // Ensures modern output and avoids legacy polyfills
    target: "esnext",

    // Prevent Vite from adding crossorigin to script tags
    rollupOptions: {
      output: {
        entryFileNames: "assets/[name]-[hash].js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash].[ext]"
      }
    }
  },

  // Ensures Vite does NOT inject crossorigin into built script tags
  experimental: {
    renderBuiltUrl(filename) {
      return `/admin/${filename}`;
    }
  }
});
