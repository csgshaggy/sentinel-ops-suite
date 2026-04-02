// ---------------------------------------------------------
// Sentinel Ops Suite — Frontend ESLint Flat Config
// Vite + React + TypeScript + Browser + Node Globals
// ---------------------------------------------------------

import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default [
  js.configs.recommended,

  {
    files: ["**/*.{js,jsx,ts,tsx}"],

    languageOptions: {
      parser: tsparser,
      ecmaVersion: "latest",
      sourceType: "module",

      globals: {
        // Browser globals
        window: "readonly",
        document: "readonly",
        console: "readonly",
        fetch: "readonly",
        EventSource: "readonly",
        KeyboardEvent: "readonly",
        HTMLElement: "readonly",
        HTMLDivElement: "readonly",
        localStorage: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        setTimeout: "readonly",
        alert: "readonly",
        crypto: "readonly",

        // Node globals
        __dirname: "readonly",
        process: "readonly",
        require: "readonly",
        module: "readonly",
      },
    },

    settings: {
      react: {
        version: "detect",
      },
    },

    plugins: {
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      "simple-import-sort": simpleImportSort,
      "@typescript-eslint": tseslint,
    },

    rules: {
      // Import sorting
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",

      // React
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",

      // Hooks
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // TS unused vars
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["warn"],

      // Accessibility
      "jsx-a11y/anchor-is-valid": "warn",
    },
  },

  // Node-only overrides
  {
    files: ["scripts/**/*.cjs", "*.config.js", "*.config.cjs"],
    languageOptions: {
      globals: {
        require: "readonly",
        module: "readonly",
        __dirname: "readonly",
        process: "readonly",
        console: "readonly",
      },
    },
  },
];
