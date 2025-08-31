import { Page } from "@playwright/test";
import { clickByID } from "./click";
import { getByID } from "./get";

export const closeToast = async (page: Page): Promise<undefined> => {
  try {
    const toast = await getByID(page, "toast");

    if (toast) await clickByID(toast, "toast__close_btn");
  } catch {}
};

export const waitTest = async (page: Page, v: number = 1000) => {
  await page.waitForTimeout(v);
};

export const waitURL = async (page: Page, url: string) => {
  await page.waitForURL(url, { timeout: 10000 });
};
