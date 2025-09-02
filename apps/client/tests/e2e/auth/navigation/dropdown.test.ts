import test from "@playwright/test";
import { preAuthNavigation } from "./pre";
import { checkLinksList, clickByID, clickByTxt, getByID } from "../../lib/idx";
import { waitURL } from "../../lib/shortcuts/wait";

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
