import test from "@playwright/test";
import { clickByID, clickByTxt } from "../../lib/click";
import { getByID } from "../../lib/get";
import { checkLinksList } from "../../lib/check";
import { pre } from "./pre";

test("with dropdown", async ({ page }) => {
  await pre(page);

  await clickByID(page, "header__toggle_drop");

  const el = await getByID(page, "drop_menu_absolute__content");

  await checkLinksList(el, [
    "Home",
    "Register",
    "Login",
    "Recover Password",
    "Confirm Email",
  ]);

  await clickByTxt(el, "register");

  await page.waitForURL("/auth/register");
});
