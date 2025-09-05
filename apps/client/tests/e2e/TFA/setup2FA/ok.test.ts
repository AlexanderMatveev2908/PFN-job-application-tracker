import test from "@playwright/test";
import { getAccessManageAccVerified } from "../../lib/idx";

test("setup 2FA ok", async ({ browser }) => {
  const { swap } = await getAccessManageAccVerified(browser);
});
