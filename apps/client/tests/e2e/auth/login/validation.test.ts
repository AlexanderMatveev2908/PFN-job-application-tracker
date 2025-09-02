import test from "@playwright/test";
import { preAuthLogin } from "./pre";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { waitTmr } from "../../lib/actions/sideActions";
import { clickByID } from "../../lib/shortcuts/click";
import { checkIsFocused } from "../../lib/shortcuts/check";

test("validation", async ({ page }) => {
  const el = await preAuthLogin(page);

  const email = await getByID(el, "email");

  await email.fill("<>@<>");

  waitTmr(page);

  await getByTxt(page, "invalid email");

  const pwd = await getByID(el, "password");

  await pwd.fill("12345");

  await waitTmr(page);

  await getByTxt(page, "invalid password");

  await clickByID(el, "login__form__submit");

  await waitTmr(page);

  await checkIsFocused(email);
});
