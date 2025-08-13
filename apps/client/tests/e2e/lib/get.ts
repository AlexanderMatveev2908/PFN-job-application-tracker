import { expect, Locator, Page } from "@playwright/test";
import { isShw } from "./check";

export const getByID = async (loc: Page | Locator, id: string) => {
  const el = loc.locator(`[data-testid='${id}']`);

  await el.waitFor({ state: "visible" });
  await isShw(el);

  return el;
};

export const getByTxt = async (loc: Locator | Page, x: string) => {
  const el = loc.getByText(new RegExp(x, "i"));
  await el.first().waitFor({ state: "visible" });
  await expect(el.first()).toBeVisible();

  return el;
};
