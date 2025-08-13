import { expect, Locator, Page } from "@playwright/test";
import { checkTxt } from "./check";

export const clickByID = async (page: Page, id: string) => {
  const el = page.getByTestId(id);
  await el.waitFor({ state: "visible" });

  await expect(el).toHaveCSS("opacity", "1", { timeout: 15000 });

  await el.click();
};

export const clickByTxt = async (el: Locator, txt: string) => {
  const elTxt = await checkTxt(el, txt);

  await elTxt.click();
};
