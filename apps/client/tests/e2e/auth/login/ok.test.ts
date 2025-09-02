import test from "@playwright/test";
import { loginUserOk, registerUserOk } from "../../lib/actions/fullActions";
import { genRegisterPayload } from "../../lib/idx";

const payload = genRegisterPayload();

test.beforeEach(async ({ page }) => {
  await registerUserOk(page, payload);
});

test("login ok", async ({ browser }) => {
  await loginUserOk(browser);
});
