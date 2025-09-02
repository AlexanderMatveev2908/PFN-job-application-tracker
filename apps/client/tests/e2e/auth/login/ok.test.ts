import test from "@playwright/test";
import { loginUserOk } from "../../lib/actions/fullActions";

test("login ok", async ({ browser }) => {
  await loginUserOk(browser);
});
