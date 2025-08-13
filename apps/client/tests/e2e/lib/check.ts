import { expect, Locator, Page } from "@playwright/test";

export const checkTxt = async (loc: Locator | Page, x: string) => {
  const el = loc.getByText(new RegExp(x, "i"));
  await el.first().waitFor({ state: "visible" });
  await expect(el.first()).toBeVisible();

  return el;
};

export const checkTxtList = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    await checkTxt(page, x);
  }
};

export const checkLinksList = async (parent: Locator, arg: string[]) => {
  for (const name of arg) {
    const lk = parent.getByRole("link", { name });
    await lk.waitFor({ state: "visible" });

    await expect(lk).toBeVisible();
  }
};

export const isShw = async (el: Locator) => {
  await el.waitFor({ state: "visible" });
  await expect(el).toBeVisible();
  await expect(el).toBeInViewport();
};
