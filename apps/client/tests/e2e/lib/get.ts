import { expect, Locator, Page } from "@playwright/test";
import { isShw } from "./check";

export const getByID = async (page: Page | Locator, id: string) => {
  const el = page.locator(`[data-testid='${id}']`);

  await el.waitFor({ state: "visible" });
  await isShw(el);

  await expect(el).toHaveCSS("opacity", "1", { timeout: 15000 });

  return el;
};
