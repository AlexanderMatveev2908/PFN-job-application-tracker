import test from "@playwright/test";
import { loginUserOk } from "../../lib/actions/auth";

test("login ok", async ({ browser }) => {
  await loginUserOk(browser);
});
