import { expect, Locator, Page } from "@playwright/test";

export const getByIDT = (page: Page, id: string) =>
  page.locator(`[data-testid='${id}']`);

export const lookTxt = async (page: Page, txt: string) => {
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

export const checkMsg = async (page: Page, x: string) => {
  await expect(page.getByText(new RegExp(x, "i"))).toBeVisible();
};

export const checkMsgList = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    await checkMsg(page, x);
  }
};

export const checkOpcMsgs = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    const txt = page.getByText(new RegExp(x, "i"));

    const hidOpc = await txt.evaluate((el) => {
      const own = parseFloat(getComputedStyle(el).opacity);
      if (!own) return true;

      let curr = el.parentElement;

      while (curr) {
        const s = getComputedStyle(curr);

        if (!parseFloat(s.opacity)) return true;

        curr = curr.parentElement;
      }

      return false;
    });

    expect(hidOpc).toBe(true);
  }
};
