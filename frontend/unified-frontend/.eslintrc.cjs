// /home/ubuntu/sentinel-ops-suite/frontend/unified-frontend/.eslintrc.cjs
// Phase 5 — Fully configured ESLint for unused variable cleanup + React hooks

module.exports = {
  env: {
    browser: true,
    es2021: true,
  },

  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
  ],

  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },

  plugins: ["react", "react-hooks", "unused-imports"],

  settings: {
    react: {
      version: "detect",
    },
  },

  rules: {
    // Auto-remove unused imports
    "unused-imports/no-unused-imports": "error",

    // Auto-remove unused variables
    "unused-imports/no-unused-vars": [
      "error",
      {
        vars: "all",
        varsIgnorePattern: "^_",
        args: "after-used",
        argsIgnorePattern: "^_",
      },
    ],

    // React 17+ / 18+ JSX transform
    "react/react-in-jsx-scope": "off",

    // Optional: reduce noise from prop-types if not used
    "react/prop-types": "off",
  },
};
