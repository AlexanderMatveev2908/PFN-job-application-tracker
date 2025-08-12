import { expect, Locator, Page } from "@playwright/test";

export const getByIDT = (page: Page, id: string) =>
  page.locator(`[data-testid='${id}']`);

export const checkTxt = async (page: Page, txt: string) => {
  await page.waitForSelector(`text=${txt}`);
  await expect(page.locator(`text=${txt}`).first()).toBeVisible();
};

export const expectArgLinks = async (parent: Locator, arg: string[]) => {
  for (const name of arg)
    await expect(parent.getByRole("link", { name })).toBeVisible();
};

export const isShw = async (el: Locator) => {
  await expect(el).toBeVisible();
  await expect(el).toBeInViewport();
};
