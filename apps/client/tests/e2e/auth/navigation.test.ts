import test from "@playwright/test";
import {
  checkLinksList,
  checkTxt,
  clickByID,
  clickByTxt,
  getByID,
} from "../lib/idx";
import { closeToast } from "../lib/sideActions";

test.describe("navigation to register page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");

    await closeToast(page);

    await checkTxt(page, "Script worked ✌🏽");
  });

  test("with dropdown", async ({ page }) => {
    await clickByID(page, "header_toggle_drop");

    const el = await getByID(page, "drop_menu_absolute_content");

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

  test("with sidebar", async ({ page }) => {
    await clickByID(page, "header_toggle_sidebar");

    const el = await getByID(page, "sidebar");

    await checkLinksList(el, ["Home", "Applications", "Add application"]);

    await clickByID(el, "drop_menu_static_btn_toggle");

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
});
