import test, { expect } from "@playwright/test";
import {
  checkTxtList,
  checkTxtListOpc,
  checkTxt,
  getByID,
  isShw,
} from "../lib/idx";

test.describe("form register", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/auth/register");

    await getByID(page, "register_form");
  });

  test("swap 0", async ({ page }) => {
    const el = await getByID(page, "register_form");

    await el.getByTestId("first_name").fill("<>!");
    await el.getByTestId("last_name").fill("...");
    await el.getByTestId("last_name").fill("");
    await el.getByTestId("email").fill("invalid@@@...");

    const msgs = [
      "invalid characters",
      "last name is required",
      "invalid email",
    ];

    await checkTxtList(page, msgs);

    await el.getByTestId("first_name").fill("John");
    await el.getByTestId("last_name").fill("Doe");
    await el.getByTestId("email").fill("john@gmail.com");

    await page.waitForTimeout(500);

    await checkTxtListOpc(page, msgs);
  });

  test("swap 1", async ({ page }) => {
    const el = await getByID(page, "register_form");

    await expect(page.getByTestId("btns_swapper_next_swap")).toBeVisible();
    await page.getByTestId("btns_swapper_next_swap").click();

    await page.waitForTimeout(500);

    const pwd = el.getByTestId("password");

    await expect(pwd).toBeVisible();
    await expect(pwd).toBeFocused();

    const msgs = ["invalid password", "you must confirm password"];

    await pwd.fill("abc");

    await checkTxtList(page, msgs);

    const confPwd = await el.getByTestId("confirm_password");
    await isShw(confPwd);

    await confPwd.fill("123");

    await checkTxt(page, "passwords do not match");
  });
});
