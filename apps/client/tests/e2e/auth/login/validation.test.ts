import test from "@playwright/test";
import { preAuthLogin } from "./pre";
import { getByID, getByTxt } from "../../lib_tests/shortcuts/get";
import { clickByID } from "../../lib_tests/shortcuts/click";
import { checkIsFocused } from "../../lib_tests/shortcuts/check";
import { waitTmr } from "../../lib_tests/shortcuts/wait";

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
