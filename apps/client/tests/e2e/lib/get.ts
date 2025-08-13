import { Locator, Page } from "@playwright/test";
import { isShw } from "./check";

export const getByID = async (page: Page | Locator, id: string) => {
  const el = page.locator(`[data-testid='${id}']`);

  await el.waitFor({ state: "visible" });
  await isShw(el);

  return el;
};
