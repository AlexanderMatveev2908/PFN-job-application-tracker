import test from "@playwright/test";
import { registerUserOk } from "../../../lib/fullActions";

test("register ok", async ({ page }) => {
  await registerUserOk(page);
});
