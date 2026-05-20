// src/command-palette/commands.ts
// Command definitions for the Sentinel Ops Console command palette.
// IMPORTANT: No React hooks or navigate() calls at module load time.
// Each command receives `navigate` from the caller at runtime.

export interface Command {
  id: string;
  title: string;
  description?: string;
  run: (navigate: (path: string) => void) => void;
}

export const commands: Command[] = [
  {
    id: "open-mfa-settings",
    title: "Open MFA Settings",
    description: "Navigate to Security → MFA Settings",
    run: (navigate) => {
      navigate("/settings/security/mfa");
    },
  },

  {
    id: "enroll-mfa",
    title: "Enroll in MFA",
    description: "Start MFA enrollment workflow",
    run: (navigate) => {
      navigate("/console/mfa/enroll");
    },
  },

  // Add additional commands here using the same pattern:
  // run: (navigate) => navigate("/your/route")
];
