import test from "@playwright/test";
import { registerUserOk } from "../../../lib/actions/fullActions";

test("register ok", async ({ page }) => {
  await registerUserOk(page);
});
