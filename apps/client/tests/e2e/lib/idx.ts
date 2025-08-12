import { expect, Locator, Page } from "@playwright/test";

export const getTxt = async (page: Page, txt: string) => {
  await page.waitForSelector(`text=${txt}`);
  await expect(page.locator(`text=${txt}`)).toBeVisible();
};

export const getLink = async (page: Page, txt: string) =>
  await expect(page.getByRole("link", { name: txt })).toBeVisible();

export const getByIDT = async (page: Page, id: string) =>
  await page.locator(`[data-testid='${id}']`);

export const expectArgLinks = async (parent: Locator, arg: string[]) => {
  for (const name of arg)
    await expect(parent.getByRole("link", { name })).toBeVisible();
};
