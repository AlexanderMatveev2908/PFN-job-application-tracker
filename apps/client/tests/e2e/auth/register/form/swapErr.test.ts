import test from "@playwright/test";
import { getByID } from "../../../lib/shortcuts/get";
import { clickByID } from "../../../lib/shortcuts/click";
import { checkIsFocused } from "../../../lib/shortcuts/check";
import { waitTmr } from "../../../lib/actions/sideActions";
import { preAuthRegister } from "../pre";

test("swap err mgmt", async ({ page }) => {
  const el = await preAuthRegister(page);

  const firstName = await getByID(el, "first_name");

  await firstName.fill("validFirstName");

  await clickByID(el, "btns_swapper_next_swap");

  await waitTmr(page);

  const pwd = await getByID(el, "password");
  await checkIsFocused(pwd);

  await clickByID(el, "register__form__submit");

  await waitTmr(page);
  const lastName = await getByID(el, "last_name");
  await checkIsFocused(lastName);

  await clickByID(el, "btns_swapper_next_swap");

  await waitTmr(page);

  await checkIsFocused(pwd);

  await clickByID(el, "btns_swapper_prev_swap");

  await waitTmr(page);

  await checkIsFocused(firstName);
});
