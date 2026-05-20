import { mfaCommands } from "./commands";

const allCommands = [
  ...systemCommands,
  ...navigationCommands,
  ...consoleCommands,
  ...mfaCommands, // ← NEW
];
