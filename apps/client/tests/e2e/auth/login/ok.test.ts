import test from "@playwright/test";
import { preAuthLogin } from "./pre";
import { genRegisterPayload } from "../../lib/gen";
import { registerUserOk } from "../../lib/fullActions";
import { getByID, getByTxt } from "../../lib/get";
import { clickByID } from "../../lib/click";
import { waitTest, waitURL } from "../../lib/sideActions";

const payload = genRegisterPayload();

test.beforeEach(async ({ page }) => {
  await registerUserOk(page, payload);
});

test("login ok", async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();

  const el = await preAuthLogin(page);

  const email = await getByID(el, "email");
  email.fill(payload.email);

  const pwd = await getByID(el, "password");
  pwd.fill(payload.password);

  await clickByID(el, "login__footer_form__submit_btn");

  await waitURL(page, "/");

  await waitTest(page);

  await getByTxt(page, "operation successful");
});
