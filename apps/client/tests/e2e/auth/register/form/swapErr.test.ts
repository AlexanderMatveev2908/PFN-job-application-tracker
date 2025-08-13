import test, { expect } from "@playwright/test";
import { pre } from "./pre";
import { getByID } from "../../../lib/get";
import { clickByID } from "../../../lib/click";

test("err management", async ({ page }) => {
  const el = await pre(page);

  const firstName = await getByID(el, "first_name");

  await firstName.fill("validFirstName");

  await clickByID(el, "btns_swapper_next_swap");

  await page.waitForTimeout(500);

  const pwd = await getByID(el, "password");
  await expect(pwd).toBeFocused();

  await clickByID(el, "register__footer_form__submit_btn");

  await page.waitForTimeout(500);

  const lastName = await getByID(el, "last_name");

  await expect(lastName).toBeFocused();

  await clickByID(el, "btns_swapper_next_swap");

  await page.waitForTimeout(500);

  await expect(pwd).toBeFocused();

  await clickByID(el, "btns_swapper_prev_swap");
  await page.waitForTimeout(500);

  await expect(firstName).toBeFocused();
});
