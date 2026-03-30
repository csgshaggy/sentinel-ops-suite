// ESLint Flat Config for Vite + React + Prettier + Import Sorting (ESLint 8.x)

import js from "@eslint/js";
import globals from "globals";

import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import jsxA11yPlugin from "eslint-plugin-jsx-a11y";
import prettierPlugin from "eslint-plugin-prettier";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default [
  {
    files: ["**/*.{js,jsx,ts,tsx}"],

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },

    // React plugin requires this to avoid warnings
    settings: {
      react: {
        version: "detect",
      },
    },

    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
      "jsx-a11y": jsxA11yPlugin,
      prettier: prettierPlugin,
      "simple-import-sort": simpleImportSort,
    },

    rules: {
      // Base JS rules
      ...js.configs.recommended.rules,

      // React rules
      ...reactPlugin.configs.recommended.rules,
      ...reactPlugin.configs["jsx-runtime"].rules,

      // Hooks rules
      ...reactHooksPlugin.configs.recommended.rules,

      // Accessibility rules
      ...jsxA11yPlugin.configs.recommended.rules,

      // Prettier formatting
      "prettier/prettier": "warn",

      // Import sorting
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",

      // React 17+ JSX transform
      "react/react-in-jsx-scope": "off",
    },
  },
];
