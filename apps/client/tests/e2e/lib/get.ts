import { Locator, Page } from "@playwright/test";
import { isShw } from "./check";

export const getByID = (page: Page | Locator, id: string) =>
  page.locator(`[data-testid='${id}']`);

export const getWithTByID = async (page: Page, id: string) => {
  const el = getByID(page, id);
  await el.waitFor({ state: "visible" });
  await isShw(el);

  return el;
};
