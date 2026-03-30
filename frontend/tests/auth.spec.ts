import { test, expect } from "vitest";
import { authPage } from "./fixtures/auth.fixture";

test("authenticated dashboard view", async () => {
  const page = await authPage();
  const result = page.getByText(/dashboard/i);

  expect(result).toBeTruthy();
});
