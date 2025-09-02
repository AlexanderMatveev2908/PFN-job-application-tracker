import test from "@playwright/test";
import { preAuthNavigation } from "./pre";
import {
  checkLinksList,
  clickByID,
  clickByTxt,
  getByID,
  waitURL,
} from "../../lib/idx";

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

  await waitURL(page, "/auth/register");
});
