import test from "@playwright/test";
import { preAuthLogin } from "./pre";
import { getByID, getByTxt } from "../../lib/get";
import { waitTest } from "../../lib/sideActions";
import { clickByID } from "../../lib/click";
import { checkIsFocused } from "../../lib/check";

test("validation", async ({ page }) => {
  const el = await preAuthLogin(page);

  const email = await getByID(el, "email");

  await email.fill("<>@<>");

  waitTest(page);

  await getByTxt(page, "invalid email");

  const pwd = await getByID(el, "password");

  await pwd.fill("12345");

  await waitTest(page);

  await getByTxt(page, "invalid password");

  await clickByID(el, "login__form__submit");

  await waitTest(page);

  await checkIsFocused(email);
});
