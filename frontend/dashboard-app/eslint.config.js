// eslint.config.js — Dashboard App (React 19 + Vite 5 + ESLint 9)
import js from "@eslint/js";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";

export default [
  {
    files: ["**/*.{js,jsx,ts,tsx}"],

    ignores: [
      "dist/**",
      "node_modules/**",
      ".vite/**",
      "coverage/**"
    ],

    languageOptions: {
      parser: tsparser,
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        // Browser globals
        window: "readonly",
        document: "readonly",
        localStorage: "readonly",
        sessionStorage: "readonly",
        navigator: "readonly",
        fetch: "readonly",
        EventSource: "readonly",
        KeyboardEvent: "readonly",
        HTMLElement: "readonly",
        console: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",

        // Vitest globals
        test: "readonly",
        expect: "readonly",
        describe: "readonly",
        beforeEach: "readonly",
        afterEach: "readonly"
      }
    },

    plugins: {
      react,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
      "@typescript-eslint": tseslint
    },

    settings: {
      react: {
        version: "detect"
      }
    },

    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,

      // React 17+ / 19 JSX transform
      "react/react-in-jsx-scope": "off",

      // Disable PropTypes (TS + React 19)
      "react/prop-types": "off",

      // Vite + React Fast Refresh
      "react-refresh/only-export-components": "warn",

      // TS-friendly unused vars
      "@typescript-eslint/no-unused-vars": "warn",
      "no-unused-vars": "off"
    }
  }
];
