import { expect, Locator, Page } from "@playwright/test";

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
