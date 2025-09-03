import test from "@playwright/test";
import { getByID } from "../../../lib/shortcuts/get";
import { clickByID } from "../../../lib/shortcuts/click";
import { checkIsFocused } from "../../../lib/shortcuts/check";
import { preAuthRegister } from "../pre";
import { waitTmr } from "../../../lib/shortcuts/wait";

test("register form swap err mgmt", async ({ browser }) => {
  const { form, page } = await preAuthRegister(browser);

  const firstName = await getByID(form, "first_name");

  await firstName.fill("validFirstName");

  await clickByID(form, "btns_swapper_next_swap");

  await waitTmr(page);

  const pwd = await getByID(form, "password");
  await checkIsFocused(pwd);

  await clickByID(form, "register__form__submit");

  await waitTmr(page);
  const lastName = await getByID(form, "last_name");
  await checkIsFocused(lastName);

  await clickByID(form, "btns_swapper_next_swap");

  await waitTmr(page);

  await checkIsFocused(pwd);

  await clickByID(form, "btns_swapper_prev_swap");

  await waitTmr(page);

  await checkIsFocused(firstName);
});
