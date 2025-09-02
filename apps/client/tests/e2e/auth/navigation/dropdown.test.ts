import test from "@playwright/test";
import { preAuthNavigation } from "./pre";
import {
  checkLinksList,
  clickByID,
  clickByTxt,
  getByID,
  waitURL,
} from "../../lib/idx";

test("with dropdown", async ({ page }) => {
  await preAuthNavigation(page);

  await clickByID(page, "header__toggle_drop");

  const el = await getByID(page, "drop_menu_absolute__content");

  await checkLinksList(el, [
    "Register",
    "Login",
    "Recover Password",
    "Confirm Email",
  ]);

  await clickByTxt(el, "register");

  await waitURL(page, "/auth/register");
});
