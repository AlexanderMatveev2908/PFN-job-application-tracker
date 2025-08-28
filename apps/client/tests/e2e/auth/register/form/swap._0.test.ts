import test from "@playwright/test";
import { checkTxtList } from "../../../lib/check";
import { checkTxtListOpc } from "../../../lib/style";
import { pre } from "./pre";

test("swap 0", async ({ page }) => {
  const el = await pre(page);

  await el.getByTestId("first_name").fill("<>!");
  await el.getByTestId("last_name").fill("...");
  await el.getByTestId("last_name").fill("");
  await el.getByTestId("email").fill("invalid@@@...");

  const msgs = ["invalid characters", "last name is required", "invalid email"];

  await page.waitForTimeout(1000);

  await checkTxtList(page, msgs);

  await el.getByTestId("first_name").fill("John");
  await el.getByTestId("last_name").fill("Doe");
  await el.getByTestId("email").fill("john@gmail.com");

  await page.waitForTimeout(1000);

  await checkTxtListOpc(page, msgs);
});
