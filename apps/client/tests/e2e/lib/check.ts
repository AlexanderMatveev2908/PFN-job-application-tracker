import { expect, Locator, Page } from "@playwright/test";
import { getByTxt } from "./get";

export const checkTxtList = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    await getByTxt(page, x);
  }
};

export const checkLinksList = async (parent: Locator, arg: string[]) => {
  for (const name of arg) {
    const lk = parent.getByRole("link", { name });
    await lk.waitFor({ state: "visible", timeout: 5000 });

    await expect(lk).toBeVisible();
  }
};

export const isShw = async (el: Locator) => {
  await el.waitFor({ state: "visible", timeout: 5000 });
  await expect(el).toBeVisible();
  await expect(el).toBeInViewport();
};
