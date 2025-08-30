import test from "@playwright/test";
import { pre } from "./pre";
import { getByID } from "../../../lib/get";
import { clickByID } from "../../../lib/click";
import { checkIsFocused } from "../../../lib/check";
import { waitTest } from "../../../lib/sideActions";

test("err management", async ({ page }) => {
  const el = await pre(page);

  const firstName = await getByID(el, "first_name");

  await firstName.fill("validFirstName");

  await clickByID(el, "btns_swapper_next_swap");

  await waitTest(page);

  const pwd = await getByID(el, "password");
  await checkIsFocused(pwd);

  await clickByID(el, "register__footer_form__submit_btn");

  await waitTest(page);
  const lastName = await getByID(el, "last_name");
  await checkIsFocused(lastName);

  await clickByID(el, "btns_swapper_next_swap");

  await waitTest(page);

  await checkIsFocused(pwd);

  await clickByID(el, "btns_swapper_prev_swap");

  await waitTest(page);

  await checkIsFocused(firstName);
});
