import test from "@playwright/test";
import { preAuthLogin } from "./pre";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { clickByID } from "../../lib/shortcuts/click";
import { checkIsFocused } from "../../lib/shortcuts/check";
import { waitTmr } from "../../lib/shortcuts/wait";

test("login validation", async ({ browser }) => {
  const { form, page } = await preAuthLogin(browser);

  const email = await getByID(form, "email");

  await email.fill("<>@<>");

  waitTmr(page);

  await getByTxt(page, "invalid email");

  const pwd = await getByID(form, "password");

  await pwd.fill("12345");

  await waitTmr(page);

  await getByTxt(page, "invalid password");

  await clickByID(form, "login__form__submit");

  await waitTmr(page);

  await checkIsFocused(email);
});
