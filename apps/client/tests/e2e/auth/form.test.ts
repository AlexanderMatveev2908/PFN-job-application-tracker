import test, { expect } from "@playwright/test";
import { checkTxt, getByIDT, isShw } from "../lib/idx";

test.describe("form register", () => {
  test("swap 0", async ({ page }) => {
    await page.goto("/auth/register");

    await checkTxt(page, "Register");

    const el = getByIDT(page, "register_form");
    await isShw(el);

    await el.getByTestId("first_name").fill("<>!");
    await el.getByTestId("last_name").fill("...");
    await el.getByTestId("last_name").fill("");
    await el.getByTestId("email").fill("invalid@@@...");

    const msgs = [
      "invalid characters",
      "last name is required",
      "invalid email",
    ];

    for (const x of msgs) {
      await expect(page.getByText(new RegExp(x, "i"))).toBeVisible();
    }

    await el.getByTestId("first_name").fill("John");
    await el.getByTestId("last_name").fill("Doe");
    await el.getByTestId("email").fill("john@gmail.com");

    await page.waitForTimeout(500);

    await page.pause();

    for (const x of msgs) {
      const txt = page.getByText(new RegExp(x, "i"));

      const parentOpc = await txt.evaluate((el) => {
        let current = el.parentElement;

        while (current) {
          const style = window.getComputedStyle(current);

          if (style.opacity === "0") return true;

          current = current.parentElement;
        }

        return false;
      });

      expect(parentOpc).toBe(true);
    }
  });
});
