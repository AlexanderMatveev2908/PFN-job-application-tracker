import test from "@playwright/test";
import { clickByID, clickByTxt } from "../../lib/click";
import { getByID } from "../../lib/get";
import { checkLinksList } from "../../lib/check";
import { preAuthNavigation } from "./pre";
import { waitURL } from "../../lib/sideActions";

test("with dropdown", async ({ page }) => {
  await preAuthNavigation(page);

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

  await waitURL(page, "/auth/register");
});
