// src/command-palette/index.ts

import { commands as mfaCommands } from "./commands";

// If you have other command groups, import them here:
// import { commands as systemCommands } from "./system";
// import { commands as navigationCommands } from "./navigation";
// import { commands as consoleCommands } from "./console";

export const allCommands = [
  // ...systemCommands,
  // ...navigationCommands,
  // ...consoleCommands,
  ...mfaCommands,
];
