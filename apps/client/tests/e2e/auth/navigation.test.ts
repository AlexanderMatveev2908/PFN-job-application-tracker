import test from "@playwright/test";
import { expectArgLinks, getByIDT, lookTxt, isShw } from "../lib/idx";

test.describe("navigation to register page", () => {
  test("with dropdown", async ({ page }) => {
    await page.goto("/");

    await lookTxt(page, "Script worked ✌🏽");

    await page.getByTestId("header_toggle_drop").click();

    const el = getByIDT(page, "drop_menu_absolute_content");

    await isShw(el);

    await expectArgLinks(el, [
      "Home",
      "Register",
      "Login",
      "Recover Password",
      "Confirm Email",
    ]);

    await el.getByRole("link", { name: "Register" }).click();

    await page.waitForURL("/auth/register");
  });

  test("with sidebar", async ({ page }) => {
    await page.goto("/");

    await lookTxt(page, "Script worked ✌🏽");

    await page.getByTestId("header_toggle_sidebar").click();

    const el = getByIDT(page, "sidebar");

    await isShw(el);

    await expectArgLinks(el, ["Home", "Applications", "Add application"]);

    await el.getByTestId("drop_menu_static_btn_toggle").click();

    await expectArgLinks(el, [
      "Home",
      "Register",
      "Login",
      "Recover Password",
      "Confirm Email",
    ]);

    await el.getByRole("link", { name: "Register" }).click();

    await page.waitForURL("/auth/register");
  });
});
