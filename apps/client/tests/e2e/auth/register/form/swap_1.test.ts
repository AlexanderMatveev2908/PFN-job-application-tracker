import test, { expect } from "@playwright/test";
import { getByID, getByTxt } from "../../../lib/get";
import { checkTxtList } from "../../../lib/check";
import { clickByID } from "../../../lib/click";
import { checkTxtOpc } from "../../../lib/style";
import { pre } from "./pre";

test("swap 1", async ({ page }) => {
  await pre(page);

  const el = await getByID(page, "register_form");

  await clickByID(el, "btns_swapper_next_swap");

  await page.waitForTimeout(500);

  const pwd = await getByID(el, "password");
  await expect(pwd).toBeFocused();

  const msgs = ["invalid password", "you must confirm password"];

  await pwd.fill("abc");

  await checkTxtList(page, msgs);

  const confPwd = await getByID(el, "confirm_password");

  await confPwd.fill("123");

  await getByTxt(page, "passwords do not match");

  await clickByID(el, "body__form_terms");
  await clickByID(el, "body__form_terms");

  const msg = "you must accept terms & conditions";

  await getByTxt(el, msg);

  await clickByID(el, "body__form_terms");

  await checkTxtOpc(page, msg);

  const btn = await getByID(el, "pwd_generator__btn");

  await btn.hover();

  await page.waitForTimeout(500);

  await getByTxt(page, "generate password");

  await btn.click();

  const resGen = await getByID(el, "pwd_generator__result");

  await resGen.click();

  await page.waitForTimeout(500);

  await getByTxt(page, "copied to clipboard");

  const content = await (
    await getByID(resGen, "cpy_paste__result")
  ).evaluate((x) => x.textContent);

  await pwd.fill(content!);
  await confPwd.fill(content!);

  await page.waitForTimeout(500);

  await checkTxtOpc(page, msgs[0]);
  await checkTxtOpc(page, "passwords do not match");

  await clickByID(el, "form_field_pwd__toggle_password");

  await expect(pwd).toHaveAttribute("type", "text");

  await clickByID(el, "form_field_pwd__toggle_confirm_password");

  await expect(pwd).toHaveAttribute("type", "password");
  await expect(confPwd).toHaveAttribute("type", "text");
});
