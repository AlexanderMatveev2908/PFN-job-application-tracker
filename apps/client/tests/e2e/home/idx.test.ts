import { test, expect } from "@playwright/test";

test("homepage loads", async ({ page }) => {
  await page.goto("/");

  await page.waitForSelector("text=Script worked ✌🏽");

  await expect(page.getByText("Script worked ✌🏽")).toBeVisible();
});
