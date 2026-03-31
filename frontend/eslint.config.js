import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default [
  // Base JS rules
  js.configs.recommended,

  // ---------------------------------------------------------
  // JS / JSX FILES
  // ---------------------------------------------------------
  {
    files: ["**/*.js", "**/*.jsx"],
    ignores: ["dist/**", "node_modules/**", "src/__mocks__/**"],

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },

    plugins: {
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      "simple-import-sort": simpleImportSort,
    },

    rules: {
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",

      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },

    settings: {
      react: { version: "detect" },
    },
  },

  // ---------------------------------------------------------
  // TS / TSX FILES
  // ---------------------------------------------------------
  {
    files: ["**/*.ts", "**/*.tsx"],
    ignores: ["dist/**", "node_modules/**", "src/__mocks__/**"],

    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },

    plugins: {
      "@typescript-eslint": tseslint,
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      "simple-import-sort": simpleImportSort,
    },

    rules: {
      "simple-import-sort/imports": "warn",
      "simple-import-sort/exports": "warn",

      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },

    settings: {
      react: { version: "detect" },
    },
  },
];
