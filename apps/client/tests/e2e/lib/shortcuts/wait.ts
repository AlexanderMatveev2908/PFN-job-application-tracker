import { Page } from "@playwright/test";

export const waitTmr = async (page: Page, v: number = 1500) => {
  await page.waitForTimeout(v);
};

export const waitURL = async (page: Page, url: string) => {
  await page.waitForURL(url, { timeout: 1000 * 100 });
};
