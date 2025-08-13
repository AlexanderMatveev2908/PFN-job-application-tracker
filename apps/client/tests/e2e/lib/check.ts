import { expect, Locator, Page } from "@playwright/test";

export const checkTxt = async (page: Page, txt: string) => {
  await page.waitForSelector(`text=${txt}`);
  await expect(page.locator(`text=${txt}`).first()).toBeVisible();
};

export const checkLinksList = async (parent: Locator, arg: string[]) => {
  for (const name of arg)
    await expect(parent.getByRole("link", { name })).toBeVisible();
};

export const isShw = async (el: Locator) => {
  await el.waitFor({ state: "visible" });
  await expect(el).toBeVisible();
  await expect(el).toBeInViewport();
};

export const checkTxtReg = async (loc: Locator | Page, x: string) => {
  const el = loc.getByText(new RegExp(x, "i"));
  await el.waitFor({ state: "visible" });
  await expect(el).toBeVisible();

  return el;
};

export const checkTxtRegList = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    await checkTxtReg(page, x);
  }
};
