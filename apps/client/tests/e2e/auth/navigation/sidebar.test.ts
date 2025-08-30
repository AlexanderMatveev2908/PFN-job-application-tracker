import test from "@playwright/test";
import { clickByID, clickByTxt } from "../../lib/click";
import { getByID } from "../../lib/get";
import { checkLinksList } from "../../lib/check";
import { preAuthNavigation } from "./pre";

test("with sidebar", async ({ page }) => {
  await preAuthNavigation(page);

  await clickByID(page, "header__toggle_sidebar");

  const el = await getByID(page, "sidebar");

  await checkLinksList(el, ["Home", "Applications", "Add application"]);

  await clickByID(el, "drop_menu_static__btn_toggle");

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
