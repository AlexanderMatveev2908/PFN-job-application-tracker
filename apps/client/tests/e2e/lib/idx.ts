import { expect, Locator, Page } from "@playwright/test";

export const getByID = (page: Page | Locator, id: string) =>
  page.locator(`[data-testid='${id}']`);

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

export const checkTxtList = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    await checkTxtReg(page, x);
  }
};

export const clickByID = async (page: Page, id: string) => {
  const el = page.getByTestId(id);
  await el.waitFor({ state: "visible" });
  await el.click();
};

export const clickByTxt = async (el: Locator, txt: string) => {
  const elTxt = await checkTxtReg(el, txt);
  await elTxt.click();
};

export const getWithTByID = async (page: Page, id: string) => {
  const el = getByID(page, id);
  await el.waitFor({ state: "visible" });
  await isShw(el);

  return el;
};

export const checkTxtOpc = async (loc: Page | Locator, txt: string) => {
  const txtEl = loc.getByText(new RegExp(txt, "i"));

  return await txtEl.evaluate((el) => {
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
};

export const checkTxtListOpc = async (page: Page, msgs: string[]) => {
  for (const x of msgs) {
    const res = await checkTxtOpc(page, x);
    expect(res).toBe(true);
  }
};
