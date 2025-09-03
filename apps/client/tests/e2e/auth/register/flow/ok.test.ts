import test from "@playwright/test";
import { registerUserOk } from "../../../lib/actions/auth";

test("register ok", async ({ browser }) => {
  await registerUserOk(browser);
});
