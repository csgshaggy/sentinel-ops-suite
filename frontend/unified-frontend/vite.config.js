import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";
import path from "path";   // <-- 🔥 REQUIRED for alias
import { version as pkgVersion } from "./package.json";

// Read version numbers for cache-busting
const version = fs.readFileSync("./version.txt", "utf8").trim();
const logoVersion = fs.readFileSync("./logo-version.txt", "utf8").trim();

export default defineConfig({
  // 🔥 FULLY disable LightningCSS (Vite 8)
  css: {
    transformer: "postcss",     // disable LightningCSS transforms
    minify: "esbuild"           // disable LightningCSS minifier
  },

  esbuild: {
    legalComments: "none"
  },

  // ------------------------------------------------------------
  // 🔥 ADD ALIAS SUPPORT (Validator-safe, project-wide)
  // ------------------------------------------------------------
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },

  plugins: [
    react(),

    {
      name: "inject-version",
      transformIndexHtml(html) {
        let updated = html;

        // Append version to JS bundle
        updated = updated.replace(
          /(<script type="module" crossorigin src="[^"]+")>/,
          `$1?v=${version}>`
        );

        // Append version to CSS bundle
        updated = updated.replace(
          /(<link rel="stylesheet" crossorigin href="[^"]+")>/,
          `$1?v=${version}>`
        );

        // Append version to logo file
        updated = updated.replace(
          /SentinelOps-[A-Za-z0-9]+\.jpg/g,
          (match) => `${match}?v=${logoVersion}`
        );

        return updated;
      },
    },
  ],

  define: {
    __APP_VERSION__: JSON.stringify(pkgVersion),
    "import.meta.env.VITE_LOGO_VERSION": JSON.stringify(logoVersion),
  },

  build: {
    outDir: "dist",
    emptyOutDir: true,
    cssMinify: "esbuild",
  },

  server: {
    port: 5173,
    strictPort: true,
  },
});
