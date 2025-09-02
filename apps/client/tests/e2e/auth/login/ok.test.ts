import test from "@playwright/test";
import { genRegisterPayload } from "../../lib/payloads";
import { loginUserOk, registerUserOk } from "../../lib/fullActions";

const payload = genRegisterPayload();

test.beforeEach(async ({ page }) => {
  await registerUserOk(page, payload);
});

test("login ok", async ({ browser }) => {
  await loginUserOk(browser);
});
