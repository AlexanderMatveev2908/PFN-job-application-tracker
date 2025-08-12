import test, { expect } from "@playwright/test";
import { expectArgLinks, getByIDT, getTxt } from "../lib/idx";

test("get to register page from home using dropdown", async ({ page }) => {
  await page.goto("/");

  await getTxt(page, "Script worked ✌🏽");

  await page.getByTestId("header_toggle_drop").click();

  const el = await getByIDT(page, "drop_menu_absolute_content");

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

test("get to register page from home using sidebar", async ({ page }) => {
  await page.goto("/");

  await getTxt(page, "Script worked ✌🏽");

  await page.getByTestId("header_toggle_sidebar").click();

  const el = await getByIDT(page, "sidebar");

  await expect(el).toBeInViewport();

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
