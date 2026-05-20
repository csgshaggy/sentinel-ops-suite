import { Router } from "express";
import { execSync } from "child_process";

const router = Router();

router.get("/health", async (req, res) => {
  try {
    // Run the validator
    execSync("make validate-makefile", { stdio: "ignore" });

    // Run the linter
    execSync("make lint-makefile", { stdio: "ignore" });

    // Run drift detector
    execSync("make check-makefile-drift", { stdio: "ignore" });

    return res.json({
      ok: true,
      score: 100,
      detail: "Makefile is valid, linted, and drift-free",
    });
  } catch (err) {
    return res.json({
      ok: false,
      score: 40,
      detail: "Makefile failed validation, linting, or drift check",
    });
  }
});

export default router;
